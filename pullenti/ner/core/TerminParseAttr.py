# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class TerminParseAttr(IntEnum):
    """ Атрибуты привязки токена к термину словаря TerminCollection методом TryParse. Битовая маска.
    Атрибуты привязки к словарю
    """
    NO = 0
    """ Атрибут не задан """
    FULLWORDSONLY = 1
    """ Не использовать сокращения """
    INDICTIONARYONLY = 2
    """ Рассматривать только варианты из морфологического словаря """
    TERMONLY = 4
    """ Игнорировать морфологические варианты, а брать только термы (TextToken.Term) """
    CANBEGEOOBJECT = 8
    """ Может иметь географический объект в середине (Министерство РФ по делам ...) - игнорируем его при привязке! """
    IGNOREBRACKETS = 0x10
    """ Игнорировать скобки внутри нескольких термов """
    IGNORESTOPWORDS = 0x20
    """ Игнорировать знаки препинания, числа, союзы и предлоги """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)