# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class DatePointerType(IntEnum):
    """ Дополнительные указатели для дат """
    NO = 0
    BEGIN = 0 + 1
    CENTER = (0 + 1) + 1
    END = ((0 + 1) + 1) + 1
    TODAY = (((0 + 1) + 1) + 1) + 1
    WINTER = ((((0 + 1) + 1) + 1) + 1) + 1
    SPRING = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    SUMMER = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    AUTUMN = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    UNDEFINED = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1