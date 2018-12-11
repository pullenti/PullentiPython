# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class OrganizationKind(IntEnum):
    """ Разновидности организаций """
    UNDEFINED = 0
    GOVENMENT = 1
    PARTY = 2
    STUDY = 3
    SCIENCE = 4
    PRESS = 5
    MEDIA = 6
    FACTORY = 7
    BANK = 8
    CULTURE = 9
    MEDICAL = 10
    TRADE = 11
    HOLDING = 12
    DEPARTMENT = 13
    FEDERATION = 14
    HOTEL = 15
    JUSTICE = 16
    CHURCH = 17
    MILITARY = 18
    AIRPORT = 19
    FESTIVAL = 20
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)