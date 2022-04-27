import math
import os

import pandas as pd
from oemof import solph
from oemof.tools import economics
from oemof_visio import ESGraphRenderer


def oemofAllroundSample(dumpfile):
    solver = "cbc"
    number_of_time_steps = 24 * 7 * 16
    solver_verbose = False

    date_time_index = pd.date_range(
        "1/1/2022", periods=number_of_time_steps, freq="H"
    )

    es = solph.EnergySystem(timeindex=date_time_index)

    demand_el = []
    import_el = []
    for x in range(0, number_of_time_steps):
        if number_of_time_steps / 4 < x < 3 * number_of_time_steps / 4:
            demand_el.append(51250)
        else:
            demand_el.append(6000 * math.sin(1 / 15 * x) * math.cos(1 / 15 * x) + 50000)
        import_el.append(3000 * math.cos(1/10*x) * math.sin(1/10 * x) * math.cos(1/20*x)**3 + 52000)

    tmp = {'demand_el': demand_el, 'import_el': import_el}
    data = pd.DataFrame(tmp)

    ##########################################################################
    # Create oemof object
    ##########################################################################

    # create electricity bus
    bel = solph.Bus(label="electricity")

    # create natural gas bus
    bgas = solph.Bus(label="natural_gas")

    # adding the buses to the energy system
    es.add(bel, bgas)

    # create excess component for the electricity bus to allow overproduction
    es.add(
        solph.Sink(
            label="excess_bel",
            inputs={bel: solph.Flow(
                balanced=False
            )}
        )
    )

    es.add(
        solph.Sink(
            label="demand",
            inputs={bel: solph.Flow(
                fix=data["demand_el"], nominal_value=1
            )},
        )
    )

    price_gas = 0.04
    # create source object representing the natural gas commodity (annual limit)
    es.add(
        solph.Source(
            label="rgas", outputs={bgas: solph.Flow(variable_costs=price_gas)}
        )
    )

    es.add(
        solph.Source(
            label="import",
            outputs={bel: solph.Flow(
                fix=data["import_el"], nominal_value=1
            )},
        )
    )

    # create simple transformer object representing a gas power plant
    es.add(
        solph.Transformer(
            label="pp_gas",
            inputs={bgas: solph.Flow()},
            outputs={bel: solph.Flow(nominal_value=10e5, variable_costs=0)},
            conversion_factors={bel: 0.58},
        )
    )

    # If the period is one year the equivalent periodical costs (epc) of an
    # investment are equal to the annuity. Use oemof's economic tools.
    epc_storage = economics.annuity(capex=1000, n=20, wacc=0.05)

    es.add(
        solph.components.GenericStorage(
            #nominal_storage_capacity=1000000,
            label="storage",
            inputs={
                bel: solph.Flow(
                    # nominal_value=1000000 / 6
                    variable_costs=0.0001
                )
            },
            outputs={
                bel: solph.Flow(
                    # nominal_value=1000000 / 6,
                    # variable_costs=0.001
                )
            },
            loss_rate=0.0,
            initial_storage_level=None,
            inflow_conversion_factor=0.3,
            outflow_conversion_factor=0.3,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            investment=solph.Investment(ep_costs=epc_storage),
        )
    )

    filepath = "images/energy_system"
    gr = ESGraphRenderer(energy_system=es, filepath=filepath)
    gr.view()

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    # initialise the operational model
    model = solph.Model(es)

    # if tee_switch is true solver messages will be displayed
    model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

    # add results to the energy system to make it possible to store them.
    es.results["main"] = solph.processing.results(model)
    es.results["meta"] = solph.processing.meta_results(model)
    es.results["compare"] = solph.processing.create_dataframe(model)

    # store energy system with results
    wdir = os.path.dirname(dumpfile)
    dumpfilename = os.path.basename(dumpfile)
    es.dump(dpath=wdir, filename=dumpfilename)