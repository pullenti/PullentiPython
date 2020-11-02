# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class NamedEntityKind(IntEnum):
    """ Категории мелких именованных сущностей """
    UNDEFINED = 0
    """ Неопределённая """
    PLANET = 1
    """ Планеты """
    LOCATION = 2
    """ Разные географические объекты (не города) - реки, моря, континенты ... """
    MONUMENT = 3
    """ Памятники и монументы """
    BUILDING = 4
    """ Выдающиеся здания """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)