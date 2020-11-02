# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.semantic.internal.SentItemType import SentItemType
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.TextToken import TextToken
from pullenti.semantic.internal.NGItem import NGItem
from pullenti.semantic.internal.SentItem import SentItem
from pullenti.semantic.SemanticService import SemanticService
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphCase import MorphCase
from pullenti.semantic.internal.NGLinkType import NGLinkType
from pullenti.semantic.internal.NGLink import NGLink

class NGSegmentVariant(object):
    
    def __init__(self) -> None:
        self.coef = 0
        self.source = None;
        self.links = list()
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0} = ".format(self.coef), end="", file=res, flush=True)
        for it in self.links: 
            if (it != self.links[0]): 
                print("; \r\n", end="", file=res)
            if (it is None): 
                print("<null>", end="", file=res)
            else: 
                print(str(it), end="", file=res)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def __compare_list_item_tails(mt1 : 'MetaToken', mt2 : 'MetaToken') -> bool:
        t1 = Utils.asObjectOrNull(mt1.end_token, TextToken)
        t2 = Utils.asObjectOrNull(mt2.end_token, TextToken)
        if (t1 is None or t2 is None): 
            return True
        k = 0
        i1 = len(t1.term) - 1
        i2 = len(t2.term) - 1
        while i1 > 0 and i2 > 0: 
            if (t1.term[i1] != t2.term[i2]): 
                break
            i1 -= 1; i2 -= 1; k += 1
        if (k >= 2): 
            return True
        nn = t2.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
        if (t1.is_value(nn, None)): 
            return True
        if (((t1.morph.number) & (t2.morph.number)) == (MorphNumber.UNDEFINED)): 
            return False
        if (((t1.morph.case_) & t2.morph.case_).is_undefined): 
            return False
        if (t1.morph.class0_.is_verb != t2.morph.class0_.is_verb and t1.morph.class0_.is_adjective != t2.morph.class0_.is_adjective): 
            return False
        return True
    
    def calc_coef(self) -> float:
        self.coef = (0)
        for it in self.links: 
            if (it is not None): 
                self.coef += it.coef
        i = 0
        first_pass3936 = True
        while True:
            if first_pass3936: first_pass3936 = False
            else: i += 1
            if (not (i < len(self.links))): break
            li1 = self.links[i]
            if (li1 is None or li1.to is None): 
                continue
            if (li1.reverce): 
                continue
            i0 = li1.to.order
            if (i0 >= li1.from0_.order): 
                self.coef = -1
                return self.coef
            k = i0 + 1
            first_pass3937 = True
            while True:
                if first_pass3937: first_pass3937 = False
                else: k += 1
                if (not (k < i)): break
                li = self.links[k]
                if (li is None): 
                    continue
                if (li.to_verb is not None): 
                    self.coef = -1
                    return self.coef
                i1 = li.to.order
                if ((i1 < i0) or i1 > i): 
                    self.coef = -1
                    return self.coef
                if (li.typ == NGLinkType.LIST and li1.typ == NGLinkType.LIST and i0 == i1): 
                    self.coef = -1
                    return self.coef
        i = 0
        first_pass3938 = True
        while True:
            if first_pass3938: first_pass3938 = False
            else: i += 1
            if (not (i < len(self.links))): break
            list0_ = self.get_list(i)
            if (list0_ is None): 
                continue
            k = 1
            while k < (len(list0_) - 1): 
                if (list0_[k].and_before): 
                    break
                k += 1
            if (k >= (len(list0_) - 1) and list0_[k].and_before): 
                self.coef += SemanticService.PARAMS.list0_
            else: 
                ors = 0
                ands = 0
                k = 1
                while k < len(list0_): 
                    if (list0_[k].or_before): 
                        ors += 1
                    elif (list0_[k].and_before): 
                        ands += 1
                    k += 1
                if (ands > 0 and ors > 0): 
                    self.coef = -1
                    return self.coef
                k = 1
                while k < len(list0_): 
                    if (not list0_[k].and_before): 
                        break
                    k += 1
                if (k >= len(list0_)): 
                    pass
                else: 
                    self.coef = -1
                    return self.coef
            ngli = NGLink._new2926(NGLinkType.LIST)
            k = 0
            while k < (len(list0_) - 2): 
                kk = k + 2
                while kk < len(list0_): 
                    ngli.from0_ = list0_[kk]
                    ngli.to = list0_[k]
                    ngli.calc_coef(False)
                    if (ngli.coef < 0): 
                        self.coef = -1
                        return self.coef
                    kk += 1
                k += 1
            prep_is_not_exi_all = False
            k = 0
            while k < (len(list0_) - 1): 
                kk = k + 1
                while kk < len(list0_): 
                    if (not NGSegmentVariant.__compare_list_item_tails(list0_[k].source.source, list0_[kk].source.source)): 
                        self.coef /= (2)
                    if (Utils.isNullOrEmpty(list0_[k].source.prep) != Utils.isNullOrEmpty(list0_[kk].source.prep)): 
                        str1 = list0_[k].source.end_token.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                        str2 = list0_[kk].source.end_token.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                        if (str1 != str2): 
                            prep_is_not_exi_all = True
                    kk += 1
                k += 1
            if (prep_is_not_exi_all): 
                self.coef /= (2)
            last = list0_[len(list0_) - 1]
            ok = True
            lalink = None
            for ll in self.links: 
                if (ll is not None and ll.typ == NGLinkType.GENETIVE): 
                    if (ll.to == last): 
                        lalink = ll
                    elif (ll.to in list0_): 
                        ok = False
                        break
            if (not ok or lalink is None): 
                continue
            test = NGLink._new2927(lalink.from0_, lalink.typ)
            j = 0
            while j < (len(list0_) - 1): 
                test.to = list0_[j]
                ord0_ = test.to.order
                test.to.order = last.order
                test.calc_coef(False)
                test.to.order = ord0_
                if (test.coef < 0): 
                    break
                j += 1
            if (j >= (len(list0_) - 1)): 
                lalink.to_all_list_items = True
        bef_ag = 0
        bef_pac = 0
        aft_ag = 0
        aft_pac = 0
        i = 0
        first_pass3939 = True
        while True:
            if first_pass3939: first_pass3939 = False
            else: i += 1
            if (not (i < len(self.links))): break
            li = self.links[i]
            if (li is None): 
                continue
            if (li.typ == NGLinkType.LIST): 
                continue
            if (li.typ == NGLinkType.PARTICIPLE): 
                if (li.from0_.source.part_verb_typ != NGLinkType.UNDEFINED): 
                    pass
            if ((li.typ == NGLinkType.AGENT or li.typ == NGLinkType.PACIENT or li.typ == NGLinkType.GENETIVE) or li.typ == NGLinkType.PARTICIPLE): 
                if (li.plural == 1): 
                    ok = False
                    if (li.typ == NGLinkType.PARTICIPLE and li.to is not None and self.get_list(li.to.order) is not None): 
                        ok = True
                    elif (li.typ != NGLinkType.PARTICIPLE and self.get_list(i) is not None): 
                        ok = True
                    else: 
                        co = li.coef
                        li.calc_coef(True)
                        if (li.coef > 0): 
                            ok = True
                        li.coef = co
                        li.plural = 1
                    if (not ok): 
                        self.coef = -1
                        return self.coef
                elif (li.plural == 0): 
                    if (li.typ != NGLinkType.PARTICIPLE and self.get_list(i) is not None): 
                        self.coef = -1
                        return self.coef
                    if (li.typ == NGLinkType.PARTICIPLE and li.to is not None and self.get_list(li.to.order) is not None): 
                        self.coef = -1
                        return self.coef
            if (li.typ == NGLinkType.AGENT or li.typ == NGLinkType.PACIENT or li.typ == NGLinkType.ACTANT): 
                pass
            else: 
                continue
            if (li.to_verb is not None and li.to_verb == self.source.before_verb): 
                if (self.source.after_verb is not None and not self.source.before_verb.first_verb.is_participle): 
                    has_delim = False
                    ind = li.from0_.order
                    list0_ = self.get_list(ind)
                    if (list0_ is not None): 
                        ind = list0_[len(list0_) - 1].order
                    ii = ind
                    while ii < len(self.source.items): 
                        if (self.source.items[ii].and_after or self.source.items[ii].comma_after): 
                            has_delim = True
                        ii += 1
                    if (not has_delim): 
                        self.coef = -1
                        return self.coef
                if (li.typ == NGLinkType.AGENT and li.to_verb.first_verb.is_dee_participle): 
                    has_delim = False
                    ii = 0
                    while ii <= li.from0_.order: 
                        if (self.source.items[ii].and_before or self.source.items[ii].comma_before): 
                            has_delim = True
                        ii += 1
                    if (not has_delim): 
                        self.coef = -1
                        return self.coef
                if (li.typ == NGLinkType.AGENT): 
                    bef_ag += 1
                elif (li.typ == NGLinkType.PACIENT): 
                    bef_pac += 1
                if (li.from0_.source.sub_sent is not None): 
                    continue
            elif (li.to_verb is not None and li.to_verb == self.source.after_verb): 
                if (self.source.before_verb is not None and not self.source.before_verb.first_verb.is_participle): 
                    has_delim = False
                    ii = 0
                    while ii <= li.from0_.order: 
                        if (self.source.items[ii].and_before or self.source.items[ii].comma_before): 
                            has_delim = True
                        ii += 1
                    if (not has_delim): 
                        self.coef = -1
                        return self.coef
                if (li.from0_.source.sub_sent is not None): 
                    continue
                if (li.typ == NGLinkType.AGENT): 
                    aft_ag += 1
                elif (li.typ == NGLinkType.PACIENT): 
                    aft_pac += 1
            if (li.typ == NGLinkType.ACTANT): 
                continue
        if ((bef_ag > 1 or bef_pac > 1 or aft_ag > 1) or aft_pac > 1): 
            self.coef = -1
            return self.coef
        i = 0
        first_pass3940 = True
        while True:
            if first_pass3940: first_pass3940 = False
            else: i += 1
            if (not (i < len(self.links))): break
            li = self.links[i]
            if (li is None): 
                continue
            if (li.typ != NGLinkType.ACTANT or li.to_verb is None): 
                continue
        i = 0
        first_pass3941 = True
        while True:
            if first_pass3941: first_pass3941 = False
            else: i += 1
            if (not (i < len(self.links))): break
            li = self.links[i]
            if (li is None): 
                continue
            if (li.typ != NGLinkType.GENETIVE or li.to is None): 
                continue
            if (li.from0_.source.typ == SentItemType.FORMULA): 
                for li0 in self.links: 
                    if ((li0 is not None and li0 != li and li0.typ == NGLinkType.GENETIVE) and li0.from0_ == li.to): 
                        self.coef /= (2)
            if (li.to.source.typ == SentItemType.FORMULA): 
                for li0 in self.links: 
                    if ((li0 is not None and li0 != li and li0.typ == NGLinkType.GENETIVE) and li0.to == li.to): 
                        if (li0.from0_.order < li.from0_.order): 
                            self.coef /= (2)
        return self.coef
    
    def compareTo(self, other : 'NGSegmentVariant') -> int:
        if (self.coef > other.coef): 
            return -1
        if (self.coef < other.coef): 
            return 1
        return 0
    
    def get_list_by_last_item(self, it : 'NGItem') -> typing.List['NGItem']:
        res = list()
        res.append(it)
        for i in range(len(self.links) - 1, -1, -1):
            if ((self.links[i] is not None and self.links[i].from0_ == it and self.links[i].typ == NGLinkType.LIST) and self.links[i].to is not None): 
                it = self.links[i].to
                res.insert(0, it)
        if (len(res) > 1): 
            return res
        return None
    
    def get_list(self, ord0_ : int) -> typing.List['NGItem']:
        if (ord0_ >= len(self.source.items)): 
            return None
        li = self.links[ord0_]
        if (li is None): 
            return None
        res = None
        ngit = self.source.items[ord0_]
        if (li.typ == NGLinkType.LIST): 
            if (li.to_verb is None): 
                return None
            res = list()
            res.append(NGItem._new2928(SentItem(li.to_verb), ord0_ - 1))
            res.append(ngit)
        i = ord0_ + 1
        first_pass3942 = True
        while True:
            if first_pass3942: first_pass3942 = False
            else: i += 1
            if (not (i < len(self.links))): break
            li = self.links[i]
            if (li is None or li.typ != NGLinkType.LIST or li.to is None): 
                continue
            if (li.to == ngit): 
                if (res is None): 
                    res = list()
                    res.append(ngit)
                ngit = self.source.items[i]
                res.append(ngit)
        return res
    
    def correct_morph(self) -> None:
        i = 0
        first_pass3943 = True
        while True:
            if first_pass3943: first_pass3943 = False
            else: i += 1
            if (not (i < len(self.links))): break
            li = self.links[i]
            if (li is None): 
                continue
            if (li.typ == NGLinkType.AGENT or li.typ == NGLinkType.PACIENT): 
                if (li.plural == 1): 
                    list0_ = self.get_list(i)
                    if (list0_ is not None): 
                        continue
                    li.from0_.source.plural = 1
    
    @staticmethod
    def _new2925(_arg1 : 'NGSegment') -> 'NGSegmentVariant':
        res = NGSegmentVariant()
        res.source = _arg1
        return res