import logging


class InRetEnsysLogger:
    def __init__(self, name, filename, level=logging.INFO):
        logging.basicConfig(filename=filename,
                            format='%(asctime)s %(message)s',
                            filemode='w',
                            level=level)

        logging.getLogger(name)

    def debug(msg):
        msg = "[----D] " + msg
        logging.debug(msg=msg)

    def info(msg):
        msg = "[---I-] " + msg
        logging.info(msg=msg)

    def warn(msg):
        msg = "[--W--] " + msg
        logging.warning(msg=msg)

    def error(msg):
        msg = "[-E---] " + msg
        logging.error(msg=msg)

    def critical(msg):
        msg = "[C----] " + msg
        logging.critical(msg=msg)

