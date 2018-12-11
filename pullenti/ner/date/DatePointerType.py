# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class DatePointerType(IntEnum):
    """ Дополнительные указатели для дат """
    NO = 0
    BEGIN = 1
    CENTER = 2
    END = 3
    TODAY = 4
    WINTER = 5
    SPRING = 6
    SUMMER = 7
    AUTUMN = 8
    UNDEFINED = 9
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)