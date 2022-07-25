from oemof import solph
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
    label: str = "Default Storage"
    bus: InRetEnsysBus = None
    diameter: float = 2
    height: float = 5
    temp_h: int = 95
    temp_c: int = 60
    temp_env: int = 10
    u_value = None
    min_storage_level: float = 0.05
    max_storage_level: float = 0.95
    capacity: int = 1
    efficiency: float = 0.9
    marginal_cost: float = 0.0001

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
