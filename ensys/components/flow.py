from oemof import solph

import ensys.components.investment
import ensys.components.nonconvex
from ensys.common.config import EnsysConfigContainer


class EnsysFlow(EnsysConfigContainer):
    label: str = "Default Flow"
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
    investment: ensys.components.investment.EnsysInvestment = None
    nonconvex: ensys.components.nonconvex.EnsysNonConvex = None

    def __init__(self,
                 label: str = "Default Flow",
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
                 investment: ensys.components.investment.EnsysInvestment = None,
                 nonconvex: ensys.components.nonconvex.EnsysNonConvex = None
                 ):
        super().__init__()
        self.label = label
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

        for attr_name in dir(self):
            if not attr_name.startswith("__") and \
                    not attr_name.startswith("to_") and \
                    not attr_name == "format":
                name = attr_name
                value = getattr(self, attr_name)

                if name.__contains__("nominal_storage"):
                    kwargs[name] = value
                elif value is not None:
                    if name == "nonconvex":
                        if value is False or value is True:
                            kwargs[name] = value
                        else:
                            kwargs[name] = value.to_oemof()
                    elif name == "investment":
                            kwargs[name] = value.to_oemof()
                    else:
                        kwargs[name] = value

        return solph.Flow(**kwargs)



