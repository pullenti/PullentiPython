# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class MeasureKind(IntEnum):
    """ Что измеряется этой величиной """
    UNDEFINED = 0
    TIME = 0 + 1
    LENGTH = (0 + 1) + 1
    AREA = ((0 + 1) + 1) + 1
    VOLUME = (((0 + 1) + 1) + 1) + 1
    WEIGHT = ((((0 + 1) + 1) + 1) + 1) + 1
    SPEED = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)