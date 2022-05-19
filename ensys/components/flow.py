from oemof import solph

from ensys import EnsysConfigContainer
from ensys.components.investment import EnsysInvestment
from ensys.components.nonconvex import EnsysNonConvex


class EnsysFlow(EnsysConfigContainer):
    nominal_value: float = None
    # numeric or sequence or None
    fix: float = None
    # numeric or sequence
    min: float = 0.0
    # numeric or sequence
    max: float = 1.0
    positive_gradient: dict = None
    negative_gradient: dict = None
    summed_max: float = None
    summed_min: float = None
    variable_costs: float = None
    investment: EnsysInvestment = None
    nonconvex: EnsysNonConvex = None
    emission_factor: float = None
    kwargs: dict = None

    def __init__(self,
                 nominal_value: float = None,
                 # numeric or sequence or None
                 fix: float = None,
                 # numeric or sequence
                 min: float = 0.0,
                 # numeric or sequence
                 max: float = 1.0,
                 positive_gradient: dict = None,
                 negative_gradient: dict = None,
                 summed_max: float = None,
                 summed_min: float = None,
                 variable_costs: float = None,
                 investment: EnsysInvestment = None,
                 nonconvex: EnsysNonConvex = None,
                 emission_factor: float = None,
                 **kwargs
                 ):
        """Init EnsysFlow-Object."""
        super().__init__()
        self.nominal_value = nominal_value
        if fix is not None:
            self.fix = fix
            self.min = None
            self.max = None
        else:
            self.min = min
            self.max = max
        self.positive_gradient = positive_gradient
        self.negative_gradient = negative_gradient
        self.summed_min = summed_min
        self.summed_max = summed_max
        self.variable_costs = variable_costs
        self.investment = investment
        self.nonconvex = nonconvex
        self.emission_factor = emission_factor
        self.kwargs = kwargs

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Flow:
        """Converts the given object to an oemof object."""
        kwargs = self.build_kwargs(energysystem)

        return solph.Flow(**kwargs)
