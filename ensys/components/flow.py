from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args
from oemof import solph


class EnsysFlow(HsnConfigContainer):
    def __init__(self,
                 label: str = "Default Label",
                 inputs=None,
                 outputs=None,
                 conversion_factors: dict = None,
                 nominal_value: float = 0.0,
                 max: float = 0.0,
                 min: float = 0.0,
                 fix: float = 0.0,
                 positive_gradient: dict = None,
                 negative_gradient: dict = None,
                 summed_max: float = 0.0,
                 summed_min: float = 0.0,
                 variable_costs: float = 0.0,
                 fixed: bool = False,
                 investment: solph.Investment = None,
                 nonconvex: solph.NonConvex = None,
                 *args,
                 **kwargs
                 ):
        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "param1": "0:0:int:0:10:5"
    }
