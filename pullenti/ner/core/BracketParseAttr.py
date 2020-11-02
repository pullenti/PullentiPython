# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class BracketParseAttr(IntEnum):
    """ Атрибуты выделения последовательности между скобок-кавычек. Битовая маска.
    Атрибуты выделения скобок и кавычек
    """
    NO = 0
    """ Нет """
    CANCONTAINSVERBS = 2
    """ По умолчанию, посл-ть не должна содержать чистых глаголов (если есть, то null).
    Почему так? Да потому, что это используется в основном для имён у именованных
    сущностей, а там не может быть глаголов.
    Если же этот ключ указан, то глаголы не проверяются. """
    NEARCLOSEBRACKET = 4
    """ Брать первую же подходящую закрывающую кавычку. Если не задано, то может искать сложные
    случаи вложенных кавычек. """
    CANBEMANYLINES = 8
    """ Внутри могут быть переходы на новую строку (многострочный) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)