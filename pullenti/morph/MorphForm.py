# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class MorphForm(IntEnum):
    """ Форма """
    UNDEFINED = 0
    """ Не определена """
    SHORT = 1
    """ Краткая форма """
    SYNONYM = 2
    """ Синонимичная форма """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)