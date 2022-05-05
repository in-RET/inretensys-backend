import os.path
import time

from oemof import solph
from oemof_visio import ESGraphRenderer

from ensys import EnsysFlow, PrintResultsFromDump
from hsncommon.log import HsnLogger

logger = HsnLogger()


class ModelBuilder:

    def __init__(self, ConfigFile, DumpFile):
        es = BuildConfiguration(ConfigFile)
        BuildEnergySystem(es, DumpFile)


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


def BuildOemofKwargs(ensys_obj, oemof_es: solph.EnergySystem):
    kwargs = {}

    args = vars(ensys_obj)

    for key in args:
        value = args[key]
        if value is not None:
            if key == "inputs" or key == "outputs" or key == "conversion_factors":
                kwargs[key] = BuildIO(value, oemof_es)
            elif key == "nonconvex":
                if value is False or value is True:
                    kwargs[key] = value
                else:
                    kwargs[key] = value.to_oemof()
            elif key == "investment":
                if type(value) is solph.Investment:
                    kwargs[key] = value
                else:
                    kwargs[key] = value.to_oemof()
            else:
                kwargs[key] = value

    return kwargs


def BuildConfiguration(filename):
    from pickle import load

    xf = open(filename, 'rb')
    es = load(xf)
    xf.close()

    return es


def BuildEnergySystem(es, file):
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

    if hasattr(es, "busses"):
        logger.info("Build busses")
        for bus in es.busses:
            if type(bus) is solph.Bus:
                oemof_es.add(bus)
            else:
                kwargs = BuildOemofKwargs(bus, oemof_es)
                oemof_bus = solph.Bus(**kwargs)
                oemof_es.add(oemof_bus)

    if hasattr(es, "sources"):
        logger.info("Build sources")
        # Add sources to the EnergySystem
        for source in es.sources:
            if type(source) is solph.Source:
                oemof_es.add(source)
            else:
                kwargs = BuildOemofKwargs(source, oemof_es)
                oemof_source = solph.Source(**kwargs)

                oemof_es.add(oemof_source)

    if hasattr(es, "sinks"):
        logger.info("Build sinks")
        # Add sinks to the EnergySystem
        for sink in es.sinks:
            if type(sink) is solph.Sink:
                oemof_es.add(sink)
            else:
                kwargs = BuildOemofKwargs(sink, oemof_es)
                oemof_sink = solph.Sink(**kwargs)

                oemof_es.add(oemof_sink)

    if hasattr(es, "transformers"):
        logger.info("Build transformers")
        # Add transformers to the EnergySystem
        for transformer in es.transformers:
            if type(transformer) is solph.Transformer:
                oemof_es.add(transformer)
            else:
                kwargs = BuildOemofKwargs(transformer, oemof_es)
                oemof_transformer = solph.Transformer(**kwargs)

                oemof_es.add(oemof_transformer)

    if hasattr(es, "storages"):
        logger.info("Build storages")
        # Add storages to the EnergySystem
        for storage in es.storages:
            if type(storage) is solph.GenericStorage:
                oemof_es.add(storage)
            else:
                kwargs = BuildOemofKwargs(storage, oemof_es)

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
    model.solve(solver="gurobi", solve_kwargs={"tee": solver_verbose})
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

    # Todo: Hier ist ein böser export fehler!! Irgendwas mit pickle und pydantic -- son mist
    # xf = open(os.path.join(wdir, filename), 'wb')
    oemof_es.dump(dpath=wdir, filename=filename)
    # xf.close()
    # oemof_es.dump(dpath=wdir, filename=filename)
    logger.info("Fin.")

    PrintResultsFromDump(output=os.path.join(os.getcwd(), "output", "ensys_out"), energysystem=oemof_es)








