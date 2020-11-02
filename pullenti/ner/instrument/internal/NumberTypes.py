# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class NumberTypes(IntEnum):
    UNDEFINED = 0
    DIGIT = 1
    TWODIGITS = 2
    THREEDIGITS = 3
    FOURDIGITS = 4
    ROMAN = 5
    LETTER = 6
    COMBO = 7
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)