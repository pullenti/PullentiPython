# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


class ExplanTreeNode:
    
    def __init__(self) -> None:
        self.nodes = None;
        self.groups = None;
        self.lazy_pos = 0
    
    def _deserialize(self, str0_ : 'ByteArrayWrapper', dic : 'DerivateDictionary', lazy_load : bool, pos : int) -> None:
        cou = str0_.deserialize_short(pos)
        li = (list() if cou > 0 else None)
        while cou > 0: 
            id0_ = str0_.deserialize_int(pos)
            if (id0_ > 0 and id0_ <= len(dic._m_all_groups)): 
                gr = dic._m_all_groups[id0_ - 1]
                if (gr._lazy_pos > 0): 
                    p0 = pos.value
                    pos.value = gr._lazy_pos
                    gr._deserialize(str0_, pos)
                    gr._lazy_pos = 0
                    pos.value = p0
            li.append(id0_)
            cou -= 1
        if (li is not None): 
            self.groups = li
        cou = str0_.deserialize_short(pos)
        if (cou == 0): 
            return
        while cou > 0: 
            ke = str0_.deserialize_short(pos)
            p1 = str0_.deserialize_int(pos)
            tn1 = ExplanTreeNode()
            if (self.nodes is None): 
                self.nodes = dict()
            sh = ke
            if (lazy_load): 
                tn1.lazy_pos = pos.value
                pos.value = p1
            else: 
                tn1._deserialize(str0_, dic, False, pos)
            if (not sh in self.nodes): 
                self.nodes[sh] = tn1
            cou -= 1