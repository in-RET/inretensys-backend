from typing import Dict
from oemof import solph

from InRetEnsys.common.config import InRetEnsysConfigContainer
from InRetEnsys.components.flow import InRetEnsysFlow

##  Container which contains the params for an InRetEnsys-Source-Object
#   
#   @param label: str = "Default Sink"
#   @param outputs: Dict[str, InRetEnsysFlow]
class InRetEnsysSource(InRetEnsysConfigContainer):
    label: str = "Default Source",
    outputs: Dict[str, InRetEnsysFlow]

    ##  Returns an oemof-object from the given args of this object.
    #
    #   Builts a dictionary with all keywords given by the object and returns the oemof object initialised with these 'kwargs'.
    #
    #   @param self The Object Pointer
    #   @param energysystem The oemof-Energysystem to reference other objects i.e. for flows.
    #   @return solph.Source-Object (oemof)
    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Source:
        kwargs = self.build_kwargs(energysystem)

        return solph.Source(**kwargs)
