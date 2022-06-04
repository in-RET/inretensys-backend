from typing import Union

from ensys.components.bus import EnsysBus
from ensys.common.config import EnsysConfigContainer
from ensys.components.source import EnsysSource
from ensys.components.sink import EnsysSink
from ensys.components.transformer import EnsysTransformer
from ensys.components.genericstorage import EnsysStorage
from ensys.components.constraints import EnsysConstraints
from ensys.types import Frequencies


class EnsysEnergysystem(EnsysConfigContainer):
    busses: Union[None, list[EnsysBus]] = None
    sinks: Union[None, list[EnsysSink]] = None
    sources: Union[None, list[EnsysSource]] = None
    transformers: Union[None, list[EnsysTransformer]] = None
    storages: Union[None, list[EnsysStorage]] = None
    constraints: Union[None, list[EnsysConstraints]] = None
    frequenz: Frequencies = Frequencies.hourly
    start_date: str
    # 24 * 7 * 52
    time_steps: int
