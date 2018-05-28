# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class NumberSpellingType(IntEnum):
    """ Возможные типы написаний """
    DIGIT = 0
    """ Цифрами """
    ROMAN = 1
    """ Римскими цифрами """
    WORDS = 2
    """ Прописью (словами) """
    AGE = 3
    """ Возраст (летие) """