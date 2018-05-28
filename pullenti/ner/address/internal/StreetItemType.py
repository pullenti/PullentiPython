# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class StreetItemType(IntEnum):
    NOUN = 0
    """ Это существительное - улица, проезд и пр. """
    NAME = 1
    """ Это название """
    NUMBER = 2
    """ Номер """
    STDADJECTIVE = 3
    """ Стандартное прилагательное (Большой, Средний ...) """
    STDNAME = 4
    """ Стандартное имя """
    STDPARTOFNAME = 5
    """ Стандартная часть имени """
    AGE = 6
    """ 40-летия чего-то там """
    FIX = 7
    """ Некоторое фиусированное название (МКАД) """