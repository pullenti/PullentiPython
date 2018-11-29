# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


class LazyInfo:
    
    def __init__(self) -> None:
        self.engine = None;
        self.data = None;
        self.begin = 0
    
    def loadNode(self, tn : 'MorphTreeNode') -> None:
        with self.engine._m_lock: 
            from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper
            self.data.seek(self.begin)
            MorphSerializeHelper._deserializeMorphTreeNodeLazy(self.data, tn, self.engine)
    
    def __str__(self) -> str:
        return "Lazy:{0}".format(self.begin)