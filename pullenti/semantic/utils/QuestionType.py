# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class QuestionType(IntEnum):
    """ Основные вопросы модели управления """
    UNDEFINED = 0
    WHERE = 1
    """ Где """
    WHEREFROM = 2
    """ Откуда """
    WHERETO = 4
    """ Куда """
    WHEN = 8
    """ Когда """
    WHATTODO = 0x10
    """ Что делать (инфинитив за группой) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)