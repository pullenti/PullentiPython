# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.date.DateRangeReferent import DateRangeReferent
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.business.BusinessFactKind import BusinessFactKind
from pullenti.ner.Token import Token
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.business.internal.FundsItemTyp import FundsItemTyp
from pullenti.ner.money.MoneyReferent import MoneyReferent
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.business.internal.BusinessFactItemTyp import BusinessFactItemTyp
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.org.OrganizationAnalyzer import OrganizationAnalyzer
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.business.internal.FundsMeta import FundsMeta
from pullenti.ner.Referent import Referent
from pullenti.ner.core.Termin import Termin
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.business.internal.MetaBusinessFact import MetaBusinessFact
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.business.internal.FundsItemToken import FundsItemToken
from pullenti.ner.business.internal.BusinessFactItem import BusinessFactItem
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.business.FundsReferent import FundsReferent

class BusinessAnalyzer(Analyzer):
    """ Семантический анализатор для бизнес-фактов
     (относится к специфическим анализаторам) """
    
    ANALYZER_NAME = "BUSINESS"
    
    @property
    def name(self) -> str:
        return BusinessAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Бизнес-объекты"
    
    @property
    def description(self) -> str:
        return "Бизнес факты"
    
    @property
    def is_specific(self) -> bool:
        return True
    
    def clone(self) -> 'Analyzer':
        return BusinessAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaBusinessFact.GLOBAL_META, FundsMeta.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaBusinessFact.IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("businessfact.png")
        res[FundsMeta.IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("creditcards.png")
        return res
    
    def createReferent(self, type0_ : str) -> 'Referent':
        if (type0_ == BusinessFactReferent.OBJ_TYPENAME): 
            return BusinessFactReferent()
        if (type0_ == FundsReferent.OBJ_TYPENAME): 
            return FundsReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.getAnalyzerData(self)
        t = kit.first_token
        while t is not None: 
            rt = FundsItemToken.tryAttach(t)
            if (rt is not None): 
                rt.referent = ad.registerReferent(rt.referent)
                kit.embedToken(rt)
                t = (rt)
            t = t.next0_
        t = kit.first_token
        first_pass2778 = True
        while True:
            if first_pass2778: first_pass2778 = False
            else: t = t.next0_
            if (not (t is not None)): break
            rt = self.__analizeFact(t)
            if (rt is not None): 
                rt.referent = ad.registerReferent(rt.referent)
                kit.embedToken(rt)
                t = (rt)
                rts = self.__analizeLikelihoods(rt)
                if (rts is not None): 
                    for rt0 in rts: 
                        for s in rt0.referent.slots: 
                            if (s.type_name == BusinessFactReferent.ATTR_WHAT and (isinstance(s.value, FundsReferent))): 
                                rt0.referent.uploadSlot(s, ad.registerReferent(Utils.asObjectOrNull(s.value, Referent)))
                        rt0.referent = ad.registerReferent(rt0.referent)
                        kit.embedToken(rt0)
                        t = (rt0)
                continue
    
    def __analizeFact(self, t : 'Token') -> 'ReferentToken':
        if (t is None): 
            return None
        bfi = BusinessFactItem.tryParse(t)
        if (bfi is None): 
            return None
        if (bfi.typ == BusinessFactItemTyp.BASE): 
            if (bfi.base_kind == BusinessFactKind.GET or bfi.base_kind == BusinessFactKind.SELL): 
                return self.__analizeGet(bfi)
            if (bfi.base_kind == BusinessFactKind.HAVE): 
                if (bfi.is_base_passive or bfi.morph.class0_.is_noun): 
                    re = self.__analizeHave(bfi)
                    if (re is not None): 
                        return re
                return self.__analizeGet(bfi)
            if (bfi.base_kind == BusinessFactKind.PROFIT or bfi.base_kind == BusinessFactKind.DAMAGES): 
                return self.__analizeProfit(bfi)
            if (bfi.base_kind == BusinessFactKind.AGREEMENT or bfi.base_kind == BusinessFactKind.LAWSUIT): 
                return self.__analizeAgreement(bfi)
            if (bfi.base_kind == BusinessFactKind.SUBSIDIARY): 
                return self.__analizeSubsidiary(bfi)
            if (bfi.base_kind == BusinessFactKind.FINANCE): 
                return self.__analizeFinance(bfi)
        return None
    
    def __FindRefBefore(self, t : 'Token') -> 'ReferentToken':
        if (t is None): 
            return None
        points = 0
        t0 = None
        t1 = t
        first_pass2779 = True
        while True:
            if first_pass2779: first_pass2779 = False
            else: t = t.previous
            if (not (t is not None)): break
            if (t.is_newline_after): 
                break
            if (t.morph.class0_.is_adverb or t.morph.class0_.is_preposition or t.is_comma): 
                continue
            if (t.morph.class0_.is_personal_pronoun): 
                break
            if (t.isValue("ИНФОРМАЦИЯ", None) or t.isValue("ДАННЫЕ", None)): 
                continue
            if (t.isValue("ІНФОРМАЦІЯ", None) or t.isValue("ДАНІ", None)): 
                continue
            if (isinstance(t, TextToken)): 
                if (t.morph.class0_.is_verb): 
                    break
                if (t.isChar('.')): 
                    break
                continue
            r = t.getReferent()
            if ((isinstance(r, DateReferent)) or (isinstance(r, DateRangeReferent))): 
                continue
            break
        if (t is None): 
            return None
        if (t.morph.class0_.is_personal_pronoun): 
            t0 = t
            points = 1
            t = t.previous
        else: 
            if (t.morph.class0_.is_pronoun): 
                t = t.previous
                if (t is not None and t.isChar(',')): 
                    t = t.previous
            if (t is None): 
                return None
            refs = t.getReferents()
            if (refs is not None): 
                for r in refs: 
                    if ((isinstance(r, PersonReferent)) or (isinstance(r, OrganizationReferent)) or (isinstance(r, FundsReferent))): 
                        return ReferentToken(r, t, t1)
            return None
        first_pass2780 = True
        while True:
            if first_pass2780: first_pass2780 = False
            else: t = t.previous
            if (not (t is not None)): break
            if (t.isChar('.')): 
                points -= 1
                if ((points) < 0): 
                    break
                continue
            refs = t.getReferents()
            if (refs is not None): 
                for r in refs: 
                    if ((isinstance(r, PersonReferent)) or (isinstance(r, OrganizationReferent))): 
                        return ReferentToken(r, t0, t1)
        return None
    
    def __FindSecRefBefore(self, rt : 'ReferentToken') -> 'ReferentToken':
        t = (None if rt is None else rt.begin_token.previous)
        if (t is None or t.whitespaces_after_count > 2): 
            return None
        if ((isinstance(rt.getReferent(), PersonReferent)) and (isinstance(t.getReferent(), OrganizationReferent))): 
            return Utils.asObjectOrNull(t, ReferentToken)
        return None
    
    def __findDate(self, bfr : 'BusinessFactReferent', t : 'Token') -> bool:
        tt = t
        while tt is not None: 
            r = tt.getReferent()
            if ((isinstance(r, DateReferent)) or (isinstance(r, DateRangeReferent))): 
                bfr.when = r
                return True
            if (tt.isChar('.')): 
                break
            if (tt.is_newline_before): 
                break
            tt = tt.previous
        tt = t
        while tt is not None: 
            if (tt != t and tt.is_newline_before): 
                break
            r = tt.getReferent()
            if ((isinstance(r, DateReferent)) or (isinstance(r, DateRangeReferent))): 
                bfr.when = r
                return True
            if (tt.isChar('.')): 
                break
            tt = tt.next0_
        return False
    
    def __findSum(self, bfr : 'BusinessFactReferent', t : 'Token') -> bool:
        while t is not None: 
            if (t.isChar('.') or t.is_newline_before): 
                break
            r = t.getReferent()
            if (isinstance(r, MoneyReferent)): 
                fu = Utils.asObjectOrNull(bfr.getSlotValue(BusinessFactReferent.ATTR_WHAT), FundsReferent)
                if (fu is not None): 
                    if (fu.sum0_ is None): 
                        fu.sum0_ = Utils.asObjectOrNull(r, MoneyReferent)
                        return True
                bfr.addSlot(BusinessFactReferent.ATTR_MISC, r, False, 0)
                return True
            t = t.next0_
        return False
    
    def __analizeGet(self, bfi : 'BusinessFactItem') -> 'ReferentToken':
        bef = self.__FindRefBefore(bfi.begin_token.previous)
        if (bef is None): 
            return None
        t1 = bfi.end_token.next0_
        if (t1 is None): 
            return None
        first_pass2781 = True
        while True:
            if first_pass2781: first_pass2781 = False
            else: t1 = t1.next0_
            if (not (t1 is not None)): break
            if (t1.morph.class0_.is_adverb): 
                continue
            if (t1.isValue("ПРАВО", None) or t1.isValue("РАСПОРЯЖАТЬСЯ", None) or t1.isValue("РОЗПОРЯДЖАТИСЯ", None)): 
                continue
            break
        if (t1 is None): 
            return None
        if ((isinstance(t1.getReferent(), FundsReferent)) and not ((isinstance(bef.referent, FundsReferent)))): 
            fr = Utils.asObjectOrNull(t1.getReferent(), FundsReferent)
            bfr = BusinessFactReferent._new437(bfi.base_kind)
            bfr.who = bef.referent
            bef2 = self.__FindSecRefBefore(bef)
            if (bef2 is not None): 
                bfr.addSlot(BusinessFactReferent.ATTR_WHO, bef2.referent, False, 0)
                bef = bef2
            if (fr.source == bef.referent and bef2 is None): 
                bef2 = self.__FindRefBefore(bef.begin_token.previous)
                if (bef2 is not None): 
                    bef = bef2
                    bfr.who = bef.referent
            if (fr.source == bef.referent): 
                cou = 0
                tt = bef.begin_token.previous
                first_pass2782 = True
                while True:
                    if first_pass2782: first_pass2782 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    cou += 1
                    if ((cou) > 100): 
                        break
                    refs = tt.getReferents()
                    if (refs is None): 
                        continue
                    for r in refs: 
                        if ((isinstance(r, OrganizationReferent)) and r != bef.referent): 
                            cou = 1000
                            fr.source = Utils.asObjectOrNull(r, OrganizationReferent)
                            break
            bfr._addWhat(fr)
            bfr.typ = ("покупка ценных бумаг" if bfi.base_kind == BusinessFactKind.GET else (("продажа ценных бумаг" if bfi.base_kind == BusinessFactKind.SELL else "владение ценными бумагами")))
            self.__findDate(bfr, bef.begin_token)
            self.__findSum(bfr, bef.end_token)
            return ReferentToken(bfr, bef.begin_token, t1)
        if ((bfi.morph.class0_.is_noun and ((bfi.base_kind == BusinessFactKind.GET or bfi.base_kind == BusinessFactKind.SELL)) and (isinstance(t1.getReferent(), OrganizationReferent))) or (isinstance(t1.getReferent(), PersonReferent))): 
            if ((isinstance(bef.referent, FundsReferent)) or (isinstance(bef.referent, OrganizationReferent))): 
                bfr = BusinessFactReferent._new437(bfi.base_kind)
                if (bfi.base_kind == BusinessFactKind.GET): 
                    bfr.typ = ("покупка ценных бумаг" if isinstance(bef.referent, FundsReferent) else "покупка компании")
                elif (bfi.base_kind == BusinessFactKind.SELL): 
                    bfr.typ = ("продажа ценных бумаг" if isinstance(bef.referent, FundsReferent) else "продажа компании")
                bfr.who = t1.getReferent()
                bfr._addWhat(bef.referent)
                self.__findDate(bfr, bef.begin_token)
                self.__findSum(bfr, bef.end_token)
                t1 = BusinessAnalyzer.__addWhosList(t1, bfr)
                return ReferentToken(bfr, bef.begin_token, t1)
        if ((isinstance(bef.referent, OrganizationReferent)) or (isinstance(bef.referent, PersonReferent))): 
            tt = t1
            if (tt is not None and tt.morph.class0_.is_preposition): 
                tt = tt.next0_
            slav = (None if tt is None else tt.getReferent())
            if ((((isinstance(slav, PersonReferent)) or (isinstance(slav, OrganizationReferent)))) and tt.next0_ is not None and (isinstance(tt.next0_.getReferent(), FundsReferent))): 
                bfr = BusinessFactReferent._new437(bfi.base_kind)
                bfr.typ = ("покупка ценных бумаг" if bfi.base_kind == BusinessFactKind.GET else "продажа ценных бумаг")
                bfr.who = bef.referent
                bef2 = self.__FindSecRefBefore(bef)
                if (bef2 is not None): 
                    bfr.addSlot(BusinessFactReferent.ATTR_WHO, bef2.referent, False, 0)
                    bef = bef2
                bfr.whom = slav
                bfr._addWhat(tt.next0_.getReferent())
                self.__findDate(bfr, bef.begin_token)
                self.__findSum(bfr, bef.end_token)
                return ReferentToken(bfr, bef.begin_token, tt.next0_)
            elif (isinstance(slav, OrganizationReferent)): 
                bfr = BusinessFactReferent._new437(bfi.base_kind)
                bfr.typ = ("покупка компании" if bfi.base_kind == BusinessFactKind.GET else "продажа компании")
                bfr.who = bef.referent
                bef2 = self.__FindSecRefBefore(bef)
                if (bef2 is not None): 
                    bfr.addSlot(BusinessFactReferent.ATTR_WHO, bef2.referent, False, 0)
                    bef = bef2
                bfr._addWhat(slav)
                self.__findDate(bfr, bef.begin_token)
                self.__findSum(bfr, bef.end_token)
                return ReferentToken(bfr, bef.begin_token, tt.next0_)
        if ((isinstance(bef.referent, FundsReferent)) and (((isinstance(t1.getReferent(), OrganizationReferent)) or (isinstance(t1.getReferent(), PersonReferent))))): 
            bfr = BusinessFactReferent._new437(bfi.base_kind)
            bfr.typ = ("покупка ценных бумаг" if bfi.base_kind == BusinessFactKind.GET else (("продажа ценных бумаг" if bfi.base_kind == BusinessFactKind.SELL else "владение ценными бумагами")))
            bfr.who = t1.getReferent()
            bfr._addWhat(bef.referent)
            self.__findDate(bfr, bef.begin_token)
            self.__findSum(bfr, bef.end_token)
            return ReferentToken(bfr, bef.begin_token, t1)
        return None
    
    @staticmethod
    def __addWhosList(t1 : 'Token', bfr : 'BusinessFactReferent') -> 'Token':
        if (t1 is None): 
            return None
        if ((t1.next0_ is not None and t1.next0_.is_comma_and and (isinstance(t1.next0_.next0_, ReferentToken))) and t1.next0_.next0_.getReferent().type_name == t1.getReferent().type_name): 
            li = list()
            li.append(t1.next0_.next0_.getReferent())
            if (t1.next0_.is_and): 
                t1 = t1.next0_.next0_
            else: 
                ok = False
                tt = t1.next0_.next0_.next0_
                while tt is not None: 
                    if (not tt.is_comma_and): 
                        break
                    if (not ((isinstance(tt.next0_, ReferentToken)))): 
                        break
                    if (tt.next0_.getReferent().type_name != t1.getReferent().type_name): 
                        break
                    li.append(tt.next0_.getReferent())
                    if (tt.is_and): 
                        ok = True
                        t1 = tt.next0_
                        break
                    tt = tt.next0_
                if (not ok): 
                    li = (None)
            if (li is not None): 
                for r in li: 
                    bfr.addSlot(BusinessFactReferent.ATTR_WHO, r, False, 0)
        return t1
    
    def __analizeGet2(self, t : 'Token') -> 'ReferentToken':
        if (t is None): 
            return None
        tt = t.previous
        ts = t
        if (tt is not None and tt.is_comma): 
            tt = tt.previous
        bef = self.__FindRefBefore(tt)
        master = None
        slave = None
        if (bef is not None and (isinstance(bef.referent, FundsReferent))): 
            slave = bef.referent
            ts = bef.begin_token
        tt = t.next0_
        if (tt is None): 
            return None
        te = tt
        r = tt.getReferent()
        if ((isinstance(r, PersonReferent)) or (isinstance(r, OrganizationReferent))): 
            master = r
            if (slave is None and tt.next0_ is not None): 
                r = tt.next0_.getReferent()
                if ((r) is not None): 
                    if ((isinstance(r, FundsReferent)) or (isinstance(r, OrganizationReferent))): 
                        slave = (Utils.asObjectOrNull(r, FundsReferent))
                        te = tt.next0_
        if (master is not None and slave is not None): 
            bfr = BusinessFactReferent._new437(BusinessFactKind.HAVE)
            bfr.who = master
            if (isinstance(slave, OrganizationReferent)): 
                bfr._addWhat(slave)
                bfr.typ = "владение компанией"
            elif (isinstance(slave, FundsReferent)): 
                bfr._addWhat(slave)
                bfr.typ = "владение ценными бумагами"
            else: 
                return None
            return ReferentToken(bfr, ts, te)
        return None
    
    def __analizeHave(self, bfi : 'BusinessFactItem') -> 'ReferentToken':
        t = bfi.end_token.next0_
        t1 = None
        if (t is not None and ((t.isValue("КОТОРЫЙ", None) or t.isValue("ЯКИЙ", None)))): 
            t1 = t.next0_
        else: 
            tt = bfi.begin_token
            while tt != bfi.end_token: 
                if (tt.morph.class0_.is_pronoun): 
                    t1 = t
                tt = tt.next0_
            if (t1 is None): 
                if (bfi.is_base_passive and t is not None and (((isinstance(t.getReferent(), PersonReferent)) or (isinstance(t.getReferent(), OrganizationReferent))))): 
                    t1 = t
                    if (t.next0_ is not None and (isinstance(t.next0_.getReferent(), FundsReferent))): 
                        bfr = BusinessFactReferent._new437(BusinessFactKind.HAVE)
                        bfr.who = t.getReferent()
                        bfr._addWhat(t.next0_.getReferent())
                        bfr.typ = "владение ценными бумагами"
                        return ReferentToken(bfr, bfi.begin_token, t.next0_)
        t0 = None
        slave = None
        mus_be_verb = False
        if (t1 is not None): 
            tt0 = bfi.begin_token.previous
            if (tt0 is not None and tt0.isChar(',')): 
                tt0 = tt0.previous
            bef = self.__FindRefBefore(tt0)
            if (bef is None): 
                return None
            if (not ((isinstance(bef.referent, OrganizationReferent)))): 
                return None
            t0 = bef.begin_token
            slave = bef.referent
        elif (bfi.end_token.getMorphClassInDictionary().is_noun and (isinstance(t.getReferent(), OrganizationReferent))): 
            slave = t.getReferent()
            t1 = t.next0_
            t0 = bfi.begin_token
            mus_be_verb = True
        if (t0 is None or t1 is None or slave is None): 
            return None
        if ((t1.is_hiphen or t1.isValue("ЯВЛЯТЬСЯ", None) or t1.isValue("БУТИ", None)) or t1.isValue("Є", None)): 
            t1 = t1.next0_
        elif (mus_be_verb): 
            return None
        r = (None if t1 is None else t1.getReferent())
        if ((isinstance(r, OrganizationReferent)) or (isinstance(r, PersonReferent))): 
            bfr = BusinessFactReferent._new437(BusinessFactKind.HAVE)
            bfr.who = r
            bfr._addWhat(slave)
            if (bfi.end_token.isValue("АКЦИОНЕР", None) or bfi.end_token.isValue("АКЦІОНЕР", None)): 
                bfr.typ = "владение ценными бумагами"
            else: 
                bfr.typ = "владение компанией"
            t1 = BusinessAnalyzer.__addWhosList(t1, bfr)
            return ReferentToken(bfr, t0, t1)
        return None
    
    def __analizeProfit(self, bfi : 'BusinessFactItem') -> 'ReferentToken':
        if (bfi.end_token.next0_ is None): 
            return None
        t0 = bfi.begin_token
        t1 = bfi.end_token
        typ = t1.getNormalCaseText(None, True, MorphGender.UNDEFINED, False).lower()
        org0_ = None
        org0_ = (Utils.asObjectOrNull(t1.next0_.getReferent(), OrganizationReferent))
        t = t1
        if (org0_ is not None): 
            t = t.next0_
        else: 
            rt = t.kit.processReferent(OrganizationAnalyzer.ANALYZER_NAME, t.next0_)
            if (rt is not None): 
                org0_ = (Utils.asObjectOrNull(rt.referent, OrganizationReferent))
                t = rt.end_token
        dt = None
        sum0_ = None
        t = t.next0_
        first_pass2783 = True
        while True:
            if first_pass2783: first_pass2783 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.isChar('.')): 
                break
            if (t.isChar('(')): 
                br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    t = br.end_token
                    continue
            if ((((t.morph.class0_.is_verb or t.isValue("ДО", None) or t.is_hiphen) or t.isValue("РАЗМЕР", None) or t.isValue("РОЗМІР", None))) and t.next0_ is not None and (isinstance(t.next0_.getReferent(), MoneyReferent))): 
                if (sum0_ is not None): 
                    break
                sum0_ = (Utils.asObjectOrNull(t.next0_.getReferent(), MoneyReferent))
                t = t.next0_
                t1 = t
                continue
            r = t.getReferent()
            if ((isinstance(r, DateRangeReferent)) or (isinstance(r, DateReferent))): 
                if (dt is None): 
                    dt = r
                    t1 = t
            elif ((isinstance(r, OrganizationReferent)) and org0_ is None): 
                org0_ = (Utils.asObjectOrNull(r, OrganizationReferent))
                t1 = t
        if (sum0_ is None): 
            return None
        if (org0_ is None): 
            tt = t0.previous
            while tt is not None: 
                if (tt.isChar('.')): 
                    break
                b0 = Utils.asObjectOrNull(tt.getReferent(), BusinessFactReferent)
                if (b0 is not None): 
                    org0_ = (Utils.asObjectOrNull(b0.who, OrganizationReferent))
                    break
                org0_ = Utils.asObjectOrNull(tt.getReferent(), OrganizationReferent)
                if ((org0_) is not None): 
                    break
                tt = tt.previous
        if (org0_ is None): 
            return None
        bfr = BusinessFactReferent._new437(bfi.base_kind)
        bfr.who = org0_
        bfr.typ = typ
        bfr.addSlot(BusinessFactReferent.ATTR_MISC, sum0_, False, 0)
        if (dt is not None): 
            bfr.when = dt
        else: 
            self.__findDate(bfr, bfi.begin_token)
        return ReferentToken(bfr, t0, t1)
    
    def __analizeAgreement(self, bfi : 'BusinessFactItem') -> 'ReferentToken':
        first = None
        second = None
        t0 = bfi.begin_token
        t1 = bfi.end_token
        max_lines = 1
        t = bfi.begin_token.previous
        first_pass2784 = True
        while True:
            if first_pass2784: first_pass2784 = False
            else: t = t.previous
            if (not (t is not None)): break
            if (t.isChar('.') or t.is_newline_after): 
                max_lines -= 1
                if ((max_lines) == 0): 
                    break
                continue
            if (t.isValue("СТОРОНА", None) and t.previous is not None and ((t.previous.isValue("МЕЖДУ", None) or t.previous.isValue("МІЖ", None)))): 
                max_lines = 2
                t = t.previous
                t0 = t
                continue
            r = t.getReferent()
            if (isinstance(r, BusinessFactReferent)): 
                b = Utils.asObjectOrNull(r, BusinessFactReferent)
                if (b.who is not None and ((b.who2 is not None or b.whom is not None))): 
                    first = b.who
                    second = (Utils.ifNotNull(b.who2, b.whom))
                    break
            if (not ((isinstance(r, OrganizationReferent)))): 
                continue
            if ((t.previous is not None and ((t.previous.is_and or t.previous.isValue("К", None))) and t.previous.previous is not None) and (isinstance(t.previous.previous.getReferent(), OrganizationReferent))): 
                t0 = t.previous.previous
                first = t0.getReferent()
                second = r
                break
            else: 
                t0 = t
                first = r
                break
        if (second is None): 
            t = bfi.end_token.next0_
            first_pass2785 = True
            while True:
                if first_pass2785: first_pass2785 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.isChar('.')): 
                    break
                if (t.is_newline_before): 
                    break
                r = t.getReferent()
                if (not ((isinstance(r, OrganizationReferent)))): 
                    continue
                if ((t.next0_ is not None and ((t.next0_.is_and or t.next0_.isValue("К", None))) and t.next0_.next0_ is not None) and (isinstance(t.next0_.next0_.getReferent(), OrganizationReferent))): 
                    t1 = t.next0_.next0_
                    first = r
                    second = t1.getReferent()
                    break
                else: 
                    t1 = t
                    second = r
                    break
        if (first is None or second is None): 
            return None
        bf = BusinessFactReferent._new437(bfi.base_kind)
        bf.who = first
        if (bfi.base_kind == BusinessFactKind.LAWSUIT): 
            bf.whom = second
        else: 
            bf.who2 = second
        self.__findDate(bf, bfi.begin_token)
        self.__findSum(bf, bfi.begin_token)
        return ReferentToken(bf, t0, t1)
    
    def __analizeSubsidiary(self, bfi : 'BusinessFactItem') -> 'ReferentToken':
        t1 = bfi.end_token.next0_
        if (t1 is None or not ((isinstance(t1.getReferent(), OrganizationReferent)))): 
            return None
        org0 = None
        t = bfi.begin_token.previous
        first_pass2786 = True
        while True:
            if first_pass2786: first_pass2786 = False
            else: t = t.previous
            if (not (t is not None)): break
            if (t.isChar('(') or t.isChar('%')): 
                continue
            if (t.morph.class0_.is_verb): 
                continue
            if (isinstance(t, NumberToken)): 
                continue
            org0 = (Utils.asObjectOrNull(t.getReferent(), OrganizationReferent))
            if (org0 is not None): 
                break
        if (org0 is None): 
            return None
        bfr = BusinessFactReferent._new437(bfi.base_kind)
        bfr.who = org0
        bfr.whom = t1.getReferent()
        return ReferentToken(bfr, t, t1)
    
    def __analizeFinance(self, bfi : 'BusinessFactItem') -> 'ReferentToken':
        bef = self.__FindRefBefore(bfi.begin_token.previous)
        if (bef is None): 
            return None
        if (not ((isinstance(bef.referent, OrganizationReferent))) and not ((isinstance(bef.referent, PersonReferent)))): 
            return None
        whom = None
        sum0_ = None
        funds = None
        t = bfi.end_token.next0_
        while t is not None: 
            if (t.is_newline_before or t.isChar('.')): 
                break
            r = t.getReferent()
            if (isinstance(r, OrganizationReferent)): 
                if (whom is None): 
                    whom = (Utils.asObjectOrNull(t, ReferentToken))
            elif (isinstance(r, MoneyReferent)): 
                if (sum0_ is None): 
                    sum0_ = (Utils.asObjectOrNull(r, MoneyReferent))
            elif (isinstance(r, FundsReferent)): 
                if (funds is None): 
                    funds = (Utils.asObjectOrNull(r, FundsReferent))
            t = t.next0_
        if (whom is None): 
            return None
        bfr = BusinessFactReferent()
        if (funds is None): 
            bfr.kind = BusinessFactKind.FINANCE
        else: 
            bfr.kind = BusinessFactKind.GET
            bfr.typ = "покупка ценных бумаг"
        bfr.who = bef.referent
        bfr.whom = whom.referent
        if (funds is not None): 
            bfr._addWhat(funds)
        if (sum0_ is not None): 
            bfr.addSlot(BusinessFactReferent.ATTR_MISC, sum0_, False, 0)
        self.__findDate(bfr, bef.begin_token)
        return ReferentToken(bfr, bef.begin_token, whom.end_token)
    
    def __analizeLikelihoods(self, rt : 'ReferentToken') -> typing.List['ReferentToken']:
        bfr0 = Utils.asObjectOrNull(rt.referent, BusinessFactReferent)
        if (bfr0 is None or len(bfr0.whats) != 1 or not ((isinstance(bfr0.whats[0], FundsReferent)))): 
            return None
        funds0 = Utils.asObjectOrNull(bfr0.whats[0], FundsReferent)
        whos = list()
        funds = list()
        t = rt.end_token.next0_
        first_pass2787 = True
        while True:
            if first_pass2787: first_pass2787 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_before or t.isChar('.')): 
                break
            if (t.morph.class0_.is_adverb): 
                continue
            if (t.is_hiphen or t.is_comma_and): 
                continue
            if (t.morph.class0_.is_conjunction or t.morph.class0_.is_preposition or t.morph.class0_.is_misc): 
                continue
            r = t.getReferent()
            if ((isinstance(r, OrganizationReferent)) or (isinstance(r, PersonReferent))): 
                whos.append(Utils.asObjectOrNull(t, ReferentToken))
                continue
            if (isinstance(r, FundsReferent)): 
                funds0 = (Utils.asObjectOrNull(r, FundsReferent))
                funds.append(funds0)
                continue
            it = FundsItemToken.tryParse(t, None)
            if (it is None): 
                break
            fu = Utils.asObjectOrNull(funds0.clone(), FundsReferent)
            fu.occurrence.clear()
            fu.addOccurenceOfRefTok(ReferentToken(fu, it.begin_token, it.end_token))
            if (it.typ == FundsItemTyp.PERCENT): 
                fu.percent = it.float_val
            elif (it.typ == FundsItemTyp.COUNT): 
                fu.count = it.long_val
            elif (it.typ == FundsItemTyp.SUM): 
                fu.sum0_ = Utils.asObjectOrNull(it.ref, MoneyReferent)
            else: 
                break
            funds.append(fu)
            t = it.end_token
        if (len(whos) == 0 or len(whos) != len(funds)): 
            return None
        res = list()
        i = 0
        while i < len(whos): 
            bfr = BusinessFactReferent._new448(bfr0.kind, bfr0.typ)
            bfr.who = whos[i].referent
            bfr._addWhat(funds[i])
            for s in bfr0.slots: 
                if (s.type_name == BusinessFactReferent.ATTR_MISC or s.type_name == BusinessFactReferent.ATTR_WHEN): 
                    bfr.addSlot(s.type_name, s.value, False, 0)
            res.append(ReferentToken(bfr, whos[i].begin_token, whos[i].end_token))
            i += 1
        return res
    
    __m_inited = None
    
    @staticmethod
    def initialize() -> None:
        if (BusinessAnalyzer.__m_inited): 
            return
        BusinessAnalyzer.__m_inited = True
        MetaBusinessFact.initialize()
        FundsMeta.initialize()
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        BusinessFactItem.initialize()
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        ProcessorService.registerAnalyzer(BusinessAnalyzer())