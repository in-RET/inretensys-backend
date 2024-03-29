from InRetEnsys.common.config import InRetEnsysConfigContainer
from InRetEnsys.components.flow import InRetEnsysFlow
from InRetEnsys.components.investment import InRetEnsysInvestment
from oemof import solph
from pydantic import Field
from typing import Union


##  Container which contains the params for an oemof-genericstorage
#   
#   @param label: str = "Default Storage"
#   @param inputs: Dict[str, InRetEnsysFlow]
#   @param outputs: Dict[str, InRetEnsysFlow]
#   @param nominal_storage_capacity: float] = None
#   @param invest_relation_input_capacity: float] = None
#   @param invest_relation_output_capacity: float] = None
#   @param invest_relation_input_output: float] = None
#   @param initial_storage_level: float] = None
#   @param balanced: bool = True
#   @param loss_rate: float = 0.0
#   @param fixed_losses_relative: float] = None
#   @param fixed_losses_absolute: float] = None
#   @param inflow_conversion_factor: float = 1
#   @param outflow_conversion_factor: float = 1
#   @param min_storage_level: float = 0
#   @param max_storage_level: float = 1
#   @param investment: InRetEnsysInvestment] = None
class InRetEnsysStorage(InRetEnsysConfigContainer):
    label: str = Field(
        "Default Storage",
        title='Label',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    inputs: dict[str, InRetEnsysFlow] = Field(
        ...,
        title='Inputs',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )
    
    outputs: dict[str, InRetEnsysFlow] = Field(
        ...,
        title='Outputs',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )
    nominal_storage_capacity: Union[float, None] = Field(
        None,
        title='nominal storage capacity',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    invest_relation_input_capacity: Union[float, None] = Field(
        None,
        title='invest relation input capacity',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    invest_relation_output_capacity: Union[float, None] = Field(
        None,
        title='invest relation output capacity',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    invest_relation_input_output: Union[float, None] = Field(
        None,
        title='invest relation input output',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    initial_storage_level: Union[float, None] = Field(
        None,
        title='initial storage level',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    balanced: bool = Field(
        True,
        title='balanced',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    loss_rate: float = Field(
        0.0,
        title='loss rate',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    fixed_losses_relative: Union[float, None] = Field(
        None,
        title='fixed losses relative',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    fixed_losses_absolute: Union[float, None] = Field(
        None,
        title='Fixed losses absolute',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    inflow_conversion_factor: float = Field(
        1,
        title='Conversion factor: Inflow',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=1,
        ge=0.0,
        step=1e-3
    )

    outflow_conversion_factor: float = Field(
        1,
        title='Conversion factor: Outflow',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=1,
        ge=0.0,
        step=1e-3
    )

    min_storage_level: float = Field(
        0,
        title='Minimum storage level',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=1,
        ge=0.0,
        step=1e-3
    )

    max_storage_level: float = Field(
        1,
        title='Maximum storage level',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=1,
        ge=0.0,
        step=1e-3
    )

    investment: Union[InRetEnsysInvestment, None] = Field(
        None,
        title='Investment',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    ##  Returns an oemof-object from the given args of this object.
    #
    #   Builts a dictionary with all keywords given by the object and returns the oemof object initialised with these 'kwargs'.
    #
    #   @param self The Object Pointer
    #   @param energysystem The oemof-Energysystem to reference other objects i.e. for flows.
    #   @return solph.GenericStorage-Object (oemof)
    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.components.GenericStorage:
        kwargs = self.build_kwargs(energysystem)

        return solph.components.GenericStorage(**kwargs)