import json
import os.path
import pickle
import time
from typing import Dict

import gurobipy as gp
import pandas as pd
import pyomo.environ as pyoenv
from gurobipy import GRB
from InRetEnsys import InRetEnsysEnergysystem, InRetEnsysModel
from InRetEnsys.callback import SolverCallback, persistentSolverCallback
from InRetEnsys.common.log import InRetEnsysLogger
from InRetEnsys.types import Constraints, Frequencies, Solver
from oemof import solph
from pyrsistent import v


##  Init Modelbuilder, load and optimise the configuration.
#
#   @param ConfigFile Path to the Configfile which contains the EnsysConfiguration
#   @param DumpFile Path to the Dumpfile where the oemof-energysystem and the results should be stored.
class ModelBuilder:
    WORKING_DIRECTORY = os.getcwd()
    LOGGING_DIRECTORY = os.path.join(WORKING_DIRECTORY, "logs")
    DUMPING_DIRECTORY = os.path.join(WORKING_DIRECTORY, "dumps")
    
    def __init__(self,
                 ConfigFile: str,
                 DumpFile: str,
                 wdir: str, 
                 logdir: str,
                 dumpdir: str,
                 only_lp: bool = False
                 ) -> None:

        self.WORKING_DIRECTORY = os.path.join(os.getcwd(), wdir)
        if not os.path.exists(self.WORKING_DIRECTORY):
            os.makedirs(self.WORKING_DIRECTORY)

        self.LOGGING_DIRECTORY = logdir
        if not os.path.exists(self.LOGGING_DIRECTORY):
            os.makedirs(self.LOGGING_DIRECTORY)
        
        self.DUMPING_DIRECTORY = dumpdir
        if not os.path.exists(self.DUMPING_DIRECTORY):
            os.makedirs(self.DUMPING_DIRECTORY)

        # handle various filetypes 
        if ConfigFile.find(".json") > 0:
            xf = open(ConfigFile, 'rt')
            model_dict = json.load(xf)
            model = InRetEnsysModel(**model_dict)
            xf.close()
        elif ConfigFile.find(".bin") > 0:
            xf = open(ConfigFile, 'rb')
            model = pickle.load(xf)
            xf.close()
        else:
            raise Exception("Fileformat is not valid!")       


        logfile = os.path.basename(ConfigFile)
        if logfile.find(".json") > 0:
            logfile = os.path.join(self.LOGGING_DIRECTORY, logfile.replace(".json", ".log"))
        elif logfile.find(".bin") > 0:
            logfile = os.path.join(self.LOGGING_DIRECTORY, logfile.replace(".bin", ".log"))
        else:
            raise Exception("Fileformat is not valid!")

        InRetEnsysLogger.info("Start Building and solving")

        if hasattr(model, "solver_kwargs"):
            cmdline_opts = model.solver_kwargs
        else:
            cmdline_opts = {}

        self.BuildEnergySystem(model.energysystem, DumpFile, model.solver, model.solver_verbose, cmdline_opts=cmdline_opts, only_lp=only_lp)

    ##  Build an energysystem from the config.
    #
    #   @param es energysystem from the binary config file
    #   @param file filename of the final dumpfile
    #   @param solver Solver to use for optimisation in Pyomo
    #   @param solver_verbose Should the Solver print the output
    def BuildEnergySystem(self, es: InRetEnsysEnergysystem, file: str, solver: Solver, solver_verbose: bool, cmdline_opts: dict, only_lp: bool):
        InRetEnsysLogger.info("Build an Energysystem from config file.")
        filename = os.path.basename(file)

        ##########################################################################
        # Build the oemof-energysystem
        ##########################################################################
        if es.frequenz is Frequencies.quarter_hourly:
            freq = "15min"
        elif es.frequenz is Frequencies.half_hourly:
            freq = "30min"
        elif es.frequenz is Frequencies.hourly:
            freq = "H"
        elif es.frequenz is Frequencies.daily:
            freq = "D"
        elif es.frequenz is Frequencies.weekly:
            freq = "7D"
        elif es.frequenz is Frequencies.monthly:
            freq = "M"
        else:
            freq = "H"

        timeindex = pd.date_range(start=es.start_date,
                                periods=es.time_steps,
                                freq=freq)

        oemof_es = solph.EnergySystem(
            timeindex=timeindex
        )

        except_vars = ["label", "start_date", "time_steps", "frequenz", "constraints"]
        
        for attr in vars(es):
            if attr not in except_vars:
                InRetEnsysLogger.info("Build " + attr)

                arg_value = getattr(es, attr)

                for value in arg_value:
                    oemof_obj = value.to_oemof(oemof_es)

                    if oemof_obj is not None:
                        oemof_es.add(oemof_obj)

        InRetEnsysLogger.info("Build completed.")

        ##########################################################################
        # Initiate the energy system model
        ##########################################################################
        InRetEnsysLogger.info("Initiate the energy system model.")
        model = solph.Model(oemof_es)

        ##########################################################################
        # Add Constraints to the model
        ##########################################################################
        if hasattr(es, "constraints"):
            for constr in es.constraints:
                kwargs = constr.to_oemof()

                if constr.typ == Constraints.shared_limit:
                    solph.constraints.shared_limit(model=model, **kwargs)

                elif constr.typ == Constraints.investment_limit:
                    model = solph.constraints.investment_limit(model=model, **kwargs)

                elif constr.typ == Constraints.additional_investment_flow_limit:
                    model = solph.constraints.additional_investment_flow_limit(model=model, **kwargs)

                elif constr.typ == Constraints.generic_integral_limit:
                    model = solph.constraints.generic_integral_limit(om=model, **kwargs)

                elif constr.typ == Constraints.emission_limit:
                    solph.constraints.emission_limit(om=model, **kwargs)

                elif constr.typ == Constraints.limit_active_flow_count:
                    model = solph.constraints.limit_active_flow_count(model=model, **kwargs)

                elif constr.typ == Constraints.limit_active_flow_count_by_keyword:
                    model = solph.constraints.limit_active_flow_count_by_keyword(model=model, **kwargs)

                elif constr.typ == Constraints.equate_variables:
                    solph.constraints.equate_variables(model=model, **kwargs)
        
        ### Create Logfile for Solver
        logfile = os.path.join(self.LOGGING_DIRECTORY, filename.replace(".dump", "_solver.log"))
        InRetEnsysLogger.info("Logfile: " + self.LOGGING_DIRECTORY)
        
        ### Store LP files
        lp_filename = os.path.join(self.DUMPING_DIRECTORY, filename.replace(".dump", ".lp"))
        
        InRetEnsysLogger.info("Store lp-file in {0}.".format(lp_filename))
        model.write(lp_filename, io_options={"symbolic_solver_labels": True})
        ### Set Environmental Variables for the solver
        # map kwargs for pyomo.enviroment and later usage
        solve_kwargs = {"tee": solver_verbose}
        cmdline_opts["logfile"] = logfile
        
        if not only_lp:
            ##########################################################################
            # solving...
            ##########################################################################
            InRetEnsysLogger.info("Solve the optimization problem.")
            
            t_start = time.time()

            if False: #solver == Solver.gurobi_persistent: 
                # create optimizer with pyomo.environment
                opt = pyoenv.SolverFactory(solver.value, solver_io='lp')

                # set command line options
                options = opt.options
                for k in cmdline_opts:
                    options[k] = cmdline_opts[k]

                opt.set_instance(model)
                opt.set_callback(persistentSolverCallback)
                solver_results = opt.solve(**solve_kwargs)

                model.es.results = solver_results

            elif False: # solver == Solver.gurobi
                gp_model = gp.read(lp_filename)

                gp_model._lastiter = -GRB.INFINITY
                gp_model._lastnode = -GRB.INFINITY
                gp_model._logfile = logfile
                gp_model._vars = gp_model.getVars()

                solver_results = gp_model.optimize(SolverCallback)

                model.es.results = solver_results

                json_filename = os.path.join(self.DUMPING_DIRECTORY, filename.replace(".dump", ".json"))
                InRetEnsysLogger.info("Store json-file in {0}.".format(json_filename))
                gp_model.write(json_filename)

            else:
                model.solve(solver=solver.value,
                            solve_kwargs=solve_kwargs,
                            cmdline_options=cmdline_opts)
            
            t_end = time.time()
            
            InRetEnsysLogger.info("Completed after " + str(round(t_end - t_start, 2)) + " seconds.")
            InRetEnsysLogger.info("Store the energy system with the results.")

            ##########################################################################
            # The processing module of the outputlib can be used to extract the results
            # from the model transfer them into a homogeneous structured dictionary.
            ##########################################################################
            oemof_es.results["main"] = solph.processing.results(model)
            oemof_es.results["meta"] = solph.processing.meta_results(model)
            oemof_es.results["verification"] = solph.processing.create_dataframe(model)
            
            InRetEnsysLogger.info("Dump file with results to: " + os.path.join(self.DUMPING_DIRECTORY, filename))

            oemof_es.dump(dpath=self.DUMPING_DIRECTORY, filename=filename)
            InRetEnsysLogger.info("Fin.")
