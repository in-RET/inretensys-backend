from typing import Union

from src.InRetEnsys.common.config import InRetEnsysConfigContainer
from src.InRetEnsys.components.bus import InRetEnsysBus
from src.InRetEnsys.components.constraints import InRetEnsysConstraints
from src.InRetEnsys.components.genericstorage import InRetEnsysStorage
from src.InRetEnsys.components.sink import InRetEnsysSink
from src.InRetEnsys.components.source import InRetEnsysSource
from src.InRetEnsys.components.transformer import InRetEnsysTransformer
from src.InRetEnsys.types import Frequencies

##  Container which contains the params for an InRetEnergysystem
#   
#   @param busses
#   @param sinks
#   @param sources
#   @param transformers
#   @param storages
#   @param constraints
#   @param frequenz
#   @param start_date
#   @param time_steps
class InRetEnsysEnergysystem(InRetEnsysConfigContainer):
    busses: Union[None, list[InRetEnsysBus]] = None
    sinks: Union[None, list[InRetEnsysSink]] = None
    sources: Union[None, list[InRetEnsysSource]] = None
    transformers: Union[None, list[InRetEnsysTransformer]] = None
    storages: Union[None, list[InRetEnsysStorage]] = None
    constraints: Union[None, list[InRetEnsysConstraints]] = None
    frequenz: Frequencies = Frequencies.hourly
    start_date: str
    # 24 * 7 * 52
    time_steps: int
