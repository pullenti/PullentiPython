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
    PLANET = 0 + 1
    """ Планеты """
    LOCATION = (0 + 1) + 1
    """ Разные географические объекты (не города) - реки, моря, континенты ... """
    MONUMENT = ((0 + 1) + 1) + 1
    """ Памятники и монументы """
    BUILDING = (((0 + 1) + 1) + 1) + 1
    """ Выдающиеся здания """