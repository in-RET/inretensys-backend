# ConfigContainer

## Code
```python linenums='1' title="config.py"
from hsncommon.config import HsnConfigContainer, get_function_args


class EnsysConfigContainer(HsnConfigContainer):
    def __init__(self):
        super().__init__()

    def to_oemof(self):
        pass


def set_init_function_args_as_instance_args(s, l):
    args_dict = get_function_args(s.__init__, l)
    execpt_keys = ["timeincrement", "initial_storage_level"]
    for key in args_dict:
        if key in execpt_keys or args_dict[key] is not None:
            setattr(s, key, args_dict[key])
```

## Parentclass
The parent class of the EnsysConfigurationContainer is the 'HsnConfigContainer' which was provided from Carsten Heise, member if the University of Applied Science Nordhausen - IAE.

## Functions

### to_oemof(self)
A object function for later use in child-classes, i.e. EnsysFlow, to implement a call to directly return an oemof.solph-Object.

### set_init_function_args_as_instance_args(s, l)
A function that overrides the given function from the 'HsnConfigContainer'.
This function only adds arguments with a given value or if there are in the list of the excepted keynames.