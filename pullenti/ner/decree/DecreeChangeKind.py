# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class DecreeChangeKind(IntEnum):
    """ Типы изменений структурных элементов (СЭ) """
    UNDEFINED = 0
    CONTAINER = 0 + 1
    """ Объединяет в себе другие изменения """
    APPEND = (0 + 1) + 1
    """ Дополнить другим СЭ-м или текстовыми конструкциями """
    EXPIRE = ((0 + 1) + 1) + 1
    """ СЭ утратил силу """
    NEW = (((0 + 1) + 1) + 1) + 1
    """ Изложить в редакции """
    EXCHANGE = ((((0 + 1) + 1) + 1) + 1) + 1
    """ Заменить одни текстовые конструкции другими """
    REMOVE = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    """ Удалить текстовые конструкции """
    CONSIDER = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Считать как """