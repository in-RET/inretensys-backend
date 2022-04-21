import logging
import os.path
import ensys

from oemof import solph
from oemof_visio import ESGraphRenderer
from hsncommon import config


def findUsedBus(name, busses):
    usedBus = None

    for bus in busses:
        if bus.label == name:
            usedBus = bus

    return usedBus


def buildIOFlows(target, possibleBusses):
    if target is None:
        return None

    busses = list(target.keys())
    usedBusses = []

    for bus in busses:
        usedBusses.append(findUsedBus(bus, possibleBusses))

    IOFlows = {}
    for usedBus in usedBusses:
        if type(target[usedBus.label]) == ensys.EnsysFlow:
            IOFlows[usedBus] = target[usedBus.label].to_oemof()
        else:
            IOFlows[usedBus] = target[usedBus.label]

    return IOFlows


class EnsysSystembuilder():
    def __init__(self):
        pass

    def BuildConfiguration(self, filename):
        es = config.config_object_from_file(filename)
        return es

    def BuildEnergySystem(self, es, file):
        ##########################################################################
        # Build an Energysystem from the config
        ##########################################################################
        filename = os.path.basename(file)
        wdir = os.path.dirname(file)

        oemof_es = solph.EnergySystem(
            label=es.label,
            timeindex=es.timeindex,
            timeincrement=es.timeincrement
        )

        # add busses to an EnergySystem
        oemof_busses = []

        for bus in es.busses:
            oemof_bus = solph.Bus(
                label=bus.label,
                balanced=bus.balanced
            )
            oemof_es.add(oemof_bus)
            # create a better solution to get the possible Busses
            oemof_busses.append(oemof_bus)

        # Add sources to the EnergySystem
        for source in es.sources:
            oemof_source = solph.Source(
                label=source.label,
                outputs=buildIOFlows(source.outputs, oemof_busses),
            )
            oemof_es.add(oemof_source)

        # Add sinks to the EnergySystem
        for sink in es.sinks:
            oemof_sink = solph.Sink(
                label=sink.label,
                inputs=buildIOFlows(sink.inputs, oemof_busses),
            )
            oemof_es.add(oemof_sink)

        # Add transformers to the EnergySystem
        for transformer in es.transformers:
            oemof_transformer = solph.Transformer(
                label=transformer.label,
                inputs=buildIOFlows(transformer.inputs, oemof_busses),
                outputs=buildIOFlows(transformer.outputs, oemof_busses)
            )
            oemof_es.add(oemof_transformer)

        # Add storages to the EnergySystem
        for storage in es.storages:
            oemof_storage = solph.GenericStorage(
                nominal_storage_capacity=storage.nominal_storage_capacity,
                label=storage.label,
                inputs=buildIOFlows(storage.inputs, oemof_busses),
                outputs=buildIOFlows(storage.outputs, oemof_busses),
                loss_rate=storage.loss_rate,
                initial_storage_level=storage.initial_storage_level,
                inflow_conversion_factor=storage.inflow_conversion_factor,
                outflow_conversion_factor=storage.outflow_conversion_factor
            )
            oemof_es.add(oemof_storage)

        ##########################################################################
        # Print the EnergySystem as Graph
        ##########################################################################
        gr = ESGraphRenderer(energy_system=oemof_es, filepath="images/energy_system")
        #gr.view()

        # oemof_es.dump(dpath=wdir, filename=filename)

        ##########################################################################
        # Optimise the energy system and plot the results
        ##########################################################################
        logging.info("Optimise the energy system")

        # initialise the operational model
        model = solph.Model(oemof_es)

        solver_verbose = False

        # if tee_switch is true solver messages will be displayed
        logging.info("Solve the optimization problem")
        model.solve(solver="cbc", solve_kwargs={"tee": solver_verbose})

        logging.info("Store the energy system with the results.")

        # The processing module of the outputlib can be used to extract the results
        # from the model transfer them into a homogeneous structured dictionary.

        # add results to the energy system to make it possible to store them.
        oemof_es.results["main"] = solph.processing.results(model)
        oemof_es.results["meta"] = solph.processing.meta_results(model)

        # store energy system with results
        oemof_es.dump(dpath=wdir, filename=filename)



