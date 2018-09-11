# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class GetTextAttr(IntEnum):
    """ Атрибуты получения текста """
    NO = 0
    KEEPREGISTER = 1
    FIRSTNOUNGROUPTONOMINATIVE = 2
    FIRSTNOUNGROUPTONOMINATIVESINGLE = 4
    KEEPQUOTES = 8
    IGNOREGEOREFERENT = 0x10
    NORMALIZENUMBERS = 0x20
    RESTOREREGISTER = 0x40
    IGNOREARTICLES = 0x80