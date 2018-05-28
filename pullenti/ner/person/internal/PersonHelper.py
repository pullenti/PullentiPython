# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ner.person.internal.PersonAttrTerminType import PersonAttrTerminType
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber



from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.NumberHelper import NumberHelper


class PersonHelper:
    
    @staticmethod
    def _create_referent_token(p : 'PersonReferent', begin : 'Token', end : 'Token', morph_ : 'MorphCollection', attrs : typing.List['PersonAttrToken'], ad : 'PersonAnalyzerData', for_attribute : bool, after_be_predicate : bool) -> 'ReferentToken':
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.morph.MorphBaseInfo import MorphBaseInfo
        from pullenti.ner.MorphCollection import MorphCollection
        from pullenti.ner.mail.internal.MailLine import MailLine
        from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
        from pullenti.morph.MorphCase import MorphCase
        from pullenti.ner.person.internal.PersonIdentityToken import PersonIdentityToken
        from pullenti.ner.person.PersonAnalyzer import PersonAnalyzer
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent
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
        elif (isinstance(begin.previous, TextToken) and (begin.whitespaces_before_count < 3)): 
            if ((begin.previous if isinstance(begin.previous, TextToken) else None).term == "ИП"): 
                a = PersonAttrToken(begin.previous, begin.previous)
                a.prop_ref = PersonPropertyReferent()
                a.prop_ref.name = "индивидуальный предприниматель"
                p.add_slot(PersonReferent.ATTR_ATTR, a, False, 0)
                begin = begin.previous
        m0 = MorphCollection()
        for it in morph_.items: 
            bi = MorphBaseInfo(it)
            bi.number = MorphNumber.SINGULAR
            if (bi.gender == MorphGender.UNDEFINED): 
                if (p.is_male and not p.is_female): 
                    bi.gender = MorphGender.MASCULINE
                if (not p.is_male and p.is_female): 
                    bi.gender = MorphGender.FEMINIE
            m0.add_item(bi)
        morph_ = m0
        if ((attrs is not None and len(attrs) > 0 and not attrs[0].morph.case.is_undefined) and morph_.case.is_undefined): 
            morph_.case = attrs[0].morph.case
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
            return ReferentToken._new2147(p, begin, end, morph_, p._m_person_identity_typ)
        if ((begin.previous is not None and begin.previous.is_comma_and and isinstance(begin.previous.previous, ReferentToken)) and isinstance(begin.previous.previous.get_referent(), PersonReferent)): 
            rt00 = (begin.previous.previous if isinstance(begin.previous.previous, ReferentToken) else None)
            ttt = rt00
            while ttt is not None: 
                if (ttt.previous is None or not ((isinstance(ttt.previous.previous, ReferentToken)))): 
                    break
                if (not ttt.previous.is_comma_and or not ((isinstance(ttt.previous.previous.get_referent(), PersonReferent)))): 
                    break
                rt00 = (ttt.previous.previous if isinstance(ttt.previous.previous, ReferentToken) else None)
                ttt = rt00
            if (isinstance(rt00.begin_token.get_referent(), PersonPropertyReferent)): 
                ok = False
                if ((rt00.begin_token if isinstance(rt00.begin_token, ReferentToken) else None).end_token.next0 is not None and (rt00.begin_token if isinstance(rt00.begin_token, ReferentToken) else None).end_token.next0.is_char(':')): 
                    ok = True
                elif (rt00.begin_token.morph.number == MorphNumber.PLURAL): 
                    ok = True
                if (ok): 
                    p.add_slot(PersonReferent.ATTR_ATTR, rt00.begin_token.get_referent(), False, 0)
        if (ad is not None): 
            if (ad.overflow_level > 10): 
                return ReferentToken._new2147(p, begin, end, morph_, p._m_person_identity_typ)
            ad.overflow_level += 1
        attrs1 = None
        has_position = False
        open_br = False
        t = end.next0
        first_pass2859 = True
        while True:
            if first_pass2859: first_pass2859 = False
            else: t = t.next0
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                break
            if (t.is_newline_before): 
                if (t.newlines_before_count > 2): 
                    break
                if (attrs1 is not None and len(attrs1) > 0): 
                    break
                ml = MailLine.parse(t, 0)
                if (ml is not None and ml.typ == MailLine.Types.FROM): 
                    break
                if (t.chars.is_capital_upper): 
                    attr1 = PersonAttrToken.try_attach(t, (None if ad is None else ad.local_ontology), PersonAttrToken.PersonAttrAttachAttrs.NO)
                    ok1 = False
                    if (attr1 is not None): 
                        if (has_prefix or attr1.is_newline_after or ((attr1.end_token.next0 is not None and attr1.end_token.next0.is_table_control_char))): 
                            ok1 = True
                        else: 
                            tt2 = t.next0
                            while tt2 is not None and tt2.end_char <= attr1.end_char: 
                                if (tt2.is_whitespace_before): 
                                    ok1 = True
                                tt2 = tt2.next0
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
            if (t.is_char('(') and t == end.next0): 
                open_br = True
                t = t.next0
                if (t is None): 
                    break
                pit1 = PersonItemToken.try_attach(t, None, PersonItemToken.ParseAttr.NO, None)
                if ((pit1 is not None and t.chars.is_capital_upper and pit1.end_token.next0 is not None) and isinstance(t, TextToken) and pit1.end_token.next0.is_char(')')): 
                    if (pit1.lastname is not None): 
                        inf = MorphBaseInfo._new2094(MorphCase.NOMINATIVE)
                        if (p.is_male): 
                            inf.gender |= MorphGender.MASCULINE
                        if (p.is_female): 
                            inf.gender |= MorphGender.FEMINIE
                        sur = PersonIdentityToken.create_lastname(pit1, inf)
                        if (sur is not None): 
                            p._add_fio_identity(sur, None, None)
                            t = pit1.end_token.next0
                            end = t
                            continue
            elif (t.is_comma): 
                t = t.next0
                if (isinstance(t, TextToken) and (t if isinstance(t, TextToken) else None).is_value("WHO", None)): 
                    continue
            elif (isinstance(t, TextToken) and (t if isinstance(t, TextToken) else None).is_verb_be): 
                t = t.next0
            elif (t.is_and and t.is_whitespace_after and not t.is_newline_after): 
                if (t == end.next0): 
                    break
                t = t.next0
            elif (t.is_hiphen and t == end.next0): 
                t = t.next0
            elif (t.is_char('.') and t == end.next0 and has_prefix): 
                t = t.next0
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
                if ((t.chars.is_capital_upper and open_br and t.next0 is not None) and t.next0.is_char(')')): 
                    if (p.find_slot(PersonReferent.ATTR_LASTNAME, None, True) is None): 
                        p.add_slot(PersonReferent.ATTR_LASTNAME, t.get_source_text().upper(), False, 0)
                        t = t.next0
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
            if (not morph_.case.is_undefined and not attr.morph.case.is_undefined): 
                if ((morph_.case & attr.morph.case).is_undefined and not is_be): 
                    break
            if (open_br): 
                if (PersonAnalyzer._try_attach_person(t, ad, False, 0, True) is not None): 
                    break
            if (attrs1 is None): 
                if (t.previous.is_comma and t.previous == end.next0): 
                    ttt = attr.end_token.next0
                    if (ttt is not None): 
                        if (ttt.morph.class0.is_verb): 
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
                    attrs1 = None
                    break
            t = attr.end_token
        if (attrs1 is not None and has_position and attrs is not None): 
            te1 = attrs[len(attrs) - 1].end_token.next0
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
                        if (te.next0 is not None): 
                            if (not te.next0.is_char('.')): 
                                attrs1 = None
                                break
        if (attrs1 is not None and not has_prefix): 
            attr = attrs1[len(attrs1) - 1]
            ok = False
            if (attr.end_token.next0 is not None and attr.end_token.next0.chars.is_capital_upper): 
                ok = True
            else: 
                rt = PersonAnalyzer._try_attach_person(attr.begin_token, ad, False, -1, False)
                if (rt is not None and isinstance(rt.referent, PersonReferent)): 
                    ok = True
            if (ok): 
                if (attr.begin_token.whitespaces_before_count > attr.end_token.whitespaces_after_count): 
                    attrs1 = None
                elif (attr.begin_token.whitespaces_before_count == attr.end_token.whitespaces_after_count): 
                    rt1 = PersonAnalyzer._try_attach_person(attr.begin_token, ad, False, -1, False)
                    if (rt1 is not None): 
                        attrs1 = None
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
                if (end.next0 is not None and end.next0.is_char(')')): 
                    end = end.next0
        crlf_cou = 0
        t = end.next0
        first_pass2860 = True
        while True:
            if first_pass2860: first_pass2860 = False
            else: t = t.next0
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                break
            if (t.is_newline_before): 
                ml = MailLine.parse(t, 0)
                if (ml is not None and ml.typ == MailLine.Types.FROM): 
                    break
                crlf_cou += 1
            if (t.is_char_of(":,(") or t.is_hiphen): 
                continue
            if (t.is_char('.') and t == end.next0): 
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
                if (t.next0 is not None and t.next0.morph.class0.is_verb): 
                    break
                if (begin.previous is not None and begin.previous.morph.class0.is_verb): 
                    break
                if (t.whitespaces_after_count == 1): 
                    break
                exist = False
                for s in p.slots: 
                    if (s.type_name == PersonReferent.ATTR_ATTR and isinstance(s.value, PersonPropertyReferent)): 
                        pr = (s.value if isinstance(s.value, PersonPropertyReferent) else None)
                        if (pr.find_slot(PersonPropertyReferent.ATTR_REF, r, True) is not None): 
                            exist = True
                            break
                    elif (s.type_name == PersonReferent.ATTR_ATTR and isinstance(s.value, PersonAttrToken)): 
                        pr = (s.value if isinstance(s.value, PersonAttrToken) else None)
                        if (pr.referent.find_slot(PersonPropertyReferent.ATTR_REF, r, True) is not None): 
                            exist = True
                            break
                if (not exist): 
                    pat = PersonAttrToken(t, t)
                    pat.prop_ref = PersonPropertyReferent._new2064("сотрудник")
                    pat.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                    p.add_slot(PersonReferent.ATTR_ATTR, pat, False, 0)
                continue
            if (r is not None): 
                break
            if (not has_prefix or crlf_cou >= 2): 
                break
        if (ad is not None): 
            ad.overflow_level -= 1
        return ReferentToken._new2147(p, begin, end, morph_, p._m_person_identity_typ)
    
    @staticmethod
    def create_nickname(pr : 'PersonReferent', t : 'Token') -> 'Token':
        """ Выделить кличку
        
        Args:
            pr(PersonReferent): 
            t(Token): начальный токен
        
        Returns:
            Token: если не null, то последний токен клички, а в pr запишет саму кличку
        """
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
        has_keyw = False
        is_br = False
        first_pass2861 = True
        while True:
            if first_pass2861: first_pass2861 = False
            else: t = t.next0
            if (not (t is not None)): break
            if (t.is_hiphen or t.is_comma or t.is_char_of(".:;")): 
                continue
            if (t.morph.class0.is_preposition): 
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
                ni = MiscHelper.get_text_value(br.begin_token.next0, br.end_token.previous, GetTextAttr.NO)
                if (ni is not None): 
                    pr.add_slot(PersonReferent.ATTR_NICKNAME, ni, False, 0)
                    t = br.end_token
                    tt = t.next0
                    first_pass2862 = True
                    while True:
                        if first_pass2862: first_pass2862 = False
                        else: tt = tt.next0
                        if (not (tt is not None)): break
                        if (tt.is_comma_and): 
                            continue
                        if (not BracketHelper.is_bracket(tt, True)): 
                            break
                        br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                        if (br is None): 
                            break
                        ni = MiscHelper.get_text_value(br.begin_token.next0, br.end_token.previous, GetTextAttr.NO)
                        if (ni is not None): 
                            pr.add_slot(PersonReferent.ATTR_NICKNAME, ni, False, 0)
                        tt = br.end_token
                        t = tt
                    if (is_br and t.next0 is not None and t.next0.is_char(')')): 
                        t = t.next0
                    return t
        else: 
            pli = PersonItemToken.try_attach_list(t, None, PersonItemToken.ParseAttr.NO, 10)
            if (pli is not None and ((len(pli) == 1 or len(pli) == 2))): 
                ni = MiscHelper.get_text_value(pli[0].begin_token, pli[len(pli) - 1].end_token, GetTextAttr.NO)
                if (ni is not None): 
                    pr.add_slot(PersonReferent.ATTR_NICKNAME, ni, False, 0)
                    t = pli[len(pli) - 1].end_token
                    if (is_br and t.next0 is not None and t.next0.is_char(')')): 
                        t = t.next0
                    return t
        return None
    
    @staticmethod
    def is_person_say_or_attr_after(t : 'Token') -> bool:
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        if (t is None): 
            return False
        tt = PersonHelper.__correct_tail_attributes(None, t)
        if (tt is not None and tt != t): 
            return True
        if (t.is_comma and t.next0 is not None): 
            t = t.next0
        if (t.chars.is_latin_letter): 
            if (t.is_value("SAY", None) or t.is_value("ASK", None) or t.is_value("WHO", None)): 
                return True
        if (t.is_char('.') and isinstance(t.next0, TextToken) and ((t.next0.morph.class0.is_pronoun or t.next0.morph.class0.is_personal_pronoun))): 
            if (t.next0.morph.gender == MorphGender.FEMINIE or t.next0.morph.gender == MorphGender.MASCULINE): 
                return True
        if (t.is_comma and t.next0 is not None): 
            t = t.next0
        if (PersonAttrToken.try_attach(t, None, PersonAttrToken.PersonAttrAttachAttrs.NO) is not None): 
            return True
        return False
    
    @staticmethod
    def __correct_tail_attributes(p : 'PersonReferent', t0 : 'Token') -> 'Token':
        from pullenti.ner.Referent import Referent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.ReferentToken import ReferentToken
        res = t0
        t = t0
        if (t is not None and t.is_char(',')): 
            t = t.next0
        born = False
        die = False
        if (t is not None and ((t.is_value("РОДИТЬСЯ", "НАРОДИТИСЯ") or t.is_value("BORN", None)))): 
            t = t.next0
            born = True
        elif (t is not None and ((t.is_value("УМЕРЕТЬ", "ПОМЕРТИ") or t.is_value("СКОНЧАТЬСЯ", None) or t.is_value("DIED", None)))): 
            t = t.next0
            die = True
        elif ((t is not None and t.is_value("ДАТА", None) and t.next0 is not None) and t.next0.is_value("РОЖДЕНИЕ", "НАРОДЖЕННЯ")): 
            t = t.next0.next0
            born = True
        while t is not None:
            if (t.morph.class0.is_preposition or t.is_hiphen or t.is_char(':')): 
                t = t.next0
            else: 
                break
        if (t is not None and t.get_referent() is not None): 
            r = t.get_referent()
            if (r.type_name == "DATE"): 
                t1 = t
                if (t.next0 is not None and ((t.next0.is_value("Р", None) or t.next0.is_value("РОЖДЕНИЕ", "НАРОДЖЕННЯ")))): 
                    born = True
                    t1 = t.next0
                    if (t1.next0 is not None and t1.next0.is_char('.')): 
                        t1 = t1.next0
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
            ag = NumberHelper.try_parse_age(t.next0)
            if (ag is not None): 
                if (p is not None): 
                    p.add_slot(PersonReferent.ATTR_AGE, str(ag.value), False, 0)
                t = ag.end_token.next0
                res = ag.end_token
        if (t is None): 
            return res
        if (t.is_char('(')): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                t1 = t.next0
                born = False
                if (t1.is_value("РОД", None)): 
                    born = True
                    t1 = t1.next0
                    if (t1 is not None and t1.is_char('.')): 
                        t1 = t1.next0
                if (isinstance(t1, ReferentToken)): 
                    r = t1.get_referent()
                    if (r.type_name == "DATERANGE" and t1.next0 == br.end_token): 
                        bd = (r.get_value("FROM") if isinstance(r.get_value("FROM"), Referent) else None)
                        to = (r.get_value("TO") if isinstance(r.get_value("TO"), Referent) else None)
                        if (bd is not None and to is not None): 
                            if (p is not None): 
                                p.add_slot(PersonReferent.ATTR_BORN, bd, False, 0)
                                p.add_slot(PersonReferent.ATTR_DIE, to, False, 0)
                            res = br.end_token
                            t = res
                    elif (r.type_name == "DATE" and t1.next0 == br.end_token): 
                        if (p is not None): 
                            p.add_slot(PersonReferent.ATTR_BORN, r, False, 0)
                        res = br.end_token
                        t = res
        return res