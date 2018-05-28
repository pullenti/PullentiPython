# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 


class LazyInfo2:
    
    def __init__(self) -> None:
        self.data = None
        self.dic = None
        self.begin = 0
    
    def load_node(self, tn : 'ExplanTreeNode') -> None:
        from pullenti.morph.Explanatory import Explanatory
        with Explanatory._m_lock: 
            from pullenti.morph.internal.ExplanSerializeHelper import ExplanSerializeHelper
            self.data.seek(self.begin)
            ExplanSerializeHelper.deserialize_tree_node(self.data, self.dic, tn, True)

    
    @staticmethod
    def _new5(_arg1 : int, _arg2 : 'ByteArrayWrapper', _arg3 : 'DerivateDictionary') -> 'LazyInfo2':
        res = LazyInfo2()
        res.begin = _arg1
        res.data = _arg2
        res.dic = _arg3
        return res