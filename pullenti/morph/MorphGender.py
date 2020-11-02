# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class MorphGender(IntEnum):
    """ Род (мужской-средний-женский)
    Род
    """
    UNDEFINED = 0
    """ Неопределён """
    MASCULINE = 1
    """ Мужской """
    FEMINIE = 2
    """ Женский """
    NEUTER = 4
    """ Средний """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)