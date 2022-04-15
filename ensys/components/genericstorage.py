from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args
from oemof import solph


class EnsysStorage(HsnConfigContainer):
    def __init__(self,
                 label: str = "Default Label",
                 inputs=None,
                 outputs=None,
                 nominal_storage_capacity: float = 1.0,
                 invest_relation_capacity: float = None,
                 invest_relation_output_capacity: float = None,
                 invest_relation_input_output: float = None,
                 initial_storage_level: float = 0.0,
                 balanced: bool = True,
                 loss_rate: float = 0.0,
                 fixed_losses_relative: float = 0.0,
                 fixed_losses_absolute: float = 0.0,
                 inflow_conversion_factor: float = 1.0,
                 outflow_conversion_factor: float = 1.0,
                 min_storage_level: float = 0.0,
                 max_storage_level: float = 1.0,
                 investment: solph.Investment = None,
                 *args,
                 **kwargs
                 ):
        super().__init__()
        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "param1": "0:0:int:0:10:5"
    }
