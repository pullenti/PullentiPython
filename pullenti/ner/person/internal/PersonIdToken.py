# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NumberHelper import NumberHelper


class PersonIdToken(MetaToken):
    
    class Typs(IntEnum):
        KEYWORD = 0
        SERIA = 0 + 1
        NUMBER = (0 + 1) + 1
        DATE = ((0 + 1) + 1) + 1
        ORG = (((0 + 1) + 1) + 1) + 1
        VIDAN = ((((0 + 1) + 1) + 1) + 1) + 1
        CODE = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
        ADDRESS = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
        
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
    def tryAttach(t : 'Token') -> 'ReferentToken':
        from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (t is None or not t.chars.is_letter): 
            return None
        noun = PersonIdToken.__tryParse(t, None)
        if (noun is None): 
            return None
        li = list()
        t = noun.end_token.next0_
        first_pass3112 = True
        while True:
            if first_pass3112: first_pass3112 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                break
            if (t.isCharOf(",:")): 
                continue
            idt = PersonIdToken.__tryParse(t, (li[len(li) - 1] if len(li) > 0 else noun))
            if (idt is None): 
                if (t.isValue("ОТДЕЛ", None) or t.isValue("ОТДЕЛЕНИЕ", None)): 
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
                if (pid.findSlot(PersonIdentityReferent.ATTR_DATE, None, True) is not None): 
                    break
                pid.addSlot(PersonIdentityReferent.ATTR_DATE, li[i].referent, False, 0)
            elif (li[i].typ == PersonIdToken.Typs.ADDRESS and li[i].referent is not None): 
                if (pid.findSlot(PersonIdentityReferent.ATTR_ADDRESS, None, True) is not None): 
                    break
                pid.addSlot(PersonIdentityReferent.ATTR_ADDRESS, li[i].referent, False, 0)
            elif (li[i].typ == PersonIdToken.Typs.ORG and li[i].referent is not None): 
                if (pid.findSlot(PersonIdentityReferent.ATTR_ORG, None, True) is not None): 
                    break
                pid.addSlot(PersonIdentityReferent.ATTR_ORG, li[i].referent, False, 0)
            else: 
                break
            i += 1
        return ReferentToken(pid, noun.begin_token, li[i - 1].end_token)
    
    @staticmethod
    def __tryParse(t : 'Token', prev : 'PersonIdToken') -> 'PersonIdToken':
        from pullenti.ner.Referent import Referent
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.address.AddressReferent import AddressReferent
        if (t.isValue("СВИДЕТЕЛЬСТВО", None)): 
            tt1 = t
            ip = False
            reg = False
            tt = t.next0_
            first_pass3113 = True
            while True:
                if first_pass3113: first_pass3113 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_comma_and or tt.morph.class0_.is_preposition): 
                    continue
                if (tt.isValue("РЕГИСТРАЦИЯ", None) or tt.isValue("РЕЕСТР", None) or tt.isValue("ЗАРЕГИСТРИРОВАТЬ", None)): 
                    reg = True
                    tt1 = tt
                elif (tt.isValue("ИНДИВИДУАЛЬНЫЙ", None) or tt.isValue("ИП", None)): 
                    ip = True
                    tt1 = tt
                elif ((tt.isValue("ВНЕСЕНИЕ", None) or tt.isValue("ГОСУДАРСТВЕННЫЙ", None) or tt.isValue("ЕДИНЫЙ", None)) or tt.isValue("ЗАПИСЬ", None) or tt.isValue("ПРЕДПРИНИМАТЕЛЬ", None)): 
                    tt1 = tt
                elif (tt.getReferent() is not None and tt.getReferent().type_name == "DATERANGE"): 
                    tt1 = tt
                else: 
                    break
            if (reg and ip): 
                return PersonIdToken._new2362(t, tt1, PersonIdToken.Typs.KEYWORD, "СВИДЕТЕЛЬСТВО О ГОСУДАРСТВЕННОЙ РЕГИСТРАЦИИ ФИЗИЧЕСКОГО ЛИЦА В КАЧЕСТВЕ ИНДИВИДУАЛЬНОГО ПРЕДПРИНИМАТЕЛЯ")
        tok = PersonIdToken.M_ONTOLOGY.tryParse(t, TerminParseAttr.NO)
        if (tok is not None): 
            ty = Utils.valToEnum(tok.termin.tag, PersonIdToken.Typs)
            res = PersonIdToken._new2362(tok.begin_token, tok.end_token, ty, tok.termin.canonic_text)
            if (prev is None): 
                if (ty != PersonIdToken.Typs.KEYWORD): 
                    return None
                t = tok.end_token.next0_
                first_pass3114 = True
                while True:
                    if first_pass3114: first_pass3114 = False
                    else: t = t.next0_
                    if (not (t is not None)): break
                    r = t.getReferent()
                    if (r is not None and (isinstance(r, GeoReferent))): 
                        res.referent = r
                        res.end_token = t
                        continue
                    if (t.isValue("ГРАЖДАНИН", None) and t.next0_ is not None and (isinstance(t.next0_.getReferent(), GeoReferent))): 
                        res.referent = t.next0_.getReferent()
                        res.end_token = t.next0_
                        t = res.end_token
                        continue
                    if (r is not None): 
                        break
                    ait = PersonAttrToken.tryAttach(t, None, PersonAttrToken.PersonAttrAttachAttrs.NO)
                    if (ait is not None): 
                        if (ait.referent is not None): 
                            for s in ait.referent.slots: 
                                if (s.type_name == PersonPropertyReferent.ATTR_REF and (isinstance(s.value, GeoReferent))): 
                                    res.referent = (Utils.asObjectOrNull(s.value, Referent))
                        res.end_token = ait.end_token
                        break
                    break
                if ((isinstance(res.referent, GeoReferent)) and not (Utils.asObjectOrNull(res.referent, GeoReferent)).is_state): 
                    res.referent = (None)
                return res
            if (ty == PersonIdToken.Typs.NUMBER): 
                tmp = io.StringIO()
                tt = tok.end_token.next0_
                if (tt is not None and tt.isChar(':')): 
                    tt = tt.next0_
                while tt is not None: 
                    if (tt.is_newline_before): 
                        break
                    if (not ((isinstance(tt, NumberToken)))): 
                        break
                    print(tt.getSourceText(), end="", file=tmp)
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
                if (tt is not None and tt.isChar(':')): 
                    tt = tt.next0_
                next_num = False
                first_pass3115 = True
                while True:
                    if first_pass3115: first_pass3115 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.is_newline_before): 
                        break
                    if (MiscHelper.checkNumberPrefix(tt) is not None): 
                        next_num = True
                        break
                    if (not ((isinstance(tt, NumberToken)))): 
                        if (not ((isinstance(tt, TextToken)))): 
                            break
                        if (not tt.chars.is_all_upper): 
                            break
                        nu = NumberHelper.tryParseRoman(tt)
                        if (nu is not None): 
                            print(nu.getSourceText(), end="", file=tmp)
                            tt = nu.end_token
                        elif (tt.length_char != 2): 
                            break
                        else: 
                            print((Utils.asObjectOrNull(tt, TextToken)).term, end="", file=tmp)
                            res.end_token = tt
                        if (tt.next0_ is not None and tt.next0_.is_hiphen): 
                            tt = tt.next0_
                        continue
                    if (tmp.tell() >= 4): 
                        break
                    print(tt.getSourceText(), end="", file=tmp)
                    res.end_token = tt
                if (tmp.tell() < 4): 
                    if ((tmp.tell() < 2) or not next_num): 
                        return None
                res.value = Utils.toStringStringIO(tmp)
                res.has_prefix = True
                return res
            if (ty == PersonIdToken.Typs.CODE): 
                tt = res.end_token.next0_
                first_pass3116 = True
                while True:
                    if first_pass3116: first_pass3116 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.isCharOf(":") or tt.is_hiphen): 
                        continue
                    if (isinstance(tt, NumberToken)): 
                        res.end_token = tt
                        continue
                    break
            if (ty == PersonIdToken.Typs.ADDRESS): 
                if (isinstance(t.getReferent(), AddressReferent)): 
                    res.referent = t.getReferent()
                    res.end_token = t
                    return res
                tt = res.end_token.next0_
                first_pass3117 = True
                while True:
                    if first_pass3117: first_pass3117 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.isCharOf(":") or tt.is_hiphen or tt.morph.class0_.is_preposition): 
                        continue
                    if (isinstance(tt.getReferent(), AddressReferent)): 
                        res.referent = tt.getReferent()
                        res.end_token = tt
                    break
                if (res.referent is None): 
                    return None
            return res
        elif (prev is None): 
            return None
        t0 = t
        t1 = MiscHelper.checkNumberPrefix(t0)
        if (t1 is not None): 
            t = t1
        if (isinstance(t, NumberToken)): 
            tmp = io.StringIO()
            res = PersonIdToken._new2364(t0, t, PersonIdToken.Typs.NUMBER)
            tt = t
            while tt is not None: 
                if (tt.is_newline_before or not ((isinstance(tt, NumberToken)))): 
                    break
                print(tt.getSourceText(), end="", file=tmp)
                res.end_token = tt
                tt = tt.next0_
            if (tmp.tell() < 4): 
                if (tmp.tell() < 2): 
                    return None
                if (prev is None or prev.typ != PersonIdToken.Typs.KEYWORD): 
                    return None
                ne = PersonIdToken.__tryParse(res.end_token.next0_, prev)
                if (ne is not None and ne.typ == PersonIdToken.Typs.NUMBER): 
                    res.typ = PersonIdToken.Typs.SERIA
                else: 
                    return None
            res.value = Utils.toStringStringIO(tmp)
            if (t0 != t): 
                res.has_prefix = True
            return res
        if (isinstance(t, ReferentToken)): 
            r = t.getReferent()
            if (r is not None): 
                if (r.type_name == "DATE"): 
                    return PersonIdToken._new2365(t, t, PersonIdToken.Typs.DATE, r)
                if (r.type_name == "ORGANIZATION"): 
                    return PersonIdToken._new2365(t, t, PersonIdToken.Typs.ORG, r)
                if (r.type_name == "ADDRESS"): 
                    return PersonIdToken._new2365(t, t, PersonIdToken.Typs.ADDRESS, r)
        if ((prev is not None and prev.typ == PersonIdToken.Typs.KEYWORD and (isinstance(t, TextToken))) and not t.chars.is_all_lower and t.chars.is_letter): 
            rr = PersonIdToken.__tryParse(t.next0_, prev)
            if (rr is not None and rr.typ == PersonIdToken.Typs.NUMBER): 
                return PersonIdToken._new2362(t, t, PersonIdToken.Typs.SERIA, (Utils.asObjectOrNull(t, TextToken)).term)
        if ((t is not None and t.isValue("ОТ", "ВІД") and (isinstance(t.next0_, ReferentToken))) and t.next0_.getReferent().type_name == "DATE"): 
            return PersonIdToken._new2365(t, t.next0_, PersonIdToken.Typs.DATE, t.next0_.getReferent())
        return None
    
    M_ONTOLOGY = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        if (PersonIdToken.M_ONTOLOGY is not None): 
            return
        PersonIdToken.M_ONTOLOGY = TerminCollection()
        t = Termin._new118("ПАСПОРТ", PersonIdToken.Typs.KEYWORD)
        t.addVariant("ПАССПОРТ", False)
        t.addVariant("ПАСПОРТНЫЕ ДАННЫЕ", False)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new118("ЗАГРАНИЧНЫЙ ПАСПОРТ", PersonIdToken.Typs.KEYWORD)
        t.addVariant("ЗАГРАНПАСПОРТ", False)
        t.addAbridge("ЗАГРАН. ПАСПОРТ")
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new118("УДОСТОВЕРЕНИЕ ЛИЧНОСТИ", PersonIdToken.Typs.KEYWORD)
        t.addVariant("УДОСТОВЕРЕНИЕ ЛИЧНОСТИ ОФИЦЕРА", False)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new118("СВИДЕТЕЛЬСТВО О ГОСУДАРСТВЕННОЙ РЕГИСТРАЦИИ ФИЗИЧЕСКОГО ЛИЦА В КАЧЕСТВЕ ИНДИВИДУАЛЬНОГО ПРЕДПРИНИМАТЕЛЯ", PersonIdToken.Typs.KEYWORD)
        t.addVariant("СВИДЕТЕЛЬСТВО О ГОСУДАРСТВЕННОЙ РЕГИСТРАЦИИ ФИЗИЧЕСКОГО ЛИЦА В КАЧЕСТВЕ ИП", False)
        t.addVariant("СВИДЕТЕЛЬСТВО О ГОСРЕГИСТРАЦИИ ФИЗЛИЦА В КАЧЕСТВЕ ИП", False)
        t.addVariant("СВИДЕТЕЛЬСТВО ГОСУДАРСТВЕННОЙ РЕГИСТРАЦИИ", False)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new118("ВОДИТЕЛЬСКОЕ УДОСТОВЕРЕНИЕ", PersonIdToken.Typs.KEYWORD)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new118("ЛИЦЕНЗИЯ", PersonIdToken.Typs.KEYWORD)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new118("СЕРИЯ", PersonIdToken.Typs.SERIA)
        t.addAbridge("СЕР.")
        t.addVariant("СЕРИ", False)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new118("НОМЕР", PersonIdToken.Typs.NUMBER)
        t.addAbridge("НОМ.")
        t.addAbridge("Н-Р")
        t.addVariant("№", False)
        t.addVariant("N", False)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new118("ВЫДАТЬ", PersonIdToken.Typs.VIDAN)
        t.addVariant("ВЫДАВАТЬ", False)
        t.addVariant("ДАТА ВЫДАЧИ", False)
        t.addVariant("ДАТА РЕГИСТРАЦИИ", False)
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new118("КОД ПОДРАЗДЕЛЕНИЯ", PersonIdToken.Typs.CODE)
        t.addAbridge("К/П")
        t.addAbridge("К.П.")
        PersonIdToken.M_ONTOLOGY.add(t)
        t = Termin._new118("РЕГИСТРАЦИЯ", PersonIdToken.Typs.ADDRESS)
        t.addVariant("ЗАРЕГИСТРИРОВАН", False)
        t.addVariant("АДРЕС РЕГИСТРАЦИИ", False)
        t.addVariant("ЗАРЕГИСТРИРОВАННЫЙ", False)
        t.addAbridge("ПРОПИСАН")
        t.addVariant("АДРЕС ПРОПИСКИ", False)
        t.addVariant("АДРЕС ПО ПРОПИСКЕ", False)
        PersonIdToken.M_ONTOLOGY.add(t)
    
    @staticmethod
    def _new2362(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : str) -> 'PersonIdToken':
        res = PersonIdToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new2364(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs') -> 'PersonIdToken':
        res = PersonIdToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2365(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : 'Referent') -> 'PersonIdToken':
        res = PersonIdToken(_arg1, _arg2)
        res.typ = _arg3
        res.referent = _arg4
        return res