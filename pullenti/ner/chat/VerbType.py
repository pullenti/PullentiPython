# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class VerbType(IntEnum):
    """ Тип глагольной формы """
    UNDEFINED = 0
    BE = 1
    HAVE = 2
    CAN = 3
    MUST = 4
    SAY = 5
    CALL = 6
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)