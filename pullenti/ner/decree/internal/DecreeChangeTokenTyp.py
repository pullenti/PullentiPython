# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class DecreeChangeTokenTyp(IntEnum):
    UNDEFINED = 0
    STARTMULTU = 1
    STARTSINGLE = 2
    SINGLE = 3
    ACTION = 4
    VALUE = 5
    AFTERVALUE = 6
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)