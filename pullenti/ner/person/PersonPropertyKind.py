# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class PersonPropertyKind(IntEnum):
    """ Типы свойств """
    UNDEFINED = 0
    BOSS = 0 + 1
    """ Начальник """
    KING = (0 + 1) + 1
    """ Вельможные и духовные особы """
    KIN = ((0 + 1) + 1) + 1
    """ Родственники """
    MILITARYRANK = (((0 + 1) + 1) + 1) + 1
    """ Воинское звание """
    NATIONALITY = ((((0 + 1) + 1) + 1) + 1) + 1
    """ Национальность """