# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class AddressDetailType(IntEnum):
    """ Детализация местоположения """
    UNDEFINED = 0
    CROSS = 1
    """ Пересечение """
    NEAR = 2
    """ Возле """
    HOSTEL = 3
    """ Общежитие """
    NORTH = 4
    """ На север """
    SOUTH = 5
    """ На юг """
    WEST = 6
    """ На запад """
    EAST = 7
    """ На восток """
    NORTHWEST = 8
    """ На сереро-запад """
    NORTHEAST = 9
    """ На северо-восток """
    SOUTHWEST = 10
    """ На юго-запад """
    SOUTHEAST = 11
    """ На юго-восток """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)