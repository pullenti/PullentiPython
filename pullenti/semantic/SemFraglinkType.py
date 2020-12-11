﻿# Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class SemFraglinkType(IntEnum):
    """ Тип связи между фрагментами """
    UNDEFINED = 0
    """ Не определён """
    IFTHEN = 1
    """ Если - то """
    IFELSE = 2
    """ Если - иначе """
    BECAUSE = 3
    """ Потому что """
    BUT = 4
    """ Но (..., однако ...) """
    FOR = 5
    """ Для того, чтобы... """
    WHAT = 6
    """ Что """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)