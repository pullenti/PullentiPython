# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class MorphMood(IntEnum):
    """ Наклонение (для глаголов)
    Наклонение
    """
    UNDEFINED = 0
    """ Неопределено """
    INDICATIVE = 1
    """ Изъявительное """
    SUBJUNCTIVE = 2
    """ Условное """
    IMPERATIVE = 4
    """ Повелительное """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)