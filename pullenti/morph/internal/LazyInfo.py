# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 


class LazyInfo:
    
    def __init__(self) -> None:
        self.engine = None
        self.data = None
        self.begin = 0
    
    def load_node(self, tn : 'MorphTreeNode') -> None:
        with self.engine._m_lock: 
            from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper
            self.data.seek(self.begin)
            MorphSerializeHelper._deserialize_morph_tree_node_lazy(self.data, tn, self.engine)