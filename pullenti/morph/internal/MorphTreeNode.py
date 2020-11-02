# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.morph.internal.MorphRuleVariantRef import MorphRuleVariantRef

class MorphTreeNode:
    
    def __init__(self) -> None:
        self.nodes = None;
        self.rule_ids = None;
        self.reverce_variants = None;
        self.lazy_pos = 0
    
    def calc_total_nodes(self) -> int:
        res = 0
        if (self.nodes is not None): 
            for v in self.nodes.items(): 
                res += (v[1].calc_total_nodes() + 1)
        return res
    
    def __str__(self) -> str:
        cou = (0 if self.rule_ids is None else len(self.rule_ids))
        return "{0} ({1}, {2})".format("?", self.calc_total_nodes(), cou)
    
    def __deserialize_base(self, str0_ : 'ByteArrayWrapper', pos : int) -> None:
        cou = str0_.deserialize_short(pos)
        if (cou > 0): 
            self.rule_ids = list()
            while cou > 0: 
                id0_ = str0_.deserialize_short(pos)
                if (id0_ == 0): 
                    pass
                self.rule_ids.append(id0_)
                cou -= 1
        cou = str0_.deserialize_short(pos)
        if (cou > 0): 
            self.reverce_variants = list()
            while cou > 0: 
                rid = str0_.deserialize_short(pos)
                if (rid == 0): 
                    pass
                id0_ = str0_.deserialize_short(pos)
                co = str0_.deserialize_short(pos)
                self.reverce_variants.append(MorphRuleVariantRef(rid, id0_, co))
                cou -= 1
    
    def _deserialize(self, str0_ : 'ByteArrayWrapper', pos : int) -> int:
        res = 0
        self.__deserialize_base(str0_, pos)
        cou = str0_.deserialize_short(pos)
        if (cou > 0): 
            self.nodes = dict()
            while cou > 0: 
                i = str0_.deserialize_short(pos)
                pp = str0_.deserialize_int(pos)
                child = MorphTreeNode()
                res1 = child._deserialize(str0_, pos)
                res += (1 + res1)
                self.nodes[i] = child
                cou -= 1
        return res
    
    def _deserialize_lazy(self, str0_ : 'ByteArrayWrapper', me : 'MorphEngine', pos : int) -> None:
        self.__deserialize_base(str0_, pos)
        cou = str0_.deserialize_short(pos)
        if (cou > 0): 
            self.nodes = dict()
            while cou > 0: 
                i = str0_.deserialize_short(pos)
                pp = str0_.deserialize_int(pos)
                child = MorphTreeNode()
                child.lazy_pos = pos.value
                self.nodes[i] = child
                pos.value = pp
                cou -= 1
        p = pos.value
        if (self.rule_ids is not None): 
            for rid in self.rule_ids: 
                r = me.get_mut_rule(rid)
                if (r.lazy_pos > 0): 
                    pos.value = r.lazy_pos
                    r._deserialize(str0_, pos)
                    r.lazy_pos = 0
            pos.value = p
        if (self.reverce_variants is not None): 
            for rv in self.reverce_variants: 
                r = me.get_mut_rule(rv.rule_id)
                if (r.lazy_pos > 0): 
                    pos.value = r.lazy_pos
                    r._deserialize(str0_, pos)
                    r.lazy_pos = 0
            pos.value = p