from typing import Dict, Sequence, Union

from InRetEnsys import InRetEnsysConfigContainer
from InRetEnsys.components.investment import InRetEnsysInvestment
from InRetEnsys.components.nonconvex import InRetEnsysNonConvex
from oemof import solph
from pydantic import Field


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
#   @param custom_attributes Keyword-Arguments for special Keywords, used by constraints.
class InRetEnsysFlow(InRetEnsysConfigContainer):
    nominal_value: float = Field(
        None,
        title='Nominal Value',
        description='The nominal value of the flow. If this value is set the corresponding optimization variable of '
                    'the flow object will be bounded by this value multiplied with min(lower bound)/max(upper bound).',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0.0,
        step=1e-3
    )

    # numeric or sequence or None
    fix: Union[float, Sequence[float]] = Field(
        None,
        title='Fix',
        description='Normed fixed value for the flow variable. '
                    'Will be multiplied with the nominal_value to get the absolute value',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0.0,
        step=1e-5
    )

    # numeric or sequence
    min: Union[float, Sequence[float]] = Field(
        None,
        title='Minimum',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0.0,
        step=1e-3
    )

    # numeric or sequence
    max: Union[float, Sequence[float]] = Field(
        None,
        title='Maximum',
        description='',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0.0,
        step=1e-3
    )

    positive_gradient: Dict = Field(
        None,
        title='Positive Gradient',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )
    negative_gradient: Dict = Field(
        None,
        title='Negative Gradient',
        description='',
        lvl_visible=21,
        lvl_edit=42
    )

    summed_max: float = Field(
        None,
        title='Summed Maximum',
        description='Specific maximum value summed over all timesteps. '
                    'Will be multiplied with the nominal_value to get the absolute limit.',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0.0,
        step=1e-3
    )

    summed_min: float = Field(
        None,
        title='Summed Minimum',
        description='Specific minimum value summed over all timesteps. '
                    'Will be multiplied with the nominal_value to get the absolute limit.',
        lvl_visible=21,
        lvl_edit=42,
        le=float("+inf"),
        ge=0.0,
        step=1e-3
    )

    variable_costs: Union[float, Sequence[float]] = Field(
        None,
        title='Variable Costs',
        description='The costs associated with one unit of the flow.',
        lvl_visible=21,
        lvl_edit=42,
        #le=float("+inf"),
        #ge=0.0,
        #step=1e-3
    )

    investment: InRetEnsysInvestment = Field(
        None,
        title='Investment',
        description='Object indicating if a nominal_value of the flow is determined by the optimization problem.',
        lvl_visible=21,
        lvl_edit=42
    )

    nonconvex: InRetEnsysNonConvex = Field(
        None,
        title='Nonconvex',
        description='If a nonconvex flow object is added here, the flow constraints will be altered significantly as '
                    'the mathematical model for the flow will be different, i.e. constraint etc. from NonConvexFlow '
                    'will be used instead of Flow. ',
        lvl_visible=21,
        lvl_edit=42
    )

    custom_attributes: dict = Field(
        {},
        title="Custom Attributes",
        description="Custom Attributes as dictionary for custom investment limits.",
        lvl_visible=21,
        lvl_edit=42
    )

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
    

class SensitivityInRetEnsysFlow(InRetEnsysFlow):
    pass