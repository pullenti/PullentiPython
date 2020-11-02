# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class MorphTense(IntEnum):
    """ Время (для глаголов)
    Время
    """
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