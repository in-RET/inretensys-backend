from oemof import solph

from ensys import EnsysConfigContainer
from ensys.common.config import BuildKwargs


class EnsysBus(EnsysConfigContainer):
    label: str = "Default Bus"
    balanced: bool = True

    def __init__(self,
                 label: str = "Default Bus",
                 balanced: bool = True
                 ):
        super().__init__()
        self.label = label
        self.balanced = balanced

    def to_oemof(self) -> solph.Bus:
        kwargs = BuildKwargs(self)

        return solph.Bus(**kwargs)
