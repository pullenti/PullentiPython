# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class QuestionType(IntEnum):
    """ Абстрактные вопросы модели управления """
    UNDEFINED = 0
    """ Обычный вопрос """
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