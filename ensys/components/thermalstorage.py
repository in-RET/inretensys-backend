from oemof import solph
from oemof.thermal.facades import StratifiedThermalStorage

from ensys import EnsysConfigContainer, EnsysBus


class EnsysStorage(EnsysConfigContainer):
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

    def __init__(self,
                 label,
                 bus,
                 diameter=2,
                 height=5,
                 temp_h=95,
                 temp_c=60,
                 temp_env=10,
                 u_value=None,
                 min_storage_level=0.05,
                 max_storage_level=0.95,
                 capacity=1,
                 efficiency=0.9,
                 marginal_cost=0.0001
                 ):
        """Init the EnsysStorage."""
        super().__init__()

        self.label = label
        self.bus = bus
        self.diameter = diameter
        self.height = height
        self.temp_h = temp_h
        self.temp_c = temp_c
        self.temp_env = temp_env
        self.u_value = u_value
        self.min_storage_level = min_storage_level
        self.max_storage_level = max_storage_level
        self.capacity = capacity
        self.effiency = efficiency
        self.marginal_cost = marginal_cost

    def to_oemof(self, energysystem: solph.EnergySystem) -> StratifiedThermalStorage:
        kwargs = self.build_kwargs(energysystem)

        return StratifiedThermalStorage(**kwargs)
