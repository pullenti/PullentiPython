# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class MorphTense(IntEnum):
    """ Время (для глаголов) """
    UNDEFINED = 0
    """ Неопределено """
    PAST = 1
    """ Прошлое """
    PRESENT = 2
    """ Настоящее """
    FUTURE = 4
    """ Будущее """