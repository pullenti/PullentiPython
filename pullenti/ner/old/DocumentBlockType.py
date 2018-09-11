# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class DocumentBlockType(IntEnum):
    """ Типы текстов """
    UNDEFINED = 0
    TITLE = 0 + 1
    TAIL = (0 + 1) + 1
    INTRODUCTION = ((0 + 1) + 1) + 1
    CONCLUSION = (((0 + 1) + 1) + 1) + 1
    LITERATURE = ((((0 + 1) + 1) + 1) + 1) + 1
    APPENDIX = (((((0 + 1) + 1) + 1) + 1) + 1) + 1