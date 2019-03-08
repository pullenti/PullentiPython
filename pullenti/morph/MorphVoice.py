# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class MorphVoice(IntEnum):
    """ Залог (для глаголов) """
    UNDEFINED = 0
    """ Неопределено """
    ACTIVE = 1
    """ Действительный """
    PASSIVE = 2
    """ Страдательный """
    MIDDLE = 4
    """ Средний """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)