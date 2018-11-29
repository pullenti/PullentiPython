# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.ner.person.internal.PersonAttrTerminType import PersonAttrTerminType
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.NumberHelper import NumberHelper


class PersonHelper:
    
    @staticmethod
    def _createReferentToken(p : 'PersonReferent', begin : 'Token', end : 'Token', morph_ : 'MorphCollection', attrs : typing.List['PersonAttrToken'], ad : 'PersonAnalyzerData', for_attribute : bool, after_be_predicate : bool) -> 'ReferentToken':
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
                            p.addSlot(PersonReferent.ATTR_AGE, a.age, False, 0)
                        if (a.prop_ref is None): 
                            p.addSlot(PersonReferent.ATTR_ATTR, a.value, False, 0)
                        else: 
                            p.addSlot(PersonReferent.ATTR_ATTR, a, False, 0)
                    elif (a.gender == MorphGender.FEMINIE and not p.is_female): 
                        p.is_female = True
                    elif (a.gender == MorphGender.MASCULINE and not p.is_male): 
                        p.is_male = True
        elif ((isinstance(begin.previous, TextToken)) and (begin.whitespaces_before_count < 3)): 
            if ((Utils.asObjectOrNull(begin.previous, TextToken)).term == "ИП"): 
                a = PersonAttrToken(begin.previous, begin.previous)
                a.prop_ref = PersonPropertyReferent()
                a.prop_ref.name = "индивидуальный предприниматель"
                p.addSlot(PersonReferent.ATTR_ATTR, a, False, 0)
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
            m0.addItem(bi)
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
            if (ttt.isValue("ИМЕНИ", "ІМЕНІ")): 
                for_attribute = True
            else: 
                if (ttt.isChar('.') and ttt.previous is not None): 
                    ttt = ttt.previous
                if (ttt.whitespaces_after_count < 3): 
                    if (ttt.isValue("ИМ", "ІМ")): 
                        for_attribute = True
        if (for_attribute): 
            return ReferentToken._new2341(p, begin, end, morph_, p._m_person_identity_typ)
        if ((begin.previous is not None and begin.previous.is_comma_and and (isinstance(begin.previous.previous, ReferentToken))) and (isinstance(begin.previous.previous.getReferent(), PersonReferent))): 
            rt00 = Utils.asObjectOrNull(begin.previous.previous, ReferentToken)
            ttt = rt00
            while ttt is not None: 
                if (ttt.previous is None or not ((isinstance(ttt.previous.previous, ReferentToken)))): 
                    break
                if (not ttt.previous.is_comma_and or not ((isinstance(ttt.previous.previous.getReferent(), PersonReferent)))): 
                    break
                rt00 = (Utils.asObjectOrNull(ttt.previous.previous, ReferentToken))
                ttt = (rt00)
            if (isinstance(rt00.begin_token.getReferent(), PersonPropertyReferent)): 
                ok = False
                if ((Utils.asObjectOrNull(rt00.begin_token, ReferentToken)).end_token.next0_ is not None and (Utils.asObjectOrNull(rt00.begin_token, ReferentToken)).end_token.next0_.isChar(':')): 
                    ok = True
                elif (rt00.begin_token.morph.number == MorphNumber.PLURAL): 
                    ok = True
                if (ok): 
                    p.addSlot(PersonReferent.ATTR_ATTR, rt00.begin_token.getReferent(), False, 0)
        if (ad is not None): 
            if (ad.overflow_level > 10): 
                return ReferentToken._new2341(p, begin, end, morph_, p._m_person_identity_typ)
            ad.overflow_level += 1
        attrs1 = None
        has_position = False
        open_br = False
        t = end.next0_
        first_pass3107 = True
        while True:
            if first_pass3107: first_pass3107 = False
            else: t = t.next0_
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
                    attr1 = PersonAttrToken.tryAttach(t, (None if ad is None else ad.local_ontology), PersonAttrToken.PersonAttrAttachAttrs.NO)
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
                        ttt = PersonHelper.__correctTailAttributes(p, t)
                        if (ttt is not None and ttt != t): 
                            t = ttt
                            end = t
                            continue
                    if (not ok1): 
                        break
            if (t.is_hiphen or t.isCharOf("_>|")): 
                continue
            if (t.isValue("МОДЕЛЬ", None)): 
                break
            tt = PersonHelper.__correctTailAttributes(p, t)
            if (tt != t and tt is not None): 
                t = tt
                end = t
                continue
            is_be = False
            if (t.isChar('(') and t == end.next0_): 
                open_br = True
                t = t.next0_
                if (t is None): 
                    break
                pit1 = PersonItemToken.tryAttach(t, None, PersonItemToken.ParseAttr.NO, None)
                if ((pit1 is not None and t.chars.is_capital_upper and pit1.end_token.next0_ is not None) and (isinstance(t, TextToken)) and pit1.end_token.next0_.isChar(')')): 
                    if (pit1.lastname is not None): 
                        inf = MorphBaseInfo._new2288(MorphCase.NOMINATIVE)
                        if (p.is_male): 
                            inf.gender = Utils.valToEnum((inf.gender) | (MorphGender.MASCULINE), MorphGender)
                        if (p.is_female): 
                            inf.gender = Utils.valToEnum((inf.gender) | (MorphGender.FEMINIE), MorphGender)
                        sur = PersonIdentityToken.createLastname(pit1, inf)
                        if (sur is not None): 
                            p._addFioIdentity(sur, None, None)
                            t = pit1.end_token.next0_
                            end = t
                            continue
            elif (t.is_comma): 
                t = t.next0_
                if ((isinstance(t, TextToken)) and (Utils.asObjectOrNull(t, TextToken)).isValue("WHO", None)): 
                    continue
            elif ((isinstance(t, TextToken)) and (Utils.asObjectOrNull(t, TextToken)).is_verb_be): 
                t = t.next0_
            elif (t.is_and and t.is_whitespace_after and not t.is_newline_after): 
                if (t == end.next0_): 
                    break
                t = t.next0_
            elif (t.is_hiphen and t == end.next0_): 
                t = t.next0_
            elif (t.isChar('.') and t == end.next0_ and has_prefix): 
                t = t.next0_
            ttt2 = PersonHelper.createNickname(p, t)
            if (ttt2 is not None): 
                end = ttt2
                t = end
                continue
            if (t is None): 
                break
            attr = None
            attr = PersonAttrToken.tryAttach(t, (None if ad is None else ad.local_ontology), PersonAttrToken.PersonAttrAttachAttrs.NO)
            if (attr is None): 
                if ((t is not None and t.getReferent() is not None and t.getReferent().type_name == "GEO") and attrs1 is not None and open_br): 
                    continue
                if ((t.chars.is_capital_upper and open_br and t.next0_ is not None) and t.next0_.isChar(')')): 
                    if (p.findSlot(PersonReferent.ATTR_LASTNAME, None, True) is None): 
                        p.addSlot(PersonReferent.ATTR_LASTNAME, t.getSourceText().upper(), False, 0)
                        t = t.next0_
                        end = t
                if (t is not None and t.isValue("КОТОРЫЙ", None) and t.morph.number == MorphNumber.SINGULAR): 
                    if (not p.is_female and t.morph.gender == MorphGender.FEMINIE): 
                        p.is_female = True
                        p._correctData()
                    elif (not p.is_male and t.morph.gender == MorphGender.MASCULINE): 
                        p.is_male = True
                        p._correctData()
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
                elif (t.previous is not None and ((t.previous.is_hiphen or t.previous.isChar(':')))): 
                    pass
                else: 
                    break
            if (not morph_.case_.is_undefined and not attr.morph.case_.is_undefined): 
                if (((morph_.case_) & attr.morph.case_).is_undefined and not is_be): 
                    break
            if (open_br): 
                if (PersonAnalyzer._tryAttachPerson(t, ad, False, 0, True) is not None): 
                    break
            if (attrs1 is None): 
                if (t.previous.is_comma and t.previous == end.next0_): 
                    ttt = attr.end_token.next0_
                    if (ttt is not None): 
                        if (ttt.morph.class0_.is_verb): 
                            if (MiscHelper.canBeStartOfSentence(begin)): 
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
            elif (((te1.is_hiphen or te1.isChar(':'))) and not attrs1[0].is_newline_before and ((te2.previous.is_comma or te2.previous == end))): 
                pass
            else: 
                for a in attrs: 
                    if (a.typ == PersonAttrTerminType.POSITION): 
                        te = attrs1[len(attrs1) - 1].end_token
                        if (te.next0_ is not None): 
                            if (not te.next0_.isChar('.')): 
                                attrs1 = (None)
                                break
        if (attrs1 is not None and not has_prefix): 
            attr = attrs1[len(attrs1) - 1]
            ok = False
            if (attr.end_token.next0_ is not None and attr.end_token.next0_.chars.is_capital_upper): 
                ok = True
            else: 
                rt = PersonAnalyzer._tryAttachPerson(attr.begin_token, ad, False, -1, False)
                if (rt is not None and (isinstance(rt.referent, PersonReferent))): 
                    ok = True
            if (ok): 
                if (attr.begin_token.whitespaces_before_count > attr.end_token.whitespaces_after_count): 
                    attrs1 = (None)
                elif (attr.begin_token.whitespaces_before_count == attr.end_token.whitespaces_after_count): 
                    rt1 = PersonAnalyzer._tryAttachPerson(attr.begin_token, ad, False, -1, False)
                    if (rt1 is not None): 
                        attrs1 = (None)
        if (attrs1 is not None): 
            for a in attrs1: 
                if (a.typ != PersonAttrTerminType.PREFIX): 
                    if (a.age is not None): 
                        p.addSlot(PersonReferent.ATTR_AGE, a.age, True, 0)
                    elif (a.prop_ref is None): 
                        p.addSlot(PersonReferent.ATTR_ATTR, a.value, False, 0)
                    else: 
                        p.addSlot(PersonReferent.ATTR_ATTR, a, False, 0)
                    end = a.end_token
                    if (a.gender != MorphGender.UNDEFINED and not p.is_female and not p.is_male): 
                        if (a.gender == MorphGender.MASCULINE and not p.is_male): 
                            p.is_male = True
                            p._correctData()
                        elif (a.gender == MorphGender.FEMINIE and not p.is_female): 
                            p.is_female = True
                            p._correctData()
            if (open_br): 
                if (end.next0_ is not None and end.next0_.isChar(')')): 
                    end = end.next0_
        crlf_cou = 0
        t = end.next0_
        first_pass3108 = True
        while True:
            if first_pass3108: first_pass3108 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                break
            if (t.is_newline_before): 
                ml = MailLine.parse(t, 0)
                if (ml is not None and ml.typ == MailLine.Types.FROM): 
                    break
                crlf_cou += 1
            if (t.isCharOf(":,(") or t.is_hiphen): 
                continue
            if (t.isChar('.') and t == end.next0_): 
                continue
            r = t.getReferent()
            if (r is not None): 
                if (r.type_name == "PHONE" or r.type_name == "URI" or r.type_name == "ADDRESS"): 
                    ty = r.getStringValue("SCHEME")
                    if (r.type_name == "URI"): 
                        if ((ty != "mailto" and ty != "skype" and ty != "ICQ") and ty != "http"): 
                            break
                    p._addContact(r)
                    end = t
                    crlf_cou = 0
                    continue
            if (isinstance(r, PersonIdentityReferent)): 
                p.addSlot(PersonReferent.ATTR_IDDOC, r, False, 0)
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
                        if (pr.findSlot(PersonPropertyReferent.ATTR_REF, r, True) is not None): 
                            exist = True
                            break
                    elif (s.type_name == PersonReferent.ATTR_ATTR and (isinstance(s.value, PersonAttrToken))): 
                        pr = Utils.asObjectOrNull(s.value, PersonAttrToken)
                        if (pr.referent.findSlot(PersonPropertyReferent.ATTR_REF, r, True) is not None): 
                            exist = True
                            break
                if (not exist): 
                    pat = PersonAttrToken(t, t)
                    pat.prop_ref = PersonPropertyReferent._new2258("сотрудник")
                    pat.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                    p.addSlot(PersonReferent.ATTR_ATTR, pat, False, 0)
                continue
            if (r is not None): 
                break
            if (not has_prefix or crlf_cou >= 2): 
                break
            rt = t.kit.processReferent("PERSON", t)
            if (rt is not None): 
                break
        if (ad is not None): 
            ad.overflow_level -= 1
        return ReferentToken._new2341(p, begin, end, morph_, p._m_person_identity_typ)
    
    @staticmethod
    def createNickname(pr : 'PersonReferent', t : 'Token') -> 'Token':
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
        first_pass3109 = True
        while True:
            if first_pass3109: first_pass3109 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_hiphen or t.is_comma or t.isCharOf(".:;")): 
                continue
            if (t.morph.class0_.is_preposition): 
                continue
            if (t.isChar('(')): 
                is_br = True
                continue
            if ((t.isValue("ПРОЗВИЩЕ", "ПРІЗВИСЬКО") or t.isValue("КЛИЧКА", None) or t.isValue("ПСЕВДОНИМ", "ПСЕВДОНІМ")) or t.isValue("ПСЕВДО", None) or t.isValue("ПОЗЫВНОЙ", "ПОЗИВНИЙ")): 
                has_keyw = True
                continue
            break
        if (not has_keyw or t is None): 
            return None
        if (BracketHelper.isBracket(t, True)): 
            br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                ni = MiscHelper.getTextValue(br.begin_token.next0_, br.end_token.previous, GetTextAttr.NO)
                if (ni is not None): 
                    pr.addSlot(PersonReferent.ATTR_NICKNAME, ni, False, 0)
                    t = br.end_token
                    tt = t.next0_
                    first_pass3110 = True
                    while True:
                        if first_pass3110: first_pass3110 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        if (tt.is_comma_and): 
                            continue
                        if (not BracketHelper.isBracket(tt, True)): 
                            break
                        br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                        if (br is None): 
                            break
                        ni = MiscHelper.getTextValue(br.begin_token.next0_, br.end_token.previous, GetTextAttr.NO)
                        if (ni is not None): 
                            pr.addSlot(PersonReferent.ATTR_NICKNAME, ni, False, 0)
                        tt = br.end_token
                        t = tt
                    if (is_br and t.next0_ is not None and t.next0_.isChar(')')): 
                        t = t.next0_
                    return t
        else: 
            pli = PersonItemToken.tryAttachList(t, None, PersonItemToken.ParseAttr.NO, 10)
            if (pli is not None and ((len(pli) == 1 or len(pli) == 2))): 
                ni = MiscHelper.getTextValue(pli[0].begin_token, pli[len(pli) - 1].end_token, GetTextAttr.NO)
                if (ni is not None): 
                    pr.addSlot(PersonReferent.ATTR_NICKNAME, ni, False, 0)
                    t = pli[len(pli) - 1].end_token
                    if (is_br and t.next0_ is not None and t.next0_.isChar(')')): 
                        t = t.next0_
                    return t
        return None
    
    @staticmethod
    def isPersonSayOrAttrAfter(t : 'Token') -> bool:
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        if (t is None): 
            return False
        tt = PersonHelper.__correctTailAttributes(None, t)
        if (tt is not None and tt != t): 
            return True
        if (t.is_comma and t.next0_ is not None): 
            t = t.next0_
        if (t.chars.is_latin_letter): 
            if (t.isValue("SAY", None) or t.isValue("ASK", None) or t.isValue("WHO", None)): 
                return True
        if (t.isChar('.') and (isinstance(t.next0_, TextToken)) and ((t.next0_.morph.class0_.is_pronoun or t.next0_.morph.class0_.is_personal_pronoun))): 
            if (t.next0_.morph.gender == MorphGender.FEMINIE or t.next0_.morph.gender == MorphGender.MASCULINE): 
                return True
        if (t.is_comma and t.next0_ is not None): 
            t = t.next0_
        if (PersonAttrToken.tryAttach(t, None, PersonAttrToken.PersonAttrAttachAttrs.NO) is not None): 
            return True
        return False
    
    @staticmethod
    def __correctTailAttributes(p : 'PersonReferent', t0 : 'Token') -> 'Token':
        from pullenti.ner.Referent import Referent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.ReferentToken import ReferentToken
        res = t0
        t = t0
        if (t is not None and t.isChar(',')): 
            t = t.next0_
        born = False
        die = False
        if (t is not None and ((t.isValue("РОДИТЬСЯ", "НАРОДИТИСЯ") or t.isValue("BORN", None)))): 
            t = t.next0_
            born = True
        elif (t is not None and ((t.isValue("УМЕРЕТЬ", "ПОМЕРТИ") or t.isValue("СКОНЧАТЬСЯ", None) or t.isValue("DIED", None)))): 
            t = t.next0_
            die = True
        elif ((t is not None and t.isValue("ДАТА", None) and t.next0_ is not None) and t.next0_.isValue("РОЖДЕНИЕ", "НАРОДЖЕННЯ")): 
            t = t.next0_.next0_
            born = True
        while t is not None:
            if (t.morph.class0_.is_preposition or t.is_hiphen or t.isChar(':')): 
                t = t.next0_
            else: 
                break
        if (t is not None and t.getReferent() is not None): 
            r = t.getReferent()
            if (r.type_name == "DATE"): 
                t1 = t
                if (t.next0_ is not None and ((t.next0_.isValue("Р", None) or t.next0_.isValue("РОЖДЕНИЕ", "НАРОДЖЕННЯ")))): 
                    born = True
                    t1 = t.next0_
                    if (t1.next0_ is not None and t1.next0_.isChar('.')): 
                        t1 = t1.next0_
                if (born): 
                    if (p is not None): 
                        p.addSlot(PersonReferent.ATTR_BORN, r, False, 0)
                    res = t1
                    t = t1
                elif (die): 
                    if (p is not None): 
                        p.addSlot(PersonReferent.ATTR_DIE, r, False, 0)
                    res = t1
                    t = t1
        if (die and t is not None): 
            ag = NumberHelper.tryParseAge(t.next0_)
            if (ag is not None): 
                if (p is not None): 
                    p.addSlot(PersonReferent.ATTR_AGE, str(ag.value), False, 0)
                t = ag.end_token.next0_
                res = ag.end_token
        if (t is None): 
            return res
        if (t.isChar('(')): 
            br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                t1 = t.next0_
                born = False
                if (t1.isValue("РОД", None)): 
                    born = True
                    t1 = t1.next0_
                    if (t1 is not None and t1.isChar('.')): 
                        t1 = t1.next0_
                if (isinstance(t1, ReferentToken)): 
                    r = t1.getReferent()
                    if (r.type_name == "DATERANGE" and t1.next0_ == br.end_token): 
                        bd = Utils.asObjectOrNull(r.getSlotValue("FROM"), Referent)
                        to = Utils.asObjectOrNull(r.getSlotValue("TO"), Referent)
                        if (bd is not None and to is not None): 
                            if (p is not None): 
                                p.addSlot(PersonReferent.ATTR_BORN, bd, False, 0)
                                p.addSlot(PersonReferent.ATTR_DIE, to, False, 0)
                            res = br.end_token
                            t = res
                    elif (r.type_name == "DATE" and t1.next0_ == br.end_token): 
                        if (p is not None): 
                            p.addSlot(PersonReferent.ATTR_BORN, r, False, 0)
                        res = br.end_token
                        t = res
        return res