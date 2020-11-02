# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class NumberExType(IntEnum):
    # Единицы измерения для NumberExToken
    UNDEFINED = 0
    PERCENT = 1
    METER = 2
    MILLIMETER = 3
    KILOMETER = 4
    SANTIMETER = 5
    SANTIMETER2 = 6
    SANTIMETER3 = 7
    METER2 = 8
    AR = 9
    GEKTAR = 10
    KILOMETER2 = 11
    METER3 = 12
    MILE = 13
    GRAMM = 14
    MILLIGRAM = 15
    KILOGRAM = 16
    TONNA = 17
    LITR = 18
    MILLILITR = 19
    HOUR = 20
    MINUTE = 21
    SECOND = 22
    YEAR = 23
    MONTH = 24
    WEEK = 25
    DAY = 26
    MONEY = 27
    SHUK = 28
    UPAK = 29
    RULON = 30
    NABOR = 31
    KOMPLEKT = 32
    PARA = 33
    FLAKON = 34
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)