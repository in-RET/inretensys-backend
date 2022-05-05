from ensys import EnsysFlow
from ensys.common.config import EnsysConfigContainer


class EnsysSink(EnsysConfigContainer):
    label: str = "Default Sink",
    inputs: dict = None

    def __init__(self,
                 label: str = "Default Sink",
                 inputs: dict[EnsysFlow] = None
                 ):
        super().__init__()
        self.label = label
        self.inputs = inputs
