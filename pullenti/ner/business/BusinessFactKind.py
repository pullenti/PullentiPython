# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class BusinessFactKind(IntEnum):
    """ Типы бизнес-фактов """
    UNDEFINED = 0
    CREATE = 0 + 1
    DELETE = (0 + 1) + 1
    GET = ((0 + 1) + 1) + 1
    SELL = (((0 + 1) + 1) + 1) + 1
    HAVE = ((((0 + 1) + 1) + 1) + 1) + 1
    PROFIT = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    DAMAGES = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    AGREEMENT = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    SUBSIDIARY = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    FINANCE = (((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    LAWSUIT = ((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)