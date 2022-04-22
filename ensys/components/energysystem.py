import pandas as pd

from ensys.components import source, sink, bus, transformer, genericstorage
from ensys.config import EnsysConfigContainer, set_init_function_args_as_instance_args


class EnsysEnergysystem(EnsysConfigContainer):
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
        "label": "0:0:string:'Default EnergySystem'",
        "busses": "0:0:EnsysBus:None",
        "sinks": "0:0:EnsysSink:None",
        "sources": "0:0:EnsysSource:None",
        "transformers": "0:0:EnsysTransformer:None",
        "storages": "0:0:EnsysStorage:None",
        "timeindex": "0:0:pd.DateTimeIndex:None",
        "timeincrement": "0:0:None"
    }
