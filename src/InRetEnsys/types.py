from enum import Enum
##  File which contains all enumeration of the package.
#   
#   @file


##  Enumeration for all selectable Constraints which can be added to an PyOmo-Model.
#
class Constraints(Enum):
    ## Adds a constraint to the given model that restricts the weighted sum of variables to a corridor.
    shared_limit = 0
    ## Set an absolute limit for the total investment costs of an investment optimization problem:
    investment_limit = 1
    ## Global limit for investment flows weighted by an attribute keyword.
    #  This constraint is only valid for Flows not for components such as an investment storage.
    #  The attribute named by keyword has to be added to every Investment attribute of the flow you want to take into account. Total value of keyword attributes after optimization can be retrieved calling the oemof.solph.Model.invest_limit_${keyword}().
    #  \f[ {\sum_{i \in IF}  P_i \cdot w_i \leq limit} \f]
    # With IF being the set of InvestmentFlows considered for the integral limit.
    additional_investment_flow_limit = 2
    ## Set a global limit for flows weighted by attribute called keyword. The attribute named by keyword has to be added to every flow you want to take into account.
    generic_integral_limit = 3
    ## Short handle for generic_integral_limit() with keyword=”emission_factor”.
    emission_limit = 4
    ## Set limits (lower and/or upper) for the number of concurrently active NonConvex flows. The flows are given as a list.
    limit_active_flow_count = 5
    ## This wrapper for limit_active_flow_count allows to set limits to the count of concurrently active flows by using a keyword instead of a list. The constraint will be named $(keyword)_count.
    limit_active_flow_count_by_keyword = 6
    ## Adds a constraint to the given model that set two variables to equal adaptable by a factor.
    equate_variables = 7


##  Enumeration for the frequenz of the pandas.date_range needed by the oemof energysystem.
#   
class Frequencies(Enum):
    ## Timestep is 15 Minutes
    quarter_hourly = 0,
    
    ## Timestep is 30 Minutes
    half_hourly = 1,
    
    ## Timestep is 60 Minutes
    hourly = 2,

    ## Timestep is 24 Hours
    daily = 3,
    
    ## Timestep is 7 Days
    weekly = 4,
    
    ## Timestep is 30 Days
    monthly = 5


##  Enumeration for all selectable solvers.
#
#   gurobi is the default solver of a InRetEnsys-Model, but it requires a license.
#   cbc is freely avaiable but not so performant.
class Solver(Enum):
    ## COIN-OR Branch-and-Cut Solver
    cbc = 0,

    ## Gurobi MILP Solver
    gurobi = 1,
    
    ## Gurobi MILP Solver
    gurobi_direct = 2,

    ## GNU Linear Programming Kit Solver
    glpk = 3,

    ## IBM ILOG CPLEX Optimization
    cplex = 4,

    ## kiwisolver from pypi
    kiwi = 5
