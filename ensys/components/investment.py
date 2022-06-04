from typing import Union, Dict
from oemof import solph

from ensys import EnsysConfigContainer


class EnsysInvestment(EnsysConfigContainer):
    maximum: float = float("+inf")
    minimum: float = 0.0
    ep_costs: float = 0.0
    existing: float = 0.0
    nonconvex: bool = False
    offset: float = 0.0
    kwargs: Union[None, Dict] = None

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Investment:
        """
        Return an oemof-object build with the args of the object.
        :return: oemof-investment-object
        :rtype: solph.Investment
        :param energysystem: the oemof-energysystem to build the kwargs of the object
        :type energysystem: solph.Energysystem
        """
        kwargs = self.build_kwargs(energysystem)

        return solph.Investment(**kwargs)
