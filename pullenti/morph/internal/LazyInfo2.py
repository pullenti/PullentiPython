# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.morph.internal.ExplanSerializeHelper import ExplanSerializeHelper
from pullenti.morph.Explanatory import Explanatory

class LazyInfo2:
    
    def __init__(self) -> None:
        self.data = None;
        self.dic = None;
        self.begin = 0
    
    def loadNode(self, tn : 'ExplanTreeNode') -> None:
        with Explanatory._m_lock: 
            self.data.seek(self.begin)
            ExplanSerializeHelper.deserializeTreeNode(self.data, self.dic, tn, True)
    
    @staticmethod
    def _new5(_arg1 : int, _arg2 : 'ByteArrayWrapper', _arg3 : 'DerivateDictionary') -> 'LazyInfo2':
        res = LazyInfo2()
        res.begin = _arg1
        res.data = _arg2
        res.dic = _arg3
        return res