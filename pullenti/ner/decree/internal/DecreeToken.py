# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import datetime
import typing
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.decree.DecreeKind import DecreeKind
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
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
        OWNER = 0 + 1
        DATE = (0 + 1) + 1
        EDITION = ((0 + 1) + 1) + 1
        NUMBER = (((0 + 1) + 1) + 1) + 1
        NAME = ((((0 + 1) + 1) + 1) + 1) + 1
        STDNAME = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
        TERR = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
        ORG = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        UNKNOWN = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        MISC = (((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        DECREEREF = ((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        DATERANGE = (((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        BETWEEN = ((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        READING = (((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        
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
        if (self.begin_token.isValue("ДЕЛО", "СПРАВА")): 
            return True
        if (self.begin_token.next0_ is not None and self.begin_token.next0_.isValue("ДЕЛО", "СПРАВА")): 
            return True
        return False
    
    def __str__(self) -> str:
        v = self.value
        if (v is None): 
            v = self.ref.referent.toString(True, self.kit.base_language, 0)
        return "{0} {1} {2}".format(Utils.enumToString(self.typ), v, Utils.ifNotNull(self.full_value, ""))
    
    @staticmethod
    def tryAttach(t : 'Token', prev : 'DecreeToken'=None, must_by_typ : bool=False) -> 'DecreeToken':
        """ Привязать с указанной позиции один примитив
        
        Args:
            cnt: 
            indFrom: 
        
        """
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.decree.internal.DecreeChangeToken import DecreeChangeToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        if (t is None): 
            return None
        if (t.isValue("НАЗВАННЫЙ", None)): 
            pass
        if (t.kit.is_recurce_overflow): 
            return None
        t.kit.recurse_level += 1
        res = DecreeToken.__TryAttach(t, prev, 0, must_by_typ)
        t.kit.recurse_level -= 1
        if (res is None): 
            if (t.is_hiphen): 
                res = DecreeToken.__TryAttach(t.next0_, prev, 0, must_by_typ)
                if (res is not None and res.typ == DecreeToken.ItemType.NAME): 
                    res.begin_token = t
                    return res
            if (t.isValue("ПРОЕКТ", None)): 
                res = DecreeToken.__TryAttach(t.next0_, prev, 0, False)
                if (res is not None and res.typ == DecreeToken.ItemType.TYP and res.value is not None): 
                    if ("ЗАКОН" in res.value or not ((isinstance(res.end_token, TextToken)))): 
                        res.value = "ПРОЕКТ ЗАКОНА"
                    else: 
                        res.value = ("ПРОЕКТ " + (Utils.asObjectOrNull(res.end_token, TextToken)).term)
                    res.begin_token = t
                    return res
                elif (res is not None and res.typ == DecreeToken.ItemType.NUMBER): 
                    res1 = DecreeToken.__TryAttach(res.end_token.next0_, prev, 0, False)
                    if (res1 is not None and res1.typ == DecreeToken.ItemType.TYP and (isinstance(res1.end_token, TextToken))): 
                        res = DecreeToken._new842(t, t, DecreeToken.ItemType.TYP)
                        res.value = ("ПРОЕКТ " + (Utils.asObjectOrNull(res1.end_token, TextToken)).term)
                        return res
            if (t.isValue("ИНФОРМАЦИЯ", "ІНФОРМАЦІЯ") and (t.whitespaces_after_count < 3)): 
                dts = DecreeToken.tryAttachList(t.next0_, None, 10, False)
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
            npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                if ((npt.end_token.isValue("СОБРАНИЕ", None) or npt.end_token.isValue("УЧАСТНИК", None) or npt.end_token.isValue("СОБСТВЕННИК", None)) or npt.end_token.isValue("УЧРЕДИТЕЛЬ", None)): 
                    res = DecreeToken._new842(t, npt.end_token, DecreeToken.ItemType.OWNER)
                    npt2 = NounPhraseHelper.tryParse(res.end_token.next0_, NounPhraseParseAttr.NO, 0)
                    if (npt2 is not None and npt2.morph.case_.is_genitive): 
                        res.end_token = npt2.end_token
                    res.value = MiscHelper.getTextValue(t, res.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
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
            first_pass2850 = True
            while True:
                if first_pass2850: first_pass2850 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (not tt.is_comma_and or tt.is_newline_before): 
                    break
                tt = tt.next0_
                if (not ((isinstance(tt, NumberToken)))): 
                    break
                if (tt.whitespaces_before_count > 2): 
                    break
                ddd = DecreeToken.__TryAttach(tt, res, 0, False)
                if (ddd is not None): 
                    if (ddd.typ != DecreeToken.ItemType.NUMBER): 
                        break
                    if (res.children is None): 
                        res.children = list()
                    res.children.append(ddd)
                    res.end_token = ddd.end_token
                    continue
                if ((Utils.asObjectOrNull(tt, NumberToken)).value > (1970)): 
                    break
                if (tt.is_whitespace_after): 
                    pass
                elif (not tt.next0_.isCharOf(",.")): 
                    pass
                else: 
                    break
                tmp = io.StringIO()
                tee = DecreeToken.__tryAttachNumber(tt, tmp, True)
                if (res.children is None): 
                    res.children = list()
                add = DecreeToken._new845(tt, tee, DecreeToken.ItemType.NUMBER, Utils.toStringStringIO(tmp))
                res.children.append(add)
                tt = tee
                res.end_token = tt
        if (res.typ != DecreeToken.ItemType.TYP): 
            return res
        if (res.begin_token == res.end_token): 
            tok = DecreeToken.M_TERMINS.tryParse(res.begin_token.previous, TerminParseAttr.NO)
            if (tok is not None and (isinstance(tok.termin.tag, DecreeToken.ItemType)) and tok.end_token == res.end_token): 
                if ((Utils.valToEnum(tok.termin.tag, DecreeToken.ItemType)) == DecreeToken.ItemType.TYP): 
                    return None
        if (((prev is not None and prev.typ == DecreeToken.ItemType.TYP and prev.value is not None) and (("ДОГОВОР" in prev.value or "ДОГОВІР" in prev.value)) and res.value is not None) and not "ДОГОВОР" in res.value and not "ДОГОВІР" in res.value): 
            return None
        for e0_ in DecreeToken.M_EMPTY_ADJECTIVES: 
            if (t.isValue(e0_, None)): 
                res = DecreeToken.__TryAttach(t.next0_, prev, 0, False)
                if (res is None or res.typ != DecreeToken.ItemType.TYP): 
                    return None
                break
        if (res.end_token.next0_ is not None and res.end_token.next0_.isChar('(')): 
            res1 = DecreeToken.__TryAttach(res.end_token.next0_, prev, 0, False)
            if (res1 is not None and res1.end_token.isChar(')')): 
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
                cha = DecreeChangeToken.tryAttach(tt, None, False, None, False)
                if (cha is not None): 
                    break
                if (tt == t1.next0_ and res.begin_token.previous is not None and res.begin_token.previous.isValue("НАСТОЯЩИЙ", "СПРАВЖНІЙ")): 
                    break
                if (not ((isinstance(tt, TextToken)))): 
                    break
                if (tt == t1.next0_ and tt.isValue("ЗАКОН", None)): 
                    if (tt.next0_ is not None and ((tt.next0_.isValue("О", None) or tt.next0_.isValue("ПРО", None)))): 
                        npt0 = NounPhraseHelper.tryParse(tt.next0_.next0_, NounPhraseParseAttr.NO, 0)
                        if (npt0 is None or not npt0.morph.case_.is_prepositional): 
                            break
                        t1 = npt0.end_token
                        break
                ooo = False
                if (tt.morph.class0_.is_preposition and tt.next0_ is not None): 
                    if (tt.isValue("ПО", None)): 
                        tt = tt.next0_
                    elif (tt.isValue("О", None) or tt.isValue("ОБ", None) or tt.isValue("ПРО", None)): 
                        ooo = True
                        tt = tt.next0_
                npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
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
                        npt = NounPhraseHelper.tryParse(ttt.next0_, NounPhraseParseAttr.NO, 0)
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
                res.full_value = MiscHelper.getTextValueOfMetaToken(res, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
        if (res.value is not None and ((res.value.startswith("ВЕДОМОСТИ СЪЕЗДА") or res.value.startswith("ВІДОМОСТІ ЗЇЗДУ")))): 
            tt = res.end_token.next0_
            if (tt is not None and (isinstance(tt.getReferent(), GeoReferent))): 
                res.ref = (Utils.asObjectOrNull(tt, ReferentToken))
                res.end_token = tt
                tt = tt.next0_
            if (tt is not None and tt.is_and): 
                tt = tt.next0_
            if (tt is not None and (isinstance(tt.getReferent(), OrganizationReferent))): 
                res.end_token = tt
                tt = tt.next0_
        return res
    
    @staticmethod
    def __TryAttach(t : 'Token', prev : 'DecreeToken', lev : int, must_by_typ : bool=False) -> 'DecreeToken':
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
            while t.isCharOf(":-") and t.next0_ is not None and not t.is_newline_after:
                t = t.next0_
        if (prev is not None): 
            if (t.isValue("ПРИ", "ЗА") and t.next0_ is not None): 
                t = t.next0_
        if ((not must_by_typ and t.isValue("МЕЖДУ", "МІЖ") and (isinstance(t.next0_, ReferentToken))) and t.next0_.next0_ is not None): 
            t11 = t.next0_.next0_
            is_br = False
            if ((t11.isChar('(') and (isinstance(t11.next0_, TextToken)) and t11.next0_.next0_ is not None) and t11.next0_.next0_.isChar(')')): 
                t11 = t11.next0_.next0_.next0_
                is_br = True
            if (t11 is not None and t11.is_comma_and and (isinstance(t11.next0_, ReferentToken))): 
                rr = DecreeToken._new842(t, t11.next0_, DecreeToken.ItemType.BETWEEN)
                rr.children = list()
                rr.children.append(DecreeToken._new847(t.next0_, t.next0_, DecreeToken.ItemType.OWNER, Utils.asObjectOrNull(t.next0_, ReferentToken)))
                rr.children.append(DecreeToken._new847(t11.next0_, t11.next0_, DecreeToken.ItemType.OWNER, Utils.asObjectOrNull(t11.next0_, ReferentToken)))
                t = rr.end_token.next0_
                first_pass2851 = True
                while True:
                    if first_pass2851: first_pass2851 = False
                    else: t = t.next0_
                    if (not (t is not None)): break
                    if ((is_br and t.isChar('(') and (isinstance(t.next0_, TextToken))) and t.next0_.next0_ is not None and t.next0_.next0_.isChar(')')): 
                        t = t.next0_.next0_
                        rr.end_token = t
                        rr.children[len(rr.children) - 1].end_token = t
                        continue
                    if ((t.is_comma_and and t.next0_ is not None and (isinstance(t.next0_, ReferentToken))) and not ((isinstance(t.next0_.getReferent(), DateReferent)))): 
                        rr.children.append(DecreeToken._new847(t.next0_, t.next0_, DecreeToken.ItemType.OWNER, Utils.asObjectOrNull(t.next0_, ReferentToken)))
                        rr.end_token = t.next0_
                        t = rr.end_token
                        continue
                    break
                return rr
        r = t.getReferent()
        if (isinstance(r, OrganizationReferent)): 
            rt = Utils.asObjectOrNull(t, ReferentToken)
            org0_ = Utils.asObjectOrNull(r, OrganizationReferent)
            res1 = None
            if (org0_.containsProfile(OrgProfile.MEDIA)): 
                tt1 = rt.begin_token
                if (BracketHelper.canBeStartOfSequence(tt1, False, False)): 
                    tt1 = tt1.next0_
                res1 = DecreeToken.__TryAttach(tt1, prev, lev + 1, False)
                if (res1 is not None and res1.typ == DecreeToken.ItemType.TYP): 
                    res1.begin_token = res1.end_token = t
                else: 
                    res1 = (None)
            if (res1 is None and org0_.containsProfile(OrgProfile.PRESS)): 
                res1 = DecreeToken._new842(t, t, DecreeToken.ItemType.TYP)
                res1.value = MiscHelper.getTextValueOfMetaToken((Utils.asObjectOrNull(t, ReferentToken)), GetTextAttr.NO)
            if (res1 is not None): 
                t11 = res1.end_token
                if (isinstance(t11.getReferent(), GeoReferent)): 
                    res1.ref = (Utils.asObjectOrNull(t11, ReferentToken))
                elif (isinstance(t11, MetaToken)): 
                    t11 = (Utils.asObjectOrNull(t11, MetaToken)).end_token
                if (isinstance(t11.getReferent(), GeoReferent)): 
                    res1.ref = (Utils.asObjectOrNull(t11, ReferentToken))
                elif (BracketHelper.isBracket(t11, False) and (isinstance(t11.previous.getReferent(), GeoReferent))): 
                    res1.ref = (Utils.asObjectOrNull(t11.previous, ReferentToken))
                return res1
        if (r is not None and not must_by_typ): 
            if (isinstance(r, GeoReferent)): 
                return DecreeToken._new851(t, t, DecreeToken.ItemType.TERR, Utils.asObjectOrNull(t, ReferentToken), r.toString(True, t.kit.base_language, 0))
            if (isinstance(r, DateReferent)): 
                if (prev is not None and prev.typ == DecreeToken.ItemType.TYP and prev.typ_kind == DecreeKind.STANDARD): 
                    ree = DecreeToken.tryAttach((Utils.asObjectOrNull(t, ReferentToken)).begin_token, prev, False)
                    if ((ree is not None and ree.typ == DecreeToken.ItemType.NUMBER and ree.num_year > 0) and ((ree.end_token == (Utils.asObjectOrNull(t, ReferentToken)).end_token or ree.end_token.isChar('*')))): 
                        if ((isinstance(t.next0_, TextToken)) and t.next0_.isChar('*')): 
                            t = t.next0_
                        ree.begin_token = ree.end_token = t
                        return ree
                if (t.previous is not None and t.previous.morph.class0_.is_preposition and t.previous.isValue("ДО", None)): 
                    return None
                return DecreeToken._new847(t, t, DecreeToken.ItemType.DATE, Utils.asObjectOrNull(t, ReferentToken))
            if (isinstance(r, OrganizationReferent)): 
                if ((t.next0_ is not None and t.next0_.isValue("В", "У") and t.next0_.next0_ is not None) and t.next0_.next0_.isValue("СОСТАВ", "СКЛАДІ")): 
                    return None
                return DecreeToken._new851(t, t, DecreeToken.ItemType.ORG, Utils.asObjectOrNull(t, ReferentToken), str(r))
            if (isinstance(r, PersonReferent)): 
                ok = False
                if (prev is not None and ((prev.typ == DecreeToken.ItemType.TYP or prev.typ == DecreeToken.ItemType.DATE))): 
                    ok = True
                elif (t.next0_ is not None and (isinstance(t.next0_.getReferent(), DecreeReferent))): 
                    ok = True
                else: 
                    ne = DecreeToken.__TryAttach(t.next0_, None, lev + 1, False)
                    if (ne is not None and ((ne.typ == DecreeToken.ItemType.TYP or ne.typ == DecreeToken.ItemType.DATE or ne.typ == DecreeToken.ItemType.OWNER))): 
                        ok = True
                if (ok): 
                    prop = Utils.asObjectOrNull(r.getSlotValue(PersonReferent.ATTR_ATTR), PersonPropertyReferent)
                    if (prop is not None and prop.kind == PersonPropertyKind.BOSS): 
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
            if (t.isValue("ОТ", "ВІД") or t.isValue("ПРИНЯТЬ", "ПРИЙНЯТИ")): 
                tdat = t.next0_
            elif (t.isValue("ВВЕСТИ", None) or t.isValue("ВВОДИТЬ", "ВВОДИТИ")): 
                tdat = t.next0_
                if (tdat is not None and tdat.isValue("В", "У")): 
                    tdat = tdat.next0_
                if (tdat is not None and tdat.isValue("ДЕЙСТВИЕ", "ДІЯ")): 
                    tdat = tdat.next0_
            if (tdat is not None): 
                if (tdat.next0_ is not None and tdat.morph.class0_.is_preposition): 
                    tdat = tdat.next0_
                if (isinstance(tdat.getReferent(), DateReferent)): 
                    return DecreeToken._new847(t, tdat, DecreeToken.ItemType.DATE, Utils.asObjectOrNull(tdat, ReferentToken))
                dr = t.kit.processReferent("DATE", tdat)
                if (dr is not None): 
                    return DecreeToken._new847(t, dr.end_token, DecreeToken.ItemType.DATE, dr)
            if (t.isValue("НА", None) and t.next0_ is not None and (isinstance(t.next0_.getReferent(), DateRangeReferent))): 
                return DecreeToken._new847(t, t.next0_, DecreeToken.ItemType.DATERANGE, Utils.asObjectOrNull(t.next0_, ReferentToken))
            if (t.isChar('(')): 
                tt = DecreeToken.__isEdition(t.next0_)
                if (tt is not None): 
                    br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        return DecreeToken._new842(t, br.end_token, DecreeToken.ItemType.EDITION)
                if (t.next0_ is not None and t.next0_.isValue("ПРОЕКТ", None)): 
                    return DecreeToken._new845(t.next0_, t.next0_, DecreeToken.ItemType.TYP, "ПРОЕКТ")
                if ((t.next0_ is not None and (isinstance(t.next0_.getReferent(), DateRangeReferent)) and t.next0_.next0_ is not None) and t.next0_.next0_.isChar(')')): 
                    return DecreeToken._new847(t, t.next0_.next0_, DecreeToken.ItemType.DATERANGE, Utils.asObjectOrNull(t.next0_, ReferentToken))
            else: 
                tt = DecreeToken.__isEdition(t)
                if (tt is not None): 
                    tt = tt.next0_
                if (tt is not None): 
                    xxx = DecreeToken.tryAttach(tt, None, False)
                    if (xxx is not None): 
                        return DecreeToken._new842(t, tt.previous, DecreeToken.ItemType.EDITION)
            if (isinstance(t, NumberToken)): 
                if (prev is not None and ((prev.typ == DecreeToken.ItemType.TYP or prev.typ == DecreeToken.ItemType.DATE))): 
                    tmp = io.StringIO()
                    t11 = DecreeToken.__tryAttachNumber(t, tmp, False)
                    if (t11 is not None): 
                        ne = DecreeToken.__TryAttach(t11.next0_, None, lev + 1, False)
                        valnum = Utils.toStringStringIO(tmp)
                        if (ne is not None and ((ne.typ == DecreeToken.ItemType.DATE or ne.typ == DecreeToken.ItemType.OWNER or ne.typ == DecreeToken.ItemType.NAME))): 
                            return DecreeToken._new845(t, t11, DecreeToken.ItemType.NUMBER, valnum)
                        if (LanguageHelper.endsWithEx(valnum, "ФЗ", "ФКЗ", None, None)): 
                            return DecreeToken._new845(t, t11, DecreeToken.ItemType.NUMBER, valnum)
                        year = 0
                        if (prev.typ == DecreeToken.ItemType.TYP): 
                            ok = False
                            if (prev.typ_kind == DecreeKind.STANDARD): 
                                ok = True
                                if (t11.next0_ is not None and t11.next0_.isChar('*')): 
                                    t11 = t11.next0_
                                if (Utils.endsWithString(valnum, "(E)", True)): 
                                    valnum = valnum[0:0+len(valnum) - 3].strip()
                                while True:
                                    if ((t11.whitespaces_after_count < 2) and (isinstance(t11.next0_, NumberToken))): 
                                        Utils.setLengthStringIO(tmp, 0)
                                        t22 = DecreeToken.__tryAttachNumber(t11.next0_, tmp, False)
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
                                        if (valnum[ii] != '-' and valnum[ii] != ':' and valnum[ii] != '.'): 
                                            break
                                        wrapnn866 = RefOutArgWrapper(0)
                                        Utils.tryParseInt(valnum[ii + 1:], wrapnn866)
                                        nn = wrapnn866.value
                                        if (nn > 50 and nn <= 99): 
                                            nn += 1900
                                        if (nn >= 1950 and nn <= datetime.datetime.now().year): 
                                            year = nn
                                            valnum = valnum[0:0+ii]
                                        break
                                valnum = valnum.replace('-', '.')
                                if (year < 1): 
                                    if (t11.next0_ is not None and t11.next0_.is_hiphen): 
                                        if (isinstance(t11.next0_.next0_, NumberToken)): 
                                            nn = (Utils.asObjectOrNull(t11.next0_.next0_, NumberToken)).value
                                            if (nn > 50 and nn <= 99): 
                                                nn += 1900
                                            if (nn >= 1950 and nn <= datetime.datetime.now().year): 
                                                year = nn
                                                t11 = t11.next0_.next0_
                            elif (prev.begin_token == prev.end_token and prev.begin_token.chars.is_all_upper and ((prev.begin_token.isValue("ФЗ", None) or prev.begin_token.isValue("ФКЗ", None)))): 
                                ok = True
                            if (ok): 
                                return DecreeToken._new867(t, t11, DecreeToken.ItemType.NUMBER, valnum, year)
                    val = (Utils.asObjectOrNull(t, NumberToken)).value
                    if (val > 1910 and (val < 2030)): 
                        return DecreeToken._new845(t, t, DecreeToken.ItemType.DATE, str(val))
                rt = t.kit.processReferent("PERSON", t)
                if (rt is not None): 
                    pr = Utils.asObjectOrNull(rt.referent, PersonPropertyReferent)
                    if (pr is not None): 
                        return DecreeToken._new869(rt.begin_token, rt.end_token, DecreeToken.ItemType.OWNER, rt, rt.morph)
                if (t.next0_ is not None and t.next0_.chars.is_letter): 
                    res1 = DecreeToken.__TryAttach(t.next0_, prev, lev + 1, False)
                    if (res1 is not None and res1.typ == DecreeToken.ItemType.OWNER): 
                        res1.begin_token = t
                        return res1
        if (not ((isinstance(t, TextToken)))): 
            return None
        toks = DecreeToken.M_TERMINS.tryParseAll(t, TerminParseAttr.NO)
        if (toks is not None): 
            for tok in toks: 
                if (tok.end_token.isChar('.') and tok.begin_token != tok.end_token): 
                    tok.end_token = tok.end_token.previous
                if (tok.termin.canonic_text == "РЕГИСТРАЦИЯ" or tok.termin.canonic_text == "РЕЄСТРАЦІЯ"): 
                    if (tok.end_token.next0_ is not None and ((tok.end_token.next0_.isValue("В", None) or tok.end_token.next0_.isValue("ПО", None)))): 
                        tok.end_token = tok.end_token.next0_
                doubt = False
                if ((tok.end_char - tok.begin_char) < 3): 
                    if (t.isValue("СП", None)): 
                        if (not ((isinstance(t.next0_, NumberToken)))): 
                            if (MiscHelper.checkNumberPrefix(t.next0_) is None): 
                                return None
                    doubt = True
                    if (tok.end_token.next0_ is None or not tok.chars.is_all_upper): 
                        pass
                    else: 
                        r = tok.end_token.next0_.getReferent()
                        if (isinstance(r, GeoReferent)): 
                            doubt = False
                if (tok.begin_token == tok.end_token and (tok.length_char < 4) and len(toks) > 1): 
                    cou = 0
                    tt = t.previous
                    first_pass2852 = True
                    while True:
                        if first_pass2852: first_pass2852 = False
                        else: tt = tt.previous; cou += 1
                        if (not (tt is not None and (cou < 500))): break
                        dr = Utils.asObjectOrNull(tt.getReferent(), DecreeReferent)
                        if (dr is None): 
                            continue
                        for tok1 in toks: 
                            if (dr.findSlot(DecreeReferent.ATTR_NAME, tok1.termin.canonic_text, True) is not None): 
                                return DecreeToken._new870(tok.begin_token, tok.end_token, Utils.valToEnum(tok1.termin.tag, DecreeToken.ItemType), tok1.termin.canonic_text, tok1.morph)
                    if (tok.begin_token.isValue("ТК", None) and tok.termin.canonic_text.startswith("ТРУД")): 
                        has_tamoz = False
                        cou = 0
                        tt = t.previous
                        while tt is not None and (cou < 500): 
                            if (tt.isValue("ТАМОЖНЯ", None) or tt.isValue("ТАМОЖЕННЫЙ", None) or tt.isValue("ГРАНИЦА", None)): 
                                has_tamoz = True
                                break
                            tt = tt.previous; cou += 1
                        if (has_tamoz): 
                            continue
                        cou = 0
                        tt = t.next0_
                        while tt is not None and (cou < 500): 
                            if (tt.isValue("ТАМОЖНЯ", None) or tt.isValue("ТАМОЖЕННЫЙ", None) or tt.isValue("ГРАНИЦА", None)): 
                                has_tamoz = True
                                break
                            tt = tt.next0_; cou += 1
                        if (has_tamoz): 
                            continue
                if (doubt and tok.chars.is_all_upper): 
                    if (PartToken.isPartBefore(tok.begin_token)): 
                        doubt = False
                    elif (tok.getSourceText().endswith("ТС")): 
                        doubt = False
                res = DecreeToken._new871(tok.begin_token, tok.end_token, Utils.valToEnum(tok.termin.tag, DecreeToken.ItemType), tok.termin.canonic_text, tok.morph, doubt)
                if (isinstance(tok.termin.tag2, DecreeKind)): 
                    res.typ_kind = (Utils.valToEnum(tok.termin.tag2, DecreeKind))
                if (res.value == "ГОСТ" and tok.end_token.next0_ is not None): 
                    if (tok.end_token.next0_.isValue("Р", None) or tok.end_token.next0_.isValue("P", None)): 
                        res.end_token = tok.end_token.next0_
                    else: 
                        g = Utils.asObjectOrNull(tok.end_token.next0_.getReferent(), GeoReferent)
                        if (g is not None and ((g.alpha2 == "RU" or g.alpha2 == "SU"))): 
                            res.end_token = tok.end_token.next0_
                if (res.value == "КОНСТИТУЦИЯ" and tok.end_token.next0_ is not None and tok.end_token.next0_.isChar('(')): 
                    npt = NounPhraseHelper.tryParse(tok.end_token.next0_.next0_, NounPhraseParseAttr.NO, 0)
                    if ((npt is not None and npt.end_token.isValue("ЗАКОН", None) and npt.end_token.next0_ is not None) and npt.end_token.next0_.isChar(')')): 
                        res.end_token = npt.end_token.next0_
                if ((isinstance(tok.termin.tag2, str)) and res.typ == DecreeToken.ItemType.TYP): 
                    res.full_value = tok.termin.canonic_text
                    res.value = (Utils.asObjectOrNull(tok.termin.tag2, str))
                    res.is_doubtful = False
                if (res.typ_kind == DecreeKind.STANDARD): 
                    cou = 0
                    tt = res.end_token.next0_
                    first_pass2853 = True
                    while True:
                        if first_pass2853: first_pass2853 = False
                        else: tt = tt.next0_; cou += 1
                        if (not (tt is not None and (cou < 3))): break
                        if (tt.whitespaces_before_count > 2): 
                            break
                        tok2 = DecreeToken.M_TERMINS.tryParse(tt, TerminParseAttr.NO)
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
                        if (tt.isCharOf("/\\") and (isinstance(tt.next0_, TextToken)) and tt.next0_.chars.is_all_upper): 
                            tt = tt.next0_
                            res.end_token = tt
                            continue
                        break
                    if (res.value == "СТАНДАРТ"): 
                        res.is_doubtful = True
                    if (res.is_doubtful and not res.is_newline_after): 
                        num1 = DecreeToken.tryAttach(res.end_token.next0_, res, False)
                        if (num1 is not None and num1.typ == DecreeToken.ItemType.NUMBER): 
                            if (num1.num_year > 0): 
                                res.is_doubtful = False
                    if (res.value == "СТАНДАРТ" and res.is_doubtful): 
                        return None
                return res
        if (((t.morph.class0_.is_adjective and ((t.isValue("УКАЗАННЫЙ", "ЗАЗНАЧЕНИЙ") or t.isValue("ВЫШЕУКАЗАННЫЙ", "ВИЩЕВКАЗАНИЙ") or t.isValue("НАЗВАННЫЙ", "НАЗВАНИЙ"))))) or ((t.morph.class0_.is_pronoun and (((t.isValue("ЭТОТ", "ЦЕЙ") or t.isValue("ТОТ", "ТОЙ") or t.isValue("ДАННЫЙ", "ДАНИЙ")) or t.isValue("САМЫЙ", "САМИЙ")))))): 
            t11 = t.next0_
            if (t11 is not None and t11.isValue("ЖЕ", None)): 
                t11 = t11.next0_
            nnn = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
            tok = DecreeToken.M_TERMINS.tryParse(t11, TerminParseAttr.NO)
            if ((tok) is not None): 
                if ((((tok.morph.number) & (MorphNumber.PLURAL))) == (MorphNumber.UNDEFINED) or ((nnn is not None and nnn.morph.number == MorphNumber.SINGULAR))): 
                    npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
                    if (npt is not None and (((npt.morph.number) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
                        pass
                    else: 
                        te = DecreeToken._findBackTyp(t.previous, tok.termin.canonic_text)
                        if (te is not None): 
                            return DecreeToken._new847(t, tok.end_token, DecreeToken.ItemType.DECREEREF, te)
        if (t.morph.class0_.is_adjective and t.isValue("НАСТОЯЩИЙ", "СПРАВЖНІЙ")): 
            tok = DecreeToken.M_TERMINS.tryParse(t.next0_, TerminParseAttr.NO)
            if ((tok) is not None): 
                return DecreeToken._new847(t, tok.end_token, DecreeToken.ItemType.DECREEREF, None)
        if (must_by_typ): 
            return None
        if (t.morph.class0_.is_adjective): 
            dt = DecreeToken.__TryAttach(t.next0_, prev, lev + 1, False)
            if (dt is not None and dt.ref is None): 
                rt = t.kit.processReferent("GEO", t)
                if (rt is not None): 
                    dt.ref = rt
                    dt.begin_token = t
                    return dt
            npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.internal_noun is not None): 
                npt = (None)
            if ((npt is not None and dt is not None and dt.typ == DecreeToken.ItemType.TYP) and dt.value == "КОДЕКС"): 
                dt.value = npt.getNormalCaseText(MorphClass(), True, MorphGender.UNDEFINED, False)
                dt.begin_token = t
                dt.is_doubtful = True
                return dt
            if (npt is not None and ((npt.end_token.isValue("ДОГОВОР", None) or npt.end_token.isValue("КОНТРАКТ", None)))): 
                dt = DecreeToken._new842(t, npt.end_token, DecreeToken.ItemType.TYP)
                dt.value = npt.getNormalCaseText(None, True, MorphGender.UNDEFINED, False)
                if (t.getMorphClassInDictionary().is_verb): 
                    dt.value = npt.end_token.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)
                return dt
            try_npt = False
            if (not t.chars.is_all_lower): 
                try_npt = True
            else: 
                for a in DecreeToken.M_STD_ADJECTIVES: 
                    if (t.isValue(a, None)): 
                        try_npt = True
                        break
            if (try_npt): 
                if (npt is not None): 
                    if (npt.end_token.isValue("ГАЗЕТА", None) or npt.end_token.isValue("БЮЛЛЕТЕНЬ", "БЮЛЕТЕНЬ")): 
                        return DecreeToken._new870(t, npt.end_token, DecreeToken.ItemType.TYP, npt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False), npt.morph)
                    if (len(npt.adjectives) > 0 and npt.end_token.getMorphClassInDictionary().is_noun): 
                        tok = DecreeToken.M_TERMINS.tryParse(npt.end_token, TerminParseAttr.NO)
                        if ((tok) is not None): 
                            if (npt.begin_token.isValue("ОБЩИЙ", "ЗАГАЛЬНИЙ")): 
                                return None
                            return DecreeToken._new876(npt.begin_token, tok.end_token, npt.getNormalCaseText(MorphClass(), True, MorphGender.UNDEFINED, False), npt.morph)
                    if (prev is not None and prev.typ == DecreeToken.ItemType.TYP): 
                        if (npt.end_token.isValue("КОЛЛЕГИЯ", "КОЛЕГІЯ")): 
                            res1 = DecreeToken._new870(t, npt.end_token, DecreeToken.ItemType.OWNER, npt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False), npt.morph)
                            t = npt.end_token.next0_
                            first_pass2854 = True
                            while True:
                                if first_pass2854: first_pass2854 = False
                                else: t = t.next0_
                                if (not (t is not None)): break
                                if (t.is_and or t.morph.class0_.is_preposition): 
                                    continue
                                re = t.getReferent()
                                if ((isinstance(re, GeoReferent)) or (isinstance(re, OrganizationReferent))): 
                                    res1.end_token = t
                                    continue
                                elif (re is not None): 
                                    break
                                dt1 = DecreeToken.__TryAttach(t, res1, lev + 1, False)
                                if (dt1 is not None and dt1.typ != DecreeToken.ItemType.UNKNOWN): 
                                    if (dt1.typ != DecreeToken.ItemType.OWNER): 
                                        break
                                    res1.end_token = dt1.end_token
                                    t = res1.end_token
                                    continue
                                npt1 = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
                                if (npt1 is None): 
                                    break
                                res1.end_token = npt1.end_token
                                t = res1.end_token
                            if (res1.end_token != npt.end_token): 
                                res1.value = "{0} {1}".format(res1.value, MiscHelper.getTextValue(npt.end_token.next0_, res1.end_token, GetTextAttr.KEEPQUOTES))
                            return res1
        t1 = None
        t0 = t
        num = False
        t1 = MiscHelper.checkNumberPrefix(t)
        if ((t1) is not None): 
            num = True
        elif (DecreeToken.__isJusNumber(t)): 
            t1 = t
        if (t1 is not None): 
            if ((t1.whitespaces_before_count < 15) and ((not t1.is_newline_before or (isinstance(t1, NumberToken)) or DecreeToken.__isJusNumber(t1)))): 
                tmp = io.StringIO()
                t11 = DecreeToken.__tryAttachNumber(t1, tmp, num)
                if (t11 is not None): 
                    if (t11.next0_ is not None and t11.next0_.isValue("ДСП", None)): 
                        t11 = t11.next0_
                        print("ДСП", end="", file=tmp)
                    return DecreeToken._new845(t0, t11, DecreeToken.ItemType.NUMBER, Utils.toStringStringIO(tmp))
            if (t1.is_newline_before and num): 
                return DecreeToken._new842(t0, t1.previous, DecreeToken.ItemType.NUMBER)
        if (BracketHelper.canBeStartOfSequence(t, False, False)): 
            if (BracketHelper.canBeStartOfSequence(t, True, False) and ((((t.next0_.isValue("О", None) or t.next0_.isValue("ОБ", None) or t.next0_.isValue("ПРО", None)) or t.next0_.isValue("ПО", None) or t.chars.is_capital_upper) or ((prev is not None and (isinstance(t.next0_, TextToken)) and ((prev.typ == DecreeToken.ItemType.DATE or prev.typ == DecreeToken.ItemType.NUMBER))))))): 
                br = BracketHelper.tryParse(t, BracketParseAttr.CANCONTAINSVERBS, 200)
                if (br is not None): 
                    tt = br.end_token
                    if (tt.previous is not None and tt.previous.isChar('>')): 
                        tt = tt.previous
                    if ((tt.isChar('>') and (isinstance(tt.previous, NumberToken)) and tt.previous.previous is not None) and tt.previous.previous.isChar('<')): 
                        tt = tt.previous.previous.previous
                        if (tt is None or tt.begin_char <= br.begin_char): 
                            return None
                        br.end_token = tt
                    tt1 = DecreeToken._tryAttachStdChangeName(t.next0_)
                    if (tt1 is not None and tt1.end_char > br.end_char): 
                        br.end_token = tt1
                    else: 
                        tt = br.begin_token.next0_
                        while tt is not None and (tt.end_char < br.end_char): 
                            if (tt.isChar('(')): 
                                dt = DecreeToken.tryAttach(tt.next0_, None, False)
                                if (dt is None and BracketHelper.canBeStartOfSequence(tt.next0_, True, False)): 
                                    dt = DecreeToken.tryAttach(tt.next0_.next0_, None, False)
                                if (dt is not None and dt.typ == DecreeToken.ItemType.TYP): 
                                    if (DecreeToken.getKind(dt.value) == DecreeKind.PUBLISHER): 
                                        br.end_token = tt.previous
                                        break
                            tt = tt.next0_
                    return DecreeToken._new845(br.begin_token, br.end_token, DecreeToken.ItemType.NAME, MiscHelper.getTextValueOfMetaToken(br, GetTextAttr.NO))
                else: 
                    tt1 = DecreeToken._tryAttachStdChangeName(t.next0_)
                    if (tt1 is not None): 
                        return DecreeToken._new845(t, tt1, DecreeToken.ItemType.NAME, MiscHelper.getTextValue(t, tt1, GetTextAttr.NO))
            elif (t.isChar('(')): 
                br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    if (not t.next0_.isValue("ДАЛЕЕ", "ДАЛІ")): 
                        if ((br.end_char - br.begin_char) < 30): 
                            return DecreeToken._new845(br.begin_token, br.end_token, DecreeToken.ItemType.MISC, MiscHelper.getTextValueOfMetaToken(br, GetTextAttr.NO))
        if (t.inner_bool): 
            rt = t.kit.processReferent("PERSON", t)
            if (rt is not None): 
                pr = Utils.asObjectOrNull(rt.referent, PersonPropertyReferent)
                if (pr is None): 
                    return None
                if (pr.kind != PersonPropertyKind.UNDEFINED): 
                    pass
                elif (Utils.startsWithString(pr.name, "ГРАЖДАН", True) or Utils.startsWithString(pr.name, "ГРОМАДЯН", True)): 
                    return None
                return DecreeToken._new869(rt.begin_token, rt.end_token, DecreeToken.ItemType.OWNER, rt, rt.morph)
        if (t.isValue("О", None) or t.isValue("ОБ", None) or t.isValue("ПРО", None)): 
            et = None
            if ((t.next0_ is not None and t.next0_.isValue("ВНЕСЕНИЕ", "ВНЕСЕННЯ") and t.next0_.next0_ is not None) and t.next0_.next0_.isValue("ИЗМЕНЕНИЕ", "ЗМІНА")): 
                et = t.next0_
            elif (t.next0_ is not None and t.next0_.isValue("ПОПРАВКА", None)): 
                et = t.next0_
            elif (t.next0_ is not None and (isinstance(t.next0_.getReferent(), OrganizationReferent))): 
                et = t.next0_
            if (et is not None and et.next0_ is not None and et.next0_.morph.class0_.is_preposition): 
                et = et.next0_
            if (et is not None and et.next0_ is not None): 
                dts2 = DecreeToken.tryAttachList(et.next0_, None, 10, False)
                if (dts2 is not None and dts2[0].typ == DecreeToken.ItemType.TYP): 
                    et = dts2[0].end_token
                    if (len(dts2) > 1 and dts2[1].typ == DecreeToken.ItemType.TERR): 
                        et = dts2[1].end_token
                    return DecreeToken._new845(t, et, DecreeToken.ItemType.NAME, MiscHelper.getTextValue(t, et, GetTextAttr.NO))
                if (et.next0_.isCharOf(",(") or (isinstance(et, ReferentToken))): 
                    return DecreeToken._new845(t, et, DecreeToken.ItemType.NAME, MiscHelper.getTextValue(t, et, GetTextAttr.NO))
            elif (et is not None): 
                return DecreeToken._new845(t, et, DecreeToken.ItemType.NAME, MiscHelper.getTextValue(t, et, GetTextAttr.NO))
            return None
        if (t.isValue("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
            return None
        if (prev is not None and prev.typ == DecreeToken.ItemType.TYP): 
            if (t.isValue("ПРАВИТЕЛЬСТВО", "УРЯД") or t.isValue("ПРЕЗИДЕНТ", None)): 
                return DecreeToken._new887(t, t, DecreeToken.ItemType.OWNER, t.morph, t.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False))
        npt2 = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.PARSEPREPOSITION, 0)
        if (npt2 is not None): 
            if (npt2.end_token.isValue("ПОЗИЦИЯ", None)): 
                return None
        if ((((t.chars.is_cyrillic_letter and ((not t.chars.is_all_lower or ((prev is not None and prev.typ == DecreeToken.ItemType.UNKNOWN))))) or t.isValue("ЗАСЕДАНИЕ", "ЗАСІДАННЯ") or t.isValue("СОБРАНИЕ", "ЗБОРИ")) or t.isValue("ПЛЕНУМ", None) or t.isValue("КОЛЛЕГИЯ", "КОЛЕГІЯ")) or t.isValue("АДМИНИСТРАЦИЯ", "АДМІНІСТРАЦІЯ")): 
            ok = False
            if (prev is not None and ((prev.typ == DecreeToken.ItemType.TYP or prev.typ == DecreeToken.ItemType.OWNER or prev.typ == DecreeToken.ItemType.ORG))): 
                ok = True
            elif (prev is not None and prev.typ == DecreeToken.ItemType.UNKNOWN and not t.morph.class0_.is_verb): 
                ok = True
            elif (t.next0_ is not None and (isinstance(t.next0_.getReferent(), GeoReferent)) and not t.isValue("ИМЕНЕМ", None)): 
                ok = True
            elif ((t.previous is not None and t.previous.isChar(',') and t.previous.previous is not None) and (isinstance(t.previous.previous.getReferent(), DecreeReferent))): 
                ok = True
            if (ok): 
                if (PartToken.tryAttach(t, None, False, False) is not None): 
                    ok = False
            if (ok): 
                t1 = t
                ty = DecreeToken.ItemType.UNKNOWN
                tmp = io.StringIO()
                tt = t
                while tt is not None: 
                    if (not ((isinstance(tt, TextToken)))): 
                        org0_ = Utils.asObjectOrNull(tt.getReferent(), OrganizationReferent)
                        if (org0_ is not None and tt.previous == t1): 
                            ty = DecreeToken.ItemType.OWNER
                            if (tmp.tell() > 0): 
                                print(' ', end="", file=tmp)
                            print(tt.getSourceText().upper(), end="", file=tmp)
                            t1 = tt
                            break
                        break
                    if (tt.is_newline_before and tt != t1): 
                        break
                    if (not tt.chars.is_cyrillic_letter): 
                        break
                    if (tt != t): 
                        if (DecreeToken.__TryAttach(tt, None, lev + 1, False) is not None): 
                            break
                    npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
                    if (tt.chars.is_all_lower and tt != t): 
                        if (npt is not None and npt.morph.case_.is_genitive): 
                            pass
                        else: 
                            break
                    if (npt is not None): 
                        if (tmp.tell() > 0): 
                            print(" {0}".format(npt.getSourceText()), end="", file=tmp, flush=True)
                        else: 
                            print(npt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False), end="", file=tmp)
                        tt = npt.end_token
                        t1 = tt
                    elif (tmp.tell() > 0): 
                        print(" {0}".format(tt.getSourceText()), end="", file=tmp, flush=True)
                        t1 = tt
                    else: 
                        s = None
                        if (tt == t): 
                            s = tt.getNormalCaseText(MorphClass.NOUN, False, MorphGender.UNDEFINED, False)
                        if (s is None): 
                            s = (Utils.asObjectOrNull(tt, TextToken)).term
                        print(s, end="", file=tmp)
                        t1 = tt
                    tt = tt.next0_
                ss = MiscHelper.convertFirstCharUpperAndOtherLower(Utils.toStringStringIO(tmp))
                return DecreeToken._new845(t, t1, ty, ss)
        if (t.isValue("ДАТА", None)): 
            t1 = t.next0_
            if (t1 is not None and t1.morph.case_.is_genitive): 
                t1 = t1.next0_
            if (t1 is not None and t1.isChar(':')): 
                t1 = t1.next0_
            res1 = DecreeToken.__TryAttach(t1, prev, lev + 1, False)
            if (res1 is not None and res1.typ == DecreeToken.ItemType.DATE): 
                res1.begin_token = t
                return res1
        if (t.isValue("ВЕСТНИК", "ВІСНИК") or t.isValue("БЮЛЛЕТЕНЬ", "БЮЛЕТЕНЬ")): 
            npt = NounPhraseHelper.tryParse(t.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                return DecreeToken._new845(t, npt.end_token, DecreeToken.ItemType.TYP, MiscHelper.getTextValue(t, npt.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE))
            elif (t.next0_ is not None and (isinstance(t.next0_.getReferent(), OrganizationReferent))): 
                return DecreeToken._new845(t, t.next0_, DecreeToken.ItemType.TYP, MiscHelper.getTextValue(t, t.next0_, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE))
        if ((prev is not None and prev.typ == DecreeToken.ItemType.TYP and prev.value is not None) and (("ДОГОВОР" in prev.value or "ДОГОВІР" in prev.value))): 
            nn = DecreeToken.tryAttachName(t, prev.value, False, False)
            if (nn is not None): 
                return nn
            t1 = (None)
            ttt = t
            first_pass2855 = True
            while True:
                if first_pass2855: first_pass2855 = False
                else: ttt = ttt.next0_
                if (not (ttt is not None)): break
                if (ttt.is_newline_before): 
                    break
                ddt1 = DecreeToken.__TryAttach(ttt, None, lev + 1, False)
                if (ddt1 is not None): 
                    break
                if (ttt.morph.class0_.is_preposition or ttt.morph.class0_.is_conjunction): 
                    continue
                npt = NounPhraseHelper.tryParse(ttt, NounPhraseParseAttr.NO, 0)
                if (npt is None): 
                    break
                t1 = npt.end_token
                ttt = t1
            if (t1 is not None): 
                nn = DecreeToken._new842(t, t1, DecreeToken.ItemType.NAME)
                nn.value = MiscHelper.getTextValue(t, t1, GetTextAttr.NO)
                return nn
        if ((isinstance(t, TextToken)) and t.length_char == 1 and t.next0_ is not None): 
            if (((Utils.asObjectOrNull(t, TextToken)).term == "Б" and t.next0_.isCharOf("\\/") and (isinstance(t.next0_.next0_, TextToken))) and (Utils.asObjectOrNull(t.next0_.next0_, TextToken)).term == "Н"): 
                return DecreeToken._new845(t, t.next0_.next0_, DecreeToken.ItemType.NUMBER, "Б/Н")
        return None
    
    @staticmethod
    def __isJusNumber(t : 'Token') -> bool:
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return False
        if (tt.term != "A" and tt.term != "А"): 
            return False
        if ((isinstance(t.next0_, NumberToken)) and (t.whitespaces_after_count < 2)): 
            if ((Utils.asObjectOrNull(t.next0_, NumberToken)).value > (20)): 
                return True
            return False
        return False
    
    @staticmethod
    def __isEdition(t : 'Token') -> 'Token':
        from pullenti.ner.NumberToken import NumberToken
        if (t is None): 
            return None
        if (t.morph.class0_.is_preposition and t.next0_ is not None): 
            t = t.next0_
        if (t.isValue("РЕДАКЦИЯ", "РЕДАКЦІЯ") or t.isValue("РЕД", None)): 
            if (t.next0_ is not None and t.next0_.isChar('.')): 
                return t.next0_
            else: 
                return t
        if (t.isValue("ИЗМЕНЕНИЕ", "ЗМІНА")): 
            if ((t.next0_ is not None and t.next0_.is_comma and t.next0_.next0_ is not None) and t.next0_.next0_.isValue("ВНЕСЕННЫЙ", "ВНЕСЕНИЙ")): 
                return t.next0_.next0_
            return t
        if ((isinstance(t, NumberToken)) and t.next0_ is not None and t.next0_.isValue("ЧТЕНИЕ", "ЧИТАННЯ")): 
            return t.next0_.next0_
        return None
    
    @staticmethod
    def _findBackTyp(t : 'Token', type_name : str) -> 'ReferentToken':
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (t is None): 
            return None
        if (t.isValue("НАСТОЯЩИЙ", "СПРАВЖНІЙ")): 
            return None
        cou = 0
        tt = t
        first_pass2856 = True
        while True:
            if first_pass2856: first_pass2856 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            cou += 1
            if (tt.is_newline_before): 
                cou += 10
            if (cou > 500): 
                break
            d = Utils.asObjectOrNull(tt.getReferent(), DecreeReferent)
            if (d is None and (isinstance(tt.getReferent(), DecreePartReferent))): 
                d = (Utils.asObjectOrNull(tt.getReferent(), DecreePartReferent)).owner
            if (d is None): 
                continue
            if (d.typ0 == type_name or d.typ == type_name): 
                return Utils.asObjectOrNull(tt, ReferentToken)
        return None
    
    @staticmethod
    def __tryAttachNumber(t : 'Token', tmp : io.StringIO, after_num : bool) -> 'Token':
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
        first_pass2857 = True
        while True:
            if first_pass2857: first_pass2857 = False
            else: t2 = t2.next0_
            if (not (t2 is not None)): break
            if (t2.isCharOf("(),;")): 
                break
            if (t2.is_table_control_char): 
                break
            if (t2.isChar('.') and t2.is_whitespace_after): 
                break
            if (t2 != t and t2.whitespaces_before_count > 1): 
                break
            if (BracketHelper.isBracket(t2, False)): 
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
                dr = Utils.asObjectOrNull(t2.getReferent(), DateReferent)
                if (dr is not None and ((t2 == t or not t2.is_whitespace_before))): 
                    if (dr.year > 0 and t2.length_char == 4): 
                        res = t2
                        print(dr.year, end="", file=tmp)
                        digs = True
                        continue
                den = Utils.asObjectOrNull(t2.getReferent(), DenominationReferent)
                if (den is not None): 
                    res = t2
                    print(t2.getSourceText().upper(), end="", file=tmp)
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
            s = t2.getSourceText()
            if (s is None): 
                break
            if (t2.is_hiphen): 
                s = "-"
            if (t2.isValue("ОТ", "ВІД")): 
                break
            if (s == "\\"): 
                s = "/"
            if (str.isdigit(s[0])): 
                for d in s: 
                    digs = True
            if (not t2.isCharOf("_@")): 
                print(s, end="", file=tmp)
            res = t2
            if (t2.is_whitespace_after): 
                if (t2.whitespaces_after_count > 1): 
                    break
                if (digs): 
                    if ((t2.next0_ is not None and ((t2.next0_.is_hiphen or t2.next0_.isCharOf(".:"))) and not t2.next0_.is_whitespace_after) and (isinstance(t2.next0_.next0_, NumberToken))): 
                        continue
                if (not after_num): 
                    break
                if (t2.is_hiphen): 
                    if (t2.next0_ is not None and t2.next0_.isValue("СМ", None)): 
                        break
                    continue
                if (t2.isChar('/')): 
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
            if (t is not None and t.isChar('_')): 
                t2 = t
                while t2 is not None: 
                    if (not t2.isChar('_') or ((t2 != t and t2.is_whitespace_before))): 
                        print('?', end="", file=tmp)
                        return t2.previous
                    t2 = t2.next0_
            return None
        if (not digs and not after_num): 
            return None
        ch = Utils.getCharAtStringIO(tmp, tmp.tell() - 1)
        if (not str.isalnum(ch) and (isinstance(res, TextToken)) and not res.isChar('_')): 
            Utils.setLengthStringIO(tmp, tmp.tell() - 1)
            res = res.previous
        if (res.next0_ is not None and res.next0_.is_hiphen and (isinstance(res.next0_.next0_, NumberToken))): 
            wrapmin893 = RefOutArgWrapper(0)
            inoutres894 = Utils.tryParseInt(Utils.toStringStringIO(tmp), wrapmin893)
            min0_ = wrapmin893.value
            if (inoutres894): 
                if (min0_ < (Utils.asObjectOrNull(res.next0_.next0_, NumberToken)).value): 
                    res = res.next0_.next0_
                    print("-{0}".format((Utils.asObjectOrNull(res, NumberToken)).value), end="", file=tmp, flush=True)
        if (res.next0_ is not None and not res.is_whitespace_after and res.next0_.isChar('(')): 
            cou = 0
            tmp2 = io.StringIO()
            tt = res.next0_.next0_
            while tt is not None: 
                if (tt.isChar(')')): 
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
                print(tt.getSourceText(), end="", file=tmp2)
                tt = tt.next0_
        if (tmp.tell() > 2): 
            if (Utils.getCharAtStringIO(tmp, tmp.tell() - 1) == '3'): 
                if (Utils.getCharAtStringIO(tmp, tmp.tell() - 2) == 'К' or Utils.getCharAtStringIO(tmp, tmp.tell() - 2) == 'Ф'): 
                    Utils.setCharAtStringIO(tmp, tmp.tell() - 1, 'З')
        if ((isinstance(res.next0_, TextToken)) and (res.whitespaces_after_count < 2) and res.next0_.chars.is_all_upper): 
            if (res.next0_.isValue("РД", None) or res.next0_.isValue("ПД", None)): 
                print(" {0}".format((Utils.asObjectOrNull(res.next0_, TextToken)).term), end="", file=tmp, flush=True)
                res = res.next0_
        if ((isinstance(res.next0_, TextToken)) and res.next0_.isChar('*')): 
            res = res.next0_
        return res
    
    @staticmethod
    def tryAttachList(t : 'Token', prev : 'DecreeToken'=None, max_count : int=10, must_start_by_typ : bool=False) -> typing.List['DecreeToken']:
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
        p = DecreeToken.tryAttach(t, prev, must_start_by_typ)
        if (p is None): 
            return None
        if (p.typ == DecreeToken.ItemType.ORG or p.typ == DecreeToken.ItemType.OWNER): 
            if (t.previous is not None and t.previous.isValue("РАССМОТРЕНИЕ", "РОЗГЛЯД")): 
                return None
        res = list()
        res.append(p)
        tt = p.end_token.next0_
        if (tt is not None and t.previous is not None): 
            if (BracketHelper.canBeStartOfSequence(t.previous, False, False) and BracketHelper.canBeEndOfSequence(tt, False, None, False)): 
                p.begin_token = t.previous
                p.end_token = tt
                tt = tt.next0_
        first_pass2858 = True
        while True:
            if first_pass2858: first_pass2858 = False
            else: tt = tt.next0_
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
            p0 = DecreeToken.tryAttach(tt, Utils.ifNotNull(prev, p), False)
            if (ws): 
                if (p0 is not None and p is not None and ((((p.typ == DecreeToken.ItemType.TYP and p0.typ == DecreeToken.ItemType.NUMBER)) or ((p0.typ == DecreeToken.ItemType.NAME and p.typ != DecreeToken.ItemType.NAME)) or ((p0.typ == DecreeToken.ItemType.ORG and p.typ == DecreeToken.ItemType.ORG))))): 
                    pass
                else: 
                    break
            if (p0 is None): 
                if (tt.is_newline_before): 
                    break
                if (tt.morph.class0_.is_preposition and res[0].typ == DecreeToken.ItemType.TYP): 
                    continue
                if (((tt.is_comma_and or tt.is_hiphen)) and res[0].typ == DecreeToken.ItemType.TYP): 
                    p0 = DecreeToken.tryAttach(tt.next0_, p, False)
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
                    p0 = (None)
                if (tt.isChar(':')): 
                    p0 = DecreeToken.tryAttach(tt.next0_, p, False)
                    if (p0 is not None): 
                        if (p0.typ == DecreeToken.ItemType.NUMBER or p0.typ == DecreeToken.ItemType.DATE): 
                            p = p0
                            res.append(p)
                            tt = p.end_token
                            continue
                if (tt.is_comma and p.typ == DecreeToken.ItemType.NUMBER): 
                    p0 = DecreeToken.tryAttach(tt.next0_, p, False)
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
                                pp = DecreeToken.tryAttach(tt1.next0_, p, False)
                                if (pp is not None): 
                                    break
                                if (not ((isinstance(tt1.next0_, NumberToken)))): 
                                    break
                                Utils.setLengthStringIO(tmp, 0)
                                tt2 = DecreeToken.__tryAttachNumber(tt1.next0_, tmp, True)
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
                    p0 = DecreeToken.tryAttach(tt.next0_, p, False)
                    if (p0 is not None and p0.typ == DecreeToken.ItemType.NUMBER): 
                        p = p0
                        res.append(p)
                        tt = p.end_token
                        continue
                    p0 = (None)
                if (tt.is_comma_and and ((p.typ == DecreeToken.ItemType.ORG or p.typ == DecreeToken.ItemType.OWNER))): 
                    p0 = DecreeToken.tryAttach(tt.next0_, p, False)
                    if (p0 is not None and ((p0.typ == DecreeToken.ItemType.ORG or p.typ == DecreeToken.ItemType.OWNER))): 
                        p = p0
                        res.append(p)
                        tt = p.end_token
                        continue
                    p0 = (None)
                if (res[0].typ == DecreeToken.ItemType.TYP): 
                    if (DecreeToken.getKind(res[0].value) == DecreeKind.PUBLISHER): 
                        if (tt.isCharOf(",;")): 
                            continue
                        p = DecreeToken.tryAttach(tt, Utils.ifNotNull(prev, res[0]), False)
                        if ((p) is not None): 
                            res.append(p)
                            tt = p.end_token
                            continue
                if (res[len(res) - 1].typ == DecreeToken.ItemType.UNKNOWN and prev is not None): 
                    p0 = DecreeToken.tryAttach(tt, res[len(res) - 1], False)
                    if (p0 is not None): 
                        p = p0
                        res.append(p)
                        tt = p.end_token
                        continue
                if ((((isinstance(tt, TextToken)) and tt.chars.is_all_upper and BracketHelper.canBeStartOfSequence(tt.next0_, False, False)) and len(res) > 1 and res[len(res) - 1].typ == DecreeToken.ItemType.NUMBER) and res[len(res) - 2].typ == DecreeToken.ItemType.TYP and res[len(res) - 2].typ_kind == DecreeKind.STANDARD): 
                    continue
                if (tt.isChar('(')): 
                    p = DecreeToken.tryAttach(tt.next0_, None, False)
                    if (p is not None and p.typ == DecreeToken.ItemType.EDITION): 
                        br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                        if (br is not None): 
                            res.append(p)
                            tt = p.end_token.next0_
                            while tt is not None: 
                                if (tt.end_char >= br.end_char): 
                                    break
                                p = DecreeToken.tryAttach(tt, None, False)
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
                    elif (NumberExToken.tryParseNumberWithPostfix(tt) is not None): 
                        pass
                    else: 
                        tmp = io.StringIO()
                        t11 = DecreeToken.__tryAttachNumber(tt, tmp, False)
                        if (t11 is not None): 
                            p0 = DecreeToken._new845(tt, t11, DecreeToken.ItemType.NUMBER, Utils.toStringStringIO(tmp))
                if (p0 is None): 
                    break
            p = p0
            res.append(p)
            tt = p.end_token
        i = 0
        first_pass2859 = True
        while True:
            if first_pass2859: first_pass2859 = False
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
        first_pass2860 = True
        while True:
            if first_pass2860: first_pass2860 = False
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
                if (not te.isChar(',') or te.next0_ is None): 
                    break
                res1 = DecreeToken.tryAttachList(te.next0_, res[0], 10, False)
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
                res1 = DecreeToken.tryAttachList(te.next0_, res[0], 10, False)
                if (res1 is not None and len(res1) > 0): 
                    if (res1[0].typ == DecreeToken.ItemType.OWNER or res1[0].typ == DecreeToken.ItemType.ORG): 
                        res.extend(res1)
        return res
    
    @staticmethod
    def tryAttachName(t : 'Token', typ_ : str, very_probable : bool=False, in_title_doc_ref : bool=False) -> 'DecreeToken':
        from pullenti.ner.mail.internal.MailLine import MailLine
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
        if (t.isChar(';')): 
            t = t.next0_
        if (t is None): 
            return None
        li = MailLine.parse(t, 0)
        if (li is not None): 
            if (li.typ == MailLine.Types.HELLO): 
                return None
        t0 = t
        t1 = t
        abou = False
        ty = DecreeToken.getKind(typ_)
        if (t.isValue("О", None) or t.isValue("ОБ", None) or t.isValue("ПРО", None)): 
            t = t.next0_
            abou = True
        elif (t.isValue("ПО", None)): 
            if (LanguageHelper.endsWith(typ_, "ЗАКОН")): 
                return None
            t = t.next0_
            abou = True
            if (t is not None): 
                if (t.isValue("ПОЗИЦИЯ", None)): 
                    return None
        elif (t.next0_ is not None): 
            if (BracketHelper.canBeStartOfSequence(t, True, False)): 
                br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                if (br is not None and br.is_quote_type): 
                    re = t.next0_.getReferent()
                    if (re is not None and re.type_name == "URI"): 
                        return None
                    if (t.next0_.chars.is_letter): 
                        if (t.next0_.chars.is_all_lower or (((isinstance(t.next0_, TextToken)) and (Utils.asObjectOrNull(t.next0_, TextToken)).is_pure_verb))): 
                            return None
                    t1 = br.end_token
                    tt1 = DecreeToken._tryAttachStdChangeName(t.next0_)
                    if (tt1 is not None): 
                        t1 = tt1
                    s0 = MiscHelper.getTextValue(t0, t1, GetTextAttr.KEEPREGISTER)
                    if (Utils.isNullOrEmpty(s0)): 
                        return None
                    if ((len(s0) < 10) and typ_ != "ПРОГРАММА" and typ_ != "ПРОГРАМА"): 
                        return None
                    return DecreeToken._new845(t, t1, DecreeToken.ItemType.NAME, s0)
                dt = DecreeToken.tryAttachName(t.next0_, typ_, False, False)
                if (dt is not None): 
                    dt.begin_token = t
                    return dt
            if (ty != DecreeKind.KONVENTION and ty != DecreeKind.PROGRAM): 
                return None
        if (t is None): 
            return None
        if (t.isValue("ЗАЯВЛЕНИЕ", "ЗАЯВА")): 
            return None
        cou = 0
        tt = t
        first_pass2861 = True
        while True:
            if first_pass2861: first_pass2861 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_newline_before and tt != t): 
                if (tt.whitespaces_before_count > 15 or not abou): 
                    break
                if (tt.isValue("ИСТОЧНИК", None)): 
                    break
                if ((isinstance(tt, TextToken)) and tt.chars.is_letter and tt.chars.is_all_lower): 
                    pass
                else: 
                    break
            if (tt.isCharOf("(,") and tt.next0_ is not None): 
                if (tt.next0_.isValue("УТВЕРЖДЕННЫЙ", "ЗАТВЕРДЖЕНИЙ") or tt.next0_.isValue("ПРИНЯТЫЙ", "ПРИЙНЯТИЙ") or tt.next0_.isValue("УТВ", "ЗАТВ")): 
                    ttt = tt.next0_.next0_
                    if (ttt is not None and ttt.isChar('.') and tt.next0_.isValue("УТВ", None)): 
                        ttt = ttt.next0_
                    dt = DecreeToken.tryAttach(ttt, None, False)
                    if (dt is not None and dt.typ == DecreeToken.ItemType.TYP): 
                        break
                    if (dt is not None and ((dt.typ == DecreeToken.ItemType.ORG or dt.typ == DecreeToken.ItemType.OWNER))): 
                        dt2 = DecreeToken.tryAttach(dt.end_token.next0_, None, False)
                        if (dt2 is not None and dt2.typ == DecreeToken.ItemType.DATE): 
                            break
            if (very_probable and abou and not tt.is_newline_before): 
                t1 = tt
                continue
            if (tt.isValue("ОТ", "ВІД")): 
                dt = DecreeToken.tryAttach(tt, None, False)
                if (dt is not None): 
                    break
            if (tt.morph.class0_.is_preposition and tt.next0_ is not None and (((isinstance(tt.next0_.getReferent(), DateReferent)) or (isinstance(tt.next0_.getReferent(), DateRangeReferent))))): 
                break
            if (in_title_doc_ref): 
                t1 = tt
                continue
            if (tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction): 
                if (cou == 0): 
                    break
                if (tt.next0_ is None): 
                    break
                continue
            if (not tt.chars.is_cyrillic_letter): 
                break
            if (tt.morph.class0_.is_personal_pronoun or tt.morph.class0_.is_pronoun): 
                if (not tt.isValue("ВСЕ", "ВСІ") and not tt.isValue("ВСЯКИЙ", None) and not tt.isValue("ДАННЫЙ", "ДАНИЙ")): 
                    break
            if (isinstance(tt, NumberToken)): 
                break
            pit = PartToken.tryAttach(tt, None, False, False)
            if (pit is not None): 
                break
            r = tt.getReferent()
            if (r is not None): 
                if (((isinstance(r, DecreeReferent)) or (isinstance(r, DateReferent)) or (isinstance(r, OrganizationReferent))) or (isinstance(r, GeoReferent)) or r.type_name == "NAMEDENTITY"): 
                    if (tt.is_newline_before): 
                        break
                    t1 = tt
                    continue
            npt = NounPhraseHelper.tryParse(tt, Utils.valToEnum((NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.PARSEPREPOSITION), NounPhraseParseAttr), 0)
            if (npt is None): 
                break
            if (npt.internal_noun is not None): 
                if (DecreeToken.isKeyword(npt.internal_noun.end_token, False) is not None): 
                    npt = NounPhraseHelper.tryParse(tt, Utils.valToEnum((NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.PARSEPREPOSITION) | (NounPhraseParseAttr.CANNOTHASCOMMAAND), NounPhraseParseAttr), 0)
            dd = npt.end_token.getMorphClassInDictionary()
            if (dd.is_verb and npt.end_token == npt.begin_token): 
                if (not dd.is_noun): 
                    break
                if (tt.isValue("БЫТЬ", "БУТИ")): 
                    break
            if (not npt.morph.case_.is_genitive): 
                if (cou > 0): 
                    if ((npt.morph.case_.is_instrumental and tt.previous is not None and tt.previous.previous is not None) and ((tt.previous.previous.isValue("РАБОТА", "РОБОТА")))): 
                        pass
                    elif (abou and very_probable): 
                        pass
                    elif (npt.noun.isValue("ГОД", "РІК") or npt.noun.isValue("ПЕРИОД", "ПЕРІОД")): 
                        pass
                    else: 
                        tt0 = tt.previous
                        prep = ""
                        if (tt0 is not None and tt0.morph.class0_.is_preposition): 
                            prep = tt0.getNormalCaseText(MorphClass.PREPOSITION, False, MorphGender.UNDEFINED, False)
                            tt0 = tt0.previous
                        ok = False
                        if (isinstance(tt0, TextToken)): 
                            norm = tt0.getNormalCaseText(MorphClass.NOUN, True, MorphGender.UNDEFINED, False)
                            exps = Explanatory.findWords(norm, tt0.morph.language)
                            if (exps is not None): 
                                for ex in exps: 
                                    if (ex.nexts is not None): 
                                        if (len(prep) > 0 and prep in ex.nexts): 
                                            ok = True
                                            break
                                        if (len(prep) == 0 and prep in ex.nexts): 
                                            if (not ((ex.nexts[prep]) & npt.morph.case_).is_undefined): 
                                                ok = True
                                                break
                        if (not ok): 
                            break
                if (not abou): 
                    break
            cou += 1
            t1 = npt.end_token
            tt = t1
            if (npt.noun.isValue("НАЛОГОПЛАТЕЛЬЩИК", None)): 
                ttn = MiscHelper.checkNumberPrefix(tt.next0_)
                if ((isinstance(ttn, NumberToken)) and (Utils.asObjectOrNull(ttn, NumberToken)).value == (1)): 
                    t1 = ttn
                    tt = t1
        if (tt == t): 
            return None
        if (abou): 
            tt1 = DecreeToken._tryAttachStdChangeName(t0)
            if (tt1 is not None and tt1.end_char > t1.end_char): 
                t1 = tt1
        s = MiscHelper.getTextValue(t0, t1, Utils.valToEnum((GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
        if (Utils.isNullOrEmpty(s) or (len(s) < 10)): 
            return None
        return DecreeToken._new845(t, t1, DecreeToken.ItemType.NAME, s)
    
    @staticmethod
    def _tryAttachStdChangeName(t : 'Token') -> 'Token':
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
        if (not ((isinstance(t, TextToken))) or t.next0_ is None): 
            return None
        t0 = t
        term = (Utils.asObjectOrNull(t, TextToken)).term
        if ((term != "О" and term != "O" and term != "ОБ") and term != "ПРО"): 
            return None
        t = t.next0_
        if (((t.isValue("ВНЕСЕНИЕ", "ВНЕСЕННЯ") or t.isValue("УТВЕРЖДЕНИЕ", "ТВЕРДЖЕННЯ") or t.isValue("ПРИНЯТИЕ", "ПРИЙНЯТТЯ")) or t.isValue("ВВЕДЕНИЕ", "ВВЕДЕННЯ") or t.isValue("ПРИОСТАНОВЛЕНИЕ", "ПРИЗУПИНЕННЯ")) or t.isValue("ОТМЕНА", "СКАСУВАННЯ") or t.isValue("МЕРА", "ЗАХІД")): 
            pass
        elif (t.isValue("ПРИЗНАНИЕ", "ВИЗНАННЯ") and t.next0_ is not None and t.next0_.isValue("УТРАТИТЬ", "ВТРАТИТИ")): 
            pass
        else: 
            return None
        t1 = t
        tt = t.next0_
        first_pass2862 = True
        while True:
            if first_pass2862: first_pass2862 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_newline_before): 
                pass
            if (tt.whitespaces_before_count > 15): 
                break
            if (MiscHelper.canBeStartOfSentence(tt)): 
                break
            if (tt.morph.class0_.is_conjunction or tt.morph.class0_.is_preposition): 
                continue
            if (tt.is_comma): 
                continue
            npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                if ((((((npt.noun.isValue("ВВЕДЕНИЕ", "ВВЕДЕННЯ") or npt.noun.isValue("ПРИОСТАНОВЛЕНИЕ", "ПРИЗУПИНЕННЯ") or npt.noun.isValue("ВНЕСЕНИЕ", "ВНЕСЕННЯ")) or npt.noun.isValue("ИЗМЕНЕНИЕ", "ЗМІНА") or npt.noun.isValue("ДОПОЛНЕНИЕ", "ДОДАТОК")) or npt.noun.isValue("АКТ", None) or npt.noun.isValue("ПРИЗНАНИЕ", "ВИЗНАННЯ")) or npt.noun.isValue("ПРИНЯТИЕ", "ПРИЙНЯТТЯ") or npt.noun.isValue("СИЛА", "ЧИННІСТЬ")) or npt.noun.isValue("ДЕЙСТВИЕ", "ДІЯ") or npt.noun.isValue("СВЯЗЬ", "ЗВЯЗОК")) or npt.noun.isValue("РЕАЛИЗАЦИЯ", "РЕАЛІЗАЦІЯ") or npt.noun.isValue("РЯД", None)): 
                    tt = npt.end_token
                    t1 = tt
                    continue
            if (tt.isValue("ТАКЖЕ", "ТАКОЖ") or tt.isValue("НЕОБХОДИМЫЙ", "НЕОБХІДНИЙ")): 
                continue
            r = tt.getReferent()
            if ((isinstance(r, GeoReferent)) or (isinstance(r, DecreeReferent)) or (isinstance(r, DecreePartReferent))): 
                t1 = tt
                continue
            if ((isinstance(r, OrganizationReferent)) and tt.is_newline_after): 
                t1 = tt
                continue
            pts = PartToken.tryAttachList(tt, False, 40)
            while pts is not None and len(pts) > 0:
                if (pts[0].typ == PartToken.ItemType.PREFIX): 
                    del pts[0]
                else: 
                    break
            if (pts is not None and len(pts) > 0): 
                tt = pts[len(pts) - 1].end_token
                t1 = tt
                continue
            dts = DecreeToken.tryAttachList(tt, None, 10, False)
            if (dts is not None and len(dts) > 0): 
                rts = DecreeAnalyzer._tryAttach(dts, None, None)
                if (rts is not None): 
                    tt = rts[0].end_token
                    t1 = tt
                    continue
                if (dts[0].typ == DecreeToken.ItemType.TYP): 
                    rt = DecreeAnalyzer._tryAttachApproved(tt, None)
                    if (rt is not None): 
                        tt = rt.end_token
                        t1 = tt
                        continue
            tt1 = DecreeToken.isKeyword(tt, False)
            if (tt1 is not None): 
                tt = tt1
                t1 = tt
                continue
            if (isinstance(tt, NumberToken)): 
                continue
            if (not tt.chars.is_all_lower and tt.length_char > 2 and tt.getMorphClassInDictionary().is_undefined): 
                t1 = tt
                continue
            break
        if (BracketHelper.canBeStartOfSequence(t0.previous, True, False)): 
            if (BracketHelper.canBeEndOfSequence(t1.next0_, True, t0.previous, False)): 
                t1 = t1.next0_
        return t1
    
    M_TERMINS = None
    
    M_KEYWORDS = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (DecreeToken.M_TERMINS is not None): 
            return
        DecreeToken.M_TERMINS = TerminCollection()
        DecreeToken.M_KEYWORDS = TerminCollection()
        for s in DecreeToken.M_MISC_TYPESRU: 
            DecreeToken.M_KEYWORDS.add(Termin(s))
        for s in DecreeToken.M_MISC_TYPESUA: 
            DecreeToken.M_KEYWORDS.add(Termin._new898(s, MorphLang.UA))
        t = Termin._new113("ТЕХНИЧЕСКОЕ ЗАДАНИЕ", "ТЗ")
        t.addVariant("ТЕХЗАДАНИЕ", False)
        t.addAbridge("ТЕХ. ЗАДАНИЕ")
        DecreeToken.M_KEYWORDS.add(t)
        t = Termin._new113("ТЕХНИКО КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ", "ТКП")
        t.addVariant("КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ", False)
        DecreeToken.M_KEYWORDS.add(t)
        for s in DecreeToken.M_ALL_TYPESRU: 
            DecreeToken.M_TERMINS.add(Termin._new118(s, DecreeToken.ItemType.TYP))
            DecreeToken.M_KEYWORDS.add(Termin._new118(s, DecreeToken.ItemType.TYP))
        for s in DecreeToken.M_ALL_TYPESUA: 
            DecreeToken.M_TERMINS.add(Termin._new119(s, DecreeToken.ItemType.TYP, MorphLang.UA))
            DecreeToken.M_KEYWORDS.add(Termin._new119(s, DecreeToken.ItemType.TYP, MorphLang.UA))
        DecreeToken.M_TERMINS.add(Termin._new118("ОТРАСЛЕВОЕ СОГЛАШЕНИЕ", DecreeToken.ItemType.TYP))
        DecreeToken.M_TERMINS.add(Termin._new477("ГАЛУЗЕВА УГОДА", MorphLang.UA, DecreeToken.ItemType.TYP))
        DecreeToken.M_TERMINS.add(Termin._new118("МЕЖОТРАСЛЕВОЕ СОГЛАШЕНИЕ", DecreeToken.ItemType.TYP))
        DecreeToken.M_TERMINS.add(Termin._new477("МІЖГАЛУЗЕВА УГОДА", MorphLang.UA, DecreeToken.ItemType.TYP))
        DecreeToken.M_TERMINS.add(Termin._new120("ОСНОВЫ ЗАКОНОДАТЕЛЬСТВА", DecreeToken.ItemType.TYP, DecreeKind.KODEX))
        DecreeToken.M_TERMINS.add(Termin._new910("ОСНОВИ ЗАКОНОДАВСТВА", MorphLang.UA, DecreeToken.ItemType.TYP, DecreeKind.KODEX))
        DecreeToken.M_TERMINS.add(Termin._new120("ОСНОВЫ ГРАЖДАНСКОГО ЗАКОНОДАТЕЛЬСТВА", DecreeToken.ItemType.TYP, DecreeKind.KODEX))
        DecreeToken.M_TERMINS.add(Termin._new910("ОСНОВИ ЦИВІЛЬНОГО ЗАКОНОДАВСТВА", MorphLang.UA, DecreeToken.ItemType.TYP, DecreeKind.KODEX))
        t = Termin._new144("ФЕДЕРАЛЬНЫЙ ЗАКОН", DecreeToken.ItemType.TYP, "ФЗ")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new914("ФЕДЕРАЛЬНИЙ ЗАКОН", MorphLang.UA, DecreeToken.ItemType.TYP, "ФЗ")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("ПРОЕКТ ЗАКОНА", DecreeToken.ItemType.TYP)
        t.addVariant("ЗАКОНОПРОЕКТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("ПАСПОРТ ПРОЕКТА", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new477("ПРОЕКТ ЗАКОНУ", MorphLang.UA, DecreeToken.ItemType.TYP)
        t.addVariant("ЗАКОНОПРОЕКТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new477("ПАСПОРТ ПРОЕКТУ", MorphLang.UA, DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new142("ГОСУДАРСТВЕННАЯ ПРОГРАММА", "ПРОГРАММА", DecreeToken.ItemType.TYP)
        t.addVariant("ГОСУДАРСТВЕННАЯ ЦЕЛЕВАЯ ПРОГРАММА", False)
        t.addVariant("ФЕДЕРАЛЬНАЯ ЦЕЛЕВАЯ ПРОГРАММА", False)
        t.addAbridge("ФЕДЕРАЛЬНАЯ ПРОГРАММА")
        t.addVariant("МЕЖГОСУДАРСТВЕННАЯ ЦЕЛЕВАЯ ПРОГРАММА", False)
        t.addAbridge("МЕЖГОСУДАРСТВЕННАЯ ПРОГРАММА")
        t.addVariant("ГОСПРОГРАММА", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new920("ДЕРЖАВНА ПРОГРАМА", "ПРОГРАМА", MorphLang.UA, DecreeToken.ItemType.TYP)
        t.addVariant("ДЕРЖАВНА ЦІЛЬОВА ПРОГРАМА", False)
        t.addVariant("ФЕДЕРАЛЬНА ЦІЛЬОВА ПРОГРАМА", False)
        t.addAbridge("ФЕДЕРАЛЬНА ПРОГРАМА")
        t.addVariant("ДЕРЖПРОГРАМА", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new144("ФЕДЕРАЛЬНЫЙ КОНСТИТУЦИОННЫЙ ЗАКОН", DecreeToken.ItemType.TYP, "ФКЗ")
        t.addVariant("КОНСТИТУЦИОННЫЙ ЗАКОН", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new914("ФЕДЕРАЛЬНИЙ КОНСТИТУЦІЙНИЙ ЗАКОН", MorphLang.UA, DecreeToken.ItemType.TYP, "ФКЗ")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("УГОЛОВНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "УК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("КРИМИНАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "КК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("КРИМІНАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "КК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("УГОЛОВНО-ПРОЦЕССУАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "УПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("КРИМІНАЛЬНО-ПРОЦЕСУАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "КПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("УГОЛОВНО-ИСПОЛНИТЕЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "УИК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("КРИМІНАЛЬНО-ВИКОНАВЧИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "КВК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ГРАЖДАНСКИЙ КОДЕКС", DecreeToken.ItemType.TYP, "ГК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("ЦИВІЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЦК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ГРАЖДАНСКИЙ ПРОЦЕССУАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ГПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("ЦИВІЛЬНИЙ ПРОЦЕСУАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЦПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ГРАДОСТРОИТЕЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ГРК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("МІСТОБУДІВНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "МБК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ХОЗЯЙСТВЕННЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ХК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("ГОСПОДАРСЬКИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ГК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ХОЗЯЙСТВЕННЫЙ ПРОЦЕССУАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ХПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("ГОСПОДАРСЬКИЙ ПРОЦЕСУАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ГПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new120("АРБИТРАЖНЫЙ ПРОЦЕССУАЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, DecreeKind.KODEX)
        t.addAbridge("АПК")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new910("АРБІТРАЖНИЙ ПРОЦЕСУАЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, DecreeKind.KODEX)
        t.addAbridge("АПК")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("КОДЕКС ВНУТРЕННЕГО ВОДНОГО ТРАНСПОРТА", DecreeToken.ItemType.TYP, "КВВТ", DecreeKind.KODEX)
        t.addVariant("КВ ВТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ТРУДОВОЙ КОДЕКС", DecreeToken.ItemType.TYP, "ТК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("ТРУДОВИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ТК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new945("КОДЕКС ЗАКОНОВ О ТРУДЕ", "КЗОТ", DecreeToken.ItemType.TYP, DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("КОДЕКС ЗАКОНІВ ПРО ПРАЦЮ", MorphLang.UA, DecreeToken.ItemType.TYP, "КЗПП", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ЖИЛИЩНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ЖК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("ЖИТЛОВИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЖК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ЗЕМЕЛЬНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ЗК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("ЗЕМЕЛЬНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЗК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ЛЕСНОЙ КОДЕКС", DecreeToken.ItemType.TYP, "ЛК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("ЛІСОВИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ЛК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("БЮДЖЕТНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "БК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("БЮДЖЕТНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "БК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("НАЛОГОВЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "НК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("ПОДАТКОВИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("СЕМЕЙНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "СК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("СІМЕЙНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "СК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ВОДНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ВК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("ВОДНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ВК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ВОЗДУШНЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ВК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("ПОВІТРЯНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "ПК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("КОДЕКС ОБ АДМИНИСТРАТИВНЫХ ПРАВОНАРУШЕНИЯХ", DecreeToken.ItemType.TYP, "КОАП", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("КОДЕКС ПРО АДМІНІСТРАТИВНІ ПРАВОПОРУШЕННЯ", MorphLang.UA, DecreeToken.ItemType.TYP, "КОАП", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("ОБ АДМИНИСТРАТИВНЫХ ПРАВОНАРУШЕНИЯХ", DecreeToken.ItemType.STDNAME)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new477("ПРО АДМІНІСТРАТИВНІ ПРАВОПОРУШЕННЯ", MorphLang.UA, DecreeToken.ItemType.STDNAME)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("КОДЕКС ОБ АДМИНИСТРАТИВНЫХ ПРАВОНАРУШЕНИЯХ", DecreeToken.ItemType.TYP, "КРКОАП", DecreeKind.KODEX)
        t.addVariant("КРК ОБ АП", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("КОДЕКС АДМИНИСТРАТИВНОГО СУДОПРОИЗВОДСТВА", DecreeToken.ItemType.TYP, "КАС", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("КОДЕКС АДМІНІСТРАТИВНОГО СУДОЧИНСТВА", MorphLang.UA, DecreeToken.ItemType.TYP, "КАС", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ТАМОЖЕННЫЙ КОДЕКС", DecreeToken.ItemType.TYP, "ТК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("МИТНИЙ КОДЕКС", MorphLang.UA, DecreeToken.ItemType.TYP, "МК", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("КОДЕКС ТОРГОВОГО МОРЕПЛАВАНИЯ", DecreeToken.ItemType.TYP, "КТМ", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("КОДЕКС ТОРГОВЕЛЬНОГО МОРЕПЛАВСТВА", MorphLang.UA, DecreeToken.ItemType.TYP, "КТМ", DecreeKind.KODEX)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new923("ПРАВИЛА ДОРОЖНОГО ДВИЖЕНИЯ", DecreeToken.ItemType.TYP, "ПДД", "ПРАВИЛА")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new925("ПРАВИЛА ДОРОЖНЬОГО РУХУ", MorphLang.UA, DecreeToken.ItemType.TYP, "ПДР", "ПРАВИЛА")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("СОБРАНИЕ ЗАКОНОДАТЕЛЬСТВА", DecreeToken.ItemType.TYP)
        t.addAbridge("СЗ")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("ОФИЦИАЛЬНЫЙ ВЕСТНИК", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new477("ОФІЦІЙНИЙ ВІСНИК", MorphLang.UA, DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("СВОД ЗАКОНОВ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("БЮЛЛЕТЕНЬ НОРМАТИВНЫХ АКТОВ ФЕДЕРАЛЬНЫХ ОРГАНОВ ИСПОЛНИТЕЛЬНОЙ ВЛАСТИ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("БЮЛЛЕТЕНЬ МЕЖДУНАРОДНЫХ ДОГОВОРОВ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("БЮЛЛЕТЕНЬ ВЕРХОВНОГО СУДА", DecreeToken.ItemType.TYP)
        t.addVariant("БЮЛЛЕТЕНЬ ВС", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("ВЕСТНИК ВЫСШЕГО АРБИТРАЖНОГО СУДА", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("ВЕСТНИК БАНКА РОССИИ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("РОССИЙСКАЯ ГАЗЕТА", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("РОССИЙСКИЕ ВЕСТИ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("СОБРАНИЕ АКТОВ ПРЕЗИДЕНТА И ПРАВИТЕЛЬСТВА", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("ВЕДОМОСТИ ВЕРХОВНОГО СОВЕТА", DecreeToken.ItemType.TYP)
        t.addVariant("ВЕДОМОСТИ ВС", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("ВЕДОМОСТИ СЪЕЗДА НАРОДНЫХ ДЕПУТАТОВ И ВЕРХОВНОГО СОВЕТА", DecreeToken.ItemType.TYP)
        t.addVariant("ВЕДОМОСТИ СЪЕЗДА НАРОДНЫХ ДЕПУТАТОВ РФ И ВЕРХОВНОГО СОВЕТА", False)
        t.addVariant("ВЕДОМОСТИ СЪЕЗДА НАРОДНЫХ ДЕПУТАТОВ", False)
        t.addVariant("ВЕДОМОСТИ СНД РФ И ВС", False)
        t.addVariant("ВЕДОМОСТИ СНД И ВС", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("БЮЛЛЕТЕНЬ НОРМАТИВНЫХ АКТОВ МИНИСТЕРСТВ И ВЕДОМСТВ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        DecreeToken.M_TERMINS.add(Termin._new118("СВОД ЗАКОНОВ", DecreeToken.ItemType.TYP))
        DecreeToken.M_TERMINS.add(Termin._new118("ВЕДОМОСТИ", DecreeToken.ItemType.TYP))
        t = Termin._new142("ЗАРЕГИСТРИРОВАТЬ", "РЕГИСТРАЦИЯ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new994("ЗАРЕЄСТРУВАТИ", MorphLang.UA, "РЕЄСТРАЦІЯ", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new120("СТАНДАРТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("МЕЖДУНАРОДНЫЙ СТАНДАРТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new144("ЕДИНЫЙ ОТРАСЛЕВОЙ СТАНДАРТ ЗАКУПОК", DecreeToken.ItemType.TYP, "ЕОСЗ")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new118("ЕДИНЫЙ ОТРАСЛЕВОЙ ПОРЯДОК", DecreeToken.ItemType.TYP)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new120("ГОСТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("ГОСУДАРСТВЕННЫЙ СТАНДАРТ", False)
        t.addVariant("ГОССТАНДАРТ", False)
        t.addVariant("НАЦИОНАЛЬНЫЙ СТАНДАРТ", False)
        t.addVariant("МЕЖГОСУДАРСТВЕННЫЙ СТАНДАРТ", False)
        t.addVariant("ДЕРЖАВНИЙ СТАНДАРТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new120("ОСТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("ОТРАСЛЕВОЙ СТАНДАРТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new120("ПНСТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("ПРЕДВАРИТЕЛЬНЫЙ НАЦИОНАЛЬНЫЙ СТАНДАРТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new120("РСТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("РЕСПУБЛИКАНСКИЙ СТАНДАРТ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new120("ПБУ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("ПОЛОЖЕНИЕ ПО БУХГАЛТЕРСКОМУ УЧЕТУ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new120("ISO", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("ИСО", False)
        t.addVariant("ISO/IEC", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new945("ТЕХНИЧЕСКИЕ УСЛОВИЯ", "ТУ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("ТЕХУСЛОВИЯ", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new120("СТРОИТЕЛЬНЫЕ НОРМЫ И ПРАВИЛА", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("СНИП", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new945("СТРОИТЕЛЬНЫЕ НОРМЫ", "СН", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("CH", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new945("ВЕДОМСТВЕННЫЕ СТРОИТЕЛЬНЫЕ НОРМЫ", "ВСН", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("BCH", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new945("РЕСПУБЛИКАНСКИЕ СТРОИТЕЛЬНЫЕ НОРМЫ", "РСН", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("PCH", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new945("НОРМЫ ПОЖАРНОЙ БЕЗОПАСНОСТИ", "НПБ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new945("ПРАВИЛА ПОЖАРНОЙ БЕЗОПАСНОСТИ", "ППБ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new945("СТРОИТЕЛЬНЫЕ ПРАВИЛА", "СП", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new945("МОСКОВСКИЕ ГОРОДСКИЕ СТРОИТЕЛЬНЫЕ НОРМЫ", "МГСН", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new120("АВОК", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("ABOK", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new120("СТАНДАРТ ОРГАНИЗАЦИИ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("СТО", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new945("ПРАВИЛА ПО ОХРАНЕ ТРУДА", "ПОТ", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("ПРАВИЛА ОХРАНЫ ТРУДА", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new945("РУКОВОДЯЩИЙ ДОКУМЕНТ", "РД", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new120("САНИТАРНЫЕ НОРМЫ И ПРАВИЛА", DecreeToken.ItemType.TYP, DecreeKind.STANDARD)
        t.addVariant("САНПИН", False)
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new144("ТЕХНИЧЕСКОЕ ЗАДАНИЕ", DecreeToken.ItemType.TYP, "ТЗ")
        t.addVariant("ТЕХЗАДАНИЕ", False)
        t.addAbridge("ТЕХ. ЗАДАНИЕ")
        DecreeToken.M_TERMINS.add(t)
        t = Termin._new113("ТЕХНИКО КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ", "ТКП")
        t.addVariant("КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ", False)
        DecreeToken.M_KEYWORDS.add(t)
    
    @staticmethod
    def isKeyword(t : 'Token', is_misc_type_only : bool=False) -> 'Token':
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.decree.internal.PartToken import PartToken
        if (t is None): 
            return None
        tok = DecreeToken.M_KEYWORDS.tryParse(t, TerminParseAttr.NO)
        if (tok is not None): 
            if (is_misc_type_only and tok.termin.tag is not None): 
                return None
            tok.end_token.tag = (tok.termin.canonic_text)
            return tok.end_token
        if (not t.morph.class0_.is_adjective and not t.morph.class0_.is_pronoun): 
            return None
        npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
        if (npt is None or npt.begin_token == npt.end_token): 
            if (t.isValue("НАСТОЯЩИЙ", "СПРАВЖНІЙ") or t.isValue("НАЗВАННЫЙ", "НАЗВАНИЙ") or t.isValue("ДАННЫЙ", "ДАНИЙ")): 
                tok = DecreeToken.M_KEYWORDS.tryParse(t.next0_, TerminParseAttr.NO)
                if ((tok) is not None): 
                    tok.end_token.tag = (tok.termin.canonic_text)
                    return tok.end_token
            return None
        tok = DecreeToken.M_KEYWORDS.tryParse(npt.end_token, TerminParseAttr.NO)
        if ((tok) is not None): 
            if (is_misc_type_only and tok.termin.tag is not None): 
                return None
            tok.end_token.tag = (tok.termin.canonic_text)
            return tok.end_token
        pp = PartToken.tryAttach(npt.end_token, None, False, True)
        if (pp is not None): 
            return pp.end_token
        return None
    
    @staticmethod
    def isKeywordStr(word : str, is_misc_type_only : bool=False) -> bool:
        if (not is_misc_type_only): 
            if (word in DecreeToken.M_ALL_TYPESRU or word in DecreeToken.M_ALL_TYPESUA): 
                return True
        if (word in DecreeToken.M_MISC_TYPESRU or word in DecreeToken.M_MISC_TYPESUA): 
            return True
        return False
    
    @staticmethod
    def addNewType(typ_ : str, acronym : str=None) -> None:
        """ Добавить новый тип НПА
        
        Args:
            typ_(str): 
            acronym(str): 
        """
        from pullenti.ner.core.Termin import Termin
        t = Termin._new144(typ_, DecreeToken.ItemType.TYP, acronym)
        DecreeToken.M_TERMINS.add(t)
        DecreeToken.M_KEYWORDS.add(Termin._new118(typ_, DecreeToken.ItemType.TYP))
    
    M_ALL_TYPESRU = None
    
    M_ALL_TYPESUA = None
    
    M_MISC_TYPESRU = None
    
    M_MISC_TYPESUA = None
    
    M_STD_ADJECTIVES = None
    
    M_EMPTY_ADJECTIVES = None
    
    @staticmethod
    def getKind(typ_ : str) -> 'DecreeKind':
        if (typ_ is None): 
            return DecreeKind.UNDEFINED
        if (LanguageHelper.endsWithEx(typ_, "КОНСТИТУЦИЯ", "КОНСТИТУЦІЯ", "КОДЕКС", None)): 
            return DecreeKind.KODEX
        if (typ_.startswith("ОСНОВ") and LanguageHelper.endsWithEx(typ_, "ЗАКОНОДАТЕЛЬСТВА", "ЗАКОНОДАВСТВА", None, None)): 
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
        if ((LanguageHelper.endsWithEx(typ_, "КОНВЕНЦИЯ", "КОНВЕНЦІЯ", None, None) or LanguageHelper.endsWithEx(typ_, "ДОГОВОР", "ДОГОВІР", None, None) or LanguageHelper.endsWithEx(typ_, "ПАКТ", "БИЛЛЬ", "БІЛЛЬ", None)) or LanguageHelper.endsWithEx(typ_, "ДЕКЛАРАЦИЯ", "ДЕКЛАРАЦІЯ", None, None)): 
            return DecreeKind.KONVENTION
        if ((((((typ_.startswith("СОБРАНИЕ") or typ_.startswith("ЗБОРИ") or typ_.startswith("РЕГИСТРАЦИЯ")) or typ_.startswith("РЕЄСТРАЦІЯ") or "БЮЛЛЕТЕНЬ" in typ_) or "БЮЛЕТЕНЬ" in typ_ or "ВЕДОМОСТИ" in typ_) or "ВІДОМОСТІ" in typ_ or typ_.startswith("СВОД")) or typ_.startswith("ЗВЕДЕННЯ") or LanguageHelper.endsWithEx(typ_, "ГАЗЕТА", "ВЕСТИ", "ВІСТІ", None)) or "ВЕСТНИК" in typ_ or LanguageHelper.endsWith(typ_, "ВІСНИК")): 
            return DecreeKind.PUBLISHER
        return DecreeKind.UNDEFINED
    
    @staticmethod
    def isLaw(typ_ : str) -> bool:
        if (typ_ is None): 
            return False
        ki = DecreeToken.getKind(typ_)
        if (ki == DecreeKind.KODEX): 
            return True
        if (LanguageHelper.endsWith(typ_, "ЗАКОН")): 
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
    def _new867(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : int) -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.num_year = _arg5
        return res
    
    @staticmethod
    def _new869(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'ReferentToken', _arg5 : 'MorphCollection') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new870(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : 'MorphCollection') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new871(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : 'MorphCollection', _arg6 : bool) -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.morph = _arg5
        res.is_doubtful = _arg6
        return res
    
    @staticmethod
    def _new876(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'MorphCollection') -> 'DecreeToken':
        res = DecreeToken(_arg1, _arg2)
        res.value = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new887(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'MorphCollection', _arg5 : str) -> 'DecreeToken':
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