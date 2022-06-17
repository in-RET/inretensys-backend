import os
import sys

from InRetEnsys import ModelBuilder
from hsncommon.log import HsnLogger


def StartFromConfigFile(configfile, dumpfile):
    HsnLogger().info("Start Building and solving")
    ModelBuilder(configfile, dumpfile)


args = sys.argv[1:]

if len(args) > 0:
    configfile = args[0]
else:
    configfile = os.getenv('BIN_FILE', None)

wkdir = os.getcwd()
dumpdir = os.path.join(wkdir, "dumps")

if configfile is not None:
    dumpfile = os.path.join(dumpdir, os.path.basename(configfile).replace(".bin", "") + ".dump")

    StartFromConfigFile(configfile=configfile,
                        dumpfile=dumpfile)
else:
    raise Exception("Configuration not given!")
