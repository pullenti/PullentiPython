# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class SentimentKind(IntEnum):
    """ Тип сентимента """
    UNDEFINED = 0
    POSITIVE = 1
    """ Положительный """
    NEGATIVE = 2
    """ Отрицательный """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)