from oemof import solph

from ensys import EnsysFlow, EnsysConfigContainer


class EnsysTransformer(EnsysConfigContainer):
    label: str = "Default Transformer",
    inputs: dict[str, EnsysFlow]  = None,
    outputs: dict[str, EnsysFlow]  = None,
    conversion_factors: dict = None

    def __init__(self,
                 label: str = "Default Transformer",
                 inputs: dict[str, EnsysFlow] = None,
                 outputs: dict[str, EnsysFlow] = None,
                 conversion_factors=None
                 ):
        """Init the EnsysTransformer object."""
        super().__init__()
        self.label = label
        self.inputs = inputs
        self.outputs = outputs
        self.conversion_factors = conversion_factors

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Transformer:
        kwargs = self.build_kwargs(energysystem)

        return solph.Transformer(**kwargs)
