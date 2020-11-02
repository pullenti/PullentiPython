# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class DecreeChangeKind(IntEnum):
    """ Типы изменений структурных элементов (СЭ) """
    UNDEFINED = 0
    CONTAINER = 1
    """ Объединяет в себе другие изменения """
    APPEND = 2
    """ Дополнить другим СЭ-м или текстовыми конструкциями """
    EXPIRE = 3
    """ СЭ утратил силу """
    NEW = 4
    """ Изложить в редакции """
    EXCHANGE = 5
    """ Заменить одни текстовые конструкции другими """
    REMOVE = 6
    """ Удалить текстовые конструкции """
    CONSIDER = 7
    """ Считать как """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)