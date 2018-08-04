# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class DecreeChangeValueKind(IntEnum):
    """ Типы изменяющих СЭ значений """
    UNDEFINED = 0
    TEXT = 0 + 1
    """ Текстовой фрагмент """
    WORDS = (0 + 1) + 1
    """ Слова (в точном значении) """
    ROBUSTWORDS = ((0 + 1) + 1) + 1
    """ Слова (в неточном значений) """
    NUMBERS = (((0 + 1) + 1) + 1) + 1
    """ Цифры """
    SEQUENCE = ((((0 + 1) + 1) + 1) + 1) + 1
    """ Предложение """
    FOOTNOTE = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    """ Сноска """
    BLOCK = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Блок со словами """