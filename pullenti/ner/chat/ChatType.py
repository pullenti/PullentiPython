# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class ChatType(IntEnum):
    """ Типы диалоговых элементов """
    UNDEFINED = 0
    THANKS = 1
    MISC = 2
    HELLO = 3
    BYE = 4
    ACCEPT = 5
    CANCEL = 6
    BUSY = 7
    VERB = 8
    LATER = 9
    DATE = 10
    REPEAT = 11
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)