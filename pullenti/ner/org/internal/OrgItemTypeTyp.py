# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class OrgItemTypeTyp(IntEnum):
    UNDEFINED = 0
    ORG = 1
    PREFIX = 2
    DEP = 3
    DEPADD = 4
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)