from typing import Dict

import pydantic
from oemof import solph
from pydantic import BaseModel, Extra


class EnsysConfigContainer(BaseModel):
    @pydantic.root_validator(pre=False)
    def check(cls, values):
        retVal = {}

        for value in values:
            if values[value] is not None:
                retVal[value] = values[value]

        return retVal

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow

    def to_oemof(self, **kwargs: Dict[str, dict]) -> None:
        """
        Abstract function for subclasses to build the Oemof-Object from an Ensys-Object
        :return: Nothing.
        :rtype: None
        :param kwargs: Dictionary with all arguments from the configuration object.
        :type kwargs: Dict[str, dict]
        """
        pass

    def build_kwargs(self, energysystem: solph.EnergySystem) -> Dict[str, dict]:
        """
        Build a dict of arguments for the init of the oemof objects.

        :return: Dictionary with all variables of the given object.
        :rtype: dict[str, dict]
        :param energysystem: Oemof-Energysystem
        :type energysystem: solph.EnergySystem
        """
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
                if type(value) is bool:
                    kwargs[key] = value
                else:
                    kwargs[key] = value.to_oemof(energysystem)

            elif key == "investment":
                kwargs[key] = value.to_oemof(energysystem)

            else:
                kwargs[key] = value

        return kwargs
