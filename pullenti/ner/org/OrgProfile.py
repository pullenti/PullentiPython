# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class OrgProfile(IntEnum):
    """ Профили организации, хранятся в атрибутах ATTR_PROFILE, может быть несколько. """
    UNDEFINED = 0
    UNIT = 1
    UNION = 2
    COMPETITION = 3
    HOLDING = 4
    STATE = 5
    BUSINESS = 6
    FINANCE = 7
    EDUCATION = 8
    SCIENCE = 9
    INDUSTRY = 10
    TRADE = 11
    MEDICINE = 12
    POLICY = 13
    JUSTICE = 14
    ENFORCEMENT = 15
    ARMY = 16
    SPORT = 17
    RELIGION = 18
    ART = 19
    MUSIC = 20
    SHOW = 21
    MEDIA = 22
    PRESS = 23
    HOTEL = 24
    FOOD = 25
    TRANSPORT = 26
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)