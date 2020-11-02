# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.semantic.internal.NGItem import NGItem
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.semantic.SemAttributeType import SemAttributeType
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.semantic.internal.AdverbToken import AdverbToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.semantic.SemFraglinkType import SemFraglinkType
from pullenti.semantic.SemFragment import SemFragment
from pullenti.semantic.SemBlock import SemBlock
from pullenti.semantic.internal.SentenceVariant import SentenceVariant
from pullenti.semantic.internal.Subsent import Subsent
from pullenti.ner.core.VerbPhraseToken import VerbPhraseToken
from pullenti.semantic.internal.SentItemType import SentItemType
from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
from pullenti.semantic.SemLinkType import SemLinkType
from pullenti.semantic.internal.NGLinkType import NGLinkType
from pullenti.semantic.internal.SentItemSubtype import SentItemSubtype
from pullenti.semantic.SemObjectType import SemObjectType
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.core.NounPhraseToken import NounPhraseToken
from pullenti.semantic.SemObject import SemObject
from pullenti.semantic.internal.CreateHelper import CreateHelper
from pullenti.semantic.internal.NGLink import NGLink

class Sentence(object):
    
    def __init__(self) -> None:
        self.items = list()
        self.coef = 0
        self.best_var = None;
        self.subs = list()
        self.res_block = None;
        self.last_noun_to_first_verb = NGLinkType.UNDEFINED
        self.not_last_noun_to_first_verb = NGLinkType.UNDEFINED
        self.last_char = None;
    
    def __create_lists(self, s : 'NGSegmentVariant') -> None:
        i = 0
        first_pass3950 = True
        while True:
            if first_pass3950: first_pass3950 = False
            else: i += 1
            if (not (i < len(s.links))): break
            list0_ = s.get_list(i)
            if (list0_ is None): 
                continue
            if (list0_[0].source.result is None): 
                continue
            root = list0_[0].source
            root.result_list = list()
            for li in list0_: 
                if (li.source.result is not None): 
                    root.result_list.append(li.source.result)
                if (li != list0_[0] and li.or_before): 
                    root.result_list_or = True
    
    def __set_last_alt_links(self, fr : 'SemGraph') -> None:
        if (len(fr.links) > 1): 
            li0 = fr.links[len(fr.links) - 2]
            li1 = fr.links[len(fr.links) - 1]
            li0.alt_link = li1
            li1.alt_link = li0
    
    def __create_links(self, s : 'NGSegmentVariant') -> None:
        i = 0
        first_pass3951 = True
        while True:
            if first_pass3951: first_pass3951 = False
            else: i += 1
            if (not (i < len(s.links))): break
            link0 = s.links[i]
            if (link0 is None): 
                continue
            if (link0.typ == NGLinkType.LIST): 
                continue
            for k in range(2):
                li = link0
                if (k == 1): 
                    li = li.alt_link
                if (li is None): 
                    break
                if (li.from0_.res_object is None): 
                    continue
                if (k == 1): 
                    pass
                gr = li.from0_.res_object.graph
                if (li.to is not None and li.to.res_object is not None): 
                    link = None
                    if (li.typ == NGLinkType.PARTICIPLE and li.from0_.source.sub_typ == SentItemSubtype.WICH): 
                        link = gr.add_link(SemLinkType.ANAFOR, li.from0_.res_object, li.to.res_object, None, False, None)
                        if (k > 0): 
                            self.__set_last_alt_links(gr)
                        continue
                    if (li.typ == NGLinkType.PARTICIPLE and li.from0_.source.typ == SentItemType.PARTBEFORE): 
                        link = gr.add_link(SemLinkType.PARTICIPLE, li.to.res_object, li.from0_.res_object, "какой", False, None)
                        if (k > 0): 
                            self.__set_last_alt_links(gr)
                        if (li.from0_.source.result_list is not None and li.typ == NGLinkType.PARTICIPLE): 
                            link.is_or = li.from0_.source.result_list_or
                            ii = 1
                            while ii < len(li.from0_.source.result_list): 
                                gr.add_link(link.typ, link.source, li.from0_.source.result_list[ii], link.question, link.is_or, None)
                                ii += 1
                        continue
                    if (li.typ == NGLinkType.BE): 
                        if ((isinstance(li.from0_.source.source, NumbersWithUnitToken)) and li.to is not None): 
                            gr.add_link(SemLinkType.DETAIL, li.to.res_object, li.from0_.res_object, "какой", False, li.from_prep)
                            continue
                        be = SemObject._new2929(gr, SemObjectType.VERB)
                        be.tokens.append(li.from0_.source.source)
                        be.morph.normal_full = "БЫТЬ"
                        be.morph.normal_case = be.morph.normal_full
                        gr.objects.append(be)
                        gr.add_link(SemLinkType.AGENT, be, li.to.res_object, None, False, None)
                        gr.add_link(SemLinkType.PACIENT, be, li.from0_.res_object, None, False, None)
                        continue
                    ty = SemLinkType.UNDEFINED
                    ques = None
                    if (li.typ == NGLinkType.GENETIVE): 
                        if (li.can_be_pacient): 
                            ty = SemLinkType.PACIENT
                        else: 
                            ty = SemLinkType.DETAIL
                            ques = "чего"
                        if (not Utils.isNullOrEmpty(li.from_prep)): 
                            ques = CreateHelper.create_question(li.from0_)
                    elif (li.typ == NGLinkType.NAME): 
                        ty = SemLinkType.NAMING
                    link = gr.add_link(ty, li.to.res_object, li.from0_.res_object, ques, False, li.from_prep)
                    if (li.from0_.source.result_list is not None): 
                        link.is_or = li.from0_.source.result_list_or
                        ii = 1
                        while ii < len(li.from0_.source.result_list): 
                            link1 = gr.add_link(ty, link.source, li.from0_.source.result_list[ii], ques, link.is_or, None)
                            link1.preposition = link.preposition
                            ii += 1
                    list0_ = None
                    if (li.to_all_list_items): 
                        list0_ = s.get_list_by_last_item(li.to)
                        if (list0_ is not None): 
                            ok = True
                            j = 0
                            while j < (len(list0_) - 1): 
                                if (list0_[j].res_object is not None and len(list0_[j].res_object.links_from) > 0): 
                                    ok = False
                                    break
                                j += 1
                            if (ok): 
                                j = 0
                                while j < (len(list0_) - 1): 
                                    gr.add_link(link.typ, list0_[j].res_object, link.target, link.question, False, link.preposition)
                                    j += 1
                    if (k > 0): 
                        self.__set_last_alt_links(gr)
                if (li.to_verb is not None and li.from0_.res_object is not None): 
                    link = None
                    vitem = None
                    for iii in self.items: 
                        if (iii.source == li.to_verb): 
                            vitem = iii
                            break
                    if (li.typ == NGLinkType.AGENT and vitem is not None and vitem.result is not None): 
                        verb = vitem.result
                        if (verb.typ == SemObjectType.PARTICIPLE and li.can_be_participle): 
                            link = gr.add_link(SemLinkType.PARTICIPLE, li.from0_.res_object, verb, "какой", False, None)
                        else: 
                            link = gr.add_link(SemLinkType.AGENT, verb, li.from0_.res_object, None, False, None)
                        if (k > 0): 
                            self.__set_last_alt_links(gr)
                    elif (((li.typ == NGLinkType.PACIENT or li.typ == NGLinkType.ACTANT)) and vitem is not None and vitem.result_verb_last is not None): 
                        verb = vitem.result_verb_last
                        ques = None
                        if (li.typ == NGLinkType.ACTANT): 
                            ques = CreateHelper.create_question(li.from0_)
                        if (verb.typ == SemObjectType.PARTICIPLE and li.typ == NGLinkType.PACIENT and li.can_be_participle): 
                            link = gr.add_link(SemLinkType.PARTICIPLE, li.from0_.res_object, verb, "какой", False, None)
                        else: 
                            link = gr.add_link((SemLinkType.PACIENT if li.typ == NGLinkType.PACIENT else SemLinkType.DETAIL), verb, li.from0_.res_object, ques, False, li.from_prep)
                        if (k > 0): 
                            self.__set_last_alt_links(gr)
                    if (link is None): 
                        continue
                    if (li.from0_.source.result_list is not None): 
                        link.is_or = li.from0_.source.result_list_or
                        jj = 1
                        while jj < len(li.from0_.source.result_list): 
                            if (link.typ == SemLinkType.PARTICIPLE): 
                                gr.add_link(link.typ, li.from0_.source.result_list[jj], link.target, link.question, link.is_or, None)
                            else: 
                                gr.add_link(link.typ, link.source, li.from0_.source.result_list[jj], link.question, link.is_or, None)
                            jj += 1
    
    def __create_result(self, blk : 'SemBlock') -> None:
        if (self.best_var is not None): 
            for s in self.best_var.segs: 
                if (s is not None): 
                    s.correct_morph()
            self.best_var.create_alt_links()
        all_items = list()
        for it in self.items: 
            if (it.res_graph is None): 
                continue
            if (it.result is None): 
                if (isinstance(it.source, NounPhraseToken)): 
                    npt = Utils.asObjectOrNull(it.source, NounPhraseToken)
                    if (it.plural == 1 and ((it.source.morph.number) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                        it.source.morph.remove_items(MorphNumber.PLURAL, False)
                    it.result = CreateHelper.create_noun_group(it.res_graph, npt)
                    if (npt.multi_nouns and it.result.quantity is None): 
                        it.result_list = list()
                        it.result_list.append(it.result)
                        if (len(npt.adjectives) > 0 and ((npt.adjectives[0].begin_token.morph.number) & (MorphNumber.SINGULAR)) == (MorphNumber.SINGULAR)): 
                            it.result.morph.number = MorphNumber.SINGULAR
                            if (it.result.morph.normal_full is not None): 
                                it.result.morph.normal_case = it.result.morph.normal_full
                        i = 1
                        while i < len(npt.adjectives): 
                            so = SemObject._new2929(it.res_graph, it.result.typ)
                            so.tokens.append(npt.noun)
                            wf = MorphWordForm()
                            wf.copy_from_word_form(it.result.morph)
                            so.morph = wf
                            for a in it.result.attrs: 
                                so.attrs.append(a)
                            so.concept = it.result.concept
                            so.not0_ = it.result.not0_
                            asem = CreateHelper.create_npt_adj(it.res_graph, npt, npt.adjectives[i])
                            if (asem is not None): 
                                it.res_graph.add_link(SemLinkType.DETAIL, so, asem, "какой", False, None)
                            it.result_list.append(so)
                            it.res_graph.objects.append(so)
                            i += 1
                elif (isinstance(it.source, VerbPhraseToken)): 
                    it.result = CreateHelper.create_verb_group(it.res_graph, Utils.asObjectOrNull(it.source, VerbPhraseToken))
                    it.result_verb_last = (Utils.asObjectOrNull(it.source.last_verb.tag, SemObject))
                elif (isinstance(it.source, NumbersWithUnitToken)): 
                    it.result = CreateHelper.create_number(it.res_graph, Utils.asObjectOrNull(it.source, NumbersWithUnitToken))
                if (it.result is not None and it.quant is not None): 
                    it.result.quantity = it.quant
                if (it.result is not None and it.attrs is not None): 
                    for a in it.attrs: 
                        it.result.attrs.append(a.attr)
                        it.result.tokens.append(a.token)
            if (it.result is not None): 
                if (it.result.graph != it.res_graph): 
                    pass
                all_items.append(it)
        if (self.best_var is not None): 
            for s in self.best_var.segs: 
                if (s is not None): 
                    self.__create_lists(s)
        if (self.best_var is not None): 
            for s in self.best_var.segs: 
                if (s is not None): 
                    self.__create_links(s)
        i = 0
        first_pass3952 = True
        while True:
            if first_pass3952: first_pass3952 = False
            else: i += 1
            if (not (i < len(self.items))): break
            it = self.items[i]
            if (it.typ != SentItemType.ADVERB or it.res_graph is None): 
                continue
            adv = Utils.asObjectOrNull(it.source, AdverbToken)
            if (adv.typ != SemAttributeType.UNDEFINED): 
                continue
            before = None
            after = None
            for ii in range(i - 1, -1, -1):
                it0 = self.items[ii]
                if (it0.typ == SentItemType.VERB): 
                    before = it0
                    break
                elif (it0.typ == SentItemType.ADVERB or it0.typ == SentItemType.NOUN): 
                    pass
                else: 
                    break
            if (before is None): 
                for ii in range(i - 1, -1, -1):
                    it0 = self.items[ii]
                    if (it0.typ == SentItemType.VERB or it0.typ == SentItemType.NOUN): 
                        before = it0
                        break
                    elif (it0.typ == SentItemType.ADVERB): 
                        pass
                    else: 
                        break
            comma_after = False
            ii = i + 1
            while ii < len(self.items): 
                it0 = self.items[ii]
                if (it0.typ == SentItemType.VERB or it0.typ == SentItemType.NOUN): 
                    after = it0
                    break
                elif (it0.typ == SentItemType.ADVERB): 
                    pass
                elif (it0.can_be_comma_end): 
                    if (before is not None and before.typ == SentItemType.VERB): 
                        break
                    if (((ii + 1) < len(self.items)) and ((self.items[ii + 1].typ == SentItemType.ADVERB or self.items[ii + 1].typ == SentItemType.VERB))): 
                        pass
                    else: 
                        comma_after = True
                else: 
                    break
                ii += 1
            if (before is not None and after is not None): 
                if (comma_after): 
                    after = (None)
                elif (before.typ == SentItemType.NOUN and after.typ == SentItemType.VERB): 
                    before = (None)
                elif (before.typ == SentItemType.VERB and after.typ == SentItemType.NOUN): 
                    after = (None)
            it.result = CreateHelper.create_adverb(it.res_graph, adv)
            if (it.attrs is not None): 
                for a in it.attrs: 
                    it.result.attrs.append(a.attr)
                    it.result.tokens.append(a.token)
            if (after is not None or before is not None): 
                it.res_graph.add_link(SemLinkType.DETAIL, (before.result if after is None else after.result), it.result, "как", False, None)
        preds = list()
        agent = None
        for it in self.items: 
            if (it.result is not None and it.typ == SentItemType.VERB and (isinstance(it.source, VerbPhraseToken))): 
                if (agent is not None): 
                    has_pac = False
                    for li in it.res_graph.links: 
                        if (li.typ == SemLinkType.PACIENT and li.source == it.result): 
                            has_pac = True
                            break
                    if (not has_pac): 
                        ni0 = NGItem._new2922(agent)
                        gli0 = NGLink._new2935(ni0, Utils.asObjectOrNull(it.source, VerbPhraseToken), NGLinkType.PACIENT)
                        if (agent.result_list is not None): 
                            gli0.from_is_plural = True
                            gli0.calc_coef(False)
                            if (gli0.coef > 0 and gli0.plural == 1): 
                                for ii in agent.result_list: 
                                    it.res_graph.add_link(SemLinkType.PACIENT, it.result, ii, None, False, None)
                                self.coef += (1)
                        else: 
                            gli0.calc_coef(True)
                            if (gli0.coef > 0): 
                                it.res_graph.add_link(SemLinkType.PACIENT, it.result, agent.result, None, False, None)
                                self.coef += (1)
                ali = None
                for li in it.res_graph.links: 
                    if (li.typ == SemLinkType.AGENT and li.source == it.result): 
                        ali = li
                        break
                if (ali is not None): 
                    agent = self.__find_item_by_res(ali.target)
                    continue
                if (agent is None): 
                    continue
                ni = NGItem._new2922(agent)
                gli = NGLink._new2935(ni, Utils.asObjectOrNull(it.source, VerbPhraseToken), NGLinkType.AGENT)
                if (agent.result_list is not None): 
                    gli.from_is_plural = True
                    gli.calc_coef(False)
                    if (gli.coef > 0 and gli.plural == 1): 
                        for ii in agent.result_list: 
                            it.res_graph.add_link(SemLinkType.AGENT, it.result, ii, None, False, None)
                        self.coef += (1)
                else: 
                    gli.calc_coef(True)
                    if (gli.coef > 0): 
                        it.res_graph.add_link(SemLinkType.AGENT, it.result, agent.result, None, False, None)
                        self.coef += (1)
        agent = (None)
        i = 0
        first_pass3953 = True
        while True:
            if first_pass3953: first_pass3953 = False
            else: i += 1
            if (not (i < len(self.items))): break
            it = self.items[i]
            if (it.result is not None and it.typ == SentItemType.DEEPART): 
                pass
            else: 
                continue
            link = None
            for j in range(i - 1, -1, -1):
                itt = self.items[j]
                if (itt.typ != SentItemType.NOUN): 
                    continue
                if (not ((itt.source.morph.case_.is_nominative))): 
                    continue
                ispacad = False
                for li in itt.res_graph.links: 
                    if (((li.typ == SemLinkType.AGENT or li.typ == SemLinkType.PACIENT)) and li.target == itt.result): 
                        ispacad = True
                if (not ispacad): 
                    continue
                if (link is None): 
                    link = itt.res_graph.add_link(SemLinkType.AGENT, it.result, itt.result, None, False, None)
                elif (link.alt_link is None): 
                    link.alt_link = itt.res_graph.add_link(SemLinkType.AGENT, it.result, itt.result, None, False, None)
                    link.alt_link.alt_link = link
                    break
            if (link is None): 
                j = i + 1
                first_pass3954 = True
                while True:
                    if first_pass3954: first_pass3954 = False
                    else: j += 1
                    if (not (j < len(self.items))): break
                    itt = self.items[j]
                    if (itt.typ != SentItemType.NOUN): 
                        continue
                    if (not ((itt.source.morph.case_.is_nominative))): 
                        continue
                    ispacad = False
                    for li in itt.res_graph.links: 
                        if (((li.typ == SemLinkType.AGENT or li.typ == SemLinkType.PACIENT)) and li.target == itt.result): 
                            ispacad = True
                    if (not ispacad): 
                        continue
                    if (link is None): 
                        link = itt.res_graph.add_link(SemLinkType.AGENT, it.result, itt.result, None, False, None)
                    elif (link.alt_link is None): 
                        link.alt_link = itt.res_graph.add_link(SemLinkType.AGENT, it.result, itt.result, None, False, None)
                        link.alt_link.alt_link = link
                        break
            if (link is not None): 
                self.coef += 1
        for fr in self.res_block.fragments: 
            if (fr.can_be_error_structure): 
                self.coef /= (2)
        if (len(self.res_block.fragments) > 0 and len(self.res_block.fragments[0].graph.objects) > 0): 
            it = self.res_block.fragments[0].graph.objects[0]
            if (self.last_char is not None and self.last_char.is_char('?')): 
                if (it.morph.normal_full == "КАКОЙ" or it.morph.normal_full == "СКОЛЬКО"): 
                    it.typ = SemObjectType.QUESTION
    
    def __find_item_by_res(self, s : 'SemObject') -> 'SentItem':
        for it in self.items: 
            if (it.result == s): 
                return it
        return None
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.coef > 0): 
            print("{0}: ".format(self.coef), end="", file=res, flush=True)
        for it in self.items: 
            if (it != self.items[0]): 
                print("; \r\n", end="", file=res)
            print(str(it), end="", file=res)
        return Utils.toStringStringIO(res)
    
    def add_to_block(self, blk : 'SemBlock', gr : 'SemGraph'=None) -> None:
        if (self.res_block is not None): 
            if (gr is None): 
                blk.add_fragments(self.res_block)
            else: 
                for fr in self.res_block.fragments: 
                    gr.objects.extend(fr.graph.objects)
                    gr.links.extend(fr.graph.links)
        for it in self.items: 
            if (it.sub_sent is not None): 
                it.sub_sent.add_to_block(blk, Utils.ifNotNull(gr, it.res_frag.graph))
    
    @staticmethod
    def parse_variants(t0 : 'Token', t1 : 'Token', lev : int, max_count : int=0, regime : 'SentItemType'=SentItemType.UNDEFINED) -> typing.List['Sentence']:
        from pullenti.semantic.internal.SentItem import SentItem
        if ((t0 is None or t1 is None or t0.end_char > t1.end_char) or lev > 100): 
            return None
        res = list()
        sent = Sentence()
        t = t0
        first_pass3955 = True
        while True:
            if first_pass3955: first_pass3955 = False
            else: t = t.next0_
            if (not (t is not None and t.end_char <= t1.end_char)): break
            if (t.is_char('(')): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    t = br.end_token
                    continue
            items_ = SentItem.parse_near_items(t, t1, lev + 1, sent.items)
            if (items_ is None or len(items_) == 0): 
                continue
            if (len(items_) == 1 or ((max_count > 0 and len(res) > max_count))): 
                sent.items.append(items_[0])
                t = items_[0].end_token
                if (regime != SentItemType.UNDEFINED): 
                    it = items_[0]
                    if (it.can_be_noun): 
                        pass
                    elif (it.typ == SentItemType.DELIM): 
                        break
                    elif (it.typ == SentItemType.VERB): 
                        if (regime == SentItemType.PARTBEFORE): 
                            break
                continue
            m_nexts = dict()
            for it in items_: 
                nexts = None
                wrapnexts2938 = RefOutArgWrapper(None)
                inoutres2939 = Utils.tryGetValue(m_nexts, it.end_token.end_char, wrapnexts2938)
                nexts = wrapnexts2938.value
                if (not inoutres2939): 
                    nexts = Sentence.parse_variants(it.end_token.next0_, t1, lev + 1, max_count, SentItemType.UNDEFINED)
                    m_nexts[it.end_token.end_char] = nexts
                if (nexts is None or len(nexts) == 0): 
                    se = Sentence()
                    for itt in sent.items: 
                        itt1 = SentItem(None)
                        itt1.copy_from(itt)
                        se.items.append(itt1)
                    itt0 = SentItem(None)
                    itt0.copy_from(it)
                    se.items.append(itt0)
                    res.append(se)
                else: 
                    for sn in nexts: 
                        se = Sentence()
                        for itt in sent.items: 
                            itt1 = SentItem(None)
                            itt1.copy_from(itt)
                            se.items.append(itt1)
                        itt0 = SentItem(None)
                        itt0.copy_from(it)
                        se.items.append(itt0)
                        for itt in sn.items: 
                            itt1 = SentItem(None)
                            itt1.copy_from(itt)
                            se.items.append(itt1)
                        res.append(se)
            return res
        if (len(sent.items) == 0): 
            return None
        res.append(sent)
        return res
    
    def compareTo(self, other : 'Sentence') -> int:
        if (self.coef > other.coef): 
            return -1
        if (self.coef < other.coef): 
            return 1
        return 0
    
    def calc_coef(self, no_result : bool) -> None:
        from pullenti.semantic.internal.NGSegment import NGSegment
        self.coef = (0)
        i = 0
        first_pass3956 = True
        while True:
            if first_pass3956: first_pass3956 = False
            else: i += 1
            if (not (i < len(self.items))): break
            it = self.items[i]
            if (it.typ != SentItemType.ADVERB): 
                continue
            adv = Utils.asObjectOrNull(it.source, AdverbToken)
            if (adv.typ == SemAttributeType.UNDEFINED): 
                continue
            before = None
            after = None
            for ii in range(i - 1, -1, -1):
                it0 = self.items[ii]
                if (it0.typ == SentItemType.VERB): 
                    before = it0
                    break
                elif (it0.typ == SentItemType.ADVERB): 
                    if (it0.source.typ == SemAttributeType.UNDEFINED): 
                        before = it0
                        break
                elif (it0.can_be_comma_end): 
                    break
                elif (it0.typ == SentItemType.FORMULA and ((adv.typ == SemAttributeType.GREAT or adv.typ == SemAttributeType.LESS))): 
                    before = it0
                    break
            comma_after = False
            ii = i + 1
            while ii < len(self.items): 
                it0 = self.items[ii]
                if (it0.typ == SentItemType.VERB): 
                    after = it0
                    break
                elif (it0.typ == SentItemType.ADVERB): 
                    if (it0.source.typ == SemAttributeType.UNDEFINED): 
                        after = it0
                        break
                elif (it0.can_be_comma_end): 
                    comma_after = True
                elif (it0.typ == SentItemType.FORMULA and ((adv.typ == SemAttributeType.GREAT or adv.typ == SemAttributeType.LESS))): 
                    before = it0
                    break
                elif (it0.typ == SentItemType.NOUN): 
                    comma_after = True
                else: 
                    break
                ii += 1
            if (before is not None and after is not None): 
                if (before.typ == SentItemType.FORMULA): 
                    after = (None)
                elif (after.typ == SentItemType.FORMULA): 
                    before = (None)
                elif (comma_after): 
                    after = (None)
            if (after is not None): 
                after.add_attr(adv)
                del self.items[i]
                i -= 1
                continue
            if (before is not None): 
                before.add_attr(adv)
                del self.items[i]
                i -= 1
                continue
        segs = NGSegment.create_segments(self)
        if (self.last_noun_to_first_verb != NGLinkType.UNDEFINED or self.not_last_noun_to_first_verb != NGLinkType.UNDEFINED): 
            if (len(segs) != 1 or len(segs[0].items) == 0): 
                if (self.last_noun_to_first_verb != NGLinkType.UNDEFINED): 
                    self.coef = (-1)
                    return
            else: 
                last = segs[0].items[len(segs[0].items) - 1]
                for i in range(len(last.links) - 1, -1, -1):
                    li = last.links[i]
                    if (self.last_noun_to_first_verb != NGLinkType.UNDEFINED): 
                        if (li.typ == self.last_noun_to_first_verb and li.to_verb == segs[0].before_verb): 
                            li.can_be_participle = True
                        else: 
                            del last.links[i]
                    elif (self.not_last_noun_to_first_verb != NGLinkType.UNDEFINED): 
                        if (li.typ == self.not_last_noun_to_first_verb and li.to_verb == segs[0].before_verb): 
                            del last.links[i]
                            break
                if (len(last.links) == 0): 
                    self.coef = (-1)
                    return
        for seg in segs: 
            seg.ind = 0
            seg.create_variants(100)
        svars = list()
        svar = None
        for kkk in range(1000):
            if (svar is None): 
                svar = SentenceVariant()
            else: 
                svar.segs.clear()
            i = 0
            while i < len(segs): 
                it = segs[i]
                if (it.ind < len(it.variants)): 
                    svar.segs.append(it.variants[it.ind])
                else: 
                    svar.segs.append(None)
                i += 1
            svar.calc_coef()
            if (svar.coef >= 0): 
                svars.append(svar)
                svar = (None)
                if (len(svars) > 100): 
                    self.__sort_vars(svars)
                    del svars[10:10+len(svars) - 10]
            for j in range(len(segs) - 1, -1, -1):
                it = segs[j]
                it.ind += 1
                if (it.ind >= len(it.variants)): 
                    it.ind = 0
                else: 
                    break
            else: j = -1
            if (j < 0): 
                break
        self.__sort_vars(svars)
        if (len(svars) > 0): 
            self.best_var = svars[0]
            self.coef = self.best_var.coef
        else: 
            pass
        for it in self.items: 
            if (it.sub_sent is not None): 
                self.coef += it.sub_sent.coef
        for it in self.items: 
            if (it.participle_coef > 0): 
                self.coef *= it.participle_coef
        self.subs = Subsent.create_subsents(self)
        if (len(self.items) == 0): 
            return
        if (no_result): 
            return
        self.res_block = SemBlock(None)
        for sub in self.subs: 
            sub.res_frag = SemFragment(self.res_block)
            self.res_block.fragments.append(sub.res_frag)
            sub.res_frag.is_or = sub.is_or
            for it in sub.items: 
                if (sub.res_frag.begin_token is None): 
                    sub.res_frag.begin_token = it.begin_token
                sub.res_frag.end_token = it.end_token
                if (it.res_graph is not None): 
                    pass
                it.res_graph = sub.res_frag.graph
                it.res_frag = sub.res_frag
        for sub in self.subs: 
            if (sub.res_frag is None or sub.owner is None or sub.owner.res_frag is None): 
                continue
            if (sub.typ == SemFraglinkType.UNDEFINED): 
                continue
            self.res_block.add_link(sub.typ, sub.res_frag, sub.owner.res_frag, sub.question)
        self.__create_result(self.res_block)
    
    def __sort_vars(self, vars0_ : typing.List['SentenceVariant']) -> None:
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
    
    def trunc_oborot(self, is_participle : bool) -> bool:
        if (self.best_var is None or len(self.best_var.segs) == 0): 
            if (len(self.items) > 1): 
                del self.items[1:1+len(self.items) - 1]
                return True
            return False
        ret = False
        ind = 0
        if (self.best_var.segs[0] is None and not is_participle): 
            ind = 1
            while ind < len(self.items): 
                if (self.items[ind].can_be_comma_end): 
                    break
                ind += 1
        else: 
            for seg in self.best_var.segs: 
                if (seg is None): 
                    break
                for li in seg.links: 
                    if (li is None): 
                        continue
                    ret = True
                    ii = Utils.indexOfList(self.items, li.from0_.source, 0)
                    if (ii < 0): 
                        continue
                    if (li.to_verb is not None): 
                        if (li.to_verb == seg.source.before_verb): 
                            ind = (ii + 1)
                        elif (not is_participle and seg == self.best_var.segs[0] and li.to_verb == seg.source.after_verb): 
                            ii = ind
                            while ii < len(self.items): 
                                if (self.items[ii].source == li.to_verb): 
                                    ind = (ii + 1)
                                    break
                                ii += 1
                        else: 
                            break
                    else: 
                        jj = Utils.indexOfList(self.items, li.to.source, 0)
                        if (jj < 0): 
                            continue
                        if (jj < ii): 
                            ind = (ii + 1)
                        else: 
                            break
                if (not is_participle and seg == self.best_var.segs[0]): 
                    pass
                else: 
                    break
        if (not ret and ind == 0): 
            ind = 1
            while ind < len(self.items): 
                if (self.items[ind].can_be_comma_end): 
                    break
                ind += 1
        if (ind > 0 and (ind < (len(self.items) - 1))): 
            del self.items[ind:ind+len(self.items) - ind]
        return ret
    
    @staticmethod
    def _new2952(_arg1 : 'NGLinkType') -> 'Sentence':
        res = Sentence()
        res.last_noun_to_first_verb = _arg1
        return res