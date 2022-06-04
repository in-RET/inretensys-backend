import inspect
import pickle

import jsons


class HsnConfigContainer(object):
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return self.to_json()

    def to_json(self):
        return jsons.dumps(self)

    def to_file(self, filename='config.bin'):
        with open(filename, 'wb') as f:
            pickle.dump(
                self,
                f
            )


def config_object_from_file(filename='config.bin'):
    obj = None
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj


def get_function_args(f, l):
    return dict((p.name, l[str(p.name)]) for p in inspect.signature(f).parameters.values() if p.name not in ['kwargs', 'args'])


def set_init_function_args_as_instance_args(s, l):
    args_dict = get_function_args(s.__init__, l)
    for key in args_dict:
        setattr(s, key, args_dict[key])
