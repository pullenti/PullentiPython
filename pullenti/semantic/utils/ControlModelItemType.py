# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class ControlModelItemType(IntEnum):
    UNDEFINED = 0
    WORD = 1
    """ Конкретное слово (не относится """
    VERB = 2
    """ Все глаголы (не Reflexive) """
    REFLEXIVE = 3
    """ Возвратные глаголы и страдательный залог """
    NOUN = 4
    """ Существительное, которое можно отглаголить """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)