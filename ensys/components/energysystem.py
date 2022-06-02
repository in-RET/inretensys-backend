from typing import Sequence

import pandas as pd

from ensys import EnsysConfigContainer
from ensys.components import bus, source, sink, genericstorage, transformer
from ensys.types import FREQUENZ_TYPES


class EnsysEnergysystem(EnsysConfigContainer):
    label: str = "Default Energysystem"
    busses: list = None
    sinks: list = None
    sources: list = None
    transformers: list = None
    storages: list = None
    constraints: list = None
    start_date: str = None
    # 24 * 7 * 52
    time_steps: int = 8.736
    frequenz: FREQUENZ_TYPES = FREQUENZ_TYPES.hourly

    def __init__(self,
                 label: str = "Default Energysystem",
                 busses: list[bus.EnsysBus] = None,
                 sinks: list[sink.EnsysSink] = None,
                 sources: list[source.EnsysSource] = None,
                 transformers: list[transformer.EnsysTransformer] = None,
                 storages: list[genericstorage.EnsysStorage] = None,
                 constraints: list = None,
                 start_date: str = None,
                 time_steps: int = 8.736,
                 frequenz: FREQUENZ_TYPES = FREQUENZ_TYPES.hourly
                 ):
        """Init the EnsysEnergysystem."""
        super().__init__()
        self.label = label
        self.busses = busses
        self.sinks = sinks
        self.sources = sources
        self.transformers = transformers
        self.storages = storages
        self.constraints = constraints
        self.start_date = start_date
        self.time_steps = time_steps
        self.frequenz = frequenz
