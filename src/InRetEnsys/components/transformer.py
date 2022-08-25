from typing import Dict
from oemof import solph
from pydantic import Field

from InRetEnsys.common.config import InRetEnsysConfigContainer
from InRetEnsys.components.flow import InRetEnsysFlow


##  Container which contains the params for an InRetEnsys-Transformer-Object
#   
#   @param label: str = "Default Transformer"
#   @param inputs: Dict[str, InRetEnsysFlow] = None
#   @param outputs: Dict[str, InRetEnsysFlow] = None
#   @param conversion_factors: Dict = None
class InRetEnsysTransformer(InRetEnsysConfigContainer):
    label: str = Field(
        "Default Transformer",
        title='Label',
        description='Label',
        lvl_visible=21,
        lvl_edit=42
    )

    inputs: Dict[str, InRetEnsysFlow] = Field(
        ...,
        title='Inputs',
        description='Inputs',
        lvl_visible=21,
        lvl_edit=42
    )

    outputs: Dict[str, InRetEnsysFlow] = Field(
        ...,
        title='Outputs',
        description='Outputs',
        lvl_visible=21,
        lvl_edit=42
    )

    conversion_factors: Dict = Field(
        ...,
        title='Conversion Factors',
        description='Dictionary with all conversion factors. <Bus.Label> : Float',
        lvl_visible=21,
        lvl_edit=42
    )

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
