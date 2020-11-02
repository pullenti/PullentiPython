# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class NGItem:
    
    def __init__(self) -> None:
        self.source = None;
        self.order = 0
        self.comma_before = False
        self.comma_after = False
        self.and_before = False
        self.and_after = False
        self.or_before = False
        self.or_after = False
        self.links = list()
        self.ind = 0
    
    @property
    def res_object(self) -> 'SemObject':
        return (None if self.source is None else self.source.result)
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.comma_before): 
            print("[,] ", end="", file=tmp)
        elif (self.or_before): 
            print("[|] ", end="", file=tmp)
        elif (self.and_before): 
            print("[&] ", end="", file=tmp)
        print(str(self.source), end="", file=tmp)
        if (self.comma_after): 
            print(" [,]", end="", file=tmp)
        elif (self.or_after): 
            print(" [|]", end="", file=tmp)
        elif (self.and_after): 
            print(" [&]", end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    def prepare(self) -> None:
        self.links.clear()
    
    @staticmethod
    def _new2922(_arg1 : 'SentItem') -> 'NGItem':
        res = NGItem()
        res.source = _arg1
        return res
    
    @staticmethod
    def _new2923(_arg1 : 'SentItem', _arg2 : bool, _arg3 : bool, _arg4 : bool) -> 'NGItem':
        res = NGItem()
        res.source = _arg1
        res.comma_before = _arg2
        res.and_before = _arg3
        res.or_before = _arg4
        return res
    
    @staticmethod
    def _new2928(_arg1 : 'SentItem', _arg2 : int) -> 'NGItem':
        res = NGItem()
        res.source = _arg1
        res.order = _arg2
        return res