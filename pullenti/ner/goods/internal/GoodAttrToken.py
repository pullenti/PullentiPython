# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphCase import MorphCase
from pullenti.semantic.utils.DerivateService import DerivateService
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.VerbPhraseHelper import VerbPhraseHelper
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.measure.MeasureReferent import MeasureReferent
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
from pullenti.ner.Referent import Referent
from pullenti.ner.goods.GoodAttrType import GoodAttrType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.internal.RusLatAccord import RusLatAccord
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.goods.GoodAttributeReferent import GoodAttributeReferent
from pullenti.ner.denomination.DenominationAnalyzer import DenominationAnalyzer
from pullenti.ner.uri.UriReferent import UriReferent
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.denomination.DenominationReferent import DenominationReferent
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.measure.internal.MeasureToken import MeasureToken

class GoodAttrToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.typ = GoodAttrType.UNDEFINED
        self.value = None;
        self.alt_value = None;
        self.name = None;
        self.ref = None;
        self.ref_tok = None;
    
    def __str__(self) -> str:
        return "{0}: {1}{2} {3}".format(Utils.enumToString(self.typ), self.value, ("" if self.alt_value is None else " / {0}".format(self.alt_value)), ("" if self.ref is None else str(self.ref)))
    
    def _create_attr(self) -> 'GoodAttributeReferent':
        if (isinstance(self.ref, GoodAttributeReferent)): 
            return Utils.asObjectOrNull(self.ref, GoodAttributeReferent)
        ar = GoodAttributeReferent()
        if (self.typ != GoodAttrType.UNDEFINED): 
            ar.typ = self.typ
        if (self.name is not None): 
            ar.add_slot(GoodAttributeReferent.ATTR_NAME, self.name, False, 0)
        if (self.ref is not None): 
            ar.add_slot(GoodAttributeReferent.ATTR_REF, self.ref, True, 0)
        elif (self.ref_tok is not None): 
            ar.add_slot(GoodAttributeReferent.ATTR_REF, self.ref_tok.referent, True, 0)
            ar.add_ext_referent(self.ref_tok)
        if (self.typ == GoodAttrType.NUMERIC): 
            pass
        vals = None
        vals = list()
        if (self.value is not None): 
            vals.append(self.value)
        if (self.alt_value is not None): 
            vals.append(self.alt_value)
        for v in vals: 
            v1 = v
            if (ar.typ == GoodAttrType.PROPER): 
                v1 = v.upper()
                if (v1.find('\'') >= 0): 
                    v1 = v1.replace("'", "")
            if (Utils.isNullOrEmpty(v1)): 
                continue
            ar.add_slot((GoodAttributeReferent.ATTR_VALUE if v == self.value else GoodAttributeReferent.ATTR_ALTVALUE), v1, False, 0)
            if ((len(v1) < 10) and LanguageHelper.is_latin_char(v1[0]) and ar.typ == GoodAttrType.PROPER): 
                rus = RusLatAccord.get_variants(v1)
                if (rus is None or len(rus) == 0): 
                    continue
                for vv in rus: 
                    if (ar.find_slot(None, vv, True) is None): 
                        ar.add_slot(GoodAttributeReferent.ATTR_ALTVALUE, vv, False, 0)
                        if (len(ar.slots) > 20): 
                            break
        if (ar.find_slot(GoodAttributeReferent.ATTR_VALUE, None, True) is None and ar.find_slot(GoodAttributeReferent.ATTR_REF, None, True) is None): 
            return None
        return ar
    
    @staticmethod
    def try_parse_list(t : 'Token') -> typing.List['ReferentToken']:
        if (t is None): 
            return None
        li = GoodAttrToken.__try_parse_list(t)
        if (li is None or len(li) == 0): 
            return None
        res = list()
        for a in li: 
            attr = a._create_attr()
            if (attr is not None): 
                res.append(ReferentToken(attr, a.begin_token, a.end_token))
        return res
    
    @staticmethod
    def __try_parse_list(t : 'Token') -> typing.List['GoodAttrToken']:
        res = list()
        key = None
        next_seq = False
        tt = t
        first_pass3670 = True
        while True:
            if first_pass3670: first_pass3670 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt != t and tt.is_newline_before): 
                break
            if (tt != t and MiscHelper.can_be_start_of_sentence(tt) and not tt.is_char('(')): 
                next_seq = True
                if (key is None): 
                    break
                re2 = GoodAttrToken.try_parse(tt, key, t != tt, False)
                if (re2 is not None and ((re2.typ == GoodAttrType.NUMERIC or re2.typ == GoodAttrType.MODEL))): 
                    pass
                elif (re2 is not None and ((re2.ref_tok is not None or re2.ref is not None))): 
                    next_seq = False
                elif ((tt.get_morph_class_in_dictionary().is_verb and re2 is not None and re2.typ == GoodAttrType.CHARACTER) and GoodAttrToken.__is_spec_verb(tt)): 
                    pass
                else: 
                    npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                    if (npt is None): 
                        break
                    noun = npt.noun.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                    if (key.value is None): 
                        if (key.ref is None): 
                            break
                        if (noun in str(key.ref).upper()): 
                            pass
                        else: 
                            break
                    elif (key.value in noun or noun in key.value): 
                        pass
                    else: 
                        break
            if ((isinstance(tt, TextToken)) and next_seq): 
                dc = tt.get_morph_class_in_dictionary()
                if (dc == MorphClass.VERB): 
                    if (not GoodAttrToken.__is_spec_verb(tt)): 
                        break
            if (tt.is_value("ДОЛЖЕН", None) or tt.is_value("ДОЛЖНА", None) or tt.is_value("ДОЛЖНО", None)): 
                if (tt.next0_ is not None and tt.next0_.get_morph_class_in_dictionary().is_verb): 
                    tt = tt.next0_
                continue
            re = GoodAttrToken.try_parse(tt, key, tt != t, False)
            if (re is not None): 
                if (key is None): 
                    if (re.typ == GoodAttrType.KEYWORD): 
                        key = re
                    elif (re.typ == GoodAttrType.NUMERIC or re.typ == GoodAttrType.MODEL): 
                        return None
                res.append(re)
                tt = re.end_token
                continue
            if ((isinstance(tt, TextToken)) and not tt.chars.is_letter): 
                continue
            if (tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction): 
                continue
            if (isinstance(tt, NumberToken)): 
                res.append(GoodAttrToken._new1275(tt, tt, tt.get_source_text()))
        if (len(res) > 0 and res[len(res) - 1].typ == GoodAttrType.CHARACTER): 
            if (res[len(res) - 1].end_token == res[len(res) - 1].begin_token and res[len(res) - 1].end_token.get_morph_class_in_dictionary().is_adverb): 
                del res[len(res) - 1]
        return res
    
    @staticmethod
    def __is_spec_verb(t : 'Token') -> bool:
        if (t is None): 
            return False
        if ((t.is_value("ПРИМЕНЯТЬ", None) or t.is_value("ИСПОЛЬЗОВАТЬ", None) or t.is_value("ИЗГОТАВЛИВАТЬ", None)) or t.is_value("ПРИМЕНЯТЬ", None) or t.is_value("ИЗГОТОВИТЬ", None)): 
            return True
        return False
    
    @staticmethod
    def try_parse(t : 'Token', key : 'GoodAttrToken', can_be_measure : bool, is_chars : bool=False) -> 'GoodAttrToken':
        res = GoodAttrToken.__try_parse_(t, key, can_be_measure, is_chars)
        if (res is None or res.value is None): 
            return res
        if ((res is not None and res.typ == GoodAttrType.CHARACTER and ((res.end_token == res.begin_token or (res.value.find(' ') < 0)))) and res.alt_value is None): 
            if (res.value == "ДЛЯ"): 
                return GoodAttrToken.try_parse(t.next0_, key, False, False)
            if (res.value is not None): 
                if (Utils.startsWithString(res.value, "ДВУ", True) and not Utils.startsWithString(res.value, "ДВУХ", True)): 
                    res.value = ("ДВУХ" + res.value[3:])
        if ((res is not None and res.typ == GoodAttrType.CHARACTER and res.begin_token.morph.class0_.is_preposition) and res.end_token != res.begin_token and res.alt_value is None): 
            npt = NounPhraseHelper.try_parse(res.begin_token.next0_, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None and npt.end_token == res.end_token): 
                res.alt_value = npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
        return res
    
    @staticmethod
    def __try_parse_(t : 'Token', key : 'GoodAttrToken', can_be_measure : bool, is_chars : bool) -> 'GoodAttrToken':
        if (t is None): 
            return None
        if (t.is_value("ПРЕДНАЗНАЧЕН", None)): 
            pass
        r = t.get_referent()
        if (r is not None): 
            if (r.type_name == "ORGANIZATION" or r.type_name == "GEO"): 
                return GoodAttrToken._new1276(t, t, GoodAttrType.REFERENT, r)
        if (can_be_measure): 
            res = GoodAttrToken.__try_parse_num(t)
            if ((res) is not None): 
                return res
        if (is_chars): 
            res = GoodAttrToken.__try_parse_chars(t)
            if ((res) is not None): 
                return res
        ms = MeasureToken.try_parse(t, None, True, False, False, False)
        if (ms is not None and ms.nums is not None): 
            nres = GoodAttrToken._new1277(t, ms.end_token, GoodAttrType.NUMERIC)
            nres.name = ms.name
            nres.value = ms.get_norm_values()
            return nres
        if (t.kit.ontology is not None): 
            li = t.kit.ontology.attach_token(GoodAttributeReferent.OBJ_TYPENAME, t)
            if (li is not None and li[0].item is not None and (isinstance(li[0].item.referent, GoodAttributeReferent))): 
                res = GoodAttrToken(li[0].begin_token, li[0].end_token)
                res.typ = li[0].item.referent.typ
                res.ref = li[0].item.referent.clone()
                return res
        tok = GoodAttrToken.__m_std_abbrs.try_parse(t, TerminParseAttr.NO)
        if ((tok) is not None): 
            ty = Utils.valToEnum(tok.termin.tag, GoodAttrType)
            if (ty == GoodAttrType.UNDEFINED and tok.termin.tag2 is not None): 
                tt2 = tok.end_token.next0_
                if (tt2 is not None and ((tt2.is_char(':') or tt2.is_hiphen))): 
                    tt2 = tt2.next0_
                res = GoodAttrToken.__try_parse_(tt2, key, False, is_chars)
                if (res is not None and ((res.typ == GoodAttrType.PROPER or res.typ == GoodAttrType.MODEL))): 
                    res.begin_token = t
                    res.name = tok.termin.canonic_text
                    return res
                tok2 = GoodAttrToken.__m_std_abbrs.try_parse(tt2, TerminParseAttr.NO)
                if (tok2 is not None and (Utils.asObjectOrNull(tok2.termin.tag2, str)) == "NO"): 
                    res = GoodAttrToken._new1277(t, tok2.end_token, GoodAttrType.UNDEFINED)
                    return res
                res = GoodAttrToken.__try_parse_model(tt2)
                if (res is not None): 
                    res.begin_token = t
                    res.name = tok.termin.canonic_text
                    return res
            if (ty != GoodAttrType.REFERENT): 
                res = GoodAttrToken._new1279(t, tok.end_token, ty, tok.termin.canonic_text, tok.morph)
                if (res.end_token.next0_ is not None and res.end_token.next0_.is_char('.')): 
                    res.end_token = res.end_token.next0_
                return res
            if (ty == GoodAttrType.REFERENT): 
                tt = tok.end_token.next0_
                first_pass3671 = True
                while True:
                    if first_pass3671: first_pass3671 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.is_newline_before): 
                        break
                    if (tt.is_hiphen or tt.is_char_of(":")): 
                        continue
                    if (tt.get_morph_class_in_dictionary().is_adverb): 
                        continue
                    tok2 = GoodAttrToken.__m_std_abbrs.try_parse(tt, TerminParseAttr.NO)
                    if (tok2 is not None): 
                        ty2 = Utils.valToEnum(tok2.termin.tag, GoodAttrType)
                        if (ty2 == GoodAttrType.REFERENT or ty2 == GoodAttrType.UNDEFINED): 
                            tt = tok2.end_token
                            continue
                    break
                if (tt is None): 
                    return None
                if (tt.get_referent() is not None): 
                    return GoodAttrToken._new1280(t, tt, tt.get_referent(), GoodAttrType.REFERENT)
                if ((isinstance(tt, TextToken)) and not tt.chars.is_all_lower and tt.chars.is_letter): 
                    rt = tt.kit.process_referent("ORGANIZATION", tt)
                    if (rt is not None): 
                        return GoodAttrToken._new1281(t, rt.end_token, rt, GoodAttrType.REFERENT)
                if (BracketHelper.can_be_start_of_sequence(tt, False, False)): 
                    rt = tt.kit.process_referent("ORGANIZATION", tt.next0_)
                    if (rt is not None): 
                        t1 = rt.end_token
                        if (BracketHelper.can_be_end_of_sequence(t1.next0_, False, None, False)): 
                            t1 = t1.next0_
                        return GoodAttrToken._new1281(t, t1, rt, GoodAttrType.REFERENT)
        if (t.is_value("КАТАЛОЖНЫЙ", None)): 
            tt = MiscHelper.check_number_prefix(t.next0_)
            if (tt is not None): 
                if (tt.is_char_of(":") or tt.is_hiphen): 
                    tt = tt.next0_
                res = GoodAttrToken.__try_parse_model(tt)
                if (res is not None): 
                    res.begin_token = t
                    res.name = "КАТАЛОЖНЫЙ НОМЕР"
                    return res
        if (t.is_value("ФАСОВКА", None) or t.is_value("УПАКОВКА", None)): 
            if (not (isinstance(t.previous, NumberToken))): 
                tt = t.next0_
                if (tt is not None): 
                    if (tt.is_char_of(":") or tt.is_hiphen): 
                        tt = tt.next0_
                if (tt is None): 
                    return None
                res = GoodAttrToken._new1283(t, tt, GoodAttrType.NUMERIC, "ФАСОВКА")
                et = None
                while tt is not None: 
                    if (tt.is_comma): 
                        break
                    if (MiscHelper.can_be_start_of_sentence(tt)): 
                        break
                    if ((isinstance(tt, TextToken)) and tt.chars.is_letter and not tt.chars.is_all_lower): 
                        break
                    et = tt
                    tt = tt.next0_
                if (et is not None): 
                    res.value = MiscHelper.get_text_value(res.end_token, et, GetTextAttr.KEEPREGISTER)
                    res.end_token = et
                return res
        if ((isinstance(t, ReferentToken)) and (((isinstance(t.get_referent(), UriReferent)) or t.get_referent().type_name == "DECREE"))): 
            res = GoodAttrToken._new1283(t, t, GoodAttrType.MODEL, "СПЕЦИФИКАЦИЯ")
            res.value = str(t.get_referent())
            return res
        if (key is None and not is_chars): 
            is_all_upper = True
            tt = t
            while tt is not None: 
                if (tt != t and tt.is_newline_before): 
                    break
                if (tt.chars.is_cyrillic_letter and not tt.chars.is_all_upper): 
                    is_all_upper = False
                    break
                tt = tt.next0_
            if ((((not t.chars.is_all_upper or is_all_upper)) and ((t.morph.class0_.is_noun or t.morph.class0_.is_undefined)) and t.chars.is_cyrillic_letter) and (isinstance(t, TextToken))): 
                if (t.is_value("СООТВЕТСТВИЕ", None)): 
                    tt1 = t.next0_
                    if (tt1 is not None and ((tt1.is_char(':') or tt1.is_hiphen))): 
                        tt1 = tt1.next0_
                    res = GoodAttrToken.__try_parse_(tt1, key, False, is_chars)
                    if (res is not None): 
                        res.begin_token = t
                    return res
                ok = True
                if (t.morph.class0_.is_adjective or t.morph.class0_.is_verb): 
                    npt1 = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSEVERBS, 0, None)
                    if (npt1 is not None and npt1.end_token != t and len(npt1.adjectives) > 0): 
                        ok = False
                if (ok): 
                    res = GoodAttrToken._new1285(t, t, GoodAttrType.KEYWORD, t.morph)
                    res.value = t.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                    if ((t.next0_ is not None and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, TextToken))) and ((t.next0_.next0_.chars.is_all_lower or t.next0_.next0_.chars == t.chars))): 
                        if (not t.is_whitespace_after and not t.next0_.is_whitespace_after): 
                            t = t.next0_.next0_
                            res.end_token = t
                            res.value = "{0}-{1}".format(res.value, t.term)
                    return res
        if ((t.is_whitespace_before and (isinstance(t, TextToken)) and t.chars.is_letter) and (t.length_char < 5) and not is_chars): 
            rt = GoodAttrToken.__m_denom_an.try_attach(t, False)
            if ((rt is None and t.whitespaces_after_count == 1 and (isinstance(t.next0_, NumberToken))) and (t.length_char < 3) and GoodAttrToken.__try_parse_num(t.next0_) is None): 
                rt = GoodAttrToken.__m_denom_an.try_attach(t, True)
            if (rt is not None): 
                res = GoodAttrToken._new1277(t, rt.end_token, GoodAttrType.MODEL)
                dr = Utils.asObjectOrNull(rt.referent, DenominationReferent)
                for s in dr.slots: 
                    if (s.type_name == DenominationReferent.ATTR_VALUE): 
                        if (res.value is None): 
                            res.value = (Utils.asObjectOrNull(s.value, str))
                        else: 
                            res.alt_value = (Utils.asObjectOrNull(s.value, str))
                return res
            if (not t.is_whitespace_after and (isinstance(t.next0_, NumberToken)) and GoodAttrToken.__try_parse_num(t.next0_) is None): 
                res = GoodAttrToken.__try_parse_model(t)
                return res
        if (t.chars.is_latin_letter and t.is_whitespace_before): 
            res = GoodAttrToken._new1277(t, t, GoodAttrType.PROPER)
            ttt = t.next0_
            while ttt is not None: 
                if (ttt.chars.is_latin_letter and ttt.chars == t.chars): 
                    res.end_token = ttt
                elif (((isinstance(ttt, TextToken)) and not ttt.is_letters and ttt.next0_ is not None) and ttt.next0_.chars.is_latin_letter): 
                    pass
                else: 
                    break
                ttt = ttt.next0_
            if (res.end_token.is_whitespace_after): 
                res.value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.NO)
                if (res.value.find(' ') > 0): 
                    res.alt_value = res.value.replace(" ", "")
                if (res.length_char < 2): 
                    return None
                return res
        pref = None
        t0 = t
        if (t.morph.class0_.is_preposition and t.next0_ is not None and t.next0_.chars.is_letter): 
            pref = t.get_normal_case_text(MorphClass.PREPOSITION, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
            t = t.next0_
            if ((t.is_comma_and and (isinstance(t.next0_, TextToken)) and t.next0_.morph.class0_.is_preposition) and t.next0_.next0_ is not None): 
                pref = "{0} И {1}".format(pref, t.next0_.get_normal_case_text(MorphClass.PREPOSITION, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
                t = t.next0_.next0_
        elif ((((((t.is_value("Д", None) or t.is_value("Б", None) or t.is_value("Н", None)) or t.is_value("H", None))) and t.next0_ is not None and t.next0_.is_char_of("\\/")) and not t.is_whitespace_after and not t.next0_.is_whitespace_after) and (isinstance(t.next0_.next0_, TextToken))): 
            pref = ("ДЛЯ" if t.is_value("Д", None) else (("БЕЗ" if t.is_value("Б", None) else "НЕ")))
            t = t.next0_.next0_
            if (pref == "НЕ"): 
                re = GoodAttrToken.__try_parse_(t, key, False, is_chars)
                if (re is not None and re.typ == GoodAttrType.CHARACTER and re.value is not None): 
                    re.begin_token = t0
                    re.value = ("НЕ" + re.value)
                    if (re.alt_value is not None): 
                        re.alt_value = ("НЕ" + re.alt_value)
                    return re
        if (pref is not None): 
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            if (npt is None and t.get_morph_class_in_dictionary().is_adverb): 
                npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None and ((npt.chars.is_all_lower or npt.chars.is_all_upper)) and npt.chars.is_cyrillic_letter): 
                re = GoodAttrToken._new1277(t0, npt.end_token, GoodAttrType.CHARACTER)
                cas = MorphCase()
                tt = npt.end_token.next0_
                while tt is not None: 
                    if (tt.is_newline_before or tt.is_char(';')): 
                        break
                    if (tt.is_comma_and and tt.next0_ is not None): 
                        tt = tt.next0_
                    npt1 = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.PARSEPREPOSITION, 0, None)
                    if (npt1 is None and tt.get_morph_class_in_dictionary().is_adverb): 
                        npt1 = NounPhraseHelper.try_parse(tt.next0_, NounPhraseParseAttr.NO, 0, None)
                    if (npt1 is None): 
                        break
                    if (npt1.chars != npt.chars): 
                        break
                    if (tt.previous.is_comma): 
                        if (not cas.is_undefined and ((cas) & npt1.morph.case_).is_undefined): 
                            break
                        re2 = GoodAttrToken.__try_parse_num(tt)
                        if (re2 is not None and re2.typ == GoodAttrType.NUMERIC): 
                            break
                    re.end_token = npt1.end_token
                    tt = re.end_token
                    cas = npt1.morph.case_
                    tt = tt.next0_
                re.value = MiscHelper.get_text_value(npt.begin_token, re.end_token, GetTextAttr.NO)
                if (npt.end_token == re.end_token and len(npt.adjectives) == 0): 
                    if (pref == "ДЛЯ" or pref == "ИЗ"): 
                        noun = npt.noun.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                        grs = DerivateService.find_derivates(noun, True, None)
                        if (grs is not None): 
                            for g in grs: 
                                if (re.alt_value is not None): 
                                    break
                                for v in g.words: 
                                    if (v.class0_.is_adjective): 
                                        re.alt_value = v.spelling
                                        break
                if (pref is not None): 
                    re.value = "{0} {1}".format(pref, re.value)
                return re
        if (t.chars.is_cyrillic_letter or (isinstance(t, NumberToken))): 
            npt1 = NounPhraseHelper.try_parse(t, Utils.valToEnum((NounPhraseParseAttr.ADJECTIVECANBELAST) | (NounPhraseParseAttr.PARSENUMERICASADJECTIVE), NounPhraseParseAttr), 0, None)
            if (npt1 is not None): 
                if (((npt1.noun.begin_token.is_value("СОРТ", None) or npt1.noun.begin_token.is_value("КЛАСС", None) or npt1.noun.begin_token.is_value("ГРУППА", None)) or npt1.noun.begin_token.is_value("КАТЕГОРИЯ", None) or npt1.noun.begin_token.is_value("ТИП", None)) or npt1.noun.begin_token.is_value("ПОДТИП", None)): 
                    res = GoodAttrToken._new1277(t, npt1.end_token, GoodAttrType.CHARACTER)
                    res.value = npt1.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                    if (res.begin_token == res.end_token): 
                        if (t.next0_ is not None and t.next0_.is_value("ВЫСШ", None)): 
                            res.value = (((("ВЫСШАЯ" if ((npt1.noun.begin_token.morph.gender) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED) else "ВЫСШИЙ "))) + res.value)
                            res.end_token = t.next0_
                            if (res.end_token.next0_ is not None and res.end_token.next0_.is_char('.')): 
                                res.end_token = res.end_token.next0_
                        elif (t.whitespaces_after_count < 2): 
                            if ((isinstance(t.next0_, NumberToken)) and t.next0_.int_value is not None): 
                                res.value = "{0} {1}".format(NumberHelper.get_number_adjective(t.next0_.int_value, (MorphGender.FEMINIE if ((npt1.morph.gender) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED) else MorphGender.MASCULINE), MorphNumber.SINGULAR), t.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False))
                                res.end_token = t.next0_
                            else: 
                                rom = NumberHelper.try_parse_roman(t.next0_)
                                if (rom is not None and rom.int_value is not None): 
                                    res.value = "{0} {1}".format(NumberHelper.get_number_adjective(rom.int_value, (MorphGender.FEMINIE if ((npt1.morph.gender) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED) else MorphGender.MASCULINE), MorphNumber.SINGULAR), t.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False))
                                    res.end_token = rom.end_token
                    if (res.begin_token != res.end_token): 
                        return res
            if (((isinstance(t, NumberToken)) and t.int_value is not None and t.typ == NumberSpellingType.DIGIT) and (isinstance(t.next0_, TextToken)) and (t.whitespaces_after_count < 2)): 
                if (((t.next0_.is_value("СОРТ", None) or t.next0_.is_value("КЛАСС", None) or t.next0_.is_value("ГРУППА", None)) or t.next0_.is_value("КАТЕГОРИЯ", None) or t.next0_.is_value("ТИП", None)) or t.next0_.is_value("ПОДТИП", None)): 
                    res = GoodAttrToken._new1277(t, t.next0_, GoodAttrType.CHARACTER)
                    res.value = "{0} {1}".format(NumberHelper.get_number_adjective(t.int_value, (MorphGender.FEMINIE if ((t.next0_.morph.gender) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED) else MorphGender.MASCULINE), MorphNumber.SINGULAR), t.next0_.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False))
                    return res
            if (npt1 is not None and npt1.noun.begin_token.is_value("ХАРАКТЕРИСТИКА", None)): 
                t11 = npt1.end_token.next0_
                if (t11 is not None and ((t11.is_value("УКАЗАТЬ", None) or t11.is_value("УКАЗЫВАТЬ", None)))): 
                    res = GoodAttrToken._new1277(t, t11, GoodAttrType.UNDEFINED)
                    npt2 = NounPhraseHelper.try_parse(t11.next0_, NounPhraseParseAttr.PARSEPREPOSITION, 0, None)
                    if (npt2 is not None): 
                        res.end_token = npt2.end_token
                    elif (t11.next0_ is not None and t11.next0_.is_value("В", None)): 
                        res.end_token = t11.next0_
                        if (res.end_token.next0_ is not None): 
                            res.end_token = res.end_token.next0_
                    return res
        if ((t.chars.is_cyrillic_letter and pref is None and (isinstance(t, TextToken))) and t.morph.class0_.is_adjective): 
            if (t.morph.contains_attr("к.ф.", None) and t.next0_ is not None and t.next0_.is_hiphen): 
                val = t.term
                tt = t.next0_.next0_
                while tt is not None: 
                    if (((isinstance(tt, TextToken)) and tt.next0_ is not None and tt.next0_.is_hiphen) and (isinstance(tt.next0_.next0_, TextToken))): 
                        val = "{0}-{1}".format(val, tt.term)
                        tt = tt.next0_.next0_
                        continue
                    re = GoodAttrToken.__try_parse_(tt, key, False, is_chars)
                    if (re is not None and re.typ == GoodAttrType.CHARACTER): 
                        re.begin_token = t
                        re.value = "{0}-{1}".format(val, re.value)
                        return re
                    break
            is_char_ = False
            if (key is not None and t.morph.check_accord(key.morph, False, False) and ((t.chars.is_all_lower or MiscHelper.can_be_start_of_sentence(t)))): 
                is_char_ = True
            elif (t.get_morph_class_in_dictionary().is_adjective and not t.morph.contains_attr("неизм.", None)): 
                is_char_ = True
            if (is_char_ and t.morph.class0_.is_verb): 
                if ((t.is_value("ПРЕДНАЗНАЧИТЬ", None) or t.is_value("ПРЕДНАЗНАЧАТЬ", None) or t.is_value("ИЗГОТОВИТЬ", None)) or t.is_value("ИЗГОТОВЛЯТЬ", None)): 
                    is_char_ = False
            if (is_char_): 
                res = GoodAttrToken._new1277(t, t, GoodAttrType.CHARACTER)
                res.value = t.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, MorphGender.MASCULINE, False)
                return res
        if ((t.chars.is_cyrillic_letter and pref is None and (isinstance(t, TextToken))) and t.morph.class0_.is_verb): 
            re = GoodAttrToken.__try_parse_(t.next0_, key, False, is_chars)
            if (re is not None and re.typ == GoodAttrType.CHARACTER): 
                re.begin_token = t
                re.alt_value = "{0} {1}".format(t.term, re.value)
                return re
        if (t.chars.is_cyrillic_letter): 
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSEVERBS, 0, None)
            if ((npt is not None and len(npt.adjectives) > 0 and npt.adjectives[0].chars.is_all_lower) and not npt.noun.chars.is_all_lower): 
                npt = (None)
            if (pref is None and npt is not None and npt.noun.end_token.get_morph_class_in_dictionary().is_adjective): 
                npt = (None)
            if (npt is not None and not npt.end_token.chars.is_cyrillic_letter): 
                npt = (None)
            if (npt is not None): 
                is_prop = False
                if (pref is not None): 
                    is_prop = True
                elif (npt.chars.is_all_lower): 
                    is_prop = True
                if (len(npt.adjectives) > 0 and pref is None): 
                    if (key is None): 
                        return GoodAttrToken._new1293(t0, npt.adjectives[0].end_token, GoodAttrType.CHARACTER, npt.adjectives[0].get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, MorphGender.MASCULINE, False))
                if (pref is None and key is not None and npt.noun.is_value(key.value, None)): 
                    if (len(npt.adjectives) == 0): 
                        return GoodAttrToken._new1279(t0, npt.end_token, GoodAttrType.KEYWORD, npt.noun.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False), npt.morph)
                    return GoodAttrToken._new1293(t0, npt.adjectives[0].end_token, GoodAttrType.CHARACTER, npt.adjectives[0].get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, MorphGender.MASCULINE, False))
                if (is_prop): 
                    res = GoodAttrToken._new1277(t0, npt.end_token, GoodAttrType.CHARACTER)
                    res.value = npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                    return res
                if (not npt.chars.is_all_lower): 
                    return GoodAttrToken._new1279(t0, npt.end_token, GoodAttrType.PROPER, npt.get_source_text(), npt.morph)
            if (isinstance(t, TextToken)): 
                if (((t.get_morph_class_in_dictionary().is_adjective or t.morph.class0_ == MorphClass.ADJECTIVE)) and pref is None): 
                    return GoodAttrToken._new1279(t0, t, GoodAttrType.CHARACTER, t.lemma, t.morph)
            if ((isinstance(t, NumberToken)) and pref is not None): 
                num = GoodAttrToken.__try_parse_num(t)
                if (num is not None): 
                    num.begin_token = t0
                    return num
            if (pref is not None and t.morph.class0_.is_adjective and (isinstance(t, TextToken))): 
                res = GoodAttrToken._new1277(t0, t, GoodAttrType.CHARACTER)
                res.value = t.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, MorphGender.MASCULINE, False)
                return res
            if (pref is not None and t.next0_ is not None and t.next0_.is_value("WC", None)): 
                return GoodAttrToken._new1293(t, t.next0_, GoodAttrType.CHARACTER, "туалет")
            if (pref is not None): 
                return None
        if (t is not None and t.is_value("№", None) and (isinstance(t.next0_, NumberToken))): 
            return GoodAttrToken._new1293(t, t.next0_, GoodAttrType.MODEL, "№{0}".format(t.next0_.value))
        if ((isinstance(t, TextToken)) and t.chars.is_letter): 
            if (t.length_char > 2 and ((not t.chars.is_all_lower or t.chars.is_latin_letter))): 
                return GoodAttrToken._new1293(t, t, GoodAttrType.PROPER, t.term)
            return None
        if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                res1 = GoodAttrToken.__try_parse_(t.next0_, key, False, is_chars)
                if (res1 is not None and res1.end_token.next0_ == br.end_token): 
                    if (res1.typ == GoodAttrType.CHARACTER): 
                        res1.typ = GoodAttrType.PROPER
                    res1.begin_token = t
                    res1.end_token = br.end_token
                else: 
                    res1 = GoodAttrToken._new1277(br.begin_token, br.end_token, GoodAttrType.PROPER)
                    res1.value = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                return res1
        if (t.is_char('(')): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                if (t.next0_.is_value("ПРИЛОЖЕНИЕ", None)): 
                    return GoodAttrToken._new1277(t, br.end_token, GoodAttrType.UNDEFINED)
        nnn = GoodAttrToken.__try_parse_num2(t)
        if (nnn is not None): 
            return nnn
        return None
    
    @staticmethod
    def __try_parse_model(t : 'Token') -> 'GoodAttrToken':
        if (t is None): 
            return None
        res = GoodAttrToken._new1277(t, t, GoodAttrType.MODEL)
        tmp = io.StringIO()
        tt = t
        first_pass3672 = True
        while True:
            if first_pass3672: first_pass3672 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_whitespace_before and tt != t): 
                break
            if (isinstance(tt, NumberToken)): 
                if (tmp.tell() > 0 and str.isdigit(Utils.getCharAtStringIO(tmp, tmp.tell() - 1))): 
                    print('-', end="", file=tmp)
                print(tt.get_source_text(), end="", file=tmp)
                res.end_token = tt
                continue
            if (isinstance(tt, ReferentToken)): 
                den = Utils.asObjectOrNull(tt.get_referent(), DenominationReferent)
                if (den is not None): 
                    print(den.value, end="", file=tmp)
                    continue
            if (not (isinstance(tt, TextToken))): 
                break
            if (not tt.chars.is_letter): 
                if (tt.is_char_of("\\/-:")): 
                    if (tt.is_char_of(":") and tt.is_whitespace_after): 
                        break
                    print('-', end="", file=tmp)
                elif (tt.is_char('.')): 
                    if (tt.is_whitespace_after): 
                        break
                    print('.', end="", file=tmp)
                else: 
                    break
            else: 
                print(tt.term, end="", file=tmp)
            res.end_token = tt
        res.value = Utils.toStringStringIO(tmp)
        return res
    
    @staticmethod
    def __try_parse_num(t : 'Token') -> 'GoodAttrToken':
        if (t is None): 
            return None
        mt = MeasureToken.try_parse(t, None, True, False, False, False)
        if (mt is None): 
            mt = MeasureToken.try_parse_minimal(t, None, False)
        if (mt is not None): 
            mrs = mt.create_refenets_tokens_with_register(None, False)
            if (mrs is not None and len(mrs) > 0 and (isinstance(mrs[len(mrs) - 1].referent, MeasureReferent))): 
                mr = Utils.asObjectOrNull(mrs[len(mrs) - 1].referent, MeasureReferent)
                res = GoodAttrToken._new1283(t, mt.end_token, GoodAttrType.NUMERIC, mr.get_string_value(MeasureReferent.ATTR_NAME))
                res.value = mr.to_string(True, None, 0)
                return res
        mts = NumbersWithUnitToken.try_parse_multi(t, None, False, False, False, False)
        if ((mts is not None and len(mts) == 1 and mts[0].units is not None) and len(mts[0].units) > 0): 
            mrs = mts[0].create_refenets_tokens_with_register(None, None, True)
            mr = mrs[len(mrs) - 1]
            res = GoodAttrToken._new1277(t, mr.end_token, GoodAttrType.NUMERIC)
            res.value = mr.referent.to_string(True, None, 0)
            return res
        return None
    
    @staticmethod
    def __try_parse_num2(t : 'Token') -> 'GoodAttrToken':
        if (not (isinstance(t, NumberToken)) or t.int_value is None): 
            return None
        tok = GoodAttrToken.__m_num_suff.try_parse(t.next0_, TerminParseAttr.NO)
        if (tok is not None and (t.whitespaces_after_count < 3)): 
            res = GoodAttrToken._new1277(t, tok.end_token, GoodAttrType.NUMERIC)
            res.value = (t.value + tok.termin.canonic_text.lower())
            if (res.end_token.next0_ is not None and res.end_token.next0_.is_char('.')): 
                res.end_token = res.end_token.next0_
            return res
        num = NumberHelper.try_parse_real_number(t, True, False)
        if (num is not None): 
            tt = num.end_token
            if (isinstance(tt, MetaToken)): 
                if (tt.end_token.is_value("СП", None)): 
                    if (num.value == "1"): 
                        return GoodAttrToken._new1293(t, tt, GoodAttrType.CHARACTER, "односпальный")
                    if (num.value == "1.5"): 
                        return GoodAttrToken._new1293(t, tt, GoodAttrType.CHARACTER, "полутораспальный")
                    if (num.value == "2"): 
                        return GoodAttrToken._new1293(t, tt, GoodAttrType.CHARACTER, "вдухспальный")
            tt = tt.next0_
            if (tt is not None and tt.is_hiphen): 
                tt = tt.next0_
            if (tt is not None and tt.is_value("СП", None)): 
                if (num.value == "1"): 
                    return GoodAttrToken._new1293(t, tt, GoodAttrType.CHARACTER, "односпальный")
                if (num.value == "1.5"): 
                    return GoodAttrToken._new1293(t, tt, GoodAttrType.CHARACTER, "полутораспальный")
                if (num.value == "2"): 
                    return GoodAttrToken._new1293(t, tt, GoodAttrType.CHARACTER, "вдухспальный")
            return GoodAttrToken._new1293(t, num.end_token, GoodAttrType.NUMERIC, num.value)
        return None
    
    @staticmethod
    def __try_parse_chars(t : 'Token') -> 'GoodAttrToken':
        if (t is None): 
            return None
        t1 = None
        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
        if (npt is not None): 
            t1 = npt.end_token
        elif (((isinstance(t, TextToken)) and t.length_char > 2 and t.get_morph_class_in_dictionary().is_undefined) and not t.chars.is_all_lower): 
            t1 = t
        if (t1 is None): 
            return None
        t11 = t1
        t2 = None
        tt = t1.next0_
        while tt is not None: 
            if (MiscHelper.can_be_start_of_sentence(tt) or tt.is_char(';')): 
                break
            if (tt.is_char(':') or tt.is_hiphen): 
                t2 = tt.next0_
                break
            if (tt.is_value("ДА", None) or tt.is_value("НЕТ", None)): 
                t2 = tt
                break
            vvv = VerbPhraseHelper.try_parse(tt, False, False, False)
            if (vvv is not None): 
                t2 = vvv.end_token.next0_
                break
            t1 = tt
            tt = tt.next0_
        if (t2 is None): 
            if (t11.next0_ is not None and t11.next0_.get_morph_class_in_dictionary().is_adjective and NounPhraseHelper.try_parse(t11.next0_, NounPhraseParseAttr.NO, 0, None) is None): 
                t1 = t11
                t2 = t11.next0_
        if (t2 is None): 
            return None
        t3 = t2
        tt = t2
        while tt is not None: 
            if (MiscHelper.can_be_start_of_sentence(tt)): 
                break
            if (tt.is_char(';')): 
                break
            t3 = tt
            tt = tt.next0_
        name_ = MiscHelper.get_text_value(t, t1, GetTextAttr.NO)
        val = MiscHelper.get_text_value(t2, (t3.previous if t3.is_char('.') else t3), GetTextAttr.NO)
        if (Utils.isNullOrEmpty(val)): 
            return None
        return GoodAttrToken._new1316(t, t3, GoodAttrType.CHARACTER, name_, val)
    
    __m_num_suff = None
    
    __m_std_abbrs = None
    
    __m_denom_an = None
    
    __m_inited = False
    
    @staticmethod
    def initialize() -> None:
        if (GoodAttrToken.__m_inited): 
            return
        GoodAttrToken.__m_inited = True
        t = Termin("ПР")
        t.add_variant("ПРЕДМЕТ", False)
        GoodAttrToken.__m_num_suff.add(t)
        t = Termin("ШТ")
        t.add_variant("ШТУКА", False)
        GoodAttrToken.__m_num_suff.add(t)
        t = Termin("УП")
        t.add_variant("УПАКОВКА", False)
        GoodAttrToken.__m_num_suff.add(t)
        t = Termin("ЯЩ")
        t.add_variant("ЯЩИК", False)
        GoodAttrToken.__m_num_suff.add(t)
        t = Termin("КОРОБ")
        t.add_variant("КОРОБКА", False)
        GoodAttrToken.__m_num_suff.add(t)
        t = Termin("БУТ")
        t.add_variant("БУТЫЛКА", False)
        GoodAttrToken.__m_num_suff.add(t)
        t = Termin("МЕШ")
        t.add_variant("МЕШОК", False)
        GoodAttrToken.__m_num_suff.add(t)
        t = Termin._new100("ЕРШ", GoodAttrType.KEYWORD)
        t.add_variant("ЕРШИК", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("КОНДИЦИОНЕР", GoodAttrType.KEYWORD)
        t.add_variant("КОНДИЦ", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("УДЛИНИТЕЛЬ", GoodAttrType.KEYWORD)
        t.add_abridge("УДЛ-ЛЬ")
        t.add_abridge("УДЛИН-ЛЬ")
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("УСТРОЙСТВО", GoodAttrType.KEYWORD)
        t.add_abridge("УСТР-ВО")
        t.add_abridge("УСТР.")
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("ПРОКЛАДКИ", GoodAttrType.KEYWORD)
        t.add_variant("ПРОКЛ", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("ДЕЗОДОРАНТ", GoodAttrType.KEYWORD)
        t.add_variant("ДЕЗ", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("ОХЛАЖДЕННЫЙ", GoodAttrType.CHARACTER)
        t.add_variant("ОХЛ", False)
        t.add_variant("ОХЛАЖД", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("МЕДИЦИНСКИЙ", GoodAttrType.CHARACTER)
        t.add_variant("МЕД", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("СТЕРИЛЬНЫЙ", GoodAttrType.CHARACTER)
        t.add_variant("СТЕР", False)
        t.add_variant("СТ", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("ХЛОПЧАТОБУМАЖНЫЙ", GoodAttrType.CHARACTER)
        t.add_abridge("Х/Б")
        t.add_abridge("ХБ")
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("ДЕТСКИЙ", GoodAttrType.CHARACTER)
        t.add_variant("ДЕТ", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("МУЖСКОЙ", GoodAttrType.CHARACTER)
        t.add_variant("МУЖ", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("ЖЕНСКИЙ", GoodAttrType.CHARACTER)
        t.add_variant("ЖЕН", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("СТРАНА", GoodAttrType.REFERENT)
        t.add_variant("СТРАНА ПРОИСХОЖДЕНИЯ", False)
        t.add_variant("ПРОИСХОЖДЕНИЕ", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("ПРОИЗВОДИТЕЛЬ", GoodAttrType.REFERENT)
        t.add_abridge("ПР-ЛЬ")
        t.add_abridge("ПРОИЗВ-ЛЬ")
        t.add_abridge("ПРОИЗВ.")
        t.add_variant("ПРОИЗВОДСТВО", False)
        t.add_abridge("ПР-ВО")
        t.add_variant("ПРОИЗВЕСТИ", False)
        t.add_variant("КОМПАНИЯ", False)
        t.add_variant("ФИРМА", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new102("ТОВАРНЫЙ ЗНАК", GoodAttrType.UNDEFINED, "")
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new102("КАТАЛОЖНЫЙ НОМЕР", GoodAttrType.UNDEFINED, "")
        t.add_variant("НОМЕР В КАТАЛОГЕ", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new102("МАРКА", GoodAttrType.UNDEFINED, "")
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new102("ФИРМА", GoodAttrType.UNDEFINED, "")
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new102("МОДЕЛЬ", GoodAttrType.UNDEFINED, "")
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new102("НЕТ", GoodAttrType.UNDEFINED, "NO")
        t.add_variant("ОТСУТСТВОВАТЬ", False)
        t.add_variant("НЕ ИМЕТЬ", False)
        GoodAttrToken.__m_std_abbrs.add(t)
        t = Termin._new100("БОЛЕЕ", GoodAttrType.UNDEFINED)
        t.add_variant("МЕНЕЕ", False)
        t.add_variant("НЕ БОЛЕЕ", False)
        t.add_variant("НЕ МЕНЕЕ", False)
        GoodAttrToken.__m_std_abbrs.add(t)
    
    @staticmethod
    def _new1275(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'GoodAttrToken':
        res = GoodAttrToken(_arg1, _arg2)
        res.value = _arg3
        return res
    
    @staticmethod
    def _new1276(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'GoodAttrType', _arg4 : 'Referent') -> 'GoodAttrToken':
        res = GoodAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        return res
    
    @staticmethod
    def _new1277(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'GoodAttrType') -> 'GoodAttrToken':
        res = GoodAttrToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1279(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'GoodAttrType', _arg4 : str, _arg5 : 'MorphCollection') -> 'GoodAttrToken':
        res = GoodAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new1280(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Referent', _arg4 : 'GoodAttrType') -> 'GoodAttrToken':
        res = GoodAttrToken(_arg1, _arg2)
        res.ref = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new1281(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ReferentToken', _arg4 : 'GoodAttrType') -> 'GoodAttrToken':
        res = GoodAttrToken(_arg1, _arg2)
        res.ref_tok = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new1283(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'GoodAttrType', _arg4 : str) -> 'GoodAttrToken':
        res = GoodAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.name = _arg4
        return res
    
    @staticmethod
    def _new1285(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'GoodAttrType', _arg4 : 'MorphCollection') -> 'GoodAttrToken':
        res = GoodAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new1293(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'GoodAttrType', _arg4 : str) -> 'GoodAttrToken':
        res = GoodAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new1316(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'GoodAttrType', _arg4 : str, _arg5 : str) -> 'GoodAttrToken':
        res = GoodAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.name = _arg4
        res.value = _arg5
        return res
    
    # static constructor for class GoodAttrToken
    @staticmethod
    def _static_ctor():
        GoodAttrToken.__m_num_suff = TerminCollection()
        GoodAttrToken.__m_std_abbrs = TerminCollection()
        GoodAttrToken.__m_denom_an = DenominationAnalyzer()

GoodAttrToken._static_ctor()