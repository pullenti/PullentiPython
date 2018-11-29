# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class ILTypes(IntEnum):
    UNDEFINED = 0
    APPENDIX = 0 + 1
    APPROVED = (0 + 1) + 1
    ORGANIZATION = ((0 + 1) + 1) + 1
    REGNUMBER = (((0 + 1) + 1) + 1) + 1
    DATE = ((((0 + 1) + 1) + 1) + 1) + 1
    GEO = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    PERSON = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    TYP = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    VERB = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    DIRECTIVE = (((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    QUESTION = ((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)