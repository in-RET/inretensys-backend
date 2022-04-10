import time

from .pattern import singleton
from .types import HsnMessageType


# base logger
@singleton
class HsnLogger:
    def __init__(
        self,
        debug_level = HsnMessageType.CRITICAL | HsnMessageType.WARN | HsnMessageType.INFO | HsnMessageType.TRACE,
        *args,
        **kwargs
    ) -> None:
        self.__debug_level = debug_level

    def output(self, msg):
        print(msg)

    def __generate_message(self, type, msg):
        if type == HsnMessageType.TRACE:
            type_indicator = '---T'
        elif type == HsnMessageType.INFO:
            type_indicator = '--I-'
        elif type == HsnMessageType.WARN:
            type_indicator = '-W--'
        elif type == HsnMessageType.CRITICAL:
            type_indicator = 'C---'

        return f'[{type_indicator}] {time.time():.9f}\t{msg}'

    def trace(self, msg):
        m = self.__generate_message(HsnMessageType.TRACE, msg)
        if self.__debug_level & HsnMessageType.TRACE:
            self.output(m)

    def info(self, msg):
        m = self.__generate_message(HsnMessageType.INFO, msg)
        if self.__debug_level & HsnMessageType.INFO:
            self.output(m)

    def warn(self, msg):
        m = self.__generate_message(HsnMessageType.WARN, msg)
        if self.__debug_level & HsnMessageType.WARN:
            self.output(m)

    def critical(self, msg):
        m = self.__generate_message(HsnMessageType.CRITICAL, msg)
        quit(m)