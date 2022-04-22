from oemof import solph

from ensys.config import EnsysConfigContainer, set_init_function_args_as_instance_args


class EnsysBus(EnsysConfigContainer):
    def __init__(self,
                 label: str = "Default Bus",
                 balanced: bool = True,
                 *args,
                 **kwargs
                 ):
        super().__init__()
        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "label": "0:0:string: min : max : 'Default Bus'",
        "balanced": "0:0:boolean:0:1:1"
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

        oemof_obj = solph.Bus(kwargs)

        return oemof_obj
