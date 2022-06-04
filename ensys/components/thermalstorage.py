from oemof import solph
from oemof.thermal.facades import StratifiedThermalStorage

from ensys import EnsysConfigContainer, EnsysBus


class EnsysThermalStorage(EnsysConfigContainer):
    label: str = "Default Storage"
    bus: EnsysBus = None,
    diameter: float = 2,
    height: float = 5,
    temp_h: int = 95,
    temp_c: int = 60,
    temp_env: int = 10,
    u_value = None,
    min_storage_level: float = 0.05,
    max_storage_level: float = 0.95,
    capacity: int = 1,
    efficiency: float = 0.9,
    marginal_cost: float = 0.0001

    def to_oemof(self, energysystem: solph.EnergySystem) -> StratifiedThermalStorage:
        """
        Return an oemof-object build with the args of the object.
        :return: oemof-StratifiedThermalStorage-object
        :rtype: solph.StratifiedThermalStorage
        :param energysystem: the oemof-energysystem to build the kwargs of the object
        :type energysystem: solph.Energysystem
        """
        kwargs = self.build_kwargs(energysystem)

        return StratifiedThermalStorage(**kwargs)
