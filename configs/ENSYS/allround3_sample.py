import math
import os
import pickle

import numpy as np
import pandas as pd
from oemof.tools import economics

from src.InRetEnsys import InRetEnsysFlow, InRetEnsysSource, InRetEnsysEnergysystem, InRetEnsysSink, \
    InRetEnsysStorage, InRetEnsysModel, InRetEnsysTransformer, InRetEnsysBus
from src.InRetEnsys import Frequencies, Solver
from hsncommon.log import HsnLogger


def CreateConfiguration():
    logger = HsnLogger()
    number_of_time_steps = 24 * 7 * 12
    import_el = []

    N = number_of_time_steps  # sample count
    P = 200  # period
    D = 75  # width of pulse
    sig = (np.arange(N) % P < D) * 5000 + 45000

    demand_el = sig.tolist()

    for x in range(0, number_of_time_steps):
        if number_of_time_steps / 3 < x < 2 * number_of_time_steps / 3:
            demand_el[x] = 38000
        import_el.append(3000 * math.cos(1 / 10 * x) * math.sin(1 / 10 * x) * math.cos(1 / 20 * x) ** 3 + 45000)

    tmp = {'demand_el': demand_el, 'import_el': import_el}
    data = pd.DataFrame(tmp)

    bel = InRetEnsysBus(label="electricity")
    bgas = InRetEnsysBus(label="natural_gas")

    excess_bel = InRetEnsysSink(
        label="excess_bel",
        inputs={bel.label: InRetEnsysFlow()}
    )

    demand_el = InRetEnsysSink(
        label="demand",
        inputs={bel.label: InRetEnsysFlow(
            fix=data["demand_el"],
            nominal_value=1
        )}
    )

    price_gas = 0.04
    epc_rgas = economics.annuity(capex=1000, n=20, wacc=0.05)
    logger.info("epc_rgas: " + str(epc_rgas))

    rgas = InRetEnsysSource(
        label="rgas",
        outputs={
            bgas.label: InRetEnsysFlow(
                variable_costs=price_gas
            )
        }
    )

    import_el = InRetEnsysSource(
        label="biomass",
        outputs={bel.label: InRetEnsysFlow(
            fix=data["import_el"].tolist(),
            nominal_value=1
        )}
    )

    epc_pp_gas = economics.annuity(capex=2000, n=20, wacc=0.05)
    logger.info("epc_pp_gas: " + str(epc_pp_gas))

    pp_gas = InRetEnsysTransformer(
        label="pp_gas",
        inputs={bgas.label: InRetEnsysFlow()},
        outputs={bel.label: InRetEnsysFlow(
            nominal_value=16000,
            min=0.1,
            max=0.8,
            variable_costs=0.1
        )},
        conversion_factors={bel.label: 0.3}
    )

    # If the period is one year the equivalent periodical costs (epc) of an
    # investment are equal to the annuity. Use oemof's economic tools.
    epc_storage = economics.annuity(capex=30, n=20, wacc=0.05)
    logger.info("epc_storage: " + str(epc_storage))

    storage = InRetEnsysStorage(
        label="storage",
        nominal_storage_capacity=10000,
        inputs={
            bel.label: InRetEnsysFlow(
                variable_costs=0.0001
            )
        },
        outputs={
            bel.label: InRetEnsysFlow()
        },
        loss_rate=0.0,
        initial_storage_level=None,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8
    )

    es = InRetEnsysEnergysystem(
        busses=[bel, bgas],
        sinks=[excess_bel, demand_el],
        sources=[import_el, rgas],
        storages=[storage],
        transformers=[pp_gas],
        start_date="01/01/2022",
        time_steps=number_of_time_steps,
        frequenz=Frequencies.hourly
    )

    allround_model = InRetEnsysModel(energysystem=es,
                                     solver=Solver.gurobi,
                                     solver_verbose=False)

    wkdir = os.path.join(os.path.dirname(__file__))
    filename = "ensys_allround3_config.bin"
    file = os.path.join(wkdir, filename)

    logger.info("Write file to " + file)
    xf = open(file, 'wb')
    pickle.dump(allround_model, xf)
    xf.close()

    return file
