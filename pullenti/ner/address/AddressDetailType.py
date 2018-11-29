# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class AddressDetailType(IntEnum):
    UNDEFINED = 0
    CROSS = 0 + 1
    NEAR = (0 + 1) + 1
    HOSTEL = ((0 + 1) + 1) + 1
    NORTH = (((0 + 1) + 1) + 1) + 1
    SOUTH = ((((0 + 1) + 1) + 1) + 1) + 1
    WEST = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    EAST = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    NORTHWEST = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    NORTHEAST = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    SOUTHWEST = (((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    SOUTHEAST = ((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)