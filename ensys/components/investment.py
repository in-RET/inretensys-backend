from oemof import solph

from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args


class EnsysInvestment(HsnConfigContainer):
    format = {
        # name : 0: 0: type: min: max: default
        "maximum": "0:0:float:0:1:0",
        "minimum": "0:0:float:0:1:0",
        "ep_costs": "0:0:float:0:1:0",
        "nonconvex": "0:0:boolean:0:1:0",
        "offset": "0:0:float:0:1:0"
    }

    def __init__(self,
                 maximum: float = float("+inf"),
                 minimum: float = 0.0,
                 ep_costs: float = 0.0,
                 existing: float = 0.0,
                 nonconvex: bool = False,
                 offset: float = 0.0,
                 *args,
                 **kwargs,
                 ):
        super().__init__()
        set_init_function_args_as_instance_args(self, locals())

    def to_oemof(self):
        kwargs = {}

        for attr_name in dir(self):
            if not attr_name.startswith("__") and \
                    not attr_name.startswith("to_") and \
                    not attr_name == "format":
                name = attr_name
                value = getattr(self, attr_name)

                kwargs[name] = value

        oemof_obj = solph.Investment(**kwargs)

        return oemof_obj
