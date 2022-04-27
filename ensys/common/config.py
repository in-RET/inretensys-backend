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
