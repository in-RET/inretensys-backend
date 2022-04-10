from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args


class EnsysTransformer(HsnConfigContainer):
    def __init__(self,
                 label: str = "Default Label",
                 inputs=None,
                 outputs=None,
                 conversion_factors: dict = None,
                 *args,
                 **kwargs
                 ):
        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "label": "0:0:string: ... ",
        "input": "0:0:dict: ... ",
        "output": "0:0:dict: ... ",
        "conversion_factors": "0:0:dict: ... "
    }
