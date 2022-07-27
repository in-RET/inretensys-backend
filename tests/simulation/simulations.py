import os

import configs.ENSYS.basic_sample
import configs.ENSYS.allround1_sample
import configs.ENSYS.allround2_sample
import configs.ENSYS.allround3_sample

import configs.OEMOF.oemof_basic_sample
import configs.OEMOF.oemof_allround1_sample
import configs.OEMOF.oemof_allround2_sample
import configs.OEMOF.oemof_allround3_sample
import configs.OEMOF.oemof_allround3_sample
from output import PrintResults

from InRetEnsys import ModelBuilder


def simulations(basic=False,
                allround1=False,
                allround2=False,
                allround3=False,
                swe=False
                ):
    wkdir = os.getcwd()
    dumpdir = os.path.join(wkdir, "dumps")
    dumpfiles = []
    if basic:
        # Oemof
        dumpfile = os.path.join(dumpdir, "oemof_basic.dump")
        dumpfiles.append(dumpfile)
        configs.OEMOF.oemof_basic_sample.oemofBasicSample(dumpfile)

        # Ensys
        dumpfile = os.path.join(dumpdir, "ensys_basic.dump")
        dumpfiles.append(dumpfile)
        configfile = configs.ENSYS.basic_sample.CreateConfiguration()
        ModelBuilder(configfile, dumpfile)

    if allround1:
        # Oemof
        dumpfile = os.path.join(dumpdir, "oemof_allround1.dump")
        dumpfiles.append(dumpfile)
        configs.OEMOF.oemof_allround1_sample.oemofAllroundSample(dumpfile)

        # Ensys
        dumpfile = os.path.join(dumpdir, "ensys_allround1.dump")
        dumpfiles.append(dumpfile)
        configfile = configs.ENSYS.allround1_sample.CreateConfiguration()
        ModelBuilder(configfile, dumpfile)

    if allround2:
        # Oemof
        dumpfile = os.path.join(dumpdir, "oemof_allround2.dump")
        dumpfiles.append(dumpfile)
        configs.OEMOF.oemof_allround2_sample.oemofAllroundSample(dumpfile)

        # Ensys
        dumpfile = os.path.join(dumpdir, "ensys_allround2.dump")
        dumpfiles.append(dumpfile)
        configfile = configs.ENSYS.allround2_sample.CreateConfiguration()
        ModelBuilder(configfile, dumpfile)

    if allround3:
        # Oemof
        dumpfile = os.path.join(dumpdir, "oemof_allround3.dump")
        dumpfiles.append(dumpfile)
        configs.OEMOF.oemof_allround3_sample.oemofAllroundSample(dumpfile)

        # Ensys
        dumpfile = os.path.join(dumpdir, "ensys_allround3.dump")
        dumpfiles.append(dumpfile)
        configfile = configs.ENSYS.allround3_sample.CreateConfiguration()
        ModelBuilder(configfile, dumpfile)

    if swe:
        raise NotImplementedError

    if len(dumpfiles) > 0:
        for dumpfile in dumpfiles:
            output = os.path.basename(dumpfile).replace(".dump", "")

            PrintResults(output=os.path.join(wkdir, "output", output),
                         dumpfile=dumpfile)


simulations(basic=True,
            allround1=True,
            allround2=True,
            allround3=True,
            swe=False
            )