# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from enum import IntEnum
from pullenti.unisharp.Utils import Utils

from pullenti.ner.instrument.internal.ILTypes import ILTypes
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.core.Termin import Termin
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.decree.internal.DecreeToken import DecreeToken
from pullenti.ner.instrument.internal.InstrToken import InstrToken
from pullenti.ner.uri.UriReferent import UriReferent
from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
from pullenti.ner.decree.DecreeReferent import DecreeReferent
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.instrument.InstrumentAnalyzer import InstrumentAnalyzer
from pullenti.ner.phone.PhoneReferent import PhoneReferent
from pullenti.ner.instrument.InstrumentParticipantReferent import InstrumentParticipantReferent
from pullenti.ner.bank.BankDataReferent import BankDataReferent
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.BracketParseAttr import BracketParseAttr

class ParticipantToken(MetaToken):
    
    class Kinds(IntEnum):
        UNDEFINED = 0
        PURE = 1
        NAMEDAS = 2
        NAMEDASPARTS = 3
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = None;
        self.kind = ParticipantToken.Kinds.UNDEFINED
        self.parts = None
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0}: {1}".format(Utils.enumToString(self.kind), Utils.ifNotNull(self.typ, "?")), end="", file=res, flush=True)
        if (self.parts is not None): 
            for p in self.parts: 
                print("; {0}".format(p.to_string(True, None, 0)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def try_attach(t : 'Token', p1 : 'InstrumentParticipantReferent'=None, p2 : 'InstrumentParticipantReferent'=None, is_contract : bool=False) -> 'ParticipantToken':
        if (t is None): 
            return None
        tt = t
        br = False
        if (p1 is None and p2 is None and is_contract): 
            r1 = t.get_referent()
            if ((r1 is not None and t.next0_ is not None and t.next0_.is_comma_and) and (isinstance(t.next0_.next0_, ReferentToken))): 
                r2 = t.next0_.next0_.get_referent()
                if (r1.type_name == r2.type_name): 
                    ttt = t.next0_.next0_.next0_
                    refs = list()
                    refs.append(r1)
                    refs.append(r2)
                    first_pass3774 = True
                    while True:
                        if first_pass3774: first_pass3774 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        if ((ttt.is_comma_and and ttt.next0_ is not None and ttt.next0_.get_referent() is not None) and ttt.next0_.get_referent().type_name == r1.type_name): 
                            ttt = ttt.next0_
                            if (not ttt.get_referent() in refs): 
                                refs.append(ttt.get_referent())
                            continue
                        break
                    first_pass3775 = True
                    while True:
                        if first_pass3775: first_pass3775 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        if (ttt.is_comma or ttt.morph.class0_.is_preposition): 
                            continue
                        if ((ttt.is_value("ИМЕНОВАТЬ", None) or ttt.is_value("ДАЛЬНЕЙШИЙ", None) or ttt.is_value("ДАЛЕЕ", None)) or ttt.is_value("ТЕКСТ", None)): 
                            continue
                        if (ttt.is_value("ДОГОВАРИВАТЬСЯ", None)): 
                            continue
                        npt = NounPhraseHelper.try_parse(ttt, NounPhraseParseAttr.NO, 0, None)
                        if (npt is not None and npt.noun.is_value("СТОРОНА", None) and npt.morph.number != MorphNumber.SINGULAR): 
                            re = ParticipantToken._new1569(t, npt.end_token, ParticipantToken.Kinds.NAMEDASPARTS)
                            re.parts = refs
                            return re
                        break
            if ((isinstance(r1, OrganizationReferent)) or (isinstance(r1, PersonReferent))): 
                has_br = False
                has_named = False
                if (isinstance(r1, PersonReferent)): 
                    if (t.previous is not None and t.previous.is_value("ЛИЦО", None)): 
                        return None
                elif (t.previous is not None and ((t.previous.is_value("ВЫДАВАТЬ", None) or t.previous.is_value("ВЫДАТЬ", None)))): 
                    return None
                ttt = t.begin_token
                while ttt is not None and (ttt.end_char < t.end_char): 
                    if (ttt.is_char('(')): 
                        has_br = True
                    elif ((ttt.is_value("ИМЕНОВАТЬ", None) or ttt.is_value("ДАЛЬНЕЙШИЙ", None) or ttt.is_value("ДАЛЕЕ", None)) or ttt.is_value("ТЕКСТ", None)): 
                        has_named = True
                    elif ((ttt.is_comma or ttt.morph.class0_.is_preposition or ttt.is_hiphen) or ttt.is_char(':')): 
                        pass
                    elif (isinstance(ttt, ReferentToken)): 
                        pass
                    elif (has_br or has_named): 
                        npt = NounPhraseHelper.try_parse(ttt, NounPhraseParseAttr.REFERENTCANBENOUN, 0, None)
                        if (npt is None): 
                            break
                        if (has_br): 
                            if (npt.end_token.next0_ is None or not npt.end_token.next0_.is_char(')')): 
                                break
                        if (not has_named): 
                            if (ParticipantToken.M_ONTOLOGY.try_parse(ttt, TerminParseAttr.NO) is None): 
                                break
                        re = ParticipantToken._new1569(t, t, ParticipantToken.Kinds.NAMEDAS)
                        re.typ = npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                        re.parts = list()
                        re.parts.append(r1)
                        return re
                    ttt = ttt.next0_
                has_br = False
                has_named = False
                end_side = None
                brr = None
                add_refs = None
                ttt = t.next0_
                first_pass3776 = True
                while True:
                    if first_pass3776: first_pass3776 = False
                    else: ttt = ttt.next0_
                    if (not (ttt is not None)): break
                    if ((isinstance(ttt, NumberToken)) and (isinstance(ttt.next0_, TextToken)) and ttt.next0_.term == "СТОРОНЫ"): 
                        ttt = ttt.next0_
                        end_side = ttt
                        if (ttt.next0_ is not None and ttt.next0_.is_comma): 
                            ttt = ttt.next0_
                        if (ttt.next0_ is not None and ttt.next0_.is_and): 
                            break
                    if (brr is not None and ttt.begin_char > brr.end_char): 
                        brr = (None)
                    if (BracketHelper.can_be_start_of_sequence(ttt, False, False)): 
                        brr = BracketHelper.try_parse(ttt, BracketParseAttr.NO, 100)
                        if (brr is not None and (brr.length_char < 7) and ttt.is_char('(')): 
                            ttt = brr.end_token
                            brr = (None)
                            continue
                    elif ((ttt.is_value("ИМЕНОВАТЬ", None) or ttt.is_value("ДАЛЬНЕЙШИЙ", None) or ttt.is_value("ДАЛЕЕ", None)) or ttt.is_value("ТЕКСТ", None)): 
                        has_named = True
                    elif ((ttt.is_comma or ttt.morph.class0_.is_preposition or ttt.is_hiphen) or ttt.is_char(':')): 
                        pass
                    elif (brr is not None or has_named): 
                        if (BracketHelper.can_be_start_of_sequence(ttt, True, False)): 
                            ttt = ttt.next0_
                        npt = NounPhraseHelper.try_parse(ttt, NounPhraseParseAttr.REFERENTCANBENOUN, 0, None)
                        typ22 = None
                        if (npt is not None): 
                            ttt = npt.end_token
                            if (npt.end_token.is_value("ДОГОВОР", None)): 
                                continue
                        else: 
                            ttok = None
                            if (isinstance(ttt, MetaToken)): 
                                ttok = ParticipantToken.M_ONTOLOGY.try_parse(ttt.begin_token, TerminParseAttr.NO)
                            if (ttok is not None): 
                                typ22 = ttok.termin.canonic_text
                            elif (has_named and ttt.morph.class0_.is_adjective): 
                                typ22 = ttt.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                            elif (brr is not None): 
                                continue
                            else: 
                                break
                        if (BracketHelper.can_be_end_of_sequence(ttt.next0_, True, None, False)): 
                            ttt = ttt.next0_
                        if (brr is not None): 
                            if (ttt.next0_ is None): 
                                ttt = brr.end_token
                                continue
                            ttt = ttt.next0_
                        if (not has_named and typ22 is None): 
                            if (ParticipantToken.M_ONTOLOGY.try_parse(npt.begin_token, TerminParseAttr.NO) is None): 
                                break
                        re = ParticipantToken._new1569(t, ttt, ParticipantToken.Kinds.NAMEDAS)
                        re.typ = (Utils.ifNotNull(typ22, npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)))
                        re.parts = list()
                        re.parts.append(r1)
                        return re
                    elif ((ttt.is_value("ЗАРЕГИСТРИРОВАННЫЙ", None) or ttt.is_value("КАЧЕСТВО", None) or ttt.is_value("ПРОЖИВАЮЩИЙ", None)) or ttt.is_value("ЗАРЕГ", None)): 
                        pass
                    elif (ttt.get_referent() == r1): 
                        pass
                    elif ((isinstance(ttt.get_referent(), PersonIdentityReferent)) or (isinstance(ttt.get_referent(), AddressReferent))): 
                        if (add_refs is None): 
                            add_refs = list()
                        add_refs.append(ttt.get_referent())
                    else: 
                        prr = ttt.kit.process_referent("PERSONPROPERTY", ttt)
                        if (prr is not None): 
                            ttt = prr.end_token
                            continue
                        if (isinstance(ttt.get_referent(), GeoReferent)): 
                            continue
                        npt = NounPhraseHelper.try_parse(ttt, NounPhraseParseAttr.NO, 0, None)
                        if (npt is not None): 
                            if ((npt.noun.is_value("МЕСТО", None) or npt.noun.is_value("ЖИТЕЛЬСТВО", None) or npt.noun.is_value("ПРЕДПРИНИМАТЕЛЬ", None)) or npt.noun.is_value("ПОЛ", None) or npt.noun.is_value("РОЖДЕНИЕ", None)): 
                                ttt = npt.end_token
                                continue
                        if (ttt.is_newline_before): 
                            break
                        if (ttt.length_char < 3): 
                            continue
                        mc = ttt.get_morph_class_in_dictionary()
                        if (mc.is_adverb or mc.is_adjective): 
                            continue
                        if (ttt.chars.is_all_upper): 
                            continue
                        break
                if (end_side is not None or ((add_refs is not None and t.previous is not None and t.previous.is_and))): 
                    re = ParticipantToken._new1569(t, Utils.ifNotNull(end_side, t), ParticipantToken.Kinds.NAMEDAS)
                    re.typ = (None)
                    re.parts = list()
                    re.parts.append(r1)
                    if (add_refs is not None): 
                        re.parts.extend(add_refs)
                    return re
            too = ParticipantToken.M_ONTOLOGY.try_parse(t, TerminParseAttr.NO)
            if (too is not None): 
                if ((isinstance(t.previous, TextToken)) and t.previous.is_value("ЛИЦО", None)): 
                    too = (None)
            if (too is not None and too.termin.tag is not None and too.termin.canonic_text != "СТОРОНА"): 
                tt1 = too.end_token.next0_
                if (tt1 is not None): 
                    if (tt1.is_hiphen or tt1.is_char(':')): 
                        tt1 = tt1.next0_
                if (isinstance(tt1, ReferentToken)): 
                    r1 = tt1.get_referent()
                    if ((isinstance(r1, PersonReferent)) or (isinstance(r1, OrganizationReferent))): 
                        re = ParticipantToken._new1569(t, tt1, ParticipantToken.Kinds.NAMEDAS)
                        re.typ = too.termin.canonic_text
                        re.parts = list()
                        re.parts.append(r1)
                        return re
        add_typ1 = (None if p1 is None else p1.typ)
        add_typ2 = (None if p2 is None else p2.typ)
        if (BracketHelper.can_be_start_of_sequence(tt, False, False) and tt.next0_ is not None): 
            br = True
            tt = tt.next0_
        term1 = None
        term2 = None
        if (add_typ1 is not None and add_typ1.find(' ') > 0 and not add_typ1.startswith("СТОРОНА")): 
            term1 = Termin(add_typ1)
        if (add_typ2 is not None and add_typ2.find(' ') > 0 and not add_typ2.startswith("СТОРОНА")): 
            term2 = Termin(add_typ2)
        named = False
        typ_ = None
        t1 = None
        t0 = tt
        first_pass3777 = True
        while True:
            if first_pass3777: first_pass3777 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.morph.class0_.is_preposition and typ_ is not None): 
                continue
            if (tt.is_char_of("(:)") or tt.is_hiphen): 
                continue
            if (tt.is_table_control_char): 
                break
            if (tt.is_newline_before and tt != t0): 
                if (isinstance(tt, NumberToken)): 
                    break
                if ((isinstance(tt, TextToken)) and (isinstance(tt.previous, TextToken))): 
                    if (tt.previous.is_value(tt.term, None)): 
                        break
            if (BracketHelper.is_bracket(tt, False)): 
                continue
            tok = (ParticipantToken.M_ONTOLOGY.try_parse(tt, TerminParseAttr.NO) if ParticipantToken.M_ONTOLOGY is not None else None)
            if (tok is not None and (isinstance(tt.previous, TextToken))): 
                if (tt.previous.is_value("ЛИЦО", None)): 
                    return None
            if (tok is None): 
                if (add_typ1 is not None and ((MiscHelper.is_not_more_than_one_error(add_typ1, tt) or (((isinstance(tt, MetaToken)) and tt.begin_token.is_value(add_typ1, None)))))): 
                    if (typ_ is not None): 
                        if (not ParticipantToken.__is_types_equal(add_typ1, typ_)): 
                            break
                    typ_ = add_typ1
                    t1 = tt
                    continue
                if (add_typ2 is not None and ((MiscHelper.is_not_more_than_one_error(add_typ2, tt) or (((isinstance(tt, MetaToken)) and tt.begin_token.is_value(add_typ2, None)))))): 
                    if (typ_ is not None): 
                        if (not ParticipantToken.__is_types_equal(add_typ2, typ_)): 
                            break
                    typ_ = add_typ2
                    t1 = tt
                    continue
                if (tt.chars.is_letter): 
                    if (term1 is not None): 
                        tok1 = term1.try_parse(tt, TerminParseAttr.NO)
                        if (tok1 is not None): 
                            if (typ_ is not None): 
                                if (not ParticipantToken.__is_types_equal(add_typ1, typ_)): 
                                    break
                            typ_ = add_typ1
                            tt = tok1.end_token
                            t1 = tt
                            continue
                    if (term2 is not None): 
                        tok2 = term2.try_parse(tt, TerminParseAttr.NO)
                        if (tok2 is not None): 
                            if (typ_ is not None): 
                                if (not ParticipantToken.__is_types_equal(add_typ2, typ_)): 
                                    break
                            typ_ = add_typ2
                            tt = tok2.end_token
                            t1 = tt
                            continue
                    if (named and tt.get_morph_class_in_dictionary().is_noun): 
                        if (not tt.chars.is_all_lower or BracketHelper.is_bracket(tt.previous, True)): 
                            if (DecreeToken.is_keyword(tt, False) is None): 
                                val = tt.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                                if (typ_ is not None): 
                                    if (not ParticipantToken.__is_types_equal(typ_, val)): 
                                        break
                                typ_ = val
                                t1 = tt
                                continue
                if (named and typ_ is None and is_contract): 
                    if ((isinstance(tt, TextToken)) and tt.chars.is_cyrillic_letter and tt.chars.is_capital_upper): 
                        dc = tt.get_morph_class_in_dictionary()
                        if (dc.is_undefined or dc.is_noun): 
                            dt = DecreeToken.try_attach(tt, None, False)
                            ok = True
                            if (dt is not None): 
                                ok = False
                            elif (tt.is_value("СТОРОНА", None)): 
                                ok = False
                            if (ok): 
                                typ_ = tt.lemma
                                t1 = tt
                                continue
                        if (dc.is_adjective): 
                            npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                            if (npt is not None and len(npt.adjectives) > 0 and npt.noun.get_morph_class_in_dictionary().is_noun): 
                                typ_ = npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                                t1 = npt.end_token
                                continue
                if (tt == t): 
                    break
                if ((isinstance(tt, NumberToken)) or tt.is_char('.')): 
                    break
                if (tt.length_char < 4): 
                    if (typ_ is not None): 
                        continue
                break
            if (tok.termin.tag is None): 
                named = True
            else: 
                if (typ_ is not None): 
                    break
                if (tok.termin.canonic_text == "СТОРОНА"): 
                    tt1 = tt.next0_
                    if (tt1 is not None and tt1.is_hiphen): 
                        tt1 = tt1.next0_
                    if (not (isinstance(tt1, NumberToken))): 
                        break
                    if (tt1.is_newline_before): 
                        break
                    typ_ = "{0} {1}".format(tok.termin.canonic_text, tt1.value)
                    t1 = tt1
                else: 
                    typ_ = tok.termin.canonic_text
                    t1 = tok.end_token
                break
            tt = tok.end_token
        if (typ_ is None): 
            return None
        if (not named and t1 != t and not typ_.startswith("СТОРОНА")): 
            if (not ParticipantToken.__is_types_equal(typ_, add_typ1) and not ParticipantToken.__is_types_equal(typ_, add_typ2)): 
                return None
        if (BracketHelper.can_be_end_of_sequence(t1.next0_, False, None, False)): 
            t1 = t1.next0_
            if (not t.is_whitespace_before and BracketHelper.can_be_start_of_sequence(t.previous, False, False)): 
                t = t.previous
        elif (BracketHelper.can_be_start_of_sequence(t, False, False) and BracketHelper.can_be_end_of_sequence(t1.next0_, True, t, True)): 
            t1 = t1.next0_
        if (br and t1.next0_ is not None and BracketHelper.can_be_end_of_sequence(t1.next0_, False, None, False)): 
            t1 = t1.next0_
        res = ParticipantToken._new1574(t, t1, (ParticipantToken.Kinds.NAMEDAS if named else ParticipantToken.Kinds.PURE), typ_)
        if (t.is_char(':')): 
            res.begin_token = t.next0_
        return res
    
    @staticmethod
    def __is_types_equal(t1 : str, t2 : str) -> bool:
        if (t1 == t2): 
            return True
        if (t1 == "ЗАЙМОДАВЕЦ" or t1 == "ЗАИМОДАВЕЦ"): 
            t1 = "ЗАИМОДАТЕЛЬ"
        if (t2 == "ЗАЙМОДАВЕЦ" or t2 == "ЗАИМОДАВЕЦ"): 
            t2 = "ЗАИМОДАТЕЛЬ"
        if (t1 == "ПРОДАВЕЦ"): 
            t1 = "ПОСТАВЩИК"
        if (t2 == "ПРОДАВЕЦ"): 
            t2 = "ПОСТАВЩИК"
        if (t1 == "ПОКУПАТЕЛЬ"): 
            t1 = "ЗАКАЗЧИК"
        if (t2 == "ПОКУПАТЕЛЬ"): 
            t2 = "ЗАКАЗЧИК"
        return t1 == t2
    
    @staticmethod
    def try_attach_to_exist(t : 'Token', p1 : 'InstrumentParticipantReferent', p2 : 'InstrumentParticipantReferent') -> 'ReferentToken':
        if (t is None): 
            return None
        if (t.begin_char >= 7674 and (t.begin_char < 7680)): 
            pass
        pp = ParticipantToken.try_attach(t, p1, p2, False)
        p = None
        rt = None
        if (pp is None or pp.kind != ParticipantToken.Kinds.PURE): 
            pers = t.get_referent()
            if ((isinstance(pers, PersonReferent)) or (isinstance(pers, GeoReferent)) or (isinstance(pers, OrganizationReferent))): 
                if (p1 is not None and p1._contains_ref(pers)): 
                    p = p1
                elif (p2 is not None and p2._contains_ref(pers)): 
                    p = p2
                if (p is not None): 
                    rt = ReferentToken(p, t, t)
        else: 
            if (p1 is not None and ParticipantToken.__is_types_equal(pp.typ, p1.typ)): 
                p = p1
            elif (p2 is not None and ParticipantToken.__is_types_equal(pp.typ, p2.typ)): 
                p = p2
            if (p is not None): 
                rt = ReferentToken(p, pp.begin_token, pp.end_token)
                if (rt.begin_token.previous is not None and rt.begin_token.previous.is_value("ОТ", None)): 
                    rt.begin_token = rt.begin_token.previous
        if (rt is None): 
            return None
        if (rt.end_token.next0_ is not None and rt.end_token.next0_.is_char(':')): 
            rt1 = ParticipantToken.try_attach_requisites(rt.end_token.next0_.next0_, p, (p2 if p == p1 else p1), False)
            if (rt1 is not None): 
                rt1.begin_token = rt.begin_token
                return rt1
            rt.end_token = rt.end_token.next0_
        while rt.end_token.next0_ is not None and (isinstance(rt.end_token.next0_.get_referent(), OrganizationReferent)):
            org0_ = Utils.asObjectOrNull(rt.end_token.next0_.get_referent(), OrganizationReferent)
            if (rt.referent.find_slot(None, org0_, True) is not None): 
                rt.end_token = rt.end_token.next0_
                continue
            break
        return rt
    
    @staticmethod
    def try_attach_requisites(t : 'Token', cur : 'InstrumentParticipantReferent', other : 'InstrumentParticipantReferent', cant_be_empty : bool=False) -> 'ReferentToken':
        if (t is None or cur is None): 
            return None
        if (t.is_table_control_char): 
            return None
        err = 0
        spec_chars = 0
        rt = None
        t0 = t
        is_in_tab_cell = False
        cou = 0
        tt = t.next0_
        while tt is not None and (cou < 300): 
            if (tt.is_table_control_char): 
                is_in_tab_cell = True
                break
            tt = tt.next0_; cou += 1
        first_pass3778 = True
        while True:
            if first_pass3778: first_pass3778 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.begin_char == 8923): 
                pass
            if (t.is_table_control_char): 
                if (t != t0): 
                    if (rt is not None): 
                        rt.end_token = t.previous
                    elif (not cant_be_empty): 
                        rt = ReferentToken(cur, t0, t.previous)
                    break
                else: 
                    continue
            if ((t.is_char_of(":.") or t.is_value("М", None) or t.is_value("M", None)) or t.is_value("П", None)): 
                if (rt is not None): 
                    rt.end_token = t
                continue
            pp = ParticipantToken.try_attach_to_exist(t, cur, other)
            if (pp is not None): 
                if (pp.referent != cur): 
                    break
                if (rt is None): 
                    rt = ReferentToken(cur, t, t)
                rt.end_token = pp.end_token
                err = 0
                continue
            if (t.is_newline_before): 
                iii = InstrToken.parse(t, 0, None)
                if (iii is not None): 
                    if (iii.typ == ILTypes.APPENDIX): 
                        break
            if (t.whitespaces_before_count > 25 and not is_in_tab_cell): 
                if (t != t0): 
                    if (t.previous is not None and t.previous.is_char_of(",;")): 
                        pass
                    elif (t.newlines_before_count > 1): 
                        break
                if ((isinstance(t.get_referent(), PersonReferent)) or (isinstance(t.get_referent(), OrganizationReferent))): 
                    if (not cur._contains_ref(t.get_referent())): 
                        break
            if ((t.is_char_of(";:,.") or t.is_hiphen or t.morph.class0_.is_preposition) or t.morph.class0_.is_conjunction): 
                continue
            if (t.is_char_of("_/\\")): 
                spec_chars += 1
                if (spec_chars > 10 and rt is None): 
                    rt = ReferentToken(cur, t0, t)
                if (rt is not None): 
                    rt.end_token = t
                continue
            if (t.is_newline_before and (isinstance(t, NumberToken))): 
                break
            if (t.is_value("ОФИС", None)): 
                if (BracketHelper.can_be_start_of_sequence(t.next0_, True, False)): 
                    br = BracketHelper.try_parse(t.next0_, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        t = br.end_token
                        continue
                if ((isinstance(t.next0_, TextToken)) and not t.next0_.chars.is_all_lower): 
                    t = t.next0_
                continue
            r = t.get_referent()
            if ((((isinstance(r, PersonReferent)) or (isinstance(r, AddressReferent)) or (isinstance(r, UriReferent))) or (isinstance(r, OrganizationReferent)) or (isinstance(r, PhoneReferent))) or (isinstance(r, PersonIdentityReferent)) or (isinstance(r, BankDataReferent))): 
                if (other is not None and other.find_slot(None, r, True) is not None): 
                    if (not (isinstance(r, UriReferent))): 
                        break
                if (rt is None): 
                    rt = ReferentToken(cur, t, t)
                if (cur.find_slot(InstrumentParticipantReferent.ATTR_DELEGATE, r, True) is not None): 
                    pass
                else: 
                    cur.add_slot(InstrumentParticipantReferent.ATTR_REF, r, False, 0)
                rt.end_token = t
                err = 0
            else: 
                if ((isinstance(t, TextToken)) and t.length_char > 1): 
                    err += 1
                if (is_in_tab_cell and rt is not None): 
                    if (err > 300): 
                        break
                elif (err > 4): 
                    break
        return rt
    
    def attach_first(self, p : 'InstrumentParticipantReferent', min_char : int, max_char : int) -> 'ReferentToken':
        tt0 = self.begin_token
        refs = list()
        t = tt0.previous
        first_pass3779 = True
        while True:
            if first_pass3779: first_pass3779 = False
            else: t = t.previous
            if (not (t is not None and t.begin_char >= min_char)): break
            if (t.is_newline_after): 
                if (t.newlines_after_count > 1): 
                    break
                if (isinstance(t.next0_, NumberToken)): 
                    break
            tt = ParticipantToken.__try_attach_contract_ground(t, p, False)
            if (tt is not None): 
                continue
            r = t.get_referent()
            if (((((isinstance(r, OrganizationReferent)) or (isinstance(r, PhoneReferent)) or (isinstance(r, PersonReferent))) or (isinstance(r, PersonPropertyReferent)) or (isinstance(r, AddressReferent))) or (isinstance(r, UriReferent)) or (isinstance(r, PersonIdentityReferent))) or (isinstance(r, BankDataReferent))): 
                if (not r in refs): 
                    refs.insert(0, r)
                tt0 = t
        if (len(refs) > 0): 
            for r in refs: 
                if (r != refs[0] and (isinstance(refs[0], OrganizationReferent)) and (((isinstance(r, PersonReferent)) or (isinstance(r, PersonPropertyReferent))))): 
                    p.add_slot(InstrumentParticipantReferent.ATTR_DELEGATE, r, False, 0)
                else: 
                    p.add_slot(InstrumentParticipantReferent.ATTR_REF, r, False, 0)
        rt = ReferentToken(p, tt0, self.end_token)
        t = self.end_token.next0_
        if (BracketHelper.is_bracket(t, False)): 
            t = t.next0_
        if (t is not None and t.is_char(',')): 
            t = t.next0_
        first_pass3780 = True
        while True:
            if first_pass3780: first_pass3780 = False
            else: t = t.next0_
            if (not (t is not None and ((max_char == 0 or t.begin_char <= max_char)))): break
            if (t.is_value("СТОРОНА", None)): 
                break
            r = t.get_referent()
            if (((((isinstance(r, OrganizationReferent)) or (isinstance(r, PhoneReferent)) or (isinstance(r, PersonReferent))) or (isinstance(r, PersonPropertyReferent)) or (isinstance(r, AddressReferent))) or (isinstance(r, UriReferent)) or (isinstance(r, PersonIdentityReferent))) or (isinstance(r, BankDataReferent))): 
                if ((((isinstance(r, PersonPropertyReferent)) and t.next0_ is not None and t.next0_.is_comma) and (isinstance(t.next0_.next0_, ReferentToken)) and (isinstance(t.next0_.next0_.get_referent(), PersonReferent))) and not t.next0_.is_newline_after): 
                    pe = Utils.asObjectOrNull(t.next0_.next0_.get_referent(), PersonReferent)
                    pe.add_slot(PersonReferent.ATTR_ATTR, r, False, 0)
                    r = (pe)
                    t = t.next0_.next0_
                is_delegate = False
                if (t.previous.is_value("ЛИЦО", None) or t.previous.is_value("ИМЯ", None)): 
                    is_delegate = True
                if (t.previous.is_value("КОТОРЫЙ", None) and t.previous.previous is not None and ((t.previous.previous.is_value("ИМЯ", None) or t.previous.previous.is_value("ЛИЦО", None)))): 
                    is_delegate = True
                p.add_slot((InstrumentParticipantReferent.ATTR_DELEGATE if (((isinstance(r, PersonReferent)) or (isinstance(r, PersonPropertyReferent)))) and is_delegate else InstrumentParticipantReferent.ATTR_REF), r, False, 0)
                rt.end_token = t
                continue
            tt = ParticipantToken.__try_attach_contract_ground(t, p, False)
            if (tt is not None): 
                rt.end_token = tt
                t = rt.end_token
                if (rt.begin_char == tt.begin_char): 
                    rt.begin_token = tt
                continue
            if (t.is_value("В", None) and t.next0_ is not None and t.next0_.is_value("ЛИЦО", None)): 
                t = t.next0_
                continue
            if (t.is_value("ОТ", None) and t.next0_ is not None and t.next0_.is_value("ИМЯ", None)): 
                t = t.next0_
                continue
            if (t.is_value("ПО", None) and t.next0_ is not None and t.next0_.is_value("ПОРУЧЕНИЕ", None)): 
                t = t.next0_
                continue
            if (t.is_newline_before): 
                break
            if (t.get_morph_class_in_dictionary() == MorphClass.VERB): 
                if ((not t.is_value("УДОСТОВЕРЯТЬ", None) and not t.is_value("ПРОЖИВАТЬ", None) and not t.is_value("ЗАРЕГИСТРИРОВАТЬ", None)) and not t.is_value("ДЕЙСТВОВАТЬ", None)): 
                    break
            if (t.is_and and t.previous is not None and t.previous.is_comma): 
                break
            if (t.is_and and t.next0_.get_referent() is not None): 
                if (isinstance(t.next0_.get_referent(), OrganizationReferent)): 
                    break
                pe = Utils.asObjectOrNull(t.next0_.get_referent(), PersonReferent)
                if (pe is not None): 
                    has_ip = False
                    for s in pe.slots: 
                        if (s.type_name == PersonReferent.ATTR_ATTR): 
                            if (str(s.value).startswith("индивидуальный предприниматель")): 
                                has_ip = True
                                break
                    if (has_ip): 
                        break
        t = rt.begin_token
        while t is not None and t.end_char <= rt.end_char: 
            tt = ParticipantToken.__try_attach_contract_ground(t, p, True)
            if (tt is not None): 
                if (tt.end_char > rt.end_char): 
                    rt.end_token = tt
                t = tt
            t = t.next0_
        return rt
    
    @staticmethod
    def __try_attach_contract_ground(t : 'Token', ip : 'InstrumentParticipantReferent', can_be_passport : bool=False) -> 'Token':
        ok = False
        first_pass3781 = True
        while True:
            if first_pass3781: first_pass3781 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_char(',') or t.morph.class0_.is_preposition): 
                continue
            if (t.is_char('(')): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    t = br.end_token
                    continue
            if (t.is_value("ОСНОВАНИЕ", None) or t.is_value("ДЕЙСТВОВАТЬ", None) or t.is_value("ДЕЙСТВУЮЩИЙ", None)): 
                ok = True
                if (t.next0_ is not None and t.next0_.is_char('(')): 
                    br = BracketHelper.try_parse(t.next0_, BracketParseAttr.NO, 100)
                    if (br is not None and (br.length_char < 10)): 
                        t = br.end_token
                continue
            dr = Utils.asObjectOrNull(t.get_referent(), DecreeReferent)
            if (dr is not None): 
                ip.ground = dr
                return t
            pir = Utils.asObjectOrNull(t.get_referent(), PersonIdentityReferent)
            if (pir is not None and can_be_passport): 
                if (pir.typ is not None and not "паспорт" in pir.typ): 
                    ip.ground = pir
                    return t
            if (t.is_value("УСТАВ", None)): 
                ip.ground = t.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                return t
            if (t.is_value("ДОВЕРЕННОСТЬ", None)): 
                dts = DecreeToken.try_attach_list(t.next0_, None, 10, False)
                if (dts is None): 
                    has_spec = False
                    ttt = t.next0_
                    first_pass3782 = True
                    while True:
                        if first_pass3782: first_pass3782 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None and ((ttt.end_char - t.end_char) < 200))): break
                        if (ttt.is_comma): 
                            continue
                        if (ttt.is_value("УДОСТОВЕРИТЬ", None) or ttt.is_value("УДОСТОВЕРЯТЬ", None)): 
                            has_spec = True
                            continue
                        dt = DecreeToken.try_attach(ttt, None, False)
                        if (dt is not None): 
                            if (dt.typ == DecreeToken.ItemType.DATE or dt.typ == DecreeToken.ItemType.NUMBER): 
                                dts = DecreeToken.try_attach_list(ttt, None, 10, False)
                                break
                        npt = NounPhraseHelper.try_parse(ttt, NounPhraseParseAttr.NO, 0, None)
                        if (npt is not None): 
                            if (npt.end_token.is_value("НОТАРИУС", None)): 
                                ttt = npt.end_token
                                has_spec = True
                                continue
                        if (ttt.get_referent() is not None): 
                            if (has_spec): 
                                continue
                        break
                if (dts is not None and len(dts) > 0): 
                    t0 = t
                    dr = DecreeReferent()
                    dr.typ = "ДОВЕРЕННОСТЬ"
                    for d in dts: 
                        if (d.typ == DecreeToken.ItemType.DATE): 
                            dr._add_date(d)
                            t = d.end_token
                        elif (d.typ == DecreeToken.ItemType.NUMBER): 
                            dr._add_number(d)
                            t = d.end_token
                        else: 
                            break
                    ad = t.kit.get_analyzer_data_by_analyzer_name(InstrumentAnalyzer.ANALYZER_NAME)
                    ip.ground = ad.register_referent(dr)
                    rt = ReferentToken(Utils.asObjectOrNull(ip.ground, Referent), t0, t)
                    t.kit.embed_token(rt)
                    return rt
                ip.ground = "ДОВЕРЕННОСТЬ"
                return t
            break
        return None
    
    @staticmethod
    def get_doc_types(name : str, name2 : str) -> typing.List[str]:
        res = list()
        if (name is None): 
            return res
        if (name == "АРЕНДОДАТЕЛЬ"): 
            res.append("ДОГОВОР АРЕНДЫ")
            res.append("ДОГОВОР СУБАРЕНДЫ")
        elif (name == "АРЕНДАТОР"): 
            res.append("ДОГОВОР АРЕНДЫ")
        elif (name == "СУБАРЕНДАТОР"): 
            res.append("ДОГОВОР СУБАРЕНДЫ")
        elif (name == "НАЙМОДАТЕЛЬ" or name == "НАНИМАТЕЛЬ"): 
            res.append("ДОГОВОР НАЙМА")
        elif (name == "АГЕНТ" or name == "ПРИНЦИПАЛ"): 
            res.append("АГЕНТСКИЙ ДОГОВОР")
        elif (name == "ПРОДАВЕЦ" or name == "ПОКУПАТЕЛЬ"): 
            res.append("ДОГОВОР КУПЛИ-ПРОДАЖИ")
        elif (name == "ЗАКАЗЧИК" or name == "ИСПОЛНИТЕЛЬ" or LanguageHelper.ends_with(name, "ПОДРЯДЧИК")): 
            res.append("ДОГОВОР УСЛУГ")
        elif (name == "ПОСТАВЩИК"): 
            res.append("ДОГОВОР ПОСТАВКИ")
        elif (name == "ЛИЦЕНЗИАР" or name == "ЛИЦЕНЗИАТ"): 
            res.append("ЛИЦЕНЗИОННЫЙ ДОГОВОР")
        elif (name == "СТРАХОВЩИК" or name == "СТРАХОВАТЕЛЬ"): 
            res.append("ДОГОВОР СТРАХОВАНИЯ")
        if (name2 is None): 
            return res
        tmp = ParticipantToken.get_doc_types(name2, None)
        for i in range(len(res) - 1, -1, -1):
            if (not res[i] in tmp): 
                del res[i]
        return res
    
    M_ONTOLOGY = None
    
    @staticmethod
    def initialize() -> None:
        if (ParticipantToken.M_ONTOLOGY is not None): 
            return
        ParticipantToken.M_ONTOLOGY = TerminCollection()
        for s in ["АРЕНДОДАТЕЛЬ", "АРЕНДАТОР", "СУБАРЕНДАТОР", "НАЙМОДАТЕЛЬ", "НАНИМАТЕЛЬ", "АГЕНТ", "ПРИНЦИПАЛ", "ПРОДАВЕЦ", "ПОКУПАТЕЛЬ", "ЗАКАЗЧИК", "ИСПОЛНИТЕЛЬ", "ПОСТАВЩИК", "ПОДРЯДЧИК", "СУБПОДРЯДЧИК", "СТОРОНА", "ЛИЦЕНЗИАР", "ЛИЦЕНЗИАТ", "СТРАХОВЩИК", "СТРАХОВАТЕЛЬ", "ПРОВАЙДЕР", "АБОНЕНТ", "ЗАСТРОЙЩИК", "УЧАСТНИК ДОЛЕВОГО СТРОИТЕЛЬСТВА", "КЛИЕНТ", "ЗАЕМЩИК", "УПРАВЛЯЮЩИЙ"]: 
            ParticipantToken.M_ONTOLOGY.add(Termin._new100(s, ParticipantToken.M_ONTOLOGY))
        t = Termin._new100("ГЕНПОДРЯДЧИК", ParticipantToken.M_ONTOLOGY)
        t.add_variant("ГЕНЕРАЛЬНЫЙ ПОДРЯДЧИК", False)
        ParticipantToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ЗАИМОДАТЕЛЬ", ParticipantToken.M_ONTOLOGY)
        t.add_variant("ЗАЙМОДАТЕЛЬ", False)
        t.add_variant("ЗАЙМОДАВЕЦ", False)
        t.add_variant("ЗАИМОДАВЕЦ", False)
        ParticipantToken.M_ONTOLOGY.add(t)
        t = Termin("ИМЕНУЕМЫЙ")
        t.add_variant("ИМЕНОВАТЬСЯ", False)
        t.add_variant("ИМЕНУЕМ", False)
        t.add_variant("ДАЛЬНЕЙШИЙ", False)
        t.add_variant("ДАЛЕЕ", False)
        t.add_variant("ДАЛЕЕ ПО ТЕКСТУ", False)
        ParticipantToken.M_ONTOLOGY.add(t)
    
    @staticmethod
    def _new1486(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'ParticipantToken':
        res = ParticipantToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1569(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Kinds') -> 'ParticipantToken':
        res = ParticipantToken(_arg1, _arg2)
        res.kind = _arg3
        return res
    
    @staticmethod
    def _new1574(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Kinds', _arg4 : str) -> 'ParticipantToken':
        res = ParticipantToken(_arg1, _arg2)
        res.kind = _arg3
        res.typ = _arg4
        return res