# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class DecreeChangeKind(IntEnum):
    """ Типы изменений структурных элементов (СЭ) """
    UNDEFINED = 0
    CONTAINER = 0 + 1
    APPEND = (0 + 1) + 1
    EXPIRE = ((0 + 1) + 1) + 1
    NEW = (((0 + 1) + 1) + 1) + 1
    EXCHANGE = ((((0 + 1) + 1) + 1) + 1) + 1
    REMOVE = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    CONSIDER = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)