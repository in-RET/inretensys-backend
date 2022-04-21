from oemof import solph

from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args


class EnsysBus(HsnConfigContainer):
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
        return solph.bus(
            label=self.label,
            balanced=self.balanced
        )
