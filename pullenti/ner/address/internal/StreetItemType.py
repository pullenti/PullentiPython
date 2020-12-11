# Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class StreetItemType(IntEnum):
    NOUN = 0
    NAME = 1
    NUMBER = 2
    STDADJECTIVE = 3
    STDNAME = 4
    STDPARTOFNAME = 5
    AGE = 6
    FIX = 7
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)