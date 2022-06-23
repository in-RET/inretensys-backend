import os.path
import time
from pickle import load

import pandas as pd
from oemof import solph

from InRetEnsys import InRetEnsysEnergysystem
from InRetEnsys.types import Constraints, Frequencies, Solver
from hsncommon.log import HsnLogger

logger = HsnLogger()


##  Init Modelbuilder, load and optimise the configuration.
#
#   @param ConfigFile Path to the Configfile which contains the EnsysConfiguration
#   @param DumpFile Path to the Dumpfile where the oemof-energysystem and the results should be stored.
class ModelBuilder:
    def __init__(self,
                 ConfigFile: str,
                 DumpFile: str
                 ) -> None:
        xf = open(ConfigFile, 'rb')
        model = load(xf)
        xf.close()

        if model.solver is Solver.gurobi:
            solver = 'gurobi'
        elif model.solver is Solver.gurobi_direct:
            solver = 'gurobi_direct'
        elif model.solver is Solver.cbc:
            solver = 'cbc'
        elif model.solver is Solver.glpk:
            solver = 'glpk'
        elif model.solver is Solver.cplex:
            solver = 'cplex'
        else:
            solver = 'gurobi'

        BuildEnergySystem(model.energysystem, DumpFile, solver, model.solver_verbose)


##  Build an energysystem from the config.
#
#   @param es energysystem from the binary config file
#   @param file filename of the final dumpfile
#   @param solver Solver to use for optimisation in Pyomo
#   @param solver_verbose Should the Solver print the output
def BuildEnergySystem(es: InRetEnsysEnergysystem, file: str, solver: str, solver_verbose: bool):
    logger.info("Build an Energysystem from config file.")
    filename = os.path.basename(file)
    wdir = os.path.dirname(file)

    if es.frequenz is Frequencies.quarter_hourly:
        freq = "15min"
    elif es.frequenz is Frequencies.half_hourly:
        freq = "15min"
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
            logger.info("Build " + attr)

            arg_value = getattr(es, attr)

            for value in arg_value:
                oemof_obj = value.to_oemof(oemof_es)

                if oemof_obj is not None:
                    oemof_es.add(oemof_obj)

    logger.info("Build completed.")

    ##########################################################################
    # Print the EnergySystem as Graph
    ##########################################################################
    filepath = "images/energy_system"
    logger.info("Print energysystem as graph")

    ##########################################################################
    # Initiate the energy system model
    ##########################################################################
    logger.info("Initiate the energy system model.")
    model = solph.Model(oemof_es)

    ##########################################################################
    # Add Constraints to the model
    ##########################################################################
    if hasattr(es, "constraints"):
        for constraint in es.constraints:
            kwargs = constraint.to_oemof()

            if constraint.typ == Constraints.shared_limit:
                solph.constraints.shared_limit(model=model, **kwargs)

            elif constraint.typ == Constraints.investment_limit:
                model = solph.constraints.investment_limit(model=model, **kwargs)

            elif constraint.typ == Constraints.additional_investment_flow_limit:
                model = solph.constraints.additional_investment_flow_limit(model=model, **kwargs)

            elif constraint.typ == Constraints.generic_integral_limit:
                model = solph.constraints.generic_integral_limit(om=model, **kwargs)

            elif constraint.typ == Constraints.emission_limit:
                solph.constraints.emission_limit(om=model, **kwargs)

            elif constraint.typ == Constraints.limit_active_flow_count:
                model = solph.constraints.limit_active_flow_count(model=model, **kwargs)

            elif constraint.typ == Constraints.limit_active_flow_count_by_keyword:
                model = solph.constraints.limit_active_flow_count_by_keyword(model=model, **kwargs)

            elif constraint.typ == Constraints.equate_variables:
                solph.constraints.equate_variables(model=model, **kwargs)

    ##########################################################################
    # solving...
    ##########################################################################
    logger.info("Solve the optimization problem.")
    t_start = time.time()
    model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})
    t_end = time.time()

    logger.info("Completed after " + str(round(t_end - t_start, 2)) + " seconds.")

    logger.info("Store the energy system with the results.")

    ##########################################################################
    # The processing module of the outputlib can be used to extract the results
    # from the model transfer them into a homogeneous structured dictionary.
    ##########################################################################
    oemof_es.results["main"] = solph.processing.results(model)
    oemof_es.results["meta"] = solph.processing.meta_results(model)
    oemof_es.results["verification"] = solph.processing.create_dataframe(model)

    logger.info("Dump file with results to: " + os.path.join(wdir, filename))

    if not os.path.exists(wdir):
        os.makedirs(wdir)

    oemof_es.dump(dpath=wdir, filename=filename)
    logger.info("Fin.")
