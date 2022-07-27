import math
import os
import time

import numpy as np
import pandas as pd
from oemof import solph
from oemof.tools import economics


def oemofAllroundSample(dumpfile, solver_verbose=False):
    solver = "gurobi"
    number_of_time_steps = 24 * 7 * 12
    solver_verbose = solver_verbose

    date_time_index = pd.date_range(
        "1/1/2022", periods=number_of_time_steps, freq="H"
    )

    es = solph.EnergySystem(timeindex=date_time_index)

    import_el = []

    N = number_of_time_steps  # sample count
    P = 200 # period
    D = 75 # width of pulse
    sig = (np.arange(N) % P < D) * 5000 + 53000

    demand_el = sig.tolist()

    for x in range(0, number_of_time_steps):
        if number_of_time_steps / 3 < x < 2 * number_of_time_steps / 3:
            demand_el[x] = 62000
        import_el.append(3000 * math.cos(1/10*x) * math.sin(1/10 * x) * math.cos(1/20*x)**3 + 54000)

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
                fix=data["demand_el"],
                nominal_value=1
            )},
        )
    )

    price_gas = 0.04
    epc_rgas = economics.annuity(capex=1000, n=20, wacc=0.05)
    print("epc_rgas: " + str(epc_rgas))
    # create source object representing the natural gas commodity (annual limit)
    es.add(
        solph.Source(
            label="rgas",
            outputs={
                bgas: solph.Flow(
                    variable_costs=price_gas,
                    emission_factor=0.3,
                    investment=solph.Investment(ep_costs=epc_rgas,
                                                my_invest_limit=1),
                )
            }
        )
    )

    es.add(
        solph.Source(
            label="biomass",
            outputs={bel: solph.Flow(
                nonconvex=solph.NonConvex(),
                #fix=data["import_el"],
                nominal_value=53000, #53000
                emission_factor=0.01
            )},
        )
    )

    # create simple transformer object representing a gas power plant
    epc_pp_gas = economics.annuity(capex=2000, n=20, wacc=0.05)
    print("epc_pp_gas: " + str(epc_pp_gas))
    transformer = solph.Transformer(
        label="pp_gas",
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(
            #investment=solph.Investment(ep_costs=epc_pp_gas),
            nominal_value=16000,
            min=0.1,
            max=0.8,
            variable_costs=0.1,
            nonconvex=solph.NonConvex(
                minimum_uptime=20,
                initial_status=0
            )
        )},
        conversion_factors={bel: 0.3},
    )

    es.add(transformer)

    # If the period is one year the equivalent periodical costs (epc) of an
    # investment are equal to the annuity. Use oemof's economic tools.
    epc_storage = economics.annuity(capex=30, n=20, wacc=0.05)
    print("epc_storage: " + str(epc_storage))

    kwargs = {
        "label": "storage",
        #"nominal_storage_capacity": 10000,
        "inputs": {
            bel: solph.Flow(
                variable_costs=0.0001
            )
        },
        "outputs": {bel: solph.Flow()},
        "loss_rate": 0.0,
        "initial_storage_level": None,
        "inflow_conversion_factor": 1,
        "outflow_conversion_factor": 0.8,
        "invest_relation_input_capacity": 1 / 6,
        "invest_relation_output_capacity": 1 / 6,
        "investment": solph.Investment(ep_costs=epc_storage)
    }

    storage = solph.GenericStorage(**kwargs)

    es.add(storage)

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    print("Initialise operational model.")
    # initialise the operational model
    model = solph.Model(es)

    # Constraints
    model = solph.constraints.investment_limit(model=model, limit=3100000) #2700900
    model = solph.constraints.limit_active_flow_count_by_keyword(model=model,
                                                                 keyword="my_keyword",
                                                                 lower_limit=0,
                                                                 upper_limit=1)
    model = solph.constraints.additional_investment_flow_limit(model=model,
                                                               keyword="my_invest_limit",
                                                               limit=29000)
    solph.constraints.emission_limit(om=model, limit=9900000)

    print("Start solving.")
    t_start = time.time()
    # if tee_switch is true solver messages will be displayed
    model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})
    t_end = time.time()

    print("Completed after " + str(round(t_end - t_start, 2)) + " seconds.")

    print("Processing data.")
    # add results to the energy system to make it possible to store them.
    es.results["main"] = solph.processing.results(model)
    es.results["meta"] = solph.processing.meta_results(model)
    es.results["verification"] = solph.processing.create_dataframe(model)

    #print(model.integral_limit_emission_factor())

    print("Dump files to filesystem.")
    # store energy system with results
    wdir = os.path.dirname(dumpfile)
    dumpfilename = os.path.basename(dumpfile)
    es.dump(dpath=wdir, filename=dumpfilename)


