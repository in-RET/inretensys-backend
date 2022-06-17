from typing import Dict
from oemof import solph
from InRetEnsys.common.config import InRetEnsysConfigContainer
from InRetEnsys.components.flow import InRetEnsysFlow


##  Container which contains the params for an InRetEnsys-Sink-Object
#   
#   @param label: str = "Default Sink"
#   @param inputs: Dict[str, InRetEnsysFlow]
class InRetEnsysSink(InRetEnsysConfigContainer):
    label: str = "Default Sink"
    inputs: Dict[str, InRetEnsysFlow]

    ##  Returns an oemof-object from the given args of this object.
    #
    #   Builts a dictionary with all keywords given by the object and returns the oemof object initialised with these 'kwargs'.
    #
    #   @param self The Object Pointer
    #   @param energysystem The oemof-Energysystem to reference other objects i.e. for flows.
    #   @return solph.Sink-Object (oemof)
    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Sink:
        kwargs = self.build_kwargs(energysystem)

        return solph.Sink(**kwargs)
