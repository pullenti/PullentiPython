# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class DecreeChangeValueKind(IntEnum):
    """ Типы изменяющих СЭ значений """
    UNDEFINED = 0
    TEXT = 1
    WORDS = 2
    ROBUSTWORDS = 3
    NUMBERS = 4
    SEQUENCE = 5
    FOOTNOTE = 6
    BLOCK = 7
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)