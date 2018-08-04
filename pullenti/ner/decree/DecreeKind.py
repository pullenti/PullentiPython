# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class DecreeKind(IntEnum):
    UNDEFINED = 0
    KODEX = 0 + 1
    USTAV = (0 + 1) + 1
    KONVENTION = ((0 + 1) + 1) + 1
    CONTRACT = (((0 + 1) + 1) + 1) + 1
    PROJECT = ((((0 + 1) + 1) + 1) + 1) + 1
    PUBLISHER = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    """ Источники опубликований """
    PROGRAM = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Госпрограммы """
    STANDARD = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Стандарт (ГОСТ, ТУ, ANSI и пр.) """