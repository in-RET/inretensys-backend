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
        hash_value = sha256_hash.hexdigest()

    return hash_value


class Verification:
    def __init__(self):
        """init verification class."""
        pass

    @classmethod
    def files(cls, filepathA, filepathB):
        hashA = calculateSHA256(filepathA)
        hashB = calculateSHA256(filepathB)

        logger = HsnLogger()

        if hashA == hashB:
            logger.info("Dateien stimmen überein!")
        else:
            logger.warn("Dateien stimmen nicht überein!")

        logger.warn("A: " + str(hashA))
        logger.warn("B: " + str(hashB))

    @classmethod
    def dataframes(cls, dfList):
        data = None

        compSystems = []
        logger = HsnLogger()

        for df in dfList:
            logger.info("Read data to Compare from: " + df)
            es = solph.EnergySystem()
            es.restore(dpath=os.path.dirname(df), filename=os.path.basename(df))

            if es.results["Verification"] is not None:
                data = es.results["Verification"]
            else:
                logger.critical("Kein DataFrame zum Vergleich gefunden! Bitte bei der Auswertung des Models "
                                "die Methode 'solph.processing.create_dataframe(model)' nutzen um dies den Ergebnissen "
                                "hinzuzufügen!")

            compSystems.append(data)

        logger.info("Verify data.")

        if len(compSystems) > 1:
            df1 = compSystems[0]["value"].reset_index(drop=True)
            df2 = compSystems[1]["value"].reset_index(drop=True)

            # Vergleich der beiden DataFrames
            if df1.equals(df2):
                logger.info("Dataframes stimmen überein!")
                print(df1.compare(df2))
            else:
                logger.warn("Dataframes stimmen nicht überein!")
                print(df1.compare(df2))
