# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class StreetItemType(IntEnum):
    NOUN = 0
    NAME = 0 + 1
    NUMBER = (0 + 1) + 1
    STDADJECTIVE = ((0 + 1) + 1) + 1
    STDNAME = (((0 + 1) + 1) + 1) + 1
    STDPARTOFNAME = ((((0 + 1) + 1) + 1) + 1) + 1
    AGE = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    FIX = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)