# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class DecreeChangeValueKind(IntEnum):
    """ Типы изменяющих СЭ значений """
    UNDEFINED = 0
    TEXT = 0 + 1
    WORDS = (0 + 1) + 1
    ROBUSTWORDS = ((0 + 1) + 1) + 1
    NUMBERS = (((0 + 1) + 1) + 1) + 1
    SEQUENCE = ((((0 + 1) + 1) + 1) + 1) + 1
    FOOTNOTE = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    BLOCK = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1