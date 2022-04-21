from hsncommon.config import HsnConfigContainer, set_init_function_args_as_instance_args
from oemof import solph


class EnsysFlow(HsnConfigContainer):
    def __init__(self,
                 label: str = "Default Flow",
                 nominal_value: float = None,
                 # numeric or sequence or None
                 fix=None,
                 # numeric or sequence
                 min=0.0,
                 # numeric or sequence
                 max=1.0,
                 positive_gradient=None,
                 negative_gradient=None,
                 summed_max: float = None,
                 summed_min=None,
                 variable_costs=None,
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
        "param1": "0:0:int:0:10:5",
        "label": "0:0: type : min : max : 'Default Flow'",
        "nominal_value": "0:0:float: min : max : None",
        "fix": "0:0: type : min : max : None",
        "min": "0:0: type : min : max : None",
        "max": "0:0: type : min : max : None",
        "positive_gradient": "0:0: min : max : None",
        "negative_gradient": "0:0: min : max : None",
        "summed_max": "0:0:float:0:1:None",
        "summed_min": "0:0:float:0:1:None",
        "variable_costs": "0:0:float: min : max : None",
        "investment": "0:0: type : min : max :None",
        "nonconvex": "0:0: type : min : max :None"
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
