# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.business.internal.ResourceHelper import ResourceHelper
from pullenti.ner.business.internal.BusinessFactItemTyp import BusinessFactItemTyp
from pullenti.ner.business.BusinessFactKind import BusinessFactKind
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.business.internal.FundsItemTyp import FundsItemTyp


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
        from pullenti.ner.business.internal.MetaBusinessFact import MetaBusinessFact
        from pullenti.ner.business.internal.FundsMeta import FundsMeta
        return [MetaBusinessFact.GLOBAL_META, FundsMeta.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        from pullenti.ner.business.internal.MetaBusinessFact import MetaBusinessFact
        from pullenti.ner.business.internal.FundsMeta import FundsMeta
        res = dict()
        res[MetaBusinessFact.IMAGE_ID] = ResourceHelper.get_bytes("businessfact.png")
        res[FundsMeta.IMAGE_ID] = ResourceHelper.get_bytes("creditcards.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        from pullenti.ner.business.FundsReferent import FundsReferent
        if (type0_ == BusinessFactReferent.OBJ_TYPENAME): 
            return BusinessFactReferent()
        if (type0_ == FundsReferent.OBJ_TYPENAME): 
            return FundsReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    def process(self, kit : 'AnalysisKit') -> None:
        from pullenti.ner.business.internal.FundsItemToken import FundsItemToken
        from pullenti.ner.Referent import Referent
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        from pullenti.ner.business.FundsReferent import FundsReferent
        ad = kit.get_analyzer_data(self)
        t = kit.first_token
        while t is not None: 
            rt = FundsItemToken.try_attach(t)
            if (rt is not None): 
                rt.referent = ad.register_referent(rt.referent)
                kit.embed_token(rt)
                t = (rt)
            t = t.next0_
        t = kit.first_token
        first_pass3670 = True
        while True:
            if first_pass3670: first_pass3670 = False
            else: t = t.next0_
            if (not (t is not None)): break
            rt = self.__analize_fact(t)
            if (rt is not None): 
                rt.referent = ad.register_referent(rt.referent)
                kit.embed_token(rt)
                t = (rt)
                rts = self.__analize_likelihoods(rt)
                if (rts is not None): 
                    for rt0 in rts: 
                        for s in rt0.referent.slots: 
                            if (s.type_name == BusinessFactReferent.ATTR_WHAT and (isinstance(s.value, FundsReferent))): 
                                rt0.referent.upload_slot(s, ad.register_referent(s.value if isinstance(s.value, Referent) else None))
                        rt0.referent = ad.register_referent(rt0.referent)
                        kit.embed_token(rt0)
                        t = (rt0)
                continue
    
    def __analize_fact(self, t : 'Token') -> 'ReferentToken':
        from pullenti.ner.business.internal.BusinessFactItem import BusinessFactItem
        if (t is None): 
            return None
        bfi = BusinessFactItem.try_parse(t)
        if (bfi is None): 
            return None
        if (bfi.typ == BusinessFactItemTyp.BASE): 
            if (bfi.base_kind == BusinessFactKind.GET or bfi.base_kind == BusinessFactKind.SELL): 
                return self.__analize_get(bfi)
            if (bfi.base_kind == BusinessFactKind.HAVE): 
                if (bfi.is_base_passive or bfi.morph.class0_.is_noun): 
                    re = self.__analize_have(bfi)
                    if (re is not None): 
                        return re
                return self.__analize_get(bfi)
            if (bfi.base_kind == BusinessFactKind.PROFIT or bfi.base_kind == BusinessFactKind.DAMAGES): 
                return self.__analize_profit(bfi)
            if (bfi.base_kind == BusinessFactKind.AGREEMENT or bfi.base_kind == BusinessFactKind.LAWSUIT): 
                return self.__analize_agreement(bfi)
            if (bfi.base_kind == BusinessFactKind.SUBSIDIARY): 
                return self.__analize_subsidiary(bfi)
            if (bfi.base_kind == BusinessFactKind.FINANCE): 
                return self.__analize_finance(bfi)
        return None
    
    def __find_ref_before(self, t : 'Token') -> 'ReferentToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.business.FundsReferent import FundsReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (t is None): 
            return None
        points = 0
        t0 = None
        t1 = t
        first_pass3671 = True
        while True:
            if first_pass3671: first_pass3671 = False
            else: t = t.previous
            if (not (t is not None)): break
            if (t.is_newline_after): 
                break
            if (t.morph.class0_.is_adverb or t.morph.class0_.is_preposition or t.is_comma): 
                continue
            if (t.morph.class0_.is_personal_pronoun): 
                break
            if (t.is_value("ИНФОРМАЦИЯ", None) or t.is_value("ДАННЫЕ", None)): 
                continue
            if (t.is_value("ІНФОРМАЦІЯ", None) or t.is_value("ДАНІ", None)): 
                continue
            if (isinstance(t, TextToken)): 
                if (t.morph.class0_.is_verb): 
                    break
                if (t.is_char('.')): 
                    break
                continue
            r = t.get_referent()
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
                if (t is not None and t.is_char(',')): 
                    t = t.previous
            if (t is None): 
                return None
            refs = t.get_referents()
            if (refs is not None): 
                for r in refs: 
                    if ((isinstance(r, PersonReferent)) or (isinstance(r, OrganizationReferent)) or (isinstance(r, FundsReferent))): 
                        return ReferentToken(r, t, t1)
            return None
        first_pass3672 = True
        while True:
            if first_pass3672: first_pass3672 = False
            else: t = t.previous
            if (not (t is not None)): break
            if (t.is_char('.')): 
                points -= 1
                if ((points) < 0): 
                    break
                continue
            refs = t.get_referents()
            if (refs is not None): 
                for r in refs: 
                    if ((isinstance(r, PersonReferent)) or (isinstance(r, OrganizationReferent))): 
                        return ReferentToken(r, t0, t1)
        return None
    
    def __find_sec_ref_before(self, rt : 'ReferentToken') -> 'ReferentToken':
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.ReferentToken import ReferentToken
        t = (None if rt is None else rt.begin_token.previous)
        if (t is None or t.whitespaces_after_count > 2): 
            return None
        if ((isinstance(rt.get_referent(), PersonReferent)) and (isinstance(t.get_referent(), OrganizationReferent))): 
            return (t if isinstance(t, ReferentToken) else None)
        return None
    
    def __find_date(self, bfr : 'BusinessFactReferent', t : 'Token') -> bool:
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        tt = t
        while tt is not None: 
            r = tt.get_referent()
            if ((isinstance(r, DateReferent)) or (isinstance(r, DateRangeReferent))): 
                bfr.when = r
                return True
            if (tt.is_char('.')): 
                break
            if (tt.is_newline_before): 
                break
            tt = tt.previous
        tt = t
        while tt is not None: 
            if (tt != t and tt.is_newline_before): 
                break
            r = tt.get_referent()
            if ((isinstance(r, DateReferent)) or (isinstance(r, DateRangeReferent))): 
                bfr.when = r
                return True
            if (tt.is_char('.')): 
                break
            tt = tt.next0_
        return False
    
    def __find_sum(self, bfr : 'BusinessFactReferent', t : 'Token') -> bool:
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        from pullenti.ner.business.FundsReferent import FundsReferent
        while t is not None: 
            if (t.is_char('.') or t.is_newline_before): 
                break
            r = t.get_referent()
            if (isinstance(r, MoneyReferent)): 
                fu = (bfr.get_value(BusinessFactReferent.ATTR_WHAT) if isinstance(bfr.get_value(BusinessFactReferent.ATTR_WHAT), FundsReferent) else None)
                if (fu is not None): 
                    if (fu.sum0_ is None): 
                        fu.sum0_ = (r if isinstance(r, MoneyReferent) else None)
                        return True
                bfr.add_slot(BusinessFactReferent.ATTR_MISC, r, False, 0)
                return True
            t = t.next0_
        return False
    
    def __analize_get(self, bfi : 'BusinessFactItem') -> 'ReferentToken':
        from pullenti.ner.business.FundsReferent import FundsReferent
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.person.PersonReferent import PersonReferent
        bef = self.__find_ref_before(bfi.begin_token.previous)
        if (bef is None): 
            return None
        t1 = bfi.end_token.next0_
        if (t1 is None): 
            return None
        first_pass3673 = True
        while True:
            if first_pass3673: first_pass3673 = False
            else: t1 = t1.next0_
            if (not (t1 is not None)): break
            if (t1.morph.class0_.is_adverb): 
                continue
            if (t1.is_value("ПРАВО", None) or t1.is_value("РАСПОРЯЖАТЬСЯ", None) or t1.is_value("РОЗПОРЯДЖАТИСЯ", None)): 
                continue
            break
        if (t1 is None): 
            return None
        if ((isinstance(t1.get_referent(), FundsReferent)) and not ((isinstance(bef.referent, FundsReferent)))): 
            fr = (t1.get_referent() if isinstance(t1.get_referent(), FundsReferent) else None)
            bfr = BusinessFactReferent._new437(bfi.base_kind)
            bfr.who = bef.referent
            bef2 = self.__find_sec_ref_before(bef)
            if (bef2 is not None): 
                bfr.add_slot(BusinessFactReferent.ATTR_WHO, bef2.referent, False, 0)
                bef = bef2
            if (fr.source == bef.referent and bef2 is None): 
                bef2 = self.__find_ref_before(bef.begin_token.previous)
                if (bef2 is not None): 
                    bef = bef2
                    bfr.who = bef.referent
            if (fr.source == bef.referent): 
                cou = 0
                tt = bef.begin_token.previous
                first_pass3674 = True
                while True:
                    if first_pass3674: first_pass3674 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    cou += 1
                    if ((cou) > 100): 
                        break
                    refs = tt.get_referents()
                    if (refs is None): 
                        continue
                    for r in refs: 
                        if ((isinstance(r, OrganizationReferent)) and r != bef.referent): 
                            cou = 1000
                            fr.source = (r if isinstance(r, OrganizationReferent) else None)
                            break
            bfr._add_what(fr)
            bfr.typ = ("покупка ценных бумаг" if bfi.base_kind == BusinessFactKind.GET else (("продажа ценных бумаг" if bfi.base_kind == BusinessFactKind.SELL else "владение ценными бумагами")))
            self.__find_date(bfr, bef.begin_token)
            self.__find_sum(bfr, bef.end_token)
            return ReferentToken(bfr, bef.begin_token, t1)
        if ((bfi.morph.class0_.is_noun and ((bfi.base_kind == BusinessFactKind.GET or bfi.base_kind == BusinessFactKind.SELL)) and (isinstance(t1.get_referent(), OrganizationReferent))) or (isinstance(t1.get_referent(), PersonReferent))): 
            if ((isinstance(bef.referent, FundsReferent)) or (isinstance(bef.referent, OrganizationReferent))): 
                bfr = BusinessFactReferent._new437(bfi.base_kind)
                if (bfi.base_kind == BusinessFactKind.GET): 
                    bfr.typ = ("покупка ценных бумаг" if isinstance(bef.referent, FundsReferent) else "покупка компании")
                elif (bfi.base_kind == BusinessFactKind.SELL): 
                    bfr.typ = ("продажа ценных бумаг" if isinstance(bef.referent, FundsReferent) else "продажа компании")
                bfr.who = t1.get_referent()
                bfr._add_what(bef.referent)
                self.__find_date(bfr, bef.begin_token)
                self.__find_sum(bfr, bef.end_token)
                t1 = BusinessAnalyzer.__add_whos_list(t1, bfr)
                return ReferentToken(bfr, bef.begin_token, t1)
        if ((isinstance(bef.referent, OrganizationReferent)) or (isinstance(bef.referent, PersonReferent))): 
            tt = t1
            if (tt is not None and tt.morph.class0_.is_preposition): 
                tt = tt.next0_
            slav = (None if tt is None else tt.get_referent())
            if ((((isinstance(slav, PersonReferent)) or (isinstance(slav, OrganizationReferent)))) and tt.next0_ is not None and (isinstance(tt.next0_.get_referent(), FundsReferent))): 
                bfr = BusinessFactReferent._new437(bfi.base_kind)
                bfr.typ = ("покупка ценных бумаг" if bfi.base_kind == BusinessFactKind.GET else "продажа ценных бумаг")
                bfr.who = bef.referent
                bef2 = self.__find_sec_ref_before(bef)
                if (bef2 is not None): 
                    bfr.add_slot(BusinessFactReferent.ATTR_WHO, bef2.referent, False, 0)
                    bef = bef2
                bfr.whom = slav
                bfr._add_what(tt.next0_.get_referent())
                self.__find_date(bfr, bef.begin_token)
                self.__find_sum(bfr, bef.end_token)
                return ReferentToken(bfr, bef.begin_token, tt.next0_)
            elif (isinstance(slav, OrganizationReferent)): 
                bfr = BusinessFactReferent._new437(bfi.base_kind)
                bfr.typ = ("покупка компании" if bfi.base_kind == BusinessFactKind.GET else "продажа компании")
                bfr.who = bef.referent
                bef2 = self.__find_sec_ref_before(bef)
                if (bef2 is not None): 
                    bfr.add_slot(BusinessFactReferent.ATTR_WHO, bef2.referent, False, 0)
                    bef = bef2
                bfr._add_what(slav)
                self.__find_date(bfr, bef.begin_token)
                self.__find_sum(bfr, bef.end_token)
                return ReferentToken(bfr, bef.begin_token, tt.next0_)
        if ((isinstance(bef.referent, FundsReferent)) and (((isinstance(t1.get_referent(), OrganizationReferent)) or (isinstance(t1.get_referent(), PersonReferent))))): 
            bfr = BusinessFactReferent._new437(bfi.base_kind)
            bfr.typ = ("покупка ценных бумаг" if bfi.base_kind == BusinessFactKind.GET else (("продажа ценных бумаг" if bfi.base_kind == BusinessFactKind.SELL else "владение ценными бумагами")))
            bfr.who = t1.get_referent()
            bfr._add_what(bef.referent)
            self.__find_date(bfr, bef.begin_token)
            self.__find_sum(bfr, bef.end_token)
            return ReferentToken(bfr, bef.begin_token, t1)
        return None
    
    @staticmethod
    def __add_whos_list(t1 : 'Token', bfr : 'BusinessFactReferent') -> 'Token':
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        if (t1 is None): 
            return None
        if ((t1.next0_ is not None and t1.next0_.is_comma_and and (isinstance(t1.next0_.next0_, ReferentToken))) and t1.next0_.next0_.get_referent().type_name == t1.get_referent().type_name): 
            li = list()
            li.append(t1.next0_.next0_.get_referent())
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
                    if (tt.next0_.get_referent().type_name != t1.get_referent().type_name): 
                        break
                    li.append(tt.next0_.get_referent())
                    if (tt.is_and): 
                        ok = True
                        t1 = tt.next0_
                        break
                    tt = tt.next0_
                if (not ok): 
                    li = (None)
            if (li is not None): 
                for r in li: 
                    bfr.add_slot(BusinessFactReferent.ATTR_WHO, r, False, 0)
        return t1
    
    def __analize_get2(self, t : 'Token') -> 'ReferentToken':
        from pullenti.ner.business.FundsReferent import FundsReferent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (t is None): 
            return None
        tt = t.previous
        ts = t
        if (tt is not None and tt.is_comma): 
            tt = tt.previous
        bef = self.__find_ref_before(tt)
        master = None
        slave = None
        if (bef is not None and (isinstance(bef.referent, FundsReferent))): 
            slave = bef.referent
            ts = bef.begin_token
        tt = t.next0_
        if (tt is None): 
            return None
        te = tt
        r = tt.get_referent()
        if ((isinstance(r, PersonReferent)) or (isinstance(r, OrganizationReferent))): 
            master = r
            if (slave is None and tt.next0_ is not None): 
                r = tt.next0_.get_referent()
                if ((r) is not None): 
                    if ((isinstance(r, FundsReferent)) or (isinstance(r, OrganizationReferent))): 
                        slave = (r if isinstance(r, FundsReferent) else None)
                        te = tt.next0_
        if (master is not None and slave is not None): 
            bfr = BusinessFactReferent._new437(BusinessFactKind.HAVE)
            bfr.who = master
            if (isinstance(slave, OrganizationReferent)): 
                bfr._add_what(slave)
                bfr.typ = "владение компанией"
            elif (isinstance(slave, FundsReferent)): 
                bfr._add_what(slave)
                bfr.typ = "владение ценными бумагами"
            else: 
                return None
            return ReferentToken(bfr, ts, te)
        return None
    
    def __analize_have(self, bfi : 'BusinessFactItem') -> 'ReferentToken':
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.business.FundsReferent import FundsReferent
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        from pullenti.ner.ReferentToken import ReferentToken
        t = bfi.end_token.next0_
        t1 = None
        if (t is not None and ((t.is_value("КОТОРЫЙ", None) or t.is_value("ЯКИЙ", None)))): 
            t1 = t.next0_
        else: 
            tt = bfi.begin_token
            while tt != bfi.end_token: 
                if (tt.morph.class0_.is_pronoun): 
                    t1 = t
                tt = tt.next0_
            if (t1 is None): 
                if (bfi.is_base_passive and t is not None and (((isinstance(t.get_referent(), PersonReferent)) or (isinstance(t.get_referent(), OrganizationReferent))))): 
                    t1 = t
                    if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), FundsReferent))): 
                        bfr = BusinessFactReferent._new437(BusinessFactKind.HAVE)
                        bfr.who = t.get_referent()
                        bfr._add_what(t.next0_.get_referent())
                        bfr.typ = "владение ценными бумагами"
                        return ReferentToken(bfr, bfi.begin_token, t.next0_)
        t0 = None
        slave = None
        mus_be_verb = False
        if (t1 is not None): 
            tt0 = bfi.begin_token.previous
            if (tt0 is not None and tt0.is_char(',')): 
                tt0 = tt0.previous
            bef = self.__find_ref_before(tt0)
            if (bef is None): 
                return None
            if (not ((isinstance(bef.referent, OrganizationReferent)))): 
                return None
            t0 = bef.begin_token
            slave = bef.referent
        elif (bfi.end_token.get_morph_class_in_dictionary().is_noun and (isinstance(t.get_referent(), OrganizationReferent))): 
            slave = t.get_referent()
            t1 = t.next0_
            t0 = bfi.begin_token
            mus_be_verb = True
        if (t0 is None or t1 is None or slave is None): 
            return None
        if ((t1.is_hiphen or t1.is_value("ЯВЛЯТЬСЯ", None) or t1.is_value("БУТИ", None)) or t1.is_value("Є", None)): 
            t1 = t1.next0_
        elif (mus_be_verb): 
            return None
        r = (None if t1 is None else t1.get_referent())
        if ((isinstance(r, OrganizationReferent)) or (isinstance(r, PersonReferent))): 
            bfr = BusinessFactReferent._new437(BusinessFactKind.HAVE)
            bfr.who = r
            bfr._add_what(slave)
            if (bfi.end_token.is_value("АКЦИОНЕР", None) or bfi.end_token.is_value("АКЦІОНЕР", None)): 
                bfr.typ = "владение ценными бумагами"
            else: 
                bfr.typ = "владение компанией"
            t1 = BusinessAnalyzer.__add_whos_list(t1, bfr)
            return ReferentToken(bfr, t0, t1)
        return None
    
    def __analize_profit(self, bfi : 'BusinessFactItem') -> 'ReferentToken':
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner._org.OrganizationAnalyzer import OrganizationAnalyzer
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (bfi.end_token.next0_ is None): 
            return None
        t0 = bfi.begin_token
        t1 = bfi.end_token
        typ = t1.get_normal_case_text(MorphClass(), True, MorphGender.UNDEFINED, False).lower()
        org0_ = None
        org0_ = (t1.next0_.get_referent() if isinstance(t1.next0_.get_referent(), OrganizationReferent) else None)
        t = t1
        if (org0_ is not None): 
            t = t.next0_
        else: 
            rt = t.kit.process_referent(OrganizationAnalyzer.ANALYZER_NAME, t.next0_)
            if (rt is not None): 
                org0_ = (rt.referent if isinstance(rt.referent, OrganizationReferent) else None)
                t = rt.end_token
        dt = None
        sum0_ = None
        t = t.next0_
        first_pass3675 = True
        while True:
            if first_pass3675: first_pass3675 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_char('.')): 
                break
            if (t.is_char('(')): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    t = br.end_token
                    continue
            if ((((t.morph.class0_.is_verb or t.is_value("ДО", None) or t.is_hiphen) or t.is_value("РАЗМЕР", None) or t.is_value("РОЗМІР", None))) and t.next0_ is not None and (isinstance(t.next0_.get_referent(), MoneyReferent))): 
                if (sum0_ is not None): 
                    break
                sum0_ = (t.next0_.get_referent() if isinstance(t.next0_.get_referent(), MoneyReferent) else None)
                t = t.next0_
                t1 = t
                continue
            r = t.get_referent()
            if ((isinstance(r, DateRangeReferent)) or (isinstance(r, DateReferent))): 
                if (dt is None): 
                    dt = r
                    t1 = t
            elif ((isinstance(r, OrganizationReferent)) and org0_ is None): 
                org0_ = (r if isinstance(r, OrganizationReferent) else None)
                t1 = t
        if (sum0_ is None): 
            return None
        if (org0_ is None): 
            tt = t0.previous
            while tt is not None: 
                if (tt.is_char('.')): 
                    break
                b0 = (tt.get_referent() if isinstance(tt.get_referent(), BusinessFactReferent) else None)
                if (b0 is not None): 
                    org0_ = (b0.who if isinstance(b0.who, OrganizationReferent) else None)
                    break
                org0_ = (tt.get_referent() if isinstance(tt.get_referent(), OrganizationReferent) else None)
                if ((org0_) is not None): 
                    break
                tt = tt.previous
        if (org0_ is None): 
            return None
        bfr = BusinessFactReferent._new437(bfi.base_kind)
        bfr.who = org0_
        bfr.typ = typ
        bfr.add_slot(BusinessFactReferent.ATTR_MISC, sum0_, False, 0)
        if (dt is not None): 
            bfr.when = dt
        else: 
            self.__find_date(bfr, bfi.begin_token)
        return ReferentToken(bfr, t0, t1)
    
    def __analize_agreement(self, bfi : 'BusinessFactItem') -> 'ReferentToken':
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.ReferentToken import ReferentToken
        first = None
        second = None
        t0 = bfi.begin_token
        t1 = bfi.end_token
        max_lines = 1
        t = bfi.begin_token.previous
        first_pass3676 = True
        while True:
            if first_pass3676: first_pass3676 = False
            else: t = t.previous
            if (not (t is not None)): break
            if (t.is_char('.') or t.is_newline_after): 
                max_lines -= 1
                if ((max_lines) == 0): 
                    break
                continue
            if (t.is_value("СТОРОНА", None) and t.previous is not None and ((t.previous.is_value("МЕЖДУ", None) or t.previous.is_value("МІЖ", None)))): 
                max_lines = 2
                t = t.previous
                t0 = t
                continue
            r = t.get_referent()
            if (isinstance(r, BusinessFactReferent)): 
                b = (r if isinstance(r, BusinessFactReferent) else None)
                if (b.who is not None and ((b.who2 is not None or b.whom is not None))): 
                    first = b.who
                    second = (Utils.ifNotNull(b.who2, b.whom))
                    break
            if (not ((isinstance(r, OrganizationReferent)))): 
                continue
            if ((t.previous is not None and ((t.previous.is_and or t.previous.is_value("К", None))) and t.previous.previous is not None) and (isinstance(t.previous.previous.get_referent(), OrganizationReferent))): 
                t0 = t.previous.previous
                first = t0.get_referent()
                second = r
                break
            else: 
                t0 = t
                first = r
                break
        if (second is None): 
            t = bfi.end_token.next0_
            first_pass3677 = True
            while True:
                if first_pass3677: first_pass3677 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_char('.')): 
                    break
                if (t.is_newline_before): 
                    break
                r = t.get_referent()
                if (not ((isinstance(r, OrganizationReferent)))): 
                    continue
                if ((t.next0_ is not None and ((t.next0_.is_and or t.next0_.is_value("К", None))) and t.next0_.next0_ is not None) and (isinstance(t.next0_.next0_.get_referent(), OrganizationReferent))): 
                    t1 = t.next0_.next0_
                    first = r
                    second = t1.get_referent()
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
        self.__find_date(bf, bfi.begin_token)
        self.__find_sum(bf, bfi.begin_token)
        return ReferentToken(bf, t0, t1)
    
    def __analize_subsidiary(self, bfi : 'BusinessFactItem') -> 'ReferentToken':
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        from pullenti.ner.ReferentToken import ReferentToken
        t1 = bfi.end_token.next0_
        if (t1 is None or not ((isinstance(t1.get_referent(), OrganizationReferent)))): 
            return None
        org0 = None
        t = bfi.begin_token.previous
        first_pass3678 = True
        while True:
            if first_pass3678: first_pass3678 = False
            else: t = t.previous
            if (not (t is not None)): break
            if (t.is_char('(') or t.is_char('%')): 
                continue
            if (t.morph.class0_.is_verb): 
                continue
            if (isinstance(t, NumberToken)): 
                continue
            org0 = (t.get_referent() if isinstance(t.get_referent(), OrganizationReferent) else None)
            if (org0 is not None): 
                break
        if (org0 is None): 
            return None
        bfr = BusinessFactReferent._new437(bfi.base_kind)
        bfr.who = org0
        bfr.whom = t1.get_referent()
        return ReferentToken(bfr, t, t1)
    
    def __analize_finance(self, bfi : 'BusinessFactItem') -> 'ReferentToken':
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        from pullenti.ner.business.FundsReferent import FundsReferent
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        bef = self.__find_ref_before(bfi.begin_token.previous)
        if (bef is None): 
            return None
        if (not ((isinstance(bef.referent, OrganizationReferent))) and not ((isinstance(bef.referent, PersonReferent)))): 
            return None
        whom = None
        sum0_ = None
        funds = None
        t = bfi.end_token.next0_
        while t is not None: 
            if (t.is_newline_before or t.is_char('.')): 
                break
            r = t.get_referent()
            if (isinstance(r, OrganizationReferent)): 
                if (whom is None): 
                    whom = (t if isinstance(t, ReferentToken) else None)
            elif (isinstance(r, MoneyReferent)): 
                if (sum0_ is None): 
                    sum0_ = (r if isinstance(r, MoneyReferent) else None)
            elif (isinstance(r, FundsReferent)): 
                if (funds is None): 
                    funds = (r if isinstance(r, FundsReferent) else None)
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
            bfr._add_what(funds)
        if (sum0_ is not None): 
            bfr.add_slot(BusinessFactReferent.ATTR_MISC, sum0_, False, 0)
        self.__find_date(bfr, bef.begin_token)
        return ReferentToken(bfr, bef.begin_token, whom.end_token)
    
    def __analize_likelihoods(self, rt : 'ReferentToken') -> typing.List['ReferentToken']:
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        from pullenti.ner.business.FundsReferent import FundsReferent
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.business.internal.FundsItemToken import FundsItemToken
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        bfr0 = (rt.referent if isinstance(rt.referent, BusinessFactReferent) else None)
        if (bfr0 is None or len(bfr0.whats) != 1 or not ((isinstance(bfr0.whats[0], FundsReferent)))): 
            return None
        funds0 = (bfr0.whats[0] if isinstance(bfr0.whats[0], FundsReferent) else None)
        whos = list()
        funds = list()
        t = rt.end_token.next0_
        first_pass3679 = True
        while True:
            if first_pass3679: first_pass3679 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_before or t.is_char('.')): 
                break
            if (t.morph.class0_.is_adverb): 
                continue
            if (t.is_hiphen or t.is_comma_and): 
                continue
            if (t.morph.class0_.is_conjunction or t.morph.class0_.is_preposition or t.morph.class0_.is_misc): 
                continue
            r = t.get_referent()
            if ((isinstance(r, OrganizationReferent)) or (isinstance(r, PersonReferent))): 
                whos.append(t if isinstance(t, ReferentToken) else None)
                continue
            if (isinstance(r, FundsReferent)): 
                funds0 = (r if isinstance(r, FundsReferent) else None)
                funds.append(funds0)
                continue
            it = FundsItemToken.try_parse(t, None)
            if (it is None): 
                break
            fu = (funds0.clone() if isinstance(funds0.clone(), FundsReferent) else None)
            fu.occurrence.clear()
            fu.add_occurence_of_ref_tok(ReferentToken(fu, it.begin_token, it.end_token))
            if (it.typ == FundsItemTyp.PERCENT): 
                fu.percent = it.float_val
            elif (it.typ == FundsItemTyp.COUNT): 
                fu.count = it.long_val
            elif (it.typ == FundsItemTyp.SUM): 
                fu.sum0_ = (it.ref if isinstance(it.ref, MoneyReferent) else None)
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
            bfr._add_what(funds[i])
            for s in bfr0.slots: 
                if (s.type_name == BusinessFactReferent.ATTR_MISC or s.type_name == BusinessFactReferent.ATTR_WHEN): 
                    bfr.add_slot(s.type_name, s.value, False, 0)
            res.append(ReferentToken(bfr, whos[i].begin_token, whos[i].end_token))
            i += 1
        return res
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.ProcessorService import ProcessorService
        from pullenti.ner.business.internal.BusinessFactItem import BusinessFactItem
        ProcessorService.register_analyzer(BusinessAnalyzer())
        BusinessFactItem.initialize()