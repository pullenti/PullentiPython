# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.mail.internal.MailLine import MailLine
from pullenti.ner.Token import Token
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.Referent import Referent
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.person.internal.PersonAttrTerminType import PersonAttrTerminType
from pullenti.ner.TextToken import TextToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.person.PersonAnalyzer import PersonAnalyzer
from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
from pullenti.ner.person.internal.PersonIdentityToken import PersonIdentityToken

class PersonHelper:
    
    @staticmethod
    def _create_referent_token(p : 'PersonReferent', begin : 'Token', end : 'Token', morph_ : 'MorphCollection', attrs : typing.List['PersonAttrToken'], ad : 'PersonAnalyzerData', for_attribute : bool, after_be_predicate : bool) -> 'ReferentToken':
        if (p is None): 
            return None
        has_prefix = False
        if (attrs is not None): 
            for a in attrs: 
                if (a.typ == PersonAttrTerminType.BESTREGARDS): 
                    has_prefix = True
                else: 
                    if (a.begin_char < begin.begin_char): 
                        begin = a.begin_token
                        if ((a.end_token.next0_ is not None and a.end_token.next0_.is_char(')') and begin.previous is not None) and begin.previous.is_char('(')): 
                            begin = begin.previous
                    if (a.typ != PersonAttrTerminType.PREFIX): 
                        if (a.age is not None): 
                            p.add_slot(PersonReferent.ATTR_AGE, a.age, False, 0)
                        if (a.prop_ref is None): 
                            p.add_slot(PersonReferent.ATTR_ATTR, a.value, False, 0)
                        else: 
                            p.add_slot(PersonReferent.ATTR_ATTR, a, False, 0)
                    elif (a.gender == MorphGender.FEMINIE and not p.is_female): 
                        p.is_female = True
                    elif (a.gender == MorphGender.MASCULINE and not p.is_male): 
                        p.is_male = True
        elif ((isinstance(begin.previous, TextToken)) and (begin.whitespaces_before_count < 3)): 
            if (begin.previous.term == "ИП"): 
                a = PersonAttrToken(begin.previous, begin.previous)
                a.prop_ref = PersonPropertyReferent()
                a.prop_ref.name = "индивидуальный предприниматель"
                p.add_slot(PersonReferent.ATTR_ATTR, a, False, 0)
                begin = begin.previous
        m0 = MorphCollection()
        for it in morph_.items: 
            bi = MorphBaseInfo()
            bi.copy_from(it)
            bi.number = MorphNumber.SINGULAR
            if (bi.gender == MorphGender.UNDEFINED): 
                if (p.is_male and not p.is_female): 
                    bi.gender = MorphGender.MASCULINE
                if (not p.is_male and p.is_female): 
                    bi.gender = MorphGender.FEMINIE
            m0.add_item(bi)
        morph_ = m0
        if ((attrs is not None and len(attrs) > 0 and not attrs[0].morph.case_.is_undefined) and morph_.case_.is_undefined): 
            morph_.case_ = attrs[0].morph.case_
            if (attrs[0].morph.number == MorphNumber.SINGULAR): 
                morph_.number = MorphNumber.SINGULAR
            if (p.is_male and not p.is_female): 
                morph_.gender = MorphGender.MASCULINE
            elif (p.is_female): 
                morph_.gender = MorphGender.FEMINIE
        if (begin.previous is not None): 
            ttt = begin.previous
            if (ttt.is_value("ИМЕНИ", "ІМЕНІ")): 
                for_attribute = True
            else: 
                if (ttt.is_char('.') and ttt.previous is not None): 
                    ttt = ttt.previous
                if (ttt.whitespaces_after_count < 3): 
                    if (ttt.is_value("ИМ", "ІМ")): 
                        for_attribute = True
        if (for_attribute): 
            return ReferentToken._new2480(p, begin, end, morph_, p._m_person_identity_typ)
        if ((begin.previous is not None and begin.previous.is_comma_and and (isinstance(begin.previous.previous, ReferentToken))) and (isinstance(begin.previous.previous.get_referent(), PersonReferent))): 
            rt00 = Utils.asObjectOrNull(begin.previous.previous, ReferentToken)
            ttt = rt00
            while ttt is not None: 
                if (ttt.previous is None or not (isinstance(ttt.previous.previous, ReferentToken))): 
                    break
                if (not ttt.previous.is_comma_and or not (isinstance(ttt.previous.previous.get_referent(), PersonReferent))): 
                    break
                rt00 = (Utils.asObjectOrNull(ttt.previous.previous, ReferentToken))
                ttt = (rt00)
            if (isinstance(rt00.begin_token.get_referent(), PersonPropertyReferent)): 
                ok = False
                if (rt00.begin_token.end_token.next0_ is not None and rt00.begin_token.end_token.next0_.is_char(':')): 
                    ok = True
                elif (rt00.begin_token.morph.number == MorphNumber.PLURAL): 
                    ok = True
                if (ok): 
                    p.add_slot(PersonReferent.ATTR_ATTR, rt00.begin_token.get_referent(), False, 0)
        if (ad is not None): 
            if (ad.overflow_level > 10): 
                return ReferentToken._new2480(p, begin, end, morph_, p._m_person_identity_typ)
            ad.overflow_level += 1
        attrs1 = None
        has_position = False
        open_br = False
        t = end.next0_
        first_pass3857 = True
        while True:
            if first_pass3857: first_pass3857 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                break
            if (t.is_newline_before): 
                if (t.newlines_before_count > 2): 
                    break
                if (attrs1 is not None and len(attrs1) > 0): 
                    break
                ml = MailLine.parse(t, 0, 0)
                if (ml is not None and ml.typ == MailLine.Types.FROM): 
                    break
                if (t.chars.is_capital_upper): 
                    attr1 = PersonAttrToken.try_attach(t, (None if ad is None else ad.local_ontology), PersonAttrToken.PersonAttrAttachAttrs.NO)
                    ok1 = False
                    if (attr1 is not None): 
                        if (has_prefix or attr1.is_newline_after or ((attr1.end_token.next0_ is not None and attr1.end_token.next0_.is_table_control_char))): 
                            ok1 = True
                        else: 
                            tt2 = t.next0_
                            while tt2 is not None and tt2.end_char <= attr1.end_char: 
                                if (tt2.is_whitespace_before): 
                                    ok1 = True
                                tt2 = tt2.next0_
                    else: 
                        ttt = PersonHelper.__correct_tail_attributes(p, t)
                        if (ttt is not None and ttt != t): 
                            t = ttt
                            end = t
                            continue
                    if (not ok1): 
                        break
            if (t.is_hiphen or t.is_char_of("_>|")): 
                continue
            if (t.is_value("МОДЕЛЬ", None)): 
                break
            tt = PersonHelper.__correct_tail_attributes(p, t)
            if (tt != t and tt is not None): 
                t = tt
                end = t
                continue
            is_be = False
            if (t.is_char('(') and t == end.next0_): 
                open_br = True
                t = t.next0_
                if (t is None): 
                    break
                pit1 = PersonItemToken.try_attach(t, None, PersonItemToken.ParseAttr.NO, None)
                if ((pit1 is not None and t.chars.is_capital_upper and pit1.end_token.next0_ is not None) and (isinstance(t, TextToken)) and pit1.end_token.next0_.is_char(')')): 
                    if (pit1.lastname is not None): 
                        inf = MorphBaseInfo._new2472(MorphCase.NOMINATIVE)
                        if (p.is_male): 
                            inf.gender = Utils.valToEnum((inf.gender) | (MorphGender.MASCULINE), MorphGender)
                        if (p.is_female): 
                            inf.gender = Utils.valToEnum((inf.gender) | (MorphGender.FEMINIE), MorphGender)
                        sur = PersonIdentityToken.create_lastname(pit1, inf)
                        if (sur is not None): 
                            p._add_fio_identity(sur, None, None)
                            t = pit1.end_token.next0_
                            end = t
                            continue
                if ((isinstance(t, TextToken)) and t.chars.is_latin_letter): 
                    pits = PersonItemToken.try_attach_list(t, None, PersonItemToken.ParseAttr.CANBELATIN, 10)
                    if (((pits is not None and len(pits) >= 2 and len(pits) <= 3) and pits[0].chars.is_latin_letter and pits[1].chars.is_latin_letter) and pits[len(pits) - 1].end_token.next0_ is not None and pits[len(pits) - 1].end_token.next0_.is_char(')')): 
                        pr2 = PersonReferent()
                        cou = 0
                        for pi0_ in pits: 
                            for si in p.slots: 
                                if (si.type_name == PersonReferent.ATTR_FIRSTNAME or si.type_name == PersonReferent.ATTR_MIDDLENAME or si.type_name == PersonReferent.ATTR_LASTNAME): 
                                    if (MiscHelper.can_be_equal_cyr_and_latss(str(si.value), pi0_.value)): 
                                        cou += 1
                                        pr2.add_slot(si.type_name, pi0_.value, False, 0)
                                        break
                        if (cou == len(pits)): 
                            for si in pr2.slots: 
                                p.add_slot(si.type_name, si.value, False, 0)
                            t = pits[len(pits) - 1].end_token.next0_
                            end = t
                            continue
            elif (t.is_comma): 
                t = t.next0_
                if ((isinstance(t, TextToken)) and t.is_value("WHO", None)): 
                    continue
                if ((isinstance(t, TextToken)) and t.chars.is_latin_letter): 
                    pits = PersonItemToken.try_attach_list(t, None, PersonItemToken.ParseAttr.CANBELATIN, 10)
                    if ((pits is not None and len(pits) >= 2 and len(pits) <= 3) and pits[0].chars.is_latin_letter and pits[1].chars.is_latin_letter): 
                        pr2 = PersonReferent()
                        cou = 0
                        for pi0_ in pits: 
                            for si in p.slots: 
                                if (si.type_name == PersonReferent.ATTR_FIRSTNAME or si.type_name == PersonReferent.ATTR_MIDDLENAME or si.type_name == PersonReferent.ATTR_LASTNAME): 
                                    if (MiscHelper.can_be_equal_cyr_and_latss(str(si.value), pi0_.value)): 
                                        cou += 1
                                        pr2.add_slot(si.type_name, pi0_.value, False, 0)
                                        break
                        if (cou == len(pits)): 
                            for si in pr2.slots: 
                                p.add_slot(si.type_name, si.value, False, 0)
                            t = pits[len(pits) - 1].end_token
                            end = t
                            continue
            elif ((isinstance(t, TextToken)) and t.is_verb_be): 
                t = t.next0_
            elif (t.is_and and t.is_whitespace_after and not t.is_newline_after): 
                if (t == end.next0_): 
                    break
                t = t.next0_
            elif (t.is_hiphen and t == end.next0_): 
                t = t.next0_
            elif (t.is_char('.') and t == end.next0_ and has_prefix): 
                t = t.next0_
            ttt2 = PersonHelper.create_nickname(p, t)
            if (ttt2 is not None): 
                end = ttt2
                t = end
                continue
            if (t is None): 
                break
            attr = None
            attr = PersonAttrToken.try_attach(t, (None if ad is None else ad.local_ontology), PersonAttrToken.PersonAttrAttachAttrs.NO)
            if (attr is None): 
                if ((t is not None and t.get_referent() is not None and t.get_referent().type_name == "GEO") and attrs1 is not None and open_br): 
                    continue
                if ((t.chars.is_capital_upper and open_br and t.next0_ is not None) and t.next0_.is_char(')')): 
                    if (p.find_slot(PersonReferent.ATTR_LASTNAME, None, True) is None): 
                        p.add_slot(PersonReferent.ATTR_LASTNAME, t.get_source_text().upper(), False, 0)
                        t = t.next0_
                        end = t
                if (t is not None and t.is_value("КОТОРЫЙ", None) and t.morph.number == MorphNumber.SINGULAR): 
                    if (not p.is_female and t.morph.gender == MorphGender.FEMINIE): 
                        p.is_female = True
                        p._correct_data()
                    elif (not p.is_male and t.morph.gender == MorphGender.MASCULINE): 
                        p.is_male = True
                        p._correct_data()
                break
            if (attr.morph.number == MorphNumber.PLURAL): 
                break
            if (attr.typ == PersonAttrTerminType.BESTREGARDS): 
                break
            if (attr.is_doubt): 
                if (has_prefix): 
                    pass
                elif (t.is_newline_before and attr.is_newline_after): 
                    pass
                elif (t.previous is not None and ((t.previous.is_hiphen or t.previous.is_char(':')))): 
                    pass
                else: 
                    break
            if (not morph_.case_.is_undefined and not attr.morph.case_.is_undefined): 
                if (((morph_.case_) & attr.morph.case_).is_undefined and not is_be): 
                    break
            if (open_br): 
                if (PersonAnalyzer._try_attach_person(t, ad, False, 0, True) is not None): 
                    break
            if (attrs1 is None): 
                if (t.previous.is_comma and t.previous == end.next0_): 
                    ttt = attr.end_token.next0_
                    if (ttt is not None): 
                        if (ttt.morph.class0_.is_verb): 
                            if (MiscHelper.can_be_start_of_sentence(begin)): 
                                pass
                            else: 
                                break
                attrs1 = list()
            attrs1.append(attr)
            if (attr.typ == PersonAttrTerminType.POSITION or attr.typ == PersonAttrTerminType.KING): 
                if (not is_be): 
                    has_position = True
            elif (attr.typ != PersonAttrTerminType.PREFIX): 
                if (attr.typ == PersonAttrTerminType.OTHER and attr.age is not None): 
                    pass
                else: 
                    attrs1 = (None)
                    break
            t = attr.end_token
        if (attrs1 is not None and has_position and attrs is not None): 
            te1 = attrs[len(attrs) - 1].end_token.next0_
            te2 = attrs1[0].begin_token
            if (te1.whitespaces_after_count > te2.whitespaces_before_count and (te2.whitespaces_before_count < 2)): 
                pass
            elif (attrs1[0].age is not None): 
                pass
            elif (((te1.is_hiphen or te1.is_char(':'))) and not attrs1[0].is_newline_before and ((te2.previous.is_comma or te2.previous == end))): 
                pass
            else: 
                for a in attrs: 
                    if (a.typ == PersonAttrTerminType.POSITION): 
                        te = attrs1[len(attrs1) - 1].end_token
                        if (te.next0_ is not None): 
                            if (not te.next0_.is_char('.')): 
                                attrs1 = (None)
                                break
        if (attrs1 is not None and not has_prefix): 
            attr = attrs1[len(attrs1) - 1]
            ok = False
            if (attr.end_token.next0_ is not None and attr.end_token.next0_.chars.is_capital_upper): 
                ok = True
            else: 
                rt = PersonAnalyzer._try_attach_person(attr.begin_token, ad, False, -1, False)
                if (rt is not None and (isinstance(rt.referent, PersonReferent))): 
                    ok = True
            if (ok): 
                if (attr.begin_token.whitespaces_before_count > attr.end_token.whitespaces_after_count): 
                    attrs1 = (None)
                elif (attr.begin_token.whitespaces_before_count == attr.end_token.whitespaces_after_count): 
                    rt1 = PersonAnalyzer._try_attach_person(attr.begin_token, ad, False, -1, False)
                    if (rt1 is not None): 
                        attrs1 = (None)
        if (attrs1 is not None): 
            for a in attrs1: 
                if (a.typ != PersonAttrTerminType.PREFIX): 
                    if (a.age is not None): 
                        p.add_slot(PersonReferent.ATTR_AGE, a.age, True, 0)
                    elif (a.prop_ref is None): 
                        p.add_slot(PersonReferent.ATTR_ATTR, a.value, False, 0)
                    else: 
                        p.add_slot(PersonReferent.ATTR_ATTR, a, False, 0)
                    end = a.end_token
                    if (a.gender != MorphGender.UNDEFINED and not p.is_female and not p.is_male): 
                        if (a.gender == MorphGender.MASCULINE and not p.is_male): 
                            p.is_male = True
                            p._correct_data()
                        elif (a.gender == MorphGender.FEMINIE and not p.is_female): 
                            p.is_female = True
                            p._correct_data()
            if (open_br): 
                if (end.next0_ is not None and end.next0_.is_char(')')): 
                    end = end.next0_
        crlf_cou = 0
        t = end.next0_
        first_pass3858 = True
        while True:
            if first_pass3858: first_pass3858 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                break
            if (t.is_newline_before): 
                ml = MailLine.parse(t, 0, 0)
                if (ml is not None and ml.typ == MailLine.Types.FROM): 
                    break
                crlf_cou += 1
            if (t.is_char_of(":,(") or t.is_hiphen): 
                continue
            if (t.is_char('.') and t == end.next0_): 
                continue
            r = t.get_referent()
            if (r is not None): 
                if (r.type_name == "PHONE" or r.type_name == "URI" or r.type_name == "ADDRESS"): 
                    ty = r.get_string_value("SCHEME")
                    if (r.type_name == "URI"): 
                        if ((ty != "mailto" and ty != "skype" and ty != "ICQ") and ty != "http"): 
                            break
                    p._add_contact(r)
                    end = t
                    crlf_cou = 0
                    continue
            if (isinstance(r, PersonIdentityReferent)): 
                p.add_slot(PersonReferent.ATTR_IDDOC, r, False, 0)
                end = t
                crlf_cou = 0
                continue
            if (r is not None and r.type_name == "ORGANIZATION"): 
                if (t.next0_ is not None and t.next0_.morph.class0_.is_verb): 
                    break
                if (begin.previous is not None and begin.previous.morph.class0_.is_verb): 
                    break
                if (t.whitespaces_after_count == 1): 
                    break
                exist = False
                for s in p.slots: 
                    if (s.type_name == PersonReferent.ATTR_ATTR and (isinstance(s.value, PersonPropertyReferent))): 
                        pr = Utils.asObjectOrNull(s.value, PersonPropertyReferent)
                        if (pr.find_slot(PersonPropertyReferent.ATTR_REF, r, True) is not None): 
                            exist = True
                            break
                    elif (s.type_name == PersonReferent.ATTR_ATTR and (isinstance(s.value, PersonAttrToken))): 
                        pr = Utils.asObjectOrNull(s.value, PersonAttrToken)
                        if (pr.referent.find_slot(PersonPropertyReferent.ATTR_REF, r, True) is not None): 
                            exist = True
                            break
                if (not exist): 
                    pat = PersonAttrToken(t, t)
                    pat.prop_ref = PersonPropertyReferent._new2442("сотрудник")
                    pat.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                    p.add_slot(PersonReferent.ATTR_ATTR, pat, False, 0)
                continue
            if (r is not None): 
                break
            if (not has_prefix or crlf_cou >= 2): 
                break
            rt = t.kit.process_referent("PERSON", t)
            if (rt is not None): 
                break
        if (ad is not None): 
            ad.overflow_level -= 1
        if (begin.is_value("НА", None) and begin.next0_ is not None and begin.next0_.is_value("ИМЯ", None)): 
            t0 = begin.previous
            if (t0 is not None and t0.is_comma): 
                t0 = t0.previous
            if (t0 is not None and (isinstance(t0.get_referent(), PersonIdentityReferent))): 
                p.add_slot(PersonReferent.ATTR_IDDOC, t0.get_referent(), False, 0)
        return ReferentToken._new2480(p, begin, end, morph_, p._m_person_identity_typ)
    
    @staticmethod
    def create_sex(pr : 'PersonReferent', t : 'Token') -> 'Token':
        """ Выделить пол
        
        Args:
            pr(PersonReferent): 
            t(Token): 
        
        """
        if (t is None): 
            return None
        while t.next0_ is not None:
            if (t.is_value("ПОЛ", None) or t.is_hiphen or t.is_char(':')): 
                t = t.next0_
            else: 
                break
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        ok = False
        if ((tt.term == "МУЖ" or tt.term == "МУЖС" or tt.term == "МУЖСК") or tt.is_value("МУЖСКОЙ", None)): 
            pr.is_male = True
            ok = True
        elif ((tt.term == "ЖЕН" or tt.term == "ЖЕНС" or tt.term == "ЖЕНСК") or tt.is_value("ЖЕНСКИЙ", None)): 
            pr.is_female = True
            ok = True
        if (not ok): 
            return None
        while t.next0_ is not None:
            if (t.next0_.is_value("ПОЛ", None) or t.next0_.is_char('.')): 
                t = t.next0_
            else: 
                break
        return t
    
    @staticmethod
    def create_nickname(pr : 'PersonReferent', t : 'Token') -> 'Token':
        """ Выделить кличку
        
        Args:
            pr(PersonReferent): 
            t(Token): начальный токен
        
        Returns:
            Token: если не null, то последний токен клички, а в pr запишет саму кличку
        """
        has_keyw = False
        is_br = False
        first_pass3859 = True
        while True:
            if first_pass3859: first_pass3859 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_hiphen or t.is_comma or t.is_char_of(".:;")): 
                continue
            if (t.morph.class0_.is_preposition): 
                continue
            if (t.is_char('(')): 
                is_br = True
                continue
            if ((t.is_value("ПРОЗВИЩЕ", "ПРІЗВИСЬКО") or t.is_value("КЛИЧКА", None) or t.is_value("ПСЕВДОНИМ", "ПСЕВДОНІМ")) or t.is_value("ПСЕВДО", None) or t.is_value("ПОЗЫВНОЙ", "ПОЗИВНИЙ")): 
                has_keyw = True
                continue
            break
        if (not has_keyw or t is None): 
            return None
        if (BracketHelper.is_bracket(t, True)): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                ni = MiscHelper.get_text_value(br.begin_token.next0_, br.end_token.previous, GetTextAttr.NO)
                if (ni is not None): 
                    pr.add_slot(PersonReferent.ATTR_NICKNAME, ni, False, 0)
                    t = br.end_token
                    tt = t.next0_
                    first_pass3860 = True
                    while True:
                        if first_pass3860: first_pass3860 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        if (tt.is_comma_and): 
                            continue
                        if (not BracketHelper.is_bracket(tt, True)): 
                            break
                        br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                        if (br is None): 
                            break
                        ni = MiscHelper.get_text_value(br.begin_token.next0_, br.end_token.previous, GetTextAttr.NO)
                        if (ni is not None): 
                            pr.add_slot(PersonReferent.ATTR_NICKNAME, ni, False, 0)
                        tt = br.end_token
                        t = tt
                    if (is_br and t.next0_ is not None and t.next0_.is_char(')')): 
                        t = t.next0_
                    return t
        else: 
            ret = None
            first_pass3861 = True
            while True:
                if first_pass3861: first_pass3861 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_comma_and): 
                    continue
                if (ret is not None and t.chars.is_all_lower): 
                    break
                if (t.whitespaces_before_count > 2): 
                    break
                pli = PersonItemToken.try_attach_list(t, None, PersonItemToken.ParseAttr.NO, 10)
                if (pli is not None and ((len(pli) == 1 or len(pli) == 2))): 
                    ni = MiscHelper.get_text_value(pli[0].begin_token, pli[len(pli) - 1].end_token, GetTextAttr.NO)
                    if (ni is not None): 
                        pr.add_slot(PersonReferent.ATTR_NICKNAME, ni, False, 0)
                        t = pli[len(pli) - 1].end_token
                        if (is_br and t.next0_ is not None and t.next0_.is_char(')')): 
                            t = t.next0_
                        ret = t
                        continue
                if ((isinstance(t, ReferentToken)) and not t.chars.is_all_lower and t.begin_token == t.end_token): 
                    val = MiscHelper.get_text_value_of_meta_token(Utils.asObjectOrNull(t, ReferentToken), GetTextAttr.NO)
                    pr.add_slot(PersonReferent.ATTR_NICKNAME, val, False, 0)
                    if (is_br and t.next0_ is not None and t.next0_.is_char(')')): 
                        t = t.next0_
                    ret = t
                    continue
                break
            return ret
        return None
    
    @staticmethod
    def is_person_say_or_attr_after(t : 'Token') -> bool:
        if (t is None): 
            return False
        tt = PersonHelper.__correct_tail_attributes(None, t)
        if (tt is not None and tt != t): 
            return True
        if (t.is_comma and t.next0_ is not None): 
            t = t.next0_
        if (t.chars.is_latin_letter): 
            if (t.is_value("SAY", None) or t.is_value("ASK", None) or t.is_value("WHO", None)): 
                return True
        if (t.is_char('.') and (isinstance(t.next0_, TextToken)) and ((t.next0_.morph.class0_.is_pronoun or t.next0_.morph.class0_.is_personal_pronoun))): 
            if (t.next0_.morph.gender == MorphGender.FEMINIE or t.next0_.morph.gender == MorphGender.MASCULINE): 
                return True
        if (t.is_comma and t.next0_ is not None): 
            t = t.next0_
        if (PersonAttrToken.try_attach(t, None, PersonAttrToken.PersonAttrAttachAttrs.NO) is not None): 
            return True
        return False
    
    @staticmethod
    def __correct_tail_attributes(p : 'PersonReferent', t0 : 'Token') -> 'Token':
        res = t0
        t = t0
        if (t is not None and t.is_char(',')): 
            t = t.next0_
        born = False
        die = False
        if (t is not None and ((t.is_value("РОДИТЬСЯ", "НАРОДИТИСЯ") or t.is_value("BORN", None)))): 
            t = t.next0_
            born = True
        elif (t is not None and ((t.is_value("УМЕРЕТЬ", "ПОМЕРТИ") or t.is_value("СКОНЧАТЬСЯ", None) or t.is_value("DIED", None)))): 
            t = t.next0_
            die = True
        elif ((t is not None and t.is_value("ДАТА", None) and t.next0_ is not None) and t.next0_.is_value("РОЖДЕНИЕ", "НАРОДЖЕННЯ")): 
            t = t.next0_.next0_
            born = True
        while t is not None:
            if (t.morph.class0_.is_preposition or t.is_hiphen or t.is_char(':')): 
                t = t.next0_
            else: 
                break
        if (t is not None and t.get_referent() is not None): 
            r = t.get_referent()
            if (r.type_name == "DATE"): 
                t1 = t
                if (t.next0_ is not None and ((t.next0_.is_value("Р", None) or t.next0_.is_value("РОЖДЕНИЕ", "НАРОДЖЕННЯ")))): 
                    born = True
                    t1 = t.next0_
                    if (t1.next0_ is not None and t1.next0_.is_char('.')): 
                        t1 = t1.next0_
                if (born): 
                    if (p is not None): 
                        p.add_slot(PersonReferent.ATTR_BORN, r, False, 0)
                    res = t1
                    t = t1
                elif (die): 
                    if (p is not None): 
                        p.add_slot(PersonReferent.ATTR_DIE, r, False, 0)
                    res = t1
                    t = t1
        if (die and t is not None): 
            ag = NumberHelper.try_parse_age(t.next0_)
            if (ag is not None): 
                if (p is not None): 
                    p.add_slot(PersonReferent.ATTR_AGE, str(ag.value), False, 0)
                t = ag.end_token.next0_
                res = ag.end_token
        if (t is None): 
            return res
        if (t.is_char('(')): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                t1 = t.next0_
                born = False
                if (t1.is_value("РОД", None)): 
                    born = True
                    t1 = t1.next0_
                    if (t1 is not None and t1.is_char('.')): 
                        t1 = t1.next0_
                if (isinstance(t1, ReferentToken)): 
                    r = t1.get_referent()
                    if (r.type_name == "DATERANGE" and t1.next0_ == br.end_token): 
                        bd = Utils.asObjectOrNull(r.get_slot_value("FROM"), Referent)
                        to = Utils.asObjectOrNull(r.get_slot_value("TO"), Referent)
                        if (bd is not None and to is not None): 
                            if (p is not None): 
                                p.add_slot(PersonReferent.ATTR_BORN, bd, False, 0)
                                p.add_slot(PersonReferent.ATTR_DIE, to, False, 0)
                            res = br.end_token
                            t = res
                    elif (r.type_name == "DATE" and t1.next0_ == br.end_token): 
                        if (p is not None): 
                            p.add_slot(PersonReferent.ATTR_BORN, r, False, 0)
                        res = br.end_token
                        t = res
        return res