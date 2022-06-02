from oemof import solph

from ensys import EnsysFlow, EnsysConfigContainer


class EnsysSink(EnsysConfigContainer):
    label: str = "Default Sink",
    inputs: dict[str, EnsysFlow] = None

    def __init__(self,
                 label: str = "Default Sink",
                 inputs: dict[str, EnsysFlow] = None
                 ):
        """Init the EnsysSink object."""
        super().__init__()
        self.label = label
        self.inputs = inputs

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Sink:
        kwargs = self.build_kwargs(energysystem)

        return solph.Sink(**kwargs)
