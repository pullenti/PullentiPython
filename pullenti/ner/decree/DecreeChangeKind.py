# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class DecreeChangeKind(IntEnum):
    """ Типы изменений структурных элементов (СЭ) """
    UNDEFINED = 0
    CONTAINER = 1
    APPEND = 2
    EXPIRE = 3
    NEW = 4
    EXCHANGE = 5
    REMOVE = 6
    CONSIDER = 7
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)