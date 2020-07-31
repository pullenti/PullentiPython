﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class SemObjectType(IntEnum):
    """ Типы семантических объектов """
    UNDEFINED = 0
    NOUN = 1
    """ Существительное (в широком смысле, например, сущности) """
    ADJECTIVE = 2
    """ Прилагательное """
    VERB = 3
    """ Предикат (глагол) """
    PARTICIPLE = 4
    """ Причастие или деепричастие """
    ADVERB = 5
    """ Наречие """
    PRONOUN = 6
    """ Местоимение """
    PERSONALPRONOUN = 7
    """ Личное местоимение """
    QUESTION = 8
    """ Вопрос """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)