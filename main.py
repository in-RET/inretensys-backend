import os
import inspect
import pandas as pd

import printresults

from configs import basicexample, modifiedexample, oemof_sample
from ensys import EnsysOptimise, EnsysSystembuilder
from ensys.config import EnsysConfigContainer, set_init_function_args_as_instance_args

from verfication import verify


class TestObject(EnsysConfigContainer):

    def __init__(self,
                 label: str = "Default Label",
                 number: float = 0.0,
                 dataFrame: pd.DataFrame = None):
        super().__init__()
        set_init_function_args_as_instance_args(self, locals())


def oemof():
    wkdir = os.path.join(os.getcwd(), "dumps")
    filename = "energy_system"

    configfile = os.path.join(wkdir, filename + ".bin")
    dumpfile = os.path.join(wkdir, filename + ".dump")
    orig_dumpfile = os.path.join(wkdir, filename + "_orig.dump")

    if os.path.exists(configfile):
        os.remove(configfile)

    if os.path.exists(dumpfile):
        os.remove(dumpfile)

    if os.path.exists(orig_dumpfile):
        os.remove(orig_dumpfile)

    ##########################################################################
    # oemof-Beispiel
    ##########################################################################
    if not os.path.exists(orig_dumpfile):
        oemof_sample.oemofSample(orig_dumpfile)

    ##########################################################################
    # ensys-Klassen
    ##########################################################################

    basicexample.CreateSampleConfiguration(configfile)
    # modifiedexample.CreateSampleConfiguration(path_to_dump_config)

    sb = EnsysSystembuilder()

    es = sb.BuildConfiguration(configfile)
    sb.BuildEnergySystem(es, dumpfile)

    verify([dumpfile, orig_dumpfile])

    #EnsysOptimise(dumpfile)
    #printresults.PrintResultsFromDump(dpath=wkdir, dumpfile=dumpfile)


if __name__ == "__main__":
    # oemof()

    test = TestObject(label="Hallo Welt", dataFrame=pd.DataFrame())
    kwargs_str = ""

    for attr in test.__dir__():
        if attr == "dataFrame":
            print(getattr(test, attr))
