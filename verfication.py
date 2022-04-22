import os.path

from oemof import solph

from hsncommon.log import HsnLogger


def verify(filepathA, filepathB):
    fileA = open(filepathA, 'r')
    fileB = open(filepathB, 'r')

    hashA = hash(fileA)
    hashB = hash(fileB)

    logger = HsnLogger()

    if hashA == hashB:
        logger.info("Daten stimmen überein!")
        logger.info("A: " + str(hashA))
        logger.info("B: " + str(hashB))
    else:
        logger.warn("Daten stimmen nicht überein!")
        logger.warn("A: " + str(hashA))
        logger.warn("B: " + str(hashB))


def verify(dfList):
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

        result = df1.compare(df2)

        print(result)
        print("Debug")
        # print(df1.reset_index(drop=True).equals(df2.reset_index(drop=True)))

