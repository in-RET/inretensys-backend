from pydantic import BaseModel


def BuildKwargs(obj):
    kwargs = {}

    for attr_name in dir(obj):
        if not attr_name.startswith("__") and \
                not attr_name.startswith("to_") and \
                not attr_name == "format":
            name = attr_name
            value = getattr(obj, attr_name)

            kwargs[name] = value

    return kwargs


class EnsysConfigContainer(BaseModel):
    def __init__(self):
        super().__init__()

    def to_oemof(self):
        pass