from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args


class EnsysSource(HsnConfigContainer):
    def __init__(self,
                 label: str = "Default Source",
                 outputs=None,
                 *args,
                 **kwargs
                 ):
        super().__init__()
        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "label": "0:0:string: ... ",
        "input": "0:0:dict: ... ",
        "output": "0:0:dict: ... "
    }
