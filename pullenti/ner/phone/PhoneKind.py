# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class PhoneKind(IntEnum):
    """ Тип телефонного номера """
    UNDEFINED = 0
    HOME = 1
    """ Домашний """
    MOBILE = 2
    """ Мобильный """
    WORK = 3
    """ Рабочий """
    FAX = 4
    """ Факс """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)