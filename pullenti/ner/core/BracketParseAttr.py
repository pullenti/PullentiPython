# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from enum import IntEnum


class BracketParseAttr(IntEnum):
    """ Параметры выделения последовательности """
    NO = 0
    CANCONTAINSVERBS = 2
    """ По умолчанию, посл-ть не должна содержать чистых глаголов (если есть, то null).
     Почему так? Да потому, что это используется в основном для имён именованных
     сущностей, а там не может быть глаголов.
     Если же этот ключ указан, то глаголы не проверяются. """
    NEARCLOSEBRACKET = 4
    """ Брать первую же подходящую закрывающую кавычку """
    CANBEMANYLINES = 8
    """ Внутри могут быть переходы на новую строку (многострочный) """