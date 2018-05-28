# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class OrganizationKind(IntEnum):
    """ Разновидности организаций """
    UNDEFINED = 0
    """ Неопределённая """
    GOVENMENT = 1
    PARTY = 2
    STUDY = 3
    SCIENCE = 4
    """ Научно-исследовательские """
    PRESS = 5
    MEDIA = 6
    FACTORY = 7
    BANK = 8
    CULTURE = 9
    MEDICAL = 10
    TRADE = 11
    HOLDING = 12
    DEPARTMENT = 13
    """ Подразделение """
    FEDERATION = 14
    """ Федерация, Союз и т.п. непонятность """
    HOTEL = 15
    """ Отели, Санатории, Пансионаты ... """
    JUSTICE = 16
    """ Суды, тюрьмы ... """
    CHURCH = 17
    """ Церкви, религиозное """
    MILITARY = 18
    """ Военные """
    AIRPORT = 19
    """ Аэропорт """
    FESTIVAL = 20
    """ События (фестиваль, чемпионат) """