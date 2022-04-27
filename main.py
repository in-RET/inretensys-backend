import os
import pandas as pd

from configs import basic_sample, oemof_sample, oemof_allround_sample, allround_sample
from ensys import EnsysSystembuilder
from ensys.common.config import EnsysConfigContainer, set_init_function_args_as_instance_args
from ensys.common.output import PrintResultsFromDump
from ensys.common.verfication import Verification
from hsncommon.log import HsnLogger
from pydantic import BaseModel


class TestObject(BaseModel, EnsysConfigContainer):
    label: str
    number: float

    def __init__(self,
                 label: str = "Default Label",
                 number: float = 0.0):
        super().__init__()
        self.label = label
        self.number = number

        set_init_function_args_as_instance_args(self, locals())


def oemof(goOemof, goEnsys):
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

    logger = HsnLogger()
    verify = Verification

    ##########################################################################
    # oemof-Beispiel
    ##########################################################################
    if goOemof:
        # if not os.path.exists(orig_dumpfile):
        #     oemof_sample.oemofSample(orig_dumpfile)

        oemof_allround_sample.oemofAllroundSample(orig_dumpfile)

        PrintResultsFromDump(dumpfile=orig_dumpfile, output=os.path.join(os.getcwd(), "output", "oemof_out.txt"))


    ##########################################################################
    # ensys-Klassen
    ##########################################################################
    if goEnsys:
        # basic_example.CreateSampleConfiguration(configfile)
        # modifiedexample.CreateSampleConfiguration(path_to_dump_config)
        allround_sample.CreateSampleConfiguration(configfile)

        sb = EnsysSystembuilder()

        es = sb.BuildConfiguration(configfile)
        sb.BuildEnergySystem(es, dumpfile)

        # EnsysOptimise(dumpfile)

        PrintResultsFromDump(dumpfile=dumpfile, output=os.path.join(os.getcwd(), "output", "ensys_out.txt"))

    verify.files("output/ensys_out.txt", "output/oemof_out.txt")

    # logger.info("Größe Ensys-Dumpfile: " + str(os.path.getsize("dumps/energy_system.dump")))
    # logger.info("Größe Oemof-Dumpfile: " + str(os.path.getsize("dumps/energy_system_orig.dump")))


def testbed():
    tobj = TestObject(label="Hallo Welt", number=42.42)

    print(tobj)
    print(tobj.json())


if __name__ == "__main__":
    oemof(goOemof=False, goEnsys=True)
    #testbed()


