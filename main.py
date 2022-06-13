import os
import sys

from InRetEnsys import ModelBuilder
from hsncommon.log import HsnLogger


def StartFromConfigFile(configfile, dumpfile):
    HsnLogger().info("Start Building and solving")
    ModelBuilder(configfile, dumpfile)


# InRetEnsys package als wheel
args = sys.argv[1:]

wkdir = os.getcwd()
configfile = None

dumpdir = os.path.join(wkdir, "dumps")

if len(args) < 1:
    raise Exception("There should be minimum one argument! (Path to the config-binary)")

for arg in args:
    arg = os.path.join(wkdir, arg)
    if os.path.exists(arg) and os.path.isfile(arg):
        configfile = arg

if configfile is not None:
    dumpfile = os.path.join(dumpdir, os.path.basename(configfile).replace(".bin", "") + ".dump")

    print(configfile)
    print(dumpfile)

    StartFromConfigFile(configfile=configfile,
                        dumpfile=dumpfile)
else:
    raise Exception("Configuration not given!")
