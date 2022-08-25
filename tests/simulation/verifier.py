import logging
import os.path
from hashlib import sha256
from typing import List

from oemof import solph


def calculateSHA256(filepath):
    sha256_hash = sha256()
    with open(filepath, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        hash_value = sha256_hash.hexdigest()

    return hash_value


class Verifier:
    @classmethod
    def files(cls, filepathA: str, filepathB: str) -> None:
        """
        Verifies two given files.

        :return: Nothing
        :rtype: None
        :param filepathA: Filepath of file A to compare
        :type: filepathA: str
        :param filepathB: Filepath of file B to compare
        :type filepathB: str
        """
        hashA = calculateSHA256(filepathA)
        hashB = calculateSHA256(filepathB)

        logger = logging.getLogger('OutputLogger')

        logger.warning("A: " + str(hashA))
        logger.warning("B: " + str(hashB))

    @classmethod
    def dataframes(cls, dfList: List[str]) -> None:
        """
        Compares two Dataframes from a given List of Dumpfiles and prints the result to the Console.

        :return: None
        :rtype: None
        :param dfList: List of 2 Dumpfiles which contains a Dataframe to compare
        :type dfList: List of String
        """
        data = None

        compSystems = []
        logger = logging.getLogger('OutputLogger')

        for df in dfList:
            logger.info("Read data to Compare from: " + df)
            es = solph.EnergySystem()
            es.restore(dpath=os.path.dirname(df), filename=os.path.basename(df))

            if es.results["verification"] is not None:
                data = es.results["verification"]
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
                logger.warning("Dataframes stimmen nicht überein!")
                print(df1.compare(df2))
