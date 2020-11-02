# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class DelimType(IntEnum):
    UNDEFINED = 0
    AND = 1
    BUT = 2
    IF = 4
    THEN = 8
    ELSE = 0x10
    BECAUSE = 0x20
    FOR = 0x40
    WHAT = 0x80
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)