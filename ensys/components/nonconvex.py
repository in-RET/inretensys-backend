from typing import Union, Dict
from oemof import solph

from ensys import EnsysConfigContainer


class EnsysNonConvex(EnsysConfigContainer):
    startup_costs: Union[None, float] = None
    shutdown_costs: Union[None, float] = None
    activity_costs: Union[None, float] = None
    minimum_uptime: Union[None, int] = None
    minimum_downtime: Union[None, int] = None
    maximum_startups: Union[None, int] = None
    maximum_shutdowns: Union[None, int] = None
    # 0/False = off, 1/True = on
    initial_status: int = 0
    positive_gradient: Union[None, Dict] = None
    negative_gradient: Union[None, Dict] = None

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.NonConvex:
        """
        Return an oemof-object build with the args of the object.
        :return: oemof-NonConvex-object
        :rtype: solph.NonConvex
        :param energysystem: the oemof-energysystem to build the kwargs of the object
        :type energysystem: solph.Energysystem
        """
        kwargs = self.build_kwargs(energysystem)

        return solph.NonConvex(**kwargs)
