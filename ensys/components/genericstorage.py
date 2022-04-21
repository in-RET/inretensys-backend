from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args
from oemof import solph


class EnsysStorage(HsnConfigContainer):
    def __init__(self,
                 label: str = "Default Storage",
                 inputs=None,
                 outputs=None,
                 nominal_storage_capacity: float = 1.0,
                 invest_relation_capacity: float = None,
                 invest_relation_output_capacity: float = None,
                 invest_relation_input_output: float = None,
                 initial_storage_level: float = None,
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
        "label": "0:0:string: min : max :'Default Storage'",
        "inputs": "0:0: type : min : max :None",
        "outputs": "0:0: type : min : max :None",
        "nominal_storage_capacity": "0:0:float:0:1:1",
        "invest_relation_capacity": "0:0: type : min : max :None",
        "invest_relation_output_capacity": "0:0: type : min : max :None",
        "invest_relation_input_output": "0:0: type : min : max :None",
        "initial_storage_level": "0:0: type : min : max :None",
        "balanced": "0:0:boolean:0:1:1",
        "loss_rate": "0:0:float:0:1:0",
        "fixed_losses_relative": "0:0: type : min : max :None",
        "fixed_losses_absolute": "0:0: type : min : max :None",
        "inflow_conversion_factor": "0:0: type : min : max :None",
        "outflow_conversion_factor": "0:0: type : min : max :None",
        "min_storage_level": "0:0: type : min : max :None",
        "max_storage_level": "0:0: type : min : max :None",
        "investment": "0:0: type : min : max :None"
    }
