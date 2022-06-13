import os

from InRetEnsys import Verification, PrintResultsFromDump, ModelBuilder
from InRetEnsys.modelbuilder import logger
from configs.ENSYS.allround1_sample import CreateAllroundSampleConfiguration

filename = "allround_energy_system"
wkdir = os.path.join(os.getcwd(), "dumps")
dumpfile = os.path.join(wkdir, filename + ".dump")
orig_dumpfile = os.path.join(wkdir, filename + "_orig.dump")

for file in [dumpfile, orig_dumpfile]:
    if os.path.exists(file):
        os.remove(file)

verify = Verification()

if False:
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
