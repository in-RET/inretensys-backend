from ensys import EnsysFlow
from ensys.common.config import EnsysConfigContainer, set_init_function_args_as_instance_args


class EnsysTransformer(EnsysConfigContainer):
    def __init__(self,
                 label: str = "Default Transformer",
                 inputs: dict[EnsysFlow] = None,
                 outputs: dict[EnsysFlow] = None,
                 conversion_factors=None,
                 *args,
                 **kwargs
                 ):
        super().__init__()
        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "label": "0:0:string: min : max :'Default Transformer'",
        "input": "0:0:dict: min : max :None",
        "output": "0:0:dict: min: max :None",
        "conversion_factors": "0:0:dict: min : max :None"
    }
