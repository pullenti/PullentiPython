# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.Morphology import Morphology
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.internal.NounPhraseItemTextVar import NounPhraseItemTextVar

class NounPhraseItem(MetaToken):
    """ Элемент именной группы """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.conj_before = False
        self.adj_morph = list()
        self.can_be_adj = False
        self.noun_morph = list()
        self.can_be_noun = False
        self.can_be_surname = False
        self.is_std_adjective = False
        self.is_doubt_adjective = False
    
    @property
    def can_be_numeric_adj(self) -> bool:
        """ Это признак количественного (число, НЕСКОЛЬКО, МНОГО) """
        if (isinstance(self.begin_token, NumberToken)): 
            return (self.begin_token).value > (1)
        if ((self.begin_token.isValue("НЕСКОЛЬКО", None) or self.begin_token.isValue("МНОГО", None) or self.begin_token.isValue("ПАРА", None)) or self.begin_token.isValue("ПОЛТОРА", None)): 
            return True
        return False
    
    @property
    def is_pronoun(self) -> bool:
        return self.begin_token.morph.class0_.is_pronoun
    
    @property
    def is_personal_pronoun(self) -> bool:
        return self.begin_token.morph.class0_.is_personal_pronoun
    
    @property
    def is_verb(self) -> bool:
        """ Это признак причастия """
        return self.begin_token.morph.class0_.is_verb
    
    @property
    def is_adverb(self) -> bool:
        return self.begin_token.morph.class0_.is_adverb
    
    @property
    def can_be_adj_for_personal_pronoun(self) -> bool:
        if (self.is_pronoun and self.can_be_adj): 
            if (self.begin_token.isValue("ВСЕ", None) or self.begin_token.isValue("ВЕСЬ", None) or self.begin_token.isValue("САМ", None)): 
                return True
        return False
    
    def __corrChars(self, str0_ : str, keep : bool) -> str:
        if (not keep): 
            return str0_
        if (self.chars.is_all_lower): 
            return str0_.lower()
        if (self.chars.is_capital_upper): 
            return MiscHelper.convertFirstCharUpperAndOtherLower(str0_)
        return str0_
    
    def getNormalCaseText(self, mc : 'MorphClass'=None, single_number : bool=False, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        if ((isinstance(self.begin_token, ReferentToken)) and self.begin_token == self.end_token): 
            return self.begin_token.getNormalCaseText(mc, single_number, gender, keep_chars)
        res = None
        max_coef = 0
        def_coef = -1
        for it in self.morph.items: 
            v = Utils.asObjectOrNull(it, NounPhraseItemTextVar)
            if (v.undef_coef > 0 and (((v.undef_coef < max_coef) or def_coef >= 0))): 
                continue
            if (single_number and v.single_number_value is not None): 
                if (mc is not None and ((gender == MorphGender.NEUTER or gender == MorphGender.FEMINIE)) and mc.is_adjective): 
                    bi = MorphBaseInfo._new489(MorphClass(mc), gender, MorphNumber.SINGULAR, MorphCase.NOMINATIVE, self.morph.language)
                    str0_ = Morphology.getWordform(v.single_number_value, bi)
                    if (str0_ is not None): 
                        res = str0_
                else: 
                    res = v.single_number_value
                if (v.undef_coef == 0): 
                    break
                max_coef = v.undef_coef
                continue
            if (Utils.isNullOrEmpty(v.normal_value)): 
                continue
            if (str.isdigit(v.normal_value[0]) and mc is not None and mc.is_adjective): 
                wrapval490 = RefOutArgWrapper(0)
                inoutres491 = Utils.tryParseInt(v.normal_value, wrapval490)
                val = wrapval490.value
                if (inoutres491): 
                    str0_ = NumberHelper.getNumberAdjective(val, gender, (MorphNumber.SINGULAR if single_number else MorphNumber.PLURAL))
                    if (str0_ is not None): 
                        res = str0_
                        if (v.undef_coef == 0): 
                            break
                        max_coef = v.undef_coef
                        continue
            res1 = (it).normal_value
            if (single_number): 
                if (res1 == "ДЕТИ"): 
                    res1 = "РЕБЕНОК"
                elif (res1 == "ЛЮДИ"): 
                    res1 = "ЧЕЛОВЕК"
            max_coef = v.undef_coef
            if (v.undef_coef > 0): 
                res = res1
                continue
            def_co = 0
            if (mc is not None and mc.is_adjective and v.undef_coef == 0): 
                pass
            elif (((isinstance(self.begin_token, TextToken)) and res1 == (self.begin_token).term and it.case_.is_nominative) and it.number == MorphNumber.SINGULAR): 
                def_co = 1
            if (res is None or def_co > def_coef): 
                res = res1
                def_coef = def_co
                if (def_co > 0): 
                    break
        if (res is not None): 
            return self.__corrChars(res, keep_chars)
        if (res is None and self.begin_token == self.end_token): 
            res = self.begin_token.getNormalCaseText(mc, single_number, gender, keep_chars)
        return Utils.ifNotNull(res, "?")
    
    def isValue(self, term : str, term2 : str=None) -> bool:
        if (self.begin_token is not None): 
            return self.begin_token.isValue(term, term2)
        else: 
            return False
    
    @staticmethod
    def tryParse(t : 'Token', items : typing.List['NounPhraseItem'], attrs : 'NounPhraseParseAttr') -> 'NounPhraseItem':
        if (t is None): 
            return None
        t0 = t
        _can_be_surname = False
        _is_doubt_adj = False
        rt = Utils.asObjectOrNull(t, ReferentToken)
        if (rt is not None and rt.begin_token == rt.end_token): 
            res = NounPhraseItem.tryParse(rt.begin_token, items, attrs)
            if (res is not None): 
                res.begin_token = res.end_token = t
                return res
        if (rt is not None and items is not None and len(items) > 0): 
            res = NounPhraseItem(t, t)
            for m in t.morph.items: 
                v = NounPhraseItemTextVar(m, None)
                v.normal_value = str(t.getReferent())
                res.noun_morph.append(v)
            res.can_be_noun = True
            return res
        if (isinstance(t, NumberToken)): 
            pass
        has_legal_verb = False
        if (isinstance(t, TextToken)): 
            if (not t.chars.is_letter): 
                return None
            str0_ = (t).term
            if (str0_[len(str0_) - 1] == 'А' or str0_[len(str0_) - 1] == 'О'): 
                for wf in t.morph.items: 
                    if ((isinstance(wf, MorphWordForm)) and (wf).is_in_dictionary): 
                        if (wf.class0_.is_verb): 
                            mc = t.getMorphClassInDictionary()
                            if (not mc.is_noun and (((attrs) & (NounPhraseParseAttr.IGNOREPARTICIPLES))) == (NounPhraseParseAttr.NO)): 
                                if (not LanguageHelper.endsWithEx(str0_, "ОГО", "ЕГО", None, None)): 
                                    return None
                            has_legal_verb = True
                        if (wf.class0_.is_adverb): 
                            if (t.next0_ is None or not t.next0_.is_hiphen): 
                                if ((str0_ == "ВСЕГО" or str0_ == "ДОМА" or str0_ == "НЕСКОЛЬКО") or str0_ == "МНОГО" or str0_ == "ПОРЯДКА"): 
                                    pass
                                else: 
                                    return None
                        if (wf.class0_.is_adjective): 
                            if (wf.containsAttr("к.ф.", None)): 
                                if (t.getMorphClassInDictionary() == MorphClass.ADJECTIVE): 
                                    pass
                                else: 
                                    _is_doubt_adj = True
            mc0 = t.morph.class0_
            if (mc0.is_proper_surname and not t.chars.is_all_lower): 
                for wf in t.morph.items: 
                    if (wf.class0_.is_proper_surname and wf.number != MorphNumber.PLURAL): 
                        wff = Utils.asObjectOrNull(wf, MorphWordForm)
                        if (wff is None): 
                            continue
                        s = Utils.ifNotNull((Utils.ifNotNull(wff.normal_full, wff.normal_case)), "")
                        if (LanguageHelper.endsWithEx(s, "ИН", "ЕН", "ЫН", None)): 
                            if (not wff.is_in_dictionary): 
                                _can_be_surname = True
                            else: 
                                return None
                        if (wff.is_in_dictionary and LanguageHelper.endsWith(s, "ОВ")): 
                            _can_be_surname = True
            if (mc0.is_proper_name and not t.chars.is_all_lower): 
                for wff in t.morph.items: 
                    wf = Utils.asObjectOrNull(wff, MorphWordForm)
                    if (wf is None): 
                        continue
                    if (wf.normal_case == "ГОР"): 
                        continue
                    if (wf.class0_.is_proper_name and wf.is_in_dictionary): 
                        if (wf.normal_case is None or not wf.normal_case.startswith("ЛЮБ")): 
                            if (mc0.is_adjective and t.morph.containsAttr("неизм.", None)): 
                                pass
                            elif ((((attrs) & (NounPhraseParseAttr.REFERENTCANBENOUN))) == (NounPhraseParseAttr.REFERENTCANBENOUN)): 
                                pass
                            else: 
                                if (items is None or (len(items) < 1)): 
                                    return None
                                if (not items[0].is_std_adjective): 
                                    return None
            if (mc0.is_adjective and t.morph.items_count == 1): 
                if (t.morph.getIndexerItem(0).containsAttr("в.ср.ст.", None)): 
                    return None
            mc1 = t.getMorphClassInDictionary()
            if (mc1 == MorphClass.VERB): 
                return None
            if (((((attrs) & (NounPhraseParseAttr.IGNOREPARTICIPLES))) == (NounPhraseParseAttr.IGNOREPARTICIPLES) and t.morph.class0_.is_verb and not t.morph.class0_.is_noun) and not t.morph.class0_.is_proper): 
                for wf in t.morph.items: 
                    if (wf.class0_.is_verb): 
                        if (wf.containsAttr("дейст.з.", None)): 
                            if (LanguageHelper.endsWith((t).term, "СЯ")): 
                                pass
                            else: 
                                return None
        t1 = None
        for k in range(2):
            t = (Utils.ifNotNull(t1, t0))
            if (k == 0): 
                if ((((isinstance(t0, TextToken))) and t0.next0_ is not None and t0.next0_.is_hiphen) and t0.next0_.next0_ is not None): 
                    if (not t0.is_whitespace_after and not t0.morph.class0_.is_pronoun): 
                        if (not t0.next0_.is_whitespace_after): 
                            t = t0.next0_.next0_
                        elif (t0.next0_.next0_.chars.is_all_lower and LanguageHelper.endsWith((t0).term, "О")): 
                            t = t0.next0_.next0_
            it = NounPhraseItem._new492(t0, t, _can_be_surname)
            if (t0 == t and (isinstance(t0, ReferentToken))): 
                it.can_be_noun = True
                it.morph = MorphCollection(t0.morph)
            can_be_prepos = False
            for v in t.morph.items: 
                wf = Utils.asObjectOrNull(v, MorphWordForm)
                if (v.class0_.is_preposition): 
                    can_be_prepos = True
                if (v.class0_.is_adjective or ((v.class0_.is_pronoun and not v.class0_.is_personal_pronoun)) or ((v.class0_.is_noun and (isinstance(t, NumberToken))))): 
                    if (NounPhraseItem.tryAccordVariant(items, (0 if items is None else len(items)), v)): 
                        is_doub = False
                        if (v.containsAttr("к.ф.", None)): 
                            continue
                        if (v.containsAttr("собир.", None) and not ((isinstance(t, NumberToken)))): 
                            if (wf is not None and wf.is_in_dictionary): 
                                return None
                            continue
                        if (v.containsAttr("сравн.", None)): 
                            continue
                        ok = True
                        if (isinstance(t, TextToken)): 
                            s = (t).term
                            if (s == "ПРАВО" or s == "ПРАВА"): 
                                ok = False
                            elif (LanguageHelper.endsWith(s, "ОВ") and t.getMorphClassInDictionary().is_noun): 
                                ok = False
                            elif (wf is not None and ((wf.normal_case == "САМ" or wf.normal_case == "ТО"))): 
                                ok = True
                        elif (isinstance(t, NumberToken)): 
                            if (v.class0_.is_noun and t.morph.class0_.is_adjective): 
                                ok = False
                            elif (t.morph.class0_.is_noun and (((attrs) & (NounPhraseParseAttr.PARSENUMERICASADJECTIVE))) == (NounPhraseParseAttr.NO)): 
                                ok = False
                        if (ok): 
                            it.adj_morph.append(NounPhraseItemTextVar(v, t))
                            it.can_be_adj = True
                            if (_is_doubt_adj and t0 == t): 
                                it.is_doubt_adjective = True
                            if (has_legal_verb and wf is not None and wf.is_in_dictionary): 
                                it.can_be_noun = True
                can_be_noun_ = False
                if (isinstance(t, NumberToken)): 
                    pass
                elif (v.class0_.is_noun or ((wf is not None and wf.normal_case == "САМ"))): 
                    can_be_noun_ = True
                elif (v.class0_.is_personal_pronoun): 
                    if (items is None or len(items) == 0): 
                        can_be_noun_ = True
                    else: 
                        for it1 in items: 
                            if (it1.is_verb): 
                                return None
                        if (len(items) == 1): 
                            if (items[0].can_be_adj_for_personal_pronoun): 
                                can_be_noun_ = True
                elif ((v.class0_.is_pronoun and ((items is None or len(items) == 0 or ((len(items) == 1 and items[0].can_be_adj_for_personal_pronoun)))) and wf is not None) and ((((wf.normal_case == "ТОТ" or wf.normal_full == "ТО" or wf.normal_case == "ТО") or wf.normal_case == "ЭТО" or wf.normal_case == "ВСЕ") or wf.normal_case == "ЧТО" or wf.normal_case == "КТО"))): 
                    if (wf.normal_case == "ВСЕ"): 
                        if (t.next0_ is not None and t.next0_.isValue("РАВНО", None)): 
                            return None
                    can_be_noun_ = True
                elif (wf is not None and ((Utils.ifNotNull(wf.normal_full, wf.normal_case))) == "КОТОРЫЙ"): 
                    return None
                elif (v.class0_.is_proper and (isinstance(t, TextToken))): 
                    if (t.length_char > 4 or v.class0_.is_proper_name): 
                        can_be_noun_ = True
                if (can_be_noun_): 
                    if (NounPhraseItem.tryAccordVariant(items, (0 if items is None else len(items)), v)): 
                        it.noun_morph.append(NounPhraseItemTextVar(v, t))
                        it.can_be_noun = True
            if (t0 != t): 
                for v in it.adj_morph: 
                    v.correctPrefix(Utils.asObjectOrNull(t0, TextToken), False)
                for v in it.noun_morph: 
                    v.correctPrefix(Utils.asObjectOrNull(t0, TextToken), True)
            if (k == 1 and it.can_be_noun and not it.can_be_adj): 
                if (t1 is not None): 
                    it.end_token = t1
                else: 
                    it.end_token = t0.next0_.next0_
                for v in it.noun_morph: 
                    if (v.normal_value is not None and (v.normal_value.find('-') < 0)): 
                        v.normal_value = "{0}-{1}".format(v.normal_value, it.end_token.getNormalCaseText(None, False, MorphGender.UNDEFINED, False))
            if (it.can_be_surname and it.can_be_adj): 
                it.can_be_adj = False
            if (it.can_be_adj): 
                if (NounPhraseItem.__m_std_adjectives.tryParse(it.begin_token, TerminParseAttr.NO) is not None): 
                    it.is_std_adjective = True
            if (can_be_prepos and it.can_be_noun): 
                if (items is not None and len(items) > 0): 
                    npt1 = NounPhraseHelper.tryParse(t, Utils.valToEnum((NounPhraseParseAttr.PARSEPREPOSITION) | (NounPhraseParseAttr.PARSEPRONOUNS) | (NounPhraseParseAttr.PARSEVERBS), NounPhraseParseAttr), 0)
                    if (npt1 is not None and npt1.end_char > t.end_char): 
                        return None
                else: 
                    npt1 = NounPhraseHelper.tryParse(t.next0_, Utils.valToEnum((NounPhraseParseAttr.PARSEPRONOUNS) | (NounPhraseParseAttr.PARSEVERBS), NounPhraseParseAttr), 0)
                    if (npt1 is not None): 
                        mc = LanguageHelper.getCaseAfterPreposition((t).lemma)
                        if (not ((mc) & npt1.morph.case_).is_undefined): 
                            return None
            if (it.can_be_noun or it.can_be_adj or k == 1): 
                if (it.begin_token.morph.class0_.is_pronoun): 
                    tt2 = it.end_token.next0_
                    if ((tt2 is not None and tt2.is_hiphen and not tt2.is_whitespace_after) and not tt2.is_whitespace_before): 
                        tt2 = tt2.next0_
                    if (isinstance(tt2, TextToken)): 
                        ss = (tt2).term
                        if ((ss == "ЖЕ" or ss == "БЫ" or ss == "ЛИ") or ss == "Ж"): 
                            it.end_token = tt2
                        elif (ss == "НИБУДЬ" or ss == "ЛИБО" or (((ss == "ТО" and tt2.previous.is_hiphen)) and it.can_be_adj)): 
                            it.end_token = tt2
                            for m in it.adj_morph: 
                                m.normal_value = "{0}-{1}".format(m.normal_value, ss)
                                if (m.single_number_value is not None): 
                                    m.single_number_value = "{0}-{1}".format(m.single_number_value, ss)
                return it
            if (t0 == t): 
                if (t0.isValue("БИЗНЕС", None) and t0.next0_ is not None and t0.next0_.chars == t0.chars): 
                    t1 = t0.next0_
                    continue
                return it
        return None
    
    def tryAccordVar(self, v : 'MorphBaseInfo') -> bool:
        for vv in self.adj_morph: 
            if (vv.checkAccord(v, False)): 
                return True
        if (self.can_be_numeric_adj): 
            if (v.number == MorphNumber.PLURAL): 
                return True
            if (isinstance(self.begin_token, NumberToken)): 
                num = (self.begin_token).value
                dig = num % (10)
                if ((((dig == (2) or dig == (3) or dig == (4))) and (num < (10))) or num > (20)): 
                    if (v.case_.is_genitive): 
                        return True
            term = None
            if (isinstance(v, MorphWordForm)): 
                term = (v).normal_case
            if (isinstance(v, NounPhraseItemTextVar)): 
                term = (v).normal_value
            if (term == "ЛЕТ" or term == "ЧЕЛОВЕК"): 
                return True
        return False
    
    @staticmethod
    def tryAccordVariant(items : typing.List['NounPhraseItem'], count : int, v : 'MorphBaseInfo') -> bool:
        if (items is None or len(items) == 0): 
            return True
        i = 0
        while i < count: 
            ok = items[i].tryAccordVar(v)
            if (not ok): 
                return False
            i += 1
        return True
    
    @staticmethod
    def tryAccordAdjAndNoun(adj : 'NounPhraseItem', noun : 'NounPhraseItem') -> bool:
        for v in adj.adj_morph: 
            for vv in noun.noun_morph: 
                if (v.checkAccord(vv, False)): 
                    return True
        return False
    
    @staticmethod
    def _initialize() -> None:
        if (NounPhraseItem.__m_std_adjectives is not None): 
            return
        NounPhraseItem.__m_std_adjectives = TerminCollection()
        for s in ["СЕВЕРНЫЙ", "ЮЖНЫЙ", "ЗАПАДНЫЙ", "ВОСТОЧНЫЙ"]: 
            NounPhraseItem.__m_std_adjectives.add(Termin(s))
    
    __m_std_adjectives = None
    
    @staticmethod
    def _new492(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'NounPhraseItem':
        res = NounPhraseItem(_arg1, _arg2)
        res.can_be_surname = _arg3
        return res