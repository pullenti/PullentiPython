﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from enum import IntEnum
from pullenti.unisharp.Utils import Utils

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
from pullenti.ner.TextToken import TextToken
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent
from pullenti.ner.Referent import Referent
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.NumberHelper import NumberHelper

class PersonIdToken(MetaToken):
    
    class Typs(IntEnum):
        KEYWORD = 0
        SERIA = 1
        NUMBER = 2
        DATE = 3
        ORG = 4
        VIDAN = 5
        CODE = 6
        ADDRESS = 7
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.typ = PersonIdToken.Typs.KEYWORD
        self.value = None;
        self.referent = None;
        self.has_prefix = False
    
    @staticmethod
    def try_attach(t : 'Token') -> 'ReferentToken':
        if (t is None or not t.chars.is_letter0): 
            return None
        noun = PersonIdToken.__try_parse(t, None)
        if (noun is None): 
            return None
        li = list()
        t = noun.end_token.next0_
        first_pass3213 = True
        while True:
            if first_pass3213: first_pass3213 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char0): 
                break
            if (t.is_char_of(",:")): 
                continue
            idt = PersonIdToken.__try_parse(t, (li[len(li) - 1] if len(li) > 0 else noun))
            if (idt is None): 
                if (t.is_value("ОТДЕЛ", None) or t.is_value("ОТДЕЛЕНИЕ", None)): 
                    continue
                break
            if (idt.typ == PersonIdToken.Typs.KEYWORD): 
                break
            li.append(idt)
            t = idt.end_token
        if (len(li) == 0): 
            return None
        num = None
        i = 0
        if (li[0].typ == PersonIdToken.Typs.NUMBER): 
            if (len(li) > 1 and li[1].typ == PersonIdToken.Typs.NUMBER and li[1].has_prefix): 
                num = (li[0].value + li[1].value)
                i = 2
            else: 
                num = li[0].value
                i = 1
        elif (li[0].typ == PersonIdToken.Typs.SERIA and len(li) > 1 and li[1].typ == PersonIdToken.Typs.NUMBER): 
            num = (li[0].value + li[1].value)
            i = 2
        elif (li[0].typ == PersonIdToken.Typs.SERIA and len(li[0].value) > 5): 
            num = li[0].value
            i = 1
        else: 
            return None
        pid = PersonIdentityReferent()
        pid.typ = noun.value.lower()
        pid.number = num
        if (isinstance(noun.referent, GeoReferent)): 
            pid.state = noun.referent
        while i < len(li): 
            if (li[i].typ == PersonIdToken.Typs.VIDAN or li[i].typ == PersonIdToken.Typs.CODE): 
                pass
            elif (li[i].typ == PersonIdToken.Typs.DATE and li[i].referent is not None): 
                if (pid.find_slot(PersonIdentityReferent.ATTR_DATE, None, True) is not None): 
                    break
                pid.add_slot(PersonIdentityReferent.ATTR_DATE, li[i].referent, False, 0)
            elif (li[i].typ == PersonIdToken.Typs.ADDRESS and li[i].referent is not None): 
                if (pid.find_slot(PersonIdentityReferent.ATTR_ADDRESS, None, True) is not None): 
                    break
                pid.add_slot(PersonIdentityReferent.ATTR_ADDRESS, li[i].referent, False, 0)
            elif (li[i].typ == PersonIdToken.Typs.ORG and li[i].referent is not None): 
                if (pid.find_slot(PersonIdentityReferent.ATTR_ORG, None, True) is not None): 
                    break
                pid.add_slot(PersonIdentityReferent.ATTR_ORG, li[i].referent, False, 0)
            else: 
                break
            i += 1
        return ReferentToken(pid, noun.begin_token, li[i - 1].end_token)
    
    @staticmethod
    def __try_parse(t : 'Token', prev : 'PersonIdToken') -> 'PersonIdToken':
        if (t.is_value("СВИДЕТЕЛЬСТВО", None)): 
            tt1 = t
            ip = False
            reg = False
            tt = t.next0_
            first_pass3214 = True
            while True:
                if first_pass3214: first_pass3214 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_comma_and0 or tt.morph.class0_.is_preposition0): 
                    continue
                if (tt.is_value("РЕГИСТРАЦИЯ", None) or tt.is_value("РЕЕСТР", None) or tt.is_value("ЗАРЕГИСТРИРОВАТЬ", None)): 
                    reg = True
                    tt1 = tt
                elif (tt.is_value("ИНДИВИДУАЛЬНЫЙ", None) or tt.is_value("ИП", None)): 
                    ip = True
                    tt1 = tt
                elif ((tt.is_value("ВНЕСЕНИЕ", None) or tt.is_value("ГОСУДАРСТВЕННЫЙ", None) or tt.is_value("ЕДИНЫЙ", None)) or tt.is_value("ЗАПИСЬ", None) or tt.is_value("ПРЕДПРИНИМАТЕЛЬ", None)): 
                    tt1 = tt
                elif (tt.get_referent() is not None and tt.get_referent().type_name == "DATERANGE"): 
                    tt1 = tt
                else: 
                    break
            if (reg and ip): 
                return PersonIdToken._new2444(t, tt1, PersonIdToken.Typs.KEYWORD, "СВИДЕТЕЛЬСТВО О ГОСУДАРСТВЕННОЙ РЕГИСТРАЦИИ ФИЗИЧЕСКОГО ЛИЦА В КАЧЕСТВЕ ИНДИВИДУАЛЬНОГО ПРЕДПРИНИМАТЕЛЯ")
        tok = PersonIdToken.M_ONTOLOGY.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            ty = Utils.valToEnum(tok.termin.tag, PersonIdToken.Typs)
            res = PersonIdToken._new2444(tok.begin_token, tok.end_token, ty, tok.termin.canonic_text)
            if (prev is None): 
                if (ty != PersonIdToken.Typs.KEYWORD): 
                    return None
                t = tok.end_token.next0_
                first_pass3215 = True
                while True:
                    if first_pass3215: first_pass3215 = False
                    else: t = t.next0_
                    if (not (t is not None)): break
                    r = t.get_referent()
                    if (r is not None and (isinstance(r, GeoReferent))): 
                        res.referent = r
                        res.end_token = t
                        continue
                    if (t.is_value("ГРАЖДАНИН", None) and t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent))): 
                        res.referent = t.next0_.get_referent()
                        res.end_token = t.next0_
                        t = res.end_token
                        continue
                    if (r is not None): 
                        break
                    ait = PersonAttrToken.try_attach(t, None, PersonAttrToken.PersonAttrAttachAttrs.NO)
                    if (ait is not None): 
                        if (ait.referent is not None): 
                            for s in ait.referent.slots: 
                                if (s.type_name == PersonPropertyReferent.ATTR_REF and (isinstance(s.value, GeoReferent))): 
                                    res.referent = (Utils.asObjectOrNull(s.value, Referent))
                        res.end_token = ait.end_token
                        break
                    break
                if ((isinstance(res.referent, GeoReferent)) and not (res.referent).is_state0): 
                    res.referent = (None)
                return res
            if (ty == PersonIdToken.Typs.NUMBER): 
                tmp = io.StringIO()
                tt = tok.end_token.next0_
                if (tt is not None and tt.is_char(':')): 
                    tt = tt.next0_
                while tt is not None: 
                    if (tt.is_newline_before0): 
                        break
                    if (not ((isinstance(tt, NumberToken)))): 
                        break
                    print(tt.get_source_text(), end="", file=tmp)
                    res.end_token = tt
                    tt = tt.next0_
                if (tmp.tell() < 1): 
                    return None
                res.value = Utils.toStringStringIO(tmp)
                res.has_prefix = True
                return res
            if (ty == PersonIdToken.Typs.SERIA): 
                tmp = io.StringIO()
                tt = tok.end_token.next0_
                if (tt is not None and tt.is_char(':')): 
                    tt = tt.next0_
                next_num = False
                first_pass3216 = True
                while True:
                    if first_pass3216: first_pass3216 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.is_newline_before0): 
                        break
                    if (MiscHelper.check_number_prefix(tt) is not None): 
                        next_num = True
                        break
                    if (not ((isinstance(tt, NumberToken)))): 
                        if (not ((isinstance(tt, TextToken)))): 
                            break
                        if (not tt.chars.is_all_upper0): 
                            break
                        nu = NumberHelper.try_parse_roman(tt)
                        if (nu is not None): 
                            print(nu.get_source_text(), end="", file=tmp)
                            tt = nu.end_token
                        elif (tt.length_char != 2): 
                            break
                        else: 
                            print((tt).term, end="", file=tmp)
                            res.end_token = tt
                        if (tt.next0_ is not None and tt.next0_.is_hiphen0): 
                            tt = tt.next0_
                        continue
                    if (tmp.tell() >= 4): 
                        break
                    print(tt.get_source_text(), end="", file=tmp)
                    res.end_token = tt
                if (tmp.tell() < 4): 
                    if (tmp.tell() < 2): 
                        return None
                    tt1 = res.end_token.next0_
                    if (tt1 is not None and tt1.is_comma0): 
                        tt1 = tt1.next0_
                    next0__ = PersonIdToken.__try_parse(tt1, res)
                    if (next0__ is not None and next0__.typ == PersonIdToken.Typs.NUMBER): 
                        pass
                    else: 
                        return None
                res.value = Utils.toStringStringIO(tmp)
                res.has_prefix = True
                return res
            if (ty == PersonIdToken.Typs.CODE): 
                tt = res.end_token.next0_
                first_pass3217 = True
                while True:
                    if first_pass3217: first_pass3217 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.is_char_of(":") or tt.is_hiphen0): 
                        continue
                    if (isinstance(tt, NumberToken)): 
                        res.end_token = tt
                        continue
                    break
            if (ty == PersonIdToken.Typs.ADDRESS): 
                if (isinstance(t.get_referent(), AddressReferent)): 
                    res.referent = t.get_referent()
                    res.end_token = t
                    return res
                tt = res.end_token.next0_
                first_pass3218 = True
                while True:
                    if first_pass3218: first_pass3218 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.is_char_of(":") or tt.is_hiphen0 or tt.morph.class0_.is_preposition0): 
                        continue
                    if (isinstance(tt.get_referent(), AddressReferent)): 
                        res.referent = tt.get_referent()
                        res.end_token = tt
                    break
                if (res.referent is None): 
                    return None
            return res
        elif (prev is None): 
            return None
        t0 = t
        t1 = MiscHelper.check_number_prefix(t0)
        if (t1 is not None): 
            t = t1
        if (isinstance(t, NumberToken)): 
            tmp = io.StringIO()
            res = PersonIdToken._new2446(t0, t, PersonIdToken.Typs.NUMBER)
            tt = t
            while tt is not None: 
                if (tt.is_newline_before0 or not ((isinstance(tt, NumberToken)))): 
                    break
                print(tt.get_source_text(), end="", file=tmp)
                res.end_token = tt
                tt = tt.next0_
            if (tmp.tell() < 4): 
                if (tmp.tell() < 2): 
                    return None
                if (prev is None or prev.typ != PersonIdToken.Typs.KEYWORD): 
                    return None
                ne = PersonIdToken.__try_parse(res.end_token.next0_, prev)
                if (ne is not None and ne.typ == PersonIdToken.Typs.NUMBER): 
                    res.typ = PersonIdToken.Typs.SERIA
                else: 
                    return None
            res.value = Utils.toStringStringIO(tmp)
            if (t0 != t): 
                res.has_prefix = True
            return res
        if (isinstance(t, ReferentToken)): 
            r = t.get_referent()
            if (r is not None): 
                if (r.type_name == "DATE"): 
                    return PersonIdToken._new2447(t, t, PersonIdToken.Typs.DATE, r)
                if (r.type_name == "ORGANIZATION"): 
                    return PersonIdToken._new2447(t, t, PersonIdToken.Typs.ORG, r)
                if (r.type_name == "ADDRESS"): 
                    return PersonIdToken._new2447(t, t, PersonIdToken.Typs.ADDRESS, r)
        if ((prev is not None and prev.typ == PersonIdToken.Typs.KEYWORD and (isinstance(t, TextToken))) and not t.chars.is_all_lower0 and t.chars.is_letter0): 
            rr = PersonIdToken.__try_parse(t.next0_, prev)
            if (rr is not None and rr.typ == PersonIdToken.Typs.NUMBER): 
                return PersonIdToken._new2444(t, t, PersonIdToken.Typs.SERIA, (t).term)
        if ((t is not None and t.is_value("ОТ", "ВІД") and (isinstance(t.next0_, ReferentToken))) and t.next0_.get_referent().type_name == "DATE"): 
            return PersonIdToken._new2447(t, t.next0_, PersonIdToken.Typs.DATE, t.next0_.get_referent())
        return None
    
    M_ONTOLOGY = None
    
    @staticmethod
    def initialize() -> None:
        if (PersonIdToken.M_ONTOLOGY is not None): 
            return
        PersonIdToken.M_ONTOLOGY = TerminCollection()
        t = Termin._new119("ПАСПОРТ", PersonIdToken.Typs.KEYWORD)
        t.add_variant("ПАССПОРТ", False)
        t.add_variant("ПАСПОРТНЫЕ ДАННЫЕ", False)
        t.add_variant("ВНУТРЕННИЙ ПАСПОРТ", False)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new119("ЗАГРАНИЧНЫЙ ПАСПОРТ", PersonIdToken.Typs.KEYWORD)
        t.add_variant("ЗАГРАНПАСПОРТ", False)
        t.add_abridge("ЗАГРАН. ПАСПОРТ")
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new119("УДОСТОВЕРЕНИЕ ЛИЧНОСТИ", PersonIdToken.Typs.KEYWORD)
        t.add_variant("УДОСТОВЕРЕНИЕ ЛИЧНОСТИ ОФИЦЕРА", False)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new119("СВИДЕТЕЛЬСТВО О ГОСУДАРСТВЕННОЙ РЕГИСТРАЦИИ ФИЗИЧЕСКОГО ЛИЦА В КАЧЕСТВЕ ИНДИВИДУАЛЬНОГО ПРЕДПРИНИМАТЕЛЯ", PersonIdToken.Typs.KEYWORD)
        t.add_variant("СВИДЕТЕЛЬСТВО О ГОСУДАРСТВЕННОЙ РЕГИСТРАЦИИ ФИЗИЧЕСКОГО ЛИЦА В КАЧЕСТВЕ ИП", False)
        t.add_variant("СВИДЕТЕЛЬСТВО О ГОСРЕГИСТРАЦИИ ФИЗЛИЦА В КАЧЕСТВЕ ИП", False)
        t.add_variant("СВИДЕТЕЛЬСТВО ГОСУДАРСТВЕННОЙ РЕГИСТРАЦИИ", False)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new119("ВОДИТЕЛЬСКОЕ УДОСТОВЕРЕНИЕ", PersonIdToken.Typs.KEYWORD)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new119("ЛИЦЕНЗИЯ", PersonIdToken.Typs.KEYWORD)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new119("СЕРИЯ", PersonIdToken.Typs.SERIA)
        t.add_abridge("СЕР.")
        t.add_variant("СЕРИ", False)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new119("НОМЕР", PersonIdToken.Typs.NUMBER)
        t.add_abridge("НОМ.")
        t.add_abridge("Н-Р")
        t.add_variant("№", False)
        t.add_variant("N", False)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new119("ВЫДАТЬ", PersonIdToken.Typs.VIDAN)
        t.add_variant("ВЫДАВАТЬ", False)
        t.add_variant("ДАТА ВЫДАЧИ", False)
        t.add_variant("ДАТА РЕГИСТРАЦИИ", False)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new119("КОД ПОДРАЗДЕЛЕНИЯ", PersonIdToken.Typs.CODE)
        t.add_abridge("К/П")
        t.add_abridge("К.П.")
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new119("РЕГИСТРАЦИЯ", PersonIdToken.Typs.ADDRESS)
        t.add_variant("ЗАРЕГИСТРИРОВАН", False)
        t.add_variant("АДРЕС РЕГИСТРАЦИИ", False)
        t.add_variant("ЗАРЕГИСТРИРОВАННЫЙ", False)
        t.add_abridge("ПРОПИСАН")
        t.add_variant("АДРЕС ПРОПИСКИ", False)
        t.add_variant("АДРЕС ПО ПРОПИСКЕ", False)
        PersonIdToken.M_ONTOLOGY.add(t)
    
    @staticmethod
    def _new2444(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : str) -> 'PersonIdToken':
        res = PersonIdToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new2446(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs') -> 'PersonIdToken':
        res = PersonIdToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2447(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : 'Referent') -> 'PersonIdToken':
        res = PersonIdToken(_arg1, _arg2)
        res.typ = _arg3
        res.referent = _arg4
        return res