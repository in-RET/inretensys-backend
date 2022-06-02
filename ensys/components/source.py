from oemof import solph

from ensys import EnsysFlow, EnsysConfigContainer


class EnsysSource(EnsysConfigContainer):
    label: str = "Default Source",
    outputs: dict[str, EnsysFlow] = None

    def __init__(self,
                 label: str = "Default Source",
                 outputs: dict[str, EnsysFlow] = None
                 ):
        """Init the EnsysSource object."""
        super().__init__()
        self.label = label
        self.outputs = outputs

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Source:
        kwargs = self.build_kwargs(energysystem)

        return solph.Source(**kwargs)
