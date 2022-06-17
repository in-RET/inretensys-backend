from typing import Union, List
from InRetEnsys.common.config import InRetEnsysConfigContainer
from InRetEnsys.components.bus import InRetEnsysBus
from InRetEnsys.components.constraints import InRetEnsysConstraints
from InRetEnsys.components.genericstorage import InRetEnsysStorage
from InRetEnsys.components.sink import InRetEnsysSink
from InRetEnsys.components.source import InRetEnsysSource
from InRetEnsys.components.transformer import InRetEnsysTransformer
from InRetEnsys.types import Frequencies


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
    busses: Union[None, List[InRetEnsysBus]] = None
    sinks: Union[None, List[InRetEnsysSink]] = None
    sources: Union[None, List[InRetEnsysSource]] = None
    transformers: Union[None, List[InRetEnsysTransformer]] = None
    storages: Union[None, List[InRetEnsysStorage]] = None
    constraints: Union[None, List[InRetEnsysConstraints]] = None
    frequenz: Frequencies = Frequencies.hourly
    start_date: str
    # 24 * 7 * 52
    time_steps: int
