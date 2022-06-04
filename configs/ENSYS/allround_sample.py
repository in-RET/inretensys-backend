import math
import os
import pickle

import numpy as np
import pandas as pd
from oemof.tools import economics

from InRetEnsys import InRetEnsysFlow, InRetEnsysSource, InRetEnsysEnergysystem, InRetInRetEnsysBus, \
    InRetEnsysInvestment, InRetEnsysSink, InRetEnsysConstraints, InRetEnsysStorage, InRetEnsysModel, \
    InRetEnsysNonConvex, InRetEnsysTransformer
from InRetEnsys.types import Constraints, Frequencies, Solver
from hsncommon.log import HsnLogger


def CreateAllroundSampleConfiguration():
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

    bel = InRetInRetEnsysBus(label="electricity")

    bgas = InRetInRetEnsysBus(label="natural_gas")

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
                variable_costs=price_gas,
                emission_factor=0.3,
                investment=InRetEnsysInvestment(ep_costs=epc_rgas,
                                                my_invest_limit=1)
            )
        }
    )

    import_el = InRetEnsysSource(
        label="biomass",
        outputs={bel.label: InRetEnsysFlow(
            nonconvex=InRetEnsysNonConvex(),
            # fix=data["import_el"].tolist(),
            nominal_value=53000,  # 53000
            emission_factor=0.01
        )}
    )

    epc_pp_gas = economics.annuity(capex=2000, n=20, wacc=0.05)
    logger.info("epc_pp_gas: " + str(epc_pp_gas))

    pp_gas = InRetEnsysTransformer(
        label="pp_gas",
        inputs={bgas.label: InRetEnsysFlow()},
        outputs={bel.label: InRetEnsysFlow(
            # investment=EnsysInvestment(ep_costs=epc_pp_gas),
            nominal_value=16000,
            min=0.1,
            max=0.8,
            variable_costs=0.1,
            nonconvex=InRetEnsysNonConvex(
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

    storage = InRetEnsysStorage(
        label="storage",
        # nominal_storage_capacity=10000,
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
        outflow_conversion_factor=0.8,
        invest_relation_input_capacity=1 / 6,
        invest_relation_output_capacity=1 / 6,
        investment=InRetEnsysInvestment(ep_costs=epc_storage),
    )

    constraint1 = InRetEnsysConstraints(typ=Constraints.investment_limit, limit=3100000)  # 2700900
    constraint2 = InRetEnsysConstraints(typ=Constraints.limit_active_flow_count_by_keyword,
                                        keyword="my_keyword",
                                        lower_limit=0,
                                        upper_limit=1)
    constraint3 = InRetEnsysConstraints(typ=Constraints.additional_investment_flow_limit,
                                        keyword="my_invest_limit",
                                        limit=29000)
    constraint4 = InRetEnsysConstraints(typ=Constraints.emission_limit,
                                        limit=9900000)

    es = InRetEnsysEnergysystem(
        busses=[bel, bgas],
        sinks=[excess_bel, demand_el],
        sources=[import_el, rgas],
        storages=[storage],
        transformers=[pp_gas],
        constraints=[constraint1, constraint2, constraint3, constraint4],
        start_date="01/01/2022",
        time_steps=number_of_time_steps,
        frequenz=Frequencies.hourly
    )

    allround_model = InRetEnsysModel(energysystem=es,
                                   solver=Solver.gurobi,
                                   solver_verbose=False)

    wkdir = os.path.join(os.path.dirname(__file__))
    filename = "ensys_allround_config.bin"
    file = os.path.join(wkdir, filename)

    xf = open(file, 'wb')
    pickle.dump(allround_model, xf)
    xf.close()

    return file
