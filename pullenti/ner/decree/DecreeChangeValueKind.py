﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class DecreeChangeValueKind(IntEnum):
    """ Типы изменяющих СЭ значений """
    UNDEFINED = 0
    TEXT = 1
    """ Текстовой фрагмент """
    WORDS = 2
    """ Слова (в точном значении) """
    ROBUSTWORDS = 3
    """ Слова (в неточном значений) """
    NUMBERS = 4
    """ Цифры """
    SEQUENCE = 5
    """ Предложение """
    FOOTNOTE = 6
    """ Сноска """
    BLOCK = 7
    """ Блок со словами """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)