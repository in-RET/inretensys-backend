from typing import Sequence

import pandas as pd

from ensys import EnsysConfigContainer
from ensys.components import bus, source, sink, genericstorage, transformer


class EnsysEnergysystem(EnsysConfigContainer):
    label: str = "Default Energysystem"
    busses: list = None
    sinks: list = None
    sources: list = None
    transformers: list = None
    storages: list = None
    timeindex: Sequence = None
    timeincrement: str = None

    def __init__(self,
                 label: str = "Default Energysystem",
                 busses: list[bus.EnsysBus] = None,
                 sinks: list[sink.EnsysSink] = None,
                 sources: list[source.EnsysSource] = None,
                 transformers: list[transformer.EnsysTransformer] = None,
                 storages: list[genericstorage.EnsysStorage] = None,
                 timeindex: pd.DatetimeIndex = None,
                 timeincrement=None
                 ):
        """Init the EnsysEnergysystem."""
        super().__init__()
        self.label = label
        self.busses = busses
        self.sinks = sinks
        self.sources = sources
        self.transformers = transformers
        self.storages = storages
        self.timeindex = timeindex
        self.timeincrement = timeincrement
