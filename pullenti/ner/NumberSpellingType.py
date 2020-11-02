# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class NumberSpellingType(IntEnum):
    """ Тип написания числительного NumberToken
    Тип числительного
    """
    DIGIT = 0
    """ Цифрами """
    ROMAN = 1
    """ Римскими цифрами """
    WORDS = 2
    """ Прописью (словами) """
    AGE = 3
    """ Возраст (летие) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)