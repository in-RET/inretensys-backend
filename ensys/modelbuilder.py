import os.path
import time
from pickle import load

from oemof import solph
from oemof_visio import ESGraphRenderer

from ensys.types import CONSTRAINT_TYPES
from hsncommon.log import HsnLogger

logger = HsnLogger()


class ModelBuilder:
    def __init__(self,
                 ConfigFile,
                 DumpFile,
                 ):
        """Init Modelbuilder and if given load and optimise the configuration."""
        xf = open(ConfigFile, 'rb')
        es = load(xf)
        xf.close()

        BuildEnergySystem(es, DumpFile)


# gurobi direct wegen exce not found
def BuildEnergySystem(es, file, solver="gurobi", solver_verbose=False):
    ##########################################################################
    # Build an Energysystem from the config
    ##########################################################################
    logger.info("Build an Energysystem from config file.")
    filename = os.path.basename(file)
    wdir = os.path.dirname(file)

    oemof_es = solph.EnergySystem(
        label=es.label,
        timeindex=es.timeindex,
        timeincrement=es.timeincrement
    )

    except_vars = ["label", "timeindex", "timeincrement", "constraints"]

    for attr in vars(es):
        if attr not in except_vars:
            logger.info("Build " + attr)

            arg_value = getattr(es, attr)

            for value in arg_value:
                oemof_obj = value.to_oemof(oemof_es)

                if oemof_obj is not None:
                    oemof_es.add(oemof_obj)

    logger.info("Building completed.")

    ##########################################################################
    # Print the EnergySystem as Graph
    ##########################################################################
    filepath = "images/energy_system"
    logger.info("Print energysystem as graph")

    gr = ESGraphRenderer(energy_system=oemof_es, filepath=filepath)
    gr.view()

    ##########################################################################
    # Initiate the energy system model
    ##########################################################################
    logger.info("Initiate the energy system model.")
    model = solph.Model(oemof_es)

    ##########################################################################
    # Add Constraints to the model
    ##########################################################################
    constraints = es.constraints

    if constraints is not None:
        for constraint in constraints:
            kwargs = constraint.to_oemof()

            if constraint.typ == CONSTRAINT_TYPES.shared_limit:
                solph.constraints.shared_limit(model=model, **kwargs)

            elif constraint.typ == CONSTRAINT_TYPES.investment_limit:
                model = solph.constraints.investment_limit(model=model, **kwargs)

            elif constraint.typ == CONSTRAINT_TYPES.additional_investment_flow_limit:
                model = solph.constraints.additional_investment_flow_limit(model=model, **kwargs)

            elif constraint.typ == CONSTRAINT_TYPES.generic_integral_limit:
                model = solph.constraints.generic_integral_limit(om=model, **kwargs)

            elif constraint.typ == CONSTRAINT_TYPES.emission_limit:
                solph.constraints.emission_limit(om=model, **kwargs)

            elif constraint.typ == CONSTRAINT_TYPES.limit_active_flow_count:
                model = solph.constraints.limit_active_flow_count(model=model, **kwargs)

            elif constraint.typ == CONSTRAINT_TYPES.limit_active_flow_count_by_keyword:
                model = solph.constraints.limit_active_flow_count_by_keyword(model=model, **kwargs)

            elif constraint.typ == CONSTRAINT_TYPES.equate_variables:
                solph.constraints.equate_variables(model=model, **kwargs)

            else:
                # do nothing
                pass

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

    print(model.integral_limit_emission_factor())

    logger.info("Dump file with results to: " + os.path.join(wdir, filename))

    oemof_es.dump(dpath=wdir, filename=filename)
    logger.info("Fin.")
