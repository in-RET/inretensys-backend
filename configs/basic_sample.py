import pandas as pd

from ensys import *


def CreateSampleConfiguration(filename):
    data_file = "/Users/pyrokar/Documents/GitHub/python/oemof/examples/basic_example/basic_example.csv"
    data = pd.read_csv(data_file)

    bel = EnsysBus(
        label="electricity"
    )

    bgas = EnsysBus(
        label="natural_gas"
    )

    rgas = EnsysSource(
        label="rgas",
        outputs={bgas.label: EnsysFlow(
            nominal_value=29825293,
            summed_max=1
        )},
    )

    pv = EnsysSource(
        label="pv",
        outputs={bel.label: EnsysFlow(
            fix=data["pv"],
            nominal_value=582000
        )},
    )

    wind = EnsysSource(
        label="wind",
        outputs={bel.label: EnsysFlow(
            fix=data["wind"],
            nominal_value=1000000
        )},
    )

    excess_bel = EnsysSink(
        label="excess_bel",
        inputs={bel.label: EnsysFlow(
            balanced=False
        )}
    )

    demand_bel = EnsysSink(
        label="demand",
        inputs={bel.label: EnsysFlow(
            fix=data["demand_el"],
            nominal_value=1
        )},
    )

    pp_gas = EnsysTransformer(
        label="pp_gas",
        inputs={bgas.label: EnsysFlow()},
        outputs={bel.label: EnsysFlow(
            nominal_value=10e10,
            variable_costs=50
        )},
        conversion_factors={bel: 0.58},
    )

    storage = EnsysStorage(
        nominal_storage_capacity=10077997,
        label="storage",
        inputs={bel.label: EnsysFlow(
            nominal_value=10077997 / 6
        )},
        outputs={bel.label: EnsysFlow(
            nominal_value=10077997 / 6,
            variable_costs=0.001
        )
        },
        loss_rate=0.00,
        initial_storage_level=None,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8,
    )

    number_of_time_steps = 24 * 7 * 8
    date_time_index = pd.date_range(
        "1/1/2012", periods=number_of_time_steps, freq="H"
    )

    es = EnsysEnergysystem(
        label="ensys Energysystem",
        busses=[bel, bgas],
        sinks=[demand_bel, excess_bel],
        sources=[wind, pv, rgas],
        transformers=[pp_gas],
        storages=[storage],
        timeindex=date_time_index
    )

    es.to_file(filename)
