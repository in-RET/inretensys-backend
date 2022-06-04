from typing import Sequence, Union, Dict

import pandas as pd
from oemof import solph

from InRetEnsys import InRetEnsysConfigContainer
from InRetEnsys.components.investment import InRetEnsysInvestment
from InRetEnsys.components.nonconvex import InRetEnsysNonConvex


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

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Flow:
        """
        Return an oemof-object build with the args of the object.
        :return: oemof-Flow-object
        :rtype: solph.Flow
        :param energysystem: the oemof-energysystem to build the kwargs of the object
        :type energysystem: solph.Energysystem
        """
        kwargs = self.build_kwargs(energysystem)

        return solph.Flow(**kwargs)
