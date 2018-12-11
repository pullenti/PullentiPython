# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class ILTypes(IntEnum):
    UNDEFINED = 0
    APPENDIX = 1
    APPROVED = 2
    ORGANIZATION = 3
    REGNUMBER = 4
    DATE = 5
    GEO = 6
    PERSON = 7
    TYP = 8
    VERB = 9
    DIRECTIVE = 10
    QUESTION = 11
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)