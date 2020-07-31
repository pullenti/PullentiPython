﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.semantic.SemAttributeType import SemAttributeType

class SemAttribute:
    """ Семантический атрибут """
    
    def __init__(self) -> None:
        self.typ = SemAttributeType.UNDEFINED
        self.spelling = None;
        self.not0_ = False
    
    def __str__(self) -> str:
        return self.spelling
    
    @staticmethod
    def _new2976(_arg1 : bool, _arg2 : 'SemAttributeType', _arg3 : str) -> 'SemAttribute':
        res = SemAttribute()
        res.not0_ = _arg1
        res.typ = _arg2
        res.spelling = _arg3
        return res
    
    @staticmethod
    def _new3015(_arg1 : str, _arg2 : 'SemAttributeType', _arg3 : bool) -> 'SemAttribute':
        res = SemAttribute()
        res.spelling = _arg1
        res.typ = _arg2
        res.not0_ = _arg3
        return res
    
    @staticmethod
    def _new3017(_arg1 : 'SemAttributeType', _arg2 : str) -> 'SemAttribute':
        res = SemAttribute()
        res.typ = _arg1
        res.spelling = _arg2
        return res