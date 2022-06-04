import enum

# message type
class HsnMessageType(enum.IntFlag):
    TRACE = 8
    INFO = 4
    WARN = 2
    CRITICAL = 1
