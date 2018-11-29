# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class CanBeEqualsAttrs(IntEnum):
    """ Атрибуты функции CanBeEqualsEx """
    NO = 0
    IGNORENONLETTERS = 1
    IGNOREUPPERCASE = 2
    CHECKMORPHEQUAFTERFIRSTNOUN = 4
    USEBRACKETS = 8
    IGNOREUPPERCASEFIRSTWORD = 0x10
    FIRSTCANBESHORTER = 0x20
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)