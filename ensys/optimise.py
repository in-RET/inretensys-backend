import logging
import os.path

from oemof import solph


def EnsysOptimise(file, solver="cbc"):
    ##########################################################################
    # Optimise the energy system
    ##########################################################################

    wdir = os.path.dirname(file)
    filename = os.path.basename(file)

    oemof_es = solph.EnergySystem()
    oemof_es.restore(dpath=wdir, filename=filename)

    logging.info("Optimise the energy system")

    # initialise the operational model
    model = solph.Model(oemof_es)

    solver_verbose = False

    # if tee_switch is true solver messages will be displayed
    logging.info("Solve the optimization problem")
    model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

    logging.info("Store the energy system with the results.")

    # The processing module of the outputlib can be used to extract the results
    # from the model transfer them into a homogeneous structured dictionary.

    # add results to the energy system to make it possible to store them.
    oemof_es.results["main"] = solph.processing.results(model)
    oemof_es.results["meta"] = solph.processing.meta_results(model)

    oemof_es.dump(dpath=wdir, filename=filename)
