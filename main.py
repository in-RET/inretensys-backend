import os
import printresults

from ensys import systembuilder
from hsncommon import config
from configs import basicexample, modifiedexample


def BuildEnergySystemFromConfiguration(filename):
    es = config.config_object_from_file(filename)
    systembuilder.EnsysSystembuilder(es)


if __name__ == "__main__":
    wkdir = os.path.join(os.getcwd(), "dumps")
    filename = "EnergySystem"

    if os.path.exists(os.path.join(wkdir, filename + ".dump")):
        os.remove(os.path.join(wkdir, filename + ".dump"))

    path_to_dump_config = os.path.join(wkdir, filename + ".bin")
    print("Dumpfilepath:", path_to_dump_config)

    #basicexample.CreateSampleConfiguration(path_to_dump_config)
    modifiedexample.CreateSampleConfiguration(path_to_dump_config)

    BuildEnergySystemFromConfiguration(path_to_dump_config)
    printresults.PrintResultsFromDump(dpath=wkdir, dumpfile=os.path.join(filename + ".dump"))
