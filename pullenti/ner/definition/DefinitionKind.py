# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class DefinitionKind(IntEnum):
    """ Тип определения """
    UNDEFINED = 0
    """ Непонятно """
    ASSERTATION = 1
    """ Просто утрерждение """
    DEFINITION = 2
    """ Строгое определение """
    NEGATION = 3
    """ Отрицание """