from typing import Union, Dict

from oemof import solph

from InRetEnsys import InRetEnsysConfigContainer


##  Container which contains the params for an oemof-investment
#    
#   @param maximum: float = float("+inf")
#   @param minimum: float = 0.0
#   @param ep_costs: float = 0.0
#   @param existing: float = 0.0
#   @param nonconvex: bool = False
#   @param offset: float = 0.0
#   @param kwargs: Union[None, Dict] = None
class InRetEnsysInvestment(InRetEnsysConfigContainer):
    maximum: float = float("+inf")
    minimum: float = 0.0
    ep_costs: float = 0.0
    existing: float = 0.0
    nonconvex: bool = False
    offset: float = 0.0
    kwargs: Union[None, Dict] = None

    ##  Returns an oemof-object from the given args of this object.
    #
    #   Builts a dictionary with all keywords given by the object and returns the oemof object initialised with these 'kwargs'.
    #
    #   @param self The Object Pointer
    #   @param energysystem The oemof-Energysystem to reference other objects i.e. for flows.
    #   @return solph.Investment-Object (oemof)
    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Investment:
        kwargs = self.build_kwargs(energysystem)

        return solph.Investment(**kwargs)
