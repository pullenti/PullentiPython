# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class BookLinkTyp(IntEnum):
    UNDEFINED = 0
    NUMBER = 1
    PERSON = 2
    EDITORS = 3
    SOSTAVITEL = 4
    NAME = 5
    NAMETAIL = 6
    DELIMETER = 7
    TYPE = 8
    YEAR = 9
    PAGES = 10
    PAGERANGE = 11
    GEO = 12
    MISC = 13
    ANDOTHERS = 14
    TRANSLATE = 15
    PRESS = 16
    N = 17
    VOLUME = 18
    ELECTRONRES = 19
    URL = 20
    SEE = 21
    TAMZE = 22
    """ там же """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)