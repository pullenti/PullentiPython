# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class NounPhraseParseAttr(IntEnum):
    """ Атрибуты выделения именных групп NounPhraseHelper.TryParse(). Битовая маска.
    Атрибуты выделения именной группы
    """
    NO = 0
    """ Нет атрибута """
    PARSEPRONOUNS = 1
    """ Выделять ли местоимения (моя страна) """
    PARSEPREPOSITION = 2
    """ Выделять ли в начале предлог """
    IGNOREADJBEST = 4
    """ Игнорировать прилагательные превосходной степени """
    IGNOREPARTICIPLES = 8
    """ Игнорировать причастия, брать только чистые прилагательные """
    REFERENTCANBENOUN = 0x10
    """ Корнем группы может выступать сущность (необъятная Россия) """
    CANNOTHASCOMMAAND = 0x20
    """ Между прилагательными не должно быть запятых и союзов """
    ADJECTIVECANBELAST = 0x40
    """ Прилагательное м.б. на последнем месте (член моржовый) """
    PARSEADVERBS = 0x80
    """ Выделять наречия """
    PARSEVERBS = 0x100
    """ Выделять причастия (это прилагательные и глаголы одновременно) """
    PARSENUMERICASADJECTIVE = 0x200
    """ Выделять ли такие конструкции, как "двое сотрудников", "пять компаний" числа как прилагательные.
    Это не касается ситуаций "второй сотрудник", "пятая компания" - это всегда как прилагательные. """
    MULTILINES = 0x400
    """ Группа может располагаться на нескольких строках (начало на одной, окончание на другой) """
    IGNOREBRACKETS = 0x800
    """ Игнорировать содержимое в скобках (...) внутри именной группы """
    MULTINOUNS = 0x1000
    """ Это для случая "грузовой и легковой автомобили" - то есть прилагательные
    относятся к одному существительному (как бы слепленному). См. NounPhraseMultivarToken. """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)