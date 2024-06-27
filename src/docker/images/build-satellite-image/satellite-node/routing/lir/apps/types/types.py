from enum import Enum


class Protocol(Enum):
    IP = 0
    LIR = 1


class TransmissionPattern(Enum):
    UNICAST = 0
    MULTICAST = 1