from oemof import solph
from pydantic import Field
from oemof.thermal.facades import StratifiedThermalStorage
from InRetEnsys import InRetEnsysConfigContainer, InRetEnsysBus


##  Container which contains the params for an InRetEnsys-ThermalStorage-Object
#   
#   @param label: str = "Default Storage"
#   @param bus: InRetEnsysBus = None,
#   @param diameter: float = 2,
#   @param height: float = 5,
#   @param temp_h: int = 95,
#   @param temp_c: int = 60,
#   @param temp_env: int = 10,
#   @param u_value = None,
#   @param min_storage_level: float = 0.05,
#   @param max_storage_level: float = 0.95,
#   @param capacity: int = 1,
#   @param efficiency: float = 0.9,
#   @param marginal_cost: float = 0.0001
class InRetEnsysThermalStorage(InRetEnsysConfigContainer):
    label: str = Field(
        "Default Storage",
        title='Label',
        description='Label',
        lvl_visible=21,
        lvl_edit=42
    )

    bus: InRetEnsysBus = Field(
        None,
        title='Bus',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    diameter: float = Field(
        2,
        title='Diameter',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    height: float = Field(
        5,
        title='Height',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    temp_h: int = Field(
        95,
        title='Temp H',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    temp_c: int = Field(
        60,
        title='Temp C',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    temp_env: int = Field(
        10,
        title='Temp Environment',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    u_value = Field(
        None,
        title='u_value',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    min_storage_level: float = Field(
        0.05,
        title='Minimum storage level',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0.0,
        step=1e-3
    )

    max_storage_level: float = Field(
        0.95,
        title='Maximum storage level',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0.0,
        step=1e-3
    )

    capacity: int = Field(
        1,
        title='Capacity',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0,
        step=1
    )

    efficiency: float = Field(
        0.9,
        title='Efficiency',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0.0,
        step=1e-3
    )

    marginal_cost: float = Field(
        0.0001,
        title='marginal costs',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0.0,
        step=1e-3
    )

    ##  Returns an oemof-object from the given args of this object.
    #
    #   Builts a dictionary with all keywords given by the object and returns the oemof object initialised with these 'kwargs'.
    #
    #   @param self The Object Pointer
    #   @param energysystem The oemof-Energysystem to reference other objects i.e. for flows.
    #   @return solph.thermal.StratifiedThermalStorage-Object (oemof)
    def to_oemof(self, energysystem: solph.EnergySystem) -> StratifiedThermalStorage:
        kwargs = self.build_kwargs(energysystem)

        return StratifiedThermalStorage(**kwargs)
