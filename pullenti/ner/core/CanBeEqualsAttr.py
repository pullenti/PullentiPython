# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class CanBeEqualsAttr(IntEnum):
    """ Атрибуты функции CanBeEqualsEx класса MiscHelper. Битовая маска.
    Атрибуты сравнения
    """
    NO = 0
    IGNORENONLETTERS = 1
    """ Игнорировать небуквенные символы (они как бы выбрасываются) """
    IGNOREUPPERCASE = 2
    """ Игнорировать регистр символов """
    CHECKMORPHEQUAFTERFIRSTNOUN = 4
    """ После первого существительного слова должны полностью совпадать
    (иначе совпадение с точностью до морфологии) """
    USEBRACKETS = 8
    """ Даже если указано IgnoreNonletters, кавычки проверять! """
    IGNOREUPPERCASEFIRSTWORD = 0x10
    """ Игнорировать регистр символов только первого слова """
    FIRSTCANBESHORTER = 0x20
    """ Первое слово может быть короче (то есть второе должно начинаться на первое слово) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)