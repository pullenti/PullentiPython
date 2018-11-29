# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class FundsItemTyp(IntEnum):
    UNDEFINED = 0
    NOUN = 0 + 1
    COUNT = (0 + 1) + 1
    ORG = ((0 + 1) + 1) + 1
    SUM = (((0 + 1) + 1) + 1) + 1
    PERCENT = ((((0 + 1) + 1) + 1) + 1) + 1
    PRICE = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)