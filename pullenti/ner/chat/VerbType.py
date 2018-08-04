# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class VerbType(IntEnum):
    """ Тип глагольной формы """
    UNDEFINED = 0
    BE = 0 + 1
    """ Быть, являться """
    HAVE = (0 + 1) + 1
    """ Иметь """
    CAN = ((0 + 1) + 1) + 1
    """ Могу """
    MUST = (((0 + 1) + 1) + 1) + 1
    """ Должен """
    SAY = ((((0 + 1) + 1) + 1) + 1) + 1
    """ Говорить, произносить ... """
    CALL = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    """ Звонить """