# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class OrgProfile(IntEnum):
    """ Профили организации, хранятся в атрибутах ATTR_PROFILE, может быть несколько. """
    UNDEFINED = 0
    """ Неопределённое """
    UNIT = 1
    """ Подразделение, отдел """
    UNION = 2
    """ Различные объединения людей (фонды, движения, партии, ассоциации) """
    COMPETITION = 3
    """ Соревнование, конкурс, чемпионат """
    HOLDING = 4
    """ Группы компаний, холдинги """
    STATE = 5
    """ Государственные """
    BUSINESS = 6
    """ Бизнес, коммерция """
    FINANCE = 7
    """ Финансы (банки, фонды) """
    EDUCATION = 8
    """ Образование """
    SCIENCE = 9
    """ Наука """
    INDUSTRY = 10
    """ Производство """
    TRADE = 11
    """ Торговля, реализация """
    MEDICINE = 12
    """ Медицина """
    POLICY = 13
    """ Политика """
    JUSTICE = 14
    """ Судебная система """
    ENFORCEMENT = 15
    """ Силовые структуры """
    ARMY = 16
    """ Армейские структуры """
    SPORT = 17
    """ Спорт """
    RELIGION = 18
    """ Религиозные """
    ART = 19
    """ Искусство """
    MUSIC = 20
    """ Музыка, группы """
    SHOW = 21
    """ Театры, выставки, музеи, концерты """
    MEDIA = 22
    """ Срадства массовой информации """
    PRESS = 23
    """ Издательства, газеты, журналы ... (обычно вместе с Media) """
    HOTEL = 24
    """ пансионаты, отели, дома отдыха """
    FOOD = 25
    """ Предприятия питания """
    TRANSPORT = 26
    """ Железные дороги, авиакомпании ... """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)