import os
import sys

from InRetEnsys import ModelBuilder

args = sys.argv[1:]

if len(args) > 0:
    configfile = args[0]
    workdir = args[1]
else:
    configfile = os.getenv('FILE', None)
    workdir = os.getenv('WDIR', None)

if configfile is not None and workdir is not None:
    dumpdir = os.path.join(workdir, "dumps")
    logdir = os.path.join(workdir, "logs")

    tmpfilename: str = os.path.basename(configfile)

    if tmpfilename.find(".json") > 0:
        dumpfile = os.path.join(dumpdir, tmpfilename.replace(".json", ".dump"))
    elif tmpfilename.find(".bin") > 0:
        dumpfile = os.path.join(dumpdir, tmpfilename.replace(".bin", ".dump"))
    else:
        raise Exception("Fileformat is not valid!")

    ModelBuilder(configfile, dumpfile, workdir, logdir, dumpdir)
else:
    raise Exception("Configuration and/or Workingdirectory not given!")
