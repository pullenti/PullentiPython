# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper


class GeneralRelationHelper:
    
    class Node:
        
        def __init__(self) -> None:
            self.ref = None
            self.ad = None
            self.refs_to = None
            self.refs_from = None
            self.gen_to = None
            self.gen_from = None
            self.deleted = False
        
        def __str__(self) -> str:
            return str(self.ref)
        
        def is_in_gen_parents_or_higher(self, n : 'Node') -> bool:
            if (self.gen_to is None): 
                return False
            for p in self.gen_to: 
                if (p == n): 
                    return True
                elif (p.is_in_gen_parents_or_higher(n)): 
                    return True
            return False
        
        def replace_values(self, new_node : 'Node') -> None:
            if (self.refs_from is not None): 
                for fr in self.refs_from: 
                    ch = False
                    for s in fr.ref.slots: 
                        if (s.value == self.ref): 
                            fr.ref.upload_slot(s, new_node.ref)
                            ch = True
                    if (not ch): 
                        continue
                    i = 0
                    while i < (len(fr.ref.slots) - 1): 
                        j = i + 1
                        while j < len(fr.ref.slots): 
                            if (fr.ref.slots[i].type_name == fr.ref.slots[j].type_name and fr.ref.slots[i].value == fr.ref.slots[j].value): 
                                del fr.ref.slots[j]
                                j -= 1
                            j += 1
                        i += 1
        
        @staticmethod
        def _new1480(_arg1 : 'Referent', _arg2 : 'AnalyzerData') -> 'Node':
            res = GeneralRelationHelper.Node()
            res.ref = _arg1
            res.ad = _arg2
            return res
    
    @staticmethod
    def refresh_generals(proc : 'Processor', kit : 'AnalysisKit') -> None:
        from pullenti.ner.Referent import Referent
        all0_ = dict()
        all_refs = list()
        for a in proc.analyzers: 
            ad = kit.get_analyzer_data(a)
            if (ad is None): 
                continue
            for r in ad.referents: 
                nod = GeneralRelationHelper.Node._new1480(r, ad)
                all_refs.append(nod)
                r.tag = nod
                inoutarg1483 = RefOutArgWrapper(None)
                inoutres1484 = Utils.tryGetValue(all0_, a.name, inoutarg1483)
                si = inoutarg1483.value
                if (not inoutres1484): 
                    si = dict()
                    all0_[a.name] = si
                strs = r.get_compare_strings()
                if (strs is None or len(strs) == 0): 
                    continue
                for s in strs: 
                    li = [ ]
                    inoutarg1481 = RefOutArgWrapper(None)
                    inoutres1482 = Utils.tryGetValue(si, s, inoutarg1481)
                    li = inoutarg1481.value
                    if (not inoutres1482): 
                        li = list()
                        si[s] = li
                    li.append(r)
        for r in all_refs: 
            for s in r.ref.slots: 
                if (isinstance(s.value, Referent)): 
                    to = (s.value if isinstance(s.value, Referent) else None)
                    tn = (to.tag if isinstance(to.tag, GeneralRelationHelper.Node) else None)
                    if (tn is None): 
                        continue
                    if (tn.refs_from is None): 
                        tn.refs_from = list()
                    tn.refs_from.append(r)
                    if (r.refs_to is None): 
                        r.refs_to = list()
                    r.refs_to.append(tn)
        for ty in all0_.values(): 
            for li in ty.values(): 
                if (len(li) < 2): 
                    continue
                i = 0
                while i < len(li): 
                    j = i + 1
                    while j < len(li): 
                        n1 = None
                        n2 = None
                        if (li[i].can_be_general_for(li[j]) and not li[j].can_be_general_for(li[i])): 
                            n1 = (li[i].tag if isinstance(li[i].tag, GeneralRelationHelper.Node) else None)
                            n2 = (li[j].tag if isinstance(li[j].tag, GeneralRelationHelper.Node) else None)
                        elif (li[j].can_be_general_for(li[i]) and not li[i].can_be_general_for(li[j])): 
                            n1 = (li[j].tag if isinstance(li[j].tag, GeneralRelationHelper.Node) else None)
                            n2 = (li[i].tag if isinstance(li[i].tag, GeneralRelationHelper.Node) else None)
                        if (n1 is not None and n2 is not None): 
                            if (n1.gen_from is None): 
                                n1.gen_from = list()
                            if (not n2 in n1.gen_from): 
                                n1.gen_from.append(n2)
                            if (n2.gen_to is None): 
                                n2.gen_to = list()
                            if (not n1 in n2.gen_to): 
                                n2.gen_to.append(n1)
                        j += 1
                    i += 1
        for n in all_refs: 
            if (n.gen_to is not None and len(n.gen_to) > 1): 
                for i in range(len(n.gen_to) - 1, -1, -1):
                    p = n.gen_to[i]
                    del0_ = False
                    j = 0
                    while j < len(n.gen_to): 
                        if (j != i and n.gen_to[j].is_in_gen_parents_or_higher(p)): 
                            del0_ = True
                        j += 1
                    if (del0_): 
                        p.gen_from.remove(n)
                        del n.gen_to[i]
        for n in all_refs: 
            if (not n.deleted and n.gen_to is not None and len(n.gen_to) == 1): 
                p = n.gen_to[0]
                if (len(p.gen_from) == 1): 
                    n.ref.merge_slots(p.ref, True)
                    p.ref.tag = n.ref
                    p.replace_values(n)
                    for o in p.ref.occurrence: 
                        n.ref.add_occurence(o)
                    p.deleted = True
                else: 
                    n.ref.general_referent = p.ref
        t = kit.first_token
        while t is not None: 
            GeneralRelationHelper.__correct_referents(t)
            t = t.next0_
        for n in all_refs: 
            if (n.deleted): 
                n.ad.remove_referent(n.ref)
            n.ref.tag = None
    
    @staticmethod
    def __correct_referents(t : 'Token') -> None:
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.Referent import Referent
        rt = (t if isinstance(t, ReferentToken) else None)
        if (rt is None): 
            return
        if (rt.referent is not None and (isinstance(rt.referent.tag, Referent))): 
            rt.referent = (rt.referent.tag if isinstance(rt.referent.tag, Referent) else None)
        tt = rt.begin_token
        while tt is not None and tt.end_char <= rt.end_char: 
            GeneralRelationHelper.__correct_referents(tt)
            tt = tt.next0_