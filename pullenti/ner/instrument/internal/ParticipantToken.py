# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

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
from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
from pullenti.ner.bank.BankDataReferent import BankDataReferent
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.BracketHelper import BracketHelper

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
                print("; {0}".format(p.toString(True, None, 0)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def tryAttach(t : 'Token', p1 : 'InstrumentParticipant'=None, p2 : 'InstrumentParticipant'=None, is_contract : bool=False) -> 'ParticipantToken':
        if (t is None): 
            return None
        tt = t
        br = False
        if (p1 is None and p2 is None and is_contract): 
            r1 = t.getReferent()
            if ((r1 is not None and t.next0_ is not None and t.next0_.is_comma_and) and (isinstance(t.next0_.next0_, ReferentToken))): 
                r2 = t.next0_.next0_.getReferent()
                if (r1.type_name == r2.type_name): 
                    ttt = t.next0_.next0_.next0_
                    refs = list()
                    refs.append(r1)
                    refs.append(r2)
                    first_pass3027 = True
                    while True:
                        if first_pass3027: first_pass3027 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        if ((ttt.is_comma_and and ttt.next0_ is not None and ttt.next0_.getReferent() is not None) and ttt.next0_.getReferent().type_name == r1.type_name): 
                            ttt = ttt.next0_
                            if (not ttt.getReferent() in refs): 
                                refs.append(ttt.getReferent())
                            continue
                        break
                    first_pass3028 = True
                    while True:
                        if first_pass3028: first_pass3028 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        if (ttt.is_comma or ttt.morph.class0_.is_preposition): 
                            continue
                        if ((ttt.isValue("ИМЕНОВАТЬ", None) or ttt.isValue("ДАЛЬНЕЙШИЙ", None) or ttt.isValue("ДАЛЕЕ", None)) or ttt.isValue("ТЕКСТ", None)): 
                            continue
                        if (ttt.isValue("ДОГОВАРИВАТЬСЯ", None)): 
                            continue
                        npt = NounPhraseHelper.tryParse(ttt, NounPhraseParseAttr.NO, 0)
                        if (npt is not None and npt.noun.isValue("СТОРОНА", None) and npt.morph.number != MorphNumber.SINGULAR): 
                            re = ParticipantToken._new1481(t, npt.end_token, ParticipantToken.Kinds.NAMEDASPARTS)
                            re.parts = refs
                            return re
                        break
            if ((isinstance(r1, OrganizationReferent)) or (isinstance(r1, PersonReferent))): 
                has_br = False
                has_named = False
                if (isinstance(r1, PersonReferent)): 
                    if (t.previous is not None and t.previous.isValue("ЛИЦО", None)): 
                        return None
                elif (t.previous is not None and ((t.previous.isValue("ВЫДАВАТЬ", None) or t.previous.isValue("ВЫДАТЬ", None)))): 
                    return None
                ttt = (t).begin_token
                while ttt is not None and (ttt.end_char < t.end_char): 
                    if (ttt.isChar('(')): 
                        has_br = True
                    elif ((ttt.isValue("ИМЕНОВАТЬ", None) or ttt.isValue("ДАЛЬНЕЙШИЙ", None) or ttt.isValue("ДАЛЕЕ", None)) or ttt.isValue("ТЕКСТ", None)): 
                        has_named = True
                    elif ((ttt.is_comma or ttt.morph.class0_.is_preposition or ttt.is_hiphen) or ttt.isChar(':')): 
                        pass
                    elif (isinstance(ttt, ReferentToken)): 
                        pass
                    elif (has_br or has_named): 
                        npt = NounPhraseHelper.tryParse(ttt, NounPhraseParseAttr.REFERENTCANBENOUN, 0)
                        if (npt is None): 
                            break
                        if (has_br): 
                            if (npt.end_token.next0_ is None or not npt.end_token.next0_.isChar(')')): 
                                break
                        if (not has_named): 
                            if (ParticipantToken.M_ONTOLOGY.tryParse(ttt, TerminParseAttr.NO) is None): 
                                break
                        re = ParticipantToken._new1481(t, t, ParticipantToken.Kinds.NAMEDAS)
                        re.typ = npt.getNormalCaseText(None, True, MorphGender.UNDEFINED, False)
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
                first_pass3029 = True
                while True:
                    if first_pass3029: first_pass3029 = False
                    else: ttt = ttt.next0_
                    if (not (ttt is not None)): break
                    if ((isinstance(ttt, NumberToken)) and (isinstance(ttt.next0_, TextToken)) and (ttt.next0_).term == "СТОРОНЫ"): 
                        ttt = ttt.next0_
                        end_side = ttt
                        if (ttt.next0_ is not None and ttt.next0_.is_comma): 
                            ttt = ttt.next0_
                        if (ttt.next0_ is not None and ttt.next0_.is_and): 
                            break
                    if (brr is not None and ttt.begin_char > brr.end_char): 
                        brr = (None)
                    if (BracketHelper.canBeStartOfSequence(ttt, False, False)): 
                        brr = BracketHelper.tryParse(ttt, BracketParseAttr.NO, 100)
                        if (brr is not None and (brr.length_char < 7) and ttt.isChar('(')): 
                            ttt = brr.end_token
                            brr = (None)
                            continue
                    elif ((ttt.isValue("ИМЕНОВАТЬ", None) or ttt.isValue("ДАЛЬНЕЙШИЙ", None) or ttt.isValue("ДАЛЕЕ", None)) or ttt.isValue("ТЕКСТ", None)): 
                        has_named = True
                    elif ((ttt.is_comma or ttt.morph.class0_.is_preposition or ttt.is_hiphen) or ttt.isChar(':')): 
                        pass
                    elif (brr is not None or has_named): 
                        if (BracketHelper.canBeStartOfSequence(ttt, True, False)): 
                            ttt = ttt.next0_
                        npt = NounPhraseHelper.tryParse(ttt, NounPhraseParseAttr.REFERENTCANBENOUN, 0)
                        typ22 = None
                        if (npt is not None): 
                            ttt = npt.end_token
                            if (npt.end_token.isValue("ДОГОВОР", None)): 
                                continue
                        else: 
                            ttok = None
                            if (isinstance(ttt, MetaToken)): 
                                ttok = ParticipantToken.M_ONTOLOGY.tryParse((ttt).begin_token, TerminParseAttr.NO)
                            if (ttok is not None): 
                                typ22 = ttok.termin.canonic_text
                            elif (has_named and ttt.morph.class0_.is_adjective): 
                                typ22 = ttt.getNormalCaseText(MorphClass.ADJECTIVE, False, MorphGender.UNDEFINED, False)
                            elif (brr is not None): 
                                continue
                            else: 
                                break
                        if (BracketHelper.canBeEndOfSequence(ttt.next0_, True, None, False)): 
                            ttt = ttt.next0_
                        if (brr is not None): 
                            if (ttt.next0_ is None): 
                                ttt = brr.end_token
                                continue
                            ttt = ttt.next0_
                        if (not has_named and typ22 is None): 
                            if (ParticipantToken.M_ONTOLOGY.tryParse(npt.begin_token, TerminParseAttr.NO) is None): 
                                break
                        re = ParticipantToken._new1481(t, ttt, ParticipantToken.Kinds.NAMEDAS)
                        re.typ = (Utils.ifNotNull(typ22, npt.getNormalCaseText(None, True, MorphGender.UNDEFINED, False)))
                        re.parts = list()
                        re.parts.append(r1)
                        return re
                    elif ((ttt.isValue("ЗАРЕГИСТРИРОВАННЫЙ", None) or ttt.isValue("КАЧЕСТВО", None) or ttt.isValue("ПРОЖИВАЮЩИЙ", None)) or ttt.isValue("ЗАРЕГ", None)): 
                        pass
                    elif (ttt.getReferent() == r1): 
                        pass
                    elif ((isinstance(ttt.getReferent(), PersonIdentityReferent)) or (isinstance(ttt.getReferent(), AddressReferent))): 
                        if (add_refs is None): 
                            add_refs = list()
                        add_refs.append(ttt.getReferent())
                    else: 
                        prr = ttt.kit.processReferent("PERSONPROPERTY", ttt)
                        if (prr is not None): 
                            ttt = prr.end_token
                            continue
                        if (isinstance(ttt.getReferent(), GeoReferent)): 
                            continue
                        npt = NounPhraseHelper.tryParse(ttt, NounPhraseParseAttr.NO, 0)
                        if (npt is not None): 
                            if ((npt.noun.isValue("МЕСТО", None) or npt.noun.isValue("ЖИТЕЛЬСТВО", None) or npt.noun.isValue("ПРЕДПРИНИМАТЕЛЬ", None)) or npt.noun.isValue("ПОЛ", None) or npt.noun.isValue("РОЖДЕНИЕ", None)): 
                                ttt = npt.end_token
                                continue
                        if (ttt.is_newline_before): 
                            break
                        if (ttt.length_char < 3): 
                            continue
                        mc = ttt.getMorphClassInDictionary()
                        if (mc.is_adverb or mc.is_adjective): 
                            continue
                        if (ttt.chars.is_all_upper): 
                            continue
                        break
                if (end_side is not None or ((add_refs is not None and t.previous is not None and t.previous.is_and))): 
                    re = ParticipantToken._new1481(t, Utils.ifNotNull(end_side, t), ParticipantToken.Kinds.NAMEDAS)
                    re.typ = (None)
                    re.parts = list()
                    re.parts.append(r1)
                    if (add_refs is not None): 
                        re.parts.extend(add_refs)
                    return re
            too = ParticipantToken.M_ONTOLOGY.tryParse(t, TerminParseAttr.NO)
            if (too is not None): 
                if ((isinstance(t.previous, TextToken)) and t.previous.isValue("ЛИЦО", None)): 
                    too = (None)
            if (too is not None and too.termin.tag is not None and too.termin.canonic_text != "СТОРОНА"): 
                tt1 = too.end_token.next0_
                if (tt1 is not None): 
                    if (tt1.is_hiphen or tt1.isChar(':')): 
                        tt1 = tt1.next0_
                if (isinstance(tt1, ReferentToken)): 
                    r1 = tt1.getReferent()
                    if ((isinstance(r1, PersonReferent)) or (isinstance(r1, OrganizationReferent))): 
                        re = ParticipantToken._new1481(t, tt1, ParticipantToken.Kinds.NAMEDAS)
                        re.typ = too.termin.canonic_text
                        re.parts = list()
                        re.parts.append(r1)
                        return re
        add_typ1 = (None if p1 is None else p1.typ)
        add_typ2 = (None if p2 is None else p2.typ)
        if (BracketHelper.canBeStartOfSequence(tt, False, False) and tt.next0_ is not None): 
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
        first_pass3030 = True
        while True:
            if first_pass3030: first_pass3030 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.morph.class0_.is_preposition and typ_ is not None): 
                continue
            if (tt.isCharOf("(:)") or tt.is_hiphen): 
                continue
            if (tt.is_table_control_char): 
                break
            if (tt.is_newline_before and tt != t0): 
                if (isinstance(tt, NumberToken)): 
                    break
                if ((isinstance(tt, TextToken)) and (isinstance(tt.previous, TextToken))): 
                    if (tt.previous.isValue((tt).term, None)): 
                        break
            if (BracketHelper.isBracket(tt, False)): 
                continue
            tok = (ParticipantToken.M_ONTOLOGY.tryParse(tt, TerminParseAttr.NO) if ParticipantToken.M_ONTOLOGY is not None else None)
            if (tok is not None and (isinstance(tt.previous, TextToken))): 
                if (tt.previous.isValue("ЛИЦО", None)): 
                    return None
            if (tok is None): 
                if (add_typ1 is not None and ((MiscHelper.isNotMoreThanOneError(add_typ1, tt) or ((((isinstance(tt, MetaToken))) and (tt).begin_token.isValue(add_typ1, None)))))): 
                    if (typ_ is not None): 
                        if (not ParticipantToken.__isTypesEqual(add_typ1, typ_)): 
                            break
                    typ_ = add_typ1
                    t1 = tt
                    continue
                if (add_typ2 is not None and ((MiscHelper.isNotMoreThanOneError(add_typ2, tt) or ((((isinstance(tt, MetaToken))) and (tt).begin_token.isValue(add_typ2, None)))))): 
                    if (typ_ is not None): 
                        if (not ParticipantToken.__isTypesEqual(add_typ2, typ_)): 
                            break
                    typ_ = add_typ2
                    t1 = tt
                    continue
                if (tt.chars.is_letter): 
                    if (term1 is not None): 
                        tok1 = term1.tryParse(tt, TerminParseAttr.NO)
                        if (tok1 is not None): 
                            if (typ_ is not None): 
                                if (not ParticipantToken.__isTypesEqual(add_typ1, typ_)): 
                                    break
                            typ_ = add_typ1
                            tt = tok1.end_token
                            t1 = tt
                            continue
                    if (term2 is not None): 
                        tok2 = term2.tryParse(tt, TerminParseAttr.NO)
                        if (tok2 is not None): 
                            if (typ_ is not None): 
                                if (not ParticipantToken.__isTypesEqual(add_typ2, typ_)): 
                                    break
                            typ_ = add_typ2
                            tt = tok2.end_token
                            t1 = tt
                            continue
                    if (named and tt.getMorphClassInDictionary().is_noun): 
                        if (not tt.chars.is_all_lower or BracketHelper.isBracket(tt.previous, True)): 
                            if (DecreeToken.isKeyword(tt, False) is None): 
                                val = tt.getNormalCaseText(MorphClass.NOUN, True, MorphGender.UNDEFINED, False)
                                if (typ_ is not None): 
                                    if (not ParticipantToken.__isTypesEqual(typ_, val)): 
                                        break
                                typ_ = val
                                t1 = tt
                                continue
                if (named and typ_ is None and is_contract): 
                    if ((isinstance(tt, TextToken)) and tt.chars.is_cyrillic_letter and tt.chars.is_capital_upper): 
                        dc = tt.getMorphClassInDictionary()
                        if (dc.is_undefined or dc.is_noun): 
                            dt = DecreeToken.tryAttach(tt, None, False)
                            ok = True
                            if (dt is not None): 
                                ok = False
                            elif (tt.isValue("СТОРОНА", None)): 
                                ok = False
                            if (ok): 
                                typ_ = (tt).getLemma()
                                t1 = tt
                                continue
                        if (dc.is_adjective): 
                            npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
                            if (npt is not None and len(npt.adjectives) > 0 and npt.noun.getMorphClassInDictionary().is_noun): 
                                typ_ = npt.getNormalCaseText(None, True, MorphGender.UNDEFINED, False)
                                t1 = npt.end_token
                                continue
                if (tt == t): 
                    break
                if ((isinstance(tt, NumberToken)) or tt.isChar('.')): 
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
                    if (not ((isinstance(tt1, NumberToken)))): 
                        break
                    if (tt1.is_newline_before): 
                        break
                    typ_ = "{0} {1}".format(tok.termin.canonic_text, (tt1).value)
                    t1 = tt1
                else: 
                    typ_ = tok.termin.canonic_text
                    t1 = tok.end_token
                break
            tt = tok.end_token
        if (typ_ is None): 
            return None
        if (not named and t1 != t and not typ_.startswith("СТОРОНА")): 
            if (not ParticipantToken.__isTypesEqual(typ_, add_typ1) and not ParticipantToken.__isTypesEqual(typ_, add_typ2)): 
                return None
        if (BracketHelper.canBeEndOfSequence(t1.next0_, False, None, False)): 
            t1 = t1.next0_
            if (not t.is_whitespace_before and BracketHelper.canBeStartOfSequence(t.previous, False, False)): 
                t = t.previous
        elif (BracketHelper.canBeStartOfSequence(t, False, False) and BracketHelper.canBeEndOfSequence(t1.next0_, True, t, True)): 
            t1 = t1.next0_
        if (br and t1.next0_ is not None and BracketHelper.canBeEndOfSequence(t1.next0_, False, None, False)): 
            t1 = t1.next0_
        res = ParticipantToken._new1486(t, t1, (ParticipantToken.Kinds.NAMEDAS if named else ParticipantToken.Kinds.PURE), typ_)
        if (t.isChar(':')): 
            res.begin_token = t.next0_
        return res
    
    @staticmethod
    def __isTypesEqual(t1 : str, t2 : str) -> bool:
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
    def tryAttachToExist(t : 'Token', p1 : 'InstrumentParticipant', p2 : 'InstrumentParticipant') -> 'ReferentToken':
        if (t is None): 
            return None
        if (t.begin_char >= 7674 and (t.begin_char < 7680)): 
            pass
        pp = ParticipantToken.tryAttach(t, p1, p2, False)
        p = None
        rt = None
        if (pp is None or pp.kind != ParticipantToken.Kinds.PURE): 
            pers = t.getReferent()
            if ((isinstance(pers, PersonReferent)) or (isinstance(pers, GeoReferent)) or (isinstance(pers, OrganizationReferent))): 
                if (p1 is not None and p1._containsRef(pers)): 
                    p = p1
                elif (p2 is not None and p2._containsRef(pers)): 
                    p = p2
                if (p is not None): 
                    rt = ReferentToken(p, t, t)
        else: 
            if (p1 is not None and ParticipantToken.__isTypesEqual(pp.typ, p1.typ)): 
                p = p1
            elif (p2 is not None and ParticipantToken.__isTypesEqual(pp.typ, p2.typ)): 
                p = p2
            if (p is not None): 
                rt = ReferentToken(p, pp.begin_token, pp.end_token)
                if (rt.begin_token.previous is not None and rt.begin_token.previous.isValue("ОТ", None)): 
                    rt.begin_token = rt.begin_token.previous
        if (rt is None): 
            return None
        if (rt.end_token.next0_ is not None and rt.end_token.next0_.isChar(':')): 
            rt1 = ParticipantToken.tryAttachRequisites(rt.end_token.next0_.next0_, p, (p2 if p == p1 else p1), False)
            if (rt1 is not None): 
                rt1.begin_token = rt.begin_token
                return rt1
            rt.end_token = rt.end_token.next0_
        while rt.end_token.next0_ is not None and (isinstance(rt.end_token.next0_.getReferent(), OrganizationReferent)):
            org0_ = Utils.asObjectOrNull(rt.end_token.next0_.getReferent(), OrganizationReferent)
            if (rt.referent.findSlot(None, org0_, True) is not None): 
                rt.end_token = rt.end_token.next0_
                continue
            break
        return rt
    
    @staticmethod
    def tryAttachRequisites(t : 'Token', cur : 'InstrumentParticipant', other : 'InstrumentParticipant', cant_be_empty : bool=False) -> 'ReferentToken':
        if (t is None or cur is None): 
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
        first_pass3031 = True
        while True:
            if first_pass3031: first_pass3031 = False
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
            if ((t.isCharOf(":.") or t.isValue("М", None) or t.isValue("M", None)) or t.isValue("П", None)): 
                if (rt is not None): 
                    rt.end_token = t
                continue
            pp = ParticipantToken.tryAttachToExist(t, cur, other)
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
                    if (t.previous is not None and t.previous.isCharOf(",;")): 
                        pass
                    elif (t.newlines_before_count > 1): 
                        break
                if ((isinstance(t.getReferent(), PersonReferent)) or (isinstance(t.getReferent(), OrganizationReferent))): 
                    if (not cur._containsRef(t.getReferent())): 
                        break
            if ((t.isCharOf(";:,.") or t.is_hiphen or t.morph.class0_.is_preposition) or t.morph.class0_.is_conjunction): 
                continue
            if (t.isCharOf("_/\\")): 
                spec_chars += 1
                if ((spec_chars) > 10 and rt is None): 
                    rt = ReferentToken(cur, t0, t)
                if (rt is not None): 
                    rt.end_token = t
                continue
            if (t.is_newline_before and (isinstance(t, NumberToken))): 
                break
            if (t.isValue("ОФИС", None)): 
                if (BracketHelper.canBeStartOfSequence(t.next0_, True, False)): 
                    br = BracketHelper.tryParse(t.next0_, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        t = br.end_token
                        continue
                if ((isinstance(t.next0_, TextToken)) and not t.next0_.chars.is_all_lower): 
                    t = t.next0_
                continue
            r = t.getReferent()
            if ((((isinstance(r, PersonReferent)) or (isinstance(r, AddressReferent)) or (isinstance(r, UriReferent))) or (isinstance(r, OrganizationReferent)) or (isinstance(r, PhoneReferent))) or (isinstance(r, PersonIdentityReferent)) or (isinstance(r, BankDataReferent))): 
                if (other is not None and other.findSlot(None, r, True) is not None): 
                    if (not ((isinstance(r, UriReferent)))): 
                        break
                if (rt is None): 
                    rt = ReferentToken(cur, t, t)
                if (cur.findSlot(InstrumentParticipant.ATTR_DELEGATE, r, True) is not None): 
                    pass
                else: 
                    cur.addSlot(InstrumentParticipant.ATTR_REF, r, False, 0)
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
    
    def attachFirst(self, p : 'InstrumentParticipant', min_char : int, max_char : int) -> 'ReferentToken':
        tt0 = self.begin_token
        refs = list()
        t = tt0.previous
        first_pass3032 = True
        while True:
            if first_pass3032: first_pass3032 = False
            else: t = t.previous
            if (not (t is not None and t.begin_char >= min_char)): break
            if (t.is_newline_after): 
                if (t.newlines_after_count > 1): 
                    break
                if (isinstance(t.next0_, NumberToken)): 
                    break
            tt = ParticipantToken.__tryAttachContractGround(t, p, False)
            if (tt is not None): 
                continue
            r = t.getReferent()
            if (((((isinstance(r, OrganizationReferent)) or (isinstance(r, PhoneReferent)) or (isinstance(r, PersonReferent))) or (isinstance(r, PersonPropertyReferent)) or (isinstance(r, AddressReferent))) or (isinstance(r, UriReferent)) or (isinstance(r, PersonIdentityReferent))) or (isinstance(r, BankDataReferent))): 
                if (not r in refs): 
                    refs.insert(0, r)
                tt0 = t
        if (len(refs) > 0): 
            for r in refs: 
                if (r != refs[0] and (isinstance(refs[0], OrganizationReferent)) and (((isinstance(r, PersonReferent)) or (isinstance(r, PersonPropertyReferent))))): 
                    p.addSlot(InstrumentParticipant.ATTR_DELEGATE, r, False, 0)
                else: 
                    p.addSlot(InstrumentParticipant.ATTR_REF, r, False, 0)
        rt = ReferentToken(p, tt0, self.end_token)
        t = self.end_token.next0_
        if (BracketHelper.isBracket(t, False)): 
            t = t.next0_
        if (t is not None and t.isChar(',')): 
            t = t.next0_
        first_pass3033 = True
        while True:
            if first_pass3033: first_pass3033 = False
            else: t = t.next0_
            if (not (t is not None and ((max_char == 0 or t.begin_char <= max_char)))): break
            if (t.isValue("СТОРОНА", None)): 
                break
            r = t.getReferent()
            if (((((isinstance(r, OrganizationReferent)) or (isinstance(r, PhoneReferent)) or (isinstance(r, PersonReferent))) or (isinstance(r, PersonPropertyReferent)) or (isinstance(r, AddressReferent))) or (isinstance(r, UriReferent)) or (isinstance(r, PersonIdentityReferent))) or (isinstance(r, BankDataReferent))): 
                if ((((isinstance(r, PersonPropertyReferent)) and t.next0_ is not None and t.next0_.is_comma) and (isinstance(t.next0_.next0_, ReferentToken)) and (isinstance(t.next0_.next0_.getReferent(), PersonReferent))) and not t.next0_.is_newline_after): 
                    pe = Utils.asObjectOrNull(t.next0_.next0_.getReferent(), PersonReferent)
                    pe.addSlot(PersonReferent.ATTR_ATTR, r, False, 0)
                    r = (pe)
                    t = t.next0_.next0_
                is_delegate = False
                if (t.previous.isValue("ЛИЦО", None) or t.previous.isValue("ИМЯ", None)): 
                    is_delegate = True
                if (t.previous.isValue("КОТОРЫЙ", None) and t.previous.previous is not None and ((t.previous.previous.isValue("ИМЯ", None) or t.previous.previous.isValue("ЛИЦО", None)))): 
                    is_delegate = True
                p.addSlot((InstrumentParticipant.ATTR_DELEGATE if (((isinstance(r, PersonReferent)) or (isinstance(r, PersonPropertyReferent)))) and is_delegate else InstrumentParticipant.ATTR_REF), r, False, 0)
                rt.end_token = t
                continue
            tt = ParticipantToken.__tryAttachContractGround(t, p, False)
            if (tt is not None): 
                rt.end_token = tt
                t = rt.end_token
                if (rt.begin_char == tt.begin_char): 
                    rt.begin_token = tt
                continue
            if (t.isValue("В", None) and t.next0_ is not None and t.next0_.isValue("ЛИЦО", None)): 
                t = t.next0_
                continue
            if (t.isValue("ОТ", None) and t.next0_ is not None and t.next0_.isValue("ИМЯ", None)): 
                t = t.next0_
                continue
            if (t.isValue("ПО", None) and t.next0_ is not None and t.next0_.isValue("ПОРУЧЕНИЕ", None)): 
                t = t.next0_
                continue
            if (t.is_newline_before): 
                break
            if (t.getMorphClassInDictionary() == MorphClass.VERB): 
                if ((not t.isValue("УДОСТОВЕРЯТЬ", None) and not t.isValue("ПРОЖИВАТЬ", None) and not t.isValue("ЗАРЕГИСТРИРОВАТЬ", None)) and not t.isValue("ДЕЙСТВОВАТЬ", None)): 
                    break
            if (t.is_and and t.previous is not None and t.previous.is_comma): 
                break
            if (t.is_and and t.next0_.getReferent() is not None): 
                if (isinstance(t.next0_.getReferent(), OrganizationReferent)): 
                    break
                pe = Utils.asObjectOrNull(t.next0_.getReferent(), PersonReferent)
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
            tt = ParticipantToken.__tryAttachContractGround(t, p, True)
            if (tt is not None): 
                if (tt.end_char > rt.end_char): 
                    rt.end_token = tt
                t = tt
            t = t.next0_
        return rt
    
    @staticmethod
    def __tryAttachContractGround(t : 'Token', ip : 'InstrumentParticipant', can_be_passport : bool=False) -> 'Token':
        ok = False
        first_pass3034 = True
        while True:
            if first_pass3034: first_pass3034 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.isChar(',') or t.morph.class0_.is_preposition): 
                continue
            if (t.isChar('(')): 
                br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    t = br.end_token
                    continue
            if (t.isValue("ОСНОВАНИЕ", None) or t.isValue("ДЕЙСТВОВАТЬ", None) or t.isValue("ДЕЙСТВУЮЩИЙ", None)): 
                ok = True
                if (t.next0_ is not None and t.next0_.isChar('(')): 
                    br = BracketHelper.tryParse(t.next0_, BracketParseAttr.NO, 100)
                    if (br is not None and (br.length_char < 10)): 
                        t = br.end_token
                continue
            dr = Utils.asObjectOrNull(t.getReferent(), DecreeReferent)
            if (dr is not None): 
                ip.ground = dr
                return t
            pir = Utils.asObjectOrNull(t.getReferent(), PersonIdentityReferent)
            if (pir is not None and can_be_passport): 
                if (pir.typ is not None and not "паспорт" in pir.typ): 
                    ip.ground = pir
                    return t
            if (t.isValue("УСТАВ", None)): 
                ip.ground = t.getNormalCaseText(MorphClass.NOUN, True, MorphGender.UNDEFINED, False)
                return t
            if (t.isValue("ДОВЕРЕННОСТЬ", None)): 
                dts = DecreeToken.tryAttachList(t.next0_, None, 10, False)
                if (dts is None): 
                    has_spec = False
                    ttt = t.next0_
                    first_pass3035 = True
                    while True:
                        if first_pass3035: first_pass3035 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None and ((ttt.end_char - t.end_char) < 200))): break
                        if (ttt.is_comma): 
                            continue
                        if (ttt.isValue("УДОСТОВЕРИТЬ", None) or ttt.isValue("УДОСТОВЕРЯТЬ", None)): 
                            has_spec = True
                            continue
                        dt = DecreeToken.tryAttach(ttt, None, False)
                        if (dt is not None): 
                            if (dt.typ == DecreeToken.ItemType.DATE or dt.typ == DecreeToken.ItemType.NUMBER): 
                                dts = DecreeToken.tryAttachList(ttt, None, 10, False)
                                break
                        npt = NounPhraseHelper.tryParse(ttt, NounPhraseParseAttr.NO, 0)
                        if (npt is not None): 
                            if (npt.end_token.isValue("НОТАРИУС", None)): 
                                ttt = npt.end_token
                                has_spec = True
                                continue
                        if (ttt.getReferent() is not None): 
                            if (has_spec): 
                                continue
                        break
                if (dts is not None and len(dts) > 0): 
                    t0 = t
                    dr = DecreeReferent()
                    dr.typ = "ДОВЕРЕННОСТЬ"
                    for d in dts: 
                        if (d.typ == DecreeToken.ItemType.DATE): 
                            dr._addDate(d)
                            t = d.end_token
                        elif (d.typ == DecreeToken.ItemType.NUMBER): 
                            dr._addNumber(d)
                            t = d.end_token
                        else: 
                            break
                    ad = t.kit.getAnalyzerDataByAnalyzerName(InstrumentAnalyzer.ANALYZER_NAME)
                    ip.ground = ad.registerReferent(dr)
                    rt = ReferentToken(Utils.asObjectOrNull(ip.ground, Referent), t0, t)
                    t.kit.embedToken(rt)
                    return rt
                ip.ground = "ДОВЕРЕННОСТЬ"
                return t
            break
        return None
    
    @staticmethod
    def getDocTypes(name : str, name2 : str) -> typing.List[str]:
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
        elif (name == "ЗАКАЗЧИК" or name == "ИСПОЛНИТЕЛЬ" or LanguageHelper.endsWith(name, "ПОДРЯДЧИК")): 
            res.append("ДОГОВОР УСЛУГ")
        elif (name == "ПОСТАВЩИК"): 
            res.append("ДОГОВОР ПОСТАВКИ")
        elif (name == "ЛИЦЕНЗИАР" or name == "ЛИЦЕНЗИАТ"): 
            res.append("ЛИЦЕНЗИОННЫЙ ДОГОВОР")
        elif (name == "СТРАХОВЩИК" or name == "СТРАХОВАТЕЛЬ"): 
            res.append("ДОГОВОР СТРАХОВАНИЯ")
        if (name2 is None): 
            return res
        tmp = ParticipantToken.getDocTypes(name2, None)
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
            ParticipantToken.M_ONTOLOGY.add(Termin._new118(s, ParticipantToken.M_ONTOLOGY))
        t = Termin._new118("ГЕНПОДРЯДЧИК", ParticipantToken.M_ONTOLOGY)
        t.addVariant("ГЕНЕРАЛЬНЫЙ ПОДРЯДЧИК", False)
        ParticipantToken.M_ONTOLOGY.add(t)
        t = Termin._new118("ЗАИМОДАТЕЛЬ", ParticipantToken.M_ONTOLOGY)
        t.addVariant("ЗАЙМОДАТЕЛЬ", False)
        t.addVariant("ЗАЙМОДАВЕЦ", False)
        t.addVariant("ЗАИМОДАВЕЦ", False)
        ParticipantToken.M_ONTOLOGY.add(t)
        t = Termin("ИМЕНУЕМЫЙ")
        t.addVariant("ИМЕНОВАТЬСЯ", False)
        t.addVariant("ИМЕНУЕМ", False)
        t.addVariant("ДАЛЬНЕЙШИЙ", False)
        t.addVariant("ДАЛЕЕ", False)
        t.addVariant("ДАЛЕЕ ПО ТЕКСТУ", False)
        ParticipantToken.M_ONTOLOGY.add(t)
    
    @staticmethod
    def _new1320(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'ParticipantToken':
        res = ParticipantToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1481(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Kinds') -> 'ParticipantToken':
        res = ParticipantToken(_arg1, _arg2)
        res.kind = _arg3
        return res
    
    @staticmethod
    def _new1486(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Kinds', _arg4 : str) -> 'ParticipantToken':
        res = ParticipantToken(_arg1, _arg2)
        res.kind = _arg3
        res.typ = _arg4
        return res