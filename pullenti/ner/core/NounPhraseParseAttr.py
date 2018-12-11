# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class NounPhraseParseAttr(IntEnum):
    """ Параметры выделения """
    NO = 0
    PARSEPRONOUNS = 1
    PARSEPREPOSITION = 2
    IGNOREADJBEST = 4
    IGNOREPARTICIPLES = 8
    REFERENTCANBENOUN = 0x10
    CANNOTHASCOMMAAND = 0x20
    ADJECTIVECANBELAST = 0x40
    PARSEADVERBS = 0x80
    PARSEVERBS = 0x100
    PARSENUMERICASADJECTIVE = 0x200
    MULTILINES = 0x400
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)