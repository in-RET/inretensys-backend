import logging
import os

from InRetEnsys.common.log import InRetEnsysLogger
from verifier import Verifier

verifier = Verifier()

wdir = os.path.join(os.getcwd(), "output")

logger = InRetEnsysLogger("Logger")

# Verify all data
logger.info("Basic Example")
fileA = os.path.join(wdir, "ensys_basic")
fileB = os.path.join(wdir, "oemof_basic")
verifier.files(filepathA=fileA, filepathB=fileB)

logger.info("Allround Example 1")
fileA = os.path.join(wdir, "ensys_allround1")
fileB = os.path.join(wdir, "oemof_allround1")
verifier.files(filepathA=fileA, filepathB=fileB)

logger.info("Allround Example 2")
fileA = os.path.join(wdir, "ensys_allround2")
fileB = os.path.join(wdir, "oemof_allround2")
verifier.files(filepathA=fileA, filepathB=fileB)

logger.info("Allround Example 3")
fileA = os.path.join(wdir, "ensys_allround3")
fileB = os.path.join(wdir, "oemof_allround3")
verifier.files(filepathA=fileA, filepathB=fileB)
