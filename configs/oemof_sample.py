import os
import pandas as pd

from oemof import solph

def oemofSample():
    solver = "cbc"  # 'glpk', 'gurobi',....
    debug = False  # Set number_of_timesteps to 3 to get a readable lp-file.
    number_of_time_steps = 24 * 7 * 8
    solver_verbose = False  # show/hide solver output

    date_time_index = pd.date_range(
        "1/1/2012", periods=number_of_time_steps, freq="H"
    )

    energysystem = solph.EnergySystem(timeindex=date_time_index)

    # Read data file
    filename = os.path.join(os.getcwd(), "/Users/pyrokar/Documents/GitHub/python/oemof/examples/basic_example/basic_example.csv")
    data = pd.read_csv(filename)

    ##########################################################################
    # Create oemof object
    ##########################################################################

    # create natural gas bus
    bgas = solph.Bus(label="natural_gas")

    # create electricity bus
    bel = solph.Bus(label="electricity")

    # adding the buses to the energy system
    energysystem.add(bgas, bel)

    # create excess component for the electricity bus to allow overproduction
    energysystem.add(
        solph.Sink(
            label="excess_bel",
            inputs={bel: solph.Flow()}
        )
    )

    # create source object representing the natural gas commodity (annual limit)
    energysystem.add(
        solph.Source(
            label="rgas",
            outputs={bgas: solph.Flow(nominal_value=29825293, summed_max=1)},
        )
    )

    # create fixed source object representing wind power plants
    energysystem.add(
        solph.Source(
            label="wind",
            outputs={bel: solph.Flow(fix=data["wind"], nominal_value=1000000)},
        )
    )

    # create fixed source object representing pv power plants
    energysystem.add(
        solph.Source(
            label="pv",
            outputs={bel: solph.Flow(fix=data["pv"], nominal_value=582000)},
        )
    )

    # create simple sink object representing the electrical demand
    energysystem.add(
        solph.Sink(
            label="demand",
            inputs={bel: solph.Flow(fix=data["demand_el"], nominal_value=1)},
        )
    )

    # create simple transformer object representing a gas power plant
    energysystem.add(
        solph.Transformer(
            label="pp_gas",
            inputs={bgas: solph.Flow()},
            outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=50)},
            conversion_factors={bel: 0.58},
        )
    )

    # create storage object representing a battery
    storage = solph.components.GenericStorage(
        nominal_storage_capacity=10077997,
        label="storage",
        inputs={bel: solph.Flow(nominal_value=10077997 / 6)},
        outputs={
            bel: solph.Flow(nominal_value=10077997 / 6, variable_costs=0.001)
        },
        loss_rate=0.00,
        initial_storage_level=None,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8,
    )

    energysystem.add(storage)

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    # initialise the operational model
    model = solph.Model(energysystem)

    # if tee_switch is true solver messages will be displayed
    model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

    # add results to the energy system to make it possible to store them.
    energysystem.results["main"] = solph.processing.results(model)
    energysystem.results["meta"] = solph.processing.meta_results(model)

    # store energy system with results
    energysystem.dump(dpath=None, filename=None)
    