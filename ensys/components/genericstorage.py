from typing import Union, Dict

from oemof import solph
from ensys import EnsysFlow, EnsysInvestment, EnsysConfigContainer


class EnsysStorage(EnsysConfigContainer):
    label: str = "Default Storage"
    inputs: Dict[str, EnsysFlow]
    outputs: Dict[str, EnsysFlow]
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
    investment: Union[None, EnsysInvestment] = None

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.GenericStorage:
        """
        Return an oemof-object build with the args of the object.
        :return: oemof-GenericStorage-object
        :rtype: solph.GenericStorage
        :param energysystem: the oemof-energysystem to build the kwargs of the object
        :type energysystem: solph.Energysystem
        """
        kwargs = self.build_kwargs(energysystem)

        return solph.GenericStorage(**kwargs)