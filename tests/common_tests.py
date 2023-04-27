import logging
import os
import unittest

from oemof import solph
from InRetEnsys import *
from InRetEnsys.common import log

class components(unittest.TestCase):

    def test_log(self):
        log.InRetEnsysLogger("unittest", os.path.join(os.getcwd(), "unittest.log"), logging.DEBUG)

        log.InRetEnsysLogger.debug("Debug")
        log.InRetEnsysLogger.info("Info")
        log.InRetEnsysLogger.warn("Warn")
        log.InRetEnsysLogger.error("Error")
        log.InRetEnsysLogger.critical("Critical")
    