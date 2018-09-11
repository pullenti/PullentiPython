# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class TerminParseAttr(IntEnum):
    """ Патаметры выделения термина словаря (TryParse) """
    NO = 0
    FULLWORDSONLY = 1
    INDICTIONARYONLY = 2
    TERMONLY = 4
    CANBEGEOOBJECT = 8
    IGNOREBRACKETS = 0x10
    IGNORESTOPWORDS = 0x20