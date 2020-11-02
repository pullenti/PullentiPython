# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


class ProxyReferent:
    
    def __init__(self) -> None:
        self.value = None;
        self.identity = None;
        self.referent = None;
        self.owner_slot = None;
        self.owner_referent = None;
    
    def __str__(self) -> str:
        return self.value
    
    @staticmethod
    def _new2846(_arg1 : str, _arg2 : 'Referent') -> 'ProxyReferent':
        res = ProxyReferent()
        res.value = _arg1
        res.owner_referent = _arg2
        return res