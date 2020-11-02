# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class SemLinkType(IntEnum):
    """ Тип семантической связи """
    UNDEFINED = 0
    DETAIL = 1
    """ Детализация (какой?) """
    NAMING = 2
    """ Именование """
    AGENT = 3
    """ Агент (кто действует) """
    PACIENT = 4
    """ Пациент (на кого действуют) """
    PARTICIPLE = 5
    """ Причастный и деепричастный оборот """
    ANAFOR = 6
    """ Анафорическая ссылка (он, который, ...) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)