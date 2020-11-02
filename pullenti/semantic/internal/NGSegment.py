# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ConjunctionType import ConjunctionType
from pullenti.semantic.internal.NGLinkType import NGLinkType
from pullenti.semantic.internal.NGLink import NGLink
from pullenti.ner.core.ConjunctionToken import ConjunctionToken
from pullenti.semantic.internal.SentItemType import SentItemType
from pullenti.semantic.internal.NGItem import NGItem
from pullenti.ner.core.VerbPhraseToken import VerbPhraseToken
from pullenti.semantic.internal.NGSegmentVariant import NGSegmentVariant

class NGSegment:
    
    def __init__(self) -> None:
        self.before_verb = None;
        self.items = list()
        self.after_verb = None;
        self.variants = list()
        self.ind = 0
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.before_verb is not None): 
            print("<{0}>: ".format(str(self.before_verb)), end="", file=tmp, flush=True)
        for it in self.items: 
            if (it != self.items[0]): 
                print("; \r\n", end="", file=tmp)
            print(str(it), end="", file=tmp)
        if (self.after_verb is not None): 
            print(" :<{0}>".format(str(self.after_verb)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def create_segments(s : 'Sentence') -> typing.List['NGSegment']:
        res = list()
        i = 0
        first_pass3932 = True
        while True:
            if first_pass3932: first_pass3932 = False
            else: i += 1
            if (not (i < len(s.items))): break
            it = s.items[i]
            if (it.typ == SentItemType.VERB or it.typ == SentItemType.DELIM): 
                continue
            seg = NGSegment()
            nit = NGItem._new2922(it)
            for j in range(i - 1, -1, -1):
                it = s.items[j]
                if (it.typ == SentItemType.VERB): 
                    seg.before_verb = (Utils.asObjectOrNull(it.source, VerbPhraseToken))
                    break
                if (it.typ == SentItemType.DELIM): 
                    break
                if (it.can_be_comma_end): 
                    if (it.source.typ == ConjunctionType.COMMA): 
                        nit.comma_before = True
                    else: 
                        nit.and_before = True
                        if (it.source.typ == ConjunctionType.OR): 
                            nit.or_before = True
                if (it.typ == SentItemType.CONJ or it.can_be_noun): 
                    break
            comma = False
            and0_ = False
            or0_ = False
            first_pass3933 = True
            while True:
                if first_pass3933: first_pass3933 = False
                else: i += 1
                if (not (i < len(s.items))): break
                it = s.items[i]
                if (it.can_be_comma_end): 
                    comma = False
                    and0_ = False
                    or0_ = False
                    if (it.source.typ == ConjunctionType.COMMA): 
                        comma = True
                    else: 
                        and0_ = True
                        if (it.source.typ == ConjunctionType.OR): 
                            or0_ = True
                    if (len(seg.items) > 0): 
                        if (comma): 
                            seg.items[len(seg.items) - 1].comma_after = True
                        else: 
                            seg.items[len(seg.items) - 1].and_after = True
                            if (or0_): 
                                seg.items[len(seg.items) - 1].or_after = True
                    continue
                if (it.can_be_noun or it.typ == SentItemType.ADVERB): 
                    nit = NGItem._new2923(it, comma, and0_, or0_)
                    seg.items.append(nit)
                    comma = False
                    and0_ = False
                    or0_ = False
                elif (it.typ == SentItemType.VERB or it.typ == SentItemType.CONJ or it.typ == SentItemType.DELIM): 
                    break
            j = i
            while j < len(s.items): 
                it = s.items[j]
                if (it.typ == SentItemType.VERB): 
                    seg.after_verb = (Utils.asObjectOrNull(it.source, VerbPhraseToken))
                    break
                if ((it.typ == SentItemType.CONJ or it.can_be_noun or it.typ == SentItemType.DELIM) or it.typ == SentItemType.ADVERB): 
                    break
                j += 1
            res.append(seg)
        for ss in res: 
            ss.create_links(False)
        return res
    
    def create_links(self, after_part : bool=False) -> None:
        """ А это создание вариантов связей между элементами """
        i = 0
        while i < len(self.items): 
            self.items[i].order = i
            self.items[i].prepare()
            i += 1
        li = None
        i = 0
        first_pass3934 = True
        while True:
            if first_pass3934: first_pass3934 = False
            else: i += 1
            if (not (i < len(self.items))): break
            it = self.items[i]
            if (it.source.typ == SentItemType.ADVERB): 
                continue
            ignore_before = False
            mult = 1
            if (it.comma_before or it.and_before): 
                for j in range(i - 1, -1, -1):
                    if (li is None): 
                        li = NGLink()
                    li.typ = NGLinkType.LIST
                    li.from0_ = it
                    li.to = self.items[j]
                    li.to_verb = (None)
                    li.calc_coef(False)
                    if (li.coef >= 0): 
                        it.links.append(li)
                        li = (None)
                    if (it.source.typ == SentItemType.PARTBEFORE or it.source.typ == SentItemType.SUBSENT or it.source.typ == SentItemType.DEEPART): 
                        if (it.comma_before): 
                            if (li is None): 
                                li = NGLink()
                            li.typ = NGLinkType.PARTICIPLE
                            li.from0_ = it
                            li.to = self.items[j]
                            li.to_verb = (None)
                            li.calc_coef(False)
                            if (li.coef >= 0): 
                                it.links.append(li)
                                li = (None)
                    if ((not it.and_before and it.source.typ == SentItemType.NOUN and self.items[j].source.typ == SentItemType.NOUN) and self.items[i - 1].source.typ == SentItemType.PARTBEFORE): 
                        ok = True
                        jj = j + 1
                        while jj < i: 
                            if ((self.items[jj].source.typ == SentItemType.DELIM or self.items[jj].source.typ == SentItemType.NOUN or self.items[jj].source.typ == SentItemType.SUBSENT) or self.items[jj].source.typ == SentItemType.PARTBEFORE): 
                                pass
                            else: 
                                ok = False
                                break
                            jj += 1
                        if (ok): 
                            if (li is None): 
                                li = NGLink()
                            li.typ = NGLinkType.GENETIVE
                            li.from0_ = it
                            li.to = self.items[j]
                            li.to_verb = (None)
                            li.calc_coef(False)
                            if (li.coef >= 0): 
                                it.links.append(li)
                                li = (None)
                ignore_before = True
            else: 
                for j in range(i - 1, -1, -1):
                    if (self.items[j].source.typ == SentItemType.SUBSENT): 
                        continue
                    if (li is None): 
                        li = NGLink()
                    li.typ = NGLinkType.GENETIVE
                    li.from0_ = it
                    li.to = self.items[j]
                    li.to_verb = (None)
                    li.calc_coef(False)
                    if (li.coef >= 0): 
                        it.links.append(li)
                        li = (None)
                    if (li is None): 
                        li = NGLink()
                    li.typ = NGLinkType.NAME
                    li.from0_ = it
                    li.to = self.items[j]
                    li.to_verb = (None)
                    li.calc_coef(False)
                    if (li.coef >= 0): 
                        it.links.append(li)
                        li = (None)
                    nodelim = True
                    jj = j + 1
                    while jj <= i: 
                        if (self.items[jj].comma_before or self.items[jj].and_before): 
                            nodelim = False
                            break
                        jj += 1
                    if (nodelim): 
                        if (li is None): 
                            li = NGLink()
                        li.typ = NGLinkType.BE
                        li.from0_ = it
                        li.to = self.items[j]
                        li.to_verb = (None)
                        li.calc_coef(False)
                        if (li.coef >= 0): 
                            it.links.append(li)
                            li = (None)
                    if (it.source.typ == SentItemType.PARTBEFORE or it.source.typ == SentItemType.SUBSENT or it.source.typ == SentItemType.DEEPART): 
                        has_delim = False
                        for jj in range(i - 1, j, -1):
                            if (self.items[jj].source.can_be_comma_end): 
                                has_delim = True
                                break
                        if (has_delim): 
                            if (li is None): 
                                li = NGLink()
                            li.typ = NGLinkType.PARTICIPLE
                            li.from0_ = it
                            li.to = self.items[j]
                            li.to_verb = (None)
                            li.calc_coef(False)
                            if (li.coef >= 0): 
                                it.links.append(li)
                                li = (None)
                    if (self.items[j].source.typ == SentItemType.PARTBEFORE): 
                        mult *= 0.5
                    if (self.items[j].source.typ == SentItemType.VERB): 
                        ignore_before = True
                        break
                if (self.before_verb is not None and not ignore_before and it.source.typ != SentItemType.DEEPART): 
                    ok = False
                    if (li is None): 
                        li = NGLink()
                    li.typ = NGLinkType.AGENT
                    li.from0_ = it
                    li.to = (None)
                    li.to_verb = self.before_verb
                    li.calc_coef(False)
                    li.coef *= mult
                    if (li.coef >= 0): 
                        it.links.append(li)
                        ok = True
                        li = (None)
                    if (li is None): 
                        li = NGLink()
                    li.typ = NGLinkType.PACIENT
                    li.from0_ = it
                    li.to = (None)
                    li.to_verb = self.before_verb
                    li.calc_coef(False)
                    li.coef *= mult
                    if (li.coef >= 0): 
                        it.links.append(li)
                        ok = True
                        li = (None)
                    if (li is None): 
                        li = NGLink()
                    li.typ = NGLinkType.ACTANT
                    li.from0_ = it
                    li.to = (None)
                    li.to_verb = self.before_verb
                    li.calc_coef(False)
                    li.coef *= mult
                    if (ok): 
                        li.coef /= (2)
                    if (li.coef >= 0): 
                        it.links.append(li)
                        ok = True
                        li = (None)
            if (self.after_verb is not None and it.source.typ != SentItemType.DEEPART): 
                ok = False
                if (after_part and self.before_verb is not None): 
                    for l_ in it.links: 
                        if (l_.to_verb == self.before_verb and ((l_.typ == NGLinkType.AGENT or l_.typ == NGLinkType.PACIENT))): 
                            ok = True
                    if (ok): 
                        continue
                if (li is None): 
                    li = NGLink()
                li.typ = NGLinkType.AGENT
                li.from0_ = it
                li.to = (None)
                li.to_verb = self.after_verb
                li.calc_coef(False)
                if (li.coef >= 0): 
                    it.links.append(li)
                    ok = True
                    li = (None)
                if (li is None): 
                    li = NGLink()
                li.typ = NGLinkType.PACIENT
                li.from0_ = it
                li.to = (None)
                li.to_verb = self.after_verb
                li.calc_coef(False)
                if (li.coef >= 0): 
                    it.links.append(li)
                    ok = True
                    li = (None)
                if (li is None): 
                    li = NGLink()
                li.typ = NGLinkType.ACTANT
                li.from0_ = it
                li.to = (None)
                li.to_verb = self.after_verb
                li.calc_coef(False)
                if (li.coef >= 0): 
                    it.links.append(li)
                    ok = True
                    li = (None)
        i = 1
        first_pass3935 = True
        while True:
            if first_pass3935: first_pass3935 = False
            else: i += 1
            if (not (i < len(self.items))): break
            it = self.items[i]
            if (it.source.typ != SentItemType.NOUN): 
                continue
            it0 = self.items[i - 1]
            if (it0.source.typ != SentItemType.NOUN): 
                continue
            if (len(it0.links) > 0): 
                continue
            li = NGLink._new2924(NGLinkType.GENETIVE, it0, it, True)
            li.calc_coef(True)
            if (li.coef > 0): 
                it0.links.append(li)
    
    def create_variants(self, max_count : int=5) -> None:
        self.variants.clear()
        i = 0
        while i < len(self.items): 
            self.items[i].ind = 0
            i += 1
        var = None
        for kkk in range(1000):
            if (var is None): 
                var = NGSegmentVariant._new2925(self)
            else: 
                var.links.clear()
            i = 0
            while i < len(self.items): 
                it = self.items[i]
                if (it.ind < len(it.links)): 
                    var.links.append(it.links[it.ind])
                else: 
                    var.links.append(None)
                i += 1
            var.calc_coef()
            if (var.coef >= 0): 
                self.variants.append(var)
                var = (None)
                if (len(self.variants) > (max_count * 5)): 
                    NGSegment.__sort_vars(self.variants)
                    del self.variants[max_count:max_count+len(self.variants) - max_count]
            for j in range(len(self.items) - 1, -1, -1):
                it = self.items[j]
                it.ind += 1
                if (it.ind >= len(it.links)): 
                    it.ind = 0
                else: 
                    break
            else: j = -1
            if (j < 0): 
                break
        NGSegment.__sort_vars(self.variants)
        if (len(self.variants) > max_count): 
            del self.variants[max_count:max_count+len(self.variants) - max_count]
    
    @staticmethod
    def __sort_vars(vars0_ : typing.List['NGSegmentVariant']) -> None:
        i = 0
        while i < len(vars0_): 
            j = 0
            while j < (len(vars0_) - 1): 
                if (vars0_[j].compareTo(vars0_[j + 1]) > 0): 
                    v = vars0_[j]
                    vars0_[j] = vars0_[j + 1]
                    vars0_[j + 1] = v
                j += 1
            i += 1