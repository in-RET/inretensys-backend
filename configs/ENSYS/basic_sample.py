import os
import pickle

import pandas as pd

from InRetEnsys import InRetEnsysBus, InRetEnsysSource, InRetEnsysFlow, InRetEnsysSink, InRetEnsysTransformer, \
    InRetEnsysEnergysystem, InRetEnsysStorage
from InRetEnsys.components.model import InRetEnsysModel
from InRetEnsys.types import Frequencies, Solver


def CreateConfiguration():
    data_file = "/Users/pyrokar/Documents/GitHub/python/InRetEnsys/configs/DATEN/Basic/basic_example.csv"
    data = pd.read_csv(data_file)

    bel = InRetEnsysBus(
        label="electricity"
    )

    bgas = InRetEnsysBus(
        label="natural_gas"
    )

    rgas = InRetEnsysSource(
        label="rgas",
        outputs={bgas.label: InRetEnsysFlow(
            nominal_value=29825293,
            summed_max=1
        )},
    )

    pv = InRetEnsysSource(
        label="pv",
        outputs={bel.label: InRetEnsysFlow(
            fix=data["pv"],
            nominal_value=582000
        )},
    )

    wind = InRetEnsysSource(
        label="wind",
        outputs={bel.label: InRetEnsysFlow(
            fix=data["wind"],
            nominal_value=1000000
        )},
    )

    excess_bel = InRetEnsysSink(
        label="excess_bel",
        inputs={bel.label: InRetEnsysFlow(
        )}
    )

    demand_bel = InRetEnsysSink(
        label="demand",
        inputs={bel.label: InRetEnsysFlow(
            fix=data["demand_el"],
            nominal_value=1
        )},
    )

    pp_gas = InRetEnsysTransformer(
        label="pp_gas",
        inputs={bgas.label: InRetEnsysFlow()},
        outputs={bel.label: InRetEnsysFlow(
            nominal_value=10e10,
            variable_costs=50
        )},
        conversion_factors={bel.label: 0.58},
    )

    storage = InRetEnsysStorage(
        nominal_storage_capacity=10077997,
        label="storage",
        inputs={bel.label: InRetEnsysFlow(
            nominal_value=10077997 / 6
        )},
        outputs={bel.label: InRetEnsysFlow(
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

    es = InRetEnsysEnergysystem(
        busses=[bel, bgas],
        sinks=[demand_bel, excess_bel],
        sources=[wind, pv, rgas],
        transformers=[pp_gas],
        storages=[storage],
        time_steps=number_of_time_steps,
        start_date="1/1/2012",
        frequenz=Frequencies.hourly
    )

    model = InRetEnsysModel(
        energysystem=es,
        solver=Solver.gurobi,
        solver_verbose=False
    )

    wkdir = os.path.join(os.path.dirname(__file__))
    filename = "ensys_basic_config.bin"
    file = os.path.join(wkdir, filename)

    xf = open(file, 'wb')
    pickle.dump(model, xf)
    xf.close()

    return file


CreateConfiguration()
