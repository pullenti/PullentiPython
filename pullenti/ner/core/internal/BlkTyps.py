# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum


class BlkTyps(IntEnum):
    UNDEFINED = 0
    INDEX = 0 + 1
    INDEXITEM = (0 + 1) + 1
    INTRO = ((0 + 1) + 1) + 1
    LITERATURE = (((0 + 1) + 1) + 1) + 1
    APPENDIX = ((((0 + 1) + 1) + 1) + 1) + 1
    CONSLUSION = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    MISC = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    CHAPTER = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)