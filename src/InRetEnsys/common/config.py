from typing import Dict

import pydantic
from oemof import solph
from pydantic import BaseModel, Extra


##  container for a configuration
class InRetEnsysConfigContainer(BaseModel):
    ## pydantic root validator to check and filter all none-type values.
    @pydantic.root_validator(pre=False)
    def check(cls, values):
        retVal = {}

        for value in values:
            if values[value] is not None:
                retVal[value] = values[value]

        return retVal

    ##  pydantic subclass to add special configurations.
    class Config:
        ## Allow arbitrary_types like pandas.DataFrames / pandas.Series which are not allow by default.
        #arbitrary_types_allowed = True

        ## Without this configuration its impossible to pass extra **kwargs to pydantic.baseModel-Objects.
        extra = Extra.allow

    ##  Build a dict of arguments for the init of the oemof objects.
    #   
    #   @return Dictionary with all variables of the given object.
    #   @param self The Object pointer
    #   @param energysystem Oemof-Energysystem
    def build_kwargs(self, energysystem: solph.EnergySystem) -> Dict[str, dict]:
        kwargs = {}
        special_keys = ["inputs", "outputs", "conversion_factors"]

        args = vars(self)

        for key in args:
            value = args[key]
            if key in special_keys:
                oemof_io = {}
                io_keys = list(value.keys())

                for io_key in io_keys:
                    bus = energysystem.groups[io_key]
                    if isinstance(value[io_key], float) or isinstance(value[io_key], list):
                        oemof_io[bus] = value[io_key]
                    else:
                        oemof_io[bus] = value[io_key].to_oemof(energysystem)

                kwargs[key] = oemof_io

            elif key == "nonconvex":
                if isinstance(value, bool):
                    kwargs[key] = value
                else:
                    kwargs[key] = value.to_oemof(energysystem)

            elif key == "investment":                
                kwargs[key] = value.to_oemof(energysystem)

            else: 
                kwargs[key] = value

        return kwargs
