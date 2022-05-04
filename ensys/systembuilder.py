import os.path
import time

from oemof import solph
from oemof_visio import ESGraphRenderer

from ensys import EnsysFlow
from hsncommon import config
from hsncommon.log import HsnLogger


def SearchNode(nodeslist, nodename):
    for node in nodeslist:
        if node.label == nodename:
            return nodeslist[nodeslist.index(node)]

    return None


def BuildIO(ensys_io, es):
    oemof_io = {}
    keys = list(ensys_io.keys())

    for key in keys:
        for node in es.nodes:
            if node.label == key:
                bus = es.nodes[es.nodes.index(node)]
                if type(ensys_io[key]) is EnsysFlow:
                    oemof_io[bus] = ensys_io[key].to_oemof()
                else:
                    oemof_io[bus] = ensys_io[key]

    return oemof_io


def BuildKwargs(ensys_obj, oemof_es: solph.EnergySystem):
    kwargs = {}

    for attr_name in dir(ensys_obj):
        if not attr_name.startswith("__") and \
                not attr_name.startswith("to_") and \
                not attr_name == "format":
            name = attr_name
            value = getattr(ensys_obj, attr_name)

            if name == "inputs" or name == "outputs" or name == "conversion_factors":
                kwargs[name] = BuildIO(value, oemof_es)
            elif name == "nonconvex":
                if value is False or value is True:
                    kwargs[name] = value
                else:
                    kwargs[name] = value.to_oemof()
            elif name == "investment":
                if type(value) is solph.Investment:
                    kwargs[name] = value
                else:
                    kwargs[name] = value.to_oemof()
            else:
                kwargs[name] = value

    return kwargs


def BuildConfiguration(filename):
    es = config.config_object_from_file(filename)
    return es


def BuildEnergySystem(es, file):
    ##########################################################################
    # Build an Energysystem from the config
    ##########################################################################
    logger = HsnLogger()

    logger.info("Build an Energysystem from config file.")
    filename = os.path.basename(file)
    wdir = os.path.dirname(file)

    oemof_es = solph.EnergySystem(
        label=es.label,
        timeindex=es.timeindex,
        timeincrement=es.timeincrement
    )

    if hasattr(es, "busses"):
        logger.info("Build busses")
        for bus in es.busses:
            if type(bus) is solph.Bus:
                oemof_es.add(bus)
            else:
                kwargs = BuildKwargs(bus, oemof_es)
                oemof_bus = solph.Bus(**kwargs)
                oemof_es.add(oemof_bus)

    if hasattr(es, "sources"):
        logger.info("Build sources")
        # Add sources to the EnergySystem
        for source in es.sources:
            if type(source) is solph.Source:
                oemof_es.add(source)
            else:
                kwargs = BuildKwargs(source, oemof_es)
                oemof_source = solph.Source(**kwargs)

                oemof_es.add(oemof_source)

    if hasattr(es, "sinks"):
        logger.info("Build sinks")
        # Add sinks to the EnergySystem
        for sink in es.sinks:
            if type(sink) is solph.Sink:
                oemof_es.add(sink)
            else:
                kwargs = BuildKwargs(sink, oemof_es)
                oemof_sink = solph.Sink(**kwargs)

                oemof_es.add(oemof_sink)

    if hasattr(es, "transformers"):
        logger.info("Build transformers")
        # Add transformers to the EnergySystem
        for transformer in es.transformers:
            if type(transformer) is solph.Transformer:
                oemof_es.add(transformer)
            else:
                kwargs = BuildKwargs(transformer, oemof_es)
                oemof_transformer = solph.Transformer(**kwargs)

                oemof_es.add(oemof_transformer)

    if hasattr(es, "storages"):
        logger.info("Build storages")
        # Add storages to the EnergySystem
        for storage in es.storages:
            if type(storage) is solph.GenericStorage:
                oemof_es.add(storage)
            else:
                kwargs = BuildKwargs(storage, oemof_es)

                oemof_storage = solph.GenericStorage(**kwargs)
                oemof_es.add(oemof_storage)

    ##########################################################################
    # Print the EnergySystem as Graph
    ##########################################################################
    filepath = "images/energy_system"
    logger.info("Print energysystem as graph")

    gr = ESGraphRenderer(energy_system=oemof_es, filepath=filepath)
    #gr.view()

    # oemof_es.dump(dpath=wdir, filename=filename)

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################
    logger.info("Optimise the energy system")

    # initialise the operational model
    model = solph.Model(oemof_es)

    solver_verbose = False

    # if tee_switch is true solver messages will be displayed
    logger.info("Solve the optimization problem")
    t_start = time.time()
    model.solve(solver="cbc", solve_kwargs={"tee": solver_verbose})
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
