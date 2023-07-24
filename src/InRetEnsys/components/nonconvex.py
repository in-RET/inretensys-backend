from typing import Dict

from InRetEnsys import InRetEnsysConfigContainer
from oemof import solph
from pydantic import Field


##  Container which contains the params for an InRetEnsys-NonConvex-Object
#   
#   @param startup_costs: float] = None
#   @param shutdown_costs: float] = None
#   @param activity_costs: float] = None
#   @param minimum_uptime: int] = None
#   @param minimum_downtime: int] = None
#   @param maximum_startups: int] = None
#   @param maximum_shutdowns: int] = None
#   @param initial_status: int = 0
#   @param positive_gradient: Dict] = None
#   @param negative_gradient: Dict] = None
#   @param startup_costs: float] = None
#   @param shutdown_costs: float] = None
#   @param activity_costs: float] = None
#   @param minimum_uptime: int] = None
#   @param minimum_downtime: int] = None
#   @param maximum_startups: int] = None
#   @param maximum_shutdowns: int] = None
#   @param initial_status: int = 0
#   @param positive_gradient: Dict] = None
#   @param negative_gradient: Dict] = None
class InRetEnsysNonConvex(InRetEnsysConfigContainer):
    startup_costs: float = Field(
        None,
        title='Startups Costs',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    shutdown_costs: float = Field(
        None,
        title='Shutdown Costs',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )
    
    activity_costs: float = Field(
        None,
        title='Activity Costs',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    minimum_uptime: int = Field(
        None,
        title='Minimum Uptime',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )
    minimum_downtime: int = Field(
        None,
        title='Minimum Downtime',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    maximum_startups: int = Field(
        None,
        title='Maximum Startups',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    maximum_shutdowns: int = Field(
        None,
        title='Maximum Shutdowns',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    # 0/False = off, 1/True = on
    initial_status: int = Field(
        0,
        title='initial Status',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )
    positive_gradient: Dict = Field(
        None,
        title='positive Gradient',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    negative_gradient: Dict = Field(
        None,
        title='negative Gradient',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    ##  Returns an oemof-object from the given args of this object.
    #
    #   Builts a dictionary with all keywords given by the object and returns the oemof object initialised with these 'kwargs'.
    #
    #   @param self The Object Pointer
    #   @param energysystem The oemof-Energysystem to reference other objects i.e. for flows.
    #   @return solph.NonConvex-Object (oemof)
    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.NonConvex:
        kwargs = self.build_kwargs(energysystem)

        return solph.NonConvex(**kwargs)
