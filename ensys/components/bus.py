from oemof import solph

from ensys import EnsysConfigContainer


class EnsysBus(EnsysConfigContainer):
    label: str = "Default Bus"
    balanced: bool = True

    def __init__(self,
                 label: str = "Default Bus",
                 balanced: bool = True
                 ):
        """Init EnsysBus-Object."""
        super().__init__()
        self.label = label
        self.balanced = balanced

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Bus:
        kwargs = self.build_kwargs(energysystem)

        return solph.Bus(**kwargs)
