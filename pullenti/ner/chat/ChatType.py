# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class ChatType(IntEnum):
    """ Типы диалоговых элементов """
    UNDEFINED = 0
    THANKS = 0 + 1
    MISC = (0 + 1) + 1
    HELLO = ((0 + 1) + 1) + 1
    BYE = (((0 + 1) + 1) + 1) + 1
    ACCEPT = ((((0 + 1) + 1) + 1) + 1) + 1
    CANCEL = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    BUSY = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
    VERB = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    LATER = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    DATE = (((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
    REPEAT = ((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1