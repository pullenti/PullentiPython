# Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.semantic.SemAttribute import SemAttribute

class SemAttributeEx:
    
    def __init__(self, mt : 'MetaToken') -> None:
        self.token = None;
        self.attr = SemAttribute()
        self.token = mt
    
    @staticmethod
    def _new2945(_arg1 : 'MetaToken', _arg2 : 'SemAttribute') -> 'SemAttributeEx':
        res = SemAttributeEx(_arg1)
        res.attr = _arg2
        return res