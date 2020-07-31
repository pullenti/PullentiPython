﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.semantic.SemAttribute import SemAttribute

class SemAttributeEx:
    
    def __init__(self, mt : 'MetaToken') -> None:
        self.token = None;
        self.attr = SemAttribute()
        self.token = mt
    
    @staticmethod
    def _new3016(_arg1 : 'MetaToken', _arg2 : 'SemAttribute') -> 'SemAttributeEx':
        res = SemAttributeEx(_arg1)
        res.attr = _arg2
        return res