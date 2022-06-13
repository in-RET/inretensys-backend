import unittest

import pandas as pd
from oemof import solph

from InRetEnsys import InRetEnsysBus, InRetEnsysSink, InRetEnsysFlow, InRetEnsysSource


class InRetEnsysTestCase(unittest.TestCase):
    date_time_index = pd.date_range(
        "1/1/2022", periods=2016, freq="H"
    )
    es = solph.EnergySystem(timeindex=date_time_index)

    es.add(solph.Bus("electricity"))

    def bus_type_test(self):
        ensys_obj = InRetEnsysBus(label="electricity").to_oemof(self.es)
        self.assertIsInstance(ensys_obj, solph.Bus)

    def bus_object_test(self):
        # todo: hier kannste noch den Test implementieren
        oemof_obj = solph.Bus(label="electricity")
        ensys_obj = InRetEnsysBus(label="electricity").to_oemof(self.es)
        var = oemof_obj == ensys_obj

        self.assertTrue(var)

    def sink_type_test(self):
        bel = InRetEnsysBus(label="electricity")

        ensys_obj = InRetEnsysSink(inputs={bel.label: InRetEnsysFlow()}).to_oemof(self.es)
        self.assertIsInstance(ensys_obj, solph.Sink)

    def sink_object_test(self):
        pass

    def source_type_test(self):
        bel = InRetEnsysBus(label="electricity")

        ensys_obj = InRetEnsysSource(outputs={bel.label: InRetEnsysFlow()}).to_oemof(self.es)
        self.assertIsInstance(ensys_obj, solph.Source)


if __name__ == '__main__':
    unittest.main()
