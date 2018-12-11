# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class AddressDetailType(IntEnum):
    UNDEFINED = 0
    CROSS = 1
    NEAR = 2
    HOSTEL = 3
    NORTH = 4
    SOUTH = 5
    WEST = 6
    EAST = 7
    NORTHWEST = 8
    NORTHEAST = 9
    SOUTHWEST = 10
    SOUTHEAST = 11
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)