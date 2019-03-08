# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class DecreeKind(IntEnum):
    """ Типы нормативных актов """
    UNDEFINED = 0
    KODEX = 1
    """ Кодекс """
    USTAV = 2
    """ Устав """
    KONVENTION = 3
    """ Конвенция """
    CONTRACT = 4
    """ Договор, контракт """
    PROJECT = 5
    """ Проект """
    PUBLISHER = 6
    """ Источники опубликований """
    PROGRAM = 7
    """ Госпрограммы """
    STANDARD = 8
    """ Стандарт (ГОСТ, ТУ, ANSI и пр.) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)