from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args
from oemof import solph


class EnsysFlow(HsnConfigContainer):
    def __init__(self,
                 label: str = "Default Flow",
                 nominal_value: float = None,
                 fix: float = None,
                 min: float = 0.0,
                 max: float = 1.0,
                 positive_gradient=None,
                 negative_gradient=None,
                 summed_max: float = 1.0,
                 summed_min: float = 0.0,
                 variable_costs: float = 0.0,
                 investment: solph.Investment = None,
                 nonconvex: solph.NonConvex = None,
                 *args,
                 **kwargs
                 ):
        super().__init__()

        if positive_gradient is None:
            positive_gradient = {"ub": None, "costs": 0}

        if negative_gradient is None:
            negative_gradient = {"ub": None, "costs": 0}

        # TODO: Hier sollte was sinnvolles sein
        if nonconvex is not None:
            investment = None

        if investment is not None:
            nominal_value = None
            nonconvex = None

        set_init_function_args_as_instance_args(self, locals())

    format = {
        # name : 0: 0: type: min: max: default
        "param1": "0:0:int:0:10:5"
    }


    def to_oemof(self):
        if self.fix is not None:
            oemof_flow = solph.Flow(
                label=self.label,
                nominal_value=self.nominal_value,
                fix=self.fix,
                positive_gradient=self.positive_gradient,
                negative_gradient=self.negative_gradient,
                summed_max=self.summed_max,
                summed_min=self.summed_min,
                variable_costs=self.variable_costs,
                investment=self.investment,
                nonconvex=self.nonconvex
            )
        else:
            oemof_flow = solph.Flow(
                label=self.label,
                nominal_value=self.nominal_value,
                max=self.max,
                min=self.min,
                positive_gradient=self.positive_gradient,
                negative_gradient=self.negative_gradient,
                summed_max=self.summed_max,
                summed_min=self.summed_min,
                variable_costs=self.variable_costs,
                investment=self.investment,
                nonconvex=self.nonconvex
            )

        return oemof_flow
