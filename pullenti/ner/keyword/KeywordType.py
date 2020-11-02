# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class KeywordType(IntEnum):
    """ Тип ключевой комбинации """
    UNDEFINED = 0
    """ Неопределён """
    OBJECT = 1
    """ Объект (именная группа) """
    REFERENT = 2
    """ Именованная сущность """
    PREDICATE = 3
    """ Предикат (глагол) """
    ANNOTATION = 4
    """ Автоаннотация всего текста """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)