# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class TextsCompareType(IntEnum):
    NONCOMPARABLE = 0
    EQUIVALENT = 0 + 1
    EARLY = (0 + 1) + 1
    LATER = ((0 + 1) + 1) + 1
    IN = (((0 + 1) + 1) + 1) + 1
    CONTAINS = ((((0 + 1) + 1) + 1) + 1) + 1
    INTERSECT = (((((0 + 1) + 1) + 1) + 1) + 1) + 1