# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class FioTemplateType(IntEnum):
    UNDEFINED = 0
    SURNAMEII = 1
    IISURNAME = 2
    SURNAMEI = 3
    ISURNAME = 4
    SURNAMENAME = 5
    SURNAMENAMESECNAME = 6
    NAMESURNAME = 7
    NAMESECNAMESURNAME = 8
    NAMEISURNAME = 9
    NAMESECNAME = 10
    KING = 11
    ASIANNAME = 12
    ASIANSURNAMENAME = 13
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)