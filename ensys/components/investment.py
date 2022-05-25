from oemof import solph

from ensys import EnsysConfigContainer


class EnsysInvestment(EnsysConfigContainer):
    maximum: float = float("+inf")
    minimum: float = 0.0
    ep_costs: float = 0.0
    existing: float = 0.0
    nonconvex: bool = False
    offset: float = 0.0
    kwargs: dict = None

    def __init__(self,
                 maximum: float = float("+inf"),
                 minimum: float = 0.0,
                 ep_costs: float = 0.0,
                 existing: float = 0.0,
                 nonconvex: bool = False,
                 offset: float = 0.0,
                 **kwargs
                 ):
        """Init the EnsysInvestment object."""
        super().__init__()
        self.maximum = maximum
        self.minimum = minimum
        self.ep_costs = ep_costs
        self.existing = existing
        self.nonconvex = nonconvex
        self.offset = offset
        self.kwargs = kwargs

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Investment:
        """Converts the given object to an oemof object."""
        kwargs = self.build_kwargs(energysystem)

        return solph.Investment(**kwargs)
