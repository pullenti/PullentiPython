# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.semantic.SemAttributeType import SemAttributeType
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.PrepositionHelper import PrepositionHelper
from pullenti.ner.core.ConjunctionHelper import ConjunctionHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.semantic.SemAttribute import SemAttribute
from pullenti.semantic.SemQuantity import SemQuantity
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.semantic.internal.NGItem import NGItem
from pullenti.morph.MorphMood import MorphMood
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.semantic.internal.NGLink import NGLink
from pullenti.semantic.internal.Sentence import Sentence
from pullenti.ner.core.VerbPhraseHelper import VerbPhraseHelper
from pullenti.ner.core.ConjunctionType import ConjunctionType
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.MetaToken import MetaToken
from pullenti.semantic.utils.DerivateService import DerivateService
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.core.NounPhraseToken import NounPhraseToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.semantic.internal.SentItemType import SentItemType
from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
from pullenti.semantic.internal.SentItemSubtype import SentItemSubtype
from pullenti.semantic.internal.NGLinkType import NGLinkType
from pullenti.semantic.internal.SemAttributeEx import SemAttributeEx
from pullenti.ner.core.VerbPhraseToken import VerbPhraseToken
from pullenti.semantic.internal.AdverbToken import AdverbToken
from pullenti.ner.core.ConjunctionToken import ConjunctionToken
from pullenti.semantic.internal.DelimToken import DelimToken

class SentItem:
    
    def __init__(self, mt : 'MetaToken') -> None:
        self.source = None;
        self.prep = None;
        self.typ = SentItemType.UNDEFINED
        self.sub_typ = SentItemSubtype.UNDEFINED
        self.sub_sent = None;
        self.plural = -1
        self.dr_groups = None;
        self.dr_groups2 = None;
        self.part_verb_typ = NGLinkType.UNDEFINED
        self.participle_coef = 1
        self.quant = None;
        self.attrs = None
        self.can_be_question = False
        self.result = None;
        self.result_verb_last = None;
        self.__m_res_graph = None;
        self.res_frag = None;
        self.result_list = None
        self.result_list_or = False
        self.__m_begin_token = None;
        self.__m_end_token = None;
        self.source = mt
        if (isinstance(mt, NounPhraseToken)): 
            npt = Utils.asObjectOrNull(mt, NounPhraseToken)
            if (npt.preposition is not None): 
                self.prep = npt.preposition.normal
            else: 
                self.prep = ""
            self.typ = SentItemType.NOUN
            normal = npt.noun.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, MorphGender.MASCULINE, False)
            if (normal is not None): 
                self.dr_groups = DerivateService.find_derivates(normal, True, None)
        elif ((isinstance(mt, ReferentToken)) or (isinstance(mt, NumbersWithUnitToken))): 
            self.typ = SentItemType.NOUN
        elif (isinstance(mt, AdverbToken)): 
            self.typ = SentItemType.ADVERB
        elif (isinstance(mt, ConjunctionToken)): 
            self.typ = SentItemType.CONJ
        elif (isinstance(mt, DelimToken)): 
            self.typ = SentItemType.DELIM
        elif (isinstance(mt, VerbPhraseToken)): 
            vpt = Utils.asObjectOrNull(mt, VerbPhraseToken)
            normal = (None if vpt.first_verb.verb_morph is None else Utils.ifNotNull(vpt.first_verb.verb_morph.normal_full, vpt.first_verb.verb_morph.normal_case))
            if (normal is not None): 
                self.dr_groups = DerivateService.find_derivates(normal, True, None)
            if (vpt.first_verb != vpt.last_verb): 
                normal = (vpt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False) if vpt.last_verb.verb_morph is None else Utils.ifNotNull(vpt.last_verb.verb_morph.normal_full, vpt.last_verb.verb_morph.normal_case))
                self.dr_groups2 = DerivateService.find_derivates(normal, True, None)
            else: 
                self.dr_groups2 = self.dr_groups
            self.prep = ("" if vpt.preposition is None else vpt.preposition.normal)
            self.typ = SentItemType.VERB
    
    def copy_from(self, it : 'SentItem') -> None:
        self.source = it.source
        self.typ = it.typ
        self.sub_typ = it.sub_typ
        self.prep = it.prep
        self.participle_coef = it.participle_coef
        self.dr_groups = it.dr_groups
        self.dr_groups2 = it.dr_groups2
        self.part_verb_typ = it.part_verb_typ
        self.__m_begin_token = it.__m_begin_token
        self.__m_end_token = it.__m_end_token
        self.plural = it.plural
        self.sub_sent = it.sub_sent
        self.quant = it.quant
        self.attrs = it.attrs
        self.can_be_question = it.can_be_question
        self.result = it.result
        self.result_list = it.result_list
        self.result_list_or = it.result_list_or
        self.result_verb_last = it.result_verb_last
        self.res_graph = it.res_graph
        self.res_frag = it.res_frag
    
    @property
    def res_graph(self) -> 'SemGraph':
        return self.__m_res_graph
    @res_graph.setter
    def res_graph(self, value) -> 'SemGraph':
        if (self.__m_res_graph is None): 
            self.__m_res_graph = value
        elif (value is not None and self.__m_res_graph != value): 
            self.__m_res_graph = value
        return value
    
    def add_attr(self, adv : 'AdverbToken') -> None:
        sa = SemAttribute._new2940(adv.spelling, adv.typ, adv.not0_)
        if (self.attrs is None): 
            self.attrs = list()
        self.attrs.append(SemAttributeEx._new2941(adv, sa))
    
    @property
    def begin_token(self) -> 'Token':
        if (self.__m_begin_token is not None): 
            return self.__m_begin_token
        if (self.source is not None): 
            return self.source.begin_token
        return None
    @begin_token.setter
    def begin_token(self, value) -> 'Token':
        self.__m_begin_token = value
        return value
    
    @property
    def end_token(self) -> 'Token':
        if (self.__m_end_token is not None): 
            return self.__m_end_token
        if (self.source is not None): 
            ret = self.source.end_token
            if (self.attrs is not None): 
                for a in self.attrs: 
                    if (a.token.end_char > ret.end_char): 
                        ret = a.token.end_token
            return ret
        return None
    @end_token.setter
    def end_token(self, value) -> 'Token':
        self.__m_end_token = value
        return value
    
    @property
    def can_be_noun(self) -> bool:
        if (((self.typ == SentItemType.NOUN or self.typ == SentItemType.DEEPART or self.typ == SentItemType.PARTAFTER) or self.typ == SentItemType.PARTBEFORE or self.typ == SentItemType.SUBSENT) or self.typ == SentItemType.FORMULA): 
            return True
        if (isinstance(self.source, VerbPhraseToken)): 
            if (self.source.first_verb.verb_morph is not None and self.source.first_verb.verb_morph.contains_attr("инф.", None)): 
                return True
        return False
    
    @property
    def can_be_comma_end(self) -> bool:
        cnj = Utils.asObjectOrNull(self.source, ConjunctionToken)
        if (cnj is None): 
            return False
        return cnj.typ == ConjunctionType.COMMA or cnj.typ == ConjunctionType.AND or cnj.typ == ConjunctionType.OR
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (not Utils.isNullOrEmpty(self.prep)): 
            print("{0} ".format(self.prep), end="", file=res, flush=True)
        print("{0}(".format(Utils.enumToString(self.typ)), end="", file=res, flush=True)
        if (self.sub_typ != SentItemSubtype.UNDEFINED): 
            print("{0}:".format(Utils.enumToString(self.sub_typ)), end="", file=res, flush=True)
        if (self.source is not None): 
            print(str(self.source), end="", file=res)
            if (self.sub_sent is not None): 
                print(" <= {0}".format(str(self.sub_sent)), end="", file=res, flush=True)
        elif (self.sub_sent is not None): 
            print(str(self.sub_sent), end="", file=res)
        print(')', end="", file=res)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def parse_near_items(t : 'Token', t1 : 'Token', lev : int, prev : typing.List['SentItem']) -> typing.List['SentItem']:
        if (lev > 100): 
            return None
        if (t is None or t.begin_char > t1.end_char): 
            return None
        res = list()
        if (isinstance(t, ReferentToken)): 
            res.append(SentItem(Utils.asObjectOrNull(t, MetaToken)))
            return res
        delim = DelimToken.try_parse(t)
        if (delim is not None): 
            res.append(SentItem(delim))
            return res
        conj = ConjunctionHelper.try_parse(t)
        if (conj is not None): 
            res.append(SentItem(conj))
            return res
        prep_ = PrepositionHelper.try_parse(t)
        t111 = (t if prep_ is None else prep_.end_token.next0_)
        if ((isinstance(t111, NumberToken)) and ((t111.morph.class0_.is_adjective and not t111.morph.class0_.is_noun))): 
            t111 = (None)
        num = (None if t111 is None else NumbersWithUnitToken.try_parse(t111, None, False, False, False, False))
        if (num is not None): 
            if (len(num.units) == 0): 
                npt1 = NounPhraseHelper.try_parse(num.end_token.next0_, SentItem.__m_npt_attrs, 0, None)
                if (npt1 is None and num.end_token.next0_ is not None and num.end_token.next0_.is_value("РАЗ", None)): 
                    npt1 = NounPhraseToken(num.end_token.next0_, num.end_token.next0_)
                    npt1.noun = MetaToken(num.end_token.next0_, num.end_token.next0_)
                if (npt1 is not None and prep_ is not None): 
                    if (npt1.noun.end_token.is_value("РАЗ", None)): 
                        npt1.morph.remove_items(prep_.next_case, False)
                    elif (((npt1.morph.case_) & prep_.next_case).is_undefined): 
                        npt1 = (None)
                    else: 
                        npt1.morph.remove_items(prep_.next_case, False)
                if ((npt1 is not None and npt1.end_token.is_value("ОНИ", None) and npt1.preposition is not None) and npt1.preposition.normal == "ИЗ"): 
                    npt1.morph = MorphCollection(num.end_token.morph)
                    npt1.preposition = (None)
                    nn = str(num)
                    si1 = SentItem(npt1)
                    if (nn == "1" and (isinstance(num.end_token, NumberToken)) and num.end_token.end_token.is_value("ОДИН", None)): 
                        a = SemAttribute._new2942(SemAttributeType.ONEOF, num.end_token.end_token.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False))
                        aex = SemAttributeEx._new2941(num, a)
                        si1.attrs = list()
                        si1.attrs.append(aex)
                    else: 
                        si1.quant = SemQuantity(nn, num.begin_token, num.end_token)
                    if (prep_ is not None): 
                        si1.prep = prep_.normal
                    res.append(si1)
                    return res
                if (npt1 is not None): 
                    si1 = SentItem._new2944(npt1, SemQuantity(str(num), num.begin_token, num.end_token))
                    if (prep_ is not None): 
                        si1.prep = prep_.normal
                    if (npt1.end_token.is_value("РАЗ", None)): 
                        si1.typ = SentItemType.FORMULA
                    if (((npt1.morph.number) & (MorphNumber.PLURAL)) == (MorphNumber.UNDEFINED) and si1.quant.spelling != "1"): 
                        ok = False
                        if (si1.quant.spelling.endswith("1")): 
                            ok = True
                        elif (si1.typ == SentItemType.FORMULA): 
                            ok = True
                        elif (si1.quant.spelling.endswith("2") and npt1.morph.case_.is_genitive): 
                            ok = True
                        elif (si1.quant.spelling.endswith("3") and npt1.morph.case_.is_genitive): 
                            ok = True
                        elif (si1.quant.spelling.endswith("4") and npt1.morph.case_.is_genitive): 
                            ok = True
                        if (ok): 
                            npt1.morph = MorphCollection()
                            npt1.morph.number = MorphNumber.PLURAL
                    res.append(si1)
                    return res
            num.begin_token = t
            num.morph = MorphCollection(num.end_token.morph)
            si = SentItem(num)
            if (prep_ is not None): 
                si.prep = prep_.normal
            res.append(si)
            if (si.prep == "НА"): 
                aa = AdverbToken.try_parse(si.end_token.next0_)
                if (aa is not None and ((aa.typ == SemAttributeType.LESS or aa.typ == SemAttributeType.GREAT))): 
                    si.add_attr(aa)
                    si.end_token = aa.end_token
            return res
        mc = t.get_morph_class_in_dictionary()
        adv = AdverbToken.try_parse(t)
        npt = NounPhraseHelper.try_parse(t, SentItem.__m_npt_attrs, 0, None)
        if (npt is not None and (isinstance(npt.end_token, TextToken)) and npt.end_token.term == "БЫЛИ"): 
            npt = (None)
        if (npt is not None and adv is not None): 
            if (adv.end_char > npt.end_char): 
                npt = (None)
            elif (adv.end_char == npt.end_char): 
                res.append(SentItem(npt))
                res.append(SentItem(adv))
                return res
        if (npt is not None and len(npt.adjectives) == 0): 
            if (npt.end_token.is_value("КОТОРЫЙ", None) and t.previous is not None and t.previous.is_comma_and): 
                res1 = SentItem.__parse_subsent(npt, t1, lev + 1, prev)
                if (res1 is not None): 
                    return res1
            if (npt.end_token.is_value("СКОЛЬКО", None)): 
                tt1 = npt.end_token.next0_
                if (tt1 is not None and tt1.is_value("ВСЕГО", None)): 
                    tt1 = tt1.next0_
                npt1 = NounPhraseHelper.try_parse(tt1, NounPhraseParseAttr.NO, 0, None)
                if (npt1 is not None and not npt1.morph.case_.is_undefined and prep_ is not None): 
                    if (((prep_.next_case) & npt1.morph.case_).is_undefined): 
                        npt1 = (None)
                    else: 
                        npt1.morph.remove_items(prep_.next_case, False)
                if (npt1 is not None): 
                    npt1.begin_token = npt.begin_token
                    npt1.preposition = npt.preposition
                    npt1.adjectives.append(MetaToken(npt.end_token, npt.end_token))
                    npt = npt1
            if (npt.end_token.morph.class0_.is_adjective): 
                if (VerbPhraseHelper.try_parse(t, True, False, False) is not None): 
                    npt = (None)
        vrb = None
        if (npt is not None and len(npt.adjectives) > 0): 
            vrb = VerbPhraseHelper.try_parse(t, True, False, False)
            if (vrb is not None and vrb.first_verb.is_participle): 
                npt = (None)
        elif (adv is None or npt is not None): 
            vrb = VerbPhraseHelper.try_parse(t, True, False, False)
        if (npt is not None): 
            res.append(SentItem(npt))
        if (vrb is not None and not vrb.first_verb.is_participle and not vrb.first_verb.is_dee_participle): 
            vars0_ = list()
            for wf in vrb.first_verb.morph.items: 
                if (wf.class0_.is_verb and (isinstance(wf, MorphWordForm)) and wf.is_in_dictionary): 
                    vars0_.append(Utils.asObjectOrNull(wf, MorphWordForm))
            if (len(vars0_) < 2): 
                res.append(SentItem(vrb))
            else: 
                vrb.first_verb.verb_morph = vars0_[0]
                res.append(SentItem(vrb))
                i = 1
                while i < len(vars0_): 
                    vrb = VerbPhraseHelper.try_parse(t, False, False, False)
                    if (vrb is None): 
                        break
                    vrb.first_verb.verb_morph = vars0_[i]
                    res.append(SentItem(vrb))
                    i += 1
                if (vars0_[0].misc.mood == MorphMood.IMPERATIVE and vars0_[1].misc.mood != MorphMood.IMPERATIVE): 
                    rr = res[0]
                    res[0] = res[1]
                    res[1] = rr
            return res
        if (vrb is not None): 
            res1 = SentItem.__parse_participles(vrb, t1, lev + 1)
            if (res1 is not None): 
                res.extend(res1)
        if (len(res) > 0): 
            return res
        if (adv is not None): 
            if (adv.typ == SemAttributeType.OTHER): 
                npt1 = NounPhraseHelper.try_parse(adv.end_token.next0_, SentItem.__m_npt_attrs, 0, None)
                if (npt1 is not None and npt1.end_token.is_value("ОНИ", None) and npt1.preposition is not None): 
                    si1 = SentItem(npt1)
                    a = SemAttribute._new2942(SemAttributeType.OTHER, adv.end_token.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
                    aex = SemAttributeEx._new2941(num, a)
                    si1.attrs = list()
                    si1.attrs.append(aex)
                    if (prep_ is not None): 
                        si1.prep = prep_.normal
                    res.append(si1)
                    return res
                for i in range(len(prev) - 1, -1, -1):
                    if (prev[i].attrs is not None): 
                        for a in prev[i].attrs: 
                            if (a.attr.typ == SemAttributeType.ONEOF): 
                                si1 = SentItem(prev[i].source)
                                aa = SemAttribute._new2942(SemAttributeType.OTHER, adv.end_token.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
                                aex = SemAttributeEx._new2941(adv, aa)
                                si1.attrs = list()
                                si1.attrs.append(aex)
                                if (prep_ is not None): 
                                    si1.prep = prep_.normal
                                si1.begin_token = adv.begin_token
                                si1.end_token = adv.end_token
                                res.append(si1)
                                return res
            res.append(SentItem(adv))
            return res
        if (mc.is_adjective): 
            npt = NounPhraseToken._new2949(t, t, MorphCollection(t.morph))
            npt.noun = MetaToken(t, t)
            res.append(SentItem(npt))
            return res
        return None
    
    @staticmethod
    def __parse_subsent(npt : 'NounPhraseToken', t1 : 'Token', lev : int, prev : typing.List['SentItem']) -> typing.List['SentItem']:
        ok = False
        if (prev is not None): 
            for i in range(len(prev) - 1, -1, -1):
                it = prev[i]
                if (it.typ == SentItemType.CONJ or it.typ == SentItemType.DELIM): 
                    ok = True
                    break
                if (it.typ == SentItemType.VERB): 
                    break
        if (not ok): 
            return None
        sents = Utils.ifNotNull(Sentence.parse_variants(npt.end_token.next0_, t1, lev + 1, 20, SentItemType.SUBSENT), list())
        endpos = list()
        res = list()
        for s in sents: 
            s.items.insert(0, SentItem(npt))
            s.calc_coef(True)
            s.trunc_oborot(False)
            end = s.items[len(s.items) - 1].end_token.end_char
            if (end in endpos): 
                continue
            endpos.append(end)
            s.calc_coef(False)
            part = SentItem(npt)
            part.typ = SentItemType.SUBSENT
            part.sub_typ = SentItemSubtype.WICH
            part.sub_sent = s
            part.result = s.items[0].result
            part.end_token = s.items[len(s.items) - 1].end_token
            res.append(part)
        return res
    
    @staticmethod
    def __parse_participles(vb : 'VerbPhraseToken', t1 : 'Token', lev : int) -> typing.List['SentItem']:
        sents = Utils.ifNotNull(Sentence.parse_variants(vb.end_token.next0_, t1, lev + 1, 20, SentItemType.PARTBEFORE), list())
        typ_ = NGLinkType.AGENT
        if (vb.first_verb.morph.contains_attr("страд.з.", None)): 
            typ_ = NGLinkType.PACIENT
        elif (vb.first_verb.morph.contains_attr("возвр.", None)): 
            typ_ = NGLinkType.PACIENT
        endpos = list()
        res = list()
        changed = False
        for s in sents: 
            if (vb.first_verb.is_dee_participle): 
                break
            i = 0
            first_pass3960 = True
            while True:
                if first_pass3960: first_pass3960 = False
                else: i += 1
                if (not (i < len(s.items))): break
                it = s.items[i]
                if (not it.can_be_noun or it.typ == SentItemType.VERB): 
                    continue
                if (not Utils.isNullOrEmpty(it.prep)): 
                    continue
                if (it.typ == SentItemType.PARTBEFORE or it.typ == SentItemType.PARTAFTER): 
                    continue
                li = NGLink._new2951(typ_, NGItem._new2922(it), vb)
                li.calc_coef(True)
                if (li.coef < 0): 
                    continue
                if (it.end_token.end_char in endpos): 
                    continue
                ss = Sentence._new2952(typ_)
                ss.items.append(SentItem(vb))
                j = 0
                while j <= i: 
                    si = SentItem(None)
                    si.copy_from(s.items[j])
                    ss.items.append(si)
                    j += 1
                ss.calc_coef(False)
                changed = True
                if (ss.coef < 0): 
                    continue
                part = SentItem(it.source)
                part.typ = SentItemType.PARTAFTER
                part.sub_sent = ss
                if (vb.preposition is not None): 
                    part.prep = vb.preposition.normal
                part.begin_token = vb.begin_token
                part.end_token = it.source.end_token
                if ((i + 1) < len(ss.items)): 
                    part.result = ss.items[i + 1].result
                endpos.append(it.end_token.end_char)
                res.append(part)
        endpos.clear()
        if (changed): 
            sents = (Utils.ifNotNull(Sentence.parse_variants(vb.end_token.next0_, t1, lev + 1, 20, SentItemType.PARTBEFORE), list()))
        for s in sents: 
            s.items.insert(0, SentItem(vb))
            s.calc_coef(True)
            s.trunc_oborot(True)
            end = s.items[len(s.items) - 1].end_token.end_char
            endpos.append(end)
            s.not_last_noun_to_first_verb = typ_
            s.calc_coef(False)
            part = SentItem(vb)
            part.part_verb_typ = typ_
            part.typ = (SentItemType.DEEPART if vb.first_verb.is_dee_participle else SentItemType.PARTBEFORE)
            part.sub_sent = s
            part.result = s.items[0].result
            part.result_verb_last = s.items[0].result_verb_last
            part.end_token = s.items[len(s.items) - 1].end_token
            res.append(part)
        if (len(res) == 0 and len(sents) == 0): 
            part = SentItem(vb)
            part.part_verb_typ = typ_
            part.typ = (SentItemType.DEEPART if vb.first_verb.is_dee_participle else SentItemType.PARTBEFORE)
            res.append(part)
        return res
    
    __m_npt_attrs = Utils.valToEnum(((((NounPhraseParseAttr.ADJECTIVECANBELAST) | (NounPhraseParseAttr.IGNOREBRACKETS) | (NounPhraseParseAttr.PARSEADVERBS)) | (NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.PARSEPREPOSITION)) | (NounPhraseParseAttr.PARSEPRONOUNS) | (NounPhraseParseAttr.PARSEVERBS)) | (NounPhraseParseAttr.REFERENTCANBENOUN) | (NounPhraseParseAttr.MULTINOUNS), NounPhraseParseAttr)
    
    @staticmethod
    def _new2944(_arg1 : 'MetaToken', _arg2 : 'SemQuantity') -> 'SentItem':
        res = SentItem(_arg1)
        res.quant = _arg2
        return res