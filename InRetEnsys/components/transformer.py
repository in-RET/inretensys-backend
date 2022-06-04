from typing import Dict
from oemof import solph

from InRetEnsys.common.config import InRetEnsysConfigContainer
from InRetEnsys.components.flow import InRetEnsysFlow


class InRetEnsysTransformer(InRetEnsysConfigContainer):
    label: str = "Default Transformer"
    inputs: Dict[str, InRetEnsysFlow] = None
    outputs: Dict[str, InRetEnsysFlow] = None
    conversion_factors: Dict = None

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Transformer:
        """
        Return an oemof-object build with the args of the object.

        :return: oemof-Transformer-object
        :rtype: solph.Transformer
        :param energysystem: the oemof-energysystem to build the kwargs of the object
        :type energysystem: solph.Energysystem
        """
        kwargs = self.build_kwargs(energysystem)

        return solph.Transformer(**kwargs)
