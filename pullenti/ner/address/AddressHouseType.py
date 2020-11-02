# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class AddressHouseType(IntEnum):
    """ Тип дома """
    UNDEFINED = 0
    ESTATE = 1
    """ Владение """
    HOUSE = 2
    """ Просто дом """
    HOUSEESTATE = 3
    """ Домовладение """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)