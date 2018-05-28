# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class NamedEntityKind(IntEnum):
    """ Разновидности организаций """
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