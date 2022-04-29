import os

from oemof import solph
from pydantic import BaseModel

from configs import oemof_allround_sample, allround_sample
from ensys import EnsysConfigContainer, Verification, PrintResultsFromDump, EnsysFlow, EnsysTransformer
from ensys.common.config import set_init_function_args_as_instance_args
from ensys.systembuilder import BuildConfiguration, BuildEnergySystem
from hsncommon.log import HsnLogger


class TestObject(BaseModel, EnsysConfigContainer):
    label: str
    number: float

    def __init__(self,
                 label: str = "Default Label",
                 number: float = 0.0):
        super().__init__()
        self.label = label
        self.number = number

        set_init_function_args_as_instance_args(self, locals())


def oemof(goOemof, goEnsys):
    wkdir = os.path.join(os.getcwd(), "dumps")
    filename = "energy_system"

    configfile = os.path.join(wkdir, filename + ".bin")
    dumpfile = os.path.join(wkdir, filename + ".dump")
    orig_dumpfile = os.path.join(wkdir, filename + "_orig.dump")

    if os.path.exists(configfile):
        os.remove(configfile)

    if os.path.exists(dumpfile):
        os.remove(dumpfile)

    if os.path.exists(orig_dumpfile):
        os.remove(orig_dumpfile)

    logger = HsnLogger()
    verify = Verification

    ##########################################################################
    # oemof-Beispiel
    ##########################################################################
    logger.info("Start oemof-Sample")
    if goOemof:
        # oemof_sample.oemofSample(orig_dumpfile)
        oemof_allround_sample.oemofAllroundSample(orig_dumpfile)

        logger.info("Print results from sample.")
        PrintResultsFromDump(dumpfile=orig_dumpfile, output=os.path.join(os.getcwd(), "output", "oemof_out.txt"))

    logger.info("Fin with oemof-Sample")

    ##########################################################################
    # ensys-Klassen
    ##########################################################################
    if goEnsys:
        # basic_sample.CreateSampleConfiguration(configfile)
        # modifiedexample.CreateSampleConfiguration(path_to_dump_config)
        allround_sample.CreateSampleConfiguration(configfile)

        es = BuildConfiguration(configfile)
        BuildEnergySystem(es, dumpfile)

        # EnsysOptimise(dumpfile)

        PrintResultsFromDump(dumpfile=dumpfile, output=os.path.join(os.getcwd(), "output", "ensys_out.txt"))

    logger.info("Start verifying.")
    verify.files("output/ensys_out.txt", "output/oemof_out.txt")
    logger.info("Fin.")

    logger.info("Größe Ensys-Dumpfile: " + str(os.path.getsize("dumps/energy_system.dump")))
    logger.info("Größe Oemof-Dumpfile: " + str(os.path.getsize("dumps/energy_system_orig.dump")))


def BuildIO(ensys_io, es):
    oemof_io = {}
    keys = list(ensys_io.keys())
    print(keys)

    for key in keys:
        print("Key:", key)
        for node in es.nodes:
            print("Node:", node)

            if node.label == key:
                bus = es.nodes[es.nodes.index(node)]
                oemof_io[bus] = ensys_io[key].to_oemof()

    return oemof_io


def testbed():
    # tobj = TestObject(label="Hallo Welt", number=42.42)

    es = solph.EnergySystem()

    bel = solph.Bus(
        label="electricity"
    )

    bgas = solph.Bus(
        label="natural gas"
    )

    bexcess = solph.Bus(
        label="excess_bel"
    )

    es.add(bel, bgas, bexcess)

    for node in es.nodes:
        if node.label == "natural gas":
            bus = es.nodes[es.nodes.index(node)]

    print("Der gesucht Bus ist:", bus)

    test = EnsysTransformer(
        inputs={"electricity": EnsysFlow(), "excess_bel": EnsysFlow()},
        outputs={"natural_gas": EnsysFlow()}
    )

    pp_gas = solph.Transformer(
        inputs=BuildIO(test.inputs, es),
        outputs={bel: solph.Flow()}
    )

    es.add(pp_gas)


if __name__ == "__main__":
    oemof(goOemof=True, goEnsys=True)
    #testbed()


