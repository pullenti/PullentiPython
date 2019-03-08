# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class TransportKind(IntEnum):
    """ Разновидности транспортных средств """
    UNDEFINED = 0
    AUTO = 1
    TRAIN = 2
    SHIP = 3
    FLY = 4
    SPACE = 5
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)