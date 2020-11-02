# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender
from pullenti.semantic.SemObjectType import SemObjectType
from pullenti.semantic.SemLinkType import SemLinkType

class AnaforHelper:
    
    class AnaforLink(object):
        
        def __init__(self) -> None:
            self.coef = 0
            self.target = None;
            self.target_list = None
        
        def __str__(self) -> str:
            if (self.target_list is None): 
                return "{0}: {1}".format(self.coef, self.target)
            tmp = io.StringIO()
            print("{0}: ".format(self.coef), end="", file=tmp, flush=True)
            for v in self.target_list: 
                print("{0}; ".format(v), end="", file=tmp, flush=True)
            return Utils.toStringStringIO(tmp)
        
        @staticmethod
        def try_create(src : 'SemObject', tgt : 'SemObject') -> 'AnaforLink':
            from pullenti.morph.MorphGender import MorphGender
            from pullenti.morph.MorphNumber import MorphNumber
            from pullenti.semantic.SemObjectType import SemObjectType
            if (tgt.typ != SemObjectType.NOUN): 
                return None
            if (((src.morph.number) & (MorphNumber.PLURAL)) == (MorphNumber.PLURAL)): 
                if (((tgt.morph.number) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                    return AnaforHelper.AnaforLink._new2902(1, tgt)
                res = AnaforHelper.AnaforLink._new2902(0.5, tgt)
                res.target_list = list()
                for li in tgt.links_to: 
                    frm = li.source
                    i = 0
                    first_pass3929 = True
                    while True:
                        if first_pass3929: first_pass3929 = False
                        else: i += 1
                        if (not (i < len(frm.links_from))): break
                        res.target_list.clear()
                        li0 = frm.links_from[i]
                        if (li0.target.typ != SemObjectType.NOUN): 
                            continue
                        res.target_list.append(li0.target)
                        j = i + 1
                        while j < len(frm.links_from): 
                            li1 = frm.links_from[j]
                            if (li1.typ == li0.typ and li1.preposition == li0.preposition and li1.target.typ == li0.target.typ): 
                                res.target_list.append(li1.target)
                            j += 1
                        if (len(res.target_list) > 1): 
                            return res
                return None
            if (tgt.morph.number != MorphNumber.UNDEFINED and ((tgt.morph.number) & (MorphNumber.SINGULAR)) == (MorphNumber.UNDEFINED)): 
                return None
            if (tgt.morph.gender != MorphGender.UNDEFINED): 
                if (((tgt.morph.gender) & (src.morph.gender)) == (MorphGender.UNDEFINED)): 
                    return None
                return AnaforHelper.AnaforLink._new2902(1, tgt)
            return AnaforHelper.AnaforLink._new2902(0.1, tgt)
        
        @staticmethod
        def sort(li : typing.List['AnaforLink']) -> None:
            i = 0
            while i < len(li): 
                ch = False
                j = 0
                while j < (len(li) - 1): 
                    if (li[j].compareTo(li[j + 1]) > 0): 
                        a = li[j]
                        li[j] = li[j + 1]
                        li[j + 1] = a
                        ch = True
                    j += 1
                if (not ch): 
                    break
                i += 1
        
        def correct(self) -> None:
            from pullenti.semantic.SemLinkType import SemLinkType
            for li in self.target.links_to: 
                if (li.typ == SemLinkType.NAMING): 
                    self.coef = (0)
                elif (li.typ == SemLinkType.AGENT): 
                    self.coef *= (2)
                elif (li.typ == SemLinkType.PACIENT): 
                    if (li.alt_link is None): 
                        self.coef *= (2)
                elif (not Utils.isNullOrEmpty(li.preposition)): 
                    self.coef /= (2)
        
        def compareTo(self, other : 'AnaforLink') -> int:
            if (self.coef > other.coef): 
                return -1
            if (self.coef < other.coef): 
                return 1
            return 0
        
        @staticmethod
        def _new2902(_arg1 : float, _arg2 : 'SemObject') -> 'AnaforLink':
            res = AnaforHelper.AnaforLink()
            res.coef = _arg1
            res.target = _arg2
            return res
    
    @staticmethod
    def process_anafors(objs : typing.List['SemObject']) -> bool:
        for i in range(len(objs) - 1, -1, -1):
            it = objs[i]
            if (it.typ == SemObjectType.PERSONALPRONOUN): 
                pass
            elif (it.morph.normal_full == "КОТОРЫЙ" and len(it.links_from) == 0): 
                pass
            else: 
                continue
            vars0_ = list()
            for j in range(i - 1, -1, -1):
                a = AnaforHelper.AnaforLink.try_create(it, objs[j])
                if (a is None): 
                    continue
                vars0_.append(a)
                a.correct()
            if (len(vars0_) < 1): 
                continue
            AnaforHelper.AnaforLink.sort(vars0_)
            if (vars0_[0].coef <= 0.1): 
                continue
            if (vars0_[0].target_list is not None): 
                for tgt in vars0_[0].target_list: 
                    it.graph.add_link(SemLinkType.ANAFOR, it, tgt, None, False, None)
            else: 
                li = it.graph.add_link(SemLinkType.ANAFOR, it, vars0_[0].target, None, False, None)
                if (len(vars0_) > 1 and vars0_[0].coef <= (vars0_[1].coef * (2)) and vars0_[1].target_list is None): 
                    li1 = it.graph.add_link(SemLinkType.ANAFOR, it, vars0_[1].target, None, False, None)
                    li1.alt_link = li
                    li.alt_link = li1
        return False