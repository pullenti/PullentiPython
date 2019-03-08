# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class MorphTense(IntEnum):
    """ Время (для глаголов) """
    UNDEFINED = 0
    """ Неопределено """
    PAST = 1
    """ Прошлое """
    PRESENT = 2
    """ Настоящее """
    FUTURE = 4
    """ Будущее """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)