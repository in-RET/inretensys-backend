import pandas as pd

from ensys.components import source, sink, bus, transformer, genericstorage
from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args


class EnsysEnergysystem(HsnConfigContainer):
    def __init__(self,
                 label: str = "Default Energysystem",
                 busses: list[bus.EnsysBus] = None,
                 sinks: list[sink.EnsysSink] = None,
                 sources: list[source.EnsysSource] = None,
                 transformers: list[transformer.EnsysTransformer] = None,
                 storages: list[genericstorage.EnsysStorage] = None,
                 timeindex: pd.DatetimeIndex = None,
                 timeincrement=None,
                 *args,
                 **kwargs
                 ):
        super().__init__()
        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "label": "0:0:string: min : max : 'Default EnergySystem'",
        "busses": "0:0: type : min : max :None",
        "sinks": "0:0: type : min : max :None",
        "sources": "0:0: type : min : max :None",
        "transformers": "0:0: type : min : max :None",
        "storages": "0:0: type : min : max :None",
        "timeindex": "0:0: type : min : max :None",
        "timeincrement": "0:0: type : min : max :None"
    }
