# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class GetTextAttr(IntEnum):
    """ Атрибуты получения текста """
    NO = 0
    KEEPREGISTER = 1
    """ Сохранять ли регистр букв (по умолчанию, верхний регистр) """
    FIRSTNOUNGROUPTONOMINATIVE = 2
    """ Первую именную группу преобразовывать к именительному падежу """
    FIRSTNOUNGROUPTONOMINATIVESINGLE = 4
    """ Первую именную группу преобразовывать к именительному падежу единственному числу """
    KEEPQUOTES = 8
    """ Оставлять кавычки (по умолчанию, кавычки игнорируются). К скобкам это не относится. """
    IGNOREGEOREFERENT = 0x10
    """ Игнорировать географические объекты """
    NORMALIZENUMBERS = 0x20
    """ Преобразовать ли числовые значения в цифры """
    RESTOREREGISTER = 0x40
    """ Если все слова в верхнем регистре, то попытаться восстановить слова в нижнем регистре
     на основе их встречаемости в других частях всего документа
     (то есть если слово есть в нижнем, то оно переводится в нижний) """
    IGNOREARTICLES = 0x80
    """ Для английского языка игнорировать артикли и суффикс 'S """