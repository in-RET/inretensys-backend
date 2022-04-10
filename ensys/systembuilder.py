import os
import logging

from oemof import solph
from oemof_visio import ESGraphRenderer

from ensys.components import energysystem


def FindUsedBus(name, busses):
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
        usedBusses.append(FindUsedBus(bus, possibleBusses))

    IOFlows = {}
    for usedBus in usedBusses:
        # Build the parameter dictionary
        IOFlows[usedBus] = target[usedBus.label]

    return IOFlows


class EnsysSystembuilder():

    def __init__(self,
                 es: energysystem.EnsysEnergysystem):
        # do the magic

        # build an EnergySystem
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
            if source.inputs is None:
                oemof_source = solph.Source(
                                        label=source.label,
                                        outputs=buildIOFlows(source.outputs, oemof_busses),
                                    )
            else:
                oemof_source = solph.Source(
                                        label=source.label,
                                        inputs=buildIOFlows(source.inputs, oemof_busses),
                                        outputs=buildIOFlows(source.outputs, oemof_busses),
                                    )
            oemof_es.add(oemof_source)

        # Add sinks to the EnergySystem
        for sink in es.sinks:
            if sink.outputs is None:
                oemof_sink = solph.Sink(
                                        label=sink.label,
                                        inputs=buildIOFlows(sink.inputs, oemof_busses),
                                    )
            else:
                oemof_sink = solph.Sink(
                                        label=sink.label,
                                        inputs=buildIOFlows(sink.inputs, oemof_busses),
                                        outputs=buildIOFlows(sink.outputs, oemof_busses),
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
        gr.view()

        ##########################################################################
        # Optimise the energy system and plot the results
        ##########################################################################

        logging.info("Optimise the energy system")

        # initialise the operational model
        model = solph.Model(oemof_es)

        solver = "cbc"  # 'glpk', 'gurobi',....
        solver_verbose = False  # show/hide solver output

        # if tee_switch is true solver messages will be displayed
        logging.info("Solve the optimization problem")
        model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

        logging.info("Store the energy system with the results.")

        # The processing module of the outputlib can be used to extract the results
        # from the model transfer them into a homogeneous structured dictionary.

        # add results to the energy system to make it possible to store them.
        oemof_es.results["main"] = solph.processing.results(model)
        oemof_es.results["meta"] = solph.processing.meta_results(model)

        # store energy system with results
        workdir = os.path.join(os.getcwd(), "dumps")
        filename = "energySystem.dump"

        oemof_es.dump(dpath=workdir, filename=filename)
