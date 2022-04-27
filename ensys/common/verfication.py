import os.path
from hashlib import sha256
from oemof import solph
from hsncommon.log import HsnLogger


def calculateSHA256(filepath):
    sha256_hash = sha256()
    with open(filepath, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        hash = sha256_hash.hexdigest()

    return hash


def files(filepathA, filepathB):
    hashA = calculateSHA256(filepathA)
    hashB = calculateSHA256(filepathB)

    logger = HsnLogger()

    if hashA == hashB:
        logger.info("Daten stimmen überein!")
        logger.info("A: " + str(hashA))
        logger.info("B: " + str(hashB))
    else:
        logger.warn("Daten stimmen nicht überein!")
        logger.warn("A: " + str(hashA))
        logger.warn("B: " + str(hashB))


def dataframes(dfList):
    data = None

    compSystems = []
    logger = HsnLogger()

    for df in dfList:
        logger.info("Read data to Compare from: " + df)
        es = solph.EnergySystem()
        es.restore(dpath=os.path.dirname(df), filename=os.path.basename(df))

        if es.results["compare"] is not None:
            data = es.results["compare"]
        else:
            logger.critical("Kein DataFrame zum Vergleich gefunden! Bitte bei der Auswertung des Models "
                            "die Methode 'solph.processing.create_dataframe(model)' nutzen um dies den Ergebnissen "
                            "hinzuzufügen!")

        compSystems.append(data)

    logger.info("Compare data.")

    if len(compSystems) > 1:
        df1 = compSystems[0].reset_index(drop=True)
        df2 = compSystems[1].reset_index(drop=True)

        # Vergleich der beiden DataFrames
        # df1.compare(df2)
        result = df1["value"].compare(df2["value"])

        print(result)
        # print(df1.reset_index(drop=True).equals(df2.reset_index(drop=True)))


class Verification:

    def __init__(self):
        pass

    @classmethod
    def files(cls, filepathA, filepathB):
        files(filepathA, filepathB)