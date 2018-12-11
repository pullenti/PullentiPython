# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class PersonPropertyKind(IntEnum):
    """ Типы свойств """
    UNDEFINED = 0
    BOSS = 1
    KING = 2
    KIN = 3
    MILITARYRANK = 4
    NATIONALITY = 5
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)