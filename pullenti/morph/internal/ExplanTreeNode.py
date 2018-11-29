# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.morph.DerivateGroup import DerivateGroup


class ExplanTreeNode:
    
    def __init__(self) -> None:
        self.nodes = None;
        self.groups = None;
        self._lazy = None
    
    def _load(self) -> None:
        if (self._lazy is None): 
            return
        self._lazy.loadNode(self)
        self._lazy = (None)
    
    def _addGroup(self, gr : 'DerivateGroup') -> None:
        if (self.groups is None): 
            self.groups = (gr)
            return
        li = Utils.asObjectOrNull(self.groups, list)
        if (li is None): 
            li = list()
            if (isinstance(self.groups, DerivateGroup)): 
                li.append(Utils.asObjectOrNull(self.groups, DerivateGroup))
        if (not gr in li): 
            li.append(gr)
        self.groups = (li)