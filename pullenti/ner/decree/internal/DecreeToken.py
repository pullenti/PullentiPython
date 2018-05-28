# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import datetime
import io
import typing
from enum import IntEnum
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.MetaToken import MetaToken

from pullenti.ner.decree.DecreeKind import DecreeKind
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.person.PersonPropertyKind import PersonPropertyKind
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender



class DecreeToken(MetaToken):
    """ Примитив, из которых состоит декрет """
    
    class ItemType(IntEnum):
        TYP = 0
        OWNER = 1
        DATE = 2
        EDITION = 3
        NUMBER = 4
        NAME = 5
        STDNAME = 6
        TERR = 7
        ORG = 8
        UNKNOWN = 9
        MISC = 10
        DECREEREF = 11
        DATERANGE = 12
        BETWEEN = 13
        READING = 14
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        self.typ = DecreeToken.ItemType.TYP
        self.value = None
        self.full_value = None
        self.ref = None
        self.children = None
        self.is_doubtful = False
        self.typ_kind = DecreeKind.UNDEFINED
        self.num_year = 0
        self.alias_token = None
        super().__init__(begin, end, None)
    
    @property
    def is_delo(self) -> bool:
        if (self.begin_token.is_value("ДЕЛО", "СПРАВА")): 
            return True
        if (self.begin_token.next0 is not None and self.begin_token.next0.is_value("ДЕЛО", "СПРАВА")): 
            return True
        return False
    
    def __str__(self) -> str:
        v = self.value
        if (v is None): 
            v = self.ref.referent.to_string(True, self.kit.base_language, 0)
        return "{0} {1} {2}".format(Utils.enumToString(self.typ), v, Utils.ifNotNull(self.full_value, ""))
    
    @staticmethod
    def try_attach(t : 'Token', prev : 'DecreeToken'=None, must_by_typ : bool=False) -> 'DecreeToken':
        """ Привязать с указанной позиции один примитив
        
        Args:
            cnt: 
            indFrom: 
        
        """
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.decree.internal.DecreeChangeToken import DecreeChangeToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        if (t is None): 
            return None
        if (t.is_value("НАЗВАННЫЙ", None)): 
            pass
        if (t.kit.is_recurce_overflow): 
            return None
        t.kit.recurse_level += 1
        res = DecreeToken.__try_attach(t, prev, 0, must_by_typ)
        t.kit.recurse_level -= 1
        if (res is None): 
            if (t.is_hiphen): 
                res = DecreeToken.__try_attach(t.next0, prev, 0, must_by_typ)
                if (res is not None and res.typ == DecreeToken.ItemType.NAME): 
                    res.begin_token = t
                    return res
            if (t.is_value("ПРОЕКТ", None)): 
                res = DecreeToken.__try_attach(t.next0, prev, 0, False)
                if (res is not None and res.typ == DecreeToken.ItemType.TYP and res.value is not None): 
                    if ("ЗАКОН" in res.value or not ((isinstance(res.end_token, TextToken)))): 
                        res.value = "ПРОЕКТ ЗАКОНА"
                    else: 
                        res.value = ("ПРОЕКТ " + (res.end_token if isinstance(res.end_token, TextToken) else None).term)
                    res.begin_token = t
                    return res
                elif (res is not None and res.typ == DecreeToken.ItemType.NUMBER): 
                    res1 = DecreeToken.__try_attach(res.end_token.next0, prev, 0, False)
                    if (res1 is not None and res1.typ == DecreeToken.ItemType.TYP and isinstance(res1.end_token, TextToken)): 
                        res = DecreeToken._new791(t, t, DecreeToken.ItemType.TYP)
                        res.value = ("ПРОЕКТ " + (res1.end_token if isinstance(res1.end_token, TextToken) else None).term)
                        return res
            if (t.is_value("ИНФОРМАЦИЯ", "ІНФОРМАЦІЯ") and (t.whitespaces_after_count < 3)): 
                dts = DecreeToken.try_attach_list(t.next0, None, 10, False)
                if (dts is None or (len(dts) < 2)): 
                    return None
                has_num = False
                has_own = False
                has_date = False
                has_name = False
                for dt in dts: 
                    if (dt.typ == DecreeToken.ItemType.NUMBER): 
                        has_num = True
                    elif (dt.typ == DecreeToken.ItemType.OWNER or dt.typ == DecreeToken.ItemType.ORG): 
                        has_own = True
                    elif (dt.typ == DecreeToken.ItemType.DATE): 
                        has_date = True
                    elif (dt.typ == DecreeToken.ItemType.NAME): 
                        has_name = True
                if (has_own and ((has_num or ((has_date and has_name))))): 
                    res = DecreeToken._new791(t, t, DecreeToken.ItemType.TYP)
                    res.value = "ИНФОРМАЦИЯ"
                    return res
            return None
        if (res.typ == DecreeToken.ItemType.DATE): 
            if (res.ref is None): 
                return None
            dre = (res.ref.referent if isinstance(res.ref.referent, DateReferent) else None)
            if (dre is None): 
                return None
        if (res.begin_token.begin_char > res.end_token.end_char): 
            pass
        if (res.typ == DecreeToken.ItemType.NUMBER): 
            tt = res.end_token.next0
            first_pass2631 = True
            while True:
                if first_pass2631: first_pass2631 = False
                else: tt = tt.next0
                if (not (tt is not None)): break
                if (not tt.is_comma_and or tt.is_newline_before): 
                    break
                tt = tt.next0
                if (not ((isinstance(tt, NumberToken)))): 
                    break
                if (tt.whitespaces_before_count > 2): 
                    break
                ddd = DecreeToken.__try_attach(tt, res, 0, False)
                if (ddd is not None): 
                    if (ddd.typ != DecreeToken.ItemType.NUMBER): 
                        break
                    if (res.children is None): 
                        res.children = list()
                    res.children.append(ddd)
                    res.end_token = ddd.end_token
                    continue
                if ((tt if isinstance(tt, NumberToken) else None).value > 1970): 
                    break
                if (tt.is_whitespace_after): 
                    pass
                elif (not tt.next0.is_char_of(",.")): 
                    pass
                else: 
                    break
                tmp = Utils.newStringIO(None)
                tee = DecreeToken.__try_attach_number(tt, tmp, True)
                if (res.children is None): 
                    res.children = list()
                add = DecreeToken._new793(tt, tee, DecreeToken.ItemType.NUMBER, Utils.toStringStringIO(tmp))
                res.children.append(add)
                tt = tee
                res.end_token = tt
        if (res.typ != DecreeToken.ItemType.TYP): 
            return res
        if (res.begin_token == res.end_token): 
            tok = DecreeToken.__m_termins.try_parse(res.begin_token.previous, TerminParseAttr.NO)
            if (tok is not None and isinstance(tok.termin.tag, DecreeToken.ItemType) and tok.end_token == res.end_token): 
                if (Utils.valToEnum(tok.termin.tag, DecreeToken.ItemType) == DecreeToken.ItemType.TYP): 
                    return None
        if (((prev is not None and prev.typ == DecreeToken.ItemType.TYP and prev.value is not None) and (("ДОГОВОР" in prev.value or "ДОГОВІР" in prev.value)) and res.value is not None) and not "ДОГОВОР" in res.value and not "ДОГОВІР" in res.value): 
            return None
        for e0 in DecreeToken.__m_empty_adjectives: 
            if (t.is_value(e0, None)): 
                res = DecreeToken.__try_attach(t.next0, prev, 0, False)
                if (res is None or res.typ != DecreeToken.ItemType.TYP): 
                    return None
                break
        if (res.value is not None and " " in res.value): 
            for s in DecreeToken.__m_all_typesru: 
                if (s in res.value and res.value != s): 
                    if (s == "КОДЕКС"): 
                        res.full_value = res.value
                        res.value = s
                        break
        if (res.value == "КОДЕКС" and res.full_value is None): 
            t1 = res.end_token
            tt = t1.next0
            while tt is not None: 
                if (tt.is_newline_before): 
                    break
                cha = DecreeChangeToken.try_attach(tt, None, False, None, False)
                if (cha is not None): 
                    break
                if (tt == t1.next0 and res.begin_token.previous is not None and res.begin_token.previous.is_value("НАСТОЯЩИЙ", "СПРАВЖНІЙ")): 
                    break
                if (not ((isinstance(tt, TextToken)))): 
                    break
                if (tt == t1.next0 and tt.is_value("ЗАКОН", None)): 
                    if (tt.next0 is not None and ((tt.next0.is_value("О", None) or tt.next0.is_value("ПРО", None)))): 
                        npt0 = NounPhraseHelper.try_parse(tt.next0.next0, NounPhraseParseAttr.NO, 0)
                        if (npt0 is None or not npt0.morph.case.is_prepositional): 
                            break
                        t1 = npt0.end_token
                        break
                ooo = False
                if (tt.morph.class0.is_preposition and tt.next0 is not None): 
                    if (tt.is_value("ПО", None)): 
                        tt = tt.next0
                    elif (tt.is_value("О", None) or tt.is_value("ОБ", None) or tt.is_value("ПРО", None)): 
                        ooo = True
                        tt = tt.next0
                npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0)
                if (npt is None): 
                    break
                if (tt == t1.next0 and npt.morph.case.is_genitive): 
                    tt = npt.end_token
                    t1 = tt
                elif (ooo and npt.morph.case.is_prepositional): 
                    tt = npt.end_token
                    t1 = tt
                    ttt = tt.next0
                    while ttt is not None: 
                        if (not ttt.is_comma_and): 
                            break
                        npt = NounPhraseHelper.try_parse(ttt.next0, NounPhraseParseAttr.NO, 0)
                        if (npt is None or not npt.morph.case.is_prepositional): 
                            break
                        tt = npt.end_token
                        t1 = tt
                        if (ttt.is_and): 
                            break
                        ttt = npt.end_token
                        ttt = ttt.next0
                else: 
                    break
                tt = tt.next0
            if (t1 != res.end_token): 
                res.end_token = t1
                res.full_value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
        if (res.value is not None and ((res.value.startswith("ВЕДОМОСТИ СЪЕЗДА") or res.value.startswith("ВІДОМОСТІ ЗЇЗДУ")))): 
            tt = res.end_token.next0
            if (tt is not None and isinstance(tt.get_referent(), GeoReferent)): 
                res.ref = (tt if isinstance(tt, ReferentToken) else None)
                res.end_token = tt
                tt = tt.next0
            if (tt is not None and tt.is_and): 
                tt = tt.next0
            if (tt is not None and isinstance(tt.get_referent(), OrganizationReferent)): 
                res.end_token = tt
                tt = tt.next0
        return res
    
    @staticmethod
    def __try_attach(t : 'Token', prev : 'DecreeToken', lev : int, must_by_typ : bool=False) -> 'DecreeToken':
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.denomination.DenominationReferent import DenominationReferent
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        if (t is None or lev > 4): 
            return None
        if (prev is not None and prev.typ == DecreeToken.ItemType.TYP): 
            while t.is_char_of(":-") and t.next0 is not None and not t.is_newline_after:
                t = t.next0
        if (prev is not None): 
            if (t.is_value("ПРИ", "ЗА") and t.next0 is not None): 
                t = t.next0
        if ((not must_by_typ and t.is_value("МЕЖДУ", "МІЖ") and isinstance(t.next0, ReferentToken)) and t.next0.next0 is not None): 
            t11 = t.next0.next0
            is_br = False
            if ((t11.is_char('(') and isinstance(t11.next0, TextToken) and t11.next0.next0 is not None) and t11.next0.next0.is_char(')')): 
                t11 = t11.next0.next0.next0
                is_br = True
            if (t11 is not None and t11.is_comma_and and isinstance(t11.next0, ReferentToken)): 
                rr = DecreeToken._new791(t, t11.next0, DecreeToken.ItemType.BETWEEN)
                rr.children = list()
                rr.children.append(DecreeToken._new795(t.next0, t.next0, DecreeToken.ItemType.OWNER, (t.next0 if isinstance(t.next0, ReferentToken) else None)))
                rr.children.append(DecreeToken._new795(t11.next0, t11.next0, DecreeToken.ItemType.OWNER, (t11.next0 if isinstance(t11.next0, ReferentToken) else None)))
                t = rr.end_token.next0
                first_pass2632 = True
                while True:
                    if first_pass2632: first_pass2632 = False
                    else: t = t.next0
                    if (not (t is not None)): break
                    if ((is_br and t.is_char('(') and isinstance(t.next0, TextToken)) and t.next0.next0 is not None and t.next0.next0.is_char(')')): 
                        t = t.next0.next0
                        rr.end_token = t
                        rr.children[len(rr.children) - 1].end_token = t
                        continue
                    if ((t.is_comma_and and t.next0 is not None and isinstance(t.next0, ReferentToken)) and not ((isinstance(t.next0.get_referent(), DateReferent)))): 
                        rr.children.append(DecreeToken._new795(t.next0, t.next0, DecreeToken.ItemType.OWNER, (t.next0 if isinstance(t.next0, ReferentToken) else None)))
                        rr.end_token = t.next0
                        t = rr.end_token
                        continue
                    break
                return rr
        r = t.get_referent()
        if (isinstance(r, OrganizationReferent)): 
            rt = (t if isinstance(t, ReferentToken) else None)
            org = (r if isinstance(r, OrganizationReferent) else None)
            res1 = None
            if (org.contains_profile(OrgProfile.MEDIA)): 
                tt1 = rt.begin_token
                if (BracketHelper.can_be_start_of_sequence(tt1, False, False)): 
                    tt1 = tt1.next0
                res1 = DecreeToken.__try_attach(tt1, prev, lev + 1, False)
                if (res1 is not None and res1.typ == DecreeToken.ItemType.TYP): 
                    res1.end_token = t
                    res1.begin_token = res1.end_token
                else: 
                    res1 = None
            if (res1 is None and org.contains_profile(OrgProfile.PRESS)): 
                res1 = DecreeToken._new791(t, t, DecreeToken.ItemType.TYP)
                res1.value = MiscHelper.get_text_value_of_meta_token((t if isinstance(t, ReferentToken) else None), GetTextAttr.NO)
            if (res1 is not None): 
                t11 = res1.end_token
                if (isinstance(t11.get_referent(), GeoReferent)): 
                    res1.ref = (t11 if isinstance(t11, ReferentToken) else None)
                elif (isinstance(t11, MetaToken)): 
                    t11 = (t11 if isinstance(t11, MetaToken) else None).end_token
                if (isinstance(t11.get_referent(), GeoReferent)): 
                    res1.ref = (t11 if isinstance(t11, ReferentToken) else None)
                elif (BracketHelper.is_bracket(t11, False) and isinstance(t11.previous.get_referent(), GeoReferent)): 
                    res1.ref = (t11.previous if isinstance(t11.previous, ReferentToken) else None)
                return res1
        if (r is not None and not must_by_typ): 
            if (isinstance(r, GeoReferent)): 
                return DecreeToken._new799(t, t, DecreeToken.ItemType.TERR, (t if isinstance(t, ReferentToken) else None), r.to_string(True, t.kit.base_language, 0))
            if (isinstance(r, DateReferent)): 
                if (prev is not None and prev.typ == DecreeToken.ItemType.TYP and prev.typ_kind == DecreeKind.STANDARD): 
                    ree = DecreeToken.try_attach((t if isinstance(t, ReferentToken) else None).begin_token, prev, False)
                    if ((ree is not None and ree.typ == DecreeToken.ItemType.NUMBER and ree.num_year > 0) and ((ree.end_token == (t if isinstance(t, ReferentToken) else None).end_token or ree.end_token.is_char('*')))): 
                        if (isinstance(t.next0, TextToken) and t.next0.is_char('*')): 
                            t = t.next0
                        ree.end_token = t
                        ree.begin_token = ree.end_token
                        return ree
                if (t.previous is not None and t.previous.morph.class0.is_preposition and t.previous.is_value("ДО", None)): 
                    return None
                return DecreeToken._new795(t, t, DecreeToken.ItemType.DATE, (t if isinstance(t, ReferentToken) else None))
            if (isinstance(r, OrganizationReferent)): 
                if ((t.next0 is not None and t.next0.is_value("В", "У") and t.next0.next0 is not None) and t.next0.next0.is_value("СОСТАВ", "СКЛАДІ")): 
                    return None
                return DecreeToken._new799(t, t, DecreeToken.ItemType.ORG, (t if isinstance(t, ReferentToken) else None), str(r))
            if (isinstance(r, PersonReferent)): 
                ok = False
                if (prev is not None and ((prev.typ == DecreeToken.ItemType.TYP or prev.typ == DecreeToken.ItemType.DATE))): 
                    ok = True
                elif (t.next0 is not None and isinstance(t.next0.get_referent(), DecreeReferent)): 
                    ok = True
                else: 
                    ne = DecreeToken.__try_attach(t.next0, None, lev + 1, False)
                    if (ne is not None and ((ne.typ == DecreeToken.ItemType.TYP or ne.typ == DecreeToken.ItemType.DATE or ne.typ == DecreeToken.ItemType.OWNER))): 
                        ok = True
                if (ok): 
                    prop = (r.get_value(PersonReferent.ATTR_ATTR) if isinstance(r.get_value(PersonReferent.ATTR_ATTR), PersonPropertyReferent) else None)
                    if (prop is not None and prop.kind == PersonPropertyKind.BOSS): 
                        return DecreeToken._new795(t, t, DecreeToken.ItemType.OWNER, ReferentToken(prop, t, t))
            if (isinstance(r, PersonPropertyReferent)): 
                return DecreeToken._new795(t, t, DecreeToken.ItemType.OWNER, ReferentToken(r, t, t))
            if (isinstance(r, DenominationReferent)): 
                s = str(r)
                if (len(s) > 1 and ((s[0] == 'A' or s[0] == 'А')) and s[1].isdigit()): 
                    return DecreeToken._new793(t, t, DecreeToken.ItemType.NUMBER, s)
            return None
        if (not must_by_typ): 
            tdat = None
            if (t.is_value("ОТ", "ВІД") or t.is_value("ПРИНЯТЬ", "ПРИЙНЯТИ")): 
                tdat = t.next0
            elif (t.is_value("ВВЕСТИ", None) or t.is_value("ВВОДИТЬ", "ВВОДИТИ")): 
                tdat = t.next0
                if (tdat is not None and tdat.is_value("В", "У")): 
                    tdat = tdat.next0
                if (tdat is not None and tdat.is_value("ДЕЙСТВИЕ", "ДІЯ")): 
                    tdat = tdat.next0
            if (tdat is not None): 
                if (tdat.next0 is not None and tdat.morph.class0.is_preposition): 
                    tdat = tdat.next0
                if (isinstance(tdat.get_referent(), DateReferent)): 
                    return DecreeToken._new795(t, tdat, DecreeToken.ItemType.DATE, (tdat if isinstance(tdat, ReferentToken) else None))
                dr = t.kit.process_referent("DATE", tdat)
                if (dr is not None): 
                    return DecreeToken._new795(t, dr.end_token, DecreeToken.ItemType.DATE, dr)
            if (t.is_value("НА", None) and t.next0 is not None and isinstance(t.next0.get_referent(), DateRangeReferent)): 
                return DecreeToken._new795(t, t.next0, DecreeToken.ItemType.DATERANGE, (t.next0 if isinstance(t.next0, ReferentToken) else None))
            if (t.is_char('(')): 
                tt = DecreeToken.__is_edition(t.next0)
                if (tt is not None): 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        return DecreeToken._new791(t, br.end_token, DecreeToken.ItemType.EDITION)
                if (t.next0 is not None and t.next0.is_value("ПРОЕКТ", None)): 
                    return DecreeToken._new793(t.next0, t.next0, DecreeToken.ItemType.TYP, "ПРОЕКТ")
                if ((t.next0 is not None and isinstance(t.next0.get_referent(), DateRangeReferent) and t.next0.next0 is not None) and t.next0.next0.is_char(')')): 
                    return DecreeToken._new795(t, t.next0.next0, DecreeToken.ItemType.DATERANGE, (t.next0 if isinstance(t.next0, ReferentToken) else None))
            else: 
                tt = DecreeToken.__is_edition(t)
                if (tt is not None): 
                    tt = tt.next0
                if (tt is not None): 
                    xxx = DecreeToken.try_attach(tt, None, False)
                    if (xxx is not None): 
                        return DecreeToken._new791(t, tt.previous, DecreeToken.ItemType.EDITION)
            if (isinstance(t, NumberToken)): 
                if (prev is not None and ((prev.typ == DecreeToken.ItemType.TYP or prev.typ == DecreeToken.ItemType.DATE))): 
                    tmp = Utils.newStringIO(None)
                    t11 = DecreeToken.__try_attach_number(t, tmp, False)
                    if (t11 is not None): 
                        ne = DecreeToken.__try_attach(t11.next0, None, lev + 1, False)
                        valnum = Utils.toStringStringIO(tmp)
                        if (ne is not None and ((ne.typ == DecreeToken.ItemType.DATE or ne.typ == DecreeToken.ItemType.OWNER or ne.typ == DecreeToken.ItemType.NAME))): 
                            return DecreeToken._new793(t, t11, DecreeToken.ItemType.NUMBER, valnum)
                        if (LanguageHelper.ends_with_ex(valnum, "ФЗ", "ФКЗ", None, None)): 
                            return DecreeToken._new793(t, t11, DecreeToken.ItemType.NUMBER, valnum)
                        year = 0
                        if (prev.typ == DecreeToken.ItemType.TYP): 
                            ok = False
                            if (prev.typ_kind == DecreeKind.STANDARD): 
                                ok = True
                                if (t11.next0 is not None and t11.next0.is_char('*')): 
                                    t11 = t11.next0
                                if (valnum.upper().endswith("(E)".upper())): 
                                    valnum = valnum[0 : (len(valnum) - 3)].strip()
                                for ii in range(len(valnum) - 1, -1, -1):
                                    if (not valnum[ii].isdigit()): 
                                        if (ii == len(valnum) or ii == 0): 
                                            break
                                        if (valnum[ii] != '-' and valnum[ii] != ':' and valnum[ii] != '.'): 
                                            break
                                        inoutarg814 = RefOutArgWrapper(None)
                                        Utils.tryParseInt(valnum[ii + 1 : ], inoutarg814)
                                        nn = inoutarg814.value
                                        if (nn > 50 and nn <= 99): 
                                            nn += 1900
                                        if (nn >= 1950 and nn <= datetime.datetime.now().year): 
                                            year = nn
                                            valnum = valnum[0 : (ii)]
                                        break
                                valnum = valnum.replace('-', '.')
                                if (year < 1): 
                                    if (t11.next0 is not None and t11.next0.is_hiphen): 
                                        if (isinstance(t11.next0.next0, NumberToken)): 
                                            nn = (t11.next0.next0 if isinstance(t11.next0.next0, NumberToken) else None).value
                                            if (nn > 50 and nn <= 99): 
                                                nn += 1900
                                            if (nn >= 1950 and nn <= datetime.datetime.now().year): 
                                                year = nn
                                                t11 = t11.next0.next0
                            elif (prev.begin_token == prev.end_token and prev.begin_token.chars.is_all_upper and ((prev.begin_token.is_value("ФЗ", None) or prev.begin_token.is_value("ФКЗ", None)))): 
                                ok = True
                            if (ok): 
                                return DecreeToken._new815(t, t11, DecreeToken.ItemType.NUMBER, valnum, year)
                    val = (t if isinstance(t, NumberToken) else None).value
                    if (val > 1910 and (val < 2030)): 
                        return DecreeToken._new793(t, t, DecreeToken.ItemType.DATE, str(val))
                rt = t.kit.process_referent("PERSON", t)
                if (rt is not None): 
                    pr = (rt.referent if isinstance(rt.referent, PersonPropertyReferent) else None)
                    if (pr is not None): 
                        return DecreeToken._new817(rt.begin_token, rt.end_token, DecreeToken.ItemType.OWNER, rt, rt.morph)
                if (t.next0 is not None and t.next0.chars.is_letter): 
                    res1 = DecreeToken.__try_attach(t.next0, prev, lev + 1, False)
                    if (res1 is not None and res1.typ == DecreeToken.ItemType.OWNER): 
                        res1.begin_token = t
                        return res1
        if (not ((isinstance(t, TextToken)))): 
            return None
        toks = DecreeToken.__m_termins.try_parse_all(t, TerminParseAttr.NO)
        if (toks is not None): 
            for tok in toks: 
                if (tok.end_token.is_char('.') and tok.begin_token != tok.end_token): 
                    tok.end_token = tok.end_token.previous
                if (tok.termin.canonic_text == "РЕГИСТРАЦИЯ" or tok.termin.canonic_text == "РЕЄСТРАЦІЯ"): 
                    if (tok.end_token.next0 is not None and ((tok.end_token.next0.is_value("В", None) or tok.end_token.next0.is_value("ПО", None)))): 
                        tok.end_token = tok.end_token.next0
                doubt = False
                if ((tok.end_char - tok.begin_char) < 3): 
                    doubt = True
                    if (tok.end_token.next0 is None or not tok.chars.is_all_upper): 
                        pass
                    else: 
                        r = tok.end_token.next0.get_referent()
                        if (isinstance(r, GeoReferent)): 
                            doubt = False
                if (tok.begin_token == tok.end_token and (tok.length_char < 4) and len(toks) > 1): 
                    cou = 0
                    tt = t.previous
                    first_pass2633 = True
                    while True:
                        if first_pass2633: first_pass2633 = False
                        else: tt = tt.previous; cou += 1
                        if (not (tt is not None and (cou < 500))): break
                        dr = (tt.get_referent() if isinstance(tt.get_referent(), DecreeReferent) else None)
                        if (dr is None): 
                            continue
                        for tok1 in toks: 
                            if (dr.find_slot(DecreeReferent.ATTR_NAME, tok1.termin.canonic_text, True) is not None): 
                                return DecreeToken._new818(tok.begin_token, tok.end_token, Utils.valToEnum(tok1.termin.tag, DecreeToken.ItemType), tok1.termin.canonic_text, tok1.morph)
                    if (tok.begin_token.is_value("ТК", None) and tok.termin.canonic_text.startswith("ТРУД")): 
                        has_tamoz = False
                        cou = 0
                        tt = t.previous
                        while tt is not None and (cou < 500): 
                            if (tt.is_value("ТАМОЖНЯ", None) or tt.is_value("ТАМОЖЕННЫЙ", None) or tt.is_value("ГРАНИЦА", None)): 
                                has_tamoz = True
                                break
                            tt = tt.previous; cou += 1
                        if (has_tamoz): 
                            continue
                        cou = 0
                        tt = t.next0
                        while tt is not None and (cou < 500): 
                            if (tt.is_value("ТАМОЖНЯ", None) or tt.is_value("ТАМОЖЕННЫЙ", None) or tt.is_value("ГРАНИЦА", None)): 
                                has_tamoz = True
                                break
                            tt = tt.next0; cou += 1
                        if (has_tamoz): 
                            continue
                if (doubt and tok.chars.is_all_upper): 
                    if (PartToken.is_part_before(tok.begin_token)): 
                        doubt = False
                    elif (tok.get_source_text().endswith("ТС")): 
                        doubt = False
                res = DecreeToken._new819(tok.begin_token, tok.end_token, Utils.valToEnum(tok.termin.tag, DecreeToken.ItemType), tok.termin.canonic_text, tok.morph, doubt)
                if (isinstance(tok.termin.tag2, DecreeKind)): 
                    res.typ_kind = Utils.valToEnum(tok.termin.tag2, DecreeKind)
                if (res.value == "ГОСТ" and tok.end_token.next0 is not None): 
                    if (tok.end_token.next0.is_value("Р", None) or tok.end_token.next0.is_value("P", None)): 
                        res.end_token = tok.end_token.next0
                    else: 
                        g = (tok.end_token.next0.get_referent() if isinstance(tok.end_token.next0.get_referent(), GeoReferent) else None)
                        if (g is not None and ((g.alpha2 == "RU" or g.alpha2 == "SU"))): 
                            res.end_token = tok.end_token.next0
                if (isinstance(tok.termin.tag2, str) and res.typ == DecreeToken.ItemType.TYP): 
                    res.full_value = tok.termin.canonic_text
                    res.value = (tok.termin.tag2 if isinstance(tok.termin.tag2, str) else None)
                    res.is_doubtful = False
                if (res.typ_kind == DecreeKind.STANDARD): 
                    cou = 0
                    tt = res.end_token.next0
                    first_pass2634 = True
                    while True:
                        if first_pass2634: first_pass2634 = False
                        else: tt = tt.next0; cou += 1
                        if (not (tt is not None and (cou < 3))): break
                        if (tt.whitespaces_before_count > 2): 
                            break
                        tok2 = DecreeToken.__m_termins.try_parse(tt, TerminParseAttr.NO)
                        if (tok2 is not None): 
                            if (isinstance(tok2.termin.tag2, DecreeKind) and Utils.valToEnum(tok2.termin.tag2, DecreeKind) == DecreeKind.STANDARD): 
                                res.end_token = tok2.end_token
                                tt = res.end_token
                                res.is_doubtful = False
                                if (res.value == "СТАНДАРТ"): 
                                    res.value = tok2.termin.canonic_text
                                continue
                        if (isinstance(tt, TextToken) and (tt.length_char < 4) and tt.chars.is_all_upper): 
                            res.end_token = tt
                            continue
                        if (tt.is_char_of("/\\") and isinstance(tt.next0, TextToken) and tt.next0.chars.is_all_upper): 
                            tt = tt.next0
                            res.end_token = tt
                            continue
                        break
                    if (res.value == "СТАНДАРТ"): 
                        res.is_doubtful = True
                    if (res.is_doubtful and not res.is_newline_after): 
                        num1 = DecreeToken.try_attach(res.end_token.next0, res, False)
                        if (num1 is not None and num1.typ == DecreeToken.ItemType.NUMBER): 
                            if (num1.num_year > 0): 
                                res.is_doubtful = False
                    if (res.value == "СТАНДАРТ" and res.is_doubtful): 
                        return None
                return res
        if (((t.morph.class0.is_adjective and ((t.is_value("УКАЗАННЫЙ", "ЗАЗНАЧЕНИЙ") or t.is_value("ВЫШЕУКАЗАННЫЙ", "ВИЩЕВКАЗАНИЙ") or t.is_value("НАЗВАННЫЙ", "НАЗВАНИЙ"))))) or ((t.morph.class0.is_pronoun and (((t.is_value("ЭТОТ", "ЦЕЙ") or t.is_value("ТОТ", "ТОЙ") or t.is_value("ДАННЫЙ", "ДАНИЙ")) or t.is_value("САМЫЙ", "САМИЙ")))))): 
            t11 = t.next0
            if (t11 is not None and t11.is_value("ЖЕ", None)): 
                t11 = t11.next0
            tok = DecreeToken.__m_termins.try_parse(t11, TerminParseAttr.NO)
            if ((tok) is not None): 
                if (((tok.morph.number & MorphNumber.PLURAL)) == MorphNumber.UNDEFINED): 
                    npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
                    if (npt is not None and ((npt.morph.number & MorphNumber.PLURAL)) != MorphNumber.UNDEFINED): 
                        pass
                    else: 
                        te = DecreeToken._find_back_typ(t.previous, tok.termin.canonic_text)
                        if (te is not None): 
                            return DecreeToken._new795(t, tok.end_token, DecreeToken.ItemType.DECREEREF, te)
        if (t.morph.class0.is_adjective and t.is_value("НАСТОЯЩИЙ", "СПРАВЖНІЙ")): 
            tok = DecreeToken.__m_termins.try_parse(t.next0, TerminParseAttr.NO)
            if ((tok) is not None): 
                return DecreeToken._new795(t, tok.end_token, DecreeToken.ItemType.DECREEREF, None)
        if (must_by_typ): 
            return None
        if (t.morph.class0.is_adjective): 
            dt = DecreeToken.__try_attach(t.next0, prev, lev + 1, False)
            if (dt is not None and dt.ref is None): 
                rt = t.kit.process_referent("GEO", t)
                if (rt is not None): 
                    dt.ref = rt
                    dt.begin_token = t
                    return dt
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.internal_noun is not None): 
                npt = None
            if ((npt is not None and dt is not None and dt.typ == DecreeToken.ItemType.TYP) and dt.value == "КОДЕКС"): 
                dt.value = npt.get_normal_case_text(MorphClass(), True, MorphGender.UNDEFINED, False)
                dt.begin_token = t
                dt.is_doubtful = True
                return dt
            try_npt = False
            if (not t.chars.is_all_lower): 
                try_npt = True
            else: 
                for a in DecreeToken.__m_std_adjectives: 
                    if (t.is_value(a, None)): 
                        try_npt = True
                        break
            if (try_npt): 
                if (npt is not None): 
                    if (npt.end_token.is_value("ГАЗЕТА", None) or npt.end_token.is_value("БЮЛЛЕТЕНЬ", "БЮЛЕТЕНЬ")): 
                        return DecreeToken._new818(t, npt.end_token, DecreeToken.ItemType.TYP, npt.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False), npt.morph)
                    if (len(npt.adjectives) > 0 and npt.end_token.get_morph_class_in_dictionary().is_noun): 
                        tok = DecreeToken.__m_termins.try_parse(npt.end_token, TerminParseAttr.NO)
                        if ((tok) is not None): 
                            if (npt.begin_token.is_value("ОБЩИЙ", "ЗАГАЛЬНИЙ")): 
                                return None
                            return DecreeToken._new823(npt.begin_token, tok.end_token, npt.get_normal_case_text(MorphClass(), True, MorphGender.UNDEFINED, False), npt.morph)
                    if (prev is not None and prev.typ == DecreeToken.ItemType.TYP): 
                        if (npt.end_token.is_value("КОЛЛЕГИЯ", "КОЛЕГІЯ")): 
                            res1 = DecreeToken._new818(t, npt.end_token, DecreeToken.ItemType.OWNER, npt.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False), npt.morph)
                            t = npt.end_token.next0
                            first_pass2635 = True
                            while True:
                                if first_pass2635: first_pass2635 = False
                                else: t = t.next0
                                if (not (t is not None)): break
                                if (t.is_and or t.morph.class0.is_preposition): 
                                    continue
                                re = t.get_referent()
                                if (isinstance(re, GeoReferent) or isinstance(re, OrganizationReferent)): 
                                    res1.end_token = t
                                    continue
                                elif (re is not None): 
                                    break
                                dt1 = DecreeToken.__try_attach(t, res1, lev + 1, False)
                                if (dt1 is not None and dt1.typ != DecreeToken.ItemType.UNKNOWN): 
                                    if (dt1.typ != DecreeToken.ItemType.OWNER): 
                                        break
                                    res1.end_token = dt1.end_token
                                    t = res1.end_token
                                    continue
                                npt1 = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
                                if (npt1 is None): 
                                    break
                                res1.end_token = npt1.end_token
                                t = res1.end_token
                            if (res1.end_token != npt.end_token): 
                                res1.value = "{0} {1}".format(res1.value, MiscHelper.get_text_value(npt.end_token.next0, res1.end_token, GetTextAttr.KEEPQUOTES))
                            return res1
        t1 = None
        t0 = t
        num = False
        t1 = MiscHelper.check_number_prefix(t)
        if ((t1) is not None): 
            num = True
        elif (DecreeToken.__is_jus_number(t)): 
            t1 = t
        if (t1 is not None): 
            if ((t1.whitespaces_before_count < 15) and ((not t1.is_newline_before or isinstance(t1, NumberToken) or DecreeToken.__is_jus_number(t1)))): 
                tmp = Utils.newStringIO(None)
                t11 = DecreeToken.__try_attach_number(t1, tmp, num)
                if (t11 is not None): 
                    if (t11.next0 is not None and t11.next0.is_value("ДСП", None)): 
                        t11 = t11.next0
                        print("ДСП", end="", file=tmp)
                    return DecreeToken._new793(t0, t11, DecreeToken.ItemType.NUMBER, Utils.toStringStringIO(tmp))
            if (t1.is_newline_before and num): 
                return DecreeToken._new791(t0, t1.previous, DecreeToken.ItemType.NUMBER)
        if (BracketHelper.can_be_start_of_sequence(t, False, False)): 
            if (BracketHelper.can_be_start_of_sequence(t, True, False) and ((((t.next0.is_value("О", None) or t.next0.is_value("ОБ", None) or t.next0.is_value("ПРО", None)) or t.next0.is_value("ПО", None) or t.chars.is_capital_upper) or ((prev is not None and isinstance(t.next0, TextToken) and ((prev.typ == DecreeToken.ItemType.DATE or prev.typ == DecreeToken.ItemType.NUMBER))))))): 
                br = BracketHelper.try_parse(t, BracketParseAttr.CANCONTAINSVERBS, 200)
                if (br is not None): 
                    tt = br.end_token
                    if (tt.previous is not None and tt.previous.is_char('>')): 
                        tt = tt.previous
                    if ((tt.is_char('>') and isinstance(tt.previous, NumberToken) and tt.previous.previous is not None) and tt.previous.previous.is_char('<')): 
                        tt = tt.previous.previous.previous
                        if (tt is None or tt.begin_char <= br.begin_char): 
                            return None
                        br.end_token = tt
                    tt1 = DecreeToken._try_attach_std_change_name(t.next0)
                    if (tt1 is not None and tt1.end_char > br.end_char): 
                        br.end_token = tt1
                    else: 
                        tt = br.begin_token.next0
                        while tt is not None and (tt.end_char < br.end_char): 
                            if (tt.is_char('(')): 
                                dt = DecreeToken.try_attach(tt.next0, None, False)
                                if (dt is None and BracketHelper.can_be_start_of_sequence(tt.next0, True, False)): 
                                    dt = DecreeToken.try_attach(tt.next0.next0, None, False)
                                if (dt is not None and dt.typ == DecreeToken.ItemType.TYP): 
                                    if (DecreeToken.get_kind(dt.value) == DecreeKind.PUBLISHER): 
                                        br.end_token = tt.previous
                                        break
                            tt = tt.next0
                    return DecreeToken._new793(br.begin_token, br.end_token, DecreeToken.ItemType.NAME, MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO))
                else: 
                    tt1 = DecreeToken._try_attach_std_change_name(t.next0)
                    if (tt1 is not None): 
                        return DecreeToken._new793(t, tt1, DecreeToken.ItemType.NAME, MiscHelper.get_text_value(t, tt1, GetTextAttr.NO))
            elif (t.is_char('(')): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    if (not t.next0.is_value("ДАЛЕЕ", "ДАЛІ")): 
                        if ((br.end_char - br.begin_char) < 30): 
                            return DecreeToken._new793(br.begin_token, br.end_token, DecreeToken.ItemType.MISC, MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO))
        if (t.inner_bool): 
            rt = t.kit.process_referent("PERSON", t)
            if (rt is not None): 
                pr = (rt.referent if isinstance(rt.referent, PersonPropertyReferent) else None)
                if (pr is None): 
                    return None
                if (pr.kind != PersonPropertyKind.UNDEFINED): 
                    pass
                elif (pr.name.upper().startswith("ГРАЖДАН".upper()) or pr.name.upper().startswith("ГРОМАДЯН".upper())): 
                    return None
                return DecreeToken._new817(rt.begin_token, rt.end_token, DecreeToken.ItemType.OWNER, rt, rt.morph)
        if (t.is_value("О", None) or t.is_value("ОБ", None) or t.is_value("ПРО", None)): 
            et = None
            if ((t.next0 is not None and t.next0.is_value("ВНЕСЕНИЕ", "ВНЕСЕННЯ") and t.next0.next0 is not None) and t.next0.next0.is_value("ИЗМЕНЕНИЕ", "ЗМІНА")): 
                et = t.next0
            elif (t.next0 is not None and t.next0.is_value("ПОПРАВКА", None)): 
                et = t.next0
            elif (t.next0 is not None and isinstance(t.next0.get_referent(), OrganizationReferent)): 
                et = t.next0
            if (et is not None and et.next0 is not None and et.next0.morph.class0.is_preposition): 
                et = et.next0
            if (et is not None and et.next0 is not None): 
                dts2 = DecreeToken.try_attach_list(et.next0, None, 10, False)
                if (dts2 is not None and dts2[0].typ == DecreeToken.ItemType.TYP): 
                    et = dts2[0].end_token
                    if (len(dts2) > 1 and dts2[1].typ == DecreeToken.ItemType.TERR): 
                        et = dts2[1].end_token
                    return DecreeToken._new793(t, et, DecreeToken.ItemType.NAME, MiscHelper.get_text_value(t, et, GetTextAttr.NO))
                if (et.next0.is_char_of(",(")): 
                    return DecreeToken._new793(t, et, DecreeToken.ItemType.NAME, MiscHelper.get_text_value(t, et, GetTextAttr.NO))
            elif (et is not None): 
                return DecreeToken._new793(t, et, DecreeToken.ItemType.NAME, MiscHelper.get_text_value(t, et, GetTextAttr.NO))
            return None
        if (t.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
            return None
        if (prev is not None and prev.typ == DecreeToken.ItemType.TYP): 
            if (t.is_value("ПРАВИТЕЛЬСТВО", "УРЯД") or t.is_value("ПРЕЗИДЕНТ", None)): 
                return DecreeToken._new834(t, t, DecreeToken.ItemType.OWNER, t.morph, t.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False))
        if ((((t.chars.is_cyrillic_letter and ((not t.chars.is_all_lower or ((prev is not None and prev.typ == DecreeToken.ItemType.UNKNOWN))))) or t.is_value("ЗАСЕДАНИЕ", "ЗАСІДАННЯ") or t.is_value("СОБРАНИЕ", "ЗБОРИ")) or t.is_value("ПЛЕНУМ", None) or t.is_value("КОЛЛЕГИЯ", "КОЛЕГІЯ")) or t.is_value("АДМИНИСТРАЦИЯ", "АДМІНІСТРАЦІЯ")): 
            ok = False
            if (prev is not None and ((prev.typ == DecreeToken.ItemType.TYP or prev.typ == DecreeToken.ItemType.OWNER or prev.typ == DecreeToken.ItemType.ORG))): 
                ok = True
            elif (prev is not None and prev.typ == DecreeToken.ItemType.UNKNOWN and not t.morph.class0.is_verb): 
                ok = True
            elif (t.next0 is not None and isinstance(t.next0.get_referent(), GeoReferent) and not t.is_value("ИМЕНЕМ", None)): 
                ok = True
            elif ((t.previous is not None and t.previous.is_char(',') and t.previous.previous is not None) and isinstance(t.previous.previous.get_referent(), DecreeReferent)): 
                ok = True
            if (ok): 
                if (PartToken.try_attach(t, None, False, False) is not None): 
                    ok = False
            if (ok): 
                t1 = t
                ty = DecreeToken.ItemType.UNKNOWN
                tmp = Utils.newStringIO(None)
                tt = t
                while tt is not None: 
                    if (not ((isinstance(tt, TextToken)))): 
                        org = (tt.get_referent() if isinstance(tt.get_referent(), OrganizationReferent) else None)
                        if (org is not None and tt.previous == t1): 
                            ty = DecreeToken.ItemType.OWNER
                            if (tmp.tell() > 0): 
                                print(' ', end="", file=tmp)
                            print(tt.get_source_text().upper(), end="", file=tmp)
                            t1 = tt
                            break
                        break
                    if (tt.is_newline_before and tt != t1): 
                        break
                    if (not tt.chars.is_cyrillic_letter): 
                        break
                    if (tt != t): 
                        if (DecreeToken.__try_attach(tt, None, lev + 1, False) is not None): 
                            break
                    npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0)
                    if (tt.chars.is_all_lower and tt != t): 
                        if (npt is not None and npt.morph.case.is_genitive): 
                            pass
                        else: 
                            break
                    if (npt is not None): 
                        if (tmp.tell() > 0): 
                            print(" {0}".format(npt.get_source_text()), end="", file=tmp, flush=True)
                        else: 
                            print(npt.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False), end="", file=tmp)
                        tt = npt.end_token
                        t1 = tt
                    elif (tmp.tell() > 0): 
                        print(" {0}".format(tt.get_source_text()), end="", file=tmp, flush=True)
                        t1 = tt
                    else: 
                        s = None
                        if (tt == t): 
                            s = tt.get_normal_case_text(MorphClass.NOUN, False, MorphGender.UNDEFINED, False)
                        if (s is None): 
                            s = (tt if isinstance(tt, TextToken) else None).term
                        print(s, end="", file=tmp)
                        t1 = tt
                    tt = tt.next0
                ss = MiscHelper.convert_first_char_upper_and_other_lower(Utils.toStringStringIO(tmp))
                return DecreeToken._new793(t, t1, ty, ss)
        if (t.is_value("ДАТА", None)): 
            t1 = t.next0
            if (t1 is not None and t1.morph.case.is_genitive): 
                t1 = t1.next0
            if (t1 is not None and t1.is_char(':')): 
                t1 = t1.next0
            res1 = DecreeToken.__try_attach(t1, prev, lev + 1, False)
            if (res1 is not None and res1.typ == DecreeToken.ItemType.DATE): 
                res1.begin_token = t
                return res1
        if (t.is_value("ВЕСТНИК", "ВІСНИК") or t.is_value("БЮЛЛЕТЕНЬ", "БЮЛЕТЕНЬ")): 
            npt = NounPhraseHelper.try_parse(t.next0, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                return DecreeToken._new793(t, npt.end_token, DecreeToken.ItemType.TYP, MiscHelper.get_text_value(t, npt.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE))
            elif (t.next0 is not None and isinstance(t.next0.get_referent(), OrganizationReferent)): 
                return DecreeToken._new793(t, t.next0, DecreeToken.ItemType.TYP, MiscHelper.get_text_value(t, t.next0, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE))
        if ((prev is not None and prev.typ == DecreeToken.ItemType.TYP and prev.value is not None) and (("ДОГОВОР" in prev.value or "ДОГОВІР" in prev.value))): 
            nn = DecreeToken.try_attach_name(t, prev.value, False, False)
            if (nn is not None): 
                return nn
            t1 = None
            ttt = t
            first_pass2636 = True
            while True:
                if first_pass2636: first_pass2636 = False
                else: ttt = ttt.next0
                if (not (ttt is not None)): break
                if (ttt.is_newline_before): 
                    break
                ddt1 = DecreeToken.__try_attach(ttt, None, lev + 1, False)
                if (ddt1 is not None): 
                    break
                if (ttt.morph.class0.is_preposition or ttt.morph.class0.is_conjunction): 
                    continue
                npt = NounPhraseHelper.try_parse(ttt, NounPhraseParseAttr.NO, 0)
                if (npt is None): 
                    break
                t1 = npt.end_token
                ttt = t1
            if (t1 is not None): 
                nn = DecreeToken._new791(t, t1, DecreeToken.ItemType.NAME)
                nn.value = MiscHelper.get_text_value(t, t1, GetTextAttr.NO)
                return nn
        return None
    
    @staticmethod
    def __is_jus_number(t : 'Token') -> bool:
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None): 
            return False
        if (tt.term != "A" and tt.term != "А"): 
            return False
        if (isinstance(t.next0, NumberToken) and (t.whitespaces_after_count < 2)): 
            if ((t.next0 if isinstance(t.next0, NumberToken) else None).value > 20): 
                return True
            return False
        return False
    
    @staticmethod
    def __is_edition(t : 'Token') -> 'Token':
        from pullenti.ner.NumberToken import NumberToken
        if (t is None): 
            return None
        if (t.morph.class0.is_preposition and t.next0 is not None): 
            t = t.next0
        if (t.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ") or t.is_value("РЕД", None)): 
            if (t.next0 is not None and t.next0.is_char('.')): 
                return t.next0
            else: 
                return t
        if (t.is_value("ИЗМЕНЕНИЕ", "ЗМІНА")): 
            if ((t.next0 is not None and t.next0.is_comma and t.next0.next0 is not None) and t.next0.next0.is_value("ВНЕСЕННЫЙ", "ВНЕСЕНИЙ")): 
                return t.next0.next0
            return t
        if (isinstance(t, NumberToken) and t.next0 is not None and t.next0.is_value("ЧТЕНИЕ", "ЧИТАННЯ")): 
            return t.next0.next0
        return None
    
    @staticmethod
    def _find_back_typ(t : 'Token', type_name : str) -> 'ReferentToken':
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (t is None): 
            return None
        if (t.is_value("НАСТОЯЩИЙ", "СПРАВЖНІЙ")): 
            return None
        cou = 0
        tt = t
        first_pass2637 = True
        while True:
            if first_pass2637: first_pass2637 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            cou += 1
            if (tt.is_newline_before): 
                cou += 10
            if (cou > 500): 
                break
            d = (tt.get_referent() if isinstance(tt.get_referent(), DecreeReferent) else None)
            if (d is None and isinstance(tt.get_referent(), DecreePartReferent)): 
                d = (tt.get_referent() if isinstance(tt.get_referent(), DecreePartReferent) else None).owner
            if (d is None): 
                continue
            if (d.typ0 == type_name or d.typ == type_name): 
                return (tt if isinstance(tt, ReferentToken) else None)
        return None
    
    @staticmethod
    def __try_attach_number(t : 'Token', tmp : io.StringIO, after_num : bool) -> 'Token':
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.denomination.DenominationReferent import DenominationReferent
        from pullenti.ner.ReferentToken import ReferentToken
        t2 = t
        res = None
        digs = False
        br = False
        first_pass2638 = True
        while True:
            if first_pass2638: first_pass2638 = False
            else: t2 = t2.next0
            if (not (t2 is not None)): break
            if (t2.is_char_of("(),;")): 
                break
            if (t2.is_table_control_char): 
                break
            if (t2.is_char('.') and t2.is_whitespace_after): 
                break
            if (t2 != t and t2.whitespaces_before_count > 1): 
                break
            if (BracketHelper.is_bracket(t2, False)): 
                if (not after_num): 
                    break
                if (not br and t2 != t): 
                    break
                res = t2
                if (br): 
                    break
                br = True
                continue
            if (not ((isinstance(t2, NumberToken))) and not ((isinstance(t2, TextToken)))): 
                dr = (t2.get_referent() if isinstance(t2.get_referent(), DateReferent) else None)
                if (dr is not None and ((t2 == t or not t2.is_whitespace_before))): 
                    if (dr.year > 0 and t2.length_char == 4): 
                        res = t2
                        print(dr.year, end="", file=tmp)
                        digs = True
                        continue
                den = (t2.get_referent() if isinstance(t2.get_referent(), DenominationReferent) else None)
                if (den is not None): 
                    res = t2
                    print(t2.get_source_text().upper(), end="", file=tmp)
                    for c in den.value: 
                        if (c.isdigit()): 
                            digs = True
                    if (t2.is_whitespace_after): 
                        break
                    continue
                break
            s = t2.get_source_text()
            if (s is None): 
                break
            if (t2.is_hiphen): 
                s = "-"
            if (t2.is_value("ОТ", "ВІД")): 
                break
            if (s == "\\"): 
                s = "/"
            if (s[0].isdigit()): 
                for d in s: 
                    digs = True
            if (not t2.is_char_of("_@")): 
                print(s, end="", file=tmp)
            res = t2
            if (t2.is_whitespace_after): 
                if (t2.whitespaces_after_count > 1): 
                    break
                if (digs): 
                    if ((t2.next0 is not None and ((t2.next0.is_hiphen or t2.next0.is_char_of(".:"))) and not t2.next0.is_whitespace_after) and isinstance(t2.next0.next0, NumberToken)): 
                        continue
                if (not after_num): 
                    break
                if (t2.is_hiphen): 
                    if (t2.next0 is not None and t2.next0.is_value("СМ", None)): 
                        break
                    continue
                if (t2.is_char('/')): 
                    continue
                if (t2.next0 is not None): 
                    if (((t2.next0.is_hiphen or isinstance(t2.next0, NumberToken))) and not digs): 
                        continue
                if (t2 == t and t2.chars.is_all_upper): 
                    continue
                if (isinstance(t2.next0, NumberToken)): 
                    if (isinstance(t2, NumberToken)): 
                        print(" ", end="", file=tmp)
                    continue
                break
        if (tmp.tell() == 0): 
            if (t is not None and t.is_char('_')): 
                t2 = t
                while t2 is not None: 
                    if (not t2.is_char('_') or ((t2 != t and t2.is_whitespace_before))): 
                        print('?', end="", file=tmp)
                        return t2.previous
                    t2 = t2.next0
            return None
        if (not digs and not after_num): 
            return None
        ch = Utils.getCharAtStringIO(tmp, tmp.tell() - 1)
        if (not ch.isalnum() and isinstance(res, TextToken) and not res.is_char('_')): 
            Utils.setLengthStringIO(tmp, tmp.tell() - 1)
            res = res.previous
        if (res.next0 is not None and res.next0.is_hiphen and isinstance(res.next0.next0, NumberToken)): 
            inoutarg839 = RefOutArgWrapper(None)
            inoutres840 = Utils.tryParseInt(Utils.toStringStringIO(tmp), inoutarg839)
            min0 = inoutarg839.value
            if (inoutres840): 
                if (min0 < (res.next0.next0 if isinstance(res.next0.next0, NumberToken) else None).value): 
                    res = res.next0.next0
                    print("-{0}".format((res if isinstance(res, NumberToken) else None).value), end="", file=tmp, flush=True)
        if (res.next0 is not None and not res.is_whitespace_after and res.next0.is_char('(')): 
            cou = 0
            tmp2 = Utils.newStringIO(None)
            tt = res.next0.next0
            while tt is not None: 
                if (tt.is_char(')')): 
                    print("({0})".format(Utils.toStringStringIO(tmp2)), end="", file=tmp, flush=True)
                    res = tt
                    break
                cou += 1
                if ((cou) > 5): 
                    break
                if (tt.is_whitespace_before or tt.is_whitespace_after): 
                    break
                if (isinstance(tt, ReferentToken)): 
                    break
                print(tt.get_source_text(), end="", file=tmp2)
                tt = tt.next0
        if (tmp.tell() > 2): 
            if (Utils.getCharAtStringIO(tmp, tmp.tell() - 1) == '3'): 
                if (Utils.getCharAtStringIO(tmp, tmp.tell() - 2) == 'К' or Utils.getCharAtStringIO(tmp, tmp.tell() - 2) == 'Ф'): 
                    Utils.setCharAtStringIO(tmp, tmp.tell() - 1, 'З')
        if (isinstance(res.next0, TextToken) and (res.whitespaces_after_count < 2) and res.next0.chars.is_all_upper): 
            if (res.next0.is_value("РД", None) or res.next0.is_value("ПД", None)): 
                print(" {0}".format((res.next0 if isinstance(res.next0, TextToken) else None).term), end="", file=tmp, flush=True)
                res = res.next0
        if (isinstance(res.next0, TextToken) and res.next0.is_char('*')): 
            res = res.next0
        return res
    
    @staticmethod
    def try_attach_list(t : 'Token', prev : 'DecreeToken'=None, max_count : int=10, must_start_by_typ : bool=False) -> typing.List['DecreeToken']:
        """ Привязать примитивы в контейнере с указанной позиции
        
        Args:
            cnt: 
            indFrom: 
        
        Returns:
            typing.List[DecreeToken]: Список примитивов
        """
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NumberExToken import NumberExToken
        p = DecreeToken.try_attach(t, prev, must_start_by_typ)
        if (p is None): 
            return None
        if (p.typ == DecreeToken.ItemType.ORG or p.typ == DecreeToken.ItemType.OWNER): 
            if (t.previous is not None and t.previous.is_value("РАССМОТРЕНИЕ", "РОЗГЛЯД")): 
                return None
        res = list()
        res.append(p)
        tt = p.end_token.next0
        if (tt is not None and t.previous is not None): 
            if (BracketHelper.can_be_start_of_sequence(t.previous, False, False) and BracketHelper.can_be_end_of_sequence(tt, False, None, False)): 
                p.begin_token = t.previous
                p.end_token = tt
                tt = tt.next0
        first_pass2639 = True
        while True:
            if first_pass2639: first_pass2639 = False
            else: tt = tt.next0
            if (not (tt is not None)): break
            ws = False
            if (tt.whitespaces_before_count > 15): 
                ws = True
                if (tt.whitespaces_before_count > 25): 
                    break
            if (max_count > 0 and len(res) >= max_count): 
                la = res[len(res) - 1]
                if (la.typ != DecreeToken.ItemType.TYP and la.typ != DecreeToken.ItemType.DATE and la.typ != DecreeToken.ItemType.NUMBER): 
                    break
                if (len(res) > (max_count * 3)): 
                    break
            p0 = DecreeToken.try_attach(tt, Utils.ifNotNull(prev, p), False)
            if (ws): 
                if (p0 is not None and p is not None and ((((p.typ == DecreeToken.ItemType.TYP and p0.typ == DecreeToken.ItemType.NUMBER)) or ((p0.typ == DecreeToken.ItemType.NAME and p.typ != DecreeToken.ItemType.NAME)) or ((p0.typ == DecreeToken.ItemType.ORG and p.typ == DecreeToken.ItemType.ORG))))): 
                    pass
                else: 
                    break
            if (p0 is None): 
                if (tt.is_newline_before): 
                    break
                if (tt.morph.class0.is_preposition and res[0].typ == DecreeToken.ItemType.TYP): 
                    continue
                if (((tt.is_comma_and or tt.is_hiphen)) and res[0].typ == DecreeToken.ItemType.TYP): 
                    p0 = DecreeToken.try_attach(tt.next0, p, False)
                    if (p0 is not None): 
                        ty0 = p0.typ
                        if (ty0 == DecreeToken.ItemType.ORG or ty0 == DecreeToken.ItemType.OWNER): 
                            ty0 = DecreeToken.ItemType.UNKNOWN
                        ty = p.typ
                        if (ty == DecreeToken.ItemType.ORG or ty == DecreeToken.ItemType.OWNER): 
                            ty = DecreeToken.ItemType.UNKNOWN
                        if (ty0 == ty): 
                            p = p0
                            res.append(p)
                            tt = p.end_token
                            continue
                    p0 = None
                if (tt.is_char(':')): 
                    p0 = DecreeToken.try_attach(tt.next0, p, False)
                    if (p0 is not None): 
                        if (p0.typ == DecreeToken.ItemType.NUMBER or p0.typ == DecreeToken.ItemType.DATE): 
                            p = p0
                            res.append(p)
                            tt = p.end_token
                            continue
                if (tt.is_comma and p.typ == DecreeToken.ItemType.NUMBER): 
                    p0 = DecreeToken.try_attach(tt.next0, p, False)
                    if (p0 is not None and p0.typ == DecreeToken.ItemType.DATE): 
                        p = p0
                        res.append(p)
                        tt = p.end_token
                        continue
                    cou = 0
                    if (res[0].typ == DecreeToken.ItemType.TYP): 
                        for ii in range(1, len(res), 1):
                            if ((res[ii].typ == DecreeToken.ItemType.ORG or res[ii].typ == DecreeToken.ItemType.TERR or res[ii].typ == DecreeToken.ItemType.UNKNOWN) or res[ii].typ == DecreeToken.ItemType.OWNER): 
                                cou += 1
                            else: 
                                break
                        if (cou > 1): 
                            num = Utils.newStringIO(p.value)
                            tmp = Utils.newStringIO(None)
                            tend = None
                            tt1 = tt
                            while tt1 is not None: 
                                if (not tt1.is_comma_and): 
                                    break
                                pp = DecreeToken.try_attach(tt1.next0, p, False)
                                if (pp is not None): 
                                    break
                                if (not ((isinstance(tt1.next0, NumberToken)))): 
                                    break
                                Utils.setLengthStringIO(tmp, 0)
                                tt2 = DecreeToken.__try_attach_number(tt1.next0, tmp, True)
                                if (tt2 is None): 
                                    break
                                print(",{0}".format(Utils.toStringStringIO(tmp)), end="", file=num, flush=True)
                                cou -= 1
                                tend = tt2
                                tt1 = tend
                                tt1 = tt1.next0
                            if (cou == 1): 
                                p.value = Utils.toStringStringIO(num)
                                p.end_token = tend
                                tt = p.end_token
                                continue
                    p0 = None
                if (tt.is_comma and p.typ == DecreeToken.ItemType.DATE): 
                    p0 = DecreeToken.try_attach(tt.next0, p, False)
                    if (p0 is not None and p0.typ == DecreeToken.ItemType.NUMBER): 
                        p = p0
                        res.append(p)
                        tt = p.end_token
                        continue
                    p0 = None
                if (tt.is_comma_and and ((p.typ == DecreeToken.ItemType.ORG or p.typ == DecreeToken.ItemType.OWNER))): 
                    p0 = DecreeToken.try_attach(tt.next0, p, False)
                    if (p0 is not None and ((p0.typ == DecreeToken.ItemType.ORG or p.typ == DecreeToken.ItemType.OWNER))): 
                        p = p0
                        res.append(p)
                        tt = p.end_token
                        continue
                    p0 = None
                if (res[0].typ == DecreeToken.ItemType.TYP): 
                    if (DecreeToken.get_kind(res[0].value) == DecreeKind.PUBLISHER): 
                        if (tt.is_char_of(",;")): 
                            continue
                        p = DecreeToken.try_attach(tt, Utils.ifNotNull(prev, res[0]), False)
                        if ((p) is not None): 
                            res.append(p)
                            tt = p.end_token
                            continue
                if (res[len(res) - 1].typ == DecreeToken.ItemType.UNKNOWN and prev is not None): 
                    p0 = DecreeToken.try_attach(tt, res[len(res) - 1], False)
                    if (p0 is not None): 
                        p = p0
                        res.append(p)
                        tt = p.end_token
                        continue
                if (((isinstance(tt, TextToken) and tt.chars.is_all_upper and BracketHelper.can_be_start_of_sequence(tt.next0, False, False)) and len(res) > 1 and res[len(res) - 1].typ == DecreeToken.ItemType.NUMBER) and res[len(res) - 2].typ == DecreeToken.ItemType.TYP and res[len(res) - 2].typ_kind == DecreeKind.STANDARD): 
                    continue
                if (tt.is_char('(')): 
                    p = DecreeToken.try_attach(tt.next0, None, False)
                    if (p is not None and p.typ == DecreeToken.ItemType.EDITION): 
                        br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                        if (br is not None): 
                            res.append(p)
                            tt = p.end_token.next0
                            while tt is not None: 
                                if (tt.end_char >= br.end_char): 
                                    break
                                p = DecreeToken.try_attach(tt, None, False)
                                if (p is not None): 
                                    res.append(p)
                                    tt = p.end_token
                                tt = tt.next0
                            res[len(res) - 1].end_token = br.end_token
                            tt = res[len(res) - 1].end_token
                            continue
                if (isinstance(tt, NumberToken) and res[len(res) - 1].typ == DecreeToken.ItemType.DATE): 
                    if (tt.previous is not None and tt.previous.morph.class0.is_preposition): 
                        pass
                    elif (NumberExToken.try_parse_number_with_postfix(tt) is not None): 
                        pass
                    else: 
                        tmp = Utils.newStringIO(None)
                        t11 = DecreeToken.__try_attach_number(tt, tmp, False)
                        if (t11 is not None): 
                            p0 = DecreeToken._new793(tt, t11, DecreeToken.ItemType.NUMBER, Utils.toStringStringIO(tmp))
                if (p0 is None): 
                    break
            p = p0
            res.append(p)
            tt = p.end_token
        i = 0
        first_pass2640 = True
        while True:
            if first_pass2640: first_pass2640 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].end_token.next0.is_comma): 
                continue
            if (res[i].typ == DecreeToken.ItemType.UNKNOWN and res[i + 1].typ == DecreeToken.ItemType.UNKNOWN): 
                res[i].value = "{0} {1}".format(res[i].value, res[i + 1].value)
                res[i].end_token = res[i + 1].end_token
                del res[i + 1]
                i -= 1
            elif (((res[i].typ == DecreeToken.ItemType.ORG or res[i].typ == DecreeToken.ItemType.OWNER)) and res[i + 1].typ == DecreeToken.ItemType.UNKNOWN): 
                ok = False
                if (res[i + 1].begin_token.previous.is_comma): 
                    pass
                elif (((i + 2) < len(res)) and res[i + 2].typ == DecreeToken.ItemType.DATE): 
                    ok = True
                if (ok): 
                    res[i].typ = DecreeToken.ItemType.OWNER
                    res[i].value = "{0} {1}".format(res[i].value, res[i + 1].value)
                    res[i].end_token = res[i + 1].end_token
                    res[i].ref = None
                    del res[i + 1]
                    i -= 1
            elif (((res[i].typ == DecreeToken.ItemType.UNKNOWN or res[i].typ == DecreeToken.ItemType.OWNER)) and ((res[i + 1].typ == DecreeToken.ItemType.ORG or res[i + 1].typ == DecreeToken.ItemType.OWNER))): 
                ok = False
                if ((res[i].typ == DecreeToken.ItemType.OWNER or res[i + 1].typ == DecreeToken.ItemType.OWNER or res[i].value == "Пленум") or res[i].value == "Сессия" or res[i].value == "Съезд"): 
                    ok = True
                if (ok): 
                    res[i].typ = DecreeToken.ItemType.OWNER
                    res[i].end_token = res[i + 1].end_token
                    if (res[i].value is not None): 
                        s1 = res[i + 1].value
                        if (s1 is None): 
                            s1 = str(res[i + 1].ref.referent)
                        res[i].value = "{0}, {1}".format(res[i].value, s1)
                    del res[i + 1]
                    i -= 1
            elif ((res[i].typ == DecreeToken.ItemType.TYP and res[i + 1].typ == DecreeToken.ItemType.TERR and ((i + 2) < len(res))) and res[i + 2].typ == DecreeToken.ItemType.STDNAME): 
                res[i].full_value = "{0} {1}".format(res[i].value, res[i + 2].value)
                res[i + 1].end_token = res[i + 2].end_token
                del res[i + 2]
                i -= 1
            else: 
                ok = False
                if (res[i].typ == DecreeToken.ItemType.UNKNOWN and ((((res[i + 1].typ == DecreeToken.ItemType.TERR and prev is not None)) or res[i + 1].typ == DecreeToken.ItemType.OWNER))): 
                    ok = True
                elif (((res[i].typ == DecreeToken.ItemType.UNKNOWN or res[i].typ == DecreeToken.ItemType.ORG or res[i].typ == DecreeToken.ItemType.OWNER)) and res[i + 1].typ == DecreeToken.ItemType.TERR): 
                    ok = True
                if (ok): 
                    res[i].typ = DecreeToken.ItemType.OWNER
                    res[i].end_token = res[i + 1].end_token
                    s1 = res[i + 1].value
                    if (s1 is None): 
                        s1 = str(res[i + 1].ref.referent)
                    res[i].value = "{0}, {1}".format(res[i].value, s1)
                    del res[i + 1]
                    i -= 1
        i = 0
        first_pass2641 = True
        while True:
            if first_pass2641: first_pass2641 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == DecreeToken.ItemType.UNKNOWN): 
                ok = False
                for j in range(i + 1, len(res), 1):
                    if (res[j].begin_token.previous.is_comma): 
                        break
                    elif (res[j].typ == DecreeToken.ItemType.DATE or res[j].typ == DecreeToken.ItemType.NUMBER): 
                        ok = True
                        break
                    elif (res[j].typ == DecreeToken.ItemType.TERR or res[j].typ == DecreeToken.ItemType.ORG or res[j].typ == DecreeToken.ItemType.UNKNOWN): 
                        pass
                    else: 
                        break
                else: j = len(res)
                if (not ok): 
                    continue
                if (j == (i + 1)): 
                    if (res[i].begin_token.previous.is_comma): 
                        res[i].typ = DecreeToken.ItemType.OWNER
                    continue
                tmp = Utils.newStringIO(None)
                ii = i
                while ii < j: 
                    if (ii > i): 
                        if (res[ii].typ == DecreeToken.ItemType.TERR): 
                            print(", ".format(), end="", file=tmp, flush=True)
                        else: 
                            print(' ', end="", file=tmp)
                    if (res[ii].value is not None): 
                        print(res[ii].value, end="", file=tmp)
                    elif (res[ii].ref is not None and res[ii].ref.referent is not None): 
                        print(str(res[ii].ref.referent), end="", file=tmp)
                    ii += 1
                res[i].value = Utils.toStringStringIO(tmp)
                res[i].end_token = res[j - 1].end_token
                res[i].typ = DecreeToken.ItemType.OWNER
                del res[i + 1:i + 1+j - i - 1]
        if ((len(res) == 3 and res[0].typ == DecreeToken.ItemType.TYP and ((res[1].typ == DecreeToken.ItemType.OWNER or res[1].typ == DecreeToken.ItemType.ORG or res[1].typ == DecreeToken.ItemType.TERR))) and res[2].typ == DecreeToken.ItemType.NUMBER): 
            te = res[2].end_token.next0
            while te is not None: 
                if (not te.is_char(',') or te.next0 is None): 
                    break
                res1 = DecreeToken.try_attach_list(te.next0, res[0], 10, False)
                if (res1 is None or (len(res1) < 2)): 
                    break
                if (((res1[0].typ == DecreeToken.ItemType.OWNER or res1[0].typ == DecreeToken.ItemType.ORG or res1[0].typ == DecreeToken.ItemType.TERR)) and res1[1].typ == DecreeToken.ItemType.NUMBER): 
                    res.extend(res1)
                    te = res1[len(res1) - 1].end_token
                else: 
                    break
                te = te.next0
        if (len(res) > 1 and ((res[len(res) - 1].typ == DecreeToken.ItemType.OWNER or res[len(res) - 1].typ == DecreeToken.ItemType.ORG))): 
            te = res[len(res) - 1].end_token.next0
            if (te is not None and te.is_comma_and): 
                res1 = DecreeToken.try_attach_list(te.next0, res[0], 10, False)
                if (res1 is not None and len(res1) > 0): 
                    if (res1[0].typ == DecreeToken.ItemType.OWNER or res1[0].typ == DecreeToken.ItemType.ORG): 
                        res.extend(res1)
        return res
    
    @staticmethod
    def try_attach_name(t : 'Token', typ_ : str, very_probable : bool=False, in_title_doc_ref : bool=False) -> 'DecreeToken':
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.morph.Explanatory import Explanatory
        if (t is None): 
            return None
        if (t.is_char(';')): 
            t = t.next0
        if (t is None): 
            return None
        t0 = t
        t1 = t
        abou = False
        ty = DecreeToken.get_kind(typ_)
        if (t.is_value("О", None) or t.is_value("ОБ", None) or t.is_value("ПРО", None)): 
            t = t.next0
            abou = True
        elif (t.is_value("ПО", None)): 
            if (LanguageHelper.ends_with(typ_, "ЗАКОН")): 
                return None
            t = t.next0
            abou = True
        elif (t.next0 is not None): 
            if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None and br.is_quote_type): 
                    re = t.next0.get_referent()
                    if (re is not None and re.type_name == "URI"): 
                        return None
                    if (t.next0.chars.is_letter): 
                        if (t.next0.chars.is_all_lower or ((isinstance(t.next0, TextToken) and (t.next0 if isinstance(t.next0, TextToken) else None).is_pure_verb))): 
                            return None
                    t1 = br.end_token
                    tt1 = DecreeToken._try_attach_std_change_name(t.next0)
                    if (tt1 is not None): 
                        t1 = tt1
                    s0 = MiscHelper.get_text_value(t0, t1, GetTextAttr.KEEPREGISTER)
                    if (Utils.isNullOrEmpty(s0)): 
                        return None
                    if ((len(s0) < 10) and typ_ != "ПРОГРАММА" and typ_ != "ПРОГРАМА"): 
                        return None
                    return DecreeToken._new793(t, t1, DecreeToken.ItemType.NAME, s0)
                dt = DecreeToken.try_attach_name(t.next0, typ_, False, False)
                if (dt is not None): 
                    dt.begin_token = t
                    return dt
            if (ty != DecreeKind.KONVENTION and ty != DecreeKind.PROGRAM): 
                return None
        if (t is None): 
            return None
        if (t.is_value("ЗАЯВЛЕНИЕ", "ЗАЯВА")): 
            return None
        cou = 0
        tt = t
        first_pass2642 = True
        while True:
            if first_pass2642: first_pass2642 = False
            else: tt = tt.next0
            if (not (tt is not None)): break
            if (tt.is_newline_before and tt != t): 
                if (tt.whitespaces_before_count > 15 or not abou): 
                    break
                if (tt.is_value("ИСТОЧНИК", None)): 
                    break
                if (isinstance(tt, TextToken) and tt.chars.is_letter and tt.chars.is_all_lower): 
                    pass
                else: 
                    break
            if (tt.is_char_of("(,") and tt.next0 is not None): 
                if (tt.next0.is_value("УТВЕРЖДЕННЫЙ", "ЗАТВЕРДЖЕНИЙ") or tt.next0.is_value("ПРИНЯТЫЙ", "ПРИЙНЯТИЙ") or tt.next0.is_value("УТВ", "ЗАТВ")): 
                    ttt = tt.next0.next0
                    if (ttt is not None and ttt.is_char('.') and tt.next0.is_value("УТВ", None)): 
                        ttt = ttt.next0
                    dt = DecreeToken.try_attach(ttt, None, False)
                    if (dt is not None and dt.typ == DecreeToken.ItemType.TYP): 
                        break
                    if (dt is not None and ((dt.typ == DecreeToken.ItemType.ORG or dt.typ == DecreeToken.ItemType.OWNER))): 
                        dt2 = DecreeToken.try_attach(dt.end_token.next0, None, False)
                        if (dt2 is not None and dt2.typ == DecreeToken.ItemType.DATE): 
                            break
            if (very_probable and abou and not tt.is_newline_before): 
                t1 = tt
                continue
            if (tt.is_value("ОТ", "ВІД")): 
                dt = DecreeToken.try_attach(tt, None, False)
                if (dt is not None): 
                    break
            if (tt.morph.class0.is_preposition and tt.next0 is not None and ((isinstance(tt.next0.get_referent(), DateReferent) or isinstance(tt.next0.get_referent(), DateRangeReferent)))): 
                break
            if (in_title_doc_ref): 
                t1 = tt
                continue
            if (tt.morph.class0.is_preposition or tt.morph.class0.is_conjunction): 
                if (cou == 0): 
                    break
                if (tt.next0 is None): 
                    break
                continue
            if (not tt.chars.is_cyrillic_letter): 
                break
            if (tt.morph.class0.is_personal_pronoun or tt.morph.class0.is_pronoun): 
                if (not tt.is_value("ВСЕ", "ВСІ") and not tt.is_value("ВСЯКИЙ", None) and not tt.is_value("ДАННЫЙ", "ДАНИЙ")): 
                    break
            if (isinstance(tt, NumberToken)): 
                break
            pit = PartToken.try_attach(tt, None, False, False)
            if (pit is not None): 
                break
            r = tt.get_referent()
            if (r is not None): 
                if ((isinstance(r, DecreeReferent) or isinstance(r, DateReferent) or isinstance(r, OrganizationReferent)) or isinstance(r, GeoReferent) or r.type_name == "NAMEDENTITY"): 
                    if (tt.is_newline_before): 
                        break
                    t1 = tt
                    continue
            npt = NounPhraseHelper.try_parse(tt, Utils.valToEnum(NounPhraseParseAttr.PARSENUMERICASADJECTIVE | NounPhraseParseAttr.PARSEPREPOSITION, NounPhraseParseAttr), 0)
            if (npt is None): 
                break
            dd = npt.end_token.get_morph_class_in_dictionary()
            if (dd.is_verb and npt.end_token == npt.begin_token): 
                if (not dd.is_noun): 
                    break
                if (tt.is_value("БЫТЬ", "БУТИ")): 
                    break
            if (not npt.morph.case.is_genitive): 
                if (cou > 0): 
                    if ((npt.morph.case.is_instrumental and tt.previous is not None and tt.previous.previous is not None) and ((tt.previous.previous.is_value("РАБОТА", "РОБОТА")))): 
                        pass
                    elif (abou and very_probable): 
                        pass
                    elif (npt.noun.is_value("ГОД", "РІК") or npt.noun.is_value("ПЕРИОД", "ПЕРІОД")): 
                        pass
                    else: 
                        tt0 = tt.previous
                        prep = ""
                        if (tt0 is not None and tt0.morph.class0.is_preposition): 
                            prep = tt0.get_normal_case_text(MorphClass.PREPOSITION, False, MorphGender.UNDEFINED, False)
                            tt0 = tt0.previous
                        ok = False
                        if (isinstance(tt0, TextToken)): 
                            norm = tt0.get_normal_case_text(MorphClass.NOUN, True, MorphGender.UNDEFINED, False)
                            exps = Explanatory.find_words(norm, tt0.morph.language)
                            if (exps is not None): 
                                for ex in exps: 
                                    if (ex.nexts is not None): 
                                        if (len(prep) > 0 and prep in ex.nexts): 
                                            ok = True
                                            break
                                        if (len(prep) == 0 and prep in ex.nexts): 
                                            if (not (ex.nexts[prep] & npt.morph.case).is_undefined): 
                                                ok = True
                                                break
                        if (not ok): 
                            break
                if (not abou): 
                    break
            cou += 1
            t1 = npt.end_token
            tt = t1
            if (npt.noun.is_value("НАЛОГОПЛАТЕЛЬЩИК", None)): 
                ttn = MiscHelper.check_number_prefix(tt.next0)
                if (isinstance(ttn, NumberToken) and (ttn if isinstance(ttn, NumberToken) else None).value == 1): 
                    t1 = ttn
                    tt = t1
        if (tt == t): 
            return None
        if (abou): 
            tt1 = DecreeToken._try_attach_std_change_name(t0)
            if (tt1 is not None and tt1.end_char > t1.end_char): 
                t1 = tt1
        s = MiscHelper.get_text_value(t0, t1, Utils.valToEnum(GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE | GetTextAttr.KEEPREGISTER, GetTextAttr))
        if (Utils.isNullOrEmpty(s) or (len(s) < 10)): 
            return None
        return DecreeToken._new793(t, t1, DecreeToken.ItemType.NAME, s)
    
    @staticmethod
    def _try_attach_std_change_name(t : 'Token') -> 'Token':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.decree.DecreeAnalyzer import DecreeAnalyzer
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        if (not ((isinstance(t, TextToken))) or t.next0 is None): 
            return None
        t0 = t
        term = (t if isinstance(t, TextToken) else None).term
        if ((term != "О" and term != "O" and term != "ОБ") and term != "ПРО"): 
            return None
        t = t.next0
        if (((t.is_value("ВНЕСЕНИЕ", "ВНЕСЕННЯ") or t.is_value("УТВЕРЖДЕНИЕ", "ТВЕРДЖЕННЯ") or t.is_value("ПРИНЯТИЕ", "ПРИЙНЯТТЯ")) or t.is_value("ВВЕДЕНИЕ", "ВВЕДЕННЯ") or t.is_value("ПРИОСТАНОВЛЕНИЕ", "ПРИЗУПИНЕННЯ")) or t.is_value("ОТМЕНА", "СКАСУВАННЯ") or t.is_value("МЕРА", "ЗАХІД")): 
            pass
        elif (t.is_value("ПРИЗНАНИЕ", "ВИЗНАННЯ") and t.next0 is not None and t.next0.is_value("УТРАТИТЬ", "ВТРАТИТИ")): 
            pass
        else: 
            return None
        t1 = t
        tt = t.next0
        first_pass2643 = True
        while True:
            if first_pass2643: first_pass2643 = False
            else: tt = tt.next0
            if (not (tt is not None)): break
            if (tt.whitespaces_before_count > 15): 
                break
            if (tt.morph.class0.is_conjunction or tt.morph.class0.is_preposition): 
                continue
            if (tt.is_comma): 
                continue
            if (MiscHelper.can_be_start_of_sentence(tt)): 
                break
            npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                if ((((((npt.noun.is_value("ВВЕДЕНИЕ", "ВВЕДЕННЯ") or npt.noun.is_value("ПРИОСТАНОВЛЕНИЕ", "ПРИЗУПИНЕННЯ") or npt.noun.is_value("ВНЕСЕНИЕ", "ВНЕСЕННЯ")) or npt.noun.is_value("ИЗМЕНЕНИЕ", "ЗМІНА") or npt.noun.is_value("ДОПОЛНЕНИЕ", "ДОДАТОК")) or npt.noun.is_value("АКТ", None) or npt.noun.is_value("ПРИЗНАНИЕ", "ВИЗНАННЯ")) or npt.noun.is_value("ПРИНЯТИЕ", "ПРИЙНЯТТЯ") or npt.noun.is_value("СИЛА", "ЧИННІСТЬ")) or npt.noun.is_value("ДЕЙСТВИЕ", "ДІЯ") or npt.noun.is_value("СВЯЗЬ", "ЗВЯЗОК")) or npt.noun.is_value("РЕАЛИЗАЦИЯ", "РЕАЛІЗАЦІЯ") or npt.noun.is_value("РЯД", None)): 
                    tt = npt.end_token
                    t1 = tt
                    continue
            if (tt.is_value("ТАКЖЕ", "ТАКОЖ") or tt.is_value("НЕОБХОДИМЫЙ", "НЕОБХІДНИЙ")): 
                continue
            r = tt.get_referent()
            if (isinstance(r, GeoReferent) or isinstance(r, DecreeReferent) or isinstance(r, DecreePartReferent)): 
                t1 = tt
                continue
            if (isinstance(r, OrganizationReferent) and tt.is_newline_after): 
                t1 = tt
                continue
            pts = PartToken.try_attach_list(tt, False, 40)
            while pts is not None and len(pts) > 0:
                if (pts[0].typ == PartToken.ItemType.PREFIX): 
                    del pts[0]
                else: 
                    break
            if (pts is not None and len(pts) > 0): 
                tt = pts[len(pts) - 1].end_token
                t1 = tt
                continue
            dts = DecreeToken.try_attach_list(tt, None, 10, False)
            if (dts is not None and len(dts) > 0): 
                rts = DecreeAnalyzer._try_attach(dts, None, None)
                if (rts is not None): 
                    tt = rts[0].end_token
                    t1 = tt
                    continue
                if (dts[0].typ == DecreeToken.ItemType.TYP): 
                    rt = DecreeAnalyzer._try_attach_approved(tt, None)
                    if (rt is not None): 
                        tt = rt.end_token
                        t1 = tt
                        continue
            tt1 = DecreeToken.is_keyword(tt, False)
            if (tt1 is not None): 
                tt = tt1
                t1 = tt
                continue
            if (isinstance(tt, NumberToken)): 
                continue
            if (not tt.chars.is_all_lower and tt.length_char > 2 and tt.get_morph_class_in_dictionary().is_undefined): 
                t1 = tt
                continue
            break
        if (BracketHelper.can_be_start_of_sequence(t0.previous, True, False)): 
            if (BracketHelper.can_be_end_of_sequence(t1.next0, True, t0.previous, False)): 
                t1 = t1.next0
        return t1
    
    __m_termins = None
    
    __m_keywords = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (DecreeToken.__m_termins is not None): 
            return
        DecreeToken.__m_termins = TerminCollection()
        DecreeToken.__m_keywords = TerminCollection()
        for s in DecreeToken.__m_misc_typesru: 
            DecreeToken.__m_keywords.add(Termin(s))
        for s in DecreeToken.__m_misc_typesua: 
            DecreeToken.__m_keywords.add(Termin._new844(s, MorphLang.UA))
        for s in DecreeToken.__m_all_typesru: 
            DecreeToken.__m_termins.add(Termin._new118(s, DecreeToken.ItemType.TYP))
            DecreeToken.__m_keywords.add(Termin._new118(s, DecreeToken.ItemType.TYP))
        for s in DecreeToken.__m_all_typesua: 
            DecreeToken.__m_termins.add(Termin._new119(s, DecreeToken.ItemType.TYP, MorphLang.UA))
            DecreeToken.__m_keywords.add(Termin._new119(s, DecreeToken.ItemType.TYP, MorphLang.UA))
        DecreeToken.__m_termins.add(Termin._new118("ОТРАСЛЕВОЕ СОГЛАШЕНИЕ", DecreeToken.ItemType.TYP))
        DecreeToken.__m_termins.add(Termin._new459("ГАЛУЗЕВА УГОДА", MorphLang.UA, DecreeToken.ItemType.TYP))
        DecreeToken.__m_termins.add(Termin._new118("МЕЖОТРАСЛЕВОЕ СОГЛАШЕНИЕ", DecreeToken.ItemType.TYP))
        DecreeToken.__m_termins.add(Termin._new459("МІЖГАЛУЗЕВА УГОДА", MorphLang.UA, DecreeToken.ItemType.TYP))
        DecreeToken.__m_termins.add(Termin._new120("ОСНОВЫ ЗАКОНОДАТЕЛЬСТВА", DecreeToken.ItemType.TYP, DecreeKind.KODEX))
        DecreeToken.__m_termins.add(Termin._new854("ОСНОВИ ЗАКОНОДАВСТВА", MorphLang.UA, DecreeToken.ItemType.TYP, DecreeKind.KODEX))
        DecreeToken.__m_termins.add(Termin._new120("ОСНОВЫ ГРАЖДАНСКОГО ЗАКОНОДАТЕЛЬСТВА", DecreeToken.ItemType.TYP, DecreeKind.KODEX))
        DecreeToken.__m_termins.add(Termin._new854("ОСНОВИ ЦИВІЛЬНОГО ЗАКОНОДАВСТВА", MorphLang.UA, DecreeToken.ItemType.TYP, DecreeKind.KODEX))
        t = Termin._new144("ФЕДЕРАЛЬНЫЙ ЗАКОН", DecreeToken.ItemType.TYP, "ФЗ")
        DecreeToken.__m_termins.add(t)
        t = Termin._new858("ФЕДЕРАЛЬНИЙ ЗАКОН", MorphLang.UA, DecreeToken.ItemType.TYP, "ФЗ")
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("ПРОЕКТ ЗАКОНА", DecreeToken.ItemType.TYP)
        t.add_variant("ЗАКОНОПРОЕКТ", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("ПАСПОРТ ПРОЕКТА", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new459("ПРОЕКТ ЗАКОНУ", MorphLang.UA, DecreeToken.ItemType.TYP)
        t.add_variant("ЗАКОНОПРОЕКТ", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new459("ПАСПОРТ ПРОЕКТУ", MorphLang.UA, DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new142("ГОСУДАРСТВЕННАЯ ПРОГРАММА", "ПРОГРАММА", DecreeToken.ItemType.TYP)
        t.add_variant("ГОСУДАРСТВЕННАЯ ЦЕЛЕВАЯ ПРОГРАММА", False)
        t.add_variant("ФЕДЕРАЛЬНАЯ ЦЕЛЕВАЯ ПРОГРАММА", False)
        t.add_abridge("ФЕДЕРАЛЬНАЯ ПРОГРАММА")
        t.add_variant("МЕЖГОСУДАРСТВЕННАЯ ЦЕЛЕВАЯ ПРОГРАММА", False)
        t.add_abridge("МЕЖГОСУДАРСТВЕННАЯ ПРОГРАММА")
        t.add_variant("ГОСПРОГРАММА", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new864("ДЕРЖАВНА ПРОГРАМА", "ПРОГРАМА", MorphLang.UA, DecreeToken.ItemType.TYP)
        t.add_variant("ДЕРЖАВНА ЦІЛЬОВА ПРОГРАМА", False)
        t.add_variant("ФЕДЕРАЛЬНА ЦІЛЬОВА ПРОГРАМА", False)
        t.add_abridge("ФЕДЕРАЛЬНА ПРОГРАМА")
        t.add_variant("ДЕРЖПРОГРАМА", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new144("ФЕДЕРАЛЬНЫЙ КОНСТИТУЦИОННЫЙ ЗАКОН", DecreeToken.ItemType.TYP, "ФКЗ")
        t.add_variant("КОНСТИТУЦИОННЫЙ ЗАКОН", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new858("ФЕДЕРАЛЬНИЙ КОНСТИТУЦІЙНИЙ ЗАКОН", MorphLang.UA, DecreeToken.ItemType.TYP, "ФКЗ")
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("УГОЛОВНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "УК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("КРИМИНАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "КК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("КРИМІНАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "КК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("УГОЛОВНО-ПРОЦЕССУАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "УПК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("КРИМІНАЛЬНО-ПРОЦЕСУАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "КПК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("УГОЛОВНО-ИСПОЛНИТЕЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "УИК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("КРИМІНАЛЬНО-ВИКОНАВЧИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "КВК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ГРАЖДАНСКИЙ КОДЕКС", DecreeToken.ItemType.TYP, "ГК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("ЦИВІЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЦК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ГРАЖДАНСКИЙ ПРОЦЕССУАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ГПК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("ЦИВІЛЬНИЙ ПРОЦЕСУАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЦПК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ГРАДОСТРОИТЕЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ГРК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("МІСТОБУДІВНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "МБК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ХОЗЯЙСТВЕННЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ХК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("ГОСПОДАРСЬКИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ГК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ХОЗЯЙСТВЕННЫЙ ПРОЦЕССУАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ХПК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("ГОСПОДАРСЬКИЙ ПРОЦЕСУАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ГПК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new120("АРБИТРАЖНЫЙ ПРОЦЕССУАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, DecreeKind.KODEX)
        t.add_abridge("АПК")
        DecreeToken.__m_termins.add(t)
        t = Termin._new854("АРБІТРАЖНИЙ ПРОЦЕСУАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, DecreeKind.KODEX)
        t.add_abridge("АПК")
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("КОДЕКС ВНУТРЕННЕГО ВОДНОГО ТРАНСПОРТА", DecreeToken.ItemType.TYP, "КВВТ", DecreeKind.KODEX)
        t.add_variant("КВ ВТ", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ТРУДОВОЙ КОДЕКС", DecreeToken.ItemType.TYP, "ТК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("ТРУДОВИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ТК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new120("КОДЕКС ЗАКОНОВ О ТРУДЕ", DecreeToken.ItemType.TYP, DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("КОДЕКС ЗАКОНІВ ПРО ПРАЦЮ", MorphLang.UA, DecreeToken.ItemType.TYP, "КЗПП", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ЖИЛИЩНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ЖК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("ЖИТЛОВИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЖК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ЗЕМЕЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ЗК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("ЗЕМЕЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЗК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ЛЕСНОЙ КОДЕКС", DecreeToken.ItemType.TYP, "ЛК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("ЛІСОВИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЛК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("БЮДЖЕТНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "БК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("БЮДЖЕТНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "БК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("НАЛОГОВЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "НК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("ПОДАТКОВИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ПК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("СЕМЕЙНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "СК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("СІМЕЙНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "СК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ВОДНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ВК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("ВОДНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ВК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ВОЗДУШНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ВК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("ПОВІТРЯНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ПК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("КОДЕКС ОБ АДМИНИСТРАТИВНЫХ ПРАВОНАРУШЕНИЯХ", DecreeToken.ItemType.TYP, "КОАП", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("КОДЕКС ПРО АДМІНІСТРАТИВНІ ПРАВОПОРУШЕННЯ", MorphLang.UA, DecreeToken.ItemType.TYP, "КОАП", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("ОБ АДМИНИСТРАТИВНЫХ ПРАВОНАРУШЕНИЯХ", DecreeToken.ItemType.STDNAME)
        DecreeToken.__m_termins.add(t)
        t = Termin._new459("ПРО АДМІНІСТРАТИВНІ ПРАВОПОРУШЕННЯ", MorphLang.UA, DecreeToken.ItemType.STDNAME)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("КОДЕКС ОБ АДМИНИСТРАТИВНЫХ ПРАВОНАРУШЕНИЯХ", DecreeToken.ItemType.TYP, "КРКОАП", DecreeKind.KODEX)
        t.add_variant("КРК ОБ АП", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("КОДЕКС АДМИНИСТРАТИВНОГО СУДОПРОИЗВОДСТВА", DecreeToken.ItemType.TYP, "КАС", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("КОДЕКС АДМІНІСТРАТИВНОГО СУДОЧИНСТВА", MorphLang.UA, DecreeToken.ItemType.TYP, "КАС", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ТАМОЖЕННЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ТК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("МИТНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "МК", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("КОДЕКС ТОРГОВОГО МОРЕПЛАВАНИЯ", DecreeToken.ItemType.TYP, "КТМ", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("КОДЕКС ТОРГОВЕЛЬНОГО МОРЕПЛАВСТВА", MorphLang.UA, DecreeToken.ItemType.TYP, "КТМ", DecreeKind.KODEX)
        DecreeToken.__m_termins.add(t)
        t = Termin._new867("ПРАВИЛА ДОРОЖНОГО ДВИЖЕНИЯ", DecreeToken.ItemType.TYP, "ПДД", "ПРАВИЛА")
        DecreeToken.__m_termins.add(t)
        t = Termin._new869("ПРАВИЛА ДОРОЖНЬОГО РУХУ", MorphLang.UA, DecreeToken.ItemType.TYP, "ПДР", "ПРАВИЛА")
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("СОБРАНИЕ ЗАКОНОДАТЕЛЬСТВА", DecreeToken.ItemType.TYP)
        t.add_abridge("СЗ")
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("ОФИЦИАЛЬНЫЙ ВЕСТНИК", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new459("ОФІЦІЙНИЙ ВІСНИК", MorphLang.UA, DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("СВОД ЗАКОНОВ", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("БЮЛЛЕТЕНЬ НОРМАТИВНЫХ АКТОВ ФЕДЕРАЛЬНЫХ ОРГАНОВ ИСПОЛНИТЕЛЬНОЙ ВЛАСТИ", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("БЮЛЛЕТЕНЬ МЕЖДУНАРОДНЫХ ДОГОВОРОВ", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("БЮЛЛЕТЕНЬ ВЕРХОВНОГО СУДА", DecreeToken.ItemType.TYP)
        t.add_variant("БЮЛЛЕТЕНЬ ВС", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("ВЕСТНИК ВЫСШЕГО АРБИТРАЖНОГО СУДА", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("ВЕСТНИК БАНКА РОССИИ", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("РОССИЙСКАЯ ГАЗЕТА", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("РОССИЙСКИЕ ВЕСТИ", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("СОБРАНИЕ АКТОВ ПРЕЗИДЕНТА И ПРАВИТЕЛЬСТВА", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("ВЕДОМОСТИ ВЕРХОВНОГО СОВЕТА", DecreeToken.ItemType.TYP)
        t.add_variant("ВЕДОМОСТИ ВС", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("ВЕДОМОСТИ СЪЕЗДА НАРОДНЫХ ДЕПУТАТОВ И ВЕРХОВНОГО СОВЕТА", DecreeToken.ItemType.TYP)
        t.add_variant("ВЕДОМОСТИ СЪЕЗДА НАРОДНЫХ ДЕПУТАТОВ РФ И ВЕРХОВНОГО СОВЕТА", False)
        t.add_variant("ВЕДОМОСТИ СЪЕЗДА НАРОДНЫХ ДЕПУТАТОВ", False)
        t.add_variant("ВЕДОМОСТИ СНД РФ И ВС", False)
        t.add_variant("ВЕДОМОСТИ СНД И ВС", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new118("БЮЛЛЕТЕНЬ НОРМАТИВНЫХ АКТОВ МИНИСТЕРСТВ И ВЕДОМСТВ", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        DecreeToken.__m_termins.add(Termin._new118("СВОД ЗАКОНОВ", DecreeToken.ItemType.TYP))
        DecreeToken.__m_termins.add(Termin._new118("ВЕДОМОСТИ", DecreeToken.ItemType.TYP))
        t = Termin._new142("ЗАРЕГИСТРИРОВАТЬ", "РЕГИСТРАЦИЯ", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new938("ЗАРЕЄСТРУВАТИ", MorphLang.UA, "РЕЄСТРАЦІЯ", DecreeToken.ItemType.TYP)
        DecreeToken.__m_termins.add(t)
        t = Termin._new120("СТАНДАРТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("МЕЖДУНАРОДНЫЙ СТАНДАРТ", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new120("ГОСТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ГОСУДАРСТВЕННЫЙ СТАНДАРТ", False)
        t.add_variant("ГОССТАНДАРТ", False)
        t.add_variant("НАЦИОНАЛЬНЫЙ СТАНДАРТ", False)
        t.add_variant("МЕЖГОСУДАРСТВЕННЫЙ СТАНДАРТ", False)
        t.add_variant("ДЕРЖАВНИЙ СТАНДАРТ", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new120("ПНСТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ПРЕДВАРИТЕЛЬНЫЙ НАЦИОНАЛЬНЫЙ СТАНДАРТ", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new120("РСТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("РЕСПУБЛИКАНСКИЙ СТАНДАРТ", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new120("ПБУ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ПОЛОЖЕНИЕ ПО БУХГАЛТЕРСКОМУ УЧЕТУ", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new120("ISO", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ИСО", False)
        t.add_variant("ISO/IEC", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new945("ТЕХНИЧЕСКИЕ УСЛОВИЯ", "ТУ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ТЕХУСЛОВИЯ", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new120("СТРОИТЕЛЬНЫЕ НОРМЫ И ПРАВИЛА", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("СНИП", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new945("СТРОИТЕЛЬНЫЕ НОРМЫ", "СН", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("CH", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new945("ВЕДОМСТВЕННЫЕ СТРОИТЕЛЬНЫЕ НОРМЫ", "ВСН", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("BCH", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new945("РЕСПУБЛИКАНСКИЕ СТРОИТЕЛЬНЫЕ НОРМЫ", "РСН", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("PCH", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new945("НОРМЫ ПОЖАРНОЙ БЕЗОПАСНОСТИ", "НПБ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.__m_termins.add(t)
        t = Termin._new945("ПРАВИЛА ПОЖАРНОЙ БЕЗОПАСНОСТИ", "ППБ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.__m_termins.add(t)
        t = Termin._new945("СТРОИТЕЛЬНЫЕ ПРАВИЛА", "СП", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.__m_termins.add(t)
        t = Termin._new945("МОСКОВСКИЕ ГОРОДСКИЕ СТРОИТЕЛЬНЫЕ НОРМЫ", "МГСН", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.__m_termins.add(t)
        t = Termin._new120("АВОК", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ABOK", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new120("СТАНДАРТ ОРГАНИЗАЦИИ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("СТО", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new945("ПРАВИЛА ПО ОХРАНЕ ТРУДА", "ПОТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ПРАВИЛА ОХРАНЫ ТРУДА", False)
        DecreeToken.__m_termins.add(t)
        t = Termin._new945("РУКОВОДЯЩИЙ ДОКУМЕНТ", "РД", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.__m_termins.add(t)
        t = Termin._new120("САНИТАРНЫЕ НОРМЫ И ПРАВИЛА", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("САНПИН", False)
        DecreeToken.__m_termins.add(t)
    
    @staticmethod
    def is_keyword(t : 'Token', is_misc_type_only : bool=False) -> 'Token':
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.decree.internal.PartToken import PartToken
        if (t is None): 
            return None
        tok = DecreeToken.__m_keywords.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            if (is_misc_type_only and tok.termin.tag is not None): 
                return None
            tok.end_token.tag = tok.termin.canonic_text
            return tok.end_token
        if (not t.morph.class0.is_adjective and not t.morph.class0.is_pronoun): 
            return None
        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
        if (npt is None or npt.begin_token == npt.end_token): 
            tok = DecreeToken.__m_keywords.try_parse(t.next0, TerminParseAttr.NO)
            if (((t.is_value("НАСТОЯЩИЙ", "СПРАВЖНІЙ") or t.is_value("НАЗВАННЫЙ", "НАЗВАНИЙ") or t.is_value("ДАННЫЙ", "ДАНИЙ"))) and (tok) is not None): 
                tok.end_token.tag = tok.termin.canonic_text
                return tok.end_token
            return None
        tok = DecreeToken.__m_keywords.try_parse(npt.end_token, TerminParseAttr.NO)
        if ((tok) is not None): 
            if (is_misc_type_only and tok.termin.tag is not None): 
                return None
            tok.end_token.tag = tok.termin.canonic_text
            return tok.end_token
        pp = PartToken.try_attach(npt.end_token, None, False, True)
        if (pp is not None): 
            return pp.end_token
        return None
    
    @staticmethod
    def is_keyword_str(word : str, is_misc_type_only : bool=False) -> bool:
        if (not is_misc_type_only): 
            if (word in DecreeToken.__m_all_typesru or word in DecreeToken.__m_all_typesua): 
                return True
        if (word in DecreeToken.__m_misc_typesru or word in DecreeToken.__m_misc_typesua): 
            return True
        return False
    
    @staticmethod
    def add_new_type(typ_ : str, acronym : str=None) -> None:
        """ Добавить новый тип НПА
        
        Args:
            typ_(str): 
            acronym(str): 
        """
        from pullenti.ner.core.Termin import Termin
        t = Termin._new144(typ_, DecreeToken.ItemType.TYP, acronym)
        DecreeToken.__m_termins.add(t)
        DecreeToken.__m_keywords.add(Termin._new118(typ_, DecreeToken.ItemType.TYP))
    
    __m_all_typesru = None
    
    __m_all_typesua = None
    
    __m_misc_typesru = None
    
    __m_misc_typesua = None
    
    __m_std_adjectives = None
    
    __m_empty_adjectives = None
    
    @staticmethod
    def get_kind(typ_ : str) -> 'DecreeKind':
        if (typ_ is None): 
            return DecreeKind.UNDEFINED
        if (LanguageHelper.ends_with_ex(typ_, "КОНСТИТУЦИЯ", "КОНСТИТУЦІЯ", "КОДЕКС", None)): 
            return DecreeKind.KODEX
        if (typ_.startswith("ОСНОВ") and LanguageHelper.ends_with_ex(typ_, "ЗАКОНОДАТЕЛЬСТВА", "ЗАКОНОДАВСТВА", None, None)): 
            return DecreeKind.KODEX
        if ((typ_ == "УСТАВ" or typ_ == "СТАТУТ" or typ_ == "ХАРТИЯ") or typ_ == "ХАРТІЯ" or typ_ == "РЕГЛАМЕНТ"): 
            return DecreeKind.USTAV
        if (("ДОГОВОР" in typ_ or "ДОГОВІР" in typ_ or "КОНТРАКТ" in typ_) or "СОГЛАШЕНИЕ" in typ_ or "ПРОТОКОЛ" in typ_): 
            return DecreeKind.CONTRACT
        if (typ_.startswith("ПРОЕКТ")): 
            return DecreeKind.PROJECT
        if (typ_ == "ПРОГРАММА" or typ_ == "ПРОГРАМА"): 
            return DecreeKind.PROGRAM
        if (((((typ_ == "ГОСТ" or typ_ == "ISO" or typ_ == "СНИП") or typ_ == "RFC" or "НОРМЫ" in typ_) or "ПРАВИЛА" in typ_ or "УСЛОВИЯ" in typ_) or "СТАНДАРТ" in typ_ or typ_ == "РУКОВОДЯЩИЙ ДОКУМЕНТ") or typ_ == "АВОК"): 
            return DecreeKind.STANDARD
        if ((LanguageHelper.ends_with_ex(typ_, "КОНВЕНЦИЯ", "КОНВЕНЦІЯ", None, None) or LanguageHelper.ends_with_ex(typ_, "ДОГОВОР", "ДОГОВІР", None, None) or LanguageHelper.ends_with_ex(typ_, "ПАКТ", "БИЛЛЬ", "БІЛЛЬ", None)) or LanguageHelper.ends_with_ex(typ_, "ДЕКЛАРАЦИЯ", "ДЕКЛАРАЦІЯ", None, None)): 
            return DecreeKind.KONVENTION
        if ((((((typ_.startswith("СОБРАНИЕ") or typ_.startswith("ЗБОРИ") or typ_.startswith("РЕГИСТРАЦИЯ")) or typ_.startswith("РЕЄСТРАЦІЯ") or "БЮЛЛЕТЕНЬ" in typ_) or "БЮЛЕТЕНЬ" in typ_ or "ВЕДОМОСТИ" in typ_) or "ВІДОМОСТІ" in typ_ or typ_.startswith("СВОД")) or typ_.startswith("ЗВЕДЕННЯ") or LanguageHelper.ends_with_ex(typ_, "ГАЗЕТА", "ВЕСТИ", "ВІСТІ", None)) or "ВЕСТНИК" in typ_ or LanguageHelper.ends_with(typ_, "ВІСНИК")): 
            return DecreeKind.PUBLISHER
        return DecreeKind.UNDEFINED
    
    @staticmethod
    def is_law(typ_ : str) -> bool:
        if (typ_ is None): 
            return False
        ki = DecreeToken.get_kind(typ_)
        if (ki == DecreeKind.KODEX): 
            return True
        if (LanguageHelper.ends_with(typ_, "ЗАКОН")): 
            return True
        return False

    
    @staticmethod
    def _new791(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new793(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str) -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new795(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'ReferentToken') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        return res
    
    @staticmethod
    def _new799(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'ReferentToken', _arg5 : str) -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new815(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : int) -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.num_year = _arg5
        return res
    
    @staticmethod
    def _new817(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'ReferentToken', _arg5 : 'MorphCollection') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new818(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : 'MorphCollection') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new819(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : 'MorphCollection', _arg6 : bool) -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.morph = _arg5
        res.is_doubtful = _arg6
        return res
    
    @staticmethod
    def _new823(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'MorphCollection') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.value = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new834(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'MorphCollection', _arg5 : str) -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.value = _arg5
        return res
    
    # static constructor for class DecreeToken
    @staticmethod
    def _static_ctor():
        DecreeToken.__m_all_typesru = list(["УКАЗ", "УКАЗАНИЕ", "ПОСТАНОВЛЕНИЕ", "РАСПОРЯЖЕНИЕ", "ПРИКАЗ", "ДИРЕКТИВА", "ПИСЬМО", "ЗАПИСКА", "ИНФОРМАЦИОННОЕ ПИСЬМО", "ИНСТРУКЦИЯ", "ЗАКОН", "КОДЕКС", "КОНСТИТУЦИЯ", "РЕШЕНИЕ", "ПОЛОЖЕНИЕ", "РАСПОРЯЖЕНИЕ", "ПОРУЧЕНИЕ", "РЕЗОЛЮЦИЯ", "ДОГОВОР", "СУБДОГОВОР", "АГЕНТСКИЙ ДОГОВОР", "ДОВЕРЕННОСТЬ", "КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ", "КОНТРАКТ", "ГОСУДАРСТВЕННЫЙ КОНТРАКТ", "ОПРЕДЕЛЕНИЕ", "ПРИГОВОР", "СОГЛАШЕНИЕ", "ПРОТОКОЛ", "ЗАЯВЛЕНИЕ", "УВЕДОМЛЕНИЕ", "РАЗЪЯСНЕНИЕ", "УСТАВ", "ХАРТИЯ", "КОНВЕНЦИЯ", "ПАКТ", "БИЛЛЬ", "ДЕКЛАРАЦИЯ", "РЕГЛАМЕНТ", "ТЕЛЕГРАММА", "ТЕЛЕФОНОГРАММА", "ТЕЛЕФАКСОГРАММА", "ТЕЛЕТАЙПОГРАММА", "ФАКСОГРАММА", "ОТВЕТЫ НА ВОПРОСЫ", "ВЫПИСКА ИЗ ПРОТОКОЛА", "ЗАКЛЮЧЕНИЕ", "ДЕКРЕТ"])
        DecreeToken.__m_all_typesua = list(["УКАЗ", "НАКАЗ", "ПОСТАНОВА", "РОЗПОРЯДЖЕННЯ", "НАКАЗ", "ДИРЕКТИВА", "ЛИСТ", "ЗАПИСКА", "ІНФОРМАЦІЙНИЙ ЛИСТ", "ІНСТРУКЦІЯ", "ЗАКОН", "КОДЕКС", "КОНСТИТУЦІЯ", "РІШЕННЯ", "ПОЛОЖЕННЯ", "РОЗПОРЯДЖЕННЯ", "ДОРУЧЕННЯ", "РЕЗОЛЮЦІЯ", "ДОГОВІР", "СУБКОНТРАКТ", "АГЕНТСЬКИЙ ДОГОВІР", "ДОРУЧЕННЯ", "КОМЕРЦІЙНА ПРОПОЗИЦІЯ", "КОНТРАКТ", "ДЕРЖАВНИЙ КОНТРАКТ", "ВИЗНАЧЕННЯ", "ВИРОК", "УГОДА", "ПРОТОКОЛ", "ЗАЯВА", "ПОВІДОМЛЕННЯ", "РОЗ'ЯСНЕННЯ", "СТАТУТ", "ХАРТІЯ", "КОНВЕНЦІЯ", "ПАКТ", "БІЛЛЬ", "ДЕКЛАРАЦІЯ", "РЕГЛАМЕНТ", "ТЕЛЕГРАМА", "ТЕЛЕФОНОГРАМА", "ТЕЛЕФАКСОГРАММА", "ТЕЛЕТАЙПОГРАМА", "ФАКСОГРАМА", "ВІДПОВІДІ НА ЗАПИТАННЯ", "ВИТЯГ З ПРОТОКОЛУ", "ВИСНОВОК", "ДЕКРЕТ"])
        DecreeToken.__m_misc_typesru = list(["ПРАВИЛО", "ПРОГРАММА", "ПЕРЕЧЕНЬ", "ПОСОБИЕ", "РЕКОМЕНДАЦИЯ", "НАСТАВЛЕНИЕ", "СТАНДАРТ", "СОГЛАШЕНИЕ", "МЕТОДИКА", "ТРЕБОВАНИЕ", "ПОЛОЖЕНИЕ", "СПИСОК", "ЛИСТ", "ТАБЛИЦА", "ЗАЯВКА", "АКТ", "ФОРМА", "НОРМАТИВ", "ПОРЯДОК", "ИНФОРМАЦИЯ", "НОМЕНКЛАТУРА", "ОСНОВА", "ОБЗОР", "КОНЦЕПЦИЯ", "СТРАТЕГИЯ", "СТРУКТУРА", "УСЛОВИЕ", "КЛАССИФИКАТОР", "ОБЩЕРОССИЙСКИЙ КЛАССИФИКАТОР", "СПЕЦИФИКАЦИЯ", "ОБРАЗЕЦ"])
        DecreeToken.__m_misc_typesua = list(["ПРАВИЛО", "ПРОГРАМА", "ПЕРЕЛІК", "ДОПОМОГА", "РЕКОМЕНДАЦІЯ", "ПОВЧАННЯ", "СТАНДАРТ", "УГОДА", "МЕТОДИКА", "ВИМОГА", "ПОЛОЖЕННЯ", "СПИСОК", "ТАБЛИЦЯ", "ЗАЯВКА", "АКТ", "ФОРМА", "НОРМАТИВ", "ПОРЯДОК", "ІНФОРМАЦІЯ", "НОМЕНКЛАТУРА", "ОСНОВА", "ОГЛЯД", "КОНЦЕПЦІЯ", "СТРАТЕГІЯ", "СТРУКТУРА", "УМОВА", "КЛАСИФІКАТОР", "ЗАГАЛЬНОРОСІЙСЬКИЙ КЛАСИФІКАТОР", "СПЕЦИФІКАЦІЯ", "ЗРАЗОК"])
        DecreeToken.__m_std_adjectives = list(["ВСЕОБЩИЙ", "МЕЖДУНАРОДНЫЙ", "ЗАГАЛЬНИЙ", "МІЖНАРОДНИЙ", "НОРМАТИВНЫЙ", "НОРМАТИВНИЙ", "КАССАЦИОННЫЙ", "АПЕЛЛЯЦИОННЫЙ", "КАСАЦІЙНИЙ", "АПЕЛЯЦІЙНИЙ"])
        DecreeToken.__m_empty_adjectives = list(["НЫНЕШНИЙ", "ПРЕДЫДУЩИЙ", "ДЕЙСТВУЮЩИЙ", "НАСТОЯЩИЙ", "НИНІШНІЙ", "ПОПЕРЕДНІЙ", "СПРАВЖНІЙ"])

DecreeToken._static_ctor()