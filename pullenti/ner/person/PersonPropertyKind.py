# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class PersonPropertyKind(IntEnum):
    """ Категории свойств персон """
    UNDEFINED = 0
    """ Неопределена """
    BOSS = 1
    """ Начальник """
    KING = 2
    """ Вельможные и духовные особы """
    KIN = 3
    """ Родственники """
    MILITARYRANK = 4
    """ Воинское звание """
    NATIONALITY = 5
    """ Национальность """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)