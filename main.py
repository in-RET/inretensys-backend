import os
import pandas as pd
from oemof import solph

from configs import basicexample, oemof_sample
from ensys import EnsysSystembuilder, EnsysBus
from ensys.config import EnsysConfigContainer, set_init_function_args_as_instance_args
from printresults import PrintResultsFromDump
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
    PrintResultsFromDump(dumpfile=dumpfile, output=os.path.join(os.getcwd(), "output", "ensys_out.txt"))
    PrintResultsFromDump(dumpfile=orig_dumpfile, output=os.path.join(os.getcwd(), "output", "oemof_out.txt"))


def testbed():
    comp = solph.Bus(
        label="Default Bus",
        balanced=True
    )
    flow = EnsysBus()

    custom_flow = flow.to_oemof()


    print(comp)
    print(type(comp))
    print(flow)
    print(type(flow))
    print(custom_flow)
    print(type(custom_flow))


if __name__ == "__main__":
    oemof()
    #testbed()

    print(os.path.getsize("dumps/energy_system.dump"))
    print(os.path.getsize("dumps/energy_system_orig.dump"))
















