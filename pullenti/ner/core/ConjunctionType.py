# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class ConjunctionType(IntEnum):
    UNDEFINED = 0
    COMMA = 1
    AND = 2
    OR = 3
    NOT = 4
    BUT = 5
    IF = 6
    THEN = 7
    ELSE = 8
    LET = 9
    WHEN = 10
    BECAUSE = 11
    INCLUDE = 12
    EXCEPT = 13
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)