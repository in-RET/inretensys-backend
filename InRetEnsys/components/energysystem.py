from typing import Union

from InRetEnsys.components.bus import InRetInRetEnsysBus
from InRetEnsys.common.config import InRetEnsysConfigContainer
from InRetEnsys.components.source import InRetEnsysSource
from InRetEnsys.components.sink import InRetEnsysSink
from InRetEnsys.components.transformer import InRetEnsysTransformer
from InRetEnsys.components.genericstorage import InRetEnsysStorage
from InRetEnsys.components.constraints import InRetEnsysConstraints
from InRetEnsys.types import Frequencies


class InRetEnsysEnergysystem(InRetEnsysConfigContainer):
    busses: Union[None, list[InRetInRetEnsysBus]] = None
    sinks: Union[None, list[InRetEnsysSink]] = None
    sources: Union[None, list[InRetEnsysSource]] = None
    transformers: Union[None, list[InRetEnsysTransformer]] = None
    storages: Union[None, list[InRetEnsysStorage]] = None
    constraints: Union[None, list[InRetEnsysConstraints]] = None
    frequenz: Frequencies = Frequencies.hourly
    start_date: str
    # 24 * 7 * 52
    time_steps: int
