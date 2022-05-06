from oemof import solph

from ensys import EnsysConfigContainer
from ensys.common.config import BuildKwargs


class EnsysNonConvex(EnsysConfigContainer):
    startup_costs: float = None
    shutdown_costs: float = None
    activity_costs: float = None
    minimum_uptime: int = None
    minimum_downtime: int = None
    maximum_startups: int = None
    maximum_shutdowns: int = None
    # 0/False = off, 1/True = on
    initial_status: int = 0
    positive_gradient: dict = None
    negative_gradient: dict = None

    def __init__(self,
                 startup_costs=None,
                 shutdown_costs=None,
                 activity_costs=None,
                 minimum_uptime: int = None,
                 minimum_downtime: int = None,
                 maximum_startups: int = None,
                 maximum_shutdowns: int = None,
                 # 0/False = off, 1/True = on
                 initial_status: int = 0,
                 positive_gradient: dict = None,
                 negative_gradient: dict = None
                 ):
        super().__init__()
        self.startup_costs = startup_costs
        self.shutdown_costs = shutdown_costs
        self.activity_costs = activity_costs
        self.minimum_uptime = minimum_uptime
        self.minimum_downtime = minimum_downtime
        self.maximum_startups = maximum_startups
        self.maximum_shutdowns = maximum_shutdowns
        self.initial_status = initial_status

        if positive_gradient is None:
            self.positive_gradient = {"ub": None, "costs": 0}
        else:
            self.positive_gradient = positive_gradient

        if negative_gradient is None:
            self.negative_gradient = {"ub": None, "costs": 0}
        else:
            self.negative_gradient = negative_gradient

    def to_oemof(self) -> solph.NonConvex:
        kwargs = BuildKwargs(self)

        return solph.NonConvex(**kwargs)
