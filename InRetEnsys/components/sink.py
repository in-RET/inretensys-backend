from typing import Dict
from oemof import solph

from InRetEnsys.common.config import InRetEnsysConfigContainer
from InRetEnsys.components.flow import InRetEnsysFlow


class InRetEnsysSink(InRetEnsysConfigContainer):
    label: str = "Default Sink"
    inputs: Dict[str, InRetEnsysFlow]

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
