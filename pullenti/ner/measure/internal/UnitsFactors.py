# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class UnitsFactors(IntEnum):
    # Степени десяток
    NO = 0
    KILO = 3
    MEGA = 6
    GIGA = 9
    TERA = 12
    DECI = -1
    CENTI = -2
    MILLI = -3
    MICRO = -6
    NANO = -9
    PICO = -12
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)