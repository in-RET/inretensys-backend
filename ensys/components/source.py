from ensys import EnsysFlow
from ensys.config import EnsysConfigContainer, set_init_function_args_as_instance_args


class EnsysSource(EnsysConfigContainer):
    def __init__(self,
                 label: str = "Default Source",
                 outputs: dict[EnsysFlow] = None,
                 *args,
                 **kwargs
                 ):
        super().__init__()
        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "label": "0:0:string: min : max : 'Default Source'",
        "outputs": "0:0:dict: min : max : None"
    }
