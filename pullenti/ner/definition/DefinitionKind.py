# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class DefinitionKind(IntEnum):
    """ Тип определения """
    UNDEFINED = 0
    ASSERTATION = 0 + 1
    DEFINITION = (0 + 1) + 1
    NEGATION = ((0 + 1) + 1) + 1