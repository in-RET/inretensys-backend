from typing import Dict
from oemof import solph

from ensys import EnsysFlow, EnsysConfigContainer


class EnsysSink(EnsysConfigContainer):
    label: str = "Default Sink"
    inputs: Dict[str, EnsysFlow]

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Sink:
        """
        Return an oemof-object build with the args of the object.
        :return: oemof-Sink-object
        :rtype: solph.Sink
        :param energysystem: the oemof-energysystem to build the kwargs of the object
        :type energysystem: solph.Energysystem
        """
        kwargs = self.build_kwargs(energysystem)

        return solph.Sink(**kwargs)
