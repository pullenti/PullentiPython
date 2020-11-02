# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import datetime
import typing
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.decree.internal.PartToken import PartToken
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.denomination.DenominationReferent import DenominationReferent
from pullenti.ner.date.DateRangeReferent import DateRangeReferent
from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
from pullenti.ner.mail.internal.MailLine import MailLine
from pullenti.ner.decree.DecreeAnalyzer import DecreeAnalyzer
from pullenti.ner.core.ConjunctionHelper import ConjunctionHelper
from pullenti.morph.MorphCase import MorphCase
from pullenti.semantic.core.SemanticHelper import SemanticHelper
from pullenti.ner.person.PersonPropertyKind import PersonPropertyKind
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.decree.DecreeKind import DecreeKind
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.decree.DecreeReferent import DecreeReferent
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.decree.internal.DecreeChangeToken import DecreeChangeToken
from pullenti.ner.org.OrganizationReferent import OrganizationReferent

class DecreeToken(MetaToken):
    # Примитив, из которых состоит декрет
    
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
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = DecreeToken.ItemType.TYP
        self.value = None;
        self.full_value = None;
        self.ref = None;
        self.children = None
        self.is_doubtful = False
        self.typ_kind = DecreeKind.UNDEFINED
        self.num_year = 0
        self.alias_token = None;
    
    @property
    def is_delo(self) -> bool:
        if (self.begin_token.is_value("ДЕЛО", "СПРАВА")): 
            return True
        if (self.begin_token.next0_ is not None and self.begin_token.next0_.is_value("ДЕЛО", "СПРАВА")): 
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
                res = DecreeToken.__try_attach(t.next0_, prev, 0, must_by_typ)
                if (res is not None and res.typ == DecreeToken.ItemType.NAME): 
                    res.begin_token = t
                    return res
            if (t.is_value("ПРОЕКТ", None)): 
                res = DecreeToken.__try_attach(t.next0_, prev, 0, False)
                if (res is not None and res.typ == DecreeToken.ItemType.TYP and res.value is not None): 
                    if ("ЗАКОН" in res.value or not (isinstance(res.end_token, TextToken))): 
                        res.value = "ПРОЕКТ ЗАКОНА"
                    else: 
                        res.value = ("ПРОЕКТ " + res.end_token.term)
                    res.begin_token = t
                    return res
                elif (res is not None and res.typ == DecreeToken.ItemType.NUMBER): 
                    res1 = DecreeToken.__try_attach(res.end_token.next0_, prev, 0, False)
                    if (res1 is not None and res1.typ == DecreeToken.ItemType.TYP and (isinstance(res1.end_token, TextToken))): 
                        res = DecreeToken._new842(t, t, DecreeToken.ItemType.TYP)
                        res.value = ("ПРОЕКТ " + res1.end_token.term)
                        return res
            if (t.is_value("ИНФОРМАЦИЯ", "ІНФОРМАЦІЯ") and (t.whitespaces_after_count < 3)): 
                dts = DecreeToken.try_attach_list(t.next0_, None, 10, False)
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
                    res = DecreeToken._new842(t, t, DecreeToken.ItemType.TYP)
                    res.value = "ИНФОРМАЦИЯ"
                    return res
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                if ((npt.end_token.is_value("СОБРАНИЕ", None) or npt.end_token.is_value("УЧАСТНИК", None) or npt.end_token.is_value("СОБСТВЕННИК", None)) or npt.end_token.is_value("УЧРЕДИТЕЛЬ", None)): 
                    res = DecreeToken._new842(t, npt.end_token, DecreeToken.ItemType.OWNER)
                    npt2 = NounPhraseHelper.try_parse(res.end_token.next0_, NounPhraseParseAttr.NO, 0, None)
                    if (npt2 is not None and npt2.morph.case_.is_genitive): 
                        res.end_token = npt2.end_token
                    res.value = MiscHelper.get_text_value(t, res.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                    return res
            return None
        if (res.typ == DecreeToken.ItemType.DATE): 
            if (res.ref is None): 
                return None
            dre = Utils.asObjectOrNull(res.ref.referent, DateReferent)
            if (dre is None): 
                return None
        if (res.begin_token.begin_char > res.end_token.end_char): 
            pass
        if (res.typ == DecreeToken.ItemType.NUMBER): 
            tt = res.end_token.next0_
            first_pass3588 = True
            while True:
                if first_pass3588: first_pass3588 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (not tt.is_comma_and or tt.is_newline_before): 
                    break
                tt = tt.next0_
                if (not (isinstance(tt, NumberToken))): 
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
                if (tt.int_value is not None and tt.int_value > 1970): 
                    break
                if (tt.is_whitespace_after): 
                    pass
                elif (not tt.next0_.is_char_of(",.")): 
                    pass
                else: 
                    break
                tmp = io.StringIO()
                tee = DecreeToken.__try_attach_number(tt, tmp, True)
                if (res.children is None): 
                    res.children = list()
                add = DecreeToken._new845(tt, tee, DecreeToken.ItemType.NUMBER, Utils.toStringStringIO(tmp))
                res.children.append(add)
                tt = tee
                res.end_token = tt
        if (res.typ != DecreeToken.ItemType.TYP): 
            return res
        if (res.begin_token == res.end_token): 
            tok = DecreeToken.M_TERMINS.try_parse(res.begin_token.previous, TerminParseAttr.NO)
            if (tok is not None and (isinstance(tok.termin.tag, DecreeToken.ItemType)) and tok.end_token == res.end_token): 
                if ((Utils.valToEnum(tok.termin.tag, DecreeToken.ItemType)) == DecreeToken.ItemType.TYP): 
                    return None
        if (((prev is not None and prev.typ == DecreeToken.ItemType.TYP and prev.value is not None) and (("ДОГОВОР" in prev.value or "ДОГОВІР" in prev.value)) and res.value is not None) and not "ДОГОВОР" in res.value and not "ДОГОВІР" in res.value): 
            return None
        for e0_ in DecreeToken.M_EMPTY_ADJECTIVES: 
            if (t.is_value(e0_, None)): 
                res = DecreeToken.__try_attach(t.next0_, prev, 0, False)
                if (res is None or res.typ != DecreeToken.ItemType.TYP): 
                    return None
                break
        if (res.end_token.next0_ is not None and res.end_token.next0_.is_char('(')): 
            res1 = DecreeToken.__try_attach(res.end_token.next0_, prev, 0, False)
            if (res1 is not None and res1.end_token.is_char(')')): 
                if (res1.value == res.value and res.typ == DecreeToken.ItemType.TYP): 
                    res.end_token = res1.end_token
                elif (res.value == "ЕДИНЫЙ ОТРАСЛЕВОЙ СТАНДАРТ ЗАКУПОК" and res1.value is not None and res1.value.startswith("ПОЛОЖЕНИЕ О ЗАКУПК")): 
                    res.end_token = res1.end_token
        if (res.value is not None and " " in res.value): 
            for s in DecreeToken.M_ALL_TYPESRU: 
                if (s in res.value and res.value != s): 
                    if (s == "КОДЕКС"): 
                        res.full_value = res.value
                        res.value = s
                        break
        if (res.value == "КОДЕКС" and res.full_value is None): 
            t1 = res.end_token
            tt = t1.next0_
            while tt is not None: 
                if (tt.is_newline_before): 
                    break
                cha = DecreeChangeToken.try_attach(tt, None, False, None, False)
                if (cha is not None): 
                    break
                if (tt == t1.next0_ and res.begin_token.previous is not None and res.begin_token.previous.is_value("НАСТОЯЩИЙ", "СПРАВЖНІЙ")): 
                    break
                if (not (isinstance(tt, TextToken))): 
                    break
                if (tt == t1.next0_ and tt.is_value("ЗАКОН", None)): 
                    if (tt.next0_ is not None and ((tt.next0_.is_value("О", None) or tt.next0_.is_value("ПРО", None)))): 
                        npt0 = NounPhraseHelper.try_parse(tt.next0_.next0_, NounPhraseParseAttr.NO, 0, None)
                        if (npt0 is None or not npt0.morph.case_.is_prepositional): 
                            break
                        t1 = npt0.end_token
                        break
                ooo = False
                if (tt.morph.class0_.is_preposition and tt.next0_ is not None): 
                    if (tt.is_value("ПО", None)): 
                        tt = tt.next0_
                    elif (tt.is_value("О", None) or tt.is_value("ОБ", None) or tt.is_value("ПРО", None)): 
                        ooo = True
                        tt = tt.next0_
                npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                if (npt is None): 
                    break
                if (tt == t1.next0_ and npt.morph.case_.is_genitive): 
                    tt = npt.end_token
                    t1 = tt
                elif (ooo and npt.morph.case_.is_prepositional): 
                    tt = npt.end_token
                    t1 = tt
                    ttt = tt.next0_
                    while ttt is not None: 
                        if (not ttt.is_comma_and): 
                            break
                        npt = NounPhraseHelper.try_parse(ttt.next0_, NounPhraseParseAttr.NO, 0, None)
                        if (npt is None or not npt.morph.case_.is_prepositional): 
                            break
                        tt = npt.end_token
                        t1 = tt
                        if (ttt.is_and): 
                            break
                        ttt = npt.end_token
                        ttt = ttt.next0_
                else: 
                    break
                tt = tt.next0_
            if (t1 != res.end_token): 
                res.end_token = t1
                res.full_value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
        if (res.value is not None and ((res.value.startswith("ВЕДОМОСТИ СЪЕЗДА") or res.value.startswith("ВІДОМОСТІ ЗЇЗДУ")))): 
            tt = res.end_token.next0_
            if (tt is not None and (isinstance(tt.get_referent(), GeoReferent))): 
                res.ref = (Utils.asObjectOrNull(tt, ReferentToken))
                res.end_token = tt
                tt = tt.next0_
            if (tt is not None and tt.is_and): 
                tt = tt.next0_
            if (tt is not None and (isinstance(tt.get_referent(), OrganizationReferent))): 
                res.end_token = tt
                tt = tt.next0_
        return res
    
    @staticmethod
    def __try_attach(t : 'Token', prev : 'DecreeToken', lev : int, must_by_typ : bool=False) -> 'DecreeToken':
        if (t is None or lev > 4): 
            return None
        if (prev is not None and prev.typ == DecreeToken.ItemType.TYP): 
            while t.is_char_of(":-") and t.next0_ is not None and not t.is_newline_after:
                t = t.next0_
        if (prev is not None): 
            if (t.is_value("ПРИ", "ЗА") and t.next0_ is not None): 
                t = t.next0_
        if ((not must_by_typ and t.is_value("МЕЖДУ", "МІЖ") and (isinstance(t.next0_, ReferentToken))) and t.next0_.next0_ is not None): 
            t11 = t.next0_.next0_
            is_br = False
            if ((t11.is_char('(') and (isinstance(t11.next0_, TextToken)) and t11.next0_.next0_ is not None) and t11.next0_.next0_.is_char(')')): 
                t11 = t11.next0_.next0_.next0_
                is_br = True
            if (t11 is not None and t11.is_comma_and and (isinstance(t11.next0_, ReferentToken))): 
                rr = DecreeToken._new842(t, t11.next0_, DecreeToken.ItemType.BETWEEN)
                rr.children = list()
                rr.children.append(DecreeToken._new847(t.next0_, t.next0_, DecreeToken.ItemType.OWNER, Utils.asObjectOrNull(t.next0_, ReferentToken)))
                rr.children.append(DecreeToken._new847(t11.next0_, t11.next0_, DecreeToken.ItemType.OWNER, Utils.asObjectOrNull(t11.next0_, ReferentToken)))
                t = rr.end_token.next0_
                first_pass3589 = True
                while True:
                    if first_pass3589: first_pass3589 = False
                    else: t = t.next0_
                    if (not (t is not None)): break
                    if ((is_br and t.is_char('(') and (isinstance(t.next0_, TextToken))) and t.next0_.next0_ is not None and t.next0_.next0_.is_char(')')): 
                        t = t.next0_.next0_
                        rr.end_token = t
                        rr.children[len(rr.children) - 1].end_token = t
                        continue
                    if ((t.is_comma_and and t.next0_ is not None and (isinstance(t.next0_, ReferentToken))) and not (isinstance(t.next0_.get_referent(), DateReferent))): 
                        rr.children.append(DecreeToken._new847(t.next0_, t.next0_, DecreeToken.ItemType.OWNER, Utils.asObjectOrNull(t.next0_, ReferentToken)))
                        rr.end_token = t.next0_
                        t = rr.end_token
                        continue
                    break
                return rr
        r = t.get_referent()
        if (isinstance(r, OrganizationReferent)): 
            rt = Utils.asObjectOrNull(t, ReferentToken)
            org0_ = Utils.asObjectOrNull(r, OrganizationReferent)
            res1 = None
            if (org0_.contains_profile(OrgProfile.MEDIA)): 
                tt1 = rt.begin_token
                if (BracketHelper.can_be_start_of_sequence(tt1, False, False)): 
                    tt1 = tt1.next0_
                res1 = DecreeToken.__try_attach(tt1, prev, lev + 1, False)
                if (res1 is not None and res1.typ == DecreeToken.ItemType.TYP): 
                    res1.begin_token = res1.end_token = t
                else: 
                    res1 = (None)
            if (res1 is None and org0_.contains_profile(OrgProfile.PRESS)): 
                res1 = DecreeToken._new842(t, t, DecreeToken.ItemType.TYP)
                res1.value = MiscHelper.get_text_value_of_meta_token(Utils.asObjectOrNull(t, ReferentToken), GetTextAttr.NO)
            if (res1 is not None): 
                t11 = res1.end_token
                if (isinstance(t11.get_referent(), GeoReferent)): 
                    res1.ref = (Utils.asObjectOrNull(t11, ReferentToken))
                elif (isinstance(t11, MetaToken)): 
                    t11 = t11.end_token
                if (isinstance(t11.get_referent(), GeoReferent)): 
                    res1.ref = (Utils.asObjectOrNull(t11, ReferentToken))
                elif (BracketHelper.is_bracket(t11, False) and (isinstance(t11.previous.get_referent(), GeoReferent))): 
                    res1.ref = (Utils.asObjectOrNull(t11.previous, ReferentToken))
                return res1
        if (r is not None and not must_by_typ): 
            if (isinstance(r, GeoReferent)): 
                return DecreeToken._new851(t, t, DecreeToken.ItemType.TERR, Utils.asObjectOrNull(t, ReferentToken), r.to_string(True, t.kit.base_language, 0))
            if (isinstance(r, DateReferent)): 
                if (prev is not None and prev.typ == DecreeToken.ItemType.TYP and prev.typ_kind == DecreeKind.STANDARD): 
                    ree = DecreeToken.try_attach(t.begin_token, prev, False)
                    if ((ree is not None and ree.typ == DecreeToken.ItemType.NUMBER and ree.num_year > 0) and ((ree.end_token == t.end_token or ree.end_token.is_char('*')))): 
                        if ((isinstance(t.next0_, TextToken)) and t.next0_.is_char('*')): 
                            t = t.next0_
                        ree.begin_token = ree.end_token = t
                        return ree
                if (t.previous is not None and t.previous.morph.class0_.is_preposition and t.previous.is_value("ДО", None)): 
                    return None
                return DecreeToken._new847(t, t, DecreeToken.ItemType.DATE, Utils.asObjectOrNull(t, ReferentToken))
            if (isinstance(r, OrganizationReferent)): 
                if ((t.next0_ is not None and t.next0_.is_value("В", "У") and t.next0_.next0_ is not None) and t.next0_.next0_.is_value("СОСТАВ", "СКЛАДІ")): 
                    return None
                return DecreeToken._new851(t, t, DecreeToken.ItemType.ORG, Utils.asObjectOrNull(t, ReferentToken), str(r))
            if (isinstance(r, PersonReferent)): 
                ok = False
                if (prev is not None and ((prev.typ == DecreeToken.ItemType.TYP or prev.typ == DecreeToken.ItemType.DATE))): 
                    ok = True
                elif (t.next0_ is not None and (isinstance(t.next0_.get_referent(), DecreeReferent))): 
                    ok = True
                else: 
                    ne = DecreeToken.__try_attach(t.next0_, None, lev + 1, False)
                    if (ne is not None and ((ne.typ == DecreeToken.ItemType.TYP or ne.typ == DecreeToken.ItemType.DATE or ne.typ == DecreeToken.ItemType.OWNER))): 
                        ok = True
                if (ok): 
                    prop = Utils.asObjectOrNull(r.get_slot_value(PersonReferent.ATTR_ATTR), PersonPropertyReferent)
                    if (prop is not None and ((prop.kind == PersonPropertyKind.BOSS or (Utils.ifNotNull(prop.name, "")).startswith("глава")))): 
                        return DecreeToken._new847(t, t, DecreeToken.ItemType.OWNER, ReferentToken(prop, t, t))
            if (isinstance(r, PersonPropertyReferent)): 
                return DecreeToken._new847(t, t, DecreeToken.ItemType.OWNER, ReferentToken(r, t, t))
            if (isinstance(r, DenominationReferent)): 
                s = str(r)
                if (len(s) > 1 and ((s[0] == 'A' or s[0] == 'А')) and str.isdigit(s[1])): 
                    return DecreeToken._new845(t, t, DecreeToken.ItemType.NUMBER, s)
            return None
        if (not must_by_typ): 
            tdat = None
            if (t.is_value("ОТ", "ВІД") or t.is_value("ПРИНЯТЬ", "ПРИЙНЯТИ")): 
                tdat = t.next0_
            elif (t.is_value("ВВЕСТИ", None) or t.is_value("ВВОДИТЬ", "ВВОДИТИ")): 
                tdat = t.next0_
                if (tdat is not None and tdat.is_value("В", "У")): 
                    tdat = tdat.next0_
                if (tdat is not None and tdat.is_value("ДЕЙСТВИЕ", "ДІЯ")): 
                    tdat = tdat.next0_
            if (tdat is not None): 
                if (tdat.next0_ is not None and tdat.morph.class0_.is_preposition): 
                    tdat = tdat.next0_
                if (isinstance(tdat.get_referent(), DateReferent)): 
                    return DecreeToken._new847(t, tdat, DecreeToken.ItemType.DATE, Utils.asObjectOrNull(tdat, ReferentToken))
                dr = t.kit.process_referent("DATE", tdat)
                if (dr is not None): 
                    return DecreeToken._new847(t, dr.end_token, DecreeToken.ItemType.DATE, dr)
            if (t.is_value("НА", None) and t.next0_ is not None and (isinstance(t.next0_.get_referent(), DateRangeReferent))): 
                return DecreeToken._new847(t, t.next0_, DecreeToken.ItemType.DATERANGE, Utils.asObjectOrNull(t.next0_, ReferentToken))
            if (t.is_char('(')): 
                tt = DecreeToken.__is_edition(t.next0_)
                if (tt is not None): 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        return DecreeToken._new842(t, br.end_token, DecreeToken.ItemType.EDITION)
                if (t.next0_ is not None and t.next0_.is_value("ПРОЕКТ", None)): 
                    return DecreeToken._new845(t.next0_, t.next0_, DecreeToken.ItemType.TYP, "ПРОЕКТ")
                if ((t.next0_ is not None and (isinstance(t.next0_.get_referent(), DateRangeReferent)) and t.next0_.next0_ is not None) and t.next0_.next0_.is_char(')')): 
                    return DecreeToken._new847(t, t.next0_.next0_, DecreeToken.ItemType.DATERANGE, Utils.asObjectOrNull(t.next0_, ReferentToken))
            else: 
                tt = DecreeToken.__is_edition(t)
                if (tt is not None): 
                    tt = tt.next0_
                if (tt is not None): 
                    xxx = DecreeToken.try_attach(tt, None, False)
                    if (xxx is not None): 
                        return DecreeToken._new842(t, tt.previous, DecreeToken.ItemType.EDITION)
            if (isinstance(t, NumberToken)): 
                if (prev is not None and ((prev.typ == DecreeToken.ItemType.TYP or prev.typ == DecreeToken.ItemType.DATE))): 
                    tmp = io.StringIO()
                    t11 = DecreeToken.__try_attach_number(t, tmp, False)
                    if (t11 is not None): 
                        ne = DecreeToken.__try_attach(t11.next0_, None, lev + 1, False)
                        valnum = Utils.toStringStringIO(tmp)
                        if (ne is not None and ((ne.typ == DecreeToken.ItemType.DATE or ne.typ == DecreeToken.ItemType.OWNER or ne.typ == DecreeToken.ItemType.NAME))): 
                            return DecreeToken._new845(t, t11, DecreeToken.ItemType.NUMBER, valnum)
                        if (LanguageHelper.ends_with_ex(valnum, "ФЗ", "ФКЗ", None, None)): 
                            return DecreeToken._new845(t, t11, DecreeToken.ItemType.NUMBER, valnum)
                        year = 0
                        if (prev.typ == DecreeToken.ItemType.TYP): 
                            ok = False
                            if (prev.typ_kind == DecreeKind.STANDARD): 
                                ok = True
                                if (t11.next0_ is not None and t11.next0_.is_char('*')): 
                                    t11 = t11.next0_
                                if (Utils.endsWithString(valnum, "(E)", True)): 
                                    valnum = valnum[0:0+len(valnum) - 3].strip()
                                while True:
                                    if ((t11.whitespaces_after_count < 2) and (isinstance(t11.next0_, NumberToken))): 
                                        Utils.setLengthStringIO(tmp, 0)
                                        t22 = DecreeToken.__try_attach_number(t11.next0_, tmp, False)
                                        if (t22 is None): 
                                            break
                                        valnum = "{0}.{1}".format(valnum, Utils.toStringStringIO(tmp))
                                        t11 = t22
                                    else: 
                                        break
                                for ii in range(len(valnum) - 1, -1, -1):
                                    if (not str.isdigit(valnum[ii])): 
                                        if (ii == len(valnum) or ii == 0): 
                                            break
                                        if ((valnum[ii] != '-' and valnum[ii] != ':' and valnum[ii] != '.') and valnum[ii] != '/' and valnum[ii] != '\\'): 
                                            break
                                        nn = 0
                                        ss = valnum[ii + 1:]
                                        if (len(ss) != 2 and len(ss) != 4): 
                                            break
                                        if (ss[0] == '0' and len(ss) == 2): 
                                            nn = (2000 + (((ord(ss[1])) - (ord('0')))))
                                        else: 
                                            wrapnn866 = RefOutArgWrapper(0)
                                            inoutres867 = Utils.tryParseInt(ss, wrapnn866)
                                            nn = wrapnn866.value
                                            if (inoutres867): 
                                                if (nn > 50 and nn <= 99): 
                                                    nn += 1900
                                                elif (len(ss) == 2 and (((2000 + nn) <= datetime.datetime.now().year))): 
                                                    nn += 2000
                                        if (nn >= 1950 and nn <= datetime.datetime.now().year): 
                                            year = nn
                                            valnum = valnum[0:0+ii]
                                        break
                                valnum = valnum.replace('-', '.')
                                if (year < 1): 
                                    if (t11.next0_ is not None and t11.next0_.is_hiphen): 
                                        if ((isinstance(t11.next0_.next0_, NumberToken)) and t11.next0_.next0_.int_value is not None): 
                                            nn = t11.next0_.next0_.int_value
                                            if (nn > 50 and nn <= 99): 
                                                nn += 1900
                                            if (nn >= 1950 and nn <= datetime.datetime.now().year): 
                                                year = nn
                                                t11 = t11.next0_.next0_
                            elif (prev.begin_token == prev.end_token and prev.begin_token.chars.is_all_upper and ((prev.begin_token.is_value("ФЗ", None) or prev.begin_token.is_value("ФКЗ", None)))): 
                                ok = True
                            if (ok): 
                                return DecreeToken._new868(t, t11, DecreeToken.ItemType.NUMBER, valnum, year)
                    if (t.int_value is not None): 
                        val = t.int_value
                        if (val > 1910 and (val < 2030)): 
                            return DecreeToken._new845(t, t, DecreeToken.ItemType.DATE, str(val))
                rt = t.kit.process_referent("PERSON", t)
                if (rt is not None): 
                    pr = Utils.asObjectOrNull(rt.referent, PersonPropertyReferent)
                    if (pr is not None): 
                        return DecreeToken._new870(rt.begin_token, rt.end_token, DecreeToken.ItemType.OWNER, rt, rt.morph)
                if (t.next0_ is not None and t.next0_.chars.is_letter): 
                    res1 = DecreeToken.__try_attach(t.next0_, prev, lev + 1, False)
                    if (res1 is not None and res1.typ == DecreeToken.ItemType.OWNER): 
                        res1.begin_token = t
                        return res1
        toks = None
        if (not (isinstance(t, TextToken))): 
            if ((isinstance(t, NumberToken)) and t.value == "100"): 
                if (t.begin_token.is_value("СТО", None) and t.begin_token.chars.is_all_upper): 
                    toks = DecreeToken.M_TERMINS.try_parse_all(t.begin_token, TerminParseAttr.NO)
                    if (toks is not None and len(toks) == 1): 
                        toks[0].begin_token = toks[0].end_token = t
            if (toks is None): 
                return None
        else: 
            toks = DecreeToken.M_TERMINS.try_parse_all(t, TerminParseAttr.NO)
        if (toks is not None): 
            for tok in toks: 
                if (tok.end_token.is_char('.') and tok.begin_token != tok.end_token): 
                    tok.end_token = tok.end_token.previous
                if (tok.termin.canonic_text == "РЕГИСТРАЦИЯ" or tok.termin.canonic_text == "РЕЄСТРАЦІЯ"): 
                    if (tok.end_token.next0_ is not None and ((tok.end_token.next0_.is_value("В", None) or tok.end_token.next0_.is_value("ПО", None)))): 
                        tok.end_token = tok.end_token.next0_
                doubt = False
                if ((tok.end_char - tok.begin_char) < 3): 
                    if (t.is_value("СП", None)): 
                        if (not (isinstance(t.next0_, NumberToken))): 
                            if (MiscHelper.check_number_prefix(t.next0_) is None): 
                                return None
                    doubt = True
                    if (tok.end_token.next0_ is None or not tok.chars.is_all_upper): 
                        pass
                    else: 
                        r = tok.end_token.next0_.get_referent()
                        if (isinstance(r, GeoReferent)): 
                            doubt = False
                if (tok.begin_token == tok.end_token and (tok.length_char < 4) and len(toks) > 1): 
                    cou = 0
                    tt = t.previous
                    first_pass3590 = True
                    while True:
                        if first_pass3590: first_pass3590 = False
                        else: tt = tt.previous; cou += 1
                        if (not (tt is not None and (cou < 500))): break
                        dr = Utils.asObjectOrNull(tt.get_referent(), DecreeReferent)
                        if (dr is None): 
                            continue
                        for tok1 in toks: 
                            if (dr.find_slot(DecreeReferent.ATTR_NAME, tok1.termin.canonic_text, True) is not None): 
                                return DecreeToken._new871(tok.begin_token, tok.end_token, Utils.valToEnum(tok1.termin.tag, DecreeToken.ItemType), tok1.termin.canonic_text, tok1.morph)
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
                        tt = t.next0_
                        while tt is not None and (cou < 500): 
                            if (tt.is_value("ТАМОЖНЯ", None) or tt.is_value("ТАМОЖЕННЫЙ", None) or tt.is_value("ГРАНИЦА", None)): 
                                has_tamoz = True
                                break
                            tt = tt.next0_; cou += 1
                        if (has_tamoz): 
                            continue
                if (doubt and tok.chars.is_all_upper): 
                    if (PartToken.is_part_before(tok.begin_token)): 
                        doubt = False
                    elif (tok.get_source_text().endswith("ТС")): 
                        doubt = False
                res = DecreeToken._new872(tok.begin_token, tok.end_token, Utils.valToEnum(tok.termin.tag, DecreeToken.ItemType), tok.termin.canonic_text, tok.morph, doubt)
                if (isinstance(tok.termin.tag2, DecreeKind)): 
                    res.typ_kind = (Utils.valToEnum(tok.termin.tag2, DecreeKind))
                if (res.value == "ГОСТ" and tok.end_token.next0_ is not None): 
                    if (tok.end_token.next0_.is_value("Р", None) or tok.end_token.next0_.is_value("P", None)): 
                        res.end_token = tok.end_token.next0_
                    else: 
                        g = Utils.asObjectOrNull(tok.end_token.next0_.get_referent(), GeoReferent)
                        if (g is not None and ((g.alpha2 == "RU" or g.alpha2 == "SU"))): 
                            res.end_token = tok.end_token.next0_
                if (res.value == "КОНСТИТУЦИЯ" and tok.end_token.next0_ is not None and tok.end_token.next0_.is_char('(')): 
                    npt = NounPhraseHelper.try_parse(tok.end_token.next0_.next0_, NounPhraseParseAttr.NO, 0, None)
                    if ((npt is not None and npt.end_token.is_value("ЗАКОН", None) and npt.end_token.next0_ is not None) and npt.end_token.next0_.is_char(')')): 
                        res.end_token = npt.end_token.next0_
                if ((isinstance(tok.termin.tag2, str)) and res.typ == DecreeToken.ItemType.TYP): 
                    res.full_value = tok.termin.canonic_text
                    res.value = (Utils.asObjectOrNull(tok.termin.tag2, str))
                    res.is_doubtful = False
                if (res.typ_kind == DecreeKind.STANDARD): 
                    cou = 0
                    tt = res.end_token.next0_
                    first_pass3591 = True
                    while True:
                        if first_pass3591: first_pass3591 = False
                        else: tt = tt.next0_; cou += 1
                        if (not (tt is not None and (cou < 3))): break
                        if (tt.whitespaces_before_count > 2): 
                            break
                        tok2 = DecreeToken.M_TERMINS.try_parse(tt, TerminParseAttr.NO)
                        if (tok2 is not None): 
                            if ((isinstance(tok2.termin.tag2, DecreeKind)) and (Utils.valToEnum(tok2.termin.tag2, DecreeKind)) == DecreeKind.STANDARD): 
                                res.end_token = tok2.end_token
                                tt = res.end_token
                                res.is_doubtful = False
                                if (res.value == "СТАНДАРТ"): 
                                    res.value = tok2.termin.canonic_text
                                continue
                        if ((isinstance(tt, TextToken)) and (tt.length_char < 4) and tt.chars.is_all_upper): 
                            res.end_token = tt
                            continue
                        if (((tt.is_char_of("/\\") or tt.is_hiphen)) and (isinstance(tt.next0_, TextToken)) and tt.next0_.chars.is_all_upper): 
                            tt = tt.next0_
                            res.end_token = tt
                            continue
                        break
                    if (res.value == "СТАНДАРТ"): 
                        res.is_doubtful = True
                    if (res.is_doubtful and not res.is_newline_after): 
                        num1 = DecreeToken.try_attach(res.end_token.next0_, res, False)
                        if (num1 is not None and num1.typ == DecreeToken.ItemType.NUMBER): 
                            if (num1.num_year > 0): 
                                res.is_doubtful = False
                    if (res.value == "СТАНДАРТ" and res.is_doubtful): 
                        return None
                return res
        if (((t.morph.class0_.is_adjective and ((t.is_value("УКАЗАННЫЙ", "ЗАЗНАЧЕНИЙ") or t.is_value("ВЫШЕУКАЗАННЫЙ", "ВИЩЕВКАЗАНИЙ") or t.is_value("НАЗВАННЫЙ", "НАЗВАНИЙ"))))) or ((t.morph.class0_.is_pronoun and (((t.is_value("ЭТОТ", "ЦЕЙ") or t.is_value("ТОТ", "ТОЙ") or t.is_value("ДАННЫЙ", "ДАНИЙ")) or t.is_value("САМЫЙ", "САМИЙ")))))): 
            t11 = t.next0_
            if (t11 is not None and t11.is_value("ЖЕ", None)): 
                t11 = t11.next0_
            nnn = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            tok = DecreeToken.M_TERMINS.try_parse(t11, TerminParseAttr.NO)
            if ((tok) is not None): 
                if (((tok.morph.number) & (MorphNumber.PLURAL)) == (MorphNumber.UNDEFINED) or ((nnn is not None and nnn.morph.number == MorphNumber.SINGULAR))): 
                    npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None and ((npt.morph.number) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                        pass
                    else: 
                        te = DecreeToken._find_back_typ(t.previous, tok.termin.canonic_text)
                        if (te is not None): 
                            return DecreeToken._new847(t, tok.end_token, DecreeToken.ItemType.DECREEREF, te)
        if (t.morph.class0_.is_adjective and t.is_value("НАСТОЯЩИЙ", "СПРАВЖНІЙ")): 
            tok = DecreeToken.M_TERMINS.try_parse(t.next0_, TerminParseAttr.NO)
            if ((tok) is not None): 
                return DecreeToken._new847(t, tok.end_token, DecreeToken.ItemType.DECREEREF, None)
        if (must_by_typ): 
            return None
        if ((((isinstance(t, TextToken)) and prev is not None and prev.typ == DecreeToken.ItemType.TYP) and t.chars.is_all_upper and t.length_char >= 2) and t.length_char <= 5): 
            if (((prev.value == "ТЕХНИЧЕСКИЕ УСЛОВИЯ" and t.next0_ is not None and t.next0_.is_char('.')) and (isinstance(t.next0_.next0_, NumberToken)) and t.next0_.next0_.next0_ is not None) and t.next0_.next0_.next0_.is_char('.') and (isinstance(t.next0_.next0_.next0_.next0_, NumberToken))): 
                res = DecreeToken._new845(t, t, DecreeToken.ItemType.NUMBER, t.term)
                t = t.next0_.next0_
                res.value = "{0}.{1}.{2}".format(res.value, t.get_source_text(), t.next0_.next0_.get_source_text())
                t = t.next0_.next0_
                res.end_token = t
                if ((t.whitespaces_after_count < 2) and t.next0_ is not None and t.next0_.is_value("ТУ", None)): 
                    res.end_token = res.end_token.next0_
                return res
        if ((((((isinstance(t, TextToken)) and t.length_char == 4 and t.chars.is_all_upper) and t.next0_ is not None and not t.is_whitespace_after) and t.next0_.is_char('.') and (isinstance(t.next0_.next0_, NumberToken))) and not t.next0_.is_whitespace_after and t.next0_.next0_.next0_ is not None) and t.next0_.next0_.next0_.is_char('.') and (isinstance(t.next0_.next0_.next0_.next0_, NumberToken))): 
            if (t.next0_.next0_.next0_.next0_.next0_ is not None and t.next0_.next0_.next0_.next0_.next0_.is_value("ТУ", None)): 
                res = DecreeToken._new845(t, t.next0_.next0_.next0_.next0_, DecreeToken.ItemType.NUMBER, t.term)
                res.value = "{0}.{1}.{2}".format(t.get_source_text(), t.next0_.next0_.get_source_text(), t.next0_.next0_.next0_.next0_.get_source_text())
                return res
        if (t.morph.class0_.is_adjective): 
            dt = DecreeToken.__try_attach(t.next0_, prev, lev + 1, False)
            if (dt is not None and dt.ref is None): 
                rt = t.kit.process_referent("GEO", t)
                if (rt is not None): 
                    dt.ref = rt
                    dt.begin_token = t
                    return dt
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None and npt.internal_noun is not None): 
                npt = (None)
            if ((npt is not None and dt is not None and dt.typ == DecreeToken.ItemType.TYP) and dt.value == "КОДЕКС"): 
                dt.value = npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                dt.begin_token = t
                dt.is_doubtful = True
                return dt
            if (npt is not None and ((npt.end_token.is_value("ДОГОВОР", None) or npt.end_token.is_value("КОНТРАКТ", None)))): 
                dt = DecreeToken._new842(t, npt.end_token, DecreeToken.ItemType.TYP)
                dt.value = npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                if (t.get_morph_class_in_dictionary().is_verb): 
                    dt.value = npt.end_token.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                return dt
            try_npt = False
            if (not t.chars.is_all_lower): 
                try_npt = True
            else: 
                for a in DecreeToken.M_STD_ADJECTIVES: 
                    if (t.is_value(a, None)): 
                        try_npt = True
                        break
            if (try_npt): 
                if (npt is not None): 
                    if (npt.end_token.is_value("ГАЗЕТА", None) or npt.end_token.is_value("БЮЛЛЕТЕНЬ", "БЮЛЕТЕНЬ")): 
                        return DecreeToken._new871(t, npt.end_token, DecreeToken.ItemType.TYP, npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), npt.morph)
                    if (len(npt.adjectives) > 0 and npt.end_token.get_morph_class_in_dictionary().is_noun): 
                        tok = DecreeToken.M_TERMINS.try_parse(npt.end_token, TerminParseAttr.NO)
                        if ((tok) is not None): 
                            if (npt.begin_token.is_value("ОБЩИЙ", "ЗАГАЛЬНИЙ")): 
                                return None
                            return DecreeToken._new879(npt.begin_token, tok.end_token, npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False), npt.morph)
                    if (prev is not None and prev.typ == DecreeToken.ItemType.TYP): 
                        if (npt.end_token.is_value("КОЛЛЕГИЯ", "КОЛЕГІЯ")): 
                            res1 = DecreeToken._new871(t, npt.end_token, DecreeToken.ItemType.OWNER, npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), npt.morph)
                            t = npt.end_token.next0_
                            first_pass3592 = True
                            while True:
                                if first_pass3592: first_pass3592 = False
                                else: t = t.next0_
                                if (not (t is not None)): break
                                if (t.is_and or t.morph.class0_.is_preposition): 
                                    continue
                                re = t.get_referent()
                                if ((isinstance(re, GeoReferent)) or (isinstance(re, OrganizationReferent))): 
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
                                npt1 = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                                if (npt1 is None): 
                                    break
                                res1.end_token = npt1.end_token
                                t = res1.end_token
                            if (res1.end_token != npt.end_token): 
                                res1.value = "{0} {1}".format(res1.value, MiscHelper.get_text_value(npt.end_token.next0_, res1.end_token, GetTextAttr.KEEPQUOTES))
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
            if ((t1.whitespaces_before_count < 15) and ((not t1.is_newline_before or (isinstance(t1, NumberToken)) or DecreeToken.__is_jus_number(t1)))): 
                tmp = io.StringIO()
                t11 = DecreeToken.__try_attach_number(t1, tmp, num)
                if (t11 is not None): 
                    if (t11.next0_ is not None and t11.next0_.is_value("ДСП", None)): 
                        t11 = t11.next0_
                        print("ДСП", end="", file=tmp)
                    return DecreeToken._new845(t0, t11, DecreeToken.ItemType.NUMBER, Utils.toStringStringIO(tmp))
            if (t1.is_newline_before and num): 
                return DecreeToken._new842(t0, t1.previous, DecreeToken.ItemType.NUMBER)
        if (BracketHelper.can_be_start_of_sequence(t, False, False)): 
            if (BracketHelper.can_be_start_of_sequence(t, True, False) and ((((t.next0_.is_value("О", None) or t.next0_.is_value("ОБ", None) or t.next0_.is_value("ПРО", None)) or t.next0_.is_value("ПО", None) or t.chars.is_capital_upper) or ((prev is not None and (isinstance(t.next0_, TextToken)) and ((prev.typ == DecreeToken.ItemType.DATE or prev.typ == DecreeToken.ItemType.NUMBER))))))): 
                br = BracketHelper.try_parse(t, BracketParseAttr.CANCONTAINSVERBS, 200)
                if (br is not None): 
                    tt = br.end_token
                    if (tt.previous is not None and tt.previous.is_char('>')): 
                        tt = tt.previous
                    if ((tt.is_char('>') and (isinstance(tt.previous, NumberToken)) and tt.previous.previous is not None) and tt.previous.previous.is_char('<')): 
                        tt = tt.previous.previous.previous
                        if (tt is None or tt.begin_char <= br.begin_char): 
                            return None
                        br.end_token = tt
                    tt1 = DecreeToken._try_attach_std_change_name(t.next0_)
                    if (tt1 is not None and tt1.end_char > br.end_char): 
                        br.end_token = tt1
                    else: 
                        tt = br.begin_token.next0_
                        while tt is not None and (tt.end_char < br.end_char): 
                            if (tt.is_char('(')): 
                                dt = DecreeToken.try_attach(tt.next0_, None, False)
                                if (dt is None and BracketHelper.can_be_start_of_sequence(tt.next0_, True, False)): 
                                    dt = DecreeToken.try_attach(tt.next0_.next0_, None, False)
                                if (dt is not None and dt.typ == DecreeToken.ItemType.TYP): 
                                    if (DecreeToken.get_kind(dt.value) == DecreeKind.PUBLISHER): 
                                        br.end_token = tt.previous
                                        break
                            tt = tt.next0_
                    return DecreeToken._new845(br.begin_token, br.end_token, DecreeToken.ItemType.NAME, MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO))
                else: 
                    tt1 = DecreeToken._try_attach_std_change_name(t.next0_)
                    if (tt1 is not None): 
                        return DecreeToken._new845(t, tt1, DecreeToken.ItemType.NAME, MiscHelper.get_text_value(t, tt1, GetTextAttr.NO))
            elif (t.is_char('(')): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    if (not t.next0_.is_value("ДАЛЕЕ", "ДАЛІ")): 
                        if ((br.end_char - br.begin_char) < 30): 
                            return DecreeToken._new845(br.begin_token, br.end_token, DecreeToken.ItemType.MISC, MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO))
        if (t.inner_bool): 
            rt = t.kit.process_referent("PERSON", t)
            if (rt is not None): 
                pr = Utils.asObjectOrNull(rt.referent, PersonPropertyReferent)
                if (pr is None): 
                    return None
                if (pr.kind != PersonPropertyKind.UNDEFINED): 
                    pass
                elif (Utils.startsWithString(pr.name, "ГРАЖДАН", True) or Utils.startsWithString(pr.name, "ГРОМАДЯН", True)): 
                    return None
                return DecreeToken._new870(rt.begin_token, rt.end_token, DecreeToken.ItemType.OWNER, rt, rt.morph)
        if (t.is_value("О", None) or t.is_value("ОБ", None) or t.is_value("ПРО", None)): 
            et = None
            if ((t.next0_ is not None and t.next0_.is_value("ВНЕСЕНИЕ", "ВНЕСЕННЯ") and t.next0_.next0_ is not None) and t.next0_.next0_.is_value("ИЗМЕНЕНИЕ", "ЗМІНА")): 
                et = t.next0_
            elif (t.next0_ is not None and t.next0_.is_value("ПОПРАВКА", None)): 
                et = t.next0_
            elif (t.next0_ is not None and (isinstance(t.next0_.get_referent(), OrganizationReferent))): 
                et = t.next0_
            if (et is not None and et.next0_ is not None and et.next0_.morph.class0_.is_preposition): 
                et = et.next0_
            if (et is not None and et.next0_ is not None): 
                dts2 = DecreeToken.try_attach_list(et.next0_, None, 10, False)
                if (dts2 is not None and dts2[0].typ == DecreeToken.ItemType.TYP): 
                    et = dts2[0].end_token
                    if (len(dts2) > 1 and dts2[1].typ == DecreeToken.ItemType.TERR): 
                        et = dts2[1].end_token
                    return DecreeToken._new845(t, et, DecreeToken.ItemType.NAME, MiscHelper.get_text_value(t, et, GetTextAttr.NO))
                if (et.next0_.is_char_of(",(") or (isinstance(et, ReferentToken))): 
                    return DecreeToken._new845(t, et, DecreeToken.ItemType.NAME, MiscHelper.get_text_value(t, et, GetTextAttr.NO))
            elif (et is not None): 
                return DecreeToken._new845(t, et, DecreeToken.ItemType.NAME, MiscHelper.get_text_value(t, et, GetTextAttr.NO))
            return None
        if (t.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
            return None
        if (prev is not None and prev.typ == DecreeToken.ItemType.TYP): 
            if (t.is_value("ПРАВИТЕЛЬСТВО", "УРЯД") or t.is_value("ПРЕЗИДЕНТ", None)): 
                return DecreeToken._new890(t, t, DecreeToken.ItemType.OWNER, t.morph, t.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
        npt2 = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSEPREPOSITION, 0, None)
        if (npt2 is not None): 
            if (npt2.end_token.is_value("ПОЗИЦИЯ", None)): 
                return None
        if ((((t.chars.is_cyrillic_letter and ((not t.chars.is_all_lower or ((prev is not None and prev.typ == DecreeToken.ItemType.UNKNOWN))))) or t.is_value("ЗАСЕДАНИЕ", "ЗАСІДАННЯ") or t.is_value("СОБРАНИЕ", "ЗБОРИ")) or t.is_value("ПЛЕНУМ", None) or t.is_value("КОЛЛЕГИЯ", "КОЛЕГІЯ")) or t.is_value("АДМИНИСТРАЦИЯ", "АДМІНІСТРАЦІЯ")): 
            ok = False
            if (prev is not None and ((prev.typ == DecreeToken.ItemType.TYP or prev.typ == DecreeToken.ItemType.OWNER or prev.typ == DecreeToken.ItemType.ORG))): 
                if (not t.morph.class0_.is_preposition and not t.morph.class0_.is_conjunction): 
                    ok = True
            elif (prev is not None and prev.typ == DecreeToken.ItemType.UNKNOWN and not t.morph.class0_.is_verb): 
                ok = True
            elif (t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent)) and not t.is_value("ИМЕНЕМ", None)): 
                ok = True
            elif ((t.previous is not None and t.previous.is_char(',') and t.previous.previous is not None) and (isinstance(t.previous.previous.get_referent(), DecreeReferent))): 
                ok = True
            if (ok): 
                if (PartToken.try_attach(t, None, False, False) is not None): 
                    ok = False
            if (ok): 
                t1 = t
                ty = DecreeToken.ItemType.UNKNOWN
                tmp = io.StringIO()
                tt = t
                while tt is not None: 
                    if (not (isinstance(tt, TextToken))): 
                        org0_ = Utils.asObjectOrNull(tt.get_referent(), OrganizationReferent)
                        if (org0_ is not None and tt.previous == t1): 
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
                    npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                    if (tt.chars.is_all_lower and tt != t): 
                        if (npt is not None and npt.morph.case_.is_genitive): 
                            pass
                        else: 
                            break
                    if (npt is not None): 
                        if (tmp.tell() > 0): 
                            print(" {0}".format(npt.get_source_text()), end="", file=tmp, flush=True)
                        else: 
                            print(npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), end="", file=tmp)
                        tt = npt.end_token
                        t1 = tt
                    elif (tmp.tell() > 0): 
                        print(" {0}".format(tt.get_source_text()), end="", file=tmp, flush=True)
                        t1 = tt
                    else: 
                        s = None
                        if (tt == t): 
                            s = tt.get_normal_case_text(MorphClass.NOUN, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                        if (s is None): 
                            s = tt.term
                        print(s, end="", file=tmp)
                        t1 = tt
                    tt = tt.next0_
                ss = MiscHelper.convert_first_char_upper_and_other_lower(Utils.toStringStringIO(tmp))
                return DecreeToken._new845(t, t1, ty, ss)
        if (t.is_value("ДАТА", None)): 
            t1 = t.next0_
            if (t1 is not None and t1.morph.case_.is_genitive): 
                t1 = t1.next0_
            if (t1 is not None and t1.is_char(':')): 
                t1 = t1.next0_
            res1 = DecreeToken.__try_attach(t1, prev, lev + 1, False)
            if (res1 is not None and res1.typ == DecreeToken.ItemType.DATE): 
                res1.begin_token = t
                return res1
        if (t.is_value("ВЕСТНИК", "ВІСНИК") or t.is_value("БЮЛЛЕТЕНЬ", "БЮЛЕТЕНЬ")): 
            npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                return DecreeToken._new845(t, npt.end_token, DecreeToken.ItemType.TYP, MiscHelper.get_text_value(t, npt.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE))
            elif (t.next0_ is not None and (isinstance(t.next0_.get_referent(), OrganizationReferent))): 
                return DecreeToken._new845(t, t.next0_, DecreeToken.ItemType.TYP, MiscHelper.get_text_value(t, t.next0_, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE))
        if ((prev is not None and prev.typ == DecreeToken.ItemType.TYP and prev.value is not None) and (("ДОГОВОР" in prev.value or "ДОГОВІР" in prev.value))): 
            nn = DecreeToken.try_attach_name(t, prev.value, False, False)
            if (nn is not None): 
                return nn
            t1 = (None)
            ttt = t
            first_pass3593 = True
            while True:
                if first_pass3593: first_pass3593 = False
                else: ttt = ttt.next0_
                if (not (ttt is not None)): break
                if (ttt.is_newline_before): 
                    break
                ddt1 = DecreeToken.__try_attach(ttt, None, lev + 1, False)
                if (ddt1 is not None): 
                    break
                if (ttt.morph.class0_.is_preposition or ttt.morph.class0_.is_conjunction): 
                    continue
                npt = NounPhraseHelper.try_parse(ttt, NounPhraseParseAttr.NO, 0, None)
                if (npt is None): 
                    break
                t1 = npt.end_token
                ttt = t1
            if (t1 is not None): 
                nn = DecreeToken._new842(t, t1, DecreeToken.ItemType.NAME)
                nn.value = MiscHelper.get_text_value(t, t1, GetTextAttr.NO)
                return nn
        if ((isinstance(t, TextToken)) and t.length_char == 1 and t.next0_ is not None): 
            if ((t.term == "Б" and t.next0_.is_char_of("\\/") and (isinstance(t.next0_.next0_, TextToken))) and t.next0_.next0_.term == "Н"): 
                return DecreeToken._new845(t, t.next0_.next0_, DecreeToken.ItemType.NUMBER, "Б/Н")
        return None
    
    @staticmethod
    def __is_jus_number(t : 'Token') -> bool:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return False
        if (tt.term != "A" and tt.term != "А"): 
            return False
        if ((isinstance(t.next0_, NumberToken)) and (t.whitespaces_after_count < 2)): 
            if (t.next0_.int_value is not None and t.next0_.int_value > 20): 
                return True
            return False
        return False
    
    @staticmethod
    def __is_edition(t : 'Token') -> 'Token':
        if (t is None): 
            return None
        if (t.morph.class0_.is_preposition and t.next0_ is not None): 
            t = t.next0_
        if (t.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ") or t.is_value("РЕД", None)): 
            if (t.next0_ is not None and t.next0_.is_char('.')): 
                return t.next0_
            else: 
                return t
        if (t.is_value("ИЗМЕНЕНИЕ", "ЗМІНА") or t.is_value("ИЗМ", None)): 
            if (t.next0_ is not None and t.next0_.is_char('.')): 
                t = t.next0_
            if ((t.next0_ is not None and t.next0_.is_comma and t.next0_.next0_ is not None) and t.next0_.next0_.is_value("ВНЕСЕННЫЙ", "ВНЕСЕНИЙ")): 
                return t.next0_.next0_
            return t
        if ((isinstance(t, NumberToken)) and t.next0_ is not None and t.next0_.is_value("ЧТЕНИЕ", "ЧИТАННЯ")): 
            return t.next0_.next0_
        return None
    
    @staticmethod
    def _find_back_typ(t : 'Token', type_name : str) -> 'ReferentToken':
        if (t is None): 
            return None
        if (t.is_value("НАСТОЯЩИЙ", "СПРАВЖНІЙ")): 
            return None
        cou = 0
        tt = t
        first_pass3594 = True
        while True:
            if first_pass3594: first_pass3594 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            cou += 1
            if (tt.is_newline_before): 
                cou += 10
            if (cou > 500): 
                break
            d = Utils.asObjectOrNull(tt.get_referent(), DecreeReferent)
            if (d is None and (isinstance(tt.get_referent(), DecreePartReferent))): 
                d = tt.get_referent().owner
            if (d is None): 
                continue
            if (d.typ0 == type_name or d.typ == type_name): 
                return Utils.asObjectOrNull(tt, ReferentToken)
        return None
    
    @staticmethod
    def __try_attach_number(t : 'Token', tmp : io.StringIO, after_num : bool) -> 'Token':
        t2 = t
        res = None
        digs = False
        br = False
        first_pass3595 = True
        while True:
            if first_pass3595: first_pass3595 = False
            else: t2 = t2.next0_
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
            if (not (isinstance(t2, NumberToken)) and not (isinstance(t2, TextToken))): 
                dr = Utils.asObjectOrNull(t2.get_referent(), DateReferent)
                if (dr is not None and not dr.is_relative and ((t2 == t or not t2.is_whitespace_before))): 
                    if (dr.year > 0 and t2.length_char == 4): 
                        res = t2
                        print(dr.year, end="", file=tmp)
                        digs = True
                        continue
                den = Utils.asObjectOrNull(t2.get_referent(), DenominationReferent)
                if (den is not None): 
                    res = t2
                    print(t2.get_source_text().upper(), end="", file=tmp)
                    for c in den.value: 
                        if (str.isdigit(c)): 
                            digs = True
                    if (t2.is_whitespace_after): 
                        break
                    continue
                if ((t2.length_char < 10) and after_num and not t2.is_whitespace_before): 
                    pass
                else: 
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
            if (str.isdigit(s[0])): 
                for d in s: 
                    digs = True
            if (not t2.is_char_of("_@")): 
                print(s, end="", file=tmp)
            res = t2
            if (t2.is_whitespace_after): 
                if (t2.whitespaces_after_count > 1): 
                    break
                if (digs): 
                    if ((t2.next0_ is not None and ((t2.next0_.is_hiphen or t2.next0_.is_char_of(".:"))) and not t2.next0_.is_whitespace_after) and (isinstance(t2.next0_.next0_, NumberToken))): 
                        continue
                if (not after_num): 
                    break
                if (t2.is_hiphen): 
                    if (t2.next0_ is not None and t2.next0_.is_value("СМ", None)): 
                        break
                    continue
                if (t2.is_char('/')): 
                    continue
                if (t2.next0_ is not None): 
                    if (((t2.next0_.is_hiphen or (isinstance(t2.next0_, NumberToken)))) and not digs): 
                        continue
                if (t2 == t and t2.chars.is_all_upper): 
                    continue
                if (isinstance(t2.next0_, NumberToken)): 
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
                    t2 = t2.next0_
            return None
        if (not digs and not after_num): 
            return None
        ch = Utils.getCharAtStringIO(tmp, tmp.tell() - 1)
        if (not str.isalnum(ch) and (isinstance(res, TextToken)) and not res.is_char('_')): 
            Utils.setLengthStringIO(tmp, tmp.tell() - 1)
            res = res.previous
        if ((res.next0_ is not None and res.next0_.is_hiphen and (isinstance(res.next0_.next0_, NumberToken))) and res.next0_.next0_.int_value is not None): 
            wrapmin896 = RefOutArgWrapper(0)
            inoutres897 = Utils.tryParseInt(Utils.toStringStringIO(tmp), wrapmin896)
            min0_ = wrapmin896.value
            if (inoutres897): 
                if (min0_ < res.next0_.next0_.int_value): 
                    res = res.next0_.next0_
                    print("-{0}".format(res.value), end="", file=tmp, flush=True)
        if (res.next0_ is not None and not res.is_whitespace_after and res.next0_.is_char('(')): 
            cou = 0
            tmp2 = io.StringIO()
            tt = res.next0_.next0_
            while tt is not None: 
                if (tt.is_char(')')): 
                    print("({0})".format(Utils.toStringStringIO(tmp2)), end="", file=tmp, flush=True)
                    res = tt
                    break
                cou += 1
                if (cou > 5): 
                    break
                if (tt.is_whitespace_before or tt.is_whitespace_after): 
                    break
                if (isinstance(tt, ReferentToken)): 
                    break
                print(tt.get_source_text(), end="", file=tmp2)
                tt = tt.next0_
        if (tmp.tell() > 2): 
            if (Utils.getCharAtStringIO(tmp, tmp.tell() - 1) == '3'): 
                if (Utils.getCharAtStringIO(tmp, tmp.tell() - 2) == 'К' or Utils.getCharAtStringIO(tmp, tmp.tell() - 2) == 'Ф'): 
                    Utils.setCharAtStringIO(tmp, tmp.tell() - 1, 'З')
        if ((isinstance(res.next0_, TextToken)) and (res.whitespaces_after_count < 2) and res.next0_.chars.is_all_upper): 
            if (res.next0_.is_value("РД", None) or res.next0_.is_value("ПД", None)): 
                print(" {0}".format(res.next0_.term), end="", file=tmp, flush=True)
                res = res.next0_
        if ((isinstance(res.next0_, TextToken)) and res.next0_.is_char('*')): 
            res = res.next0_
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
        p = DecreeToken.try_attach(t, prev, must_start_by_typ)
        if (p is None): 
            return None
        if (p.typ == DecreeToken.ItemType.ORG or p.typ == DecreeToken.ItemType.OWNER): 
            if (t.previous is not None and t.previous.is_value("РАССМОТРЕНИЕ", "РОЗГЛЯД")): 
                return None
        if (p.typ == DecreeToken.ItemType.NUMBER and (isinstance(t, NumberToken))): 
            pass
        res = list()
        res.append(p)
        tt = p.end_token.next0_
        if (tt is not None and t.previous is not None): 
            if (BracketHelper.can_be_start_of_sequence(t.previous, False, False) and BracketHelper.can_be_end_of_sequence(tt, False, None, False)): 
                p.begin_token = t.previous
                p.end_token = tt
                tt = tt.next0_
        first_pass3596 = True
        while True:
            if first_pass3596: first_pass3596 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            ws = False
            if (tt.whitespaces_before_count > 15): 
                ws = True
            if (max_count > 0 and len(res) >= max_count): 
                la = res[len(res) - 1]
                if (la.typ != DecreeToken.ItemType.TYP and la.typ != DecreeToken.ItemType.DATE and la.typ != DecreeToken.ItemType.NUMBER): 
                    break
                if (len(res) > (max_count * 3)): 
                    break
            p0 = DecreeToken.try_attach(tt, Utils.ifNotNull(prev, p), False)
            if (ws): 
                if (p0 is None or p is None): 
                    break
                if (((p.typ == DecreeToken.ItemType.TYP and p0.typ == DecreeToken.ItemType.NUMBER)) or ((p0.typ == DecreeToken.ItemType.NAME and p.typ != DecreeToken.ItemType.NAME)) or ((p0.typ == DecreeToken.ItemType.ORG and p.typ == DecreeToken.ItemType.ORG))): 
                    pass
                elif ((((p0.typ == DecreeToken.ItemType.DATE or p0.typ == DecreeToken.ItemType.NUMBER)) and p.typ == DecreeToken.ItemType.ORG and len(res) == 2) and res[0].typ == DecreeToken.ItemType.TYP): 
                    pass
                else: 
                    break
            if (p0 is None): 
                if (tt.is_newline_before): 
                    break
                if (tt.morph.class0_.is_preposition and res[0].typ == DecreeToken.ItemType.TYP): 
                    continue
                if (tt.is_char('.') and p.typ == DecreeToken.ItemType.NUMBER and (tt.whitespaces_after_count < 3)): 
                    p0 = DecreeToken.__try_attach(tt.next0_, p, 0, False)
                    if (p0 is not None and ((p0.typ == DecreeToken.ItemType.NAME or p0.typ == DecreeToken.ItemType.DATE))): 
                        continue
                    p0 = (None)
                if (((tt.is_comma_and or tt.is_hiphen)) and res[0].typ == DecreeToken.ItemType.TYP): 
                    p0 = DecreeToken.try_attach(tt.next0_, p, False)
                    if (p0 is not None): 
                        ty0 = p0.typ
                        if (ty0 == DecreeToken.ItemType.ORG or ty0 == DecreeToken.ItemType.OWNER): 
                            ty0 = DecreeToken.ItemType.UNKNOWN
                        ty = p.typ
                        if (ty == DecreeToken.ItemType.ORG or ty == DecreeToken.ItemType.OWNER): 
                            ty = DecreeToken.ItemType.UNKNOWN
                        if (ty0 == ty or p0.typ == DecreeToken.ItemType.EDITION): 
                            p = p0
                            res.append(p)
                            tt = p.end_token
                            continue
                    p0 = (None)
                if (tt.is_char(':')): 
                    p0 = DecreeToken.try_attach(tt.next0_, p, False)
                    if (p0 is not None): 
                        if (p0.typ == DecreeToken.ItemType.NUMBER or p0.typ == DecreeToken.ItemType.DATE): 
                            p = p0
                            res.append(p)
                            tt = p.end_token
                            continue
                if (tt.is_comma and p.typ == DecreeToken.ItemType.NUMBER): 
                    p0 = DecreeToken.try_attach(tt.next0_, p, False)
                    if (p0 is not None and p0.typ == DecreeToken.ItemType.DATE): 
                        p = p0
                        res.append(p)
                        tt = p.end_token
                        continue
                    cou = 0
                    if (res[0].typ == DecreeToken.ItemType.TYP): 
                        ii = 1
                        while ii < len(res): 
                            if ((res[ii].typ == DecreeToken.ItemType.ORG or res[ii].typ == DecreeToken.ItemType.TERR or res[ii].typ == DecreeToken.ItemType.UNKNOWN) or res[ii].typ == DecreeToken.ItemType.OWNER): 
                                cou += 1
                            else: 
                                break
                            ii += 1
                        if (cou > 1): 
                            num = Utils.newStringIO(p.value)
                            tmp = io.StringIO()
                            tend = None
                            tt1 = tt
                            while tt1 is not None: 
                                if (not tt1.is_comma_and): 
                                    break
                                pp = DecreeToken.try_attach(tt1.next0_, p, False)
                                if (pp is not None): 
                                    break
                                if (not (isinstance(tt1.next0_, NumberToken))): 
                                    break
                                Utils.setLengthStringIO(tmp, 0)
                                tt2 = DecreeToken.__try_attach_number(tt1.next0_, tmp, True)
                                if (tt2 is None): 
                                    break
                                print(",{0}".format(Utils.toStringStringIO(tmp)), end="", file=num, flush=True)
                                cou -= 1
                                tend = tt2
                                tt1 = tend
                                tt1 = tt1.next0_
                            if (cou == 1): 
                                p.value = Utils.toStringStringIO(num)
                                p.end_token = tend
                                tt = p.end_token
                                continue
                    p0 = (None)
                if (tt.is_comma and p.typ == DecreeToken.ItemType.DATE): 
                    p0 = DecreeToken.try_attach(tt.next0_, p, False)
                    if (p0 is not None and p0.typ == DecreeToken.ItemType.NUMBER): 
                        p = p0
                        res.append(p)
                        tt = p.end_token
                        continue
                    p0 = (None)
                if (tt.is_comma_and and ((p.typ == DecreeToken.ItemType.ORG or p.typ == DecreeToken.ItemType.OWNER))): 
                    p0 = DecreeToken.try_attach(tt.next0_, p, False)
                    if (p0 is not None and ((p0.typ == DecreeToken.ItemType.ORG or p.typ == DecreeToken.ItemType.OWNER))): 
                        p = p0
                        res.append(p)
                        tt = p.end_token
                        continue
                    p0 = (None)
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
                if ((((isinstance(tt, TextToken)) and tt.chars.is_all_upper and BracketHelper.can_be_start_of_sequence(tt.next0_, False, False)) and len(res) > 1 and res[len(res) - 1].typ == DecreeToken.ItemType.NUMBER) and res[len(res) - 2].typ == DecreeToken.ItemType.TYP and res[len(res) - 2].typ_kind == DecreeKind.STANDARD): 
                    continue
                if (tt.is_char('(')): 
                    p = DecreeToken.try_attach(tt.next0_, None, False)
                    if (p is not None and p.typ == DecreeToken.ItemType.EDITION): 
                        br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                        if (br is not None): 
                            res.append(p)
                            tt = p.end_token.next0_
                            while tt is not None: 
                                if (tt.end_char >= br.end_char): 
                                    break
                                p = DecreeToken.try_attach(tt, None, False)
                                if (p is not None): 
                                    res.append(p)
                                    tt = p.end_token
                                tt = tt.next0_
                            res[len(res) - 1].end_token = br.end_token
                            tt = res[len(res) - 1].end_token
                            continue
                if ((isinstance(tt, NumberToken)) and res[len(res) - 1].typ == DecreeToken.ItemType.DATE): 
                    if (tt.previous is not None and tt.previous.morph.class0_.is_preposition): 
                        pass
                    elif (NumberHelper.try_parse_number_with_postfix(tt) is not None): 
                        pass
                    else: 
                        tmp = io.StringIO()
                        t11 = DecreeToken.__try_attach_number(tt, tmp, False)
                        if (t11 is not None): 
                            p0 = DecreeToken._new845(tt, t11, DecreeToken.ItemType.NUMBER, Utils.toStringStringIO(tmp))
                if (p0 is None): 
                    break
            p = p0
            res.append(p)
            tt = p.end_token
        i = 0
        first_pass3597 = True
        while True:
            if first_pass3597: first_pass3597 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].end_token.next0_.is_comma): 
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
                    res[i].ref = (None)
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
        first_pass3598 = True
        while True:
            if first_pass3598: first_pass3598 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == DecreeToken.ItemType.UNKNOWN): 
                ok = False
                j = (i + 1)
                while j < len(res): 
                    if (res[j].begin_token.previous.is_comma): 
                        break
                    elif (res[j].typ == DecreeToken.ItemType.DATE or res[j].typ == DecreeToken.ItemType.NUMBER): 
                        ok = True
                        break
                    elif (res[j].typ == DecreeToken.ItemType.TERR or res[j].typ == DecreeToken.ItemType.ORG or res[j].typ == DecreeToken.ItemType.UNKNOWN): 
                        pass
                    else: 
                        break
                    j += 1
                if (not ok): 
                    continue
                if (j == (i + 1)): 
                    if (res[i].begin_token.previous.is_comma): 
                        res[i].typ = DecreeToken.ItemType.OWNER
                    continue
                tmp = io.StringIO()
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
            te = res[2].end_token.next0_
            while te is not None: 
                if (not te.is_char(',') or te.next0_ is None): 
                    break
                res1 = DecreeToken.try_attach_list(te.next0_, res[0], 10, False)
                if (res1 is None or (len(res1) < 2)): 
                    break
                if (((res1[0].typ == DecreeToken.ItemType.OWNER or res1[0].typ == DecreeToken.ItemType.ORG or res1[0].typ == DecreeToken.ItemType.TERR)) and res1[1].typ == DecreeToken.ItemType.NUMBER): 
                    res.extend(res1)
                    te = res1[len(res1) - 1].end_token
                else: 
                    break
                te = te.next0_
        if (len(res) > 1 and ((res[len(res) - 1].typ == DecreeToken.ItemType.OWNER or res[len(res) - 1].typ == DecreeToken.ItemType.ORG))): 
            te = res[len(res) - 1].end_token.next0_
            if (te is not None and te.is_comma_and): 
                res1 = DecreeToken.try_attach_list(te.next0_, res[0], 10, False)
                if (res1 is not None and len(res1) > 0): 
                    if (res1[0].typ == DecreeToken.ItemType.OWNER or res1[0].typ == DecreeToken.ItemType.ORG): 
                        res.extend(res1)
        return res
    
    @staticmethod
    def try_attach_name(t : 'Token', typ_ : str, very_probable : bool=False, in_title_doc_ref : bool=False) -> 'DecreeToken':
        if (t is None): 
            return None
        if (t.is_char(';')): 
            t = t.next0_
        if (t is None): 
            return None
        li = MailLine.parse(t, 0, 20)
        if (li is not None): 
            if (li.typ == MailLine.Types.HELLO): 
                return None
        t0 = t
        t1 = t
        abou = False
        ty = DecreeToken.get_kind(typ_)
        if (t.is_value("О", None) or t.is_value("ОБ", None) or t.is_value("ПРО", None)): 
            t = t.next0_
            abou = True
        elif (t.is_value("ПО", None)): 
            if (LanguageHelper.ends_with(typ_, "ЗАКОН")): 
                return None
            t = t.next0_
            abou = True
            if (t is not None): 
                if (t.is_value("ПОЗИЦИЯ", None)): 
                    return None
        elif (t.next0_ is not None): 
            if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None and br.is_quote_type): 
                    re = t.next0_.get_referent()
                    if (re is not None and re.type_name == "URI"): 
                        return None
                    if (t.next0_.chars.is_letter): 
                        if (t.next0_.chars.is_all_lower or (((isinstance(t.next0_, TextToken)) and t.next0_.is_pure_verb))): 
                            return None
                    t1 = br.end_token
                    tt1 = DecreeToken._try_attach_std_change_name(t.next0_)
                    if (tt1 is not None): 
                        t1 = tt1
                    s0 = MiscHelper.get_text_value(t0, t1, GetTextAttr.KEEPREGISTER)
                    if (Utils.isNullOrEmpty(s0)): 
                        return None
                    if ((len(s0) < 10) and typ_ != "ПРОГРАММА" and typ_ != "ПРОГРАМА"): 
                        return None
                    return DecreeToken._new845(t, t1, DecreeToken.ItemType.NAME, s0)
                dt = DecreeToken.try_attach_name(t.next0_, typ_, False, False)
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
        npts = list()
        tt = t
        first_pass3599 = True
        while True:
            if first_pass3599: first_pass3599 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_newline_before and tt != t): 
                if (tt.whitespaces_before_count > 15 or not abou): 
                    break
                if (tt.is_value("ИСТОЧНИК", None)): 
                    break
                if ((isinstance(tt, TextToken)) and tt.chars.is_letter and tt.chars.is_all_lower): 
                    pass
                else: 
                    break
            if (tt.is_char_of("(,") and tt.next0_ is not None): 
                if (tt.next0_.is_value("УТВЕРЖДЕННЫЙ", "ЗАТВЕРДЖЕНИЙ") or tt.next0_.is_value("ПРИНЯТЫЙ", "ПРИЙНЯТИЙ") or tt.next0_.is_value("УТВ", "ЗАТВ")): 
                    ttt = tt.next0_.next0_
                    if (ttt is not None and ttt.is_char('.') and tt.next0_.is_value("УТВ", None)): 
                        ttt = ttt.next0_
                    dt = DecreeToken.try_attach(ttt, None, False)
                    if (dt is not None and dt.typ == DecreeToken.ItemType.TYP): 
                        break
                    if (dt is not None and ((dt.typ == DecreeToken.ItemType.ORG or dt.typ == DecreeToken.ItemType.OWNER))): 
                        dt2 = DecreeToken.try_attach(dt.end_token.next0_, None, False)
                        if (dt2 is not None and dt2.typ == DecreeToken.ItemType.DATE): 
                            break
            if (very_probable and abou and not tt.is_newline_before): 
                t1 = tt
                continue
            if (tt.is_value("ОТ", "ВІД")): 
                dt = DecreeToken.try_attach(tt, None, False)
                if (dt is not None): 
                    break
            if (tt.morph.class0_.is_preposition and tt.next0_ is not None and (((isinstance(tt.next0_.get_referent(), DateReferent)) or (isinstance(tt.next0_.get_referent(), DateRangeReferent))))): 
                break
            if (in_title_doc_ref): 
                t1 = tt
                continue
            conj = ConjunctionHelper.try_parse(tt)
            if (conj is not None): 
                if (cou == 0): 
                    break
                if (conj.end_token.next0_ is None): 
                    break
                tt = conj.end_token
                continue
            if (not tt.chars.is_cyrillic_letter): 
                break
            if (tt.morph.class0_.is_personal_pronoun or tt.morph.class0_.is_pronoun): 
                if (not tt.is_value("ВСЕ", "ВСІ") and not tt.is_value("ВСЯКИЙ", None) and not tt.is_value("ДАННЫЙ", "ДАНИЙ")): 
                    break
            if (isinstance(tt, NumberToken)): 
                break
            pit = PartToken.try_attach(tt, None, False, False)
            if (pit is not None): 
                break
            r = tt.get_referent()
            if (r is not None): 
                if (((isinstance(r, DecreeReferent)) or (isinstance(r, DateReferent)) or (isinstance(r, OrganizationReferent))) or (isinstance(r, GeoReferent)) or r.type_name == "NAMEDENTITY"): 
                    if (tt.is_newline_before): 
                        break
                    t1 = tt
                    continue
            npt = NounPhraseHelper.try_parse(tt, Utils.valToEnum((NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.PARSEPREPOSITION) | (NounPhraseParseAttr.PARSEVERBS), NounPhraseParseAttr), 0, None)
            if (npt is None): 
                if (tt.morph.class0_.is_preposition): 
                    continue
                break
            dd = npt.end_token.get_morph_class_in_dictionary()
            if (dd.is_verb and npt.end_token == npt.begin_token): 
                if (not dd.is_noun): 
                    break
                if (tt.is_value("БЫТЬ", "БУТИ")): 
                    break
            if (not npt.morph.case_.is_genitive): 
                if (cou > 0): 
                    if ((npt.morph.case_.is_instrumental and tt.previous is not None and tt.previous.previous is not None) and ((tt.previous.previous.is_value("РАБОТА", "РОБОТА")))): 
                        pass
                    elif (abou and very_probable): 
                        pass
                    elif (npt.noun.is_value("ГОД", "РІК") or npt.noun.is_value("ПЕРИОД", "ПЕРІОД")): 
                        pass
                    else: 
                        ok = False
                        for n in npts: 
                            links = SemanticHelper.try_create_links(n, npt, None)
                            if (len(links) > 0): 
                                ok = True
                                break
                            if (n == npts[len(npts) - 1]): 
                                if (not ((npts[len(npts) - 1].morph.case_) & npt.morph.case_).is_undefined): 
                                    ok = True
                        if (not ok): 
                            break
                if (not abou): 
                    break
            cou += 1
            t1 = npt.end_token
            tt = t1
            if (npt.noun.is_value("НАЛОГОПЛАТЕЛЬЩИК", None)): 
                ttn = MiscHelper.check_number_prefix(tt.next0_)
                if ((isinstance(ttn, NumberToken)) and ttn.value == "1"): 
                    t1 = ttn
                    tt = t1
            npts.append(npt)
        if (tt == t): 
            return None
        if (abou): 
            tt1 = DecreeToken._try_attach_std_change_name(t0)
            if (tt1 is not None and tt1.end_char > t1.end_char): 
                t1 = tt1
        s = MiscHelper.get_text_value(t0, t1, Utils.valToEnum((GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
        if (Utils.isNullOrEmpty(s) or (len(s) < 10)): 
            return None
        return DecreeToken._new845(t, t1, DecreeToken.ItemType.NAME, s)
    
    @staticmethod
    def _try_attach_std_change_name(t : 'Token') -> 'Token':
        if (not (isinstance(t, TextToken)) or t.next0_ is None): 
            return None
        t0 = t
        term = t.term
        if ((term != "О" and term != "O" and term != "ОБ") and term != "ПРО"): 
            return None
        t = t.next0_
        if (((t.is_value("ВНЕСЕНИЕ", "ВНЕСЕННЯ") or t.is_value("УТВЕРЖДЕНИЕ", "ТВЕРДЖЕННЯ") or t.is_value("ПРИНЯТИЕ", "ПРИЙНЯТТЯ")) or t.is_value("ВВЕДЕНИЕ", "ВВЕДЕННЯ") or t.is_value("ПРИОСТАНОВЛЕНИЕ", "ПРИЗУПИНЕННЯ")) or t.is_value("ОТМЕНА", "СКАСУВАННЯ") or t.is_value("МЕРА", "ЗАХІД")): 
            pass
        elif (t.is_value("ПРИЗНАНИЕ", "ВИЗНАННЯ") and t.next0_ is not None and t.next0_.is_value("УТРАТИТЬ", "ВТРАТИТИ")): 
            pass
        else: 
            return None
        t1 = t
        tt = t.next0_
        first_pass3600 = True
        while True:
            if first_pass3600: first_pass3600 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_newline_before): 
                pass
            if (tt.whitespaces_before_count > 15): 
                break
            if (MiscHelper.can_be_start_of_sentence(tt)): 
                break
            if (tt.morph.class0_.is_conjunction or tt.morph.class0_.is_preposition): 
                continue
            if (tt.is_comma): 
                continue
            npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                if ((((((npt.noun.is_value("ВВЕДЕНИЕ", "ВВЕДЕННЯ") or npt.noun.is_value("ПРИОСТАНОВЛЕНИЕ", "ПРИЗУПИНЕННЯ") or npt.noun.is_value("ВНЕСЕНИЕ", "ВНЕСЕННЯ")) or npt.noun.is_value("ИЗМЕНЕНИЕ", "ЗМІНА") or npt.noun.is_value("ДОПОЛНЕНИЕ", "ДОДАТОК")) or npt.noun.is_value("АКТ", None) or npt.noun.is_value("ПРИЗНАНИЕ", "ВИЗНАННЯ")) or npt.noun.is_value("ПРИНЯТИЕ", "ПРИЙНЯТТЯ") or npt.noun.is_value("СИЛА", "ЧИННІСТЬ")) or npt.noun.is_value("ДЕЙСТВИЕ", "ДІЯ") or npt.noun.is_value("СВЯЗЬ", "ЗВЯЗОК")) or npt.noun.is_value("РЕАЛИЗАЦИЯ", "РЕАЛІЗАЦІЯ") or npt.noun.is_value("РЯД", None)): 
                    tt = npt.end_token
                    t1 = tt
                    continue
            if (tt.is_value("ТАКЖЕ", "ТАКОЖ") or tt.is_value("НЕОБХОДИМЫЙ", "НЕОБХІДНИЙ")): 
                continue
            r = tt.get_referent()
            if ((isinstance(r, GeoReferent)) or (isinstance(r, DecreeReferent)) or (isinstance(r, DecreePartReferent))): 
                t1 = tt
                continue
            if ((isinstance(r, OrganizationReferent)) and tt.is_newline_after): 
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
            if (BracketHelper.can_be_end_of_sequence(t1.next0_, True, t0.previous, False)): 
                t1 = t1.next0_
        return t1
    
    M_TERMINS = None
    
    M_KEYWORDS = None
    
    @staticmethod
    def initialize() -> None:
        if (DecreeToken.M_TERMINS is not None): 
            return
        DecreeToken.M_TERMINS = TerminCollection()
        DecreeToken.M_KEYWORDS = TerminCollection()
        for s in DecreeToken.M_MISC_TYPESRU: 
            DecreeToken.M_KEYWORDS.add(Termin(s))
        for s in DecreeToken.M_MISC_TYPESUA: 
            DecreeToken.M_KEYWORDS.add(Termin._new901(s, MorphLang.UA))
        t = Termin._new95("ТЕХНИЧЕСКОЕ ЗАДАНИЕ", "ТЗ")
        t.add_variant("ТЕХЗАДАНИЕ", False)
        t.add_abridge("ТЕХ. ЗАДАНИЕ")
        DecreeToken.M_KEYWORDS.add(t)
        t = Termin._new95("ТЕХНИКО КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ", "ТКП")
        t.add_variant("КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ", False)
        DecreeToken.M_KEYWORDS.add(t)
        for s in DecreeToken.M_ALL_TYPESRU: 
            DecreeToken.M_TERMINS.add(Termin._new100(s, DecreeToken.ItemType.TYP))
            DecreeToken.M_KEYWORDS.add(Termin._new100(s, DecreeToken.ItemType.TYP))
        for s in DecreeToken.M_ALL_TYPESUA: 
            DecreeToken.M_TERMINS.add(Termin._new101(s, DecreeToken.ItemType.TYP, MorphLang.UA))
            DecreeToken.M_KEYWORDS.add(Termin._new101(s, DecreeToken.ItemType.TYP, MorphLang.UA))
        DecreeToken.M_TERMINS.add(Termin._new100("ОТРАСЛЕВОЕ СОГЛАШЕНИЕ", DecreeToken.ItemType.TYP))
        DecreeToken.M_TERMINS.add(Termin._new388("ГАЛУЗЕВА УГОДА", MorphLang.UA, DecreeToken.ItemType.TYP))
        DecreeToken.M_TERMINS.add(Termin._new100("МЕЖОТРАСЛЕВОЕ СОГЛАШЕНИЕ", DecreeToken.ItemType.TYP))
        DecreeToken.M_TERMINS.add(Termin._new388("МІЖГАЛУЗЕВА УГОДА", MorphLang.UA, DecreeToken.ItemType.TYP))
        DecreeToken.M_TERMINS.add(Termin._new102("ОСНОВЫ ЗАКОНОДАТЕЛЬСТВА", DecreeToken.ItemType.TYP, DecreeKind.KODEX))
        DecreeToken.M_TERMINS.add(Termin._new913("ОСНОВИ ЗАКОНОДАВСТВА", MorphLang.UA, DecreeToken.ItemType.TYP, DecreeKind.KODEX))
        DecreeToken.M_TERMINS.add(Termin._new102("ОСНОВЫ ГРАЖДАНСКОГО ЗАКОНОДАТЕЛЬСТВА", DecreeToken.ItemType.TYP, DecreeKind.KODEX))
        DecreeToken.M_TERMINS.add(Termin._new913("ОСНОВИ ЦИВІЛЬНОГО ЗАКОНОДАВСТВА", MorphLang.UA, DecreeToken.ItemType.TYP, DecreeKind.KODEX))
        t = Termin._new126("ФЕДЕРАЛЬНЫЙ ЗАКОН", DecreeToken.ItemType.TYP, "ФЗ")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new917("ФЕДЕРАЛЬНИЙ ЗАКОН", MorphLang.UA, DecreeToken.ItemType.TYP, "ФЗ")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("ПРОЕКТ ЗАКОНА", DecreeToken.ItemType.TYP)
        t.add_variant("ЗАКОНОПРОЕКТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("ПАСПОРТ ПРОЕКТА", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new388("ПРОЕКТ ЗАКОНУ", MorphLang.UA, DecreeToken.ItemType.TYP)
        t.add_variant("ЗАКОНОПРОЕКТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new388("ПАСПОРТ ПРОЕКТУ", MorphLang.UA, DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new124("ГОСУДАРСТВЕННАЯ ПРОГРАММА", "ПРОГРАММА", DecreeToken.ItemType.TYP)
        t.add_variant("ГОСУДАРСТВЕННАЯ ЦЕЛЕВАЯ ПРОГРАММА", False)
        t.add_variant("ФЕДЕРАЛЬНАЯ ЦЕЛЕВАЯ ПРОГРАММА", False)
        t.add_abridge("ФЕДЕРАЛЬНАЯ ПРОГРАММА")
        t.add_variant("МЕЖГОСУДАРСТВЕННАЯ ЦЕЛЕВАЯ ПРОГРАММА", False)
        t.add_abridge("МЕЖГОСУДАРСТВЕННАЯ ПРОГРАММА")
        t.add_variant("ГОСПРОГРАММА", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ДЕРЖАВНА ПРОГРАМА", "ПРОГРАМА", MorphLang.UA, DecreeToken.ItemType.TYP)
        t.add_variant("ДЕРЖАВНА ЦІЛЬОВА ПРОГРАМА", False)
        t.add_variant("ФЕДЕРАЛЬНА ЦІЛЬОВА ПРОГРАМА", False)
        t.add_abridge("ФЕДЕРАЛЬНА ПРОГРАМА")
        t.add_variant("ДЕРЖПРОГРАМА", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new126("ФЕДЕРАЛЬНЫЙ КОНСТИТУЦИОННЫЙ ЗАКОН", DecreeToken.ItemType.TYP, "ФКЗ")
        t.add_variant("КОНСТИТУЦИОННЫЙ ЗАКОН", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new917("ФЕДЕРАЛЬНИЙ КОНСТИТУЦІЙНИЙ ЗАКОН", MorphLang.UA, DecreeToken.ItemType.TYP, "ФКЗ")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("УГОЛОВНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "УК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("КРИМИНАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "КК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("КРИМІНАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "КК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("УГОЛОВНО-ПРОЦЕССУАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "УПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("КРИМІНАЛЬНО-ПРОЦЕСУАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "КПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("УГОЛОВНО-ИСПОЛНИТЕЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "УИК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("КРИМІНАЛЬНО-ВИКОНАВЧИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "КВК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ГРАЖДАНСКИЙ КОДЕКС", DecreeToken.ItemType.TYP, "ГК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("ЦИВІЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЦК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ГРАЖДАНСКИЙ ПРОЦЕССУАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ГПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("ЦИВІЛЬНИЙ ПРОЦЕСУАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЦПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ГРАДОСТРОИТЕЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ГРК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("МІСТОБУДІВНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "МБК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ХОЗЯЙСТВЕННЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ХК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("ГОСПОДАРСЬКИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ГК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ХОЗЯЙСТВЕННЫЙ ПРОЦЕССУАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ХПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("ГОСПОДАРСЬКИЙ ПРОЦЕСУАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ГПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new102("АРБИТРАЖНЫЙ ПРОЦЕССУАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, DecreeKind.KODEX)
        t.add_abridge("АПК")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new913("АРБІТРАЖНИЙ ПРОЦЕСУАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, DecreeKind.KODEX)
        t.add_abridge("АПК")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("КОДЕКС ВНУТРЕННЕГО ВОДНОГО ТРАНСПОРТА", DecreeToken.ItemType.TYP, "КВВТ", DecreeKind.KODEX)
        t.add_variant("КВ ВТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ТРУДОВОЙ КОДЕКС", DecreeToken.ItemType.TYP, "ТК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("ТРУДОВИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ТК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("КОДЕКС ЗАКОНОВ О ТРУДЕ", "КЗОТ", DecreeToken.ItemType.TYP, DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("КОДЕКС ЗАКОНІВ ПРО ПРАЦЮ", MorphLang.UA, DecreeToken.ItemType.TYP, "КЗПП", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ЖИЛИЩНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ЖК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("ЖИТЛОВИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЖК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ЗЕМЕЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ЗК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("ЗЕМЕЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЗК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ЛЕСНОЙ КОДЕКС", DecreeToken.ItemType.TYP, "ЛК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("ЛІСОВИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЛК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("БЮДЖЕТНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "БК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("БЮДЖЕТНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "БК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("НАЛОГОВЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "НК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("ПОДАТКОВИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("СЕМЕЙНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "СК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("СІМЕЙНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "СК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ВОДНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ВК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("ВОДНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ВК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ВОЗДУШНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ВК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("ПОВІТРЯНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("КОДЕКС ОБ АДМИНИСТРАТИВНЫХ ПРАВОНАРУШЕНИЯХ", DecreeToken.ItemType.TYP, "КОАП", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("КОДЕКС ПРО АДМІНІСТРАТИВНІ ПРАВОПОРУШЕННЯ", MorphLang.UA, DecreeToken.ItemType.TYP, "КОАП", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("ОБ АДМИНИСТРАТИВНЫХ ПРАВОНАРУШЕНИЯХ", DecreeToken.ItemType.STDNAME)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new388("ПРО АДМІНІСТРАТИВНІ ПРАВОПОРУШЕННЯ", MorphLang.UA, DecreeToken.ItemType.STDNAME)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("КОДЕКС ОБ АДМИНИСТРАТИВНЫХ ПРАВОНАРУШЕНИЯХ", DecreeToken.ItemType.TYP, "КРКОАП", DecreeKind.KODEX)
        t.add_variant("КРК ОБ АП", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("КОДЕКС АДМИНИСТРАТИВНОГО СУДОПРОИЗВОДСТВА", DecreeToken.ItemType.TYP, "КАС", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("КОДЕКС АДМІНІСТРАТИВНОГО СУДОЧИНСТВА", MorphLang.UA, DecreeToken.ItemType.TYP, "КАС", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ТАМОЖЕННЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ТК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("МИТНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "МК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("КОДЕКС ТОРГОВОГО МОРЕПЛАВАНИЯ", DecreeToken.ItemType.TYP, "КТМ", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("КОДЕКС ТОРГОВЕЛЬНОГО МОРЕПЛАВСТВА", MorphLang.UA, DecreeToken.ItemType.TYP, "КТМ", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new926("ПРАВИЛА ДОРОЖНОГО ДВИЖЕНИЯ", DecreeToken.ItemType.TYP, "ПДД", "ПРАВИЛА")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new928("ПРАВИЛА ДОРОЖНЬОГО РУХУ", MorphLang.UA, DecreeToken.ItemType.TYP, "ПДР", "ПРАВИЛА")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("СОБРАНИЕ ЗАКОНОДАТЕЛЬСТВА", DecreeToken.ItemType.TYP)
        t.add_abridge("СЗ")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("ОФИЦИАЛЬНЫЙ ВЕСТНИК", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new388("ОФІЦІЙНИЙ ВІСНИК", MorphLang.UA, DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("СВОД ЗАКОНОВ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("БЮЛЛЕТЕНЬ НОРМАТИВНЫХ АКТОВ ФЕДЕРАЛЬНЫХ ОРГАНОВ ИСПОЛНИТЕЛЬНОЙ ВЛАСТИ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("БЮЛЛЕТЕНЬ МЕЖДУНАРОДНЫХ ДОГОВОРОВ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("БЮЛЛЕТЕНЬ ВЕРХОВНОГО СУДА", DecreeToken.ItemType.TYP)
        t.add_variant("БЮЛЛЕТЕНЬ ВС", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("ВЕСТНИК ВЫСШЕГО АРБИТРАЖНОГО СУДА", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("ВЕСТНИК БАНКА РОССИИ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("РОССИЙСКАЯ ГАЗЕТА", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("РОССИЙСКИЕ ВЕСТИ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("СОБРАНИЕ АКТОВ ПРЕЗИДЕНТА И ПРАВИТЕЛЬСТВА", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("ВЕДОМОСТИ ВЕРХОВНОГО СОВЕТА", DecreeToken.ItemType.TYP)
        t.add_variant("ВЕДОМОСТИ ВС", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("ВЕДОМОСТИ СЪЕЗДА НАРОДНЫХ ДЕПУТАТОВ И ВЕРХОВНОГО СОВЕТА", DecreeToken.ItemType.TYP)
        t.add_variant("ВЕДОМОСТИ СЪЕЗДА НАРОДНЫХ ДЕПУТАТОВ РФ И ВЕРХОВНОГО СОВЕТА", False)
        t.add_variant("ВЕДОМОСТИ СЪЕЗДА НАРОДНЫХ ДЕПУТАТОВ", False)
        t.add_variant("ВЕДОМОСТИ СНД РФ И ВС", False)
        t.add_variant("ВЕДОМОСТИ СНД И ВС", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("БЮЛЛЕТЕНЬ НОРМАТИВНЫХ АКТОВ МИНИСТЕРСТВ И ВЕДОМСТВ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        DecreeToken.M_TERMINS.add(Termin._new100("СВОД ЗАКОНОВ", DecreeToken.ItemType.TYP))
        DecreeToken.M_TERMINS.add(Termin._new100("ВЕДОМОСТИ", DecreeToken.ItemType.TYP))
        t = Termin._new124("ЗАРЕГИСТРИРОВАТЬ", "РЕГИСТРАЦИЯ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new997("ЗАРЕЄСТРУВАТИ", MorphLang.UA, "РЕЄСТРАЦІЯ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new102("СТАНДАРТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("МЕЖДУНАРОДНЫЙ СТАНДАРТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new126("ЕДИНЫЙ ОТРАСЛЕВОЙ СТАНДАРТ ЗАКУПОК", DecreeToken.ItemType.TYP, "ЕОСЗ")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new100("ЕДИНЫЙ ОТРАСЛЕВОЙ ПОРЯДОК", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new102("ГОСТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ГОСУДАРСТВЕННЫЙ СТАНДАРТ", False)
        t.add_variant("ГОССТАНДАРТ", False)
        t.add_variant("НАЦИОНАЛЬНЫЙ СТАНДАРТ", False)
        t.add_variant("МЕЖГОСУДАРСТВЕННЫЙ СТАНДАРТ", False)
        t.add_variant("ДЕРЖАВНИЙ СТАНДАРТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new102("ОСТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ОТРАСЛЕВОЙ СТАНДАРТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new102("ПНСТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ПРЕДВАРИТЕЛЬНЫЙ НАЦИОНАЛЬНЫЙ СТАНДАРТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new102("РСТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("РЕСПУБЛИКАНСКИЙ СТАНДАРТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new102("ПБУ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ПОЛОЖЕНИЕ ПО БУХГАЛТЕРСКОМУ УЧЕТУ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new102("ISO", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ИСО", False)
        t.add_variant("ISO/IEC", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("ТЕХНИЧЕСКИЕ УСЛОВИЯ", "ТУ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ТЕХУСЛОВИЯ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("ФЕДЕРАЛЬНЫЕ НОРМЫ И ПРАВИЛА", "ФНП", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("НОРМАТИВНЫЕ ПРАВИЛА", "НП", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new102("СТРОИТЕЛЬНЫЕ НОРМЫ И ПРАВИЛА", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("СНИП", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("СТРОИТЕЛЬНЫЕ НОРМЫ", "СН", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("CH", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("ВЕДОМСТВЕННЫЕ СТРОИТЕЛЬНЫЕ НОРМЫ", "ВСН", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("BCH", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("РЕСПУБЛИКАНСКИЕ СТРОИТЕЛЬНЫЕ НОРМЫ", "РСН", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("PCH", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("ПРАВИЛА БЕЗОПАСНОСТИ", "ПБ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("НОРМЫ РАДИАЦИОННОЙ БЕЗОПАСНОСТИ", "НРБ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("ПРАВИЛА РАДИАЦИОННОЙ БЕЗОПАСНОСТИ", "ПРБ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("НОРМЫ ПОЖАРНОЙ БЕЗОПАСНОСТИ", "НПБ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("ПРАВИЛА ПОЖАРНОЙ БЕЗОПАСНОСТИ", "ППБ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("СТРОИТЕЛЬНЫЕ ПРАВИЛА", "СП", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("МОСКОВСКИЕ ГОРОДСКИЕ СТРОИТЕЛЬНЫЕ НОРМЫ", "МГСН", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new102("АВОК", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ABOK", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("ТЕХНИЧЕСКИЙ РЕГЛАМЕНТ", "ТР", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("ОБЩИЕ ПРАВИЛА БЕЗОПАСНОСТИ", "ОПБ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("ПРАВИЛА ЯДЕРНОЙ БЕЗОПАСНОСТИ", "ПБЯ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new102("СТАНДАРТ ОРГАНИЗАЦИИ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("СТО", False)
        t.add_variant("STO", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("ПРАВИЛА ПО ОХРАНЕ ТРУДА", "ПОТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ПРАВИЛА ОХРАНЫ ТРУДА", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("ИНСТРУКЦИЯ ПО ОХРАНЕ ТРУДА", "ИОТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("ИНСТРУКЦИЯ ОХРАНЫ ТРУДА", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new948("РУКОВОДЯЩИЙ ДОКУМЕНТ", "РД", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new102("САНИТАРНЫЕ НОРМЫ И ПРАВИЛА", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.add_variant("САНПИН", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new126("ТЕХНИЧЕСКОЕ ЗАДАНИЕ", DecreeToken.ItemType.TYP, "ТЗ")
        t.add_variant("ТЕХЗАДАНИЕ", False)
        t.add_abridge("ТЕХ. ЗАДАНИЕ")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new95("ТЕХНИКО КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ", "ТКП")
        t.add_variant("КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ", False)
        DecreeToken.M_KEYWORDS.add(t)
    
    @staticmethod
    def is_keyword(t : 'Token', is_misc_type_only : bool=False) -> 'Token':
        if (t is None): 
            return None
        tok = DecreeToken.M_KEYWORDS.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            if (is_misc_type_only and tok.termin.tag is not None): 
                return None
            tok.end_token.tag = (tok.termin.canonic_text)
            return tok.end_token
        if (not t.morph.class0_.is_adjective and not t.morph.class0_.is_pronoun): 
            return None
        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
        if (npt is None or npt.begin_token == npt.end_token): 
            if ((t.is_value("НАСТОЯЩИЙ", "СПРАВЖНІЙ") or t.is_value("НАЗВАННЫЙ", "НАЗВАНИЙ") or t.is_value("ДАННЫЙ", "ДАНИЙ")) or ((t.get_morph_class_in_dictionary().is_verb and t.get_morph_class_in_dictionary().is_adjective))): 
                tok = DecreeToken.M_KEYWORDS.try_parse(t.next0_, TerminParseAttr.NO)
                if ((tok) is not None): 
                    tok.end_token.tag = (tok.termin.canonic_text)
                    return tok.end_token
            return None
        tok = DecreeToken.M_KEYWORDS.try_parse(npt.end_token, TerminParseAttr.NO)
        if ((tok) is not None): 
            if (is_misc_type_only and tok.termin.tag is not None): 
                return None
            tok.end_token.tag = (tok.termin.canonic_text)
            return tok.end_token
        pp = PartToken.try_attach(npt.end_token, None, False, True)
        if (pp is not None): 
            return pp.end_token
        return None
    
    @staticmethod
    def is_keyword_str(word : str, is_misc_type_only : bool=False) -> bool:
        if (not is_misc_type_only): 
            if (word in DecreeToken.M_ALL_TYPESRU or word in DecreeToken.M_ALL_TYPESUA): 
                return True
        if (word in DecreeToken.M_MISC_TYPESRU or word in DecreeToken.M_MISC_TYPESUA): 
            return True
        return False
    
    @staticmethod
    def add_new_type(typ_ : str, acronym : str=None) -> None:
        """ Добавить новый тип НПА
        
        Args:
            typ_(str): 
            acronym(str): 
        """
        t = Termin._new126(typ_, DecreeToken.ItemType.TYP, acronym)
        DecreeToken.M_TERMINS.add(t)
        DecreeToken.M_KEYWORDS.add(Termin._new100(typ_, DecreeToken.ItemType.TYP))
    
    M_ALL_TYPESRU = None
    
    M_ALL_TYPESUA = None
    
    M_MISC_TYPESRU = None
    
    M_MISC_TYPESUA = None
    
    M_STD_ADJECTIVES = None
    
    M_EMPTY_ADJECTIVES = None
    
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
        if (((((typ_ == "ГОСТ" or typ_ == "ОСТ" or typ_ == "ISO") or typ_ == "СНИП" or typ_ == "RFC") or "НОРМЫ" in typ_ or "ПРАВИЛА" in typ_) or "УСЛОВИЯ" in typ_ or "СТАНДАРТ" in typ_) or typ_ == "РУКОВОДЯЩИЙ ДОКУМЕНТ" or typ_ == "АВОК"): 
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
    def _new842(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new845(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str) -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new847(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'ReferentToken') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        return res
    
    @staticmethod
    def _new851(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'ReferentToken', _arg5 : str) -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new868(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : int) -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.num_year = _arg5
        return res
    
    @staticmethod
    def _new870(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'ReferentToken', _arg5 : 'MorphCollection') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new871(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : 'MorphCollection') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new872(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : 'MorphCollection', _arg6 : bool) -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.morph = _arg5
        res.is_doubtful = _arg6
        return res
    
    @staticmethod
    def _new879(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'MorphCollection') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.value = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new890(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'MorphCollection', _arg5 : str) -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.value = _arg5
        return res
    
    # static constructor for class DecreeToken
    @staticmethod
    def _static_ctor():
        DecreeToken.M_ALL_TYPESRU = list(["УКАЗ", "УКАЗАНИЕ", "ПОСТАНОВЛЕНИЕ", "РАСПОРЯЖЕНИЕ", "ПРИКАЗ", "ДИРЕКТИВА", "ПИСЬМО", "ЗАПИСКА", "ИНФОРМАЦИОННОЕ ПИСЬМО", "ИНСТРУКЦИЯ", "ЗАКОН", "КОДЕКС", "КОНСТИТУЦИЯ", "РЕШЕНИЕ", "ПОЛОЖЕНИЕ", "РАСПОРЯЖЕНИЕ", "ПОРУЧЕНИЕ", "РЕЗОЛЮЦИЯ", "ДОГОВОР", "СУБДОГОВОР", "АГЕНТСКИЙ ДОГОВОР", "ДОВЕРЕННОСТЬ", "КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ", "КОНТРАКТ", "ГОСУДАРСТВЕННЫЙ КОНТРАКТ", "ОПРЕДЕЛЕНИЕ", "ПРИГОВОР", "СОГЛАШЕНИЕ", "ПРОТОКОЛ", "ЗАЯВЛЕНИЕ", "УВЕДОМЛЕНИЕ", "РАЗЪЯСНЕНИЕ", "УСТАВ", "ХАРТИЯ", "КОНВЕНЦИЯ", "ПАКТ", "БИЛЛЬ", "ДЕКЛАРАЦИЯ", "РЕГЛАМЕНТ", "ТЕЛЕГРАММА", "ТЕЛЕФОНОГРАММА", "ТЕЛЕФАКСОГРАММА", "ТЕЛЕТАЙПОГРАММА", "ФАКСОГРАММА", "ОТВЕТЫ НА ВОПРОСЫ", "ВЫПИСКА ИЗ ПРОТОКОЛА", "ЗАКЛЮЧЕНИЕ", "ДЕКРЕТ"])
        DecreeToken.M_ALL_TYPESUA = list(["УКАЗ", "НАКАЗ", "ПОСТАНОВА", "РОЗПОРЯДЖЕННЯ", "НАКАЗ", "ДИРЕКТИВА", "ЛИСТ", "ЗАПИСКА", "ІНФОРМАЦІЙНИЙ ЛИСТ", "ІНСТРУКЦІЯ", "ЗАКОН", "КОДЕКС", "КОНСТИТУЦІЯ", "РІШЕННЯ", "ПОЛОЖЕННЯ", "РОЗПОРЯДЖЕННЯ", "ДОРУЧЕННЯ", "РЕЗОЛЮЦІЯ", "ДОГОВІР", "СУБКОНТРАКТ", "АГЕНТСЬКИЙ ДОГОВІР", "ДОРУЧЕННЯ", "КОМЕРЦІЙНА ПРОПОЗИЦІЯ", "КОНТРАКТ", "ДЕРЖАВНИЙ КОНТРАКТ", "ВИЗНАЧЕННЯ", "ВИРОК", "УГОДА", "ПРОТОКОЛ", "ЗАЯВА", "ПОВІДОМЛЕННЯ", "РОЗ'ЯСНЕННЯ", "СТАТУТ", "ХАРТІЯ", "КОНВЕНЦІЯ", "ПАКТ", "БІЛЛЬ", "ДЕКЛАРАЦІЯ", "РЕГЛАМЕНТ", "ТЕЛЕГРАМА", "ТЕЛЕФОНОГРАМА", "ТЕЛЕФАКСОГРАММА", "ТЕЛЕТАЙПОГРАМА", "ФАКСОГРАМА", "ВІДПОВІДІ НА ЗАПИТАННЯ", "ВИТЯГ З ПРОТОКОЛУ", "ВИСНОВОК", "ДЕКРЕТ"])
        DecreeToken.M_MISC_TYPESRU = list(["ПРАВИЛО", "ПРОГРАММА", "ПЕРЕЧЕНЬ", "ПОСОБИЕ", "РЕКОМЕНДАЦИЯ", "НАСТАВЛЕНИЕ", "СТАНДАРТ", "СОГЛАШЕНИЕ", "МЕТОДИКА", "ТРЕБОВАНИЕ", "ПОЛОЖЕНИЕ", "СПИСОК", "ЛИСТ", "ТАБЛИЦА", "ЗАЯВКА", "АКТ", "ФОРМА", "НОРМАТИВ", "ПОРЯДОК", "ИНФОРМАЦИЯ", "НОМЕНКЛАТУРА", "ОСНОВА", "ОБЗОР", "КОНЦЕПЦИЯ", "СТРАТЕГИЯ", "СТРУКТУРА", "УСЛОВИЕ", "КЛАССИФИКАТОР", "ОБЩЕРОССИЙСКИЙ КЛАССИФИКАТОР", "СПЕЦИФИКАЦИЯ", "ОБРАЗЕЦ"])
        DecreeToken.M_MISC_TYPESUA = list(["ПРАВИЛО", "ПРОГРАМА", "ПЕРЕЛІК", "ДОПОМОГА", "РЕКОМЕНДАЦІЯ", "ПОВЧАННЯ", "СТАНДАРТ", "УГОДА", "МЕТОДИКА", "ВИМОГА", "ПОЛОЖЕННЯ", "СПИСОК", "ТАБЛИЦЯ", "ЗАЯВКА", "АКТ", "ФОРМА", "НОРМАТИВ", "ПОРЯДОК", "ІНФОРМАЦІЯ", "НОМЕНКЛАТУРА", "ОСНОВА", "ОГЛЯД", "КОНЦЕПЦІЯ", "СТРАТЕГІЯ", "СТРУКТУРА", "УМОВА", "КЛАСИФІКАТОР", "ЗАГАЛЬНОРОСІЙСЬКИЙ КЛАСИФІКАТОР", "СПЕЦИФІКАЦІЯ", "ЗРАЗОК"])
        DecreeToken.M_STD_ADJECTIVES = list(["ВСЕОБЩИЙ", "МЕЖДУНАРОДНЫЙ", "ЗАГАЛЬНИЙ", "МІЖНАРОДНИЙ", "НОРМАТИВНЫЙ", "НОРМАТИВНИЙ", "КАССАЦИОННЫЙ", "АПЕЛЛЯЦИОННЫЙ", "КАСАЦІЙНИЙ", "АПЕЛЯЦІЙНИЙ"])
        DecreeToken.M_EMPTY_ADJECTIVES = list(["НЫНЕШНИЙ", "ПРЕДЫДУЩИЙ", "ДЕЙСТВУЮЩИЙ", "НАСТОЯЩИЙ", "НИНІШНІЙ", "ПОПЕРЕДНІЙ", "СПРАВЖНІЙ"])

DecreeToken._static_ctor()