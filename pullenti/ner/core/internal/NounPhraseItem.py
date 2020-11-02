# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.internal.NounPhraseItemTextVar import NounPhraseItemTextVar
from pullenti.ner.core.MiscHelper import MiscHelper

class NounPhraseItem(MetaToken):
    """ Элемент именной группы """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.conj_before = False
        self.adj_morph = list()
        self.can_be_adj = False
        self.noun_morph = list()
        self.can_be_noun = False
        self.multi_nouns = False
        self.can_be_surname = False
        self.is_std_adjective = False
        self.is_doubt_adjective = False
    
    @property
    def can_be_numeric_adj(self) -> bool:
        """ Это признак количественного (число, НЕСКОЛЬКО, МНОГО) """
        num = Utils.asObjectOrNull(self.begin_token, NumberToken)
        if (num is not None): 
            if (num.int_value is not None and num.int_value > 1): 
                return True
            else: 
                return False
        if ((self.begin_token.is_value("НЕСКОЛЬКО", None) or self.begin_token.is_value("МНОГО", None) or self.begin_token.is_value("ПАРА", None)) or self.begin_token.is_value("ПОЛТОРА", None)): 
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
            if (self.begin_token.is_value("ВСЕ", None) or self.begin_token.is_value("ВЕСЬ", None) or self.begin_token.is_value("САМ", None)): 
                return True
        return False
    
    def __corr_chars(self, str0_ : str, keep : bool) -> str:
        if (not keep): 
            return str0_
        if (self.chars.is_all_lower): 
            return str0_.lower()
        if (self.chars.is_capital_upper): 
            return MiscHelper.convert_first_char_upper_and_other_lower(str0_)
        return str0_
    
    def get_normal_case_text(self, mc : 'MorphClass'=None, num : 'MorphNumber'=MorphNumber.UNDEFINED, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        if ((isinstance(self.begin_token, ReferentToken)) and self.begin_token == self.end_token): 
            return self.begin_token.get_normal_case_text(mc, num, gender, keep_chars)
        res = None
        max_coef = 0
        def_coef = -1
        for it in self.morph.items: 
            v = Utils.asObjectOrNull(it, NounPhraseItemTextVar)
            if (v is None): 
                continue
            if (v.undef_coef > 0 and (((v.undef_coef < max_coef) or def_coef >= 0))): 
                continue
            if (num == MorphNumber.SINGULAR and v.single_number_value is not None): 
                if (mc is not None and ((gender == MorphGender.NEUTER or gender == MorphGender.FEMINIE)) and mc.is_adjective): 
                    bi = MorphBaseInfo._new401(MorphClass._new53(mc.value), gender, MorphNumber.SINGULAR, MorphCase.NOMINATIVE, self.morph.language)
                    str0_ = MorphologyService.get_wordform(v.single_number_value, bi)
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
                wrapval402 = RefOutArgWrapper(0)
                inoutres403 = Utils.tryParseInt(v.normal_value, wrapval402)
                val = wrapval402.value
                if (inoutres403): 
                    str0_ = NumberHelper.get_number_adjective(val, gender, (MorphNumber.SINGULAR if num == MorphNumber.SINGULAR or val == 1 else MorphNumber.PLURAL))
                    if (str0_ is not None): 
                        res = str0_
                        if (v.undef_coef == 0): 
                            break
                        max_coef = v.undef_coef
                        continue
            res1 = it.normal_value
            if (num == MorphNumber.SINGULAR): 
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
            elif (((isinstance(self.begin_token, TextToken)) and res1 == self.begin_token.term and it.case_.is_nominative) and it.number == MorphNumber.SINGULAR): 
                def_co = 1
            if (num == MorphNumber.PLURAL and ((v.number) & (MorphNumber.PLURAL)) == (MorphNumber.PLURAL)): 
                def_co += 3
            if (res is None or def_co > def_coef): 
                res = res1
                def_coef = def_co
                if (def_co > 0): 
                    break
        if (res is not None): 
            return self.__corr_chars(res, keep_chars)
        if (res is None and self.begin_token == self.end_token): 
            res = self.begin_token.get_normal_case_text(mc, num, gender, keep_chars)
        elif (res is None): 
            res = self.begin_token.get_normal_case_text(mc, num, gender, keep_chars)
            if (res is None): 
                res = MiscHelper.get_text_value_of_meta_token(self, (GetTextAttr.KEEPREGISTER if keep_chars else GetTextAttr.NO))
            else: 
                res = "{0} {1}".format(res, MiscHelper.get_text_value(self.begin_token.next0_, self.end_token, (GetTextAttr.KEEPREGISTER if keep_chars else GetTextAttr.NO)))
        return Utils.ifNotNull(res, "?")
    
    def is_value(self, term : str, term2 : str=None) -> bool:
        if (self.begin_token is not None): 
            return self.begin_token.is_value(term, term2)
        else: 
            return False
    
    @staticmethod
    def try_parse(t : 'Token', items : typing.List['NounPhraseItem'], attrs : 'NounPhraseParseAttr') -> 'NounPhraseItem':
        if (t is None): 
            return None
        t0 = t
        _can_be_surname = False
        _is_doubt_adj = False
        rt = Utils.asObjectOrNull(t, ReferentToken)
        if (rt is not None and rt.begin_token == rt.end_token and (isinstance(rt.begin_token, TextToken))): 
            res = NounPhraseItem.try_parse(rt.begin_token, items, attrs)
            if (res is not None): 
                res.begin_token = res.end_token = t
                res.can_be_noun = True
                return res
        if (rt is not None): 
            res = NounPhraseItem(t, t)
            for m in t.morph.items: 
                v = NounPhraseItemTextVar(m, None)
                v.normal_value = str(t.get_referent())
                res.noun_morph.append(v)
            res.can_be_noun = True
            return res
        if (isinstance(t, NumberToken)): 
            pass
        has_legal_verb = False
        if (isinstance(t, TextToken)): 
            if (not t.chars.is_letter): 
                return None
            str0_ = t.term
            if (str0_[len(str0_) - 1] == 'А' or str0_[len(str0_) - 1] == 'О'): 
                for wf in t.morph.items: 
                    if ((isinstance(wf, MorphWordForm)) and wf.is_in_dictionary): 
                        if (wf.class0_.is_verb): 
                            mc = t.get_morph_class_in_dictionary()
                            if (not mc.is_noun and (((attrs) & (NounPhraseParseAttr.IGNOREPARTICIPLES))) == (NounPhraseParseAttr.NO)): 
                                if (not LanguageHelper.ends_with_ex(str0_, "ОГО", "ЕГО", None, None)): 
                                    return None
                            has_legal_verb = True
                        if (wf.class0_.is_adverb): 
                            if (t.next0_ is None or not t.next0_.is_hiphen): 
                                if ((str0_ == "ВСЕГО" or str0_ == "ДОМА" or str0_ == "НЕСКОЛЬКО") or str0_ == "МНОГО" or str0_ == "ПОРЯДКА"): 
                                    pass
                                else: 
                                    return None
                        if (wf.class0_.is_adjective): 
                            if (wf.contains_attr("к.ф.", None)): 
                                if (t.get_morph_class_in_dictionary() == MorphClass.ADJECTIVE): 
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
                        if (LanguageHelper.ends_with_ex(s, "ИН", "ЕН", "ЫН", None)): 
                            if (not wff.is_in_dictionary): 
                                _can_be_surname = True
                            else: 
                                return None
                        if (wff.is_in_dictionary and LanguageHelper.ends_with(s, "ОВ")): 
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
                            if (mc0.is_adjective and t.morph.contains_attr("неизм.", None)): 
                                pass
                            elif ((((attrs) & (NounPhraseParseAttr.REFERENTCANBENOUN))) == (NounPhraseParseAttr.REFERENTCANBENOUN)): 
                                pass
                            else: 
                                if (items is None or (len(items) < 1)): 
                                    return None
                                if (not items[0].is_std_adjective): 
                                    return None
            if (mc0.is_adjective and t.morph.items_count == 1): 
                if (t.morph.get_indexer_item(0).contains_attr("в.ср.ст.", None)): 
                    return None
            mc1 = t.get_morph_class_in_dictionary()
            if (mc1 == MorphClass.VERB and t.morph.case_.is_undefined): 
                return None
            if (((((attrs) & (NounPhraseParseAttr.IGNOREPARTICIPLES))) == (NounPhraseParseAttr.IGNOREPARTICIPLES) and t.morph.class0_.is_verb and not t.morph.class0_.is_noun) and not t.morph.class0_.is_proper): 
                for wf in t.morph.items: 
                    if (wf.class0_.is_verb): 
                        if (wf.contains_attr("дейст.з.", None)): 
                            if (LanguageHelper.ends_with(t.term, "СЯ")): 
                                pass
                            else: 
                                return None
        t1 = None
        for k in range(2):
            t = (Utils.ifNotNull(t1, t0))
            if (k == 0): 
                if (((isinstance(t0, TextToken)) and t0.next0_ is not None and t0.next0_.is_hiphen) and t0.next0_.next0_ is not None): 
                    if (not t0.is_whitespace_after and not t0.morph.class0_.is_pronoun and not (isinstance(t0.next0_.next0_, NumberToken))): 
                        if (not t0.next0_.is_whitespace_after): 
                            t = t0.next0_.next0_
                        elif (t0.next0_.next0_.chars.is_all_lower and LanguageHelper.ends_with(t0.term, "О")): 
                            t = t0.next0_.next0_
            it = NounPhraseItem._new404(t0, t, _can_be_surname)
            if (t0 == t and (isinstance(t0, ReferentToken))): 
                it.can_be_noun = True
                it.morph = MorphCollection(t0.morph)
            can_be_prepos = False
            for v in t.morph.items: 
                wf = Utils.asObjectOrNull(v, MorphWordForm)
                if (v.class0_.is_verb and not v.case_.is_undefined): 
                    it.can_be_adj = True
                    it.adj_morph.append(NounPhraseItemTextVar(v, t))
                    continue
                if (v.class0_.is_preposition): 
                    can_be_prepos = True
                if (v.class0_.is_adjective or ((v.class0_.is_pronoun and not v.class0_.is_personal_pronoun and not v.contains_attr("неизм.", None))) or ((v.class0_.is_noun and (isinstance(t, NumberToken))))): 
                    if (NounPhraseItem.try_accord_variant(items, (0 if items is None else len(items)), v, False)): 
                        is_doub = False
                        if (v.contains_attr("к.ф.", None)): 
                            continue
                        if (v.contains_attr("собир.", None) and not (isinstance(t, NumberToken))): 
                            if (wf is not None and wf.is_in_dictionary): 
                                return None
                            continue
                        if (v.contains_attr("сравн.", None)): 
                            continue
                        ok = True
                        if (isinstance(t, TextToken)): 
                            s = t.term
                            if (s == "ПРАВО" or s == "ПРАВА"): 
                                ok = False
                            elif (LanguageHelper.ends_with(s, "ОВ") and t.get_morph_class_in_dictionary().is_noun): 
                                ok = False
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
                            if (wf is not None and wf.class0_.is_pronoun): 
                                it.can_be_noun = True
                                it.noun_morph.append(NounPhraseItemTextVar(v, t))
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
                                if (len(items) == 1 and not v.case_.is_nominative): 
                                    can_be_noun_ = True
                                else: 
                                    return None
                        if (len(items) == 1): 
                            if (items[0].can_be_adj_for_personal_pronoun): 
                                can_be_noun_ = True
                elif ((v.class0_.is_pronoun and ((items is None or len(items) == 0 or ((len(items) == 1 and items[0].can_be_adj_for_personal_pronoun)))) and wf is not None) and (((((wf.normal_case == "ТОТ" or wf.normal_full == "ТО" or wf.normal_case == "ТО") or wf.normal_case == "ЭТО" or wf.normal_case == "ВСЕ") or wf.normal_case == "ЧТО" or wf.normal_case == "КТО") or wf.normal_full == "КОТОРЫЙ" or wf.normal_case == "КОТОРЫЙ"))): 
                    if (wf.normal_case == "ВСЕ"): 
                        if (t.next0_ is not None and t.next0_.is_value("РАВНО", None)): 
                            return None
                    can_be_noun_ = True
                elif (wf is not None and ((Utils.ifNotNull(wf.normal_full, wf.normal_case))) == "КОТОРЫЙ" and (((attrs) & (NounPhraseParseAttr.PARSEPRONOUNS))) == (NounPhraseParseAttr.NO)): 
                    return None
                elif (v.class0_.is_proper and (isinstance(t, TextToken))): 
                    if (t.length_char > 4 or v.class0_.is_proper_name): 
                        can_be_noun_ = True
                if (can_be_noun_): 
                    added = False
                    if (items is not None and len(items) > 1 and (((attrs) & (NounPhraseParseAttr.MULTINOUNS))) != (NounPhraseParseAttr.NO)): 
                        ok1 = True
                        ii = 1
                        while ii < len(items): 
                            if (not items[ii].conj_before): 
                                ok1 = False
                                break
                            ii += 1
                        if (ok1): 
                            if (NounPhraseItem.try_accord_variant(items, (0 if items is None else len(items)), v, True)): 
                                it.noun_morph.append(NounPhraseItemTextVar(v, t))
                                it.can_be_noun = True
                                it.multi_nouns = True
                                added = True
                    if (not added): 
                        if (NounPhraseItem.try_accord_variant(items, (0 if items is None else len(items)), v, False)): 
                            it.noun_morph.append(NounPhraseItemTextVar(v, t))
                            it.can_be_noun = True
                            if (v.class0_.is_personal_pronoun and t.morph.contains_attr("неизм.", None) and not it.can_be_adj): 
                                itt = NounPhraseItemTextVar(v, t)
                                itt.case_ = MorphCase.ALL_CASES
                                itt.number = MorphNumber.UNDEFINED
                                if (itt.normal_value is None): 
                                    pass
                                it.adj_morph.append(itt)
                                it.can_be_adj = True
                        elif ((len(items) > 0 and len(items[0].adj_morph) > 0 and items[0].adj_morph[0].number == MorphNumber.PLURAL) and not ((items[0].adj_morph[0].case_) & v.case_).is_undefined and not items[0].adj_morph[0].class0_.is_verb): 
                            if (t.next0_ is not None and t.next0_.is_comma_and and (isinstance(t.next0_.next0_, TextToken))): 
                                npt2 = NounPhraseHelper.try_parse(t.next0_.next0_, attrs, 0, None)
                                if (npt2 is not None and npt2.preposition is None and not ((npt2.morph.case_) & v.case_ & items[0].adj_morph[0].case_).is_undefined): 
                                    it.noun_morph.append(NounPhraseItemTextVar(v, t))
                                    it.can_be_noun = True
            if (t0 != t): 
                for v in it.adj_morph: 
                    v.correct_prefix(Utils.asObjectOrNull(t0, TextToken), False)
                for v in it.noun_morph: 
                    v.correct_prefix(Utils.asObjectOrNull(t0, TextToken), True)
            if (k == 1 and it.can_be_noun and not it.can_be_adj): 
                if (t1 is not None): 
                    it.end_token = t1
                else: 
                    it.end_token = t0.next0_.next0_
                for v in it.noun_morph: 
                    if (v.normal_value is not None and (v.normal_value.find('-') < 0)): 
                        v.normal_value = "{0}-{1}".format(v.normal_value, it.end_token.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
            if (it.can_be_adj): 
                if (NounPhraseItem.__m_std_adjectives.try_parse(it.begin_token, TerminParseAttr.NO) is not None): 
                    it.is_std_adjective = True
            if (can_be_prepos and it.can_be_noun): 
                if (items is not None and len(items) > 0): 
                    npt1 = NounPhraseHelper.try_parse(t, Utils.valToEnum((NounPhraseParseAttr.PARSEPREPOSITION) | (NounPhraseParseAttr.PARSEPRONOUNS) | (NounPhraseParseAttr.PARSEVERBS), NounPhraseParseAttr), 0, None)
                    if (npt1 is not None and npt1.end_char > t.end_char): 
                        return None
                else: 
                    npt1 = NounPhraseHelper.try_parse(t.next0_, Utils.valToEnum((NounPhraseParseAttr.PARSEPRONOUNS) | (NounPhraseParseAttr.PARSEVERBS), NounPhraseParseAttr), 0, None)
                    if (npt1 is not None): 
                        mc = LanguageHelper.get_case_after_preposition(t.lemma)
                        if (not ((mc) & npt1.morph.case_).is_undefined): 
                            return None
            if (it.can_be_noun or it.can_be_adj or k == 1): 
                if (it.begin_token.morph.class0_.is_pronoun): 
                    tt2 = it.end_token.next0_
                    if ((tt2 is not None and tt2.is_hiphen and not tt2.is_whitespace_after) and not tt2.is_whitespace_before): 
                        tt2 = tt2.next0_
                    if (isinstance(tt2, TextToken)): 
                        ss = tt2.term
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
                if (t0.is_value("БИЗНЕС", None) and t0.next0_ is not None and t0.next0_.chars == t0.chars): 
                    t1 = t0.next0_
                    continue
                return it
        return None
    
    def try_accord_var(self, v : 'MorphBaseInfo', multinouns : bool=False) -> bool:
        for vv in self.adj_morph: 
            if (vv.check_accord(v, False, multinouns)): 
                if (multinouns): 
                    pass
                return True
            elif (vv.normal_value == "СКОЛЬКО"): 
                return True
        if (self.can_be_numeric_adj): 
            if (v.number == MorphNumber.PLURAL): 
                return True
            if (isinstance(self.begin_token, NumberToken)): 
                val = self.begin_token.int_value
                if (val is None): 
                    return False
                num = self.begin_token.value
                if (Utils.isNullOrEmpty(num)): 
                    return False
                dig = num[len(num) - 1]
                if ((((dig == '2' or dig == '3' or dig == '4')) and (val < 10)) or val > 20): 
                    if (v.case_.is_genitive): 
                        return True
            term = None
            if (isinstance(v, MorphWordForm)): 
                term = v.normal_case
            if (isinstance(v, NounPhraseItemTextVar)): 
                term = v.normal_value
            if (term == "ЛЕТ" or term == "ЧЕЛОВЕК"): 
                return True
        if (len(self.adj_morph) > 0 and self.begin_token.morph.class0_.is_personal_pronoun and self.begin_token.morph.contains_attr("3 л.", None)): 
            return True
        return False
    
    @staticmethod
    def try_accord_variant(items : typing.List['NounPhraseItem'], count : int, v : 'MorphBaseInfo', multinouns : bool=False) -> bool:
        if (items is None or len(items) == 0): 
            return True
        i = 0
        while i < count: 
            ok = items[i].try_accord_var(v, multinouns)
            if (not ok): 
                return False
            i += 1
        return True
    
    @staticmethod
    def try_accord_adj_and_noun(adj : 'NounPhraseItem', noun : 'NounPhraseItem') -> bool:
        for v in adj.adj_morph: 
            for vv in noun.noun_morph: 
                if (v.check_accord(vv, False, False)): 
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
    def _new404(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'NounPhraseItem':
        res = NounPhraseItem(_arg1, _arg2)
        res.can_be_surname = _arg3
        return res