﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

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
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)