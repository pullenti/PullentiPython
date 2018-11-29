﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class OrganizationKind(IntEnum):
    """ Разновидности организаций """
    UNDEFINED = 0
    GOVENMENT = 0 + 1
    PARTY = (0 + 1) + 1
    STUDY = ((0 + 1) + 1) + 1
    SCIENCE = (((0 + 1) + 1) + 1) + 1
    PRESS = ((((0 + 1) + 1) + 1) + 1) + 1
    MEDIA = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    FACTORY = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    BANK = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    CULTURE = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    MEDICAL = (((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    TRADE = ((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    HOLDING = (((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    DEPARTMENT = ((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    FEDERATION = (((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    HOTEL = ((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    JUSTICE = (((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    CHURCH = ((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    MILITARY = (((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    AIRPORT = ((((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    FESTIVAL = (((((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)