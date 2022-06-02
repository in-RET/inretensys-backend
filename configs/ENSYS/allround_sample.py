import math
import pickle

import numpy as np
import pandas as pd
from oemof.tools import economics

from ensys import EnsysBus, EnsysFlow, EnsysSink, EnsysSource, EnsysTransformer, EnsysStorage, EnsysInvestment, \
    EnsysEnergysystem, EnsysNonConvex, EnsysConstraints
from ensys.types import CONSTRAINT_TYPES, FREQUENZ_TYPES
from hsncommon.log import HsnLogger


def CreateSampleConfiguration(filename):
    logger = HsnLogger()

    number_of_time_steps = 24 * 7 * 12

    import_el = []

    N = number_of_time_steps  # sample count
    P = 200  # period
    D = 75  # width of pulse
    sig = (np.arange(N) % P < D) * 5000 + 53000

    demand_el = sig.tolist()

    for x in range(0, number_of_time_steps):
        if number_of_time_steps / 3 < x < 2 * number_of_time_steps / 3:
            demand_el[x] = 62000
        import_el.append(3000 * math.cos(1 / 10 * x) * math.sin(1 / 10 * x) * math.cos(1 / 20 * x) ** 3 + 54000)

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
                emission_factor=0.3,
                investment=EnsysInvestment(ep_costs=epc_rgas,
                                           my_invest_limit=1)
            )
        }
    )

    import_el = EnsysSource(
        label="biomass",
        outputs={bel.label: EnsysFlow(
            nonconvex=EnsysNonConvex(),
            # fix=data["import_el"],
            nominal_value=53000,  # 53000
            emission_factor=0.01
        )}
    )

    epc_pp_gas = economics.annuity(capex=2000, n=20, wacc=0.05)
    logger.info("epc_pp_gas: " + str(epc_pp_gas))

    pp_gas = EnsysTransformer(
        label="pp_gas",
        inputs={bgas.label: EnsysFlow()},
        outputs={bel.label: EnsysFlow(
            # investment=EnsysInvestment(ep_costs=epc_pp_gas),
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
        # nominal_storage_capacity=10000,
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

    constraint1 = EnsysConstraints(typ=CONSTRAINT_TYPES.investment_limit, limit=3100000)  # 2700900
    constraint2 = EnsysConstraints(typ=CONSTRAINT_TYPES.limit_active_flow_count_by_keyword,
                                   keyword="my_keyword",
                                   lower_limit=0,
                                   upper_limit=1)
    constraint3 = EnsysConstraints(typ=CONSTRAINT_TYPES.additional_investment_flow_limit,
                                   keyword="my_invest_limit",
                                   limit=29000)
    constraint4 = EnsysConstraints(typ=CONSTRAINT_TYPES.emission_limit,
                                   limit=9900000)

    es = EnsysEnergysystem(
        label="ensys Energysystem",
        busses=[bel, bgas],
        sinks=[excess_bel, demand_el],
        sources=[import_el, rgas],
        storages=[storage],
        transformers=[pp_gas],
        constraints=[constraint1, constraint2, constraint3, constraint4],
        start_date="01/01/2022",
        time_steps=number_of_time_steps,
        frequenz=FREQUENZ_TYPES.hourly
    )

    xf = open(filename, 'wb')
    pickle.dump(es, xf)
    xf.close()
