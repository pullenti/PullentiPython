# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class BlkTyps(IntEnum):
    UNDEFINED = 0
    INDEX = 1
    INDEXITEM = 2
    INTRO = 3
    LITERATURE = 4
    APPENDIX = 5
    CONSLUSION = 6
    MISC = 7
    CHAPTER = 8
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)