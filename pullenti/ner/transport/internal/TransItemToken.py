# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from enum import IntEnum
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.Token import Token
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.transport.TransportKind import TransportKind
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.BracketHelper import BracketHelper

class TransItemToken(MetaToken):
    
    class Typs(IntEnum):
        NOUN = 0
        BRAND = 1
        MODEL = 2
        NUMBER = 3
        NAME = 4
        ORG = 5
        ROUTE = 6
        CLASS = 7
        DATE = 8
        GEO = 9
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    class TransTermin(Termin):
        
        def __init__(self, source : str, add_lemma_variant : bool=False) -> None:
            super().__init__(None, None, False)
            self.kind = TransportKind.UNDEFINED
            self.typ = TransItemToken.Typs.NOUN
            self.is_doubt = False
            self.init_by_normal_text(source, None)
        
        @staticmethod
        def _new2686(_arg1 : str, _arg2 : bool, _arg3 : 'Typs', _arg4 : 'TransportKind') -> 'TransTermin':
            res = TransItemToken.TransTermin(_arg1, _arg2)
            res.typ = _arg3
            res.kind = _arg4
            return res
        
        @staticmethod
        def _new2689(_arg1 : str, _arg2 : bool, _arg3 : 'Typs', _arg4 : str) -> 'TransTermin':
            res = TransItemToken.TransTermin(_arg1, _arg2)
            res.typ = _arg3
            res.acronym = _arg4
            return res
        
        @staticmethod
        def _new2690(_arg1 : str, _arg2 : bool, _arg3 : 'Typs', _arg4 : 'MorphLang') -> 'TransTermin':
            res = TransItemToken.TransTermin(_arg1, _arg2)
            res.typ = _arg3
            res.lang = _arg4
            return res
        
        @staticmethod
        def _new2691(_arg1 : str, _arg2 : bool, _arg3 : 'Typs') -> 'TransTermin':
            res = TransItemToken.TransTermin(_arg1, _arg2)
            res.typ = _arg3
            return res
        
        @staticmethod
        def _new2693(_arg1 : str, _arg2 : bool, _arg3 : 'Typs', _arg4 : 'MorphLang', _arg5 : 'TransportKind') -> 'TransTermin':
            res = TransItemToken.TransTermin(_arg1, _arg2)
            res.typ = _arg3
            res.lang = _arg4
            res.kind = _arg5
            return res
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = TransItemToken.Typs.NOUN
        self.value = None;
        self.alt_value = None;
        self.kind = TransportKind.UNDEFINED
        self.is_doubt = False
        self.is_after_conjunction = False
        self.state = None;
        self.ref = None;
        self.route_items = None;
    
    def __str__(self) -> str:
        return "{0}: {1} {2}".format(Utils.enumToString(self.typ), Utils.ifNotNull(self.value, (("" if self.ref is None else str(self.ref)))), Utils.ifNotNull(self.alt_value, ""))
    
    @staticmethod
    def try_parse_list(t : 'Token', max_count : int=10) -> typing.List['TransItemToken']:
        tr = TransItemToken.try_parse(t, None, False, False)
        if (tr is None): 
            return None
        if ((tr.typ == TransItemToken.Typs.ORG or tr.typ == TransItemToken.Typs.NUMBER or tr.typ == TransItemToken.Typs.CLASS) or tr.typ == TransItemToken.Typs.DATE): 
            return None
        tr0 = tr
        res = list()
        res.append(tr)
        t = tr.end_token.next0_
        if (tr.typ == TransItemToken.Typs.NOUN): 
            while t is not None: 
                if (t.is_char(':') or t.is_hiphen): 
                    pass
                else: 
                    break
                t = t.next0_
        and_conj = False
        brareg = False
        first_pass3893 = True
        while True:
            if first_pass3893: first_pass3893 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_count > 0 and len(res) >= max_count): 
                break
            if (tr0.typ == TransItemToken.Typs.NOUN or tr0.typ == TransItemToken.Typs.ORG): 
                if (t.is_hiphen and t.next0_ is not None): 
                    t = t.next0_
            tr = TransItemToken.try_parse(t, tr0, False, False)
            if (tr is None): 
                if (BracketHelper.can_be_end_of_sequence(t, True, None, False) and t.next0_ is not None): 
                    if (tr0.typ == TransItemToken.Typs.MODEL or tr0.typ == TransItemToken.Typs.BRAND): 
                        tt1 = t.next0_
                        if (tt1 is not None and tt1.is_comma): 
                            tt1 = tt1.next0_
                        tr = TransItemToken.try_parse(tt1, tr0, False, False)
            if (tr is None and (isinstance(t, ReferentToken))): 
                rt = Utils.asObjectOrNull(t, ReferentToken)
                if (rt.begin_token == rt.end_token and (isinstance(rt.begin_token, TextToken))): 
                    tr = TransItemToken.try_parse(rt.begin_token, tr0, False, False)
                    if (tr is not None and tr.begin_token == tr.end_token): 
                        tr.begin_token = tr.end_token = t
            if (tr is None and t.is_char('(')): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    brareg = True
                    tr = TransItemToken.try_parse(t.next0_, tr0, False, False)
                    if (tr is not None): 
                        if (tr.typ != TransItemToken.Typs.NUMBER and tr.typ != TransItemToken.Typs.GEO): 
                            tr = (None)
                        elif (tr.end_token.next0_ is not None): 
                            tr.begin_token = t
                            if (tr.end_token.next0_.is_char(')')): 
                                tr.end_token = tr.end_token.next0_
                                brareg = False
                    if (tr is None): 
                        tt = br.end_token.next0_
                        if (tt is not None and tt.is_comma): 
                            tt = tt.next0_
                        tr = TransItemToken.try_parse(tt, tr0, False, False)
                        if (tr is not None and tr.typ == TransItemToken.Typs.NUMBER): 
                            pass
                        else: 
                            tr = (None)
            if (tr is None and t.is_hiphen): 
                if (tr0.typ == TransItemToken.Typs.BRAND or tr0.typ == TransItemToken.Typs.MODEL): 
                    tr = TransItemToken.try_parse(t.next0_, tr0, False, False)
            if (tr is None and t.is_comma): 
                if (((tr0.typ == TransItemToken.Typs.NAME or tr0.typ == TransItemToken.Typs.BRAND or tr0.typ == TransItemToken.Typs.MODEL) or tr0.typ == TransItemToken.Typs.CLASS or tr0.typ == TransItemToken.Typs.DATE) or tr0.typ == TransItemToken.Typs.GEO): 
                    tr = TransItemToken.try_parse(t.next0_, tr0, True, False)
                    if (tr is not None): 
                        if (tr.typ == TransItemToken.Typs.NUMBER): 
                            pass
                        else: 
                            tr = (None)
            if (tr is None): 
                if (tr0.typ == TransItemToken.Typs.NAME): 
                    if (t.is_char(',')): 
                        tr = TransItemToken.try_parse(t.next0_, tr0, True, False)
                    elif (t.morph.class0_.is_conjunction and t.is_and): 
                        tr = TransItemToken.try_parse(t.next0_, tr0, True, False)
                        and_conj = True
                if (tr is not None): 
                    if (tr.typ != TransItemToken.Typs.NAME): 
                        break
                    tr.is_after_conjunction = True
            if (t.is_comma_and and tr is None): 
                ne = TransItemToken.try_parse(t.next0_, tr0, True, False)
                if (ne is not None and ne.typ == TransItemToken.Typs.NUMBER): 
                    exi = False
                    for v in res: 
                        if (v.typ == ne.typ): 
                            exi = True
                            break
                    if (not exi): 
                        tr = ne
            if (tr is None and brareg and t.is_char(')')): 
                brareg = False
                tr0.end_token = t
                continue
            if (tr is None and BracketHelper.can_be_end_of_sequence(t, True, None, False)): 
                tr0.end_token = t
                continue
            if (tr is None): 
                break
            if (t.is_newline_before): 
                if (tr.typ != TransItemToken.Typs.NUMBER): 
                    break
            res.append(tr)
            if (tr.typ == TransItemToken.Typs.ORG and tr0.typ == TransItemToken.Typs.NOUN): 
                pass
            else: 
                tr0 = tr
            t = tr.end_token
            if (and_conj): 
                break
        i = 0
        while i < (len(res) - 1): 
            if (res[i].typ == TransItemToken.Typs.MODEL and res[i + 1].typ == TransItemToken.Typs.MODEL): 
                res[i].end_token = res[i + 1].end_token
                res[i].value = "{0}{1}{2}".format(res[i].value, ('-' if res[i].end_token.next0_ is not None and res[i].end_token.next0_.is_hiphen else ' '), res[i + 1].value)
                del res[i + 1]
                i -= 1
            i += 1
        if ((len(res) > 1 and res[0].typ == TransItemToken.Typs.BRAND and res[1].typ == TransItemToken.Typs.MODEL) and res[1].length_char == 1 and not (isinstance(res[1].begin_token, NumberToken))): 
            return None
        return res
    
    @staticmethod
    def try_parse(t : 'Token', prev : 'TransItemToken', after_conj : bool, attach_high : bool=False) -> 'TransItemToken':
        res = TransItemToken.__try_parse(t, prev, after_conj, attach_high)
        if (res is None): 
            return None
        if (res.typ == TransItemToken.Typs.NAME): 
            br = BracketHelper.try_parse(res.end_token.next0_, BracketParseAttr.NO, 100)
            if (br is not None and br.begin_token.is_char('(')): 
                alt = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                if (MiscHelper.can_be_equal_cyr_and_latss(res.value, alt)): 
                    res.alt_value = alt
                    res.end_token = br.end_token
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', prev : 'TransItemToken', after_conj : bool, attach_high : bool=False) -> 'TransItemToken':
        if (t is None): 
            return None
        t1 = t
        if (t1.is_char(',')): 
            t1 = t1.next0_
        if (t1 is not None): 
            if (t1.is_value("ПРИНАДЛЕЖАТЬ", "НАЛЕЖАТИ") or t1.is_value("СУДОВЛАДЕЛЕЦ", "СУДНОВЛАСНИК") or t1.is_value("ВЛАДЕЛЕЦ", "ВЛАСНИК")): 
                t1 = t1.next0_
        if (isinstance(t1, ReferentToken)): 
            if (t1.get_referent().type_name == "ORGANIZATION"): 
                return TransItemToken._new2671(t, t1, TransItemToken.Typs.ORG, t1.get_referent(), t1.morph)
        if (t1 is not None and t1.is_value("ФЛАГ", None)): 
            tt = t1.next0_
            while tt is not None:
                if (tt.is_hiphen or tt.is_char(':')): 
                    tt = tt.next0_
                else: 
                    break
            if ((isinstance(tt, ReferentToken)) and (isinstance(tt.get_referent(), GeoReferent))): 
                return TransItemToken._new2672(t, tt, TransItemToken.Typs.GEO, tt.get_referent())
        if (t1 is not None and t1.is_value("ПОРТ", None)): 
            tt = t1.next0_
            while tt is not None: 
                if (tt.is_value("ПРИПИСКА", None) or tt.is_char(':')): 
                    pass
                else: 
                    break
                tt = tt.next0_
            if (tt is not None and (isinstance(tt.get_referent(), GeoReferent))): 
                return TransItemToken._new2672(t, tt, TransItemToken.Typs.GEO, tt.get_referent())
        route = False
        if (t1 is not None and ((t1.is_value("СЛЕДОВАТЬ", "СЛІДУВАТИ") or t1.is_value("ВЫПОЛНЯТЬ", "ВИКОНУВАТИ")))): 
            t1 = t1.next0_
            route = True
        if (t1 is not None and t1.morph.class0_.is_preposition): 
            t1 = t1.next0_
        if (t1 is not None and ((t1.is_value("РЕЙС", None) or t1.is_value("МАРШРУТ", None)))): 
            t1 = t1.next0_
            route = True
        if (isinstance(t1, ReferentToken)): 
            if (isinstance(t1.get_referent(), GeoReferent)): 
                geo_ = Utils.asObjectOrNull(t1.get_referent(), GeoReferent)
                if (geo_.is_state or geo_.is_city): 
                    tit = TransItemToken._new2674(t, t1, TransItemToken.Typs.ROUTE, list())
                    tit.route_items.append(geo_)
                    t1 = t1.next0_
                    first_pass3894 = True
                    while True:
                        if first_pass3894: first_pass3894 = False
                        else: t1 = t1.next0_
                        if (not (t1 is not None)): break
                        if (t1.is_hiphen): 
                            continue
                        if (t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction): 
                            continue
                        geo_ = (Utils.asObjectOrNull(t1.get_referent(), GeoReferent))
                        if (geo_ is None): 
                            break
                        if (not geo_.is_city and not geo_.is_state): 
                            break
                        tit.route_items.append(geo_)
                        tit.end_token = t1
                    if (len(tit.route_items) > 1 or route): 
                        return tit
            elif ((isinstance(t1.get_referent(), DateReferent)) and (t1.whitespaces_before_count < 3)): 
                tit = TransItemToken._new2672(t, t1, TransItemToken.Typs.DATE, t1.get_referent())
                if (t1.next0_ is not None): 
                    if (t1.next0_.is_value("В", None) and t1.next0_.next0_ is not None and t1.next0_.next0_.is_char('.')): 
                        tit.end_token = t1.next0_.next0_
                    elif (t1.next0_.is_value("ВЫП", None) or t1.next0_.is_value("ВЫПУСК", None)): 
                        tit.end_token = t1.next0_
                        if (t1.next0_.next0_ is not None and t1.next0_.next0_.is_char('.')): 
                            tit.end_token = t1.next0_.next0_
                return tit
        if (isinstance(t, TextToken)): 
            num = MiscHelper.check_number_prefix(t)
            if (num is not None): 
                tit = TransItemToken._attach_rus_auto_number(num)
                if (tit is None): 
                    tit = TransItemToken._attach_number(num, False)
                if (tit is not None): 
                    tit.begin_token = t
                    return tit
            tok = TransItemToken.M_ONTOLOGY.try_parse(t, TerminParseAttr.NO)
            if (tok is None and ((t.is_value("С", None) or t.is_value("C", None) or t.is_value("ЗА", None)))): 
                tok = TransItemToken.M_ONTOLOGY.try_parse(t.next0_, TerminParseAttr.NO)
            is_br = False
            if (tok is None and BracketHelper.is_bracket(t, True)): 
                tok1 = TransItemToken.M_ONTOLOGY.try_parse(t.next0_, TerminParseAttr.NO)
                if (tok1 is not None and BracketHelper.is_bracket(tok1.end_token.next0_, True)): 
                    tok = tok1
                    tok.begin_token = t
                    tok.end_token = tok.end_token.next0_
                    tok.begin_token = t
                    is_br = True
                elif (tok1 is not None): 
                    tt = Utils.asObjectOrNull(tok1.termin, TransItemToken.TransTermin)
                    if (tt.typ == TransItemToken.Typs.BRAND): 
                        tok = tok1
                        tok.begin_token = t
                if (tok is not None and BracketHelper.can_be_end_of_sequence(tok.end_token.next0_, True, None, False)): 
                    tok.end_token = tok.end_token.next0_
                    is_br = True
            if (tok is None and t.is_value("МАРКА", None)): 
                res1 = TransItemToken.__try_parse(t.next0_, prev, after_conj, False)
                if (res1 is not None): 
                    if (res1.typ == TransItemToken.Typs.NAME or res1.typ == TransItemToken.Typs.BRAND): 
                        res1.begin_token = t
                        res1.typ = TransItemToken.Typs.BRAND
                        return res1
            if (tok is not None): 
                tt = Utils.asObjectOrNull(tok.termin, TransItemToken.TransTermin)
                if (tt.typ == TransItemToken.Typs.NUMBER): 
                    tit = TransItemToken._attach_rus_auto_number(tok.end_token.next0_)
                    if (tit is None): 
                        tit = TransItemToken._attach_number(tok.end_token.next0_, False)
                    if (tit is not None): 
                        tit.begin_token = t
                        return tit
                    else: 
                        return None
                if (tt.is_doubt and not attach_high): 
                    if (prev is None or prev.typ != TransItemToken.Typs.NOUN): 
                        if ((prev is not None and prev.typ == TransItemToken.Typs.BRAND and tt.typ == TransItemToken.Typs.BRAND) and Utils.compareStrings(tt.canonic_text, prev.value, True) == 0): 
                            pass
                        else: 
                            return None
                if (tt.canonic_text == "СУДНО"): 
                    if (((tok.morph.number) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                        if (not BracketHelper.can_be_start_of_sequence(tok.end_token.next0_, False, False)): 
                            return None
                tit = TransItemToken._new2676(tok.begin_token, tok.end_token, tt.kind, tt.typ, tt.is_doubt and not is_br, tok.chars, tok.morph)
                tit.value = tt.canonic_text
                if (tit.typ == TransItemToken.Typs.NOUN): 
                    tit.value = tit.value.lower()
                    if (((tit.end_token.next0_ is not None and tit.end_token.next0_.is_hiphen and not tit.end_token.is_whitespace_after) and (isinstance(tit.end_token.next0_.next0_, TextToken)) and not tit.end_token.next0_.is_whitespace_after) and tit.end_token.next0_.next0_.get_morph_class_in_dictionary().is_noun): 
                        tit.end_token = tit.end_token.next0_.next0_
                        tit.value = "{0}-{1}".format(tit.value, Utils.ifNotNull(tit.end_token.get_normal_case_text(MorphClass.NOUN, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), "?")).lower()
                else: 
                    tit.value = tit.value.upper()
                return tit
            if (tok is None and t.morph.class0_.is_adjective): 
                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and len(npt.adjectives) > 0): 
                    state_ = None
                    tt = t
                    first_pass3895 = True
                    while True:
                        if first_pass3895: first_pass3895 = False
                        else: tt = tt.next0_
                        if (not (tt is not None and tt.previous != npt.end_token)): break
                        tok = TransItemToken.M_ONTOLOGY.try_parse(tt, TerminParseAttr.NO)
                        if (tok is None and state_ is None): 
                            state_ = tt.kit.process_referent("GEO", tt)
                        if (tok is not None and tok.end_token == npt.end_token): 
                            if (tok.termin.typ == TransItemToken.Typs.NOUN): 
                                tit = TransItemToken._new2676(t, tok.end_token, tok.termin.kind, TransItemToken.Typs.NOUN, tok.termin.is_doubt, tok.chars, npt.morph)
                                tit.value = tok.termin.canonic_text.lower()
                                tit.alt_value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False).lower()
                                if (LanguageHelper.ends_with_ex(tit.alt_value, "суд", "суда", None, None)): 
                                    if (not BracketHelper.can_be_start_of_sequence(tok.end_token.next0_, False, False)): 
                                        continue
                                if (state_ is not None): 
                                    if (state_.referent.is_state): 
                                        tit.state = state_
                                return tit
        if (t is not None and t.is_value("КЛАСС", None) and t.next0_ is not None): 
            br = BracketHelper.try_parse(t.next0_, BracketParseAttr.NO, 100)
            if (br is not None): 
                return TransItemToken._new2678(t, br.end_token, TransItemToken.Typs.CLASS, MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO))
        nt = Utils.asObjectOrNull(t, NumberToken)
        if (nt is not None): 
            if (prev is None or nt.typ != NumberSpellingType.DIGIT): 
                return None
            if (prev.typ == TransItemToken.Typs.BRAND): 
                return TransItemToken.__attach_model(t, False, prev)
            else: 
                return None
        res = TransItemToken._attach_rus_auto_number(t)
        if ((res) is not None): 
            if (not res.is_doubt): 
                return res
            if (prev is not None and prev.typ == TransItemToken.Typs.NOUN and prev.kind == TransportKind.AUTO): 
                return res
            if (prev is not None and ((prev.typ == TransItemToken.Typs.BRAND or prev.typ == TransItemToken.Typs.MODEL))): 
                return res
        t1 = t
        if (t.is_hiphen): 
            t1 = t.next0_
        if (prev is not None and prev.typ == TransItemToken.Typs.BRAND and t1 is not None): 
            tit = TransItemToken.__attach_model(t1, True, prev)
            if (tit is not None): 
                tit.begin_token = t
                return tit
        if (prev is not None and ((prev.typ == TransItemToken.Typs.NOUN or after_conj))): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (br is not None and br.is_quote_type): 
                tit = TransItemToken.try_parse(br.begin_token.next0_, prev, after_conj, False)
                if (tit is not None and tit.end_token.next0_ == br.end_token): 
                    if (not tit.is_doubt or tit.typ == TransItemToken.Typs.BRAND): 
                        tit.begin_token = br.begin_token
                        tit.end_token = br.end_token
                        return tit
                s = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                if (not Utils.isNullOrEmpty(s) and (len(s) < 30)): 
                    chars_ = 0
                    digs = 0
                    un = 0
                    for c in s: 
                        if (not Utils.isWhitespace(c)): 
                            if (str.isalpha(c)): 
                                chars_ += 1
                            elif (str.isdigit(c)): 
                                digs += 1
                            else: 
                                un += 1
                    if (((digs == 0 and un == 0 and t.next0_.chars.is_capital_upper)) or prev.kind == TransportKind.SHIP or prev.kind == TransportKind.SPACE): 
                        return TransItemToken._new2678(br.begin_token, br.end_token, TransItemToken.Typs.NAME, s)
                    if (digs > 0 and (chars_ < 5)): 
                        return TransItemToken._new2678(br.begin_token, br.end_token, TransItemToken.Typs.MODEL, s.replace(" ", ""))
        if (prev is not None and (((prev.typ == TransItemToken.Typs.NOUN or prev.typ == TransItemToken.Typs.BRAND or prev.typ == TransItemToken.Typs.NAME) or prev.typ == TransItemToken.Typs.MODEL))): 
            tit = TransItemToken.__attach_model(t, prev.typ != TransItemToken.Typs.NAME, prev)
            if (tit is not None): 
                return tit
        if (((prev is not None and prev.typ == TransItemToken.Typs.NOUN and prev.kind == TransportKind.AUTO) and (isinstance(t, TextToken)) and t.chars.is_letter) and not t.chars.is_all_lower and (t.whitespaces_before_count < 2)): 
            pt = t.kit.process_referent("PERSON", t)
            if (pt is None): 
                tit = TransItemToken._new2681(t, t, TransItemToken.Typs.BRAND)
                tit.value = t.term
                mc = t.get_morph_class_in_dictionary()
                if (mc.is_noun): 
                    tit.is_doubt = True
                return tit
        if (((prev is not None and prev.typ == TransItemToken.Typs.NOUN and ((prev.kind == TransportKind.SHIP or prev.kind == TransportKind.SPACE)))) or after_conj): 
            if (t.chars.is_capital_upper): 
                ok = True
                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and len(npt.adjectives) > 0): 
                    ok = False
                else: 
                    rt = t.kit.process_referent("PERSON", t)
                    if (rt is not None): 
                        ok = False
                if (t.get_morph_class_in_dictionary().is_proper_surname): 
                    if (not t.morph.case_.is_nominative): 
                        ok = False
                if (ok): 
                    t1 = t
                    tt = t.next0_
                    while tt is not None: 
                        if (tt.whitespaces_before_count > 1): 
                            break
                        if (tt.chars != t.chars): 
                            break
                        tit = TransItemToken.try_parse(tt, None, False, False)
                        if ((tit) is not None): 
                            break
                        t1 = tt
                        tt = tt.next0_
                    s = MiscHelper.get_text_value(t, t1, GetTextAttr.NO)
                    if (s is not None): 
                        res1 = TransItemToken._new2682(t, t1, TransItemToken.Typs.NAME, True, s)
                        if (not t1.is_newline_after): 
                            br = BracketHelper.try_parse(t1.next0_, BracketParseAttr.NO, 100)
                            if (br is not None): 
                                res1.end_token = br.end_token
                                res1.alt_value = res1.value
                                res1.value = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                        return res1
        return None
    
    @staticmethod
    def __attach_model(t : 'Token', can_be_first_word : bool, prev : 'TransItemToken') -> 'TransItemToken':
        res = TransItemToken._new2681(t, t, TransItemToken.Typs.MODEL)
        cyr = io.StringIO()
        lat = io.StringIO()
        t0 = t
        num = False
        first_pass3896 = True
        while True:
            if first_pass3896: first_pass3896 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t != t0 and t.whitespaces_before_count > 1): 
                break
            if (t == t0): 
                if (t.is_hiphen or t.chars.is_all_lower): 
                    if (prev is None or prev.typ != TransItemToken.Typs.BRAND): 
                        return None
            else: 
                pp = TransItemToken.try_parse(t, None, False, False)
                if (pp is not None): 
                    break
            if (t.is_hiphen): 
                num = False
                continue
            nt = Utils.asObjectOrNull(t, NumberToken)
            if (nt is not None): 
                if (num): 
                    break
                num = True
                if (nt.typ != NumberSpellingType.DIGIT): 
                    break
                if (cyr is not None): 
                    print(nt.value, end="", file=cyr)
                if (lat is not None): 
                    print(nt.value, end="", file=lat)
                res.end_token = t
                continue
            if (t != t0 and TransItemToken.try_parse(t, None, False, False) is not None): 
                break
            if (num and t.is_whitespace_before): 
                break
            num = False
            vv = MiscHelper.get_cyr_lat_word(t, 3)
            if (vv is None): 
                if (can_be_first_word and t == t0): 
                    if (t.chars.is_letter and t.chars.is_capital_upper): 
                        vv = MiscHelper.get_cyr_lat_word(t, 0)
                        if ((vv) is not None): 
                            if (t.morph.case_.is_genitive and ((prev is None or prev.typ != TransItemToken.Typs.BRAND))): 
                                vv = (None)
                            elif (prev is not None and prev.typ == TransItemToken.Typs.NOUN and ((prev.kind == TransportKind.SHIP or prev.kind == TransportKind.SPACE))): 
                                vv = (None)
                            else: 
                                res.is_doubt = True
                    if (((vv is None and (isinstance(t, TextToken)) and not t.chars.is_all_lower) and t.chars.is_latin_letter and prev is not None) and prev.typ == TransItemToken.Typs.BRAND): 
                        print(t.term, end="", file=lat)
                        res.end_token = t
                        continue
                if (vv is None): 
                    break
            if ((vv.length < 4) or t.morph.class0_.is_preposition or t.morph.class0_.is_conjunction): 
                if (t.is_whitespace_before and t.is_whitespace_after): 
                    if (t.previous is not None and not t.previous.is_hiphen): 
                        if (t.chars.is_all_lower): 
                            break
            if (cyr is not None): 
                if (vv.cyr_word is not None): 
                    print(vv.cyr_word, end="", file=cyr)
                else: 
                    cyr = (None)
            if (lat is not None): 
                if (vv.lat_word is not None): 
                    print(vv.lat_word, end="", file=lat)
                else: 
                    lat = (None)
            res.end_token = t
        if (lat is None and cyr is None): 
            return None
        if (lat is not None and lat.tell() > 0): 
            res.value = Utils.toStringStringIO(lat)
            if (cyr is not None and cyr.tell() > 0 and res.value != Utils.toStringStringIO(cyr)): 
                res.alt_value = Utils.toStringStringIO(cyr)
        elif (cyr is not None and cyr.tell() > 0): 
            res.value = Utils.toStringStringIO(cyr)
        if (Utils.isNullOrEmpty(res.value)): 
            return None
        if (res.kit.process_referent("PERSON", res.begin_token) is not None): 
            return None
        return res
    
    @staticmethod
    def _attach_number(t : 'Token', ignore_region : bool=False) -> 'TransItemToken':
        if (t is None): 
            return None
        if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                res1 = TransItemToken._attach_number(t.next0_, False)
                if (res1 is not None and res1.end_token.next0_ == br.end_token): 
                    res1.begin_token = t
                    res1.end_token = br.end_token
                    return res1
        t0 = t
        t1 = t
        if (t.is_value("НА", None)): 
            npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None and npt.noun.is_value("ФОН", None)): 
                t = npt.end_token.next0_
        res = None
        first_pass3897 = True
        while True:
            if first_pass3897: first_pass3897 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_before): 
                break
            if (t != t0 and t.whitespaces_before_count > 1): 
                break
            if (t.is_hiphen): 
                continue
            nt = Utils.asObjectOrNull(t, NumberToken)
            if (nt is not None): 
                if (nt.typ != NumberSpellingType.DIGIT or nt.morph.class0_.is_adjective): 
                    break
                if (res is None): 
                    res = io.StringIO()
                elif (str.isdigit(Utils.getCharAtStringIO(res, res.tell() - 1))): 
                    print(' ', end="", file=res)
                print(nt.get_source_text(), end="", file=res)
                t1 = t
                continue
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is None): 
                if ((isinstance(t, MetaToken)) and (t.begin_token.length_char < 3) and (isinstance(t.begin_token, TextToken))): 
                    tt = (Utils.asObjectOrNull(t.begin_token, TextToken))
                else: 
                    break
            if (not tt.chars.is_letter): 
                break
            if (not tt.chars.is_all_upper and tt.is_whitespace_before): 
                break
            if (tt.length_char > 3): 
                break
            if (res is None): 
                res = io.StringIO()
            print(tt.term, end="", file=res)
            t1 = t
        if (res is None or (res.tell() < 4)): 
            return None
        re = TransItemToken._new2678(t0, t1, TransItemToken.Typs.NUMBER, Utils.toStringStringIO(res))
        if (not ignore_region): 
            k = 0; i = res.tell() - 1
            while i > 4: 
                if (not str.isdigit(Utils.getCharAtStringIO(res, i))): 
                    if (Utils.getCharAtStringIO(res, i) == ' ' and ((k == 2 or k == 3))): 
                        re.alt_value = re.value[i + 1:]
                        re.value = re.value[0:0+i]
                    break
                i -= 1; k += 1
        re.value = re.value.replace(" ", "")
        if (ignore_region): 
            re.alt_value = MiscHelper.create_cyr_lat_alternative(re.value)
        return re
    
    @staticmethod
    def _attach_rus_auto_number(t : 'Token') -> 'TransItemToken':
        if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                res1 = TransItemToken._attach_rus_auto_number(t.next0_)
                if (res1 is not None and res1.end_token.next0_ == br.end_token): 
                    res1.begin_token = t
                    res1.end_token = br.end_token
                    return res1
        v1 = MiscHelper.get_cyr_lat_word(t, 1)
        if (v1 is None or v1.cyr_word is None): 
            return None
        t0 = t
        doubt = 0
        if (not t.chars.is_all_upper or t.is_whitespace_after): 
            doubt += 1
        t = t.next0_
        nt = Utils.asObjectOrNull(t, NumberToken)
        if ((nt is None or nt.typ != NumberSpellingType.DIGIT or nt.morph.class0_.is_adjective) or (nt.end_char - nt.begin_char) != 2): 
            return None
        t = t.next0_
        v2 = MiscHelper.get_cyr_lat_word(t, 2)
        if (v2 is None or v2.cyr_word is None or v2.length != 2): 
            return None
        if (not t.chars.is_all_upper or t.is_whitespace_after): 
            doubt += 1
        res = TransItemToken._new2685(t0, t, TransItemToken.Typs.NUMBER, TransportKind.AUTO)
        res.value = "{0}{1}{2}".format(v1.cyr_word, nt.get_source_text(), v2.cyr_word)
        nt = (Utils.asObjectOrNull(t.next0_, NumberToken))
        if (((nt is not None and nt.int_value is not None and nt.typ == NumberSpellingType.DIGIT) and not nt.morph.class0_.is_adjective and nt.int_value is not None) and (nt.int_value < 1000) and (t.whitespaces_after_count < 2)): 
            n = nt.value
            if (len(n) < 2): 
                n = ("0" + n)
            res.alt_value = n
            res.end_token = nt
        if (res.end_token.next0_ is not None and res.end_token.next0_.is_value("RUS", None)): 
            res.end_token = res.end_token.next0_
            doubt = 0
        if (doubt > 1): 
            res.is_doubt = True
        return res
    
    M_ONTOLOGY = None
    
    @staticmethod
    def check_number_keyword(t : 'Token') -> 'Token':
        tok = TransItemToken.M_ONTOLOGY.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        tt = Utils.asObjectOrNull(tok.termin, TransItemToken.TransTermin)
        if (tt is not None and tt.typ == TransItemToken.Typs.NUMBER): 
            return tok.end_token.next0_
        return None
    
    @staticmethod
    def initialize() -> None:
        if (TransItemToken.M_ONTOLOGY is not None): 
            return
        TransItemToken.M_ONTOLOGY = TerminCollection()
        t = TransItemToken.TransTermin._new2686("автомобиль", True, TransItemToken.Typs.NOUN, TransportKind.AUTO)
        t.add_abridge("а-м")
        t.add_variant("автомашина", False)
        t.add_variant("ТРАНСПОРТНОЕ СРЕДСТВО", False)
        t.add_variant("автомобіль", False)
        TransItemToken.M_ONTOLOGY.add(t)
        for s in ["ВНЕДОРОЖНИК", "ПОЗАШЛЯХОВИК", "АВТОБУС", "МИКРОАВТОБУС", "ГРУЗОВИК", "МОТОЦИКЛ", "МОПЕД"]: 
            TransItemToken.M_ONTOLOGY.add(TransItemToken.TransTermin._new2686(s, True, TransItemToken.Typs.NOUN, TransportKind.AUTO))
        t = TransItemToken.TransTermin._new2686("", True, TransItemToken.Typs.NOUN, TransportKind.AUTO)
        t.add_abridge("а-м")
        TransItemToken.M_ONTOLOGY.add(t)
        t = TransItemToken.TransTermin._new2689("государственный номер", True, TransItemToken.Typs.NUMBER, "ИМО")
        t.add_abridge("г-н")
        t.add_abridge("н\\з")
        t.add_abridge("г\\н")
        t.add_variant("госномер", False)
        t.add_abridge("гос.номер")
        t.add_abridge("гос.ном.")
        t.add_abridge("г.н.з.")
        t.add_abridge("г.р.з.")
        t.add_variant("ГРЗ", False)
        t.add_variant("ГНЗ", False)
        t.add_variant("регистрационный знак", False)
        t.add_abridge("рег. знак")
        t.add_variant("государственный регистрационный знак", False)
        t.add_variant("бортовой номер", False)
        TransItemToken.M_ONTOLOGY.add(t)
        t = TransItemToken.TransTermin._new2690("державний номер", True, TransItemToken.Typs.NUMBER, MorphLang.UA)
        t.add_variant("держномер", False)
        t.add_abridge("держ.номер")
        t.add_abridge("держ.ном.")
        TransItemToken.M_ONTOLOGY.add(t)
        t = TransItemToken.TransTermin._new2691("номер", True, TransItemToken.Typs.NUMBER)
        TransItemToken.M_ONTOLOGY.add(t)
        for s in ["КРУИЗНЫЙ ЛАЙНЕР", "ТЕПЛОХОД", "ПАРОХОД", "ЯХТА", "ЛОДКА", "КАТЕР", "КОРАБЛЬ", "СУДНО", "ПОДВОДНАЯ ЛОДКА", "АПК", "ШХУНА", "ПАРОМ", "КРЕЙСЕР", "АВИАНОСЕЦ", "ЭСМИНЕЦ", "ФРЕГАТ", "ЛИНКОР", "АТОМОХОД", "ЛЕДОКОЛ", "ПЛАВБАЗА", "ТАНКЕР", "СУПЕРТАНКЕР", "СУХОГРУЗ", "ТРАУЛЕР", "РЕФРИЖЕРАТОР"]: 
            t = TransItemToken.TransTermin._new2686(s, True, TransItemToken.Typs.NOUN, TransportKind.SHIP)
            TransItemToken.M_ONTOLOGY.add(t)
            if (s == "АПК"): 
                t.is_doubt = True
        for s in ["КРУЇЗНИЙ ЛАЙНЕР", "ПАРОПЛАВ", "ПАРОПЛАВ", "ЯХТА", "ЧОВЕН", "КОРАБЕЛЬ", "СУДНО", "ПІДВОДНИЙ ЧОВЕН", "АПК", "ШХУНА", "ПОРОМ", "КРЕЙСЕР", "АВІАНОСЕЦЬ", "ЕСМІНЕЦЬ", "ФРЕГАТ", "ЛІНКОР", "АТОМОХІД", "КРИГОЛАМ", "ПЛАВБАЗА", "ТАНКЕР", "СУПЕРТАНКЕР", "СУХОВАНТАЖ", "ТРАУЛЕР", "РЕФРИЖЕРАТОР"]: 
            t = TransItemToken.TransTermin._new2693(s, True, TransItemToken.Typs.NOUN, MorphLang.UA, TransportKind.SHIP)
            TransItemToken.M_ONTOLOGY.add(t)
            if (s == "АПК"): 
                t.is_doubt = True
        for s in ["САМОЛЕТ", "АВИАЛАЙНЕР", "ИСТРЕБИТЕЛЬ", "БОМБАРДИРОВЩИК", "ВЕРТОЛЕТ"]: 
            TransItemToken.M_ONTOLOGY.add(TransItemToken.TransTermin._new2686(s, True, TransItemToken.Typs.NOUN, TransportKind.FLY))
        for s in ["ЛІТАК", "АВІАЛАЙНЕР", "ВИНИЩУВАЧ", "БОМБАРДУВАЛЬНИК", "ВЕРТОЛІТ"]: 
            TransItemToken.M_ONTOLOGY.add(TransItemToken.TransTermin._new2693(s, True, TransItemToken.Typs.NOUN, MorphLang.UA, TransportKind.FLY))
        for s in ["КОСМИЧЕСКИЙ КОРАБЛЬ", "ЗВЕЗДОЛЕТ", "КОСМИЧЕСКАЯ СТАНЦИЯ", "РАКЕТА-НОСИТЕЛЬ"]: 
            TransItemToken.M_ONTOLOGY.add(TransItemToken.TransTermin._new2686(s, True, TransItemToken.Typs.NOUN, TransportKind.SPACE))
        for s in ["КОСМІЧНИЙ КОРАБЕЛЬ", "ЗОРЕЛІТ", "КОСМІЧНА СТАНЦІЯ", "РАКЕТА-НОСІЙ"]: 
            TransItemToken.M_ONTOLOGY.add(TransItemToken.TransTermin._new2693(s, True, TransItemToken.Typs.NOUN, MorphLang.UA, TransportKind.SPACE))
        TransItemToken.__load_brands(TransItemToken.M_CARS, TransportKind.AUTO)
        TransItemToken.__load_brands(TransItemToken.M_FLYS, TransportKind.FLY)
    
    @staticmethod
    def __load_brands(str0_ : str, kind_ : 'TransportKind') -> None:
        cars = Utils.splitString(str0_, ';', False)
        vars0_ = list()
        for c in cars: 
            its = Utils.splitString(c, ',', False)
            vars0_.clear()
            doubt = False
            for it in its: 
                s = it.strip()
                if (not Utils.isNullOrEmpty(s)): 
                    if (s == "true"): 
                        doubt = True
                    else: 
                        vars0_.append(s)
            if (len(vars0_) == 0): 
                continue
            for v in vars0_: 
                t = TransItemToken.TransTermin(v)
                t.canonic_text = vars0_[0]
                t.kind = kind_
                t.typ = TransItemToken.Typs.BRAND
                t.is_doubt = doubt
                TransItemToken.M_ONTOLOGY.add(t)
    
    M_FLYS = "\n        Boeing, Боинг;\n        Airbus, Аэробус, Эрбас;\n        Ил, Илюшин, true;\n        Ту, Туполев, true;\n        Ан, Антонов, true;\n        Су, Сухой, Sukhoi, Sukhoy, true;\n        Як, Яковлев, true;\n        BAE Systems, БАЕ Системз;\n        ATR, АТР, true;\n        AVIC;\n        Bombardier, Бомбардье;  \n        Britten-Norman, Бриттен-Норман;\n        Cessna, Цессна;\n        Dornier, Дорнье;\n        Embraer, Эмбраер;\n        Fairchild, Fairchild Aerospace, Фэйрчайлд;\n        Fokker, Фоккер;\n        Hawker Beechcraft, Хокер Бичкрафт;\n        Indonesian Aerospace, Индонезиан;\n        Lockheed Martin, Локхид Мартин;\n        LZ Auronautical Industries, LET;\n        Douglas, McDonnell Douglas, Дуглас;\n        NAMC, НАМК;\n        Pilatus, Пилатус, true;\n        Piper Aircraft;\n        Saab, Сааб, true;\n        Shorts, Шортс, true;\n"
    
    M_CARS = "\n        AC Cars;\n        Acura, Акура;\n        Abarth;\n        Alfa Romeo, Альфа Ромео;\n        ALPINA, Альпина, true;\n        Ariel Motor, Ариэль Мотор;\n        ARO, true;\n        Artega, true;\n        Aston Martin;\n        AUDI, Ауди;\n        Austin Healey;\n        BAW;\n        Beijing Jeep;\n        Bentley, Бентли;\n        Bitter, Биттер, true;\n        BMW, БМВ;\n        Brilliance;\n        Bristol, Бристоль, true;\n        Bugatti, Бугатти;\n        Buick, Бьюик;\n        BYD, true;\n        Cadillac, Кадиллак, Кадилак;\n        Caterham;\n        Chery, trye;\n        Chevrolet, Шевроле, Шеврале;\n        Chrysler, Крайслер;\n        Citroen, Ситроен, Ситроэн;\n        Dacia;\n        DADI;\n        Daewoo, Дэо;\n        Dodge, Додж;\n        Daihatsu;\n        Daimler, Даймлер;\n        DKW;\n        Derways;\n        Eagle, true;\n        Elfin Sports Cars;\n        FAW, true;\n        Ferrari, Феррари, Ферари;\n        FIAT, Фиат;\n        Fisker Karma;\n        Ford, Форд;\n        Geely;\n        GEO, true;\n        GMC, true;\n        Gonow;\n        Great Wall, true;\n        Gumpert;\n        Hafei;\n        Haima;\n        Honda, Хонда;\n        Horch;\n        Hudson, true;\n        Hummer, Хаммер;\n        Harley, Харлей;\n        Hyundai, Хюндай, Хундай;\n        Infiniti, true;\n        Isuzu, Исузу;\n        Jaguar, Ягуар, true;\n        Jeep, Джип, true;\n        Kia, Киа, true;\n        Koenigsegg;\n        Lamborghini, Ламборджини;\n        Land Rover, Лендровер, Лэндровер;\n        Landwind;\n        Lancia;\n        Lexus, Лексус;\n        Leyland;\n        Lifan;\n        Lincoln, Линкольн, true;\n        Lotus, true;\n        Mahindra;\n        Maserati;\n        Maybach;\n        Mazda, Мазда;\n        Mercedes-Benz, Mercedes, Мерседес, Мэрседес, Мерседес-бенц;\n        Mercury, true;\n        Mini, true;\n        Mitsubishi, Mitsubishi Motors, Мицубиши, Мицубиси;\n        Morgan, true;\n        Nissan, Nissan Motor, Ниссан, Нисан;\n        Opel, Опель;\n        Pagani;\n        Peugeot, Пежо;\n        Plymouth;\n        Pontiac, Понтиак;\n        Porsche, Порше;\n        Renault, Рено;\n        Rinspeed;\n        Rolls-Royce, Роллс-Ройс;\n        SAAB, Сааб;\n        Saleen;\n        Saturn, Сатурн, true;\n        Scion;\n        Seat, true;\n        Skoda, Шкода;\n        Smart, true;\n        Spyker, true;\n        Ssang Yong, Ссанг янг;\n        Subaru, Субару;\n        Suzuki, Судзуки;\n        Tesla, true;\n        Toyota, Тойота;\n        Vauxhall;\n        Volkswagen, Фольксваген;\n        Volvo, Вольво;\n        Wartburg;\n        Wiesmann;\n        Yamaha, Ямаха;\n        Zenvo;\n\n        ВАЗ, VAZ;\n        ГАЗ, GAZ, true;\n        ЗАЗ, ZAZ;\n        ЗИЛ, ZIL;\n        АЗЛК, AZLK;\n        Иж, true;\n        Москвич, true;\n        УАЗ, UAZ;\n        ТАГАЗ, TaGAZ;\n        Лада, Жигули, true;\n\n"
    
    @staticmethod
    def _new2671(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : 'Referent', _arg5 : 'MorphCollection') -> 'TransItemToken':
        res = TransItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new2672(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : 'Referent') -> 'TransItemToken':
        res = TransItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        return res
    
    @staticmethod
    def _new2674(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : typing.List[object]) -> 'TransItemToken':
        res = TransItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.route_items = _arg4
        return res
    
    @staticmethod
    def _new2676(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'TransportKind', _arg4 : 'Typs', _arg5 : bool, _arg6 : 'CharsInfo', _arg7 : 'MorphCollection') -> 'TransItemToken':
        res = TransItemToken(_arg1, _arg2)
        res.kind = _arg3
        res.typ = _arg4
        res.is_doubt = _arg5
        res.chars = _arg6
        res.morph = _arg7
        return res
    
    @staticmethod
    def _new2678(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : str) -> 'TransItemToken':
        res = TransItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new2681(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs') -> 'TransItemToken':
        res = TransItemToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2682(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : bool, _arg5 : str) -> 'TransItemToken':
        res = TransItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new2685(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : 'TransportKind') -> 'TransItemToken':
        res = TransItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.kind = _arg4
        return res