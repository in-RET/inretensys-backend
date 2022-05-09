from oemof import solph

from ensys import EnsysConfigContainer
from ensys.common.config import BuildKwargs


class EnsysInvestment(EnsysConfigContainer):
    maximum: float = float("+inf")
    minimum: float = 0.0
    ep_costs: float = 0.0
    existing: float = 0.0
    nonconvex: bool = False
    offset: float = 0.0

    def __init__(self,
                 maximum: float = float("+inf"),
                 minimum: float = 0.0,
                 ep_costs: float = 0.0,
                 existing: float = 0.0,
                 nonconvex: bool = False,
                 offset: float = 0.0
                 ):
        """Init the EnsysInvestment object."""
        super().__init__()
        self.maximum = maximum
        self.minimum = minimum
        self.ep_costs = ep_costs
        self.existing = existing
        self.nonconvex = nonconvex
        self.offset = offset

    def to_oemof(self) -> solph.Investment:
        """Converts the given object to an oemof object."""
        kwargs = BuildKwargs(self)

        return solph.Investment(**kwargs)
