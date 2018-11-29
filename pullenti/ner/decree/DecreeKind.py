# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class DecreeKind(IntEnum):
    UNDEFINED = 0
    KODEX = 0 + 1
    USTAV = (0 + 1) + 1
    KONVENTION = ((0 + 1) + 1) + 1
    CONTRACT = (((0 + 1) + 1) + 1) + 1
    PROJECT = ((((0 + 1) + 1) + 1) + 1) + 1
    PUBLISHER = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    PROGRAM = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    STANDARD = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)