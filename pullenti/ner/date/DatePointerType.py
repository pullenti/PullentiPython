# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class DatePointerType(IntEnum):
    """ Дополнительные указатели для дат """
    NO = 0
    BEGIN = 0 + 1
    """ В начале """
    CENTER = (0 + 1) + 1
    """ В середине """
    END = ((0 + 1) + 1) + 1
    """ В конце """
    TODAY = (((0 + 1) + 1) + 1) + 1
    """ В настоящее время, сегодня """
    WINTER = ((((0 + 1) + 1) + 1) + 1) + 1
    """ Зимой """
    SPRING = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    """ Весной """
    SUMMER = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Летом """
    AUTUMN = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Осенью """
    UNDEFINED = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Неопределено (например, 20__ года ) """