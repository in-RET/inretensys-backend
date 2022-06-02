from ensys.components.bus import EnsysBus
from ensys.common.config import EnsysConfigContainer
from ensys.components.source import EnsysSource
from ensys.components.sink import EnsysSink
from ensys.components.transformer import EnsysTransformer
from ensys.components.genericstorage import EnsysStorage
from ensys.components.constraints import EnsysConstraints
from ensys.types import Frequencies


class EnsysEnergysystem(EnsysConfigContainer):
    label: str = "Default Energysystem"
    busses: list[EnsysBus] = None
    sinks: list[EnsysSink] = None
    sources: list[EnsysSource] = None
    transformers: list[EnsysTransformer] = None
    storages: list[EnsysStorage] = None
    constraints: list[EnsysConstraints] = None
    start_date: str = None
    # 24 * 7 * 52
    time_steps: int = 8.736
    frequenz: Frequencies = Frequencies.hourly

    def __init__(self,
                 label: str = "Default Energysystem",
                 busses: list[EnsysBus] = None,
                 sinks: list[EnsysSink] = None,
                 sources: list[EnsysSource] = None,
                 transformers: list[EnsysTransformer] = None,
                 storages: list[EnsysStorage] = None,
                 constraints: list[EnsysConstraints] = None,
                 start_date: str = None,
                 time_steps: int = 8.736,
                 frequenz: Frequencies = Frequencies.hourly
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
