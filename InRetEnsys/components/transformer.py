from typing import Dict
from oemof import solph

from InRetEnsys.common.config import InRetEnsysConfigContainer
from InRetEnsys.components.flow import InRetEnsysFlow

##  Container which contains the params for an InRetEnsys-Transformer-Object
#   
#   @param label: str = "Default Transformer"
#   @param inputs: Dict[str, InRetEnsysFlow] = None
#   @param outputs: Dict[str, InRetEnsysFlow] = None
#   @param conversion_factors: Dict = None
class InRetEnsysTransformer(InRetEnsysConfigContainer):
    label: str = "Default Transformer"
    inputs: Dict[str, InRetEnsysFlow] = None
    outputs: Dict[str, InRetEnsysFlow] = None
    conversion_factors: Dict = None

    ##  Returns an oemof-object from the given args of this object.
    #
    #   Builts a dictionary with all keywords given by the object and returns the oemof object initialised with these 'kwargs'.
    #
    #   @param self The Object Pointer
    #   @param energysystem The oemof-Energysystem to reference other objects i.e. for flows.
    #   @return solph.Transformer-Object (oemof)
    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Transformer:
        kwargs = self.build_kwargs(energysystem)

        return solph.Transformer(**kwargs)
