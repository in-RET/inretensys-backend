import pandas as pd

from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args


class EnsysEnergysystem(HsnConfigContainer):
    def __init__(self,
                 label: str = "Default Label",
                 busses: list = None,
                 sinks: list = None,
                 sources: list = None,
                 transformers: list = None,
                 storages: list = None,
                 timeindex: pd.DatetimeIndex = None,
                 timeincrement=None,
                 *args,
                 **kwargs
                 ):
        super().__init__()
        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "label": "0:0:string: ... ",
    }
