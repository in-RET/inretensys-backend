import cProfile
import os
import pstats
import sys

from InRetEnsys import ModelBuilder

args = sys.argv[1:]

pr = cProfile.Profile()

if len(args) > 0:
    configfile = args[0]
else:
    configfile = os.getenv('BIN_FILE', None)

wkdir = os.getcwd()
dumpdir = os.path.join(wkdir, "dumps")

if configfile is not None:
    dumpfile = os.path.join(dumpdir, os.path.basename(configfile).replace(".bin", "") + ".dump")

    pr.enable()
    ModelBuilder(configfile, dumpfile)
    pr.disable()
else:
    raise Exception("Configuration not given!")

filename = os.path.basename(configfile.replace(".bin", ""))
pr.dump_stats("logs/" + filename + ".cprof")

with open("logs/" + filename + ".prof", "w") as f:
    ps = pstats.Stats("logs/" + filename + ".cprof", stream=f)
    ps.strip_dirs().sort_stats('tottime').print_stats()

os.remove("logs/" + filename + ".cprof")
