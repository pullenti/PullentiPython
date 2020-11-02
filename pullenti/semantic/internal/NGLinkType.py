# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class NGLinkType(IntEnum):
    UNDEFINED = 0
    LIST = 1
    GENETIVE = 2
    NAME = 3
    AGENT = 4
    PACIENT = 5
    ACTANT = 6
    PARTICIPLE = 7
    ADVERB = 8
    BE = 9
    """ Это пропущенный глагол БЫТЬ """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)