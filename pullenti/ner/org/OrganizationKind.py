# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class OrganizationKind(IntEnum):
    """ Категории организаций. Не хранятся, а вычисляются на основе других атрибутов. """
    UNDEFINED = 0
    """ Неопределённая """
    GOVENMENT = 1
    """ Правительственная """
    PARTY = 2
    """ Политическая """
    STUDY = 3
    """ Образовательная """
    SCIENCE = 4
    """ Научно-исследовательская """
    PRESS = 5
    """ Пресса """
    MEDIA = 6
    """ Масс-медиа """
    FACTORY = 7
    """ Производственная """
    BANK = 8
    """ Банковская """
    CULTURE = 9
    """ Культурная """
    MEDICAL = 10
    """ Медицинская """
    TRADE = 11
    """ Торговая """
    HOLDING = 12
    """ Холдинг """
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
    SEAPORT = 20
    """ Морские порты """
    FESTIVAL = 21
    """ События (фестиваль, чемпионат) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)