# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class ConjunctionType(IntEnum):
    """ Типы союзов и служебных слов """
    UNDEFINED = 0
    """ Неопределено """
    COMMA = 1
    """ Запятая """
    AND = 2
    """ И """
    OR = 3
    """ Или """
    NOT = 4
    """ ни ... ни ... """
    BUT = 5
    """ Но """
    IF = 6
    """ Если """
    THEN = 7
    """ То """
    ELSE = 8
    """ Иначе """
    WHEN = 9
    """ Когда """
    BECAUSE = 10
    """ Потому что """
    INCLUDE = 11
    """ Включая """
    EXCEPT = 12
    """ Исключая """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)