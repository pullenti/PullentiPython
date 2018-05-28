# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class NounPhraseParseAttr(IntEnum):
    """ Параметры выделения """
    NO = 0
    PARSEPRONOUNS = 1
    """ Выделять ли местоимения (моя страна) """
    PARSEPREPOSITION = 2
    """ Выделять ли в начале предлог """
    IGNOREADJBEST = 4
    """ Игнорировать прилагательные превосходной степени """
    IGNOREPARTICIPLES = 8
    """ Игнорировать причастия, брать только чистые прилагательные """
    REFERENTCANBENOUN = 0x10
    """ Корнем может выступать выделенная сущность (необъятная Россия) """
    CANNOTHASCOMMAAND = 0x20
    """ Между прилагательными не должно быть запятых и союзов """
    ADJECTIVECANBELAST = 0x40
    """ Прилагательное м.б. на последнем месте (член моржовый) """
    PARSEADVERBS = 0x80
    """ Выделять наречия """
    PARSEVERBS = 0x100
    """ Выделять причастия (это прилагательные и глаголы одновременно) """
    PARSENUMERICASADJECTIVE = 0x200
    """ Выделять ли такие констркуции "двое сотрудников", "пять компаний" числа как прилагательные.
     Это не касается ситуаций "второй сотрудник", "пятая компания" - это всегда как прилагательные """
    MULTILINES = 0x400
    """ Группа может быть на разбита на нескольких строках (начало на одной, окончание на другой) """