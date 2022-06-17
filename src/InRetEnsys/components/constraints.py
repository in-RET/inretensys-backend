from typing import Union, List, Dict
from InRetEnsys import InRetEnsysConfigContainer
from InRetEnsys.types import Constraints


##  Container which contains the params for constraints
#   
#   @param typ Type of the Constraints, all possible types are given in the Enum types.Constraints
#   @param var1 (pyomo.environ.Var) – First variable, to be set to equal with Var2 and multiplied with factor1.
#   @param var2 (pyomo.environ.Var) – Second variable, to be set equal to @f$Var1 * factor1@f$.
#   @param factor1 (float) – Factor to define the proportion between the variables.
#   @param name (str) – Optional name for the equation e.g. in the LP file. By default the name is: equate + string representation of var1 and var2.
#   @param keyword (string) – keyword to consider (searches all NonConvexFlows)
#   @param quantity (pyomo.core.base.var.IndexedVar) – Shared Pyomo variable for all components of a type.
#   @param limit_name (string) – Name of the constraint to create
#   @param components (list of components) – list of components of the same type
#   @param weights (list of numeric values) – has to have the same length as the list of components
#   @param limit (numeric) – Absolute limit of keyword attribute for the energy system.
#   @param flows (list of flows) – flows (have to be NonConvex) in the format [(in, out)]
#   @param constraint_name (string) – name for the constraint
#   @param upper_limit (integer) – maximum number of active flows in the list
#   @param lower_limit (integer) – minimum number of active flows in the list
class InRetEnsysConstraints(InRetEnsysConfigContainer):
    typ: Union[None, Constraints] = None
    var1: Union[None, object] = None
    var2: Union[None, object] = None
    factor1: Union[None, float] = None
    name: Union[None, str] = None
    keyword: Union[None, str] = None
    quantity: Union[None, object] = None
    limit_name: Union[None, str] = None
    components: Union[None, List] = None
    weights: Union[None, List[float]] = None
    limit: Union[None, float] = None
    flows: Union[None, List, dict] = None
    constraint_name: Union[None, str] = None
    upper_limit: Union[None, int] = None
    lower_limit: Union[None, int] = None

    ##  Returns an dictionary of the given args of this object.
    #
    #   @param self The Object Pointer
    #   @return dictionary of kwargs 
    def to_oemof(self) -> Dict[str, dict]:
        args = {}
        for var in vars(self):
            if var != "typ":
                args[var] = vars(self)[var]

        return args
