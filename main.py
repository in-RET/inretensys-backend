import os

from pydantic import BaseModel

from configs import oemof_allround_sample, allround_sample
from ensys import Verification, PrintResultsFromDump, ModelBuilder
from hsncommon.log import HsnLogger


class TestObject(BaseModel):
    label: str = "Testlabel"
    number: float = 3.14

    def to_oemof(self):
        return "Hallo Welt 42"


def CheckAndRemove(file):
    if os.path.exists(file):
        os.remove(file)


def oemof(goOemof, goEnsys):
    logger = HsnLogger()

    wkdir = os.path.join(os.getcwd(), "dumps")
    filename = "energy_system"

    configfile = os.path.join(wkdir, filename + ".bin")
    dumpfile = os.path.join(wkdir, filename + ".dump")
    orig_dumpfile = os.path.join(wkdir, filename + "_orig.dump")

    for file in [configfile, dumpfile, orig_dumpfile]:
        CheckAndRemove(file)

    verify = Verification

    ##########################################################################
    # oemof-Beispiel
    ##########################################################################
    if goOemof:
        logger.info("Start oemof-Sample")

        # oemof_sample.oemofSample(orig_dumpfile)
        oemof_allround_sample.oemofAllroundSample(orig_dumpfile)

        logger.info("Print results from sample.")
        PrintResultsFromDump(dumpfile=orig_dumpfile, output=os.path.join(os.getcwd(), "output", "oemof_out"))

        logger.info("Fin with oemof-Sample")

    ##########################################################################
    # ensys-Klassen
    ##########################################################################
    if goEnsys:
        # basic_sample.CreateSampleConfiguration(configfile)
        # modifiedexample.CreateSampleConfiguration(path_to_dump_config)
        allround_sample.CreateSampleConfiguration(configfile)

        ModelBuilder(configfile, dumpfile)

        #PrintResultsFromDump(dumpfile=dumpfile, output=os.path.join(os.getcwd(), "output", "ensys_out.txt"))

    logger.info("Start verifying.")
    verify.files("output/ensys_out", "output/oemof_out")
    logger.info("Fin.")

    #logger.info("Größe Ensys-Dumpfile: " + str(os.path.getsize("dumps/energy_system.dump")))
    #logger.info("Größe Oemof-Dumpfile: " + str(os.path.getsize("dumps/energy_system_orig.dump")))


def testbed():
    tobj = TestObject(
        label="Hallo xyz!",
        number=314.42)
    print(tobj)
    x = tobj.to_oemof()

    print(x)


if __name__ == "__main__":
    oemof(goOemof=True, goEnsys=True)
    #testbed()


