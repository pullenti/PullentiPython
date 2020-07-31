# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class SemFraglinkType(IntEnum):
    """ Типы связей между фрагментами """
    UNDEFINED = 0
    IFTHEN = 1
    IFELSE = 2
    BECAUSE = 3
    BUT = 4
    FOR = 5
    WHAT = 6
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)