from oemof import solph
from typing import Dict

from ensys import EnsysFlow, EnsysConfigContainer


class EnsysTransformer(EnsysConfigContainer):
    label: str = "Default Transformer"
    inputs: Dict[str, EnsysFlow] = None
    outputs: Dict[str, EnsysFlow] = None
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
