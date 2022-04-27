import math
import pandas as pd
from oemof.tools import economics

from ensys import *


def CreateSampleConfiguration(filename):
    number_of_time_steps = 24 * 7 * 16
    date_time_index = pd.date_range(
        "1/1/2022", periods=number_of_time_steps, freq="H"
    )

    demand_el = []
    import_el = []
    for x in range(0, number_of_time_steps):
        if number_of_time_steps / 4 < x < 3 * number_of_time_steps / 4:
            demand_el.append(51250)
        else:
            demand_el.append(6000 * math.sin(1/15*x) * math.cos(1/15*x) + 50000)
        import_el.append(3000 * math.cos(1/10*x) * math.sin(1/10 * x) * math.cos(1/20*x)**3 + 52000)

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
            balanced=False
        )}
    )

    demand_el = EnsysSink(
        label="demand",
        inputs={bel.label: EnsysFlow(
            fix=data["demand_el"], nominal_value=1
        )}
    )

    price_gas = 0.04
    rgas = EnsysSource(
        label="rgas",
        outputs={bgas.label: EnsysFlow(
            variable_costs=price_gas
        )}
    )

    import_el = EnsysSource(
        label="import",
        outputs={bel.label: EnsysFlow(
            fix=data["import_el"], nominal_value=1
        )}
    )

    pp_gas = EnsysTransformer(
        label="pp_gas",
        inputs={bgas.label: EnsysFlow()},
        outputs={bel.label: EnsysFlow(
            nominal_value=10e5,
            variable_costs=0
        )},
        conversion_factors={bel.label: 0.58}
    )

    # If the period is one year the equivalent periodical costs (epc) of an
    # investment are equal to the annuity. Use oemof's economic tools.
    epc_storage = economics.annuity(capex=1000, n=20, wacc=0.05)

    storage = EnsysStorage(
        #nominal_storage_capacity=1000000,
        label="storage",
        inputs={
            bel.label: EnsysFlow(
                # nominal_value=1000000 / 6
                variable_costs=0.0001
            )
        },
        outputs={
            bel.label: EnsysFlow(
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
        investment=EnsysInvestment(
            ep_costs=epc_storage
        ),
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

    es.to_file(filename)
