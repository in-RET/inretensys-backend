import os
import printresults

from configs import basicexample, modifiedexample, oemof_sample
from ensys import EnsysOptimise, EnsysSystembuilder
from verfication import verify

if __name__ == "__main__":
    wkdir = os.path.join(os.getcwd(), "dumps")
    filename = "energy_system"

    configfile = os.path.join(wkdir, filename + ".bin")
    dumpfile = os.path.join(wkdir, filename + ".dump")
    orig_dumpfile = os.path.join(wkdir, filename + "_orig.dump")

    if os.path.exists(configfile):
        os.remove(configfile)

    if os.path.exists(dumpfile):
        os.remove(dumpfile)

    ##########################################################################
    # oemof-Beispiel
    ##########################################################################
    if not os.path.exists(orig_dumpfile):
        oemof_sample.oemofSample(orig_dumpfile)

    ##########################################################################
    # ensys-Klassen
    ##########################################################################

    basicexample.CreateSampleConfiguration(configfile)
    # modifiedexample.CreateSampleConfiguration(path_to_dump_config)

    sb = EnsysSystembuilder()

    es = sb.BuildConfiguration(configfile)
    sb.BuildEnergySystem(es, dumpfile)

    verify(dumpfile, orig_dumpfile)

    #EnsysOptimise(dumpfile)
    printresults.PrintResultsFromDump(dpath=wkdir, dumpfile=dumpfile)
