import os
import sys

from InRetEnsys import ModelBuilder

args = sys.argv[1:]

if len(args) > 0:
    configfile = args[0]
else:
    configfile = os.getenv('BIN_FILE', None)

wkdir = os.getcwd()
dumpdir = os.path.join(wkdir, "dumps")
logdir = os.path.join(wkdir, "logs")

if not os.path.exists(dumpdir):
    os.makedirs(dumpdir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

if configfile is not None:
    dumpfile = os.path.join(dumpdir, os.path.basename(configfile).replace(".bin", "") + ".dump")

    ModelBuilder(configfile, dumpfile)
else:
    raise Exception("Configuration not given!")

filename = os.path.basename(configfile.replace(".bin", ""))
