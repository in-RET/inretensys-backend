from typing import Sequence, Union, Dict

import pandas as pd
from oemof import solph

from src.InRetEnsys import InRetEnsysConfigContainer
from src.InRetEnsys.components.investment import InRetEnsysInvestment
from src.InRetEnsys.components.nonconvex import InRetEnsysNonConvex

##  Container which contains the params for an oemof-flow
#   
#   @param nominal_value 
#   @param fix
#   @param min
#   @param max
#   @param positive_gradient
#   @param negative_gradient 
#   @param summed_max
#   @param summed_min 
#   @param variable_costs 
#   @param investement InRetEnsys-Investment-Object, if the Flow should be optimized for an Investmentlimit.
#   @param nonconvex InRetEnsys-NonConvex-Object, if the Flow should be nonconvex. Non possible if the flow is an Investmentflow. 
#   @param kwargs Keyword-Arguments for special Keywords, used by constraints.
class InRetEnsysFlow(InRetEnsysConfigContainer):
    nominal_value: Union[None, float] = None
    # numeric or sequence or None
    fix: Union[None, float, Sequence, pd.Series] = None
    # numeric or sequence
    min: Union[None, float, Sequence, pd.Series] = None
    # numeric or sequence
    max: Union[None, float, Sequence, pd.Series] = None
    positive_gradient: Union[None, Dict] = None
    negative_gradient: Union[None, Dict] = None
    summed_max: Union[None, float] = None
    summed_min: Union[None, float] = None
    variable_costs: Union[None, float, Sequence, pd.Series] = None
    investment: Union[None, InRetEnsysInvestment] = None
    nonconvex: Union[None, InRetEnsysNonConvex] = None
    kwargs: Union[None, Dict] = None

    ##  Returns an oemof-object from the given args of this object.
    #
    #   Builts a dictionary with all keywords given by the object and returns the oemof object initialised with these 'kwargs'.
    #
    #   @param self The Object Pointer
    #   @param energysystem The oemof-Energysystem to reference other objects i.e. for flows.
    #   @return solph.Flow-Object (oemof)
    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Flow:
        kwargs = self.build_kwargs(energysystem)

        return solph.Flow(**kwargs)
