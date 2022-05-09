import os.path
import time
from pickle import load

from oemof import solph
from oemof_visio import ESGraphRenderer

from ensys import EnsysFlow, EnsysBus, EnsysSource, EnsysSink, EnsysTransformer, EnsysStorage
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


def SearchNode(nodeslist, nodename):
    """Search a specific node in  list and return this Node."""
    for node in nodeslist:
        if node.label == nodename:
            return nodeslist[nodeslist.index(node)]

    return None


def BuildIO(ensys_io, es):
    """Build Input/Output-Dicts for oemof-Objects."""
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
    """Build a dict of arguments for the init of the oemof objects."""
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

    except_vars = ["label", "timeindex", "timeincrement"]
    oemof_types = [solph.Bus, solph.GenericStorage, solph.Sink, solph.Source, solph.Transformer]

    for attr in vars(es):
        if attr not in except_vars:
            logger.info("Build " + attr)

            arg_value = getattr(es, attr)

            for value in arg_value:
                if type(value) in oemof_types:
                    oemof_es.add(arg_value)
                else:
                    kwargs = BuildOemofKwargs(value, oemof_es)

                    if type(value) == EnsysBus:
                        oemof_obj = solph.Bus(**kwargs)
                    elif type(value) == EnsysSource:
                        oemof_obj = solph.Source(**kwargs)
                    elif type(value) == EnsysSink:
                        oemof_obj = solph.Sink(**kwargs)
                    elif type(value) == EnsysTransformer:
                        oemof_obj = solph.Transformer(**kwargs)
                    elif type(value) == EnsysStorage:
                        oemof_obj = solph.GenericStorage(**kwargs)
                    else:
                        oemof_obj = None

                    if oemof_obj is not None:
                        oemof_es.add(oemof_obj)

    logger.info("Building completed.")

    ##########################################################################
    # Print the EnergySystem as Graph
    ##########################################################################
    filepath = "images/energy_system"
    logger.info("Print energysystem as graph")

    ESGraphRenderer(energy_system=oemof_es, filepath=filepath)

    ##########################################################################
    # Initiate the energy system model
    ##########################################################################
    logger.info("Initiate the energy system model.")
    model = solph.Model(oemof_es)

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

    oemof_es.dump(dpath=wdir, filename=filename)
    logger.info("Fin.")
