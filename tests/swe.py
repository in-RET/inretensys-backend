import os

from src.InRetEnsys import Verification
from src.InRetEnsys import logger, ModelBuilder
from configs.ENSYS.SWE2021_V08_O4_2045_BEW0_S1_Geoth_Wind import createConfigBinary

# goOemof und goEnsys als keyword args
args = ""


filename = "swe_energy_system"
wkdir = os.path.join(os.getcwd(), "dumps")
dumpfile = os.path.join(wkdir, filename + ".dump")
orig_dumpfile = os.path.join(wkdir, filename + "_orig.dump")
verify = Verification()

datadir = os.path.join(os.getcwd(), "configs", "DATEN", "SWE Test")
logger.info(datadir)

if False:
    logger.info("Start oemof-Sample.")
    oemof_swe_test(orig_dumpfile, datadir)
    logger.info("oemof-sample fin.")

if True:
    logger.info("Start InRetEnsys-Sample.")
    configfile = createConfigBinary(datadir)

    ModelBuilder(ConfigFile=configfile,
                 DumpFile=dumpfile)

logger.info("Start verifying.")

verify.dataframes([orig_dumpfile, dumpfile])
logger.info("Fin.")

logger.info("Größe Ensys-Dumpfile: " + str(os.path.getsize(dumpfile)))
logger.info("Größe Oemof-Dumpfile: " + str(os.path.getsize(orig_dumpfile)))
