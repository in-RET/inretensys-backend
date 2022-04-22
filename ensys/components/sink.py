from ensys import EnsysFlow
from ensys.config import EnsysConfigContainer, set_init_function_args_as_instance_args


class EnsysSink(EnsysConfigContainer):
    def __init__(self,
                 label: str = "Default Sink",
                 inputs: dict[EnsysFlow] = None,
                 *args,
                 **kwargs
                 ):
        super().__init__()
        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "label": "0:0:string: min : max : 'Default Sink'",
        "inputs": "0:0:dict: min : max : None"
    }
