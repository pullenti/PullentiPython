# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class NormalizeTextAttr(IntEnum):
    """ Атрибуты нормализации текста """
    NO = 0
    KEEPREGISTER = 1
    """ Сохранять ли регистр букв (по умолчанию, верхний регистр) """
    KEEPPUNCTUATION = 2
    """ Игонорировать пунктуацию, скобки, кавычки и пр. несимволы и не числа """
    NERPROCESS = 4
    """ Выделять ли именованные сущности и их потом нормализовывать (через ToString()) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)