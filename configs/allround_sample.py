import math
import pickle

import numpy as np
import pandas as pd
from oemof.tools import economics

from ensys import EnsysBus, EnsysFlow, EnsysSink, EnsysSource, EnsysTransformer, EnsysStorage, EnsysInvestment, \
    EnsysEnergysystem, EnsysNonConvex
from hsncommon.log import HsnLogger


def CreateSampleConfiguration(filename):
    logger = HsnLogger()
    number_of_time_steps = 24 * 7 * 12
    date_time_index = pd.date_range(
        "1/1/2022", periods=number_of_time_steps, freq="H"
    )

    import_el = []

    N = number_of_time_steps  # sample count
    P = 100 # period
    D = 25 # width of pulse
    sig = (np.arange(N) % P < D) * 10000 + 50000

    demand_el = sig.tolist()

    for x in range(0, number_of_time_steps):
        if number_of_time_steps / 3 < x < 2 * number_of_time_steps / 3:
            demand_el[x] = 62000
        import_el.append(3000 * math.cos(1/10*x) * math.sin(1/10 * x) * math.cos(1/20*x)**3 + 54000)

    tmp = {'demand_el': demand_el, 'import_el': import_el}
    data = pd.DataFrame(tmp)

    bel = EnsysBus(
        label="electricity"
    )

    bgas = EnsysBus(
        label="natural_gas"
    )

    excess_bel = EnsysSink(
        label="excess_bel",
        inputs={bel.label: EnsysFlow(
        )}
    )

    demand_el = EnsysSink(
        label="demand",
        inputs={bel.label: EnsysFlow(
            fix=data["demand_el"],
            nominal_value=1
        )}
    )

    price_gas = 0.04
    epc_rgas = economics.annuity(capex=1000, n=20, wacc=0.05)
    logger.info("epc_rgas: " + str(epc_rgas))

    rgas = EnsysSource(
        label="rgas",
        outputs={
            bgas.label: EnsysFlow(
                variable_costs=price_gas,
                investment=EnsysInvestment(ep_costs=epc_rgas)
            )
        }
    )

    import_el = EnsysSource(
        label="import",
        outputs={bel.label: EnsysFlow(
            fix=data["import_el"],
            nominal_value=1
        )}
    )

    epc_pp_gas = economics.annuity(capex=2000, n=20, wacc=0.05)
    logger.info("epc_pp_gas: " + str(epc_pp_gas))

    pp_gas = EnsysTransformer(
        label="pp_gas",
        inputs={bgas.label: EnsysFlow()},
        outputs={bel.label: EnsysFlow(
            #investment=EnsysInvestment(ep_costs=epc_pp_gas),
            nominal_value=16000,
            min=0.1,
            max=0.8,
            variable_costs=0.1,
            nonconvex=EnsysNonConvex(
                minimum_uptime=20,
                initial_status=0
            )
        )},
        conversion_factors={bel.label: 0.3}
    )

    # If the period is one year the equivalent periodical costs (epc) of an
    # investment are equal to the annuity. Use oemof's economic tools.
    epc_storage = economics.annuity(capex=30, n=20, wacc=0.05)
    logger.info("epc_storage: " + str(epc_storage))

    storage = EnsysStorage(
        label="storage",
        #nominal_storage_capacity=10000,
        inputs={
            bel.label: EnsysFlow(
                variable_costs=0.0001
            )
        },
        outputs={
            bel.label: EnsysFlow()
        },
        loss_rate=0.0,
        initial_storage_level=None,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8,
        invest_relation_input_capacity=1 / 6,
        invest_relation_output_capacity=1 / 6,
        investment=EnsysInvestment(ep_costs=epc_storage),
    )

    es = EnsysEnergysystem(
        label="ensys Energysystem",
        busses=[bel, bgas],
        sinks=[excess_bel, demand_el],
        sources=[import_el, rgas],
        storages=[storage],
        transformers=[pp_gas],
        timeindex=date_time_index
    )

    xf = open(filename, 'wb')
    pickle.dump(es, xf)
    xf.close()
