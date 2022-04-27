from oemof import solph

from ensys.common.config import EnsysConfigContainer, set_init_function_args_as_instance_args


class EnsysFlow(EnsysConfigContainer):
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

        if fix is not None:
            min=None
            max=None

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

    def to_oemof(self):
        kwargs = {}

        for attr_name in dir(self):
            if not attr_name.startswith("__") and \
                    not attr_name.startswith("to_") and \
                    not attr_name == "format":
                name = attr_name
                value = getattr(self, attr_name)

                kwargs[name] = value

        oemof_obj = solph.Flow(**kwargs)

        return oemof_obj



