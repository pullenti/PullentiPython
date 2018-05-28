# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class DatePointerType(IntEnum):
    """ Дополнительные указатели для дат """
    NO = 0
    BEGIN = 1
    """ В начале """
    CENTER = 2
    """ В середине """
    END = 3
    """ В конце """
    TODAY = 4
    """ В настоящее время, сегодня """
    WINTER = 5
    """ Зимой """
    SPRING = 6
    """ Весной """
    SUMMER = 7
    """ Летом """
    AUTUMN = 8
    """ Осенью """
    UNDEFINED = 9
    """ Неопределено (например, 20__ года ) """