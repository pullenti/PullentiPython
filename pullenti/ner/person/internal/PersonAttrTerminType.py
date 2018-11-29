# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class PersonAttrTerminType(IntEnum):
    PREFIX = 0
    BESTREGARDS = 0 + 1
    POSITION = (0 + 1) + 1
    KING = ((0 + 1) + 1) + 1
    OTHER = (((0 + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)