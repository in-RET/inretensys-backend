from typing import Union, Dict

from oemof import solph

from InRetEnsys.common.config import InRetEnsysConfigContainer
from InRetEnsys.components.flow import InRetEnsysFlow
from InRetEnsys.components.investment import InRetEnsysInvestment


##  Container which contains the params for an oemof-genericstorage
#   
#   @param label: str = "Default Storage"
#   @param inputs: Dict[str, InRetEnsysFlow]
#   @param outputs: Dict[str, InRetEnsysFlow]
#   @param nominal_storage_capacity: Union[None, float] = None
#   @param invest_relation_input_capacity: Union[None, float] = None
#   @param invest_relation_output_capacity: Union[None, float] = None
#   @param invest_relation_input_output: Union[None, float] = None
#   @param initial_storage_level: Union[None, float] = None
#   @param balanced: bool = True
#   @param loss_rate: float = 0.0
#   @param fixed_losses_relative: Union[None, float] = None
#   @param fixed_losses_absolute: Union[None, float] = None
#   @param inflow_conversion_factor: float = 1
#   @param outflow_conversion_factor: float = 1
#   @param min_storage_level: float = 0
#   @param max_storage_level: float = 1
#   @param investment: Union[None, InRetEnsysInvestment] = None
class InRetEnsysStorage(InRetEnsysConfigContainer):
    label: str = "Default Storage"
    inputs: Dict[str, InRetEnsysFlow]
    outputs: Dict[str, InRetEnsysFlow]
    nominal_storage_capacity: Union[None, float] = None
    invest_relation_input_capacity: Union[None, float] = None
    invest_relation_output_capacity: Union[None, float] = None
    invest_relation_input_output: Union[None, float] = None
    initial_storage_level: Union[None, float] = None
    balanced: bool = True
    loss_rate: float = 0.0
    fixed_losses_relative: Union[None, float] = None
    fixed_losses_absolute: Union[None, float] = None
    inflow_conversion_factor: float = 1
    outflow_conversion_factor: float = 1
    min_storage_level: float = 0
    max_storage_level: float = 1
    investment: Union[None, InRetEnsysInvestment] = None

    ##  Returns an oemof-object from the given args of this object.
    #
    #   Builts a dictionary with all keywords given by the object and returns the oemof object initialised with these 'kwargs'.
    #
    #   @param self The Object Pointer
    #   @param energysystem The oemof-Energysystem to reference other objects i.e. for flows.
    #   @return solph.GenericStorage-Object (oemof)
    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.GenericStorage:
        kwargs = self.build_kwargs(energysystem)

        return solph.GenericStorage(**kwargs)