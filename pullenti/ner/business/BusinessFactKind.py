# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class BusinessFactKind(IntEnum):
    """ Типы бизнес-фактов """
    UNDEFINED = 0
    CREATE = 1
    DELETE = 2
    GET = 3
    SELL = 4
    HAVE = 5
    PROFIT = 6
    DAMAGES = 7
    AGREEMENT = 8
    SUBSIDIARY = 9
    FINANCE = 10
    LAWSUIT = 11
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)