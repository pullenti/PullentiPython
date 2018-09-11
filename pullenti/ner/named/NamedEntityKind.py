# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class NamedEntityKind(IntEnum):
    """ Разновидности организаций """
    UNDEFINED = 0
    PLANET = 0 + 1
    LOCATION = (0 + 1) + 1
    MONUMENT = ((0 + 1) + 1) + 1
    BUILDING = (((0 + 1) + 1) + 1) + 1