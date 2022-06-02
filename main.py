import os

from ensys import Verification, PrintResultsFromDump, ModelBuilder
from hsncommon.log import HsnLogger

from configs.OEMOF.oemof_SWE2021_V08_O4_2045_BEW0_S1_Geoth_Wind import oemof_swe_test
from configs.OEMOF.oemof_allround_sample import oemofAllroundSample
from configs.ENSYS.SWE2021_V08_O4_2045_BEW0_S1_Geoth_Wind import createConfigBinary
from configs.ENSYS.allround_sample import CreateSampleConfiguration


def swe_samples(goOemof, goEnsys):
    logger = HsnLogger()
    filename = "swe_energy_system"
    dumpfile = os.path.join(os.getcwd(), "dumps", filename + ".dump")
    orig_dumpfile = os.path.join(os.getcwd(), "dumps", filename + "orig.dump")
    verify = Verification()

    datadir = os.path.join(os.getcwd(), "configs", "DATEN", "SWE Test")
    logger.info(datadir)

    if goOemof:
        logger.info("Start oemof-Sample.")
        oemof_swe_test(orig_dumpfile, datadir)
        logger.info("oemof-sample fin.")

    if goEnsys:
        logger.info("Start ensys-Sample.")
        configfile = os.path.join(os.getcwd(), "dumps", "ensys_swe_config.bin")
        dumpfile = os.path.join(os.getcwd(), "dumps", "ensys_swe_energy_system.dump")

        logger.info(configfile)
        createConfigBinary(configfile, datadir)

        ModelBuilder(ConfigFile=configfile,
                     DumpFile=dumpfile,
                     solver_verbose=True)

    logger.info("Start verifying.")

    verify.dataframes([orig_dumpfile, dumpfile])
    logger.info("Fin.")

    logger.info("Größe Ensys-Dumpfile: " + str(os.path.getsize("dumps/ensys_swe_energy_system.dump")))
    logger.info("Größe Oemof-Dumpfile: " + str(os.path.getsize("dumps/ensys_swe_energy_system_orig.dump")))


def allround_samples(goOemof, goEnsys):
    logger = HsnLogger()

    wkdir = os.path.join(os.getcwd(), "dumps")
    filename = "allround_energy_system"

    configfile = os.path.join(wkdir, filename + ".bin")
    dumpfile = os.path.join(wkdir, filename + ".dump")
    orig_dumpfile = os.path.join(wkdir, filename + "_orig.dump")

    for file in [configfile, dumpfile, orig_dumpfile]:
        if os.path.exists(file):
            os.remove(file)

    verify = Verification()

    if goOemof:
        logger.info("Start oemof-Sample")

        # oemof_sample.oemofSample(orig_dumpfile)
        oemofAllroundSample(orig_dumpfile)

        logger.info("Print results from sample.")
        PrintResultsFromDump(dumpfile=orig_dumpfile, output=os.path.join(os.getcwd(), "output", "oemof_out"))

        logger.info("Fin with oemof-Sample")

    if goEnsys:
        # basic_sample.CreateSampleConfiguration(configfile)
        # modifiedexample.CreateSampleConfiguration(path_to_dump_config)
        CreateSampleConfiguration(configfile)

        ModelBuilder(configfile, dumpfile)
        PrintResultsFromDump(dumpfile=dumpfile, output=os.path.join(os.getcwd(), "output", "ensys_out"))

    logger.info("Start verifying.")

    verify.dataframes([orig_dumpfile, dumpfile])
    verify.files("output/ensys_out", "output/oemof_out")

    logger.info("Fin.")

    logger.info("Größe Ensys-Dumpfile: " + str(os.path.getsize("dumps/allround_energy_system.dump")))
    logger.info("Größe Oemof-Dumpfile: " + str(os.path.getsize("dumps/allround_energy_system_orig.dump")))


if __name__ == "__main__":
    allround_samples(goOemof=True, goEnsys=True)
    #swe_samples(goOemof=False, goEnsys=True)
