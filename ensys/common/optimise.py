import os.path
import time

from oemof import solph
from oemof_visio import ESGraphRenderer

from hsncommon.log import HsnLogger


def EnsysOptimise(file, solver="gurobi", solver_verbose=False):
    logger = HsnLogger()

    wdir = os.path.dirname(file)
    filename = os.path.basename(file)

    oemof_es = solph.EnergySystem()
    oemof_es.restore(dpath=wdir, filename=filename)

    ##########################################################################
    # Print the EnergySystem as Graph
    ##########################################################################
    filepath = "images/energy_system"
    logger.info("Print energysystem as graph")

    gr = ESGraphRenderer(energy_system=oemof_es, filepath=filepath)
    # gr.view()

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################
    logger.info("Optimise the energy system")

    # initialise the operational model
    model = solph.Model(oemof_es)

    # if tee_switch is true solver messages will be displayed
    logger.info("Solve the optimization problem")
    t_start = time.time()
    model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})
    t_end = time.time()

    logger.info("Completed after " + str(round(t_end - t_start, 2)) + " seconds.")

    logger.info("Store the energy system with the results.")

    # The processing module of the outputlib can be used to extract the results
    # from the model transfer them into a homogeneous structured dictionary.

    # add results to the energy system to make it possible to store them.
    oemof_es.results["main"] = solph.processing.results(model)
    oemof_es.results["meta"] = solph.processing.meta_results(model)

    logger.info("Dump file with results to: " + os.path.join(wdir, filename))
    # store energy system with results

    oemof_es.dump(dpath=wdir, filename=filename)
    logger.info("Fin.")
