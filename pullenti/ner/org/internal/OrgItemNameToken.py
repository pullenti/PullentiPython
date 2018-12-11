# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.Explanatory import Explanatory
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.Token import Token
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.org.internal.EpNerOrgInternalResourceHelper import EpNerOrgInternalResourceHelper
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.TextToken import TextToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.org.internal.OrgItemTypeToken import OrgItemTypeToken
from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.org.internal.OrgItemEponymToken import OrgItemEponymToken
from pullenti.ner.org.OrganizationAnalyzer import OrganizationAnalyzer
from pullenti.ner.org.internal.OrgItemEngItem import OrgItemEngItem

class OrgItemNameToken(MetaToken):
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.value = None;
        self.is_noun_phrase = False
        self.is_denomination = False
        self.is_in_dictionary = False
        self.is_std_tail = False
        self.is_std_name = False
        self.is_empty_word = False
        self.is_ignored_part = False
        self.std_org_name_nouns = 0
        self.org_std_prof = OrgProfile.UNDEFINED
        self.is_after_conjunction = False
        self.preposition = None;
    
    def __str__(self) -> str:
        res = Utils.newStringIO(self.value)
        if (self.is_noun_phrase): 
            print(" NounPrase", end="", file=res)
        if (self.is_denomination): 
            print(" Denom", end="", file=res)
        if (self.is_in_dictionary): 
            print(" InDictionary", end="", file=res)
        if (self.is_after_conjunction): 
            print(" IsAfterConjunction", end="", file=res)
        if (self.is_std_tail): 
            print(" IsStdTail", end="", file=res)
        if (self.is_std_name): 
            print(" IsStdName", end="", file=res)
        if (self.is_ignored_part): 
            print(" IsIgnoredPart", end="", file=res)
        if (self.preposition is not None): 
            print(" IsAfterPreposition '{0}'".format(self.preposition), end="", file=res, flush=True)
        print(" {0} ({1})".format(str(self.chars), self.getSourceText()), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def tryAttach(t : 'Token', prev : 'OrgItemNameToken', ext_onto : bool, first : bool) -> 'OrgItemNameToken':
        if (t is None): 
            return None
        if (t.isValue("ОРДЕНА", None) and t.next0_ is not None): 
            npt = NounPhraseHelper.tryParse(t.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                t1 = npt.end_token
                if (((t1.isValue("ЗНАК", None) or t1.isValue("ДРУЖБА", None))) and (t1.whitespaces_after_count < 2)): 
                    npt = NounPhraseHelper.tryParse(t1.next0_, NounPhraseParseAttr.NO, 0)
                    if (npt is not None): 
                        t1 = npt.end_token
                return OrgItemNameToken._new1696(t, t1, True)
            if (t.next0_.getMorphClassInDictionary().is_proper_surname): 
                return OrgItemNameToken._new1696(t, t.next0_, True)
            ppp = t.kit.processReferent("PERSON", t.next0_)
            if (ppp is not None): 
                return OrgItemNameToken._new1696(t, ppp.end_token, True)
            if ((t.whitespaces_after_count < 2) and BracketHelper.canBeStartOfSequence(t.next0_, True, False)): 
                br = BracketHelper.tryParse(t.next0_, BracketParseAttr.NEARCLOSEBRACKET, 10)
                if (br is not None and (br.length_char < 40)): 
                    return OrgItemNameToken._new1696(t, br.end_token, True)
        if (first and t.chars.is_cyrillic_letter and t.morph.class0_.is_preposition): 
            if (not t.isValue("ПО", None) and not t.isValue("ПРИ", None)): 
                return None
        res = OrgItemNameToken.__TryAttach(t, prev, ext_onto)
        if (res is None): 
            if (ext_onto): 
                if (((isinstance(t.getReferent(), GeoReferent))) or (((isinstance(t, TextToken)) and not t.isChar(';')))): 
                    return OrgItemNameToken._new1700(t, t, t.getSourceText())
            return None
        if (prev is None and not ext_onto): 
            if (t.kit.ontology is not None): 
                ad = Utils.asObjectOrNull(t.kit.ontology._getAnalyzerData(OrganizationAnalyzer.ANALYZER_NAME), OrganizationAnalyzer.OrgAnalyzerData)
                if (ad is not None): 
                    tok = ad.org_pure_names.tryParse(t, TerminParseAttr.NO)
                    if (tok is not None and tok.end_char > res.end_char): 
                        res.end_token = tok.end_token
        if (prev is not None and not ext_onto): 
            if ((prev.chars.is_all_lower and not res.chars.is_all_lower and not res.is_std_tail) and not res.is_std_name): 
                if (prev.chars.is_latin_letter and res.chars.is_latin_letter): 
                    pass
                elif (OrgItemNameToken.__m_std_nouns.tryParse(res.begin_token, TerminParseAttr.NO) is not None): 
                    pass
                else: 
                    return None
        if ((res.end_token.next0_ is not None and not res.end_token.is_whitespace_after and res.end_token.next0_.is_hiphen) and not res.end_token.next0_.is_whitespace_after): 
            tt = Utils.asObjectOrNull(res.end_token.next0_.next0_, TextToken)
            if (tt is not None): 
                if (tt.chars == res.chars or tt.chars.is_all_upper): 
                    res.end_token = tt
                    res.value = "{0}-{1}".format(res.value, tt.term)
        if ((res.end_token.next0_ is not None and res.end_token.next0_.is_and and res.end_token.whitespaces_after_count == 1) and res.end_token.next0_.whitespaces_after_count == 1): 
            res1 = OrgItemNameToken.__TryAttach(res.end_token.next0_.next0_, prev, ext_onto)
            if (res1 is not None and res1.chars == res.chars and OrgItemTypeToken.tryAttach(res.end_token.next0_.next0_, False, None) is None): 
                if (not ((res1.morph.case_) & res.morph.case_).is_undefined): 
                    res.end_token = res1.end_token
                    res.value = "{0} {1} {2}".format(res.value, ("ТА" if res.kit.base_language.is_ua else "И"), res1.value)
        tt = res.begin_token
        while tt is not None and tt.end_char <= res.end_char: 
            if (OrgItemNameToken.__m_std_nouns.tryParse(tt, TerminParseAttr.NO) is not None): 
                res.std_org_name_nouns += 1
            tt = tt.next0_
        if (OrgItemNameToken.__m_std_nouns.tryParse(res.end_token, TerminParseAttr.NO) is not None): 
            cou = 1
            non = False
            et = res.end_token
            if (not OrgItemNameToken.__isNotTermNoun(res.end_token)): 
                non = True
            br = False
            tt = res.end_token.next0_
            first_pass3057 = True
            while True:
                if first_pass3057: first_pass3057 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_table_control_char): 
                    break
                if (tt.isChar('(')): 
                    if (not non): 
                        break
                    br = True
                    continue
                if (tt.isChar(')')): 
                    br = False
                    et = tt
                    break
                if (not ((isinstance(tt, TextToken)))): 
                    break
                if (tt.whitespaces_before_count > 1): 
                    if (tt.newlines_before_count > 1): 
                        break
                    if (tt.chars != res.end_token.chars): 
                        break
                if (tt.morph.class0_.is_preposition or tt.is_comma_and): 
                    continue
                dd = tt.getMorphClassInDictionary()
                if (not dd.is_noun and not dd.is_adjective): 
                    break
                npt2 = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
                if (npt2 is None): 
                    if (dd == MorphClass.ADJECTIVE): 
                        continue
                    break
                if (OrgItemNameToken.__m_std_nouns.tryParse(npt2.end_token, TerminParseAttr.NO) is None): 
                    break
                if (npt2.end_token.chars != res.end_token.chars): 
                    break
                if ((npt2.end_token.isValue("УПРАВЛЕНИЕ", None) or npt2.end_token.isValue("ИНСТИТУТ", None) or npt2.end_token.isValue("УПРАВЛІННЯ", None)) or npt2.end_token.isValue("ІНСТИТУТ", None) or tt.previous.isValue("ПРИ", None)): 
                    rt = tt.kit.processReferent(OrganizationAnalyzer.ANALYZER_NAME, tt)
                    if (rt is not None): 
                        break
                cou += 1
                tt = npt2.end_token
                if (not OrgItemNameToken.__isNotTermNoun(tt)): 
                    non = True
                    et = tt
            if (non and not br): 
                res.std_org_name_nouns += cou
                res.end_token = et
        return res
    
    __m_not_terminate_nouns = None
    
    @staticmethod
    def __isNotTermNoun(t : 'Token') -> bool:
        if (not ((isinstance(t, TextToken)))): 
            return False
        if (not ((isinstance(t.previous, TextToken)))): 
            return False
        if ((t.previous).term != "ПО"): 
            return False
        for v in OrgItemNameToken.__m_not_terminate_nouns: 
            if (t.isValue(v, None)): 
                return True
        return False
    
    @staticmethod
    def __TryAttach(t : 'Token', prev : 'OrgItemNameToken', ext_onto : bool) -> 'OrgItemNameToken':
        if (t is None): 
            return None
        r = t.getReferent()
        if (r is not None): 
            if (r.type_name == "DENOMINATION"): 
                return OrgItemNameToken._new1701(t, t, r.toString(True, t.kit.base_language, 0), True)
            if ((isinstance(r, GeoReferent)) and t.chars.is_latin_letter): 
                res2 = OrgItemNameToken.__TryAttach(t.next0_, prev, ext_onto)
                if (res2 is not None and res2.chars.is_latin_letter): 
                    res2.begin_token = t
                    res2.value = "{0} {1}".format(MiscHelper.getTextValueOfMetaToken(Utils.asObjectOrNull(t, MetaToken), GetTextAttr.NO), res2.value)
                    res2.is_in_dictionary = False
                    return res2
            return None
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        res = None
        tok = OrgItemNameToken.__m_std_tails.tryParse(t, TerminParseAttr.NO)
        if (tok is None and t.isChar(',')): 
            tok = OrgItemNameToken.__m_std_tails.tryParse(t.next0_, TerminParseAttr.NO)
        if (tok is not None): 
            return OrgItemNameToken._new1702(t, tok.end_token, tok.termin.canonic_text, tok.termin.tag is None, tok.termin.tag is not None, tok.morph)
        tok = OrgItemNameToken.__m_std_names.tryParse(t, TerminParseAttr.NO)
        if ((tok) is not None): 
            return OrgItemNameToken._new1703(t, tok.end_token, tok.termin.canonic_text, True)
        eng = OrgItemEngItem.tryAttach(t, False)
        if (eng is None and t.isChar(',')): 
            eng = OrgItemEngItem.tryAttach(t.next0_, False)
        if (eng is not None): 
            return OrgItemNameToken._new1704(t, eng.end_token, eng.full_value, True)
        if (tt.chars.is_all_lower and prev is not None): 
            if (not prev.chars.is_all_lower and not prev.chars.is_capital_upper): 
                return None
        if (tt.isChar(',') and prev is not None): 
            npt1 = NounPhraseHelper.tryParse(t.next0_, NounPhraseParseAttr.NO, 0)
            if (npt1 is None or npt1.chars != prev.chars or ((npt1.morph.case_) & prev.morph.case_).is_undefined): 
                return None
            ty = OrgItemTypeToken.tryAttach(t.next0_, False, None)
            if (ty is not None): 
                return None
            if (npt1.end_token.next0_ is None or not npt1.end_token.next0_.isValue("И", None)): 
                return None
            t1 = npt1.end_token.next0_
            npt2 = NounPhraseHelper.tryParse(t1.next0_, NounPhraseParseAttr.NO, 0)
            if (npt2 is None or npt2.chars != prev.chars or ((npt2.morph.case_) & npt1.morph.case_ & prev.morph.case_).is_undefined): 
                return None
            ty = OrgItemTypeToken.tryAttach(t1.next0_, False, None)
            if (ty is not None): 
                return None
            res = OrgItemNameToken._new1705(npt1.begin_token, npt1.end_token, npt1.morph, npt1.getNormalCaseText(None, False, MorphGender.UNDEFINED, False))
            res.is_noun_phrase = True
            res.is_after_conjunction = True
            if (prev.preposition is not None): 
                res.preposition = prev.preposition
            return res
        if (((tt.isChar('&') or tt.isValue("AND", None) or tt.isValue("UND", None))) and prev is not None): 
            if ((isinstance(tt.next0_, TextToken)) and tt.length_char == 1 and tt.next0_.chars.is_latin_letter): 
                res = OrgItemNameToken._new1706(tt, tt.next0_, tt.next0_.chars)
                res.is_after_conjunction = True
                res.value = ("& " + (tt.next0_).term)
                return res
            res = OrgItemNameToken.tryAttach(tt.next0_, None, ext_onto, False)
            if (res is None or res.chars != prev.chars): 
                return None
            res.is_after_conjunction = True
            res.value = ("& " + res.value)
            return res
        if (not tt.chars.is_letter): 
            return None
        expinf = None
        if (prev is not None and prev.end_token.getMorphClassInDictionary().is_noun): 
            wo = prev.end_token.getNormalCaseText(MorphClass.NOUN, True, MorphGender.UNDEFINED, False)
            expinf = Explanatory.findWords(wo, prev.end_token.morph.language)
        npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
        if (npt is not None and npt.internal_noun is not None): 
            npt = (None)
        expl_ok = False
        if (npt is not None and expinf is not None): 
            for ei in expinf: 
                if (ei.nexts is not None and "" in ei.nexts): 
                    mc = ei.nexts[""]
                    if (not ((mc) & npt.morph.case_).is_undefined): 
                        expl_ok = True
                        break
        if (npt is not None and ((expl_ok or npt.morph.case_.is_genitive or ((prev is not None and not ((prev.morph.case_) & npt.morph.case_).is_undefined))))): 
            mc = npt.begin_token.getMorphClassInDictionary()
            if (mc.is_verb or mc.is_pronoun): 
                return None
            if (mc.is_adverb): 
                if (npt.begin_token.next0_ is not None and npt.begin_token.next0_.is_hiphen): 
                    pass
                else: 
                    return None
            if (mc.is_preposition): 
                return None
            if (mc.is_noun and npt.chars.is_all_lower): 
                ca = npt.morph.case_
                if ((not ca.is_dative and not ca.is_genitive and not ca.is_instrumental) and not ca.is_prepositional): 
                    return None
            res = OrgItemNameToken._new1705(npt.begin_token, npt.end_token, npt.morph, npt.getNormalCaseText(None, False, MorphGender.UNDEFINED, False))
            res.is_noun_phrase = True
            if ((npt.end_token.whitespaces_after_count < 2) and (isinstance(npt.end_token.next0_, TextToken))): 
                npt2 = NounPhraseHelper.tryParse(npt.end_token.next0_, NounPhraseParseAttr.NO, 0)
                if (npt2 is not None and npt2.morph.case_.is_genitive and npt2.chars.is_all_lower): 
                    typ = OrgItemTypeToken.tryAttach(npt.end_token.next0_, True, None)
                    epo = OrgItemEponymToken.tryAttach(npt.end_token.next0_, False)
                    rtt = t.kit.processReferent("PERSONPROPERTY", npt.end_token.next0_)
                    if (typ is None and epo is None and ((rtt is None or rtt.morph.number == MorphNumber.PLURAL))): 
                        res.end_token = npt2.end_token
                        res.value = "{0} {1}".format(res.value, MiscHelper.getTextValueOfMetaToken(npt2, GetTextAttr.NO))
                elif (npt.end_token.next0_.is_comma and (isinstance(npt.end_token.next0_.next0_, TextToken))): 
                    tt2 = npt.end_token.next0_.next0_
                    mv2 = tt2.getMorphClassInDictionary()
                    if (mv2.is_adjective and mv2.is_verb): 
                        bi = MorphBaseInfo._new1708(npt.morph.case_, npt.morph.gender, npt.morph.number)
                        if (tt2.morph.checkAccord(bi, False)): 
                            npt2 = NounPhraseHelper.tryParse(tt2.next0_, NounPhraseParseAttr.NO, 0)
                            if (npt2 is not None and ((npt2.morph.case_.is_dative or npt2.morph.case_.is_genitive)) and npt2.chars.is_all_lower): 
                                res.end_token = npt2.end_token
                                res.value = "{0} {1}".format(res.value, MiscHelper.getTextValue(npt.end_token.next0_, res.end_token, GetTextAttr.NO))
            if (expl_ok): 
                res.is_after_conjunction = True
        elif (npt is not None and ((((prev is not None and prev.is_noun_phrase and npt.morph.case_.is_instrumental)) or ext_onto))): 
            res = OrgItemNameToken._new1705(npt.begin_token, npt.end_token, npt.morph, npt.getNormalCaseText(None, False, MorphGender.UNDEFINED, False))
            res.is_noun_phrase = True
        elif (tt.is_and): 
            res = OrgItemNameToken.tryAttach(tt.next0_, prev, ext_onto, False)
            if (res is None or not res.is_noun_phrase or prev is None): 
                return None
            if (((prev.morph.case_) & res.morph.case_).is_undefined): 
                return None
            if (prev.morph.number != MorphNumber.UNDEFINED and res.morph.number != MorphNumber.UNDEFINED): 
                if ((((prev.morph.number) & (res.morph.number))) == (MorphNumber.UNDEFINED)): 
                    if (prev.chars != res.chars): 
                        return None
                    ty = OrgItemTypeToken.tryAttach(res.end_token.next0_, False, None)
                    if (ty is not None): 
                        return None
            ci = res.chars
            res.chars = ci
            res.is_after_conjunction = True
            return res
        elif (((tt.term == "ПО" or tt.term == "ПРИ" or tt.term == "ЗА") or tt.term == "С" or tt.term == "В") or tt.term == "НА"): 
            npt = NounPhraseHelper.tryParse(t.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                if (OrgItemNameToken.__m_vervot_words.tryParse(npt.end_token, TerminParseAttr.NO) is not None): 
                    return None
                ok = False
                if (tt.term == "ПО"): 
                    ok = npt.morph.case_.is_dative
                elif (tt.term == "С"): 
                    ok = npt.morph.case_.is_instrumental
                elif (tt.term == "ЗА"): 
                    ok = (npt.morph.case_.is_genitive | npt.morph.case_.is_instrumental)
                elif (tt.term == "НА"): 
                    ok = npt.morph.case_.is_prepositional
                elif (tt.term == "В"): 
                    ok = (npt.morph.case_.is_dative | npt.morph.case_.is_prepositional)
                    if (ok): 
                        ok = False
                        if (t.next0_.isValue("СФЕРА", None) or t.next0_.isValue("ОБЛАСТЬ", None)): 
                            ok = True
                elif (tt.term == "ПРИ"): 
                    ok = npt.morph.case_.is_prepositional
                    if (ok): 
                        if (OrgItemTypeToken.tryAttach(tt.next0_, True, None) is not None): 
                            ok = False
                        else: 
                            rt = tt.kit.processReferent(OrganizationAnalyzer.ANALYZER_NAME, tt.next0_)
                            if (rt is not None): 
                                ok = False
                    s = npt.noun.getNormalCaseText(None, False, MorphGender.UNDEFINED, False)
                    if (s == "ПОДДЕРЖКА" or s == "УЧАСТИЕ"): 
                        ok = False
                else: 
                    ok = npt.morph.case_.is_prepositional
                if (ok): 
                    res = OrgItemNameToken._new1710(t, npt.end_token, npt.morph, npt.getNormalCaseText(None, True, MorphGender.UNDEFINED, False), npt.chars)
                    res.is_noun_phrase = True
                    res.preposition = tt.term
                    if (((res.value == "ДЕЛО" or res.value == "ВОПРОС")) and not res.is_newline_after): 
                        res2 = OrgItemNameToken.__TryAttach(res.end_token.next0_, res, ext_onto)
                        if (res2 is not None and res2.morph.case_.is_genitive): 
                            res.value = "{0} {1}".format(res.value, res2.value)
                            res.end_token = res2.end_token
                            ttt = res2.end_token.next0_
                            while ttt is not None: 
                                if (not ttt.is_comma_and): 
                                    break
                                res3 = OrgItemNameToken.__TryAttach(ttt.next0_, res2, ext_onto)
                                if (res3 is None): 
                                    break
                                res.value = "{0} {1}".format(res.value, res3.value)
                                res.end_token = res3.end_token
                                if (ttt.is_and): 
                                    break
                                ttt = res.end_token
                                ttt = ttt.next0_
            if (res is None): 
                return None
        elif (tt.term == "OF"): 
            t1 = tt.next0_
            if (t1 is not None and MiscHelper.isEngArticle(t1)): 
                t1 = t1.next0_
            if (t1 is not None and t1.chars.is_latin_letter and not t1.chars.is_all_lower): 
                res = OrgItemNameToken._new1711(t, t1, t1.chars, t1.morph)
                ttt = t1.next0_
                first_pass3058 = True
                while True:
                    if first_pass3058: first_pass3058 = False
                    else: ttt = ttt.next0_
                    if (not (ttt is not None)): break
                    if (ttt.whitespaces_before_count > 2): 
                        break
                    if (MiscHelper.isEngAdjSuffix(ttt)): 
                        ttt = ttt.next0_
                        continue
                    if (not ttt.chars.is_latin_letter): 
                        break
                    if (ttt.morph.class0_.is_preposition): 
                        break
                    res.end_token = ttt
                    t1 = res.end_token
                res.value = MiscHelper.getTextValue(t, t1, GetTextAttr.IGNOREARTICLES)
                res.preposition = tt.term
                return res
        if (res is None): 
            if (tt.chars.is_latin_letter and tt.length_char == 1): 
                pass
            elif (tt.chars.is_all_lower or (tt.length_char < 2)): 
                if (not tt.chars.is_latin_letter or prev is None or not prev.chars.is_latin_letter): 
                    return None
            if (tt.chars.is_cyrillic_letter): 
                mc = tt.getMorphClassInDictionary()
                if (mc.is_verb or mc.is_adverb): 
                    return None
            elif (tt.chars.is_latin_letter and not tt.is_whitespace_after): 
                if (not tt.is_whitespace_after and (tt.length_char < 5)): 
                    if (isinstance(tt.next0_, NumberToken)): 
                        return None
            res = OrgItemNameToken._new1712(tt, tt, tt.term, tt.morph)
            t = tt.next0_
            while t is not None: 
                if ((((t.is_hiphen or t.isCharOf("\\/"))) and t.next0_ is not None and (isinstance(t.next0_, TextToken))) and not t.is_whitespace_before and not t.is_whitespace_after): 
                    t = t.next0_
                    res.end_token = t
                    res.value = "{0}{1}{2}".format(res.value, ('.' if t.previous.isChar('.') else '-'), (t).term)
                elif (t.isChar('.')): 
                    if (not t.is_whitespace_after and not t.is_whitespace_before and (isinstance(t.next0_, TextToken))): 
                        res.end_token = t.next0_
                        t = t.next0_
                        res.value = "{0}.{1}".format(res.value, (t).term)
                    elif ((t.next0_ is not None and not t.is_newline_after and t.next0_.chars.is_latin_letter) and tt.chars.is_latin_letter): 
                        res.end_token = t
                    else: 
                        break
                else: 
                    break
                t = t.next0_
        t0 = res.begin_token
        while t0 is not None: 
            tt = Utils.asObjectOrNull(t0, TextToken)
            if ((tt) is not None and tt.is_letters): 
                if (not tt.morph.class0_.is_conjunction and not tt.morph.class0_.is_preposition): 
                    for mf in tt.morph.items: 
                        if ((mf).is_in_dictionary): 
                            res.is_in_dictionary = True
            if (t0 == res.end_token): 
                break
            t0 = t0.next0_
        if (res.begin_token == res.end_token and res.begin_token.chars.is_all_upper): 
            if (res.end_token.next0_ is not None and not res.end_token.is_whitespace_after): 
                t1 = res.end_token.next0_
                if (t1.next0_ is not None and not t1.is_whitespace_after and t1.is_hiphen): 
                    t1 = t1.next0_
                if (isinstance(t1, NumberToken)): 
                    res.value += str((t1).value)
                    res.end_token = t1
        if (res.begin_token == res.end_token and res.begin_token.chars.is_last_lower): 
            src = res.begin_token.getSourceText()
            for i in range(len(src) - 1, -1, -1):
                if (str.isupper(src[i])): 
                    res.value = src[0:0+i + 1]
                    break
        return res
    
    __m_std_names = None
    
    __m_std_tails = None
    
    __m_vervot_words = None
    
    __m_std_nouns = None
    
    _m_dep_std_names = None
    
    @staticmethod
    def initialize() -> None:
        OrgItemNameToken.__m_std_tails = TerminCollection()
        OrgItemNameToken.__m_std_names = TerminCollection()
        OrgItemNameToken.__m_vervot_words = TerminCollection()
        t = Termin("INCORPORATED")
        t.addAbridge("INC.")
        OrgItemNameToken.__m_std_tails.add(t)
        t = Termin("CORPORATION")
        t.addAbridge("CORP.")
        OrgItemNameToken.__m_std_tails.add(t)
        t = Termin("LIMITED")
        t.addAbridge("LTD.")
        OrgItemNameToken.__m_std_tails.add(t)
        t = Termin("AG")
        OrgItemNameToken.__m_std_tails.add(t)
        t = Termin("GMBH")
        OrgItemNameToken.__m_std_tails.add(t)
        for s in ["ЗАКАЗЧИК", "ИСПОЛНИТЕЛЬ", "РАЗРАБОТЧИК", "БЕНЕФИЦИАР", "ПОЛУЧАТЕЛЬ", "ОТПРАВИТЕЛЬ", "ИЗГОТОВИТЕЛЬ", "ПРОИЗВОДИТЕЛЬ", "ПОСТАВЩИК", "АБОНЕНТ", "КЛИЕНТ", "ВКЛАДЧИК", "СУБЪЕКТ", "ПРОДАВЕЦ", "ПОКУПАТЕЛЬ", "АРЕНДОДАТЕЛЬ", "АРЕНДАТОР", "СУБАРЕНДАТОР", "НАЙМОДАТЕЛЬ", "НАНИМАТЕЛЬ", "АГЕНТ", "ПРИНЦИПАЛ", "ПРОДАВЕЦ", "ПОСТАВЩИК", "ПОДРЯДЧИК", "СУБПОДРЯДЧИК"]: 
            OrgItemNameToken.__m_std_tails.add(Termin._new118(s, s))
        for s in ["ЗАМОВНИК", "ВИКОНАВЕЦЬ", "РОЗРОБНИК", "БЕНЕФІЦІАР", "ОДЕРЖУВАЧ", "ВІДПРАВНИК", "ВИРОБНИК", "ВИРОБНИК", "ПОСТАЧАЛЬНИК", "АБОНЕНТ", "КЛІЄНТ", "ВКЛАДНИК", "СУБ'ЄКТ", "ПРОДАВЕЦЬ", "ПОКУПЕЦЬ", "ОРЕНДОДАВЕЦЬ", "ОРЕНДАР", "СУБОРЕНДАР", "НАЙМОДАВЕЦЬ", "НАЙМАЧ", "АГЕНТ", "ПРИНЦИПАЛ", "ПРОДАВЕЦЬ", "ПОСТАЧАЛЬНИК", "ПІДРЯДНИК", "СУБПІДРЯДНИК"]: 
            OrgItemNameToken.__m_std_tails.add(Termin._new477(s, MorphLang.UA, s))
        t = Termin("РАЗРАБОТКА ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ")
        t.addAbridge("РАЗРАБОТКИ ПО")
        OrgItemNameToken.__m_std_names.add(t)
        for s in ["СПЕЦИАЛЬНОСТЬ", "ДИАГНОЗ"]: 
            OrgItemNameToken.__m_vervot_words.add(Termin(s))
        for s in ["СПЕЦІАЛЬНІСТЬ", "ДІАГНОЗ"]: 
            OrgItemNameToken.__m_vervot_words.add(Termin(s, MorphLang.UA))
        OrgItemNameToken.__m_std_nouns = TerminCollection()
        for k in range(2):
            name = ("NameNouns_ru.dat" if k == 0 else "NameNouns_ua.dat")
            dat = EpNerOrgInternalResourceHelper.getBytes(name)
            if (dat is None): 
                raise Utils.newException("Can't file resource file {0} in Organization analyzer".format(name), None)
            str0_ = OrgItemTypeToken._deflate(dat).decode("UTF-8", 'ignore')
            for line0 in Utils.splitString(str0_, '\n', False): 
                line = line0.strip()
                if (Utils.isNullOrEmpty(line)): 
                    continue
                if (k == 0): 
                    OrgItemNameToken.__m_std_nouns.add(Termin(line))
                else: 
                    OrgItemNameToken.__m_std_nouns.add(Termin._new898(line, MorphLang.UA))
    
    @staticmethod
    def _new1696(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.is_ignored_part = _arg3
        return res
    
    @staticmethod
    def _new1700(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.value = _arg3
        return res
    
    @staticmethod
    def _new1701(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : bool) -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.value = _arg3
        res.is_denomination = _arg4
        return res
    
    @staticmethod
    def _new1702(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : bool, _arg5 : bool, _arg6 : 'MorphCollection') -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.value = _arg3
        res.is_std_tail = _arg4
        res.is_empty_word = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new1703(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : bool) -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.value = _arg3
        res.is_std_name = _arg4
        return res
    
    @staticmethod
    def _new1704(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : bool) -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.value = _arg3
        res.is_std_tail = _arg4
        return res
    
    @staticmethod
    def _new1705(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : str) -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.morph = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new1706(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'CharsInfo') -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.chars = _arg3
        return res
    
    @staticmethod
    def _new1710(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : str, _arg5 : 'CharsInfo') -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.morph = _arg3
        res.value = _arg4
        res.chars = _arg5
        return res
    
    @staticmethod
    def _new1711(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'CharsInfo', _arg4 : 'MorphCollection') -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.chars = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new1712(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'MorphCollection') -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.value = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new2216(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.is_std_name = _arg3
        return res
    
    @staticmethod
    def _new2218(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'CharsInfo') -> 'OrgItemNameToken':
        res = OrgItemNameToken(_arg1, _arg2)
        res.value = _arg3
        res.chars = _arg4
        return res
    
    # static constructor for class OrgItemNameToken
    @staticmethod
    def _static_ctor():
        OrgItemNameToken.__m_not_terminate_nouns = list(["РАБОТА", "ВОПРОС", "ДЕЛО", "УПРАВЛЕНИЕ", "ОРГАНИЗАЦИЯ", "ОБЕСПЕЧЕНИЕ", "РОБОТА", "ПИТАННЯ", "СПРАВА", "УПРАВЛІННЯ", "ОРГАНІЗАЦІЯ", "ЗАБЕЗПЕЧЕННЯ"])

OrgItemNameToken._static_ctor()