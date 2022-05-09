from ensys import EnsysFlow, EnsysInvestment, EnsysConfigContainer


class EnsysStorage(EnsysConfigContainer):
    label: str = "Default Storage"
    inputs: dict = None
    outputs: dict = None
    nominal_storage_capacity: float = None
    invest_relation_input_capacity: float = None
    invest_relation_output_capacity: float = None
    invest_relation_input_output: float = None
    initial_storage_level: float = None
    balanced: bool = True
    loss_rate: float = 0.0
    fixed_losses_relative: float = None
    fixed_losses_absolute: float = None
    inflow_conversion_factor: float = 1
    outflow_conversion_factor: float = 1
    min_storage_level: float = 0
    max_storage_level: float = 1
    investment: EnsysInvestment = None

    def __init__(self,
                 label: str = "Default Storage",
                 inputs: dict[EnsysFlow] = None,
                 outputs: dict[EnsysFlow] = None,
                 nominal_storage_capacity: float = None,
                 invest_relation_input_capacity: float = None,
                 invest_relation_output_capacity: float = None,
                 invest_relation_input_output: float = None,
                 initial_storage_level: float = None,
                 balanced: bool = True,
                 loss_rate: float = 0.0,
                 fixed_losses_relative: float = None,
                 fixed_losses_absolute: float = None,
                 inflow_conversion_factor: float = 1,
                 outflow_conversion_factor: float = 1,
                 min_storage_level: float = None,
                 max_storage_level: float = None,
                 investment: EnsysInvestment = None
                 ):
        """Init the EnsysStorage."""
        super().__init__()

        self.label = label
        self.inputs = inputs
        self.outputs = outputs
        self.nominal_storage_capacity = nominal_storage_capacity
        self.invest_relation_input_capacity = invest_relation_input_capacity
        self.invest_relation_output_capacity = invest_relation_output_capacity
        self.invest_relation_input_output = invest_relation_input_output
        self.initial_storage_level = initial_storage_level
        self.balanced = balanced
        self.loss_rate = loss_rate
        self.fixed_losses_absolute = fixed_losses_absolute
        self.fixed_losses_relative = fixed_losses_relative
        self.inflow_conversion_factor = inflow_conversion_factor
        self.outflow_conversion_factor = outflow_conversion_factor
        self.min_storage_level = min_storage_level
        self.max_storage_level = max_storage_level
        self.investment = investment
