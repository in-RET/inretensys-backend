from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args
from oemof import solph


class EnsysInvestment(HsnConfigContainer):
    def __init__(self,
                 label: str = "Default Investment",
                 maximum: float = 0,
                 minimum: float = 0,
                 ep_costs: float = 0,
                 existing: float = 0,
                 nonconvex: bool = False,
                 offset: float = 0,
                 *args,
                 **kwargs,
                 ):
        super().__init__()
        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "param1": "0:0:int:0:10:5"
    }

    def to_oemof(self):
        oemof_investment = solph.Investment(
            label = self.label,
            maximum=self.maximum,
            minimum=self.minimum,
            ep_costs=self.ep_costs,
            existing=self.existing,
            nonconvex=self.nonconvex,
            offset=self.offset
        )

        return oemof_investment