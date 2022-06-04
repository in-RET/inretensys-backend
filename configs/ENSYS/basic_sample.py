import os
import pickle

import pandas as pd

from ensys import EnsysBus, EnsysSource, EnsysFlow, EnsysSink, EnsysTransformer, EnsysEnergysystem, EnsysStorage, \
    InRetSysModel
from ensys.types import Frequencies, Solver


def CreateBasisSampleConfiguration():
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
        conversion_factors={bel.label: 0.58},
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

    es = EnsysEnergysystem(
        busses=[bel, bgas],
        sinks=[demand_bel, excess_bel],
        sources=[wind, pv, rgas],
        transformers=[pp_gas],
        storages=[storage],
        time_steps=number_of_time_steps,
        start_date="1/1/2012",
        frequenz=Frequencies.hourly
    )

    model = InRetSysModel(
        energysystem=es,
        solver=Solver.gurobi
    )

    wkdir = os.path.join(os.path.dirname(__file__))
    filename = "ensys_basic_config.bin"
    file = os.path.join(wkdir, filename)

    xf = open(file, 'wb')
    pickle.dump(model, xf)
    xf.close()

    return file