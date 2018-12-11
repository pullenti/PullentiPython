# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class FundsItemTyp(IntEnum):
    UNDEFINED = 0
    NOUN = 1
    COUNT = 2
    ORG = 3
    SUM = 4
    PERCENT = 5
    PRICE = 6
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)