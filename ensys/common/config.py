from pydantic import BaseModel


class EnsysConfigContainer(BaseModel):
    def __init__(self):
        """Default config container."""
        super().__init__()

    def to_oemof(self, **kwargs):
        pass

    def build_kwargs(self, energysystem=None):
        """Build a dict of arguments for the init of the oemof objects."""
        kwargs = {}
        special_keys = ["inputs", "outputs", "conversion_factors"]

        args = vars(self)

        for key in args:
            value = args[key]
            if value is not None and key != "typ":
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
                    if value is False or value is True:
                        kwargs[key] = value
                    else:
                        kwargs[key] = value.to_oemof(energysystem)

                elif key == "investment":
                    kwargs[key] = value.to_oemof(energysystem)

                elif key == "kwargs":
                    for arg in args[key]:
                        kwargs[arg] = args[key][arg]

                else:
                    kwargs[key] = value

        return kwargs
