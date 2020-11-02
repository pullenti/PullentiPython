# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class PersonAttrTerminType2(IntEnum):
    UNDEFINED = 0
    IO = 1
    GRADE = 2
    ABBR = 3
    ADJ = 4
    IGNOREDADJ = 5
    IO2 = 6
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)