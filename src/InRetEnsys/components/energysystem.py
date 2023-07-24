from typing import List, Union

from InRetEnsys.common.config import InRetEnsysConfigContainer
from InRetEnsys.components.bus import InRetEnsysBus
from InRetEnsys.components.constraints import InRetEnsysConstraints
from InRetEnsys.components.genericstorage import InRetEnsysStorage
from InRetEnsys.components.sink import InRetEnsysSink
from InRetEnsys.components.source import InRetEnsysSource
from InRetEnsys.components.transformer import InRetEnsysTransformer
from InRetEnsys.types import Frequencies
from pydantic import Field


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
    busses: List[InRetEnsysBus] = Field(
        [],
        title='Busses',
        description='List of all busses.',
        lvl_visible=21,
        lvl_edit=42
    )
    
    sinks: List[InRetEnsysSink] = Field(
        [],
        title='Sinks',
        description='List of all sinks.',
        lvl_visible=21,
        lvl_edit=42
    )

    sources: List[InRetEnsysSource] = Field(
        [],
        title='Sources',
        description='List of all Sources.',
        lvl_visible=21,
        lvl_edit=42
    )

    transformers: List[InRetEnsysTransformer] = Field(
        [],
        title='Transformers',
        description='List of all transformers.',
        lvl_visible=21,
        lvl_edit=42
    )

    storages: List[InRetEnsysStorage] = Field(
        [],
        title='Storages',
        description='List of all storages.',
        lvl_visible=21,
        lvl_edit=42
    )

    constraints: List[InRetEnsysConstraints] = Field(
        [],
        title='Constraints',
        description='List of all constraints.',
        lvl_visible=21,
        lvl_edit=42
    )

    frequenz: Frequencies = Field(
        Frequencies.hourly,
        title='Frequency',
        description='Frequency of the timesteps',
        lvl_visible=21,
        lvl_edit=42
    )

    start_date: str = Field(
        title='Start Date',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    time_steps: int = Field(
        title='Time Steps',
        description='Number of timesteps from Startdate',
        lvl_visible=21,
        lvl_edit=42
    )

    def add(self, elem: Union[InRetEnsysSink, InRetEnsysSource, InRetEnsysBus, InRetEnsysStorage, InRetEnsysTransformer, InRetEnsysConstraints]):
        if type(elem) is InRetEnsysSink:
            self.sinks.append(elem)
        elif type(elem) is InRetEnsysSource:
            self.sources.append(elem)
        elif type(elem) is InRetEnsysBus:
            self.busses.append(elem)
        elif type(elem) is InRetEnsysStorage:
            self.storages.append(elem)
        elif type(elem) is InRetEnsysTransformer:
            self.transformers.append(elem)
        elif type(elem) is InRetEnsysConstraints:
            self.constraints.append(elem)
        else:
            raise Exception("Unknown Type given!")
