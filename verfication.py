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