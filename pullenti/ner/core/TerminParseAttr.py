# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class TerminParseAttr(IntEnum):
    """ Патаметры выделения термина словаря (TryParse) """
    NO = 0
    FULLWORDSONLY = 1
    """ не использовать сокращения """
    INDICTIONARYONLY = 2
    """ Рассматривать только варианты из морфологичского словаря """
    TERMONLY = 4
    """ Игнорировать морфологические варианты, а брать только терм """
    CANBEGEOOBJECT = 8
    """ Может иметь географический объект в середине (Министерство РФ по делам ...) """
    IGNOREBRACKETS = 0x10
    """ Игнорировать скобки внутри нескольких термов """
    IGNORESTOPWORDS = 0x20
    """ Игнорировать знаки препинания, числа, союзы и предлоги """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)