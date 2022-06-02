from ensys import EnsysConfigContainer
from ensys.types import Constraints


class EnsysConstraints(EnsysConfigContainer):
    typ: Constraints = None
    var1: object = None
    var2: object = None
    factor1: float = None
    name: str = None
    keyword: str = None
    quantity: object = None
    limit_name: str = None
    components: list = None
    weights: list[float] = None
    limit: float = None
    flows: list = None
    constraint_name: str = None
    upper_limit: int = None
    lower_limit: int = None

    def __init__(self,
                 typ: Constraints,
                 var1=None,
                 var2=None,
                 name=None,
                 factor1=None,
                 keyword: str = None,
                 quantity=None,
                 limit_name=None,
                 components=None,
                 weights=None,
                 limit=None,
                 flows=None,
                 constraint_name=None,
                 upper_limit: int = None,
                 lower_limit: int = None
                 ):
        """Init EnsysConstraint-Object."""
        super().__init__()
        self.typ = typ

        if self.typ == Constraints.shared_limit:
            # Shared_Limit
            self.quantity = quantity
            self.limit_name = limit_name
            self.components = components
            self.weights = weights
            self.lower_limit = lower_limit
            self.upper_limit = upper_limit

        elif self.typ == Constraints.investment_limit:
            # Investment_limit
            self.limit = limit

        elif self.typ == Constraints.additional_investment_flow_limit:
            # Additional_investment_flow_limit
            self.keyword = keyword
            self.limit = limit

        elif self.typ == Constraints.generic_integral_limit:
            # generic_integral_limit
            self.keyword = keyword
            self.flows = flows
            self.limit = limit

        elif self.typ == Constraints.emission_limit:
            # emission_limit
            self.flows = flows
            self.limit = limit

        elif self.typ == Constraints.limit_active_flow_count:
            # limit_active_flow_count
            self.constraint_name = constraint_name
            self.flows = flows
            self.lower_limit = lower_limit
            self.upper_limit = upper_limit

        elif self.typ == Constraints.limit_active_flow_count_by_keyword:
            # limit_active_flow_count_by_keyword
            self.keyword = keyword
            self.lower_limit = lower_limit
            self.upper_limit = upper_limit

        elif self.typ == Constraints.equate_variables:
            # equate_variables
            self.var1 = var1
            self.var2 = var2
            self.factor1 = factor1
            self.name = name

        else:
            # do nothing
            pass

    def to_oemof(self):
        return self.build_kwargs()
