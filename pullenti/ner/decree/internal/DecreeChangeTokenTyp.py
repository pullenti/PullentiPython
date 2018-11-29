# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class DecreeChangeTokenTyp(IntEnum):
    UNDEFINED = 0
    STARTMULTU = 0 + 1
    STARTSINGLE = (0 + 1) + 1
    SINGLE = ((0 + 1) + 1) + 1
    ACTION = (((0 + 1) + 1) + 1) + 1
    VALUE = ((((0 + 1) + 1) + 1) + 1) + 1
    AFTERVALUE = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)