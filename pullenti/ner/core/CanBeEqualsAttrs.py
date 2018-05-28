# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class CanBeEqualsAttrs(IntEnum):
    """ Атрибуты функции CanBeEqualsEx """
    NO = 0
    IGNORENONLETTERS = 1
    """ Игнорировать небуквенные символы (они как бы выбрасываются) """
    IGNOREUPPERCASE = 2
    """ Игнорировать регистр символов """
    CHECKMORPHEQUAFTERFIRSTNOUN = 4
    """ После первого существительного слова должны полностью совпадать
     (иначе совпадение с точностью до морфологии) """
    USEBRACKETS = 8
    """ Даже если указано IgnoreNonletters, кавычки проверять! """
    IGNOREUPPERCASEFIRSTWORD = 0x10
    """ Игнорировать регистр символов только первого слова """