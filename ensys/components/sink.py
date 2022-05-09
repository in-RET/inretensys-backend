from ensys import EnsysFlow, EnsysConfigContainer


class EnsysSink(EnsysConfigContainer):
    label: str = "Default Sink",
    inputs: dict = None

    def __init__(self,
                 label: str = "Default Sink",
                 inputs: dict[EnsysFlow] = None
                 ):
        """Init the EnsysSink object."""
        super().__init__()
        self.label = label
        self.inputs = inputs
