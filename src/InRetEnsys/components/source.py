from InRetEnsys.common.config import InRetEnsysConfigContainer
from InRetEnsys.components.flow import InRetEnsysFlow
from oemof import solph
from pydantic import Field


##  Container which contains the params for an InRetEnsys-Source-Object
#   
#   @param label: str = "Default Sink"
#   @param outputs: Dict[str, InRetEnsysFlow]
class InRetEnsysSource(InRetEnsysConfigContainer):
    label: str = Field(
        "Default Source",
        title='Label',
        description='Label',
        lvl_visible=21,
        lvl_edit=42
    )

    outputs: dict[str, InRetEnsysFlow] = Field(
        ...,
        title='Outputs',
        description='Outputs',
        lvl_visible=21,
        lvl_edit=42
    )

    ##  Returns an oemof-object from the given args of this object.
    #
    #   Builts a dictionary with all keywords given by the object and returns the oemof object initialised with these 'kwargs'.
    #
    #   @param self The Object Pointer
    #   @param energysystem The oemof-Energysystem to reference other objects i.e. for flows.
    #   @return solph.Source-Object (oemof)
    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.components.Source:
        kwargs = self.build_kwargs(energysystem)

        return solph.components.Source(**kwargs)
