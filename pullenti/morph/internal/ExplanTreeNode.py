# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.morph.DerivateGroup import DerivateGroup


class ExplanTreeNode:
    
    def __init__(self) -> None:
        self.nodes = None
        self.groups = None
        self._lazy = None
    
    def _load(self) -> None:
        if (self._lazy is None): 
            return
        self._lazy.load_node(self)
        self._lazy = None
    
    def _add_group(self, gr : 'DerivateGroup') -> None:
        if (self.groups is None): 
            self.groups = gr
            return
        li = (self.groups if isinstance(self.groups, list) else None)
        if (li is None): 
            li = list()
            if (isinstance(self.groups, DerivateGroup)): 
                li.append(self.groups if isinstance(self.groups, DerivateGroup) else None)
        if (not gr in li): 
            li.append(gr)
        self.groups = li