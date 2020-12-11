# Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class SentItemType(IntEnum):
    UNDEFINED = 0
    NOUN = 1
    VERB = 2
    CONJ = 3
    DELIM = 4
    ADVERB = 5
    DEEPART = 6
    PARTBEFORE = 7
    PARTAFTER = 8
    SUBSENT = 9
    FORMULA = 10
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)