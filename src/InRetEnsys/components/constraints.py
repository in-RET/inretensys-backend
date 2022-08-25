from typing import Union, List, Dict
from pydantic import Field

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
    typ: Constraints = Field(
        None,
        title='Typ',
        description='Type of the constraint.',
        lvl_visible=21,
        lvl_edit=42
    )

    var1: object = Field(
        None,
        title='var1',
        description='First variable, to be set to equal with Var2 and multiplied with factor1.',
        lvl_visible=21,
        lvl_edit=42
    )

    var2: object = Field(
        None,
        title='var2',
        description='Second variable, to be set equal to (Var1 * factor1).',
        lvl_visible=21,
        lvl_edit=42
    )

    factor1: float = Field(
        None,
        title='factor1',
        description='Factor to define the proportion between the variables.',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0.0,
        step=1e-3
    )

    name: str = Field(
        None,
        title='Name',
        description='Optional name',
        lvl_visible=21,
        lvl_edit=42
    )

    keyword: str = Field(
        None,
        title='Keyword',
        description='Keyword to consider (searches all NonConvexFlows)',
        lvl_visible=21,
        lvl_edit=42
    )

    quantity: object = Field(
        None,
        title='Quantity',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    limit_name: str = Field(
        None,
        title='Limit Name',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    components: List = Field(
        None,
        title='Components',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    weights: List[float] = Field(
        None,
        title='Weights',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0.0,
        step=1e-3
    )

    limit: float = Field(
        None,
        title='Limit',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0,
        step=1e-3
    )

    flows: Union[List, dict] = Field(
        None,
        title='Flows',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    constraint_name: str = Field(
        None,
        title='constraint name',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    upper_limit: int = Field(
        None,
        title='Upper Limit',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0,
        step=1e-3
    )

    lower_limit: int = Field(
        None,
        title='Lower Limit',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0,
        step=1e-3
    )

    ##  Returns a dictionary of the given args of this object.
    #
    #   @param self The Object Pointer
    #   @return dictionary of kwargs 
    def to_oemof(self) -> Dict[str, dict]:
        args = {}
        for var in vars(self):
            if var != "typ":
                args[var] = vars(self)[var]

        return args
