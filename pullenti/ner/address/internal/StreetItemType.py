# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class StreetItemType(IntEnum):
    NOUN = 0
    """ Это существительное - улица, проезд и пр. """
    NAME = 0 + 1
    """ Это название """
    NUMBER = (0 + 1) + 1
    """ Номер """
    STDADJECTIVE = ((0 + 1) + 1) + 1
    """ Стандартное прилагательное (Большой, Средний ...) """
    STDNAME = (((0 + 1) + 1) + 1) + 1
    """ Стандартное имя """
    STDPARTOFNAME = ((((0 + 1) + 1) + 1) + 1) + 1
    """ Стандартная часть имени """
    AGE = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    """ 40-летия чего-то там """
    FIX = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    """ Некоторое фиусированное название (МКАД) """