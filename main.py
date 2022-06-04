import os

from configs.ENSYS.SWE2021_V08_O4_2045_BEW0_S1_Geoth_Wind import createConfigBinary
from configs.ENSYS.allround_sample import CreateAllroundSampleConfiguration
from configs.ENSYS.basic_sample import CreateBasisSampleConfiguration
from configs.OEMOF.oemof_SWE2021_V08_O4_2045_BEW0_S1_Geoth_Wind import oemof_swe_test
from configs.OEMOF.oemof_allround_sample import oemofAllroundSample
from configs.OEMOF.oemof_basic_sample import oemofBasicSample
from InRetEnsys import Verification, PrintResultsFromDump, ModelBuilder
from hsncommon.log import HsnLogger

logger = HsnLogger()


def swe_samples(goOemof, goEnsys):
    filename = "swe_energy_system"
    wkdir = os.path.join(os.getcwd(), "dumps")
    dumpfile = os.path.join(wkdir, filename + ".dump")
    orig_dumpfile = os.path.join(wkdir, filename + "_orig.dump")
    verify = Verification()

    datadir = os.path.join(os.getcwd(), "configs", "DATEN", "SWE Test")
    logger.info(datadir)

    if goOemof:
        logger.info("Start oemof-Sample.")
        oemof_swe_test(orig_dumpfile, datadir)
        logger.info("oemof-sample fin.")

    if goEnsys:
        logger.info("Start InRetEnsys-Sample.")
        configfile = createConfigBinary(datadir)

        ModelBuilder(ConfigFile=configfile,
                     DumpFile=dumpfile)

    logger.info("Start verifying.")

    verify.dataframes([orig_dumpfile, dumpfile])
    logger.info("Fin.")

    logger.info("Größe Ensys-Dumpfile: " + str(os.path.getsize(dumpfile)))
    logger.info("Größe Oemof-Dumpfile: " + str(os.path.getsize(orig_dumpfile)))


def allround_samples(goOemof, goEnsys):
    filename = "allround_energy_system"
    wkdir = os.path.join(os.getcwd(), "dumps")
    dumpfile = os.path.join(wkdir, filename + ".dump")
    orig_dumpfile = os.path.join(wkdir, filename + "_orig.dump")

    for file in [dumpfile, orig_dumpfile]:
        if os.path.exists(file):
            os.remove(file)

    verify = Verification()

    if goOemof:
        logger.info("Start oemof-Sample")
        oemofAllroundSample(orig_dumpfile)

        logger.info("Print results from sample.")
        PrintResultsFromDump(dumpfile=orig_dumpfile, output=os.path.join(os.getcwd(), "output", "oemof_allround_out"))

        logger.info("Fin with oemof-Sample")

    if goEnsys:
        configfile = CreateAllroundSampleConfiguration()

        ModelBuilder(configfile, dumpfile)
        PrintResultsFromDump(dumpfile=dumpfile, output=os.path.join(os.getcwd(), "output", "ensys_allround_out"))

    logger.info("Start verifying.")

    verify.dataframes([orig_dumpfile, dumpfile])
    verify.files("output/ensys_allround_out", "output/oemof_allround_out")

    logger.info("Fin.")

    logger.info("Größe Ensys-Dumpfile: " + str(os.path.getsize(dumpfile)))
    logger.info("Größe Oemof-Dumpfile: " + str(os.path.getsize(orig_dumpfile)))


def basic_samples(goOemof, goEnsys):
    filename = "basic_energy_system"
    wkdir = os.path.join(os.getcwd(), "dumps")
    dumpfile = os.path.join(wkdir, filename + ".dump")
    orig_dumpfile = os.path.join(wkdir, filename + "_orig.dump")

    for file in [dumpfile, orig_dumpfile]:
        if os.path.exists(file):
            os.remove(file)

    verify = Verification()

    if goOemof:
        logger.info("Start oemof-Sample")
        oemofBasicSample(orig_dumpfile)

        logger.info("Print results from sample.")
        PrintResultsFromDump(dumpfile=orig_dumpfile, output=os.path.join(os.getcwd(), "output", "oemof_basic_out"))

        logger.info("Fin with oemof-Sample")

    if goEnsys:
        configfile = CreateBasisSampleConfiguration()

        ModelBuilder(configfile, dumpfile)
        PrintResultsFromDump(dumpfile=dumpfile, output=os.path.join(os.getcwd(), "output", "ensys_basic_out"))

    logger.info("Start verifying.")

    verify.dataframes([orig_dumpfile, dumpfile])
    verify.files("output/ensys_basic_out", "output/oemof_basic_out")

    logger.info("Fin.")

    logger.info("Größe Ensys-Dumpfile: " + str(os.path.getsize(dumpfile)))
    logger.info("Größe Oemof-Dumpfile: " + str(os.path.getsize(orig_dumpfile)))


def StartFromConfigFile(configfile, dumpfile):
    logger.info("Start Building and solving")
    ModelBuilder(configfile, dumpfile)


def BuildConfigFiles(Allround=False, SWE=True):
    configFilesList = []

    if Allround:
        configFilesList.append(CreateAllroundSampleConfiguration())

    if SWE:
        datadir = os.path.join(os.getcwd(), "configs", "DATEN", "SWE Test")
        logger.info(datadir)

        configFilesList.append(createConfigBinary(datadir))

    return configFilesList


def main(*args, **kwargs):
    # pro job ein config file > was mit args gestartet wird
    # InRetEnsys package als wheel
    # Only Ensys Energysystems
    wkdir = os.getcwd()
    dumpdir = os.path.join(wkdir, "dumps")

    dumpfileList = [os.path.join(dumpdir, "allround_energy_system.dump"), os.path.join(dumpdir, "ensys_swe_energy_system.dump")]
    configfileList = BuildConfigFiles(Allround=True, SWE=True)

    i = 0

    for configfile in configfileList:
        dumpfile = dumpfileList[i]
        logger.info("Config: " + configfile)

        StartFromConfigFile(configfile, dumpfile)
        # PrintResultsFromDump(dumpfile=dumpfile, output=os.path.join(os.getcwd(), "output", "ensys_out"))

        i += 1


if __name__ == "__main__":
    # main()

    # For Debugging
    allround_samples(goOemof=True, goEnsys=True)
    # basic_samples(goOemof=True, goEnsys=True)
    # swe_samples(goOemof=True, goEnsys=True)
