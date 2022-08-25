from typing import Union, List
from pydantic import Field
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
    busses: List[InRetEnsysBus] = Field(
        None,
        title='Busses',
        description='List of all busses.',
        lvl_visible=21,
        lvl_edit=42
    )
    
    sinks: List[InRetEnsysSink] = Field(
        None,
        title='Sinks',
        description='List of all sinks.',
        lvl_visible=21,
        lvl_edit=42
    )

    sources: List[InRetEnsysSource] = Field(
        None,
        title='Sources',
        description='List of all Sources.',
        lvl_visible=21,
        lvl_edit=42
    )

    transformers: List[InRetEnsysTransformer] = Field(
        None,
        title='Transformers',
        description='List of all transformers.',
        lvl_visible=21,
        lvl_edit=42
    )

    storages: List[InRetEnsysStorage] = Field(
        None,
        title='Storages',
        description='List of all storages.',
        lvl_visible=21,
        lvl_edit=42
    )

    constraints: List[InRetEnsysConstraints] = Field(
        None,
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
        None,
        title='Start Date',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    time_steps: int = Field(
        None,
        title='Time Steps',
        description='Number of timesteps from Startdate',
        lvl_visible=21,
        lvl_edit=42,
        ge=0,
        le=float("+inf")
    )
