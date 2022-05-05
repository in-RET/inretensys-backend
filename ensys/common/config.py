import logging

from pydantic import BaseModel


class EnsysConfigContainer(BaseModel):
    def __init__(self):
        super().__init__()

    def to_oemof(self):
        pass


def BuildKwargs(obj):
    kwargs = {}

    args = vars(obj)
    except_keys = [""]

    for key in args:
        if key is not None or key in except_keys:
            value = args[key]

            kwargs[key] = value
        else:
            logging.warning("Is None: " + str(key) + ": " + str(args[key]))

    return kwargs
