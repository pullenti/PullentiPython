# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class MeasureKind(IntEnum):
    """ Что измеряется этой величиной """
    UNDEFINED = 0
    TIME = 1
    """ Время """
    LENGTH = 2
    """ Длина """
    AREA = 3
    """ Площадь """
    VOLUME = 4
    """ Объём """
    WEIGHT = 5
    """ Вес """
    SPEED = 6
    """ Скорость """
    TEMPERATURE = 7
    """ Температура """
    IP = 8
    """ Класс защиты """
    PERCENT = 9
    """ Процент """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)