# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class SentItemSubtype(IntEnum):
    UNDEFINED = 0
    WICH = 1
    WHAT = 2
    HOW = 3
    HOWMANY = 4
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)