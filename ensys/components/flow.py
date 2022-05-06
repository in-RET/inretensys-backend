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
                 nonconvex: EnsysNonConvex = None
                 ):
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

    def to_oemof(self) -> solph.Flow:
        kwargs = {}

        args = vars(self)

        for key in args:
            value = args[key]

            if key.__contains__("nominal_storage"):
                kwargs[key] = value
            elif value is not None:
                if key == "nonconvex":
                    if value is False or value is True:
                        kwargs[key] = value
                    else:
                        kwargs[key] = value.to_oemof()
                elif key == "investment":
                        kwargs[key] = value.to_oemof()
                else:
                    kwargs[key] = value

        return solph.Flow(**kwargs)



