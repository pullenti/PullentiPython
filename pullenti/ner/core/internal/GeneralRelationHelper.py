﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.Referent import Referent

class GeneralRelationHelper:
    
    class Node:
        
        def __init__(self) -> None:
            self.ref = None;
            self.ad = None;
            self.refs_to = None;
            self.refs_from = None;
            self.gen_to = None;
            self.gen_from = None;
            self.deleted = False
        
        def __str__(self) -> str:
            return str(self.ref)
        
        def isInGenParentsOrHigher(self, n : 'Node') -> bool:
            if (self.gen_to is None): 
                return False
            for p in self.gen_to: 
                if (p == n): 
                    return True
                elif (p.isInGenParentsOrHigher(n)): 
                    return True
            return False
        
        def replaceValues(self, new_node : 'Node') -> None:
            if (self.refs_from is not None): 
                for fr in self.refs_from: 
                    ch = False
                    for s in fr.ref.slots: 
                        if (s.value == self.ref): 
                            fr.ref.uploadSlot(s, new_node.ref)
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
        def _new484(_arg1 : 'Referent', _arg2 : 'AnalyzerData') -> 'Node':
            res = GeneralRelationHelper.Node()
            res.ref = _arg1
            res.ad = _arg2
            return res
    
    @staticmethod
    def refreshGenerals(proc : 'Processor', kit : 'AnalysisKit') -> None:
        all0_ = dict()
        all_refs = list()
        for a in proc.analyzers: 
            ad = kit.getAnalyzerData(a)
            if (ad is None): 
                continue
            for r in ad.referents: 
                nod = GeneralRelationHelper.Node._new484(r, ad)
                all_refs.append(nod)
                r.tag = nod
                wrapsi487 = RefOutArgWrapper(None)
                inoutres488 = Utils.tryGetValue(all0_, a.name, wrapsi487)
                si = wrapsi487.value
                if (not inoutres488): 
                    si = dict()
                    all0_[a.name] = si
                strs = r.getCompareStrings()
                if (strs is None or len(strs) == 0): 
                    continue
                for s in strs: 
                    li = [ ]
                    wrapli485 = RefOutArgWrapper(None)
                    inoutres486 = Utils.tryGetValue(si, s, wrapli485)
                    li = wrapli485.value
                    if (not inoutres486): 
                        li = list()
                        si[s] = li
                    li.append(r)
        for r in all_refs: 
            for s in r.ref.slots: 
                if (isinstance(s.value, Referent)): 
                    to = Utils.asObjectOrNull(s.value, Referent)
                    tn = Utils.asObjectOrNull(to.tag, GeneralRelationHelper.Node)
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
                if (len(li) > 3000): 
                    continue
                i = 0
                while i < len(li): 
                    j = i + 1
                    while j < len(li): 
                        n1 = None
                        n2 = None
                        if (li[i].canBeGeneralFor(li[j]) and not li[j].canBeGeneralFor(li[i])): 
                            n1 = (Utils.asObjectOrNull(li[i].tag, GeneralRelationHelper.Node))
                            n2 = (Utils.asObjectOrNull(li[j].tag, GeneralRelationHelper.Node))
                        elif (li[j].canBeGeneralFor(li[i]) and not li[i].canBeGeneralFor(li[j])): 
                            n1 = (Utils.asObjectOrNull(li[j].tag, GeneralRelationHelper.Node))
                            n2 = (Utils.asObjectOrNull(li[i].tag, GeneralRelationHelper.Node))
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
                        if (j != i and n.gen_to[j].isInGenParentsOrHigher(p)): 
                            del0_ = True
                        j += 1
                    if (del0_): 
                        p.gen_from.remove(n)
                        del n.gen_to[i]
        for n in all_refs: 
            if (not n.deleted and n.gen_to is not None and len(n.gen_to) == 1): 
                p = n.gen_to[0]
                if (len(p.gen_from) == 1): 
                    n.ref.mergeSlots(p.ref, True)
                    p.ref.tag = n.ref
                    p.replaceValues(n)
                    for o in p.ref.occurrence: 
                        n.ref.addOccurence(o)
                    p.deleted = True
                else: 
                    n.ref.general_referent = p.ref
        t = kit.first_token
        while t is not None: 
            GeneralRelationHelper.__correctReferents(t)
            t = t.next0_
        for n in all_refs: 
            if (n.deleted): 
                n.ad.removeReferent(n.ref)
            n.ref.tag = None
    
    @staticmethod
    def __correctReferents(t : 'Token') -> None:
        rt = Utils.asObjectOrNull(t, ReferentToken)
        if (rt is None): 
            return
        if (rt.referent is not None and (isinstance(rt.referent.tag, Referent))): 
            rt.referent = (Utils.asObjectOrNull(rt.referent.tag, Referent))
        tt = rt.begin_token
        while tt is not None and tt.end_char <= rt.end_char: 
            GeneralRelationHelper.__correctReferents(tt)
            tt = tt.next0_