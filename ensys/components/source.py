from ensys import EnsysFlow, EnsysConfigContainer


class EnsysSource(EnsysConfigContainer):
    label: str = "Default Source",
    outputs: dict = None

    def __init__(self,
                 label: str = "Default Source",
                 outputs: dict[EnsysFlow] = None
                 ):
        """Init the EnsysSource object."""
        super().__init__()
        self.label = label
        self.outputs = outputs
