# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 


class MorphTreeNode:
    
    def __init__(self) -> None:
        self.nodes = None
        self.rules = None
        self.reverce_variants = None
        self._lazy = None
    
    def calc_total_nodes(self) -> int:
        res = 0
        if (self.nodes is not None): 
            for v in self.nodes.items(): 
                res += (v[1].calc_total_nodes() + 1)
        return res
    
    def __str__(self) -> str:
        return "{0} ({1}, {2})".format("?", self.calc_total_nodes(), (0 if self.rules is None else len(self.rules)))
    
    def _load(self) -> None:
        if (self._lazy is None): 
            return
        self._lazy.load_node(self)
        self._lazy = None