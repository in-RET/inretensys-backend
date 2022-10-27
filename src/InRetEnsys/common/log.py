import logging


class InRetEnsysLogger:
    logger = None

    def __init__(self, name, filename, level=logging.INFO):
        logging.basicConfig(filename=filename,
                            format='%(asctime)s %(message)s',
                            filemode='w')

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    def debug(self, msg):
        msg = "[----D] " + msg
        self.logger.debug(msg)

    def info(self, msg):
        msg = "[---I-] " + msg
        self.logger.info(msg)

    def warn(self, msg):
        msg = "[--W--] " + msg
        self.logger.warning(msg)

    def error(self, msg):
        msg = "[-E---] " + msg
        self.logger.error(msg)

    def critical(self, msg):
        msg = "[C----] " + msg
        self.logger.critical(msg)

