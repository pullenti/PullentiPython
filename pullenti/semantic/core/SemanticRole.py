﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class SemanticRole(IntEnum):
    """ Семантические роли """
    COMMON = 0
    """ Обычная """
    AGENT = 1
    """ Агент """
    PACIENT = 2
    """ Пациент """
    STRONG = 3
    """ Сильная связь """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)