from typing import Union, Dict

from oemof import solph

from InRetEnsys import InRetEnsysConfigContainer

##  Container which contains the params for an InRetEnsys-NonConvex-Object
#   
#   @param startup_costs: Union[None, float] = None
#   @param shutdown_costs: Union[None, float] = None
#   @param activity_costs: Union[None, float] = None
#   @param minimum_uptime: Union[None, int] = None
#   @param minimum_downtime: Union[None, int] = None
#   @param maximum_startups: Union[None, int] = None
#   @param maximum_shutdowns: Union[None, int] = None
#   @param initial_status: int = 0
#   @param positive_gradient: Union[None, Dict] = None
#   @param negative_gradient: Union[None, Dict] = None
#   @param startup_costs: Union[None, float] = None
#   @param shutdown_costs: Union[None, float] = None
#   @param activity_costs: Union[None, float] = None
#   @param minimum_uptime: Union[None, int] = None
#   @param minimum_downtime: Union[None, int] = None
#   @param maximum_startups: Union[None, int] = None
#   @param maximum_shutdowns: Union[None, int] = None
#   @param initial_status: int = 0
#   @param positive_gradient: Union[None, Dict] = None
#   @param negative_gradient: Union[None, Dict] = None
class InRetEnsysNonConvex(InRetEnsysConfigContainer):
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

    ##  Returns an oemof-object from the given args of this object.
    #
    #   Builts a dictionary with all keywords given by the object and returns the oemof object initialised with these 'kwargs'.
    #
    #   @param self The Object Pointer
    #   @param energysystem The oemof-Energysystem to reference other objects i.e. for flows.
    #   @return solph.NonConvex-Object (oemof)
    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.NonConvex:
        kwargs = self.build_kwargs(energysystem)

        return solph.NonConvex(**kwargs)
