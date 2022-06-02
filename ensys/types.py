from enum import Enum


class CONSTRAINT_TYPES(Enum):
    shared_limit = 0
    investment_limit = 1
    additional_investment_flow_limit = 2
    generic_integral_limit = 3
    emission_limit = 4
    limit_active_flow_count = 5
    limit_active_flow_count_by_keyword = 6
    equate_variables = 7

class FREQUENZ_TYPES(Enum):
    quarter_hourly = 0,
    half_hourly = 1,
    hourly = 2,
    daily = 3,
    weekly = 4,
    monthly = 5