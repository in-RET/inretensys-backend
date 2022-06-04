from typing import Union, List, Dict

from InRetEnsys import InRetEnsysConfigContainer
from InRetEnsys.types import Constraints


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
    flows: Union[None, list] = None
    constraint_name: Union[None, str] = None
    upper_limit: Union[None, int] = None
    lower_limit: Union[None, int] = None

    def to_oemof(self) -> Dict[str, dict]:
        """
        :return: Dictionary with all arguments.
        :rtype: Dict[str, dict]
        """
        args = {}
        for var in vars(self):
            if var != "typ":
                args[var] = vars(self)[var]

        return args
