from oemof import solph

from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args


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
        "label": "0:0:string: min : max : 'Default NonConvex'",
        "startup_costs": "0:0: type : min : max :None",
        "shutdown_costs": "0:0: type : min : max :None",
        "activity_costs": "0:0: type : min : max :None",
        "minimum_uptime": "0:0: type : min : max :None",
        "minimum_downtime": "0:0: type : min : max :None",
        "maximum_startups": "0:0: type : min : max :None",
        "initial_status": "0:0: type : min : max :None",
        "positive_gradient": "0:0: type : min : max :None",
        "negative_gradient": "0:0: type : min : max :None"
    }

    def to_oemof(self):
        kwargs = {}

        for attr_name in dir(self):
            if not attr_name.startswith("__") and \
                    not attr_name.startswith("to_") and \
                    not attr_name == "format":
                name = attr_name
                value = getattr(self, attr_name)

                kwargs[name] = value

        oemof_obj = solph.NonConvex(**kwargs)

        return oemof_obj
