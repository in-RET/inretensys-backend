from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args
from oemof import solph


class EnsysNonConvex(HsnConfigContainer):
    def __init__(self,
                 label: str = "Default NonConvex",
                 startup_costs=None,
                 shutdown_costs=None,
                 activity_costs=None,
                 minimum_uptime: int = 1,
                 minimum_downtime: int = 1,
                 maximum_startups: int = 0,
                 # 0/False = off, 1/True = on
                 initial_status: bool = False,
                 positive_gradient=None,
                 negative_gradient=None,
                 *args,
                 **kwargs
                 ):
        super().__init__()

        if initial_status:
            initial_status = 1
        else:
            initial_status = 0

        if positive_gradient is None:
            positive_gradient = {"ub": None, "costs": 0}

        if negative_gradient is None:
            negative_gradient = {"ub": None, "costs": 0}

        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "param1": "0:0:int:0:10:5"
    }
