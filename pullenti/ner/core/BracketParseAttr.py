# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class BracketParseAttr(IntEnum):
    """ Параметры выделения последовательности """
    NO = 0
    CANCONTAINSVERBS = 2
    NEARCLOSEBRACKET = 4
    CANBEMANYLINES = 8