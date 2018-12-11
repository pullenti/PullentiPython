# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class DecreeKind(IntEnum):
    UNDEFINED = 0
    KODEX = 1
    USTAV = 2
    KONVENTION = 3
    CONTRACT = 4
    PROJECT = 5
    PUBLISHER = 6
    PROGRAM = 7
    STANDARD = 8
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)