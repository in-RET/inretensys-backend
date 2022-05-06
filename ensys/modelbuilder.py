import os.path

from pickle import load
from oemof import solph

from ensys import EnsysFlow, EnsysOptimise
from hsncommon.log import HsnLogger

logger = HsnLogger()


class ModelBuilder:
    def __init__(self,
                 ConfigFile,
                 DumpFile,
                 BuildModel=True,
                 Optimise=True
                 ):
        if BuildModel:
            xf = open(ConfigFile, 'rb')
            es = load(xf)
            xf.close()

            BuildEnergySystem(es, DumpFile)

        if Optimise:
            EnsysOptimise(DumpFile)


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

    logger.info("Building completed. Dump to file.")
    oemof_es.dump(dpath=wdir, filename=filename)
