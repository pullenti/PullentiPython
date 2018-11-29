# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class FioTemplateType(IntEnum):
    UNDEFINED = 0
    SURNAMEII = 0 + 1
    IISURNAME = (0 + 1) + 1
    SURNAMEI = ((0 + 1) + 1) + 1
    ISURNAME = (((0 + 1) + 1) + 1) + 1
    SURNAMENAME = ((((0 + 1) + 1) + 1) + 1) + 1
    SURNAMENAMESECNAME = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    NAMESURNAME = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    NAMESECNAMESURNAME = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    NAMEISURNAME = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    NAMESECNAME = (((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    KING = ((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    ASIANNAME = (((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    ASIANSURNAMENAME = ((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)