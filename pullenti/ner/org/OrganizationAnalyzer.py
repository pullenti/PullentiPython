# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import math
import io
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.org.internal.OrgItemTypeTyp import OrgItemTypeTyp
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.TextAnnotation import TextAnnotation
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.org.internal.OrgItemNumberToken import OrgItemNumberToken
from pullenti.morph.CharsInfo import CharsInfo
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.org.internal.OrgGlobal import OrgGlobal
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.Token import Token
from pullenti.ner.org.OrganizationKind import OrganizationKind
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.internal.PullentiNerCoreInternalResourceHelper import PullentiNerCoreInternalResourceHelper
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.Referent import Referent
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.org.internal.MetaOrganization import MetaOrganization
from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.org.internal.OrgOwnershipHelper import OrgOwnershipHelper
from pullenti.ner.org.internal.OrgItemTypeToken import OrgItemTypeToken
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class OrganizationAnalyzer(Analyzer):
    """ Анализатор организаций """
    
    class AttachType(IntEnum):
        NORMAL = 0
        NORMALAFTERDEP = 1
        MULTIPLE = 2
        HIGH = 3
        EXTONTOLOGY = 4
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    class OrgAnalyzerData(AnalyzerDataWithOntology):
        
        def __init__(self) -> None:
            from pullenti.ner.core.TerminCollection import TerminCollection
            from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
            super().__init__()
            self.loc_orgs = IntOntologyCollection()
            self.org_pure_names = TerminCollection()
            self.aliases = TerminCollection()
            self.large_text_regim = False
        
        def register_referent(self, referent : 'Referent') -> 'Referent':
            from pullenti.ner.core.Termin import Termin
            from pullenti.ner.org.OrganizationReferent import OrganizationReferent
            if (isinstance(referent, OrganizationReferent)): 
                referent._final_correction()
            slots = len(referent.slots)
            res = super().register_referent(referent)
            if (not self.large_text_regim and (isinstance(res, OrganizationReferent)) and ((res == referent or len(res.slots) != slots))): 
                ioi = res.create_ontology_item_ex(2, True, False)
                if (ioi is not None): 
                    self.loc_orgs.add_item(ioi)
                names = res._get_pure_names()
                if (names is not None): 
                    for n in names: 
                        self.org_pure_names.add(Termin(n))
            return res
    
    ANALYZER_NAME = "ORGANIZATION"
    """ Имя анализатора ("ORGANIZATION") """
    
    @property
    def name(self) -> str:
        return OrganizationAnalyzer.ANALYZER_NAME
    
    def clone(self) -> 'Analyzer':
        return OrganizationAnalyzer()
    
    @property
    def caption(self) -> str:
        return "Организации"
    
    @property
    def description(self) -> str:
        return "Организации, предприятия, компании..."
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaOrganization._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[Utils.enumToString(OrgProfile.UNIT)] = PullentiNerCoreInternalResourceHelper.get_bytes("dep.png")
        res[Utils.enumToString(OrgProfile.UNION)] = PullentiNerCoreInternalResourceHelper.get_bytes("party.png")
        res[Utils.enumToString(OrgProfile.COMPETITION)] = PullentiNerCoreInternalResourceHelper.get_bytes("festival.png")
        res[Utils.enumToString(OrgProfile.HOLDING)] = PullentiNerCoreInternalResourceHelper.get_bytes("holding.png")
        res[Utils.enumToString(OrgProfile.STATE)] = PullentiNerCoreInternalResourceHelper.get_bytes("gov.png")
        res[Utils.enumToString(OrgProfile.FINANCE)] = PullentiNerCoreInternalResourceHelper.get_bytes("bank.png")
        res[Utils.enumToString(OrgProfile.EDUCATION)] = PullentiNerCoreInternalResourceHelper.get_bytes("study.png")
        res[Utils.enumToString(OrgProfile.SCIENCE)] = PullentiNerCoreInternalResourceHelper.get_bytes("science.png")
        res[Utils.enumToString(OrgProfile.INDUSTRY)] = PullentiNerCoreInternalResourceHelper.get_bytes("factory.png")
        res[Utils.enumToString(OrgProfile.TRADE)] = PullentiNerCoreInternalResourceHelper.get_bytes("trade.png")
        res[Utils.enumToString(OrgProfile.POLICY)] = PullentiNerCoreInternalResourceHelper.get_bytes("politics.png")
        res[Utils.enumToString(OrgProfile.JUSTICE)] = PullentiNerCoreInternalResourceHelper.get_bytes("justice.png")
        res[Utils.enumToString(OrgProfile.ENFORCEMENT)] = PullentiNerCoreInternalResourceHelper.get_bytes("gov.png")
        res[Utils.enumToString(OrgProfile.ARMY)] = PullentiNerCoreInternalResourceHelper.get_bytes("military.png")
        res[Utils.enumToString(OrgProfile.SPORT)] = PullentiNerCoreInternalResourceHelper.get_bytes("sport.png")
        res[Utils.enumToString(OrgProfile.RELIGION)] = PullentiNerCoreInternalResourceHelper.get_bytes("church.png")
        res[Utils.enumToString(OrgProfile.MUSIC)] = PullentiNerCoreInternalResourceHelper.get_bytes("music.png")
        res[Utils.enumToString(OrgProfile.MEDIA)] = PullentiNerCoreInternalResourceHelper.get_bytes("media.png")
        res[Utils.enumToString(OrgProfile.PRESS)] = PullentiNerCoreInternalResourceHelper.get_bytes("press.png")
        res[Utils.enumToString(OrgProfile.HOTEL)] = PullentiNerCoreInternalResourceHelper.get_bytes("hotel.png")
        res[Utils.enumToString(OrgProfile.MEDICINE)] = PullentiNerCoreInternalResourceHelper.get_bytes("medicine.png")
        res[Utils.enumToString(OrgProfile.TRANSPORT)] = PullentiNerCoreInternalResourceHelper.get_bytes("train.png")
        res[Utils.enumToString(OrganizationKind.BANK)] = PullentiNerCoreInternalResourceHelper.get_bytes("bank.png")
        res[Utils.enumToString(OrganizationKind.CULTURE)] = PullentiNerCoreInternalResourceHelper.get_bytes("culture.png")
        res[Utils.enumToString(OrganizationKind.DEPARTMENT)] = PullentiNerCoreInternalResourceHelper.get_bytes("dep.png")
        res[Utils.enumToString(OrganizationKind.FACTORY)] = PullentiNerCoreInternalResourceHelper.get_bytes("factory.png")
        res[Utils.enumToString(OrganizationKind.GOVENMENT)] = PullentiNerCoreInternalResourceHelper.get_bytes("gov.png")
        res[Utils.enumToString(OrganizationKind.MEDICAL)] = PullentiNerCoreInternalResourceHelper.get_bytes("medicine.png")
        res[Utils.enumToString(OrganizationKind.PARTY)] = PullentiNerCoreInternalResourceHelper.get_bytes("party.png")
        res[Utils.enumToString(OrganizationKind.STUDY)] = PullentiNerCoreInternalResourceHelper.get_bytes("study.png")
        res[Utils.enumToString(OrganizationKind.FEDERATION)] = PullentiNerCoreInternalResourceHelper.get_bytes("federation.png")
        res[Utils.enumToString(OrganizationKind.CHURCH)] = PullentiNerCoreInternalResourceHelper.get_bytes("church.png")
        res[Utils.enumToString(OrganizationKind.MILITARY)] = PullentiNerCoreInternalResourceHelper.get_bytes("military.png")
        res[Utils.enumToString(OrganizationKind.AIRPORT)] = PullentiNerCoreInternalResourceHelper.get_bytes("avia.png")
        res[Utils.enumToString(OrganizationKind.FESTIVAL)] = PullentiNerCoreInternalResourceHelper.get_bytes("festival.png")
        res[MetaOrganization.ORG_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("org.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == OrganizationReferent.OBJ_TYPENAME): 
            return OrganizationReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return [GeoReferent.OBJ_TYPENAME, AddressReferent.OBJ_TYPENAME]
    
    @property
    def progress_weight(self) -> int:
        return 45
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        return OrganizationAnalyzer.OrgAnalyzerData()
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = Utils.asObjectOrNull(kit.get_analyzer_data(self), OrganizationAnalyzer.OrgAnalyzerData)
        if (len(kit.sofa.text) > 400000): 
            ad.large_text_regim = True
        else: 
            ad.large_text_regim = False
        t = kit.first_token
        while t is not None: 
            t.inner_bool = False
            t = t.next0_
        steps = 2
        max0_ = steps
        delta = 100000
        parts = math.floor((((len(kit.sofa.text) + delta) - 1)) / delta)
        if (parts == 0): 
            parts = 1
        max0_ *= parts
        cur = 0
        step = 0
        while step < steps: 
            next_pos = delta
            t = kit.first_token
            while t is not None: 
                if (t.begin_char > next_pos): 
                    next_pos += delta
                    cur += 1
                    if (not self._on_progress(cur, max0_, kit)): 
                        return
                if (step > 0 and (isinstance(t, ReferentToken)) and (isinstance(t.get_referent(), OrganizationReferent))): 
                    mt = OrganizationAnalyzer._check_alias_after(Utils.asObjectOrNull(t, ReferentToken), t.next0_)
                    if (mt is not None): 
                        if (ad is not None): 
                            term = Termin()
                            term.init_by(mt.begin_token, mt.end_token.previous, t.get_referent(), False)
                            ad.aliases.add(term)
                        rt = ReferentToken(t.get_referent(), t, mt.end_token)
                        kit.embed_token(rt)
                        t = (rt)
                while True:
                    rts = self.__try_attach_orgs(t, ad, step)
                    if (rts is None or len(rts) == 0): 
                        break
                    if (not MetaToken.check(rts)): 
                        break
                    emb = False
                    for rt in rts: 
                        if (not rt.referent._check_correction()): 
                            continue
                        rt.referent = ad.register_referent(rt.referent)
                        if (rt.begin_token.get_referent() == rt.referent or rt.end_token.get_referent() == rt.referent): 
                            continue
                        kit.embed_token(rt)
                        emb = True
                        if (rt.begin_char <= t.begin_char): 
                            t = (rt)
                    if ((len(rts) == 1 and t == rts[0] and (isinstance(t.next0_, ReferentToken))) and (isinstance(t.next0_.get_referent(), OrganizationReferent))): 
                        org0 = Utils.asObjectOrNull(rts[0].referent, OrganizationReferent)
                        org1 = Utils.asObjectOrNull(t.next0_.get_referent(), OrganizationReferent)
                        if (org1.higher is None and OrgOwnershipHelper.can_be_higher(org0, org1, False) and not OrgOwnershipHelper.can_be_higher(org1, org0, False)): 
                            rtt = Utils.asObjectOrNull(t.next0_, ReferentToken)
                            kit.debed_token(rtt)
                            org1.higher = org0
                            rt1 = ReferentToken._new734(ad.register_referent(org1), t, rtt.end_token, t.next0_.morph)
                            kit.embed_token(rt1)
                            t = (rt1)
                    if (emb and not (isinstance(t, ReferentToken))): 
                        continue
                    break
                if (step > 0): 
                    rt = self.__check_ownership(t)
                    if (rt is not None): 
                        kit.embed_token(rt)
                        t = (rt)
                if ((isinstance(t, ReferentToken)) and (isinstance(t.get_referent(), OrganizationReferent))): 
                    rt0 = Utils.asObjectOrNull(t, ReferentToken)
                    while rt0 is not None:
                        rt0 = self.__try_attach_org_before(rt0, ad)
                        if (rt0 is None): 
                            break
                        self.__do_post_analyze(rt0, ad)
                        rt0.referent = ad.register_referent(rt0.referent)
                        kit.embed_token(rt0)
                        t = (rt0)
                if (step > 0 and (isinstance(t, ReferentToken)) and (isinstance(t.get_referent(), OrganizationReferent))): 
                    mt = OrganizationAnalyzer._check_alias_after(Utils.asObjectOrNull(t, ReferentToken), t.next0_)
                    if (mt is not None): 
                        if (ad is not None): 
                            term = Termin()
                            term.init_by(mt.begin_token, mt.end_token.previous, t.get_referent(), False)
                            ad.aliases.add(term)
                        rt = ReferentToken(t.get_referent(), t, mt.end_token)
                        kit.embed_token(rt)
                        t = (rt)
                t = t.next0_
            if (len(ad.referents) == 0): 
                if (not "o2step" in kit.misc_data): 
                    break
            step += 1
        list0_ = list()
        t = kit.first_token
        first_pass3813 = True
        while True:
            if first_pass3813: first_pass3813 = False
            else: t = t.next0_
            if (not (t is not None)): break
            org0_ = Utils.asObjectOrNull(t.get_referent(), OrganizationReferent)
            if (org0_ is None): 
                continue
            t1 = t.next0_
            if (((t1 is not None and t1.is_char('(') and t1.next0_ is not None) and (isinstance(t1.next0_.get_referent(), OrganizationReferent)) and t1.next0_.next0_ is not None) and t1.next0_.next0_.is_char(')')): 
                org0 = Utils.asObjectOrNull(t1.next0_.get_referent(), OrganizationReferent)
                if (org0 == org0_ or org0_.higher == org0): 
                    rt1 = ReferentToken._new734(org0_, t, t1.next0_.next0_, t.morph)
                    kit.embed_token(rt1)
                    t = (rt1)
                    t1 = t.next0_
                elif (org0_.higher is None and OrgOwnershipHelper.can_be_higher(org0, org0_, False) and not OrgOwnershipHelper.can_be_higher(org0_, org0, False)): 
                    org0_.higher = org0
                    rt1 = ReferentToken._new734(org0_, t, t1.next0_.next0_, t.morph)
                    kit.embed_token(rt1)
                    t = (rt1)
                    t1 = t.next0_
            of_tok = None
            if (t1 is not None): 
                if (t1.is_char_of(",") or t1.is_hiphen): 
                    t1 = t1.next0_
                elif (not kit.onto_regime and t1.is_char(';')): 
                    t1 = t1.next0_
                elif (t1.is_value("ПРИ", None) or t1.is_value("OF", None) or t1.is_value("AT", None)): 
                    of_tok = (Utils.asObjectOrNull(t1, TextToken))
                    t1 = t1.next0_
            if (t1 is None): 
                break
            org1 = Utils.asObjectOrNull(t1.get_referent(), OrganizationReferent)
            if (org1 is None): 
                continue
            if (of_tok is None): 
                if (org0_.higher is None): 
                    if (not OrgOwnershipHelper.can_be_higher(org1, org0_, False)): 
                        if (t1.previous != t or t1.whitespaces_after_count > 2): 
                            continue
                        pp = t.kit.process_referent("PERSON", t1.next0_)
                        if (pp is not None): 
                            pass
                        else: 
                            continue
            if (org0_.higher is not None): 
                if (not org0_.higher.can_be_equals(org1, ReferentsEqualType.WITHINONETEXT)): 
                    continue
            list0_.clear()
            list0_.append(Utils.asObjectOrNull(t, ReferentToken))
            list0_.append(Utils.asObjectOrNull(t1, ReferentToken))
            if (of_tok is not None and org0_.higher is None): 
                t2 = t1.next0_
                while t2 is not None: 
                    if (((isinstance(t2, TextToken)) and t2.term == of_tok.term and t2.next0_ is not None) and (isinstance(t2.next0_.get_referent(), OrganizationReferent))): 
                        t2 = t2.next0_
                        if (org1.higher is not None): 
                            if (not org1.higher.can_be_equals(t2.get_referent(), ReferentsEqualType.WITHINONETEXT)): 
                                break
                        list0_.append(Utils.asObjectOrNull(t2, ReferentToken))
                        org1 = (Utils.asObjectOrNull(t2.get_referent(), OrganizationReferent))
                    else: 
                        break
                    t2 = t2.next0_
            rt0 = list0_[len(list0_) - 1]
            for i in range(len(list0_) - 2, -1, -1):
                org0_ = (Utils.asObjectOrNull(list0_[i].referent, OrganizationReferent))
                org1 = (Utils.asObjectOrNull(rt0.referent, OrganizationReferent))
                if (org0_.higher is None): 
                    org0_.higher = org1
                    org0_ = (Utils.asObjectOrNull(ad.register_referent(org0_), OrganizationReferent))
                rt = ReferentToken(org0_, list0_[i], rt0)
                kit.embed_token(rt)
                t = (rt)
                rt0 = rt
        owners = dict()
        t = kit.first_token
        first_pass3814 = True
        while True:
            if first_pass3814: first_pass3814 = False
            else: t = t.next0_
            if (not (t is not None)): break
            org0_ = Utils.asObjectOrNull(t.get_referent(), OrganizationReferent)
            if (org0_ is None): 
                continue
            hi = org0_.higher
            if (hi is None): 
                continue
            for ty in org0_.types: 
                li = [ ]
                wrapli2344 = RefOutArgWrapper(None)
                inoutres2345 = Utils.tryGetValue(owners, ty, wrapli2344)
                li = wrapli2344.value
                if (not inoutres2345): 
                    li = list()
                    owners[ty] = li
                childs = None
                if (not hi in li): 
                    li.append(hi)
                    childs = list()
                    hi.tag = childs
                else: 
                    childs = (Utils.asObjectOrNull(hi.tag, list))
                if (childs is not None and not org0_ in childs): 
                    childs.append(org0_)
        owns = list()
        last_mvd_org = None
        t = kit.first_token
        first_pass3815 = True
        while True:
            if first_pass3815: first_pass3815 = False
            else: t = t.next0_
            if (not (t is not None)): break
            org0_ = Utils.asObjectOrNull(t.get_referent(), OrganizationReferent)
            if (org0_ is None): 
                continue
            if (OrganizationAnalyzer.__is_mvd_org(org0_) is not None): 
                last_mvd_org = t
            if (org0_.higher is not None): 
                continue
            owns.clear()
            for ty in org0_.types: 
                li = [ ]
                wrapli2346 = RefOutArgWrapper(None)
                inoutres2347 = Utils.tryGetValue(owners, ty, wrapli2346)
                li = wrapli2346.value
                if (not inoutres2347): 
                    continue
                for h in li: 
                    if (not h in owns): 
                        owns.append(h)
            if (len(owns) != 1): 
                continue
            if (OrgOwnershipHelper.can_be_higher(owns[0], org0_, True)): 
                childs = Utils.asObjectOrNull(owns[0].tag, list)
                if (childs is None): 
                    continue
                has_num = False
                has_geo = False
                for oo in childs: 
                    if (oo.find_slot(OrganizationReferent.ATTR_GEO, None, True) is not None): 
                        has_geo = True
                    if (oo.find_slot(OrganizationReferent.ATTR_NUMBER, None, True) is not None): 
                        has_num = True
                if (has_num != ((org0_.find_slot(OrganizationReferent.ATTR_NUMBER, None, True) is not None))): 
                    continue
                if (has_geo != ((org0_.find_slot(OrganizationReferent.ATTR_GEO, None, True) is not None))): 
                    continue
                org0_.higher = owns[0]
                if (org0_.kind != OrganizationKind.DEPARTMENT): 
                    org0_.higher = None
        t = last_mvd_org
        first_pass3816 = True
        while True:
            if first_pass3816: first_pass3816 = False
            else: t = t.previous
            if (not (t is not None)): break
            if (not (isinstance(t, ReferentToken))): 
                continue
            mvd = OrganizationAnalyzer.__is_mvd_org(Utils.asObjectOrNull(t.get_referent(), OrganizationReferent))
            if (mvd is None): 
                continue
            t1 = None
            br = False
            tt = t.previous
            first_pass3817 = True
            while True:
                if first_pass3817: first_pass3817 = False
                else: tt = tt.previous
                if (not (tt is not None)): break
                if (tt.is_char(')')): 
                    br = True
                    continue
                if (br): 
                    if (tt.is_char('(')): 
                        br = False
                    continue
                if (not (isinstance(tt, TextToken))): 
                    break
                if (tt.length_char < 2): 
                    continue
                if (tt.chars.is_all_upper or ((not tt.chars.is_all_upper and not tt.chars.is_all_lower and not tt.chars.is_capital_upper))): 
                    t1 = tt
                break
            if (t1 is None): 
                continue
            t0 = t1
            if ((isinstance(t0.previous, TextToken)) and (t0.whitespaces_before_count < 2) and t0.previous.length_char >= 2): 
                if (t0.previous.chars.is_all_upper or ((not t0.previous.chars.is_all_upper and not t0.previous.chars.is_all_lower and not t0.previous.chars.is_capital_upper))): 
                    t0 = t0.previous
            nam = MiscHelper.get_text_value(t0, t1, GetTextAttr.NO)
            if ((nam == "ОВД" or nam == "ГУВД" or nam == "УВД") or nam == "ГУ"): 
                continue
            mc = t0.get_morph_class_in_dictionary()
            if (not mc.is_undefined): 
                continue
            mc = t1.get_morph_class_in_dictionary()
            if (not mc.is_undefined): 
                continue
            org0_ = OrganizationReferent()
            org0_.add_profile(OrgProfile.UNIT)
            org0_.add_name(nam, True, None)
            org0_.higher = mvd
            rt = ReferentToken(ad.register_referent(org0_), t0, t1)
            kit.embed_token(rt)
            t = rt.next0_
            if (t is None): 
                break
    
    @staticmethod
    def __is_mvd_org(org0_ : 'OrganizationReferent') -> 'OrganizationReferent':
        if (org0_ is None): 
            return None
        res = None
        for i in range(5):
            if (res is None): 
                for s in org0_.slots: 
                    if (s.type_name == OrganizationReferent.ATTR_TYPE): 
                        res = org0_
                        break
            if (org0_.find_slot(OrganizationReferent.ATTR_NAME, "МВД", True) is not None or org0_.find_slot(OrganizationReferent.ATTR_NAME, "ФСБ", True) is not None): 
                return Utils.ifNotNull(res, org0_)
            org0_ = org0_.higher
            if (org0_ is None): 
                break
        return None
    
    @staticmethod
    def _check_alias_after(rt : 'ReferentToken', t : 'Token') -> 'MetaToken':
        if ((t is not None and t.is_char('<') and t.next0_ is not None) and t.next0_.next0_ is not None and t.next0_.next0_.is_char('>')): 
            t = t.next0_.next0_.next0_
        if (t is None or t.next0_ is None or not t.is_char('(')): 
            return None
        t = t.next0_
        if (t.is_value("ДАЛЕЕ", None) or t.is_value("ДАЛІ", None)): 
            t = t.next0_
        elif (t.is_value("HEREINAFTER", None) or t.is_value("ABBREVIATED", None) or t.is_value("HEREAFTER", None)): 
            t = t.next0_
            if (t is not None and t.is_value("REFER", None)): 
                t = t.next0_
        else: 
            return None
        while t is not None:
            if (not (isinstance(t, TextToken))): 
                break
            elif (not t.chars.is_letter): 
                t = t.next0_
            elif (t.morph.class0_.is_preposition or t.morph.class0_.is_misc or t.is_value("ИМЕНОВАТЬ", None)): 
                t = t.next0_
            else: 
                break
        if (t is None): 
            return None
        t1 = None
        tt = t
        while tt is not None: 
            if (tt.is_newline_before): 
                break
            elif (tt.is_char(')')): 
                t1 = tt.previous
                break
            tt = tt.next0_
        if (t1 is None): 
            return None
        mt = MetaToken(t, t1.next0_)
        nam = MiscHelper.get_text_value(t, t1, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
        mt.tag = (nam)
        if (nam.find(' ') < 0): 
            tt = rt.begin_token
            while tt is not None and tt.end_char <= rt.end_char: 
                if (tt.is_value(Utils.asObjectOrNull(mt.tag, str), None)): 
                    return mt
                tt = tt.next0_
            return None
        return mt
    
    def process_referent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        from pullenti.ner.org.internal.OrgItemEngItem import OrgItemEngItem
        if (begin is None): 
            return None
        if (begin.kit.recurse_level > 2): 
            return None
        begin.kit.recurse_level += 1
        rt = self.__try_attach_org(begin, None, OrganizationAnalyzer.AttachType.NORMAL, None, False, 0, -1)
        if (rt is None): 
            rt = OrgItemEngItem.try_attach_org(begin, False)
        if (rt is None): 
            rt = OrgItemEngItem.try_attach_org(begin, True)
        if (rt is None): 
            rt = OrgItemTypeToken.try_attach_reference_to_exist_org(begin)
        begin.kit.recurse_level -= 1
        if (rt is None): 
            return None
        rt.data = begin.kit.get_analyzer_data(self)
        return rt
    
    def __try_attach_orgs(self, t : 'Token', ad : 'OrgAnalyzerData', step : int) -> typing.List['ReferentToken']:
        from pullenti.ner.org.internal.OrgItemEngItem import OrgItemEngItem
        from pullenti.ner.org.internal.OrgItemNameToken import OrgItemNameToken
        if (t is None): 
            return None
        if (ad is not None and len(ad.local_ontology.items) > 1000): 
            ad = (None)
        if (t.chars.is_latin_letter and MiscHelper.is_eng_article(t)): 
            res11 = self.__try_attach_orgs(t.next0_, ad, step)
            if (res11 is not None and len(res11) > 0): 
                res11[0].begin_token = t
                return res11
        rt = None
        typ = None
        if (step == 0 or t.inner_bool): 
            typ = OrgItemTypeToken.try_attach(t, False, None)
            if (typ is not None): 
                t.inner_bool = True
            if (typ is None or typ.chars.is_latin_letter): 
                ltyp = OrgItemEngItem.try_attach(t, False)
                if (ltyp is not None): 
                    t.inner_bool = True
                elif (t.chars.is_latin_letter): 
                    rte = OrgItemEngItem.try_attach_org(t, False)
                    if (rte is not None): 
                        self.__do_post_analyze(rte, ad)
                        ree = list()
                        ree.append(rte)
                        return ree
        rt00 = self.__try_attach_spec(t, ad)
        if (rt00 is None): 
            rt00 = self.__try_attach_org_by_alias(t, ad)
        if (rt00 is not None): 
            res0 = list()
            self.__do_post_analyze(rt00, ad)
            res0.append(rt00)
            return res0
        if (typ is not None): 
            if (typ.root is None or not typ.root.is_pure_prefix): 
                if (((typ.morph.number) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                    t1 = typ.end_token
                    ok = True
                    ok1 = False
                    if (t1.next0_ is not None and t1.next0_.is_char(',')): 
                        t1 = t1.next0_
                        ok1 = True
                        if (t1.next0_ is not None and t1.next0_.is_value("КАК", None)): 
                            t1 = t1.next0_
                        else: 
                            ok = False
                    if (t1.next0_ is not None and t1.next0_.is_value("КАК", None)): 
                        t1 = t1.next0_
                        ok1 = True
                    if (t1.next0_ is not None and t1.next0_.is_char(':')): 
                        t1 = t1.next0_
                    if (t1 == t and t1.is_newline_after): 
                        ok = False
                    rt = (None)
                    if (ok): 
                        if (not ok1 and typ.coef > 0): 
                            ok1 = True
                        if (ok1): 
                            rt = self.__try_attach_org(t1.next0_, ad, OrganizationAnalyzer.AttachType.MULTIPLE, typ, False, 0, -1)
                    if (rt is not None): 
                        self.__do_post_analyze(rt, ad)
                        res = list()
                        res.append(rt)
                        org0_ = Utils.asObjectOrNull(rt.referent, OrganizationReferent)
                        if (ok1): 
                            rt.begin_token = t
                        t1 = rt.end_token.next0_
                        ok = True
                        while t1 is not None: 
                            if (t1.is_newline_before): 
                                ok = False
                                break
                            last = False
                            if (t1.is_char(',')): 
                                pass
                            elif (t1.is_and or t1.is_or): 
                                last = True
                            else: 
                                if (len(res) < 2): 
                                    ok = False
                                break
                            t1 = t1.next0_
                            typ1 = OrgItemTypeToken.try_attach(t1, True, ad)
                            if (typ1 is not None): 
                                ok = False
                                break
                            rt = self.__try_attach_org(t1, ad, OrganizationAnalyzer.AttachType.MULTIPLE, typ, False, 0, -1)
                            if (rt is not None and rt.begin_token == rt.end_token): 
                                if (not rt.begin_token.get_morph_class_in_dictionary().is_undefined and rt.begin_token.chars.is_all_upper): 
                                    rt = (None)
                            if (rt is None): 
                                if (len(res) < 2): 
                                    ok = False
                                break
                            self.__do_post_analyze(rt, ad)
                            res.append(rt)
                            if (len(res) > 100): 
                                ok = False
                                break
                            org0_ = (Utils.asObjectOrNull(rt.referent, OrganizationReferent))
                            org0_.add_type(typ, False)
                            if (last): 
                                break
                            t1 = rt.end_token
                            t1 = t1.next0_
                        if (ok and len(res) > 1): 
                            return res
        rt = (None)
        if (typ is not None and ((typ.is_dep or typ.can_be_dep_before_organization))): 
            rt = self.__try_attach_dep_before_org(typ, None)
            if (rt is None): 
                rt = self.__try_attach_dep_after_org(typ)
            if (rt is None): 
                rt = self.__try_attach_org(typ.end_token.next0_, ad, OrganizationAnalyzer.AttachType.NORMALAFTERDEP, None, False, 0, -1)
        tt = Utils.asObjectOrNull(t, TextToken)
        if (((step == 0 and rt is None and tt is not None) and not tt.chars.is_all_lower and tt.chars.is_cyrillic_letter) and tt.get_morph_class_in_dictionary().is_undefined): 
            s = tt.term
            if (((s.startswith("ГУ") or s.startswith("РУ"))) and len(s) > 3 and ((len(s) > 4 or s == "ГУВД"))): 
                tt.term = ("МВД" if s == "ГУВД" else tt.term[2:])
                inv = tt.invariant_prefix_length_of_morph_vars
                tt.invariant_prefix_length_of_morph_vars = (0)
                max0_ = tt.max_length_of_morph_vars
                tt.max_length_of_morph_vars = (len(tt.term))
                rt = self.__try_attach_org(tt, ad, OrganizationAnalyzer.AttachType.NORMALAFTERDEP, None, False, 0, -1)
                tt.term = s
                tt.invariant_prefix_length_of_morph_vars = inv
                tt.max_length_of_morph_vars = max0_
                if (rt is not None): 
                    if (ad is not None and ad.loc_orgs.try_attach(tt, None, False) is not None): 
                        rt = (None)
                    if (t.kit.ontology is not None and t.kit.ontology.attach_token(OrganizationReferent.OBJ_TYPENAME, tt) is not None): 
                        rt = (None)
                if (rt is not None): 
                    typ = OrgItemTypeToken(tt, tt)
                    typ.typ = ("главное управление" if s.startswith("ГУ") else "региональное управление")
                    rt0 = self.__try_attach_dep_before_org(typ, rt)
                    if (rt0 is not None): 
                        if (ad is not None): 
                            rt.referent = ad.register_referent(rt.referent)
                        rt.referent.add_occurence(TextAnnotation(t, rt.end_token, rt.referent))
                        rt0.referent.higher = Utils.asObjectOrNull(rt.referent, OrganizationReferent)
                        li2 = list()
                        self.__do_post_analyze(rt0, ad)
                        li2.append(rt0)
                        return li2
            elif ((((((((((s[0] == 'У' and len(s) > 3 and tt.get_morph_class_in_dictionary().is_undefined)) or s == "ОВД" or s == "РОВД") or s == "ОМВД" or s == "ОСБ") or s == "УПФ" or s == "УФНС") or s == "ИФНС" or s == "ИНФС") or s == "УВД" or s == "УФМС") or s == "УФСБ" or s == "ОУФМС") or s == "ОФМС" or s == "УФК") or s == "УФССП"): 
                if (s == "ОВД" or s == "УВД" or s == "РОВД"): 
                    tt.term = "МВД"
                elif (s == "ОСБ"): 
                    tt.term = "СБЕРБАНК"
                elif (s == "УПФ"): 
                    tt.term = "ПФР"
                elif (s == "УФНС" or s == "ИФНС" or s == "ИНФС"): 
                    tt.term = "ФНС"
                elif (s == "УФМС" or s == "ОУФМС" or s == "ОФМС"): 
                    tt.term = "ФМС"
                else: 
                    tt.term = tt.term[1:]
                inv = tt.invariant_prefix_length_of_morph_vars
                tt.invariant_prefix_length_of_morph_vars = (0)
                max0_ = tt.max_length_of_morph_vars
                tt.max_length_of_morph_vars = (len(tt.term))
                rt = self.__try_attach_org(tt, ad, OrganizationAnalyzer.AttachType.NORMALAFTERDEP, None, False, 0, -1)
                tt.term = s
                tt.invariant_prefix_length_of_morph_vars = inv
                tt.max_length_of_morph_vars = max0_
                if (rt is not None): 
                    org1 = Utils.asObjectOrNull(rt.referent, OrganizationReferent)
                    if (len(org1.geo_objects) == 0 and rt.end_token.next0_ is not None): 
                        g = Utils.asObjectOrNull(rt.end_token.next0_.get_referent(), GeoReferent)
                        if (g is not None and g.is_state): 
                            org1._add_geo_object(g)
                            rt.end_token = rt.end_token.next0_
                    typ = OrgItemTypeToken(tt, tt)
                    typ.typ = ("отделение" if s[0] == 'О' else (("инспекция" if s[0] == 'И' else "управление")))
                    gen = (MorphGender.FEMINIE if s[0] == 'И' else MorphGender.NEUTER)
                    if (s.startswith("ОУ")): 
                        typ.typ = "управление"
                    elif (s.startswith("РО")): 
                        typ.typ = "отдел"
                        typ.alt_typ = "районный отдел"
                        typ.name_is_name = True
                        gen = MorphGender.MASCULINE
                    rt0 = self.__try_attach_dep_before_org(typ, rt)
                    if (rt0 is not None): 
                        org0 = Utils.asObjectOrNull(rt0.referent, OrganizationReferent)
                        org0.add_profile(OrgProfile.UNIT)
                        if (org0.number is None and not tt.is_newline_after): 
                            num = OrgItemNumberToken.try_attach(tt.next0_, True, typ)
                            if (num is not None): 
                                org0.number = num.number
                                rt0.end_token = num.end_token
                        if (rt0.referent.find_slot(OrganizationReferent.ATTR_GEO, None, True) is None): 
                            geo_ = self.__is_geo(rt0.end_token.next0_, False)
                            if ((geo_) is not None): 
                                if (rt0.referent._add_geo_object(geo_)): 
                                    rt0.end_token = self.__get_geo_end_token(geo_, rt0.end_token.next0_)
                            elif (rt0.end_token.whitespaces_after_count < 3): 
                                nam = OrgItemNameToken.try_attach(rt0.end_token.next0_, None, False, True)
                                if (nam is not None and not nam.value.startswith("СУБЪЕКТ")): 
                                    geo_ = self.__is_geo(nam.end_token.next0_, False)
                                    if ((geo_) is not None): 
                                        if (rt0.referent._add_geo_object(geo_)): 
                                            rt0.end_token = self.__get_geo_end_token(geo_, nam.end_token.next0_)
                                        rt0.referent.add_name(nam.value, True, None)
                        if (len(rt0.referent.slots) > 3): 
                            if (tt.previous is not None and ((tt.previous.morph.class0_.is_adjective and not tt.previous.morph.class0_.is_verb)) and tt.whitespaces_before_count == 1): 
                                adj = MorphologyService.get_wordform(tt.previous.get_source_text().upper(), MorphBaseInfo._new2348(MorphClass.ADJECTIVE, gen, tt.previous.morph.language))
                                if (adj is not None and not adj.startswith("УПОЛНОМОЧ") and not adj.startswith("ОПЕРУПОЛНОМОЧ")): 
                                    tyy = "{0} {1}".format(adj.lower(), typ.typ)
                                    rt0.begin_token = tt.previous
                                    if (rt0.begin_token.previous is not None and rt0.begin_token.previous.is_hiphen and rt0.begin_token.previous.previous is not None): 
                                        tt0 = rt0.begin_token.previous.previous
                                        if (tt0.chars == rt0.begin_token.chars and (isinstance(tt0, TextToken))): 
                                            adj = tt0.term
                                            if (tt0.morph.class0_.is_adjective and not tt0.morph.contains_attr("неизм.", None)): 
                                                adj = MorphologyService.get_wordform(adj, MorphBaseInfo._new2348(MorphClass.ADJECTIVE, gen, tt0.morph.language))
                                            tyy = "{0} {1}".format(adj.lower(), tyy)
                                            rt0.begin_token = tt0
                                    if (typ.name_is_name): 
                                        org0.add_name(tyy.upper(), True, None)
                                    else: 
                                        org0.add_type_str(tyy)
                            for g in org1.geo_objects: 
                                if (not g.is_state): 
                                    sl = org1.find_slot(OrganizationReferent.ATTR_GEO, g, True)
                                    if (sl is not None): 
                                        org1.slots.remove(sl)
                                    if (rt.begin_token.begin_char < rt0.begin_token.begin_char): 
                                        rt0.begin_token = rt.begin_token
                                    org0._add_geo_object(g)
                                    org1.move_ext_referent(org0, g)
                            if (ad is not None): 
                                rt.referent = ad.register_referent(rt.referent)
                            rt.referent.add_occurence(TextAnnotation(t, rt.end_token, rt.referent))
                            rt0.referent.higher = Utils.asObjectOrNull(rt.referent, OrganizationReferent)
                            self.__do_post_analyze(rt0, ad)
                            li2 = list()
                            li2.append(rt0)
                            return li2
                    rt = (None)
        if (rt is None): 
            if (step > 0 and typ is None): 
                if (not BracketHelper.is_bracket(t, False)): 
                    if (not t.chars.is_letter): 
                        return None
                    if (t.chars.is_all_lower): 
                        return None
            rt = self.__try_attach_org(t, ad, OrganizationAnalyzer.AttachType.NORMAL, None, False, 0, step)
            if (rt is None and step == 0): 
                rt = OrgItemEngItem.try_attach_org(t, False)
            if (rt is not None): 
                pass
        if (((rt is None and step == 1 and typ is not None) and typ.is_dep and typ.root is not None) and not typ.root.can_be_normal_dep): 
            if (OrgItemTypeToken.check_org_special_word_before(typ.begin_token.previous)): 
                rt = self.__try_attach_dep(typ, OrganizationAnalyzer.AttachType.HIGH, True)
        if (rt is None and step == 0 and t is not None): 
            ok = False
            if (t.length_char > 2 and not t.chars.is_all_lower and t.chars.is_latin_letter): 
                ok = True
            elif (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                ok = True
            if (ok and t.whitespaces_before_count != 1): 
                ok = False
            if (ok and not OrgItemTypeToken.check_person_property(t.previous)): 
                ok = False
            if (ok): 
                org0_ = OrganizationReferent()
                rt = ReferentToken(org0_, t, t)
                if (t.chars.is_latin_letter and NumberHelper.try_parse_roman(t) is None): 
                    nam = OrgItemNameToken.try_attach(t, None, False, True)
                    if (nam is not None): 
                        name_ = io.StringIO()
                        print(nam.value, end="", file=name_)
                        rt.end_token = nam.end_token
                        ttt = nam.end_token.next0_
                        while ttt is not None: 
                            if (not ttt.chars.is_latin_letter): 
                                break
                            nam = OrgItemNameToken.try_attach(ttt, None, False, False)
                            if (nam is None): 
                                break
                            rt.end_token = nam.end_token
                            if (not nam.is_std_tail): 
                                print(" {0}".format(nam.value), end="", file=name_, flush=True)
                            else: 
                                ei = OrgItemEngItem.try_attach(nam.begin_token, False)
                                if (ei is not None): 
                                    org0_.add_type_str(ei.full_value)
                                    if (ei.short_value is not None): 
                                        org0_.add_type_str(ei.short_value)
                            ttt = ttt.next0_
                        org0_.add_name(Utils.toStringStringIO(name_), True, None)
                else: 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        rt11 = self.__try_attach_org(t.next0_, ad, OrganizationAnalyzer.AttachType.NORMAL, None, False, 0, -1)
                        if (rt11 is not None and ((rt11.end_token == br.end_token.previous or rt11.end_token == br.end_token))): 
                            rt11.begin_token = t
                            rt11.end_token = br.end_token
                            rt = rt11
                            org0_ = (Utils.asObjectOrNull(rt11.referent, OrganizationReferent))
                        else: 
                            org0_.add_name(MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE), True, None)
                            org0_.add_name(MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO), True, br.begin_token.next0_)
                            if (br.begin_token.next0_ == br.end_token.previous and br.begin_token.next0_.get_morph_class_in_dictionary().is_undefined): 
                                for wf in br.begin_token.next0_.morph.items: 
                                    if (wf.case_.is_genitive and (isinstance(wf, MorphWordForm))): 
                                        org0_.add_name(wf.normal_case, True, None)
                            rt.end_token = br.end_token
                if (len(org0_.slots) == 0): 
                    rt = (None)
        if (rt is None): 
            if (BracketHelper.can_be_start_of_sequence(t, False, False)): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is None or br.length_char > 100): 
                    br = (None)
                if (br is not None): 
                    t1 = br.end_token.next0_
                    if (t1 is not None and t1.is_comma): 
                        t1 = t1.next0_
                    if (t1 is not None and (t1.whitespaces_before_count < 3)): 
                        typ = OrgItemTypeToken.try_attach(t1, False, None)
                        if ((typ) is not None and typ.root is not None and typ.root.typ == OrgItemTypeTyp.PREFIX): 
                            t2 = typ.end_token.next0_
                            ok = False
                            if (t2 is None or t2.is_newline_before): 
                                ok = True
                            elif (t2.is_char_of(".,:;")): 
                                ok = True
                            elif (isinstance(t2, ReferentToken)): 
                                ok = True
                            if (ok): 
                                org0_ = OrganizationReferent()
                                rt = ReferentToken(org0_, t, typ.end_token)
                                org0_.add_type(typ, False)
                                nam = MiscHelper.get_text_value(br.begin_token.next0_, br.end_token.previous, GetTextAttr.NO)
                                org0_.add_name(nam, True, None)
                                rt11 = self.__try_attach_org(br.begin_token.next0_, ad, OrganizationAnalyzer.AttachType.NORMAL, None, False, 0, -1)
                                if (rt11 is not None and rt11.end_char <= typ.end_char): 
                                    org0_.merge_slots(rt11.referent, True)
            if (rt is None): 
                return None
        self.__do_post_analyze(rt, ad)
        if (step > 0): 
            mt = OrganizationAnalyzer._check_alias_after(rt, rt.end_token.next0_)
            if (mt is not None): 
                if (ad is not None): 
                    term = Termin()
                    term.init_by(mt.begin_token, mt.end_token.previous, rt.referent, False)
                    ad.aliases.add(term)
                rt.end_token = mt.end_token
        li = list()
        li.append(rt)
        tt1 = rt.end_token.next0_
        if (tt1 is not None and tt1.is_char('(')): 
            br = BracketHelper.try_parse(tt1, BracketParseAttr.NO, 100)
            if (br is not None): 
                tt1 = br.end_token.next0_
        if (tt1 is not None and tt1.is_comma_and): 
            if (BracketHelper.can_be_start_of_sequence(tt1.next0_, True, False)): 
                if (BracketHelper.can_be_end_of_sequence(rt.end_token, True, None, False)): 
                    ok = False
                    ttt = tt1
                    first_pass3818 = True
                    while True:
                        if first_pass3818: first_pass3818 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        if (ttt.is_char('.')): 
                            ok = True
                            break
                        if (ttt.is_char('(')): 
                            br1 = BracketHelper.try_parse(ttt, BracketParseAttr.NO, 100)
                            if (br1 is not None): 
                                ttt = br1.end_token
                                continue
                        if (not ttt.is_comma_and): 
                            break
                        if (not BracketHelper.can_be_start_of_sequence(ttt.next0_, True, False)): 
                            break
                        br = BracketHelper.try_parse(ttt.next0_, BracketParseAttr.NO, 100)
                        if (br is None): 
                            break
                        add_typ = False
                        rt1 = self.__try_attach_org_(ttt.next0_.next0_, ttt.next0_.next0_, ad, None, True, OrganizationAnalyzer.AttachType.NORMAL, None, False, 0)
                        if (rt1 is None or (rt1.end_char < (br.end_char - 1))): 
                            add_typ = True
                            rt1 = self.__try_attach_org_(ttt.next0_, ttt.next0_, ad, None, True, OrganizationAnalyzer.AttachType.HIGH, None, False, 0)
                        if (rt1 is None or (rt1.end_char < (br.end_char - 1))): 
                            break
                        li.append(rt1)
                        org1 = Utils.asObjectOrNull(rt1.referent, OrganizationReferent)
                        if (typ is not None): 
                            ok = True
                        if (len(org1.types) == 0): 
                            add_typ = True
                        if (add_typ): 
                            if (typ is not None): 
                                org1.add_type(typ, False)
                            s = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                            if (s is not None): 
                                ex = False
                                for n in org1.names: 
                                    if (s.startswith(n)): 
                                        ex = True
                                        break
                                if (not ex): 
                                    org1.add_name(s, True, br.begin_token.next0_)
                        if (ttt.is_and): 
                            ok = True
                            break
                        ttt = rt1.end_token
                    if (not ok and len(li) > 1): 
                        del li[1:1+len(li) - 1]
        return li
    
    def __try_attach_spec(self, t : 'Token', ad : 'OrgAnalyzerData') -> 'ReferentToken':
        rt = self.__try_attach_prop_names(t, ad)
        if (rt is None): 
            rt = self.__try_attach_politic_party(t, ad, False)
        if (rt is None): 
            rt = self.__try_attach_army(t, ad)
        return rt
    
    @staticmethod
    def __corr_brackets(rt : 'ReferentToken') -> bool:
        if (not BracketHelper.can_be_start_of_sequence(rt.begin_token.previous, True, False) or not BracketHelper.can_be_end_of_sequence(rt.end_token.next0_, True, None, False)): 
            return False
        rt.begin_token = rt.begin_token.previous
        rt.end_token = rt.end_token.next0_
        return True
    
    def __do_post_analyze(self, rt : 'ReferentToken', ad : 'OrgAnalyzerData') -> None:
        if (rt.morph.case_.is_undefined): 
            if (not rt.begin_token.chars.is_all_upper): 
                npt1 = NounPhraseHelper.try_parse(rt.begin_token, NounPhraseParseAttr.NO, 0, None)
                if (npt1 is None): 
                    npt1 = NounPhraseHelper.try_parse(rt.begin_token.next0_, NounPhraseParseAttr.NO, 0, None)
                if (npt1 is not None): 
                    rt.morph = npt1.morph
        o = Utils.asObjectOrNull(rt.referent, OrganizationReferent)
        if ((rt.kit.ontology is not None and o.ontology_items is None and o.higher is None) and o._m_temp_parent_org is None): 
            ot = rt.kit.ontology.attach_referent(o)
            if (ot is not None and len(ot) == 1 and (isinstance(ot[0].referent, OrganizationReferent))): 
                oo = Utils.asObjectOrNull(ot[0].referent, OrganizationReferent)
                o.merge_slots(oo, False)
                o.ontology_items = ot
                for sl in o.slots: 
                    if (isinstance(sl.value, Referent)): 
                        ext = False
                        for ss in oo.slots: 
                            if (ss.value == sl.value): 
                                ext = True
                                break
                        if (not ext): 
                            continue
                        rr = sl.value.clone()
                        rr.occurrence.clear()
                        o.upload_slot(sl, rr)
                        rt_ex = ReferentToken(rr, rt.begin_token, rt.end_token)
                        rt_ex.set_default_local_onto(rt.kit.processor)
                        o.add_ext_referent(rt_ex)
                        for sss in rr.slots: 
                            if (isinstance(sss.value, Referent)): 
                                rrr = sss.value.clone()
                                rrr.occurrence.clear()
                                rr.upload_slot(sss, rrr)
                                rt_ex2 = ReferentToken(rrr, rt.begin_token, rt.end_token)
                                rt_ex2.set_default_local_onto(rt.kit.processor)
                                sl.value.add_ext_referent(rt_ex2)
        if (o.higher is None and o._m_temp_parent_org is None): 
            if ((isinstance(rt.begin_token.previous, ReferentToken)) and (isinstance(rt.begin_token.previous.get_referent(), OrganizationReferent))): 
                oo = Utils.asObjectOrNull(rt.begin_token.previous.get_referent(), OrganizationReferent)
                if (OrgOwnershipHelper.can_be_higher(oo, o, False)): 
                    o._m_temp_parent_org = oo
            if (o._m_temp_parent_org is None and (isinstance(rt.end_token.next0_, ReferentToken)) and (isinstance(rt.end_token.next0_.get_referent(), OrganizationReferent))): 
                oo = Utils.asObjectOrNull(rt.end_token.next0_.get_referent(), OrganizationReferent)
                if (OrgOwnershipHelper.can_be_higher(oo, o, False)): 
                    o._m_temp_parent_org = oo
            if (o._m_temp_parent_org is None): 
                rt1 = self.__try_attach_org(rt.end_token.next0_, None, OrganizationAnalyzer.AttachType.NORMALAFTERDEP, None, False, 0, -1)
                if (rt1 is not None and rt.end_token.next0_ == rt1.begin_token): 
                    if (OrgOwnershipHelper.can_be_higher(Utils.asObjectOrNull(rt1.referent, OrganizationReferent), o, False)): 
                        o._m_temp_parent_org = (Utils.asObjectOrNull(rt1.referent, OrganizationReferent))
        if (rt.end_token.next0_ is None): 
            return
        OrganizationAnalyzer.__corr_brackets(rt)
        if (rt.begin_token.previous is not None and rt.begin_token.previous.morph.class0_.is_adjective and (rt.whitespaces_before_count < 2)): 
            if (len(rt.referent.geo_objects) == 0): 
                geo_ = self.__is_geo(rt.begin_token.previous, True)
                if (geo_ is not None): 
                    if (rt.referent._add_geo_object(geo_)): 
                        rt.begin_token = rt.begin_token.previous
        ttt = rt.end_token.next0_
        errs = 1
        br = False
        if (ttt is not None and ttt.is_char('(')): 
            br = True
            ttt = ttt.next0_
        refs = list()
        keyword_ = False
        has_inn = False
        has_ok = 0
        te = None
        first_pass3819 = True
        while True:
            if first_pass3819: first_pass3819 = False
            else: ttt = ttt.next0_
            if (not (ttt is not None)): break
            if (ttt.is_char_of(",;") or ttt.morph.class0_.is_preposition): 
                continue
            if (ttt.is_char(')')): 
                if (br): 
                    te = ttt
                break
            rr = ttt.get_referent()
            if (rr is not None): 
                if (rr.type_name == "ADDRESS" or rr.type_name == "DATE" or ((rr.type_name == "GEO" and br))): 
                    if (keyword_ or br or (ttt.whitespaces_before_count < 2)): 
                        refs.append(rr)
                        te = ttt
                        continue
                    break
                if (rr.type_name == "URI"): 
                    sch = rr.get_string_value("SCHEME")
                    if (sch is None): 
                        break
                    if (sch == "ИНН"): 
                        errs = 5
                        has_inn = True
                    elif (sch.startswith("ОК")): 
                        has_ok += 1
                    elif (sch != "КПП" and sch != "ОГРН" and not br): 
                        break
                    refs.append(rr)
                    te = ttt
                    if (ttt.next0_ is not None and ttt.next0_.is_char('(')): 
                        brrr = BracketHelper.try_parse(ttt.next0_, BracketParseAttr.NO, 100)
                        if (brrr is not None): 
                            ttt = brrr.end_token
                    continue
                elif (rr == rt.referent): 
                    continue
            if (ttt.is_newline_before and not br): 
                break
            if (isinstance(ttt, TextToken)): 
                npt = NounPhraseHelper.try_parse(ttt, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None): 
                    if ((npt.end_token.is_value("ДАТА", None) or npt.end_token.is_value("РЕГИСТРАЦИЯ", None) or npt.end_token.is_value("ЛИЦО", None)) or npt.end_token.is_value("ЮР", None) or npt.end_token.is_value("АДРЕС", None)): 
                        ttt = npt.end_token
                        keyword_ = True
                        continue
                if (ttt.is_value("REGISTRATION", None) and ttt.next0_ is not None and ttt.next0_.is_value("NUMBER", None)): 
                    tmp = io.StringIO()
                    tt3 = ttt.next0_.next0_
                    first_pass3820 = True
                    while True:
                        if first_pass3820: first_pass3820 = False
                        else: tt3 = tt3.next0_
                        if (not (tt3 is not None)): break
                        if (tt3.is_whitespace_before and tmp.tell() > 0): 
                            break
                        if (((tt3.is_char_of(":") or tt3.is_hiphen)) and tmp.tell() == 0): 
                            continue
                        if (isinstance(tt3, TextToken)): 
                            print(tt3.term, end="", file=tmp)
                        elif (isinstance(tt3, NumberToken)): 
                            print(tt3.get_source_text(), end="", file=tmp)
                        else: 
                            break
                        ttt = tt3
                        rt.end_token = ttt
                    if (tmp.tell() > 0): 
                        rt.referent.add_slot(OrganizationReferent.ATTR_MISC, Utils.toStringStringIO(tmp), False, 0)
                    continue
                if ((ttt.is_value("REGISTERED", None) and ttt.next0_ is not None and ttt.next0_.is_value("IN", None)) and (isinstance(ttt.next0_.next0_, ReferentToken)) and (isinstance(ttt.next0_.next0_.get_referent(), GeoReferent))): 
                    rt.referent.add_slot(OrganizationReferent.ATTR_MISC, ttt.next0_.next0_.get_referent(), False, 0)
                    ttt = ttt.next0_.next0_
                    rt.end_token = ttt
                    continue
                if (br): 
                    otyp = OrgItemTypeToken.try_attach(ttt, True, None)
                    if (otyp is not None and (ttt.whitespaces_before_count < 2) and otyp.geo is None): 
                        or1 = OrganizationReferent()
                        or1.add_type(otyp, False)
                        if (not OrgItemTypeToken.is_types_antagonisticoo(o, or1) and otyp.end_token.next0_ is not None and otyp.end_token.next0_.is_char(')')): 
                            o.add_type(otyp, False)
                            ttt = otyp.end_token
                            rt.end_token = ttt
                            if (br and ttt.next0_ is not None and ttt.next0_.is_char(')')): 
                                rt.end_token = ttt.next0_
                                break
                            continue
            keyword_ = False
            errs -= 1
            if (errs <= 0): 
                break
        if (te is not None and len(refs) > 0 and ((te.is_char(')') or has_inn or has_ok > 0))): 
            for rr in refs: 
                if (rr.type_name == OrganizationAnalyzer.GEONAME): 
                    rt.referent._add_geo_object(rr)
                else: 
                    rt.referent.add_slot(OrganizationReferent.ATTR_MISC, rr, False, 0)
            rt.end_token = te
        if ((rt.whitespaces_before_count < 2) and (isinstance(rt.begin_token.previous, TextToken)) and rt.begin_token.previous.chars.is_all_upper): 
            term = rt.begin_token.previous.term
            for s in o.slots: 
                if (isinstance(s.value, str)): 
                    a = MiscHelper.get_abbreviation(Utils.asObjectOrNull(s.value, str))
                    if (a is not None and a == term): 
                        rt.begin_token = rt.begin_token.previous
                        break
    
    def __try_attach_org_by_alias(self, t : 'Token', ad : 'OrgAnalyzerData') -> 'ReferentToken':
        if (t is None): 
            return None
        t0 = t
        br = False
        if (t0.next0_ is not None and BracketHelper.can_be_start_of_sequence(t0, True, False)): 
            t = t0.next0_
            br = True
        if ((isinstance(t, TextToken)) and t.chars.is_letter and not t.chars.is_all_lower): 
            if (t.length_char > 3): 
                pass
            elif (t.length_char > 1 and t.chars.is_all_upper): 
                pass
            else: 
                return None
        else: 
            return None
        if (ad is not None): 
            tok = ad.aliases.try_parse(t, TerminParseAttr.NO)
            if (tok is not None): 
                rt0 = ReferentToken(Utils.asObjectOrNull(tok.termin.tag, Referent), t0, tok.end_token)
                if (br): 
                    if (BracketHelper.can_be_end_of_sequence(tok.end_token.next0_, True, None, False)): 
                        rt0.end_token = tok.end_token.next0_
                    else: 
                        return None
                return rt0
        if (not br): 
            if (MiscHelper.can_be_start_of_sentence(t)): 
                return None
            if (not OrgItemTypeToken.check_org_special_word_before(t0.previous)): 
                return None
            if (t.chars.is_latin_letter): 
                if (t.next0_ is not None and t.next0_.chars.is_latin_letter): 
                    return None
            elif (t.next0_ is not None and ((t.next0_.chars.is_cyrillic_letter or not t.next0_.chars.is_all_lower))): 
                return None
        elif (not BracketHelper.can_be_end_of_sequence(t.next0_, True, None, False)): 
            return None
        cou = 0
        ttt = t.previous
        first_pass3821 = True
        while True:
            if first_pass3821: first_pass3821 = False
            else: ttt = ttt.previous; cou += 1
            if (not (ttt is not None and (cou < 100))): break
            org00 = Utils.asObjectOrNull(ttt.get_referent(), OrganizationReferent)
            if (org00 is None): 
                continue
            for n in org00.names: 
                str0_ = n
                ii = n.find(' ')
                if (ii > 0): 
                    str0_ = n[0:0+ii]
                if (t.is_value(str0_, None)): 
                    if (ad is not None): 
                        ad.aliases.add(Termin._new100(str0_, org00))
                    term = t.term
                    if (ii < 0): 
                        org00.add_name(term, True, t)
                    if (br): 
                        t = t.next0_
                    rt = ReferentToken(org00, t0, t)
                    return rt
        return None
    
    def __attach_middle_attributes(self, org0_ : 'OrganizationReferent', t : 'Token') -> 'Token':
        from pullenti.ner.org.internal.OrgItemEponymToken import OrgItemEponymToken
        te = None
        first_pass3822 = True
        while True:
            if first_pass3822: first_pass3822 = False
            else: t = t.next0_
            if (not (t is not None)): break
            ont = OrgItemNumberToken.try_attach(t, False, None)
            if (ont is not None): 
                org0_.number = ont.number
                t = ont.end_token
                te = t
                continue
            oet = OrgItemEponymToken.try_attach(t, False)
            if (oet is not None): 
                for v in oet.eponyms: 
                    org0_.add_eponym(v)
                t = oet.end_token
                te = t
                continue
            break
        return te
    
    GEONAME = "GEO"
    
    def __is_geo(self, t : 'Token', can_be_adjective : bool=False) -> object:
        if (t is None): 
            return None
        if (t.is_value("В", None) and t.next0_ is not None): 
            t = t.next0_
        r = t.get_referent()
        if (r is not None): 
            if (r.type_name == OrganizationAnalyzer.GEONAME): 
                if (t.whitespaces_before_count <= 15 or t.morph.case_.is_genitive): 
                    return r
            if (isinstance(r, AddressReferent)): 
                tt = t.begin_token
                if (tt.get_referent() is not None and tt.get_referent().type_name == OrganizationAnalyzer.GEONAME): 
                    if (t.whitespaces_before_count < 3): 
                        return tt.get_referent()
            return None
        if (t.whitespaces_before_count > 15 and not can_be_adjective): 
            return None
        rt = t.kit.process_referent("GEO", t)
        if (rt is None): 
            return None
        if (t.previous is not None and t.previous.is_value("ОРДЕН", None)): 
            return None
        if (not can_be_adjective): 
            if (rt.morph.class0_.is_adjective): 
                return None
        return rt
    
    def __get_geo_end_token(self, geo_ : object, t : 'Token') -> 'Token':
        if (isinstance(geo_, ReferentToken)): 
            if (isinstance(geo_.get_referent(), AddressReferent)): 
                return t.previous
            return geo_.end_token
        elif (t is not None and t.next0_ is not None and t.morph.class0_.is_preposition): 
            return t.next0_
        else: 
            return t
    
    def __attach_tail_attributes(self, org0_ : 'OrganizationReferent', t : 'Token', ad : 'OrgAnalyzerData', attach_for_new_org : bool, attach_typ : 'AttachType', is_global : bool=False) -> 'Token':
        from pullenti.ner.org.internal.OrgItemEngItem import OrgItemEngItem
        t1 = None
        ki = org0_.kind
        can_has_geo = True
        if (not can_has_geo): 
            if (org0_._types_contains("комитет") or org0_._types_contains("академия") or org0_._types_contains("инспекция")): 
                can_has_geo = True
        first_pass3823 = True
        while True:
            if first_pass3823: first_pass3823 = False
            else: t = (((None if t is None else t.next0_)))
            if (not (t is not None)): break
            if (((t.is_value("ПО", None) or t.is_value("В", None) or t.is_value("IN", None))) and t.next0_ is not None): 
                if (attach_typ == OrganizationAnalyzer.AttachType.NORMALAFTERDEP): 
                    break
                if (not can_has_geo): 
                    break
                r = self.__is_geo(t.next0_, False)
                if (r is None): 
                    break
                if (not org0_._add_geo_object(r)): 
                    break
                t1 = self.__get_geo_end_token(r, t.next0_)
                t = t1
                continue
            if (t.is_value("ИЗ", None) and t.next0_ is not None): 
                if (attach_typ == OrganizationAnalyzer.AttachType.NORMALAFTERDEP): 
                    break
                if (not can_has_geo): 
                    break
                r = self.__is_geo(t.next0_, False)
                if (r is None): 
                    break
                if (not org0_._add_geo_object(r)): 
                    break
                t1 = self.__get_geo_end_token(r, t.next0_)
                t = t1
                continue
            if (can_has_geo and org0_.find_slot(OrganizationReferent.ATTR_GEO, None, True) is None and not t.is_newline_before): 
                r = self.__is_geo(t, False)
                if (r is not None): 
                    if (not org0_._add_geo_object(r)): 
                        break
                    t1 = self.__get_geo_end_token(r, t)
                    t = t1
                    continue
                if (t.is_char('(')): 
                    r = self.__is_geo(t.next0_, False)
                    if ((isinstance(r, ReferentToken)) and r.end_token.next0_ is not None and r.end_token.next0_.is_char(')')): 
                        if (not org0_._add_geo_object(r)): 
                            break
                        t1 = r.end_token.next0_
                        t = t1
                        continue
                    if ((isinstance(r, GeoReferent)) and t.next0_.next0_ is not None and t.next0_.next0_.is_char(')')): 
                        if (not org0_._add_geo_object(r)): 
                            break
                        t1 = t.next0_.next0_
                        t = t1
                        continue
            if ((isinstance(t.get_referent(), GeoReferent)) and (t.whitespaces_before_count < 2)): 
                if (org0_.find_slot(OrganizationReferent.ATTR_GEO, t.get_referent(), True) is not None): 
                    t1 = t
                    continue
            if (((t.is_value("ПРИ", None) or t.is_value("В", None))) and t.next0_ is not None and (isinstance(t.next0_, ReferentToken))): 
                r = t.next0_.get_referent()
                if (isinstance(r, OrganizationReferent)): 
                    if (t.is_value("В", None) and not OrgOwnershipHelper.can_be_higher(Utils.asObjectOrNull(r, OrganizationReferent), org0_, False)): 
                        pass
                    else: 
                        org0_.higher = Utils.asObjectOrNull(r, OrganizationReferent)
                        t1 = t.next0_
                        t = t1
                        continue
            if (t.chars.is_latin_letter and (t.whitespaces_before_count < 2)): 
                has_latin_name = False
                for s in org0_.names: 
                    if (LanguageHelper.is_latin_char(s[0])): 
                        has_latin_name = True
                        break
                if (has_latin_name): 
                    eng = OrgItemEngItem.try_attach(t, False)
                    if (eng is not None): 
                        org0_.add_type_str(eng.full_value)
                        if (eng.short_value is not None): 
                            org0_.add_type_str(eng.short_value)
                        t1 = eng.end_token
                        t = t1
                        continue
            re = self.__is_geo(t, False)
            if (re is None and t.is_char(',')): 
                re = self.__is_geo(t.next0_, False)
            if (re is not None): 
                if (attach_typ != OrganizationAnalyzer.AttachType.NORMALAFTERDEP): 
                    if ((not can_has_geo and ki != OrganizationKind.BANK and ki != OrganizationKind.FEDERATION) and not "университет" in org0_.types): 
                        break
                    if ("Сбербанк" in str(org0_) and org0_.find_slot(OrganizationReferent.ATTR_GEO, None, True) is not None): 
                        break
                    if (not org0_._add_geo_object(re)): 
                        break
                    if (t.is_char(',')): 
                        t = t.next0_
                    t1 = self.__get_geo_end_token(re, t)
                    if (t1.end_char <= t.end_char): 
                        break
                    t = t1
                    continue
                else: 
                    break
            if (t.is_char('(')): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is None): 
                    break
                if (t.next0_ is not None and t.next0_.get_referent() is not None): 
                    if (t.next0_.next0_ != br.end_token): 
                        break
                    r = t.next0_.get_referent()
                    if (r.type_name == OrganizationAnalyzer.GEONAME): 
                        if (not org0_._add_geo_object(r)): 
                            break
                        t1 = br.end_token
                        t = t1
                        continue
                    if ((isinstance(r, OrganizationReferent)) and not is_global): 
                        if (not attach_for_new_org and not org0_.can_be_equals(r, ReferentsEqualType.WITHINONETEXT)): 
                            break
                        org0_.merge_slots(r, True)
                        t1 = br.end_token
                        t = t1
                        continue
                    break
                if (not is_global): 
                    if (attach_typ != OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
                        typ = OrgItemTypeToken.try_attach(t.next0_, True, None)
                        if (typ is not None and typ.end_token == br.end_token.previous and not typ.is_dep): 
                            org0_.add_type(typ, False)
                            if (typ.name is not None): 
                                org0_.add_type_str(typ.name.lower())
                            t1 = br.end_token
                            t = t1
                            continue
                    rte = OrgItemEngItem.try_attach_org(br.begin_token, False)
                    if (rte is not None): 
                        if (org0_.can_be_equals(rte.referent, ReferentsEqualType.FORMERGING)): 
                            org0_.merge_slots(rte.referent, True)
                            t1 = rte.end_token
                            t = t1
                            continue
                    nam = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                    if (nam is not None): 
                        eq = False
                        for s in org0_.slots: 
                            if (s.type_name == OrganizationReferent.ATTR_NAME): 
                                if (MiscHelper.can_be_equal_cyr_and_latss(nam, s.value)): 
                                    org0_.add_name(nam, True, br.begin_token.next0_)
                                    eq = True
                                    break
                        if (eq): 
                            t1 = br.end_token
                            t = t1
                            continue
                    old_name = False
                    tt0 = t.next0_
                    if (tt0 is not None): 
                        if (tt0.is_value("РАНЕЕ", None)): 
                            old_name = True
                            tt0 = tt0.next0_
                        elif (tt0.morph.class0_.is_adjective and tt0.next0_ is not None and ((tt0.next0_.is_value("НАЗВАНИЕ", None) or tt0.next0_.is_value("НАИМЕНОВАНИЕ", None)))): 
                            old_name = True
                            tt0 = tt0.next0_.next0_
                        if (old_name and tt0 is not None): 
                            if (tt0.is_hiphen or tt0.is_char_of(",:")): 
                                tt0 = tt0.next0_
                    rt = self.__try_attach_org(tt0, ad, OrganizationAnalyzer.AttachType.HIGH, None, False, 0, -1)
                    if (rt is None): 
                        break
                    if (not org0_.can_be_equals(rt.referent, ReferentsEqualType.FORMERGING)): 
                        break
                    if (rt.end_token != br.end_token.previous): 
                        break
                    if (not attach_for_new_org and not org0_.can_be_equals(rt.referent, ReferentsEqualType.WITHINONETEXT)): 
                        break
                    if (attach_typ == OrganizationAnalyzer.AttachType.NORMAL): 
                        if (not old_name and not OrganizationReferent.can_be_second_definition(org0_, Utils.asObjectOrNull(rt.referent, OrganizationReferent))): 
                            break
                        typ = OrgItemTypeToken.try_attach(t.next0_, True, None)
                        if (typ is not None and typ.is_douter_org): 
                            break
                    org0_.merge_slots(rt.referent, True)
                    t1 = br.end_token
                    t = t1
                    continue
                break
            elif (attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY and BracketHelper.can_be_start_of_sequence(t, True, False)): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is None): 
                    break
                nam = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                if (nam is not None): 
                    org0_.add_name(nam, True, br.begin_token.next0_)
                rt1 = self.__try_attach_org(t.next0_, ad, OrganizationAnalyzer.AttachType.HIGH, None, True, 0, -1)
                if (rt1 is not None and rt1.end_token.next0_ == br.end_token): 
                    org0_.merge_slots(rt1.referent, True)
                    t1 = br.end_token
                    t = t1
            else: 
                break
        if (t is not None and (t.whitespaces_before_count < 2) and ((ki == OrganizationKind.UNDEFINED or ki == OrganizationKind.BANK))): 
            ty1 = OrgItemTypeToken.try_attach(t, False, None)
            if (ty1 is not None and ty1.root is not None and ty1.root.is_pure_prefix): 
                if (t.kit.recurse_level > 2): 
                    return None
                t.kit.recurse_level += 1
                rt22 = self.__try_attach_org(t, ad, OrganizationAnalyzer.AttachType.NORMAL, None, False, 0, -1)
                t.kit.recurse_level -= 1
                if (rt22 is None): 
                    org0_.add_type(ty1, False)
                    t1 = ty1.end_token
        return t1
    
    def __correct_owner_before(self, res : 'ReferentToken') -> None:
        if (res is None): 
            return
        if (res.referent.kind == OrganizationKind.PRESS): 
            if (res.begin_token.is_value("КОРРЕСПОНДЕНТ", None) and res.begin_token != res.end_token): 
                res.begin_token = res.begin_token.next0_
        org0_ = Utils.asObjectOrNull(res.referent, OrganizationReferent)
        if (org0_.higher is not None or org0_._m_temp_parent_org is not None): 
            return
        hi_before = None
        cou_before = 0
        t0 = None
        t = res.begin_token.previous
        first_pass3824 = True
        while True:
            if first_pass3824: first_pass3824 = False
            else: t = t.previous
            if (not (t is not None)): break
            cou_before += t.whitespaces_after_count
            if (t.is_char(',')): 
                cou_before += 5
                continue
            elif (t.is_value("ПРИ", None)): 
                return
            if (isinstance(t, ReferentToken)): 
                hi_before = Utils.asObjectOrNull(t.get_referent(), OrganizationReferent)
                if ((hi_before) is not None): 
                    t0 = t
            break
        if (t0 is None): 
            return
        if (not OrgOwnershipHelper.can_be_higher(hi_before, org0_, False)): 
            return
        if (OrgOwnershipHelper.can_be_higher(org0_, hi_before, False)): 
            return
        hi_after = None
        cou_after = 0
        t = res.end_token.next0_
        first_pass3825 = True
        while True:
            if first_pass3825: first_pass3825 = False
            else: t = t.next0_
            if (not (t is not None)): break
            cou_before += t.whitespaces_before_count
            if (t.is_char(',') or t.is_value("ПРИ", None)): 
                cou_after += 5
                continue
            if (isinstance(t, ReferentToken)): 
                hi_after = (Utils.asObjectOrNull(t.get_referent(), OrganizationReferent))
                break
            rt = self.__try_attach_org(t, None, OrganizationAnalyzer.AttachType.NORMAL, None, False, 0, -1)
            if (rt is not None): 
                hi_after = (Utils.asObjectOrNull(rt.referent, OrganizationReferent))
            break
        if (hi_after is not None): 
            if (OrgOwnershipHelper.can_be_higher(hi_after, org0_, False)): 
                if (cou_before >= cou_after): 
                    return
        if (org0_.kind == hi_before.kind and org0_.kind != OrganizationKind.UNDEFINED): 
            if (org0_.kind != OrganizationKind.DEPARTMENT & org0_.kind != OrganizationKind.GOVENMENT): 
                return
        org0_.higher = hi_before
        res.begin_token = t0
    
    def __check_ownership(self, t : 'Token') -> 'ReferentToken':
        if (t is None): 
            return None
        res = None
        org0_ = Utils.asObjectOrNull(t.get_referent(), OrganizationReferent)
        if (org0_ is None): 
            return None
        tt0 = t
        while t is not None: 
            tt = t.next0_
            always = False
            br = False
            if (tt is not None and tt.morph.class0_.is_preposition): 
                if (tt.is_value("ПРИ", None)): 
                    always = True
                elif (tt.is_value("В", None)): 
                    pass
                else: 
                    break
                tt = tt.next0_
            if ((tt is not None and tt.is_char('(') and (isinstance(tt.next0_, ReferentToken))) and tt.next0_.next0_ is not None and tt.next0_.next0_.is_char(')')): 
                br = True
                tt = tt.next0_
            if (isinstance(tt, ReferentToken)): 
                org2 = Utils.asObjectOrNull(tt.get_referent(), OrganizationReferent)
                if (org2 is not None): 
                    ok = OrgOwnershipHelper.can_be_higher(org2, org0_, False)
                    if (always or ok): 
                        ok = True
                    elif (OrgOwnershipHelper.can_be_higher(org2, org0_, True)): 
                        t0 = t.previous
                        if (t0 is not None and t0.is_char(',')): 
                            t0 = t0.previous
                        rt = t.kit.process_referent("PERSON", t0)
                        if (rt is not None and rt.referent.type_name == "PERSONPROPERTY" and rt.morph.number == MorphNumber.SINGULAR): 
                            ok = True
                    if (ok and ((org0_.higher is None or org0_.higher.can_be_equals(org2, ReferentsEqualType.WITHINONETEXT)))): 
                        org0_.higher = org2
                        if (br): 
                            tt = tt.next0_
                        if (org0_.higher == org2): 
                            if (res is None): 
                                res = ReferentToken._new734(org0_, t, tt, tt0.morph)
                            else: 
                                res.end_token = tt
                            t = tt
                            if (len(org0_.geo_objects) == 0): 
                                ttt = t.next0_
                                if (ttt is not None and ttt.is_value("В", None)): 
                                    ttt = ttt.next0_
                                if (self.__is_geo(ttt, False) is not None): 
                                    org0_._add_geo_object(ttt)
                                    res.end_token = ttt
                                    t = ttt
                            org0_ = org2
                            continue
                    if (org0_.higher is not None and org0_.higher.higher is None and OrgOwnershipHelper.can_be_higher(org2, org0_.higher, False)): 
                        org0_.higher.higher = org2
                        res = ReferentToken(org0_, t, tt)
                        if (br): 
                            res.end_token = tt.next0_
                        return res
                    if ((org0_.higher is not None and org2.higher is None and OrgOwnershipHelper.can_be_higher(org0_.higher, org2, False)) and OrgOwnershipHelper.can_be_higher(org2, org0_, False)): 
                        org2.higher = org0_.higher
                        org0_.higher = org2
                        res = ReferentToken(org0_, t, tt)
                        if (br): 
                            res.end_token = tt.next0_
                        return res
            break
        if (res is not None): 
            return res
        if (org0_.kind == OrganizationKind.DEPARTMENT and org0_.higher is None and org0_._m_temp_parent_org is None): 
            cou = 0
            tt = tt0.previous
            first_pass3826 = True
            while True:
                if first_pass3826: first_pass3826 = False
                else: tt = tt.previous
                if (not (tt is not None)): break
                if (tt.is_newline_after): 
                    cou += 10
                cou += 1
                if (cou > 100): 
                    break
                org0 = Utils.asObjectOrNull(tt.get_referent(), OrganizationReferent)
                if (org0 is None): 
                    continue
                tmp = list()
                while org0 is not None: 
                    if (OrgOwnershipHelper.can_be_higher(org0, org0_, False)): 
                        org0_.higher = org0
                        break
                    if (org0.kind != OrganizationKind.DEPARTMENT): 
                        break
                    if (org0 in tmp): 
                        break
                    tmp.append(org0)
                    org0 = org0.higher
                break
        return None
    
    def process_ontology_item(self, begin : 'Token') -> 'ReferentToken':
        if (begin is None): 
            return None
        rt = self.__try_attach_org(begin, None, OrganizationAnalyzer.AttachType.EXTONTOLOGY, None, begin.previous is not None, 0, -1)
        if (rt is not None): 
            r = Utils.asObjectOrNull(rt.referent, OrganizationReferent)
            if (r.higher is None and rt.end_token.next0_ is not None): 
                h = Utils.asObjectOrNull(rt.end_token.next0_.get_referent(), OrganizationReferent)
                if (h is not None): 
                    if (OrgOwnershipHelper.can_be_higher(h, r, True) or not OrgOwnershipHelper.can_be_higher(r, h, True)): 
                        r.higher = h
                        rt.end_token = rt.end_token.next0_
            if (rt.begin_token != begin): 
                nam = MiscHelper.get_text_value(begin, rt.begin_token.previous, GetTextAttr.NO)
                if (not Utils.isNullOrEmpty(nam)): 
                    org0 = OrganizationReferent()
                    org0.add_name(nam, True, begin)
                    org0.higher = r
                    rt = ReferentToken(org0, begin, rt.end_token)
            return rt
        t = begin
        et = begin
        while t is not None: 
            if (t.is_char_of(",;")): 
                break
            et = t
            t = t.next0_
        name_ = MiscHelper.get_text_value(begin, et, GetTextAttr.NO)
        if (Utils.isNullOrEmpty(name_)): 
            return None
        org0_ = OrganizationReferent()
        org0_.add_name(name_, True, begin)
        return ReferentToken(org0_, begin, et)
    
    M_INITED = False
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.org.internal.OrgItemEngItem import OrgItemEngItem
        from pullenti.ner.org.internal.OrgItemNameToken import OrgItemNameToken
        if (OrganizationAnalyzer.M_INITED): 
            return
        OrganizationAnalyzer.M_INITED = True
        MetaOrganization.initialize()
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            OrganizationAnalyzer.__init_sport()
            OrganizationAnalyzer.__init_politic()
            OrgItemTypeToken.initialize()
            OrgItemEngItem.initialize()
            OrgItemNameToken.initialize()
            OrgGlobal.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.register_analyzer(OrganizationAnalyzer())
    
    def __try_attach_politic_party(self, t : 'Token', ad : 'OrgAnalyzerData', only_abbrs : bool=False) -> 'ReferentToken':
        if (not (isinstance(t, TextToken))): 
            return None
        name_tok = None
        root = None
        prev_toks = None
        prev_words = 0
        geo_ = None
        t0 = t
        t1 = t
        coef = 0
        words_after = 0
        is_fraction = False
        is_politic = False
        first_pass3827 = True
        while True:
            if first_pass3827: first_pass3827 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t != t0 and t.is_newline_before): 
                break
            if (only_abbrs): 
                break
            if (t.is_hiphen): 
                if (prev_toks is None): 
                    return None
                continue
            tokn = OrganizationAnalyzer.M_POLITIC_NAMES.try_parse(t, TerminParseAttr.NO)
            if (tokn is not None): 
                if (not t.chars.is_all_lower): 
                    break
                t1 = tokn.end_token
            tok = OrganizationAnalyzer.M_POLITIC_PREFS.try_parse(t, TerminParseAttr.NO)
            if (tok is None): 
                if (t.morph.class0_.is_adjective): 
                    rt = t.kit.process_referent("GEO", t)
                    if (rt is not None): 
                        geo_ = rt
                        t = rt.end_token
                        t1 = t
                        coef += 0.5
                        continue
                if (t.end_char < t1.end_char): 
                    continue
                break
            if (tok.termin.tag is not None and tok.termin.tag2 is not None): 
                if (t.end_char < t1.end_char): 
                    continue
                break
            if (tok.termin.tag is None and tok.termin.tag2 is None): 
                is_politic = True
            if (prev_toks is None): 
                prev_toks = list()
            prev_toks.append(tok)
            if (tok.termin.tag is None): 
                coef += (1)
                prev_words += 1
            elif (tok.morph.class0_.is_adjective): 
                coef += 0.5
            t = tok.end_token
            if (t.end_char > t1.end_char): 
                t1 = t
        if (t is None): 
            return None
        if (t.is_value("ПАРТИЯ", None) or t.is_value("ФРОНТ", None) or t.is_value("ГРУППИРОВКА", None)): 
            if (not t.is_value("ПАРТИЯ", None)): 
                is_politic = True
            root = t
            coef += 0.5
            if (t.chars.is_capital_upper and not MiscHelper.can_be_start_of_sentence(t)): 
                coef += 0.5
            t1 = t
            t = t.next0_
        elif (t.is_value("ФРАКЦИЯ", None)): 
            t1 = t
            root = t1
            is_fraction = True
            if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), OrganizationReferent))): 
                coef += (2)
            else: 
                return None
        br = None
        name_tok = OrganizationAnalyzer.M_POLITIC_NAMES.try_parse(t, TerminParseAttr.NO)
        if ((name_tok) is not None and not t.chars.is_all_lower): 
            coef += 0.5
            is_politic = True
            if (not t.chars.is_all_lower): 
                coef += 0.5
            if (name_tok.length_char > 10): 
                coef += 0.5
            elif (t.chars.is_all_upper): 
                coef += 0.5
            t1 = name_tok.end_token
            t = t1.next0_
        else: 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 10)
            if ((br) is not None): 
                if (not BracketHelper.can_be_start_of_sequence(t, True, False)): 
                    return None
                name_tok = OrganizationAnalyzer.M_POLITIC_NAMES.try_parse(t.next0_, TerminParseAttr.NO)
                if ((name_tok) is not None): 
                    coef += 1.5
                elif (only_abbrs): 
                    return None
                elif (t.next0_ is not None and t.next0_.is_value("О", None)): 
                    return None
                else: 
                    tt = t.next0_
                    while tt is not None and tt.end_char <= br.end_char: 
                        tok2 = OrganizationAnalyzer.M_POLITIC_PREFS.try_parse(tt, TerminParseAttr.NO)
                        if (tok2 is not None and tok2.termin.tag is None): 
                            if (tok2.termin.tag2 is None): 
                                is_politic = True
                            coef += 0.5
                            words_after += 1
                        elif (OrganizationAnalyzer.M_POLITIC_SUFFS.try_parse(tt, TerminParseAttr.NO) is not None): 
                            coef += 0.5
                            words_after += 1
                        elif (isinstance(tt.get_referent(), GeoReferent)): 
                            coef += 0.5
                        elif (isinstance(tt, ReferentToken)): 
                            coef = (0)
                            break
                        else: 
                            mc = tt.get_morph_class_in_dictionary()
                            if ((mc == MorphClass.VERB or mc == MorphClass.ADVERB or mc.is_pronoun) or mc.is_personal_pronoun): 
                                coef = (0)
                                break
                            if (mc.is_noun or mc.is_undefined): 
                                coef -= 0.5
                        tt = tt.next0_
                t1 = br.end_token
                t = t1.next0_
            elif (only_abbrs): 
                return None
            elif (root is not None): 
                tt = t
                first_pass3828 = True
                while True:
                    if first_pass3828: first_pass3828 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (isinstance(tt.get_referent(), GeoReferent)): 
                        break
                    if (tt.whitespaces_before_count > 2): 
                        break
                    if (tt.morph.class0_.is_preposition): 
                        if (tt != root.next0_): 
                            break
                        continue
                    if (tt.is_and): 
                        npt2 = NounPhraseHelper.try_parse(tt.next0_, NounPhraseParseAttr.REFERENTCANBENOUN, 0, None)
                        if (npt2 is not None and OrganizationAnalyzer.M_POLITIC_SUFFS.try_parse(npt2.end_token, TerminParseAttr.NO) is not None and npt2.end_token.chars == tt.previous.chars): 
                            continue
                        break
                    npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.REFERENTCANBENOUN, 0, None)
                    if (npt is None): 
                        break
                    if (npt.noun.is_value("ПАРТИЯ", None) or npt.noun.is_value("ФРОНТ", None)): 
                        break
                    co = 0
                    ttt = tt
                    while ttt is not None and ttt.end_char <= npt.end_char: 
                        tok2 = OrganizationAnalyzer.M_POLITIC_PREFS.try_parse(ttt, TerminParseAttr.NO)
                        if (tok2 is not None and tok2.termin.tag is None): 
                            if (tok2.termin.tag2 is None): 
                                is_politic = True
                            co += 0.5
                            words_after += 1
                        elif (OrganizationAnalyzer.M_POLITIC_SUFFS.try_parse(ttt, TerminParseAttr.NO) is not None): 
                            co += 0.5
                            words_after += 1
                        elif (isinstance(ttt.get_referent(), GeoReferent)): 
                            co += 0.5
                        ttt = ttt.next0_
                    if (co == 0): 
                        if (not npt.morph.case_.is_genitive): 
                            break
                        last_suf = OrganizationAnalyzer.M_POLITIC_SUFFS.try_parse(tt.previous, TerminParseAttr.NO)
                        if (((words_after > 0 and npt.end_token.chars == tt.previous.chars)) or ((last_suf is not None and last_suf.termin.tag is not None)) or ((tt.previous == root and npt.end_token.chars.is_all_lower and npt.morph.number == MorphNumber.PLURAL) and root.chars.is_capital_upper)): 
                            pp = tt.kit.process_referent("PERSON", tt)
                            if (pp is not None): 
                                break
                            words_after += 1
                        else: 
                            break
                    tt = npt.end_token
                    t1 = tt
                    t = t1.next0_
                    coef += co
        if (t is not None and (isinstance(t.get_referent(), GeoReferent)) and (t.whitespaces_before_count < 3)): 
            t1 = t
            coef += 0.5
        tt = t0.previous
        first_pass3829 = True
        while True:
            if first_pass3829: first_pass3829 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            if (not (isinstance(tt, TextToken))): 
                org1 = Utils.asObjectOrNull(tt.get_referent(), OrganizationReferent)
                if (org1 is not None and org1.contains_profile(OrgProfile.POLICY)): 
                    coef += 0.5
                continue
            if (not tt.chars.is_letter): 
                continue
            if (tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction): 
                continue
            if (OrganizationAnalyzer.M_POLITIC_PREFS.try_parse(tt, TerminParseAttr.NO) is not None): 
                coef += 0.5
                if (tt.is_value("ФРАКЦИЯ", None)): 
                    coef += 0.5
            else: 
                break
        if (coef < 1): 
            return None
        if (root is None): 
            if (name_tok is None and br is None): 
                return None
        elif ((name_tok is None and words_after == 0 and br is None) and not is_fraction): 
            if ((coef < 2) or prev_words == 0): 
                return None
        org0_ = OrganizationReferent()
        if (br is not None and name_tok is not None and (name_tok.end_char < br.end_token.previous.end_char)): 
            name_tok = (None)
        if (name_tok is not None): 
            is_politic = True
        if (is_fraction): 
            org0_.add_profile(OrgProfile.POLICY)
            org0_.add_profile(OrgProfile.UNIT)
        elif (is_politic): 
            org0_.add_profile(OrgProfile.POLICY)
            org0_.add_profile(OrgProfile.UNION)
        else: 
            org0_.add_profile(OrgProfile.UNION)
        if (name_tok is not None): 
            is_politic = True
            org0_.add_name(name_tok.termin.canonic_text, True, None)
            if (name_tok.termin.additional_vars is not None): 
                for v in name_tok.termin.additional_vars: 
                    org0_.add_name(v.canonic_text, True, None)
            if (name_tok.termin.acronym is not None): 
                geo1 = Utils.asObjectOrNull(name_tok.termin.tag, GeoReferent)
                if (geo1 is None): 
                    org0_.add_name(name_tok.termin.acronym, True, None)
                elif (geo_ is not None): 
                    if (geo1.can_be_equals(geo_.referent, ReferentsEqualType.WITHINONETEXT)): 
                        org0_.add_name(name_tok.termin.acronym, True, None)
                elif (isinstance(t1.get_referent(), GeoReferent)): 
                    if (geo1.can_be_equals(t1.get_referent(), ReferentsEqualType.WITHINONETEXT)): 
                        org0_.add_name(name_tok.termin.acronym, True, None)
                elif (name_tok.begin_token == name_tok.end_token and name_tok.begin_token.is_value(name_tok.termin.acronym, None)): 
                    org0_.add_name(name_tok.termin.acronym, True, None)
                    rtg = ReferentToken(geo1.clone(), name_tok.begin_token, name_tok.end_token)
                    rtg.set_default_local_onto(t0.kit.processor)
                    org0_._add_geo_object(rtg)
        elif (br is not None): 
            nam = MiscHelper.get_text_value(br.begin_token, br.end_token, GetTextAttr.NO)
            org0_.add_name(nam, True, None)
            if (root is None): 
                nam2 = MiscHelper.get_text_value(br.begin_token, br.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                if (nam2 != nam): 
                    org0_.add_name(nam, True, None)
        if (root is not None): 
            typ1 = root
            if (geo_ is not None): 
                typ1 = geo_.begin_token
            if (prev_toks is not None): 
                for p in prev_toks: 
                    if (p.termin.tag is None): 
                        if (p.begin_char < typ1.begin_char): 
                            typ1 = p.begin_token
                        break
            typ = MiscHelper.get_text_value(typ1, root, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
            if (typ is not None): 
                if (br is None): 
                    nam = None
                    t2 = t1
                    if (isinstance(t2.get_referent(), GeoReferent)): 
                        t2 = t2.previous
                    if (t2.end_char > root.end_char): 
                        nam = "{0} {1}".format(typ, MiscHelper.get_text_value(root.next0_, t2, GetTextAttr.NO))
                        org0_.add_name(nam, True, None)
                if (len(org0_.names) == 0 and typ1 != root): 
                    org0_.add_name(typ, True, None)
                else: 
                    org0_.add_type_str(typ.lower())
            if (is_fraction and (isinstance(t1.next0_, ReferentToken))): 
                org0_.add_type_str("фракция")
                t1 = t1.next0_
                org0_.higher = Utils.asObjectOrNull(t1.get_referent(), OrganizationReferent)
                if (t1.next0_ is not None and t1.next0_.is_value("В", None) and (isinstance(t1.next0_.next0_, ReferentToken))): 
                    oo = Utils.asObjectOrNull(t1.next0_.next0_.get_referent(), OrganizationReferent)
                    if (oo is not None and oo.kind == OrganizationKind.GOVENMENT): 
                        t1 = t1.next0_.next0_
                        org0_.add_slot(OrganizationReferent.ATTR_MISC, oo, False, 0)
                    elif (isinstance(t1.next0_.next0_.get_referent(), GeoReferent)): 
                        t1 = t1.next0_.next0_
                        org0_.add_slot(OrganizationReferent.ATTR_MISC, t1.get_referent(), False, 0)
        if (geo_ is not None): 
            org0_._add_geo_object(geo_)
        elif (isinstance(t1.get_referent(), GeoReferent)): 
            org0_._add_geo_object(t1.get_referent())
        return ReferentToken(org0_, t0, t1)
    
    @staticmethod
    def __init_politic() -> None:
        OrganizationAnalyzer.M_POLITIC_PREFS = TerminCollection()
        for s in ["либеральный", "либерал", "лейбористский", "демократический", "коммунистрический", "большевистский", "социальный", "социал", "национал", "националистическая", "свободный", "радикальный", "леворадикальный", "радикал", "революционная", "левый", "правый", "социалистический", "рабочий", "трудовой", "республиканский", "народный", "аграрный", "монархический", "анархический", "прогрессивый", "прогрессистский", "консервативный", "гражданский", "фашистский", "марксистский", "ленинский", "маоистский", "имперский", "славянский", "анархический", "баскский", "конституционный", "пиратский", "патриотический", "русский"]: 
            OrganizationAnalyzer.M_POLITIC_PREFS.add(Termin(s.upper()))
        for s in ["объединенный", "всероссийский", "общероссийский", "христианский", "независимый", "альтернативный"]: 
            OrganizationAnalyzer.M_POLITIC_PREFS.add(Termin._new2352(s.upper(), s))
        for s in ["политический", "правящий", "оппозиционный", "запрешенный", "террористический", "запрещенный", "экстремистский"]: 
            OrganizationAnalyzer.M_POLITIC_PREFS.add(Termin._new100(s.upper(), s))
        for s in ["активист", "член", "руководство", "лидер", "глава", "демонстрация", "фракция", "съезд", "пленум", "террорист", "парламент", "депутат", "парламентарий", "оппозиция", "дума", "рада"]: 
            OrganizationAnalyzer.M_POLITIC_PREFS.add(Termin._new102(s.upper(), s, s))
        OrganizationAnalyzer.M_POLITIC_SUFFS = TerminCollection()
        for s in ["коммунист", "социалист", "либерал", "республиканец", "националист", "радикал", "лейборист", "анархист", "патриот", "консерватор", "левый", "правый", "новый", "зеленые", "демократ", "фашист", "защитник", "труд", "равенство", "прогресс", "жизнь", "мир", "родина", "отечество", "отчизна", "республика", "революция", "революционер", "народовластие", "фронт", "сила", "платформа", "воля", "справедливость", "преображение", "преобразование", "солидарность", "управление", "демократия", "народ", "гражданин", "предприниматель", "предпринимательство", "бизнес", "пенсионер", "христианин"]: 
            OrganizationAnalyzer.M_POLITIC_SUFFS.add(Termin(s.upper()))
        for s in ["реформа", "свобода", "единство", "развитие", "освобождение", "любитель", "поддержка", "возрождение", "независимость"]: 
            OrganizationAnalyzer.M_POLITIC_SUFFS.add(Termin._new100(s.upper(), s))
        OrganizationAnalyzer.M_POLITIC_NAMES = TerminCollection()
        for s in ["Республиканская партия", "Демократическая партия;Демпартия", "Христианско демократический союз;ХДС", "Свободная демократическая партия;СвДП", "ЯБЛОКО", "ПАРНАС", "ПАМЯТЬ", "Движение против нелегальной иммиграции;ДПНИ", "НАЦИОНАЛ БОЛЬШЕВИСТСКАЯ ПАРТИЯ;НБП", "НАЦИОНАЛЬНЫЙ ФРОНТ;НАЦФРОНТ", "Национальный патриотический фронт;НПФ", "Батькивщина;Батькiвщина", "НАРОДНАЯ САМООБОРОНА", "Гражданская платформа", "Народная воля", "Славянский союз", "ПРАВЫЙ СЕКТОР", "ПЕГИДА;PEGIDA", "Венгерский гражданский союз;ФИДЕС", "БЛОК ЮЛИИ ТИМОШЕНКО;БЮТ", "Аль Каида;Аль Каеда;Аль Кайда;Al Qaeda;Al Qaida", "Талибан;движение талибан", "Бригады мученников Аль Аксы", "Хезболла;Хезбалла;Хизбалла", "Народный фронт освобождения палестины;НФОП", "Организация освобождения палестины;ООП", "Союз исламского джихада;Исламский джихад", "Аль-Джихад;Египетский исламский джихад", "Братья-мусульмане;Аль Ихван альМуслимун", "ХАМАС", "Движение за освобождение Палестины;ФАТХ", "Фронт Аль Нусра;Аль Нусра", "Джабхат ан Нусра"]: 
            pp = Utils.splitString(s.upper(), ';', False)
            t = Termin._new100(pp[0], OrgProfile.POLICY)
            i = 0
            while i < len(pp): 
                if ((len(pp[i]) < 5) and t.acronym is None): 
                    t.acronym = pp[i]
                    if (t.acronym.endswith("Р") or t.acronym.endswith("РФ")): 
                        t.tag = (MiscLocationHelper.get_geo_referent_by_name("RU"))
                    elif (t.acronym.endswith("У")): 
                        t.tag = (MiscLocationHelper.get_geo_referent_by_name("UA"))
                    elif (t.acronym.endswith("СС")): 
                        t.tag = (MiscLocationHelper.get_geo_referent_by_name("СССР"))
                else: 
                    t.add_variant(pp[i], False)
                i += 1
            OrganizationAnalyzer.M_POLITIC_NAMES.add(t)
    
    M_POLITIC_PREFS = None
    
    M_POLITIC_SUFFS = None
    
    M_POLITIC_NAMES = None
    
    MAX_ORG_NAME = 200
    
    def __try_attach_org(self, t : 'Token', ad : 'OrgAnalyzerData', attach_typ : 'AttachType', mult_typ : 'OrgItemTypeToken'=None, is_additional_attach : bool=False, level : int=0, step : int=-1) -> 'ReferentToken':
        if (level > 2 or t is None): 
            return None
        if (t.chars.is_latin_letter and MiscHelper.is_eng_article(t)): 
            re = self.__try_attach_org(t.next0_, ad, attach_typ, mult_typ, is_additional_attach, level, step)
            if (re is not None): 
                re.begin_token = t
                return re
        org0_ = None
        types = None
        if (mult_typ is not None): 
            types = list()
            types.append(mult_typ)
        t0 = t
        t1 = t
        ot_ex_li = None
        typ = None
        hiph = False
        spec_word_before = False
        in_brackets = False
        rt0 = None
        first_pass3830 = True
        while True:
            if first_pass3830: first_pass3830 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (isinstance(t.get_referent(), OrganizationReferent)): 
                break
            rt0 = self.__attach_global_org(t, attach_typ, ad, None)
            if ((rt0 is None and typ is not None and typ.geo is not None) and typ.begin_token.next0_ == typ.end_token): 
                rt0 = self.__attach_global_org(typ.end_token, attach_typ, ad, typ.geo)
                if (rt0 is not None): 
                    rt0.begin_token = typ.begin_token
            if (rt0 is not None): 
                if (attach_typ == OrganizationAnalyzer.AttachType.MULTIPLE): 
                    if (types is None or len(types) == 0): 
                        return None
                    if (not OrgItemTypeToken.is_type_accords(Utils.asObjectOrNull(rt0.referent, OrganizationReferent), types[0])): 
                        return None
                    rt0.referent.add_type(types[0], False)
                    if ((rt0.begin_token.begin_char - types[0].end_token.next0_.end_char) < 3): 
                        rt0.begin_token = types[0].begin_token
                    break
                if (typ is not None and not typ.end_token.morph.class0_.is_verb): 
                    if (OrganizationAnalyzer.__is_mvd_org(Utils.asObjectOrNull(rt0.referent, OrganizationReferent)) is not None and typ.typ is not None and "служба" in typ.typ): 
                        rt0 = (None)
                        break
                    if (OrgItemTypeToken.is_type_accords(Utils.asObjectOrNull(rt0.referent, OrganizationReferent), typ)): 
                        rt0.begin_token = typ.begin_token
                        rt0.referent.add_type(typ, False)
                break
            if (t.is_hiphen): 
                if (t == t0 or types is None): 
                    if (ot_ex_li is not None): 
                        break
                    return None
                if ((typ is not None and typ.root is not None and typ.root.can_has_number) and (isinstance(t.next0_, NumberToken))): 
                    pass
                else: 
                    hiph = True
                continue
            if (ad is not None and ot_ex_li is None): 
                ok1 = False
                tt = t
                if (t.inner_bool): 
                    ok1 = True
                elif (t.chars.is_all_lower): 
                    pass
                elif (t.chars.is_letter): 
                    ok1 = True
                elif (t.previous is not None and BracketHelper.is_bracket(t.previous, False)): 
                    ok1 = True
                elif (BracketHelper.can_be_start_of_sequence(t, True, False) and t.next0_ is not None): 
                    ok1 = True
                    tt = t.next0_
                if (ok1 and tt is not None): 
                    ot_ex_li = ad.loc_orgs.try_attach(tt, None, False)
                    if (ot_ex_li is None and t.kit.ontology is not None): 
                        ot_ex_li = t.kit.ontology.attach_token(OrganizationReferent.OBJ_TYPENAME, tt)
                        if ((ot_ex_li) is not None): 
                            pass
                    if (ot_ex_li is None and tt.length_char == 2 and tt.chars.is_all_upper): 
                        ot_ex_li = ad.local_ontology.try_attach(tt, None, False)
                        if (ot_ex_li is not None): 
                            if (len(tt.kit.sofa.text) > 300): 
                                ot_ex_li = (None)
                if (ot_ex_li is not None): 
                    t.inner_bool = True
            if ((step >= 0 and not t.inner_bool and t == t0) and (isinstance(t, TextToken))): 
                typ = (None)
            else: 
                typ = OrgItemTypeToken.try_attach(t, attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY, ad)
                if (typ is None and BracketHelper.can_be_start_of_sequence(t, False, False)): 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        typ = OrgItemTypeToken.try_attach(t.next0_, attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY, ad)
                        if (typ is not None and typ.end_token == br.end_token.previous and ((BracketHelper.can_be_start_of_sequence(br.end_token.next0_, True, False) or t.is_char('(')))): 
                            typ.end_token = br.end_token
                            typ.begin_token = t
                        else: 
                            typ = (None)
            if (typ is None): 
                break
            if (types is None): 
                if ((((typ.typ == "главное управление" or typ.typ == "главное территориальное управление" or typ.typ == "головне управління") or typ.typ == "головне територіальне управління" or typ.typ == "пограничное управление")) and ot_ex_li is not None): 
                    break
                types = list()
                t0 = typ.begin_token
                if (typ.is_not_typ and typ.end_token.next0_ is not None): 
                    t0 = typ.end_token.next0_
                if (OrgItemTypeToken.check_org_special_word_before(typ.begin_token.previous)): 
                    spec_word_before = True
            else: 
                ok = True
                for ty in types: 
                    if (OrgItemTypeToken.is_types_antagonistictt(ty, typ)): 
                        ok = False
                        break
                if (not ok): 
                    break
                if (typ.is_dep): 
                    break
                if (in_brackets): 
                    break
                typ0 = OrganizationAnalyzer.__last_typ(types)
                if (hiph and ((t.whitespaces_before_count > 0 and ((typ0 is not None and typ0.is_doubt_root_word))))): 
                    break
                if (typ.end_token == typ.begin_token): 
                    if (typ.is_value("ОРГАНИЗАЦИЯ", "ОРГАНІЗАЦІЯ") or typ.is_value("УПРАВЛІННЯ", "")): 
                        break
                if (typ0.typ == "банк" and typ.root is not None and typ.root.typ == OrgItemTypeTyp.PREFIX): 
                    rt = self.__try_attach_org(typ.begin_token, ad, attach_typ, None, False, 0, -1)
                    if (rt is not None and "Сбербанк" in str(rt.referent)): 
                        return None
                if (typ0.is_dep or typ0.typ == "департамент"): 
                    break
                if ((typ0.root is not None and typ0.root.is_pure_prefix and typ.root is not None) and not typ.root.is_pure_prefix and not typ.begin_token.chars.is_all_lower): 
                    if ("НИИ" in typ0.typ): 
                        break
                pref0 = typ0.root is not None and typ0.root.is_pure_prefix
                pref = typ.root is not None and typ.root.is_pure_prefix
                if (not pref0 and not pref): 
                    if (typ0.name is not None and len(typ0.name) != len(typ0.typ)): 
                        if (t.whitespaces_before_count > 1): 
                            break
                    if (not typ0.morph.case_.is_undefined and not typ.morph.case_.is_undefined): 
                        if (not ((typ0.morph.case_) & typ.morph.case_).is_nominative and not hiph): 
                            if (not typ.morph.case_.is_nominative): 
                                break
                    if (typ0.morph.number != MorphNumber.UNDEFINED and typ.morph.number != MorphNumber.UNDEFINED): 
                        if (((typ0.morph.number) & (typ.morph.number)) == (MorphNumber.UNDEFINED)): 
                            break
                if (not pref0 and pref and not hiph): 
                    nom = False
                    for m in typ.morph.items: 
                        if (m.number == MorphNumber.SINGULAR and m.case_.is_nominative): 
                            nom = True
                            break
                    if (not nom): 
                        if (LanguageHelper.ends_with(typ0.typ, "фракция") or LanguageHelper.ends_with(typ0.typ, "фракція") or typ0.typ == "банк"): 
                            pass
                        else: 
                            break
                for ty in types: 
                    if (OrgItemTypeToken.is_types_antagonistictt(ty, typ)): 
                        return None
            types.append(typ)
            in_brackets = False
            if (typ.name is not None): 
                if (BracketHelper.can_be_start_of_sequence(typ.begin_token.previous, True, False) and BracketHelper.can_be_end_of_sequence(typ.end_token.next0_, False, None, False)): 
                    typ.begin_token = typ.begin_token.previous
                    typ.end_token = typ.end_token.next0_
                    if (typ.begin_token.end_char < t0.begin_char): 
                        t0 = typ.begin_token
                    in_brackets = True
            t = typ.end_token
            hiph = False
        if ((types is None and ot_ex_li is None and ((attach_typ == OrganizationAnalyzer.AttachType.NORMAL or attach_typ == OrganizationAnalyzer.AttachType.NORMALAFTERDEP))) and rt0 is None): 
            ok = False
            if (not ok): 
                if (t0 is not None and t0.morph.class0_.is_adjective and t0.next0_ is not None): 
                    rt0 = self.__try_attach_org(t0.next0_, ad, attach_typ, mult_typ, is_additional_attach, level + 1, step)
                    if ((rt0) is not None): 
                        if (rt0.begin_token == t0): 
                            return rt0
                if (attach_typ == OrganizationAnalyzer.AttachType.NORMAL): 
                    rt0 = self.__try_attach_org_med(t, ad)
                    if ((rt0) is not None): 
                        return rt0
                if ((((t0.kit.recurse_level < 4) and (isinstance(t0, TextToken)) and t0.previous is not None) and t0.length_char > 2 and not t0.chars.is_all_lower) and not t0.is_newline_after and not MiscHelper.can_be_start_of_sentence(t0)): 
                    typ = OrgItemTypeToken.try_attach(t0.next0_, False, None)
                    if (typ is not None): 
                        t0.kit.recurse_level += 1
                        rrr = self.__try_attach_org(t0.next0_, ad, attach_typ, mult_typ, is_additional_attach, level + 1, step)
                        t0.kit.recurse_level -= 1
                        if (rrr is None): 
                            if (spec_word_before or t0.previous.is_value("ТЕРРИТОРИЯ", None)): 
                                org0 = OrganizationReferent()
                                org0.add_type(typ, False)
                                org0.add_name(t0.term, False, t0)
                                t1 = typ.end_token
                                t1 = (Utils.ifNotNull(self.__attach_tail_attributes(org0, t1.next0_, ad, False, OrganizationAnalyzer.AttachType.NORMAL, False), t1))
                                return ReferentToken(org0, t0, t1)
                tt = t
                first_pass3831 = True
                while True:
                    if first_pass3831: first_pass3831 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.is_and): 
                        if (tt == t): 
                            break
                        continue
                    if ((((isinstance(tt, TextToken)) and tt.chars.is_letter and not tt.chars.is_all_lower) and not tt.chars.is_capital_upper and tt.length_char > 1) and (tt.whitespaces_after_count < 2)): 
                        mc = tt.get_morph_class_in_dictionary()
                        if (mc.is_undefined): 
                            pass
                        elif (((tt.length_char < 5) and not mc.is_conjunction and not mc.is_preposition) and not mc.is_noun): 
                            pass
                        elif ((tt.length_char <= 3 and (isinstance(tt.previous, TextToken)) and tt.previous.chars.is_letter) and not tt.previous.chars.is_all_upper): 
                            pass
                        else: 
                            break
                    else: 
                        break
                    if ((isinstance(tt.next0_, ReferentToken)) and (isinstance(tt.next0_.get_referent(), OrganizationReferent))): 
                        ttt = t.previous
                        if ((((isinstance(ttt, TextToken)) and tt.chars.is_letter and not ttt.chars.is_all_lower) and not ttt.chars.is_capital_upper and ttt.length_char > 1) and ttt.get_morph_class_in_dictionary().is_undefined and (ttt.whitespaces_after_count < 2)): 
                            break
                        tt0 = t
                        t = t.previous
                        while t is not None: 
                            if (not (isinstance(t, TextToken)) or t.whitespaces_after_count > 2): 
                                break
                            elif (t.is_and): 
                                pass
                            elif ((t.chars.is_letter and not t.chars.is_all_lower and not t.chars.is_capital_upper) and t.length_char > 1 and t.get_morph_class_in_dictionary().is_undefined): 
                                tt0 = t
                            else: 
                                break
                            t = t.previous
                        nam = MiscHelper.get_text_value(tt0, tt, GetTextAttr.NO)
                        if (nam == "СЭД" or nam == "ЕОСЗ"): 
                            break
                        own = Utils.asObjectOrNull(tt.next0_.get_referent(), OrganizationReferent)
                        if (OrgProfile.UNIT in own.profiles): 
                            break
                        if (nam == "НК" or nam == "ГК"): 
                            return ReferentToken(own, t, tt.next0_)
                        org0 = OrganizationReferent()
                        org0.add_profile(OrgProfile.UNIT)
                        org0.add_name(nam, True, None)
                        if (nam.find(' ') > 0): 
                            org0.add_name(nam.replace(" ", ""), True, None)
                        org0.higher = own
                        t1 = tt.next0_
                        ttt1 = self.__attach_tail_attributes(org0, t1, ad, True, attach_typ, False)
                        if (tt0.kit.ontology is not None): 
                            li = tt0.kit.ontology.attach_token(OrganizationReferent.OBJ_TYPENAME, tt0)
                            if (li is not None): 
                                for v in li: 
                                    pass
                        return ReferentToken(org0, tt0, Utils.ifNotNull(ttt1, t1))
                if (((isinstance(t, TextToken)) and t.is_newline_before and t.length_char > 1) and not t.chars.is_all_lower and t.get_morph_class_in_dictionary().is_undefined): 
                    t1 = t.next0_
                    if (t1 is not None and not t1.is_newline_before and (isinstance(t1, TextToken))): 
                        t1 = t1.next0_
                    if (t1 is not None and t1.is_newline_before): 
                        typ0 = OrgItemTypeToken.try_attach(t1, False, None)
                        if ((typ0 is not None and typ0.root is not None and typ0.root.typ == OrgItemTypeTyp.PREFIX) and typ0.is_newline_after): 
                            if (self.__try_attach_org(t1, ad, OrganizationAnalyzer.AttachType.NORMAL, None, False, 0, -1) is None): 
                                org0_ = OrganizationReferent()
                                org0_.add_type(typ0, False)
                                org0_.add_name(MiscHelper.get_text_value(t, t1.previous, GetTextAttr.NO), True, None)
                                t1 = typ0.end_token
                                ttt1 = self.__attach_tail_attributes(org0_, t1.next0_, ad, True, attach_typ, False)
                                return ReferentToken(org0_, t, Utils.ifNotNull(ttt1, t1))
                        if (t1.is_char('(')): 
                            typ0 = OrgItemTypeToken.try_attach(t1.next0_, False, None)
                            if ((typ0) is not None): 
                                if (typ0.end_token.next0_ is not None and typ0.end_token.next0_.is_char(')') and typ0.end_token.next0_.is_newline_after): 
                                    org0_ = OrganizationReferent()
                                    org0_.add_type(typ0, False)
                                    org0_.add_name(MiscHelper.get_text_value(t, t1.previous, GetTextAttr.NO), True, None)
                                    t1 = typ0.end_token.next0_
                                    ttt1 = self.__attach_tail_attributes(org0_, t1.next0_, ad, True, attach_typ, False)
                                    return ReferentToken(org0_, t, Utils.ifNotNull(ttt1, t1))
                if ((isinstance(t, TextToken)) and t.is_newline_before and BracketHelper.can_be_start_of_sequence(t, False, False)): 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None and br.is_newline_after and (br.length_char < 100)): 
                        t1 = br.end_token.next0_
                        typ0 = OrgItemTypeToken.try_attach(t1, False, None)
                        if ((typ0 is not None and typ0.root is not None and typ0.root.typ == OrgItemTypeTyp.PREFIX) and typ0.is_newline_after): 
                            if (self.__try_attach_org(t1, ad, OrganizationAnalyzer.AttachType.NORMAL, None, False, 0, -1) is None): 
                                org0_ = OrganizationReferent()
                                org0_.add_type(typ0, False)
                                org0_.add_name(MiscHelper.get_text_value(t, t1.previous, GetTextAttr.NO), True, None)
                                t1 = typ0.end_token
                                ttt1 = self.__attach_tail_attributes(org0_, t1.next0_, ad, True, attach_typ, False)
                                return ReferentToken(org0_, t, Utils.ifNotNull(ttt1, t1))
                        if (t1 is not None and t1.is_char('(')): 
                            typ0 = OrgItemTypeToken.try_attach(t1.next0_, False, None)
                            if ((typ0) is not None): 
                                if (typ0.end_token.next0_ is not None and typ0.end_token.next0_.is_char(')') and typ0.end_token.next0_.is_newline_after): 
                                    org0_ = OrganizationReferent()
                                    org0_.add_type(typ0, False)
                                    org0_.add_name(MiscHelper.get_text_value(t, t1.previous, GetTextAttr.NO), True, None)
                                    t1 = typ0.end_token.next0_
                                    ttt1 = self.__attach_tail_attributes(org0_, t1.next0_, ad, True, attach_typ, False)
                                    return ReferentToken(org0_, t, Utils.ifNotNull(ttt1, t1))
                return None
        if (types is not None and len(types) > 1 and attach_typ != OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
            if (types[0].typ == "предприятие" or types[0].typ == "підприємство"): 
                del types[0]
                t0 = types[0].begin_token
        if (rt0 is None): 
            rt0 = self.__try_attach_org_(t0, t, ad, types, spec_word_before, attach_typ, mult_typ, is_additional_attach, level)
            if (rt0 is not None and ot_ex_li is not None): 
                for ot in ot_ex_li: 
                    if ((ot.end_char > rt0.end_char and ot.item is not None and ot.item.owner is not None) and ot.item.owner.is_ext_ontology): 
                        rt0 = (None)
                        break
                    elif (ot.end_char < rt0.begin_char): 
                        ot_ex_li = (None)
                        break
                    elif (ot.end_char < rt0.end_char): 
                        if (ot.end_token.next0_.get_morph_class_in_dictionary().is_preposition): 
                            rt0 = (None)
                            break
            if (rt0 is not None): 
                if (types is not None and rt0.begin_token == types[0].begin_token): 
                    for ty in types: 
                        rt0.referent.add_type(ty, True)
                if ((rt0.begin_token == t0 and t0.previous is not None and t0.previous.morph.class0_.is_adjective) and (t0.whitespaces_before_count < 2)): 
                    if (len(rt0.referent.geo_objects) == 0): 
                        geo_ = self.__is_geo(t0.previous, True)
                        if (geo_ is not None): 
                            if (rt0.referent._add_geo_object(geo_)): 
                                rt0.begin_token = t0.previous
        if (ot_ex_li is not None and rt0 is None and (len(ot_ex_li) < 10)): 
            for ot in ot_ex_li: 
                org0 = Utils.asObjectOrNull(ot.item.referent, OrganizationReferent)
                if (org0 is None): 
                    continue
                if (len(org0.names) == 0 and len(org0.eponyms) == 0): 
                    continue
                tyty = OrgItemTypeToken.try_attach(ot.begin_token, True, None)
                if (tyty is not None and tyty.begin_token == ot.end_token): 
                    continue
                ts = ot.begin_token
                te = ot.end_token
                is_quots = False
                is_very_doubt = False
                name_eq = False
                if (BracketHelper.can_be_start_of_sequence(ts.previous, False, False) and BracketHelper.is_bracket(ts.previous, False)): 
                    if (BracketHelper.can_be_end_of_sequence(te.next0_, False, None, False)): 
                        if (ot.length_char < 2): 
                            continue
                        if (ot.length_char == 2 and not te.get_source_text() in org0.names): 
                            pass
                        else: 
                            is_quots = True
                            ts = ts.previous
                            te = te.next0_
                    else: 
                        continue
                ok = types is not None
                if (ot.end_token.next0_ is not None and (isinstance(ot.end_token.next0_.get_referent(), OrganizationReferent))): 
                    ok = True
                elif (ot.end_token != ot.begin_token): 
                    if (step == 0): 
                        if (not "o2step" in t.kit.misc_data): 
                            t.kit.misc_data["o2step"] = None
                        continue
                    if (not ot.begin_token.chars.is_all_lower): 
                        ok = True
                    elif (spec_word_before or is_quots): 
                        ok = True
                elif (isinstance(ot.begin_token, TextToken)): 
                    if (step == 0): 
                        if (not "o2step" in t.kit.misc_data): 
                            t.kit.misc_data["o2step"] = None
                        continue
                    ok = False
                    len0_ = ot.begin_token.length_char
                    if (not ot.chars.is_all_lower): 
                        if (not ot.chars.is_all_upper and ot.morph.class0_.is_preposition): 
                            continue
                        for n in org0.names: 
                            if (ot.begin_token.is_value(n, None)): 
                                name_eq = True
                                break
                        ano = org0.find_near_occurence(ot.begin_token)
                        if (ano is None): 
                            if (not ot.item.owner.is_ext_ontology): 
                                if (len0_ < 3): 
                                    continue
                                else: 
                                    is_very_doubt = True
                        else: 
                            if (len0_ == 2 and not t.chars.is_all_upper): 
                                continue
                            d = ano.begin_char - ot.begin_token.begin_char
                            if (d < 0): 
                                d = (- d)
                            if (d > 2000): 
                                if (len0_ < 3): 
                                    continue
                                elif (len0_ < 5): 
                                    is_very_doubt = True
                            elif (d > 300): 
                                if (len0_ < 3): 
                                    continue
                            elif (len0_ < 3): 
                                if (d > 100 or not ot.begin_token.chars.is_all_upper): 
                                    is_very_doubt = True
                        if (((ot.begin_token.chars.is_all_upper or ot.begin_token.chars.is_last_lower)) and ((len0_ > 3 or ((len0_ == 3 and ((name_eq or ano is not None))))))): 
                            ok = True
                        elif ((spec_word_before or types is not None or is_quots) or name_eq): 
                            ok = True
                        elif ((ot.length_char < 3) and is_very_doubt): 
                            continue
                        elif (ot.item.owner.is_ext_ontology and ot.begin_token.get_morph_class_in_dictionary().is_undefined and ((len0_ > 3 or ((len0_ == 3 and ((name_eq or ano is not None))))))): 
                            ok = True
                        elif (ot.begin_token.chars.is_latin_letter): 
                            ok = True
                        elif ((name_eq and not ot.chars.is_all_lower and not ot.item.owner.is_ext_ontology) and not MiscHelper.can_be_start_of_sentence(ot.begin_token)): 
                            ok = True
                elif (isinstance(ot.begin_token, ReferentToken)): 
                    r = ot.begin_token.get_referent()
                    if (r.type_name != "DENOMINATION" and not is_quots): 
                        ok = False
                if (not ok): 
                    pass
                if (ok): 
                    ok = False
                    org0_ = OrganizationReferent()
                    if (types is not None): 
                        for ty in types: 
                            org0_.add_type(ty, False)
                        if (not org0_.can_be_equals(org0, ReferentsEqualType.FORMERGING)): 
                            continue
                    else: 
                        for ty in org0.types: 
                            org0_.add_type_str(ty)
                    if (org0.number is not None and (isinstance(ot.begin_token.previous, NumberToken)) and org0_.number is None): 
                        if (org0.number != str(ot.begin_token.previous.value) and (ot.begin_token.whitespaces_before_count < 2)): 
                            if (len(org0_.names) > 0 or org0_.higher is not None): 
                                is_very_doubt = False
                                ok = True
                                org0_.number = str(ot.begin_token.previous.value)
                                if (org0.higher is not None): 
                                    org0_.higher = org0.higher
                                t0 = ot.begin_token.previous
                    if (org0_.number is None): 
                        ttt = ot.end_token.next0_
                        nnn = OrgItemNumberToken.try_attach(ttt, (org0.number is not None or not ot.is_whitespace_after), None)
                        if (nnn is None and not ot.is_whitespace_after and ttt is not None): 
                            if (ttt.is_hiphen and ttt.next0_ is not None): 
                                ttt = ttt.next0_
                            if (isinstance(ttt, NumberToken)): 
                                nnn = OrgItemNumberToken._new1823(ot.end_token.next0_, ttt, str(ttt.value))
                        if (nnn is not None): 
                            org0_.number = nnn.number
                            te = nnn.end_token
                    norm = (ot.end_token.end_char - ot.begin_token.begin_char) > 5
                    s = MiscHelper.get_text_value_of_meta_token(ot, Utils.valToEnum((((GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE if norm else GetTextAttr.NO))) | (GetTextAttr.IGNOREARTICLES), GetTextAttr))
                    org0_.add_name(s, True, (None if norm else ot.begin_token))
                    if (types is None or len(types) == 0): 
                        s1 = MiscHelper.get_text_value_of_meta_token(ot, GetTextAttr.IGNOREARTICLES)
                        if (s1 != s and norm): 
                            org0_.add_name(s1, True, ot.begin_token)
                    t1 = te
                    if (t1.is_char(')') and t1.is_newline_after): 
                        pass
                    else: 
                        t1 = (Utils.ifNotNull(self.__attach_middle_attributes(org0_, t1.next0_), t1))
                        if (attach_typ != OrganizationAnalyzer.AttachType.NORMALAFTERDEP): 
                            t1 = (Utils.ifNotNull(self.__attach_tail_attributes(org0_, t1.next0_, ad, False, OrganizationAnalyzer.AttachType.NORMAL, False), t1))
                    hi = None
                    if (t1.next0_ is not None): 
                        hi = (Utils.asObjectOrNull(t1.next0_.get_referent(), OrganizationReferent))
                    if (org0.higher is not None and hi is not None and len(ot_ex_li) == 1): 
                        if (hi.can_be_equals(org0.higher, ReferentsEqualType.WITHINONETEXT)): 
                            org0_.higher = hi
                            t1 = t1.next0_
                    if ((len(org0_.eponyms) == 0 and org0_.number is None and is_very_doubt) and not name_eq and types is None): 
                        continue
                    if (not org0_.can_be_equals_ex(org0, True, ReferentsEqualType.WITHINONETEXT)): 
                        if (t is not None and OrgItemTypeToken.check_org_special_word_before(t.previous)): 
                            ok = True
                        elif (not is_very_doubt and ok): 
                            pass
                        else: 
                            if (not is_very_doubt): 
                                if (len(org0_.eponyms) > 0 or org0_.number is not None or org0_.higher is not None): 
                                    ok = True
                            ok = False
                    elif (org0_.can_be_equals(org0, ReferentsEqualType.DIFFERENTTEXTS)): 
                        org0_.merge_slots(org0, False)
                        ok = True
                    elif (org0.higher is None or org0_.higher is not None or ot.item.owner.is_ext_ontology): 
                        ok = True
                        org0_.merge_slots(org0, False)
                    elif (not ot.item.owner.is_ext_ontology and org0_.can_be_equals(org0, ReferentsEqualType.WITHINONETEXT)): 
                        if (org0.higher is None): 
                            org0_.merge_slots(org0, False)
                        ok = True
                    if (not ok): 
                        continue
                    if (ts.begin_char < t0.begin_char): 
                        t0 = ts
                    rt0 = ReferentToken(org0_, t0, t1)
                    if (org0_.kind == OrganizationKind.DEPARTMENT): 
                        self.__correct_dep_attrs(rt0, typ, False)
                    self.__correct_after(rt0)
                    if (ot.item.owner.is_ext_ontology): 
                        for sl in org0_.slots: 
                            if (isinstance(sl.value, Referent)): 
                                ext = False
                                for ss in org0.slots: 
                                    if (ss.value == sl.value): 
                                        ext = True
                                        break
                                if (not ext): 
                                    continue
                                rr = sl.value.clone()
                                rr.occurrence.clear()
                                org0_.upload_slot(sl, rr)
                                rt_ex = ReferentToken(rr, t0, t1)
                                rt_ex.set_default_local_onto(t0.kit.processor)
                                org0_.add_ext_referent(rt_ex)
                                for sss in rr.slots: 
                                    if (isinstance(sss.value, Referent)): 
                                        rrr = sss.value.clone()
                                        rrr.occurrence.clear()
                                        rr.upload_slot(sss, rrr)
                                        rt_ex2 = ReferentToken(rrr, t0, t1)
                                        rt_ex2.set_default_local_onto(t0.kit.processor)
                                        sl.value.add_ext_referent(rt_ex2)
                    self.__correct_after(rt0)
                    return rt0
        if ((rt0 is None and types is not None and len(types) == 1) and types[0].name is None): 
            tt0 = None
            if (MiscHelper.is_eng_article(types[0].begin_token)): 
                tt0 = types[0].begin_token
            elif (MiscHelper.is_eng_adj_suffix(types[0].end_token.next0_)): 
                tt0 = types[0].begin_token
            else: 
                tt00 = types[0].begin_token.previous
                if (tt00 is not None and (tt00.whitespaces_after_count < 2) and tt00.chars.is_latin_letter == types[0].chars.is_latin_letter): 
                    if (MiscHelper.is_eng_article(tt00)): 
                        tt0 = tt00
                    elif (tt00.morph.class0_.is_preposition or tt00.morph.class0_.is_pronoun): 
                        tt0 = tt00.next0_
            cou = 100
            if (tt0 is not None): 
                tt00 = tt0.previous
                while tt00 is not None and cou > 0: 
                    if (isinstance(tt00.get_referent(), OrganizationReferent)): 
                        if (OrgItemTypeToken.is_type_accords(Utils.asObjectOrNull(tt00.get_referent(), OrganizationReferent), types[0])): 
                            if ((types[0].whitespaces_after_count < 3) and OrgItemTypeToken.try_attach(types[0].end_token.next0_, True, None) is not None): 
                                pass
                            else: 
                                rt0 = ReferentToken(tt00.get_referent(), tt0, types[0].end_token)
                        break
                    tt00 = tt00.previous; cou -= 1
        if (rt0 is not None): 
            self.__correct_owner_before(rt0)
        if (hiph and not in_brackets and ((attach_typ == OrganizationAnalyzer.AttachType.NORMAL or attach_typ == OrganizationAnalyzer.AttachType.NORMALAFTERDEP))): 
            ok1 = False
            if (rt0 is not None and BracketHelper.can_be_end_of_sequence(rt0.end_token, True, None, False)): 
                if (len(types) > 0): 
                    ty = types[len(types) - 1]
                    if (ty.end_token.next0_ is not None and ty.end_token.next0_.is_hiphen and BracketHelper.can_be_start_of_sequence(ty.end_token.next0_.next0_, True, False)): 
                        ok1 = True
            elif (rt0 is not None and rt0.end_token.next0_ is not None and rt0.end_token.next0_.is_hiphen): 
                ty = OrgItemTypeToken.try_attach(rt0.end_token.next0_.next0_, False, None)
                if (ty is None): 
                    ok1 = True
            if (not ok1): 
                return None
        if (attach_typ == OrganizationAnalyzer.AttachType.MULTIPLE and t is not None): 
            if (t.chars.is_all_lower): 
                return None
        if (rt0 is None): 
            return rt0
        doubt = rt0.tag is not None
        org0_ = (Utils.asObjectOrNull(rt0.referent, OrganizationReferent))
        if (doubt and ad is not None): 
            rli = ad.local_ontology.try_attach_by_referent(org0_, None, True)
            if (rli is not None and len(rli) > 0): 
                doubt = False
            else: 
                for it in ad.local_ontology.items: 
                    if (it.referent is not None): 
                        if (it.referent.can_be_equals(org0_, ReferentsEqualType.WITHINONETEXT)): 
                            doubt = False
                            break
        if ((ad is not None and t is not None and t.kit.ontology is not None) and attach_typ == OrganizationAnalyzer.AttachType.NORMAL and doubt): 
            rli = t.kit.ontology.attach_referent(org0_)
            if (rli is not None): 
                if (len(rli) >= 1): 
                    doubt = False
        if (doubt): 
            return None
        self.__correct_after(rt0)
        return rt0
    
    def __correct_after(self, rt0 : 'ReferentToken') -> None:
        if (rt0 is None): 
            return
        if (not rt0.is_newline_after and rt0.end_token.next0_ is not None and rt0.end_token.next0_.is_char('(')): 
            tt = rt0.end_token.next0_.next0_
            if (isinstance(tt, TextToken)): 
                if (tt.is_char(')')): 
                    rt0.end_token = tt
                elif ((tt.length_char > 2 and (tt.length_char < 7) and tt.chars.is_latin_letter) and tt.chars.is_all_upper): 
                    act = tt.get_source_text().upper()
                    if ((isinstance(tt.next0_, NumberToken)) and not tt.is_whitespace_after and tt.next0_.typ == NumberSpellingType.DIGIT): 
                        tt = tt.next0_
                        act += tt.get_source_text()
                    if (tt.next0_ is not None and tt.next0_.is_char(')')): 
                        rt0.referent.add_slot(OrganizationReferent.ATTR_MISC, act, False, 0)
                        rt0.end_token = tt.next0_
                else: 
                    org0_ = Utils.asObjectOrNull(rt0.referent, OrganizationReferent)
                    if (org0_.kind == OrganizationKind.BANK and tt.chars.is_latin_letter): 
                        pass
        if (rt0.is_newline_before and rt0.is_newline_after and rt0.end_token.next0_ is not None): 
            t1 = rt0.end_token.next0_
            typ1 = OrgItemTypeToken.try_attach(t1, False, None)
            if ((typ1 is not None and typ1.is_newline_after and typ1.root is not None) and typ1.root.typ == OrgItemTypeTyp.PREFIX): 
                if (self.__try_attach_org(t1, None, OrganizationAnalyzer.AttachType.NORMAL, None, False, 0, -1) is None): 
                    rt0.referent.add_type(typ1, False)
                    rt0.end_token = typ1.end_token
            if (t1.is_char('(')): 
                typ1 = OrgItemTypeToken.try_attach(t1.next0_, False, None)
                if ((typ1) is not None): 
                    if ((typ1.root is not None and typ1.root.typ == OrgItemTypeTyp.PREFIX and typ1.end_token.next0_ is not None) and typ1.end_token.next0_.is_char(')') and typ1.end_token.next0_.is_newline_after): 
                        rt0.referent.add_type(typ1, False)
                        rt0.end_token = typ1.end_token.next0_
    
    @staticmethod
    def __last_typ(types : typing.List['OrgItemTypeToken']) -> 'OrgItemTypeToken':
        if (types is None): 
            return None
        for i in range(len(types) - 1, -1, -1):
            return types[i]
        return None
    
    def __try_attach_org_(self, t0 : 'Token', t : 'Token', ad : 'OrgAnalyzerData', types : typing.List['OrgItemTypeToken'], spec_word_before : bool, attach_typ : 'AttachType', mult_typ : 'OrgItemTypeToken', is_additional_attach : bool, level : int) -> 'ReferentToken':
        from pullenti.ner.org.internal.OrgItemEngItem import OrgItemEngItem
        from pullenti.ner.org.internal.OrgItemEponymToken import OrgItemEponymToken
        from pullenti.ner.org.internal.OrgItemNameToken import OrgItemNameToken
        if (t0 is None): 
            return None
        t1 = t
        typ = OrganizationAnalyzer.__last_typ(types)
        if (typ is not None): 
            if (typ.is_dep): 
                rt0 = self.__try_attach_dep(typ, attach_typ, spec_word_before)
                if (rt0 is not None): 
                    return rt0
                if (typ.typ == "группа" or typ.typ == "група"): 
                    typ.is_dep = False
                else: 
                    return None
            if (typ.is_newline_after and typ.name is None): 
                if (t1 is not None and (isinstance(t1.get_referent(), GeoReferent)) and OrgProfile.STATE in typ.profiles): 
                    pass
                elif (typ.root is not None and ((typ.root.coeff >= 3 or typ.root.is_pure_prefix))): 
                    pass
                elif (typ.coef >= 4): 
                    pass
                elif ((typ.coef >= 3 and (typ.newlines_after_count < 2) and typ.end_token.next0_ is not None) and typ.end_token.next0_.morph.class0_.is_preposition): 
                    pass
                else: 
                    return None
            if (typ != mult_typ and ((typ.morph.number == MorphNumber.PLURAL and not str.isupper(typ.typ[0])))): 
                if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                    pass
                elif (typ.end_token.is_value("ВЛАСТЬ", None)): 
                    pass
                else: 
                    return None
            if (attach_typ == OrganizationAnalyzer.AttachType.NORMAL or attach_typ == OrganizationAnalyzer.AttachType.NORMALAFTERDEP): 
                if (((typ.typ == "предприятие" or typ.typ == "підприємство")) and not spec_word_before and len(types) == 1): 
                    return None
        org0_ = OrganizationReferent()
        if (types is not None): 
            for ty in types: 
                org0_.add_type(ty, False)
        if (typ is not None and typ.root is not None and typ.root.is_pure_prefix): 
            if ((isinstance(t, TextToken)) and t.chars.is_all_upper and not t.is_newline_after): 
                b = BracketHelper.try_parse(t.next0_, BracketParseAttr.NO, 100)
                if (b is not None and b.is_quote_type): 
                    org0_.add_type_str(t.term)
                    t = t.next0_
                else: 
                    s = t.term
                    if (len(s) == 2 and s[len(s) - 1] == 'К'): 
                        org0_.add_type_str(s)
                        t = t.next0_
                    elif (((t.get_morph_class_in_dictionary().is_undefined and t.next0_ is not None and (isinstance(t.next0_, TextToken))) and t.next0_.chars.is_capital_upper and t.next0_.next0_ is not None) and not t.next0_.is_newline_after): 
                        if (t.next0_.next0_.is_char_of(",.;") or BracketHelper.can_be_end_of_sequence(t.next0_.next0_, False, None, False)): 
                            org0_.add_type_str(s)
                            t = t.next0_
            elif ((isinstance(t, TextToken)) and t.morph.class0_.is_adjective and not t.chars.is_all_lower): 
                rtg = Utils.asObjectOrNull(self.__is_geo(t, True), ReferentToken)
                if (rtg is not None and BracketHelper.can_be_start_of_sequence(rtg.end_token.next0_, False, False)): 
                    org0_._add_geo_object(rtg)
                    t = rtg.end_token.next0_
            elif ((t is not None and (isinstance(t.get_referent(), GeoReferent)) and t.next0_ is not None) and BracketHelper.can_be_start_of_sequence(t.next0_, True, False)): 
                org0_._add_geo_object(t.get_referent())
                t = t.next0_
        te = None
        ki0 = org0_.kind
        if (((((ki0 == OrganizationKind.GOVENMENT or ki0 == OrganizationKind.AIRPORT or ki0 == OrganizationKind.FACTORY) or ki0 == OrganizationKind.SEAPORT or ki0 == OrganizationKind.PARTY) or ki0 == OrganizationKind.JUSTICE or ki0 == OrganizationKind.MILITARY)) and t is not None): 
            g = self.__is_geo(t, False)
            if (g is None and t.morph.class0_.is_preposition and t.next0_ is not None): 
                g = self.__is_geo(t.next0_, False)
            if (g is not None): 
                if (org0_._add_geo_object(g)): 
                    t1 = self.__get_geo_end_token(g, t)
                    te = t1
                    t = t1.next0_
                    gt = OrgGlobal.GLOBAL_ORGS.try_attach(t, None, False)
                    if (gt is None and t is not None and t.kit.base_language.is_ua): 
                        gt = OrgGlobal.GLOBAL_ORGS_UA.try_attach(t, None, False)
                    if (gt is not None and len(gt) == 1): 
                        if (org0_.can_be_equals(gt[0].item.referent, ReferentsEqualType.FORMERGING)): 
                            org0_.merge_slots(gt[0].item.referent, False)
                            return ReferentToken(org0_, t0, gt[0].end_token)
        if (typ is not None and typ.root is not None and ((typ.root.can_be_single_geo and not typ.root.can_has_single_name))): 
            if (len(org0_.geo_objects) > 0 and te is not None): 
                return ReferentToken(org0_, t0, te)
            r = None
            t1 = (typ.end_token if typ != mult_typ else t0.previous)
            te = t1
            if (t is not None and t1.next0_ is not None): 
                r = self.__is_geo(t1.next0_, False)
                if (r is None and t1.next0_.morph.class0_.is_preposition): 
                    r = self.__is_geo(t1.next0_.next0_, False)
            if (r is not None): 
                if (not org0_._add_geo_object(r)): 
                    return None
                te = self.__get_geo_end_token(r, t1.next0_)
            if (len(org0_.geo_objects) > 0 and te is not None): 
                npt11 = NounPhraseHelper.try_parse(te.next0_, NounPhraseParseAttr.NO, 0, None)
                if (npt11 is not None and (te.whitespaces_after_count < 2) and npt11.noun.is_value("ДЕПУТАТ", None)): 
                    pass
                else: 
                    res11 = ReferentToken(org0_, t0, te)
                    if (org0_.find_slot(OrganizationReferent.ATTR_TYPE, "посольство", True) is not None): 
                        if (te.next0_ is not None and te.next0_.is_value("В", None)): 
                            r = self.__is_geo(te.next0_.next0_, False)
                            if (org0_._add_geo_object(r)): 
                                res11.end_token = self.__get_geo_end_token(r, te.next0_.next0_)
                    if (typ.root.can_has_number): 
                        num11 = OrgItemNumberToken.try_attach(res11.end_token.next0_, False, None)
                        if (num11 is not None): 
                            res11.end_token = num11.end_token
                            org0_.number = num11.number
                    return res11
        if (typ is not None and (((typ.typ == "милиция" or typ.typ == "полиция" or typ.typ == "міліція") or typ.typ == "поліція"))): 
            if (len(org0_.geo_objects) > 0 and te is not None): 
                return ReferentToken(org0_, t0, te)
            else: 
                return None
        if (t is not None and t.morph.class0_.is_proper_name): 
            rt1 = t.kit.process_referent("PERSON", t)
            if (rt1 is not None and (rt1.whitespaces_after_count < 2)): 
                if (BracketHelper.can_be_start_of_sequence(rt1.end_token.next0_, True, False)): 
                    t = rt1.end_token.next0_
                elif (rt1.end_token.next0_ is not None and rt1.end_token.next0_.is_hiphen and BracketHelper.can_be_start_of_sequence(rt1.end_token.next0_.next0_, True, False)): 
                    t = rt1.end_token.next0_.next0_
        elif ((t is not None and t.chars.is_capital_upper and t.morph.class0_.is_proper_surname) and t.next0_ is not None and (t.whitespaces_after_count < 2)): 
            if (BracketHelper.can_be_start_of_sequence(t.next0_, True, False)): 
                t = t.next0_
            elif (((t.next0_.is_char_of(":") or t.next0_.is_hiphen)) and BracketHelper.can_be_start_of_sequence(t.next0_.next0_, True, False)): 
                t = t.next0_.next0_
        tmax = None
        br = None
        if (t is not None): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (typ is not None and br is None and BracketHelper.can_be_start_of_sequence(t, False, False)): 
                if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), OrganizationReferent))): 
                    org0 = Utils.asObjectOrNull(t.next0_.get_referent(), OrganizationReferent)
                    if (not OrgItemTypeToken.is_types_antagonisticoo(org0_, org0)): 
                        org0.merge_slots(org0_, False)
                        return ReferentToken(org0, t0, t.next0_)
                if (((typ.typ == "компания" or typ.typ == "предприятие" or typ.typ == "организация") or typ.typ == "компанія" or typ.typ == "підприємство") or typ.typ == "організація"): 
                    if (OrgItemTypeToken.is_decree_keyword(t0.previous, 1)): 
                        return None
                ty2 = OrgItemTypeToken.try_attach(t.next0_, False, None)
                if (ty2 is not None): 
                    typs2 = list()
                    typs2.append(ty2)
                    rt2 = self.__try_attach_org_(t.next0_, ty2.end_token.next0_, ad, typs2, True, OrganizationAnalyzer.AttachType.HIGH, None, is_additional_attach, level + 1)
                    if (rt2 is not None): 
                        org0 = Utils.asObjectOrNull(rt2.referent, OrganizationReferent)
                        if (not OrgItemTypeToken.is_types_antagonisticoo(org0_, org0)): 
                            org0.merge_slots(org0_, False)
                            rt2.begin_token = t0
                            if (BracketHelper.can_be_end_of_sequence(rt2.end_token.next0_, False, None, False)): 
                                rt2.end_token = rt2.end_token.next0_
                            return rt2
        if (br is not None and typ is not None and org0_.kind == OrganizationKind.GOVENMENT): 
            if (typ.root is not None and not typ.root.can_has_single_name): 
                br = (None)
        if (br is not None and br.is_quote_type): 
            if (br.begin_token.next0_.is_value("О", None) or br.begin_token.next0_.is_value("ОБ", None)): 
                br = (None)
            elif (br.begin_token.previous is not None and br.begin_token.previous.is_char(':')): 
                br = (None)
        if (br is not None and br.is_quote_type and ((br.open_char != '<' or ((typ is not None and typ.root is not None and typ.root.is_pure_prefix))))): 
            if (t.is_newline_before and ((attach_typ == OrganizationAnalyzer.AttachType.NORMAL or attach_typ == OrganizationAnalyzer.AttachType.NORMALAFTERDEP))): 
                if (not br.is_newline_after): 
                    return None
            if (org0_.find_slot(OrganizationReferent.ATTR_TYPE, "организация", True) is not None or org0_.find_slot(OrganizationReferent.ATTR_TYPE, "організація", True) is not None): 
                if (typ.begin_token == typ.end_token): 
                    if (not spec_word_before): 
                        return None
            if (typ is not None and ((((typ.typ == "компания" or typ.typ == "предприятие" or typ.typ == "организация") or typ.typ == "компанія" or typ.typ == "підприємство") or typ.typ == "організація"))): 
                if (OrgItemTypeToken.is_decree_keyword(t0.previous, 1)): 
                    return None
            nn = OrgItemNameToken.try_attach(t.next0_, None, False, True)
            if (nn is not None and nn.is_ignored_part): 
                t = nn.end_token
            org0 = Utils.asObjectOrNull(t.next0_.get_referent(), OrganizationReferent)
            if (org0 is not None): 
                if (not OrgItemTypeToken.is_types_antagonisticoo(org0_, org0) and t.next0_.next0_ is not None): 
                    if (BracketHelper.can_be_end_of_sequence(t.next0_.next0_, False, None, False)): 
                        org0.merge_slots(org0_, False)
                        return ReferentToken(org0, t0, t.next0_.next0_)
                    if ((isinstance(t.next0_.next0_.get_referent(), OrganizationReferent)) and BracketHelper.can_be_end_of_sequence(t.next0_.next0_.next0_, False, None, False)): 
                        org0.merge_slots(org0_, False)
                        return ReferentToken(org0, t0, t.next0_)
                return None
            na0 = OrgItemNameToken.try_attach(br.begin_token.next0_, None, False, True)
            if (na0 is not None and na0.is_empty_word and na0.end_token.next0_ == br.end_token): 
                return None
            rt0 = self.__try_attach_org(t.next0_, None, attach_typ, None, is_additional_attach, level + 1, -1)
            if (len(br.internal) > 1): 
                if (rt0 is not None and BracketHelper.can_be_end_of_sequence(rt0.end_token, False, None, False)): 
                    br.end_token = rt0.end_token
                else: 
                    return None
            abbr = None
            tt00 = (None if rt0 is None else rt0.begin_token)
            if (((rt0 is None and t.next0_ is not None and (isinstance(t.next0_, TextToken))) and t.next0_.chars.is_all_upper and t.next0_.length_char > 2) and t.next0_.chars.is_cyrillic_letter): 
                rt0 = self.__try_attach_org(t.next0_.next0_, None, attach_typ, None, is_additional_attach, level + 1, -1)
                if (rt0 is not None and rt0.begin_token == t.next0_.next0_): 
                    tt00 = t.next0_
                    abbr = t.next0_.get_source_text()
                else: 
                    rt0 = (None)
            ok2 = False
            if (rt0 is not None): 
                if (rt0.end_token == br.end_token.previous or rt0.end_token == br.end_token): 
                    ok2 = True
                elif (BracketHelper.can_be_end_of_sequence(rt0.end_token, False, None, False) and rt0.end_char > br.end_char): 
                    br2 = BracketHelper.try_parse(br.end_token.next0_, BracketParseAttr.NO, 100)
                    if (br2 is not None and rt0.end_token == br2.end_token): 
                        ok2 = True
            if (ok2 and (isinstance(rt0.referent, OrganizationReferent))): 
                org0 = (Utils.asObjectOrNull(rt0.referent, OrganizationReferent))
                if (typ is not None and typ.typ == "служба" and ((org0.kind == OrganizationKind.MEDIA or org0.kind == OrganizationKind.PRESS))): 
                    if (br.begin_token == rt0.begin_token and br.end_token == rt0.end_token): 
                        return rt0
                typ1 = None
                if (tt00 != t.next0_): 
                    typ1 = OrgItemTypeToken.try_attach(t.next0_, False, ad)
                    if (typ1 is not None and typ1.end_token.next0_ == tt00): 
                        org0_.add_type(typ1, False)
                hi = False
                if (OrgOwnershipHelper.can_be_higher(org0, org0_, True)): 
                    if (OrgItemTypeToken.is_types_antagonisticoo(org0, org0_)): 
                        hi = True
                if (hi): 
                    org0_.higher = org0
                    rt0.set_default_local_onto(t.kit.processor)
                    org0_.add_ext_referent(rt0)
                    if (typ1 is not None): 
                        org0_.add_type(typ1, True)
                    if (abbr is not None): 
                        org0_.add_name(abbr, True, None)
                elif (not OrgItemTypeToken.is_types_antagonisticoo(org0, org0_)): 
                    org0_.merge_slots(org0, True)
                    if (abbr is not None): 
                        for s in org0_.slots: 
                            if (s.type_name == OrganizationReferent.ATTR_NAME): 
                                org0_.upload_slot(s, "{0} {1}".format(abbr, s.value))
                else: 
                    rt0 = (None)
                if (rt0 is not None): 
                    t11 = br.end_token
                    if (rt0.end_char > t11.end_char): 
                        t11 = rt0.end_token
                    ep11 = OrgItemEponymToken.try_attach(t11.next0_, True)
                    if (ep11 is not None): 
                        t11 = ep11.end_token
                        for e0_ in ep11.eponyms: 
                            org0_.add_eponym(e0_)
                    t1 = self.__attach_tail_attributes(org0_, t11.next0_, None, True, attach_typ, False)
                    if (t1 is None): 
                        t1 = t11
                    if (typ is not None): 
                        if ((typ.name is not None and typ.geo is None and len(org0_.names) > 0) and not typ.name in org0_.names): 
                            org0_.add_type_str(typ.name.lower())
                    return ReferentToken(org0_, t0, t1)
            if (rt0 is not None and (rt0.end_char < br.end_token.previous.end_char)): 
                rt1 = self.__try_attach_org(rt0.end_token.next0_, None, attach_typ, None, is_additional_attach, level + 1, -1)
                if (rt1 is not None and rt1.end_token.next0_ == br.end_token): 
                    return rt1
                org1 = Utils.asObjectOrNull(rt0.end_token.next0_.get_referent(), OrganizationReferent)
                if (org1 is not None and br.end_token.previous == rt0.end_token): 
                    pass
            for step in range(2):
                tt0 = t.next0_
                tt1 = None
                pref = True
                not_empty = 0
                t1 = t.next0_
                first_pass3832 = True
                while True:
                    if first_pass3832: first_pass3832 = False
                    else: t1 = t1.next0_
                    if (not (t1 is not None and t1 != br.end_token)): break
                    if (t1.is_char('(')): 
                        if (not_empty == 0): 
                            break
                        r = None
                        if (t1.next0_ is not None): 
                            r = t1.next0_.get_referent()
                        if (r is not None and t1.next0_.next0_ is not None and t1.next0_.next0_.is_char(')')): 
                            if (r.type_name == OrganizationAnalyzer.GEONAME): 
                                org0_._add_geo_object(r)
                                break
                        if (level == 0): 
                            rt = self.__try_attach_org(t1.next0_, None, OrganizationAnalyzer.AttachType.HIGH, None, False, level + 1, -1)
                            if (rt is not None and rt.end_token.next0_ is not None and rt.end_token.next0_.is_char(')')): 
                                if (not OrganizationReferent.can_be_second_definition(org0_, Utils.asObjectOrNull(rt.referent, OrganizationReferent))): 
                                    break
                                org0_.merge_slots(rt.referent, False)
                        break
                    else: 
                        org0 = Utils.asObjectOrNull(t1.get_referent(), OrganizationReferent)
                        if ((org0) is not None): 
                            if (((isinstance(t1.previous, NumberToken)) and t1.previous.previous == br.begin_token and not OrgItemTypeToken.is_types_antagonisticoo(org0_, org0)) and org0.number is None): 
                                org0.number = str(t1.previous.value)
                                org0.merge_slots(org0_, False)
                                if (BracketHelper.can_be_end_of_sequence(t1.next0_, False, None, False)): 
                                    t1 = t1.next0_
                                return ReferentToken(org0, t0, t1)
                            ne = OrgItemNameToken.try_attach(br.begin_token.next0_, None, attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY, True)
                            if (ne is not None and ne.is_ignored_part and ne.end_token.next0_ == t1): 
                                org0.merge_slots(org0_, False)
                                if (BracketHelper.can_be_end_of_sequence(t1.next0_, False, None, False)): 
                                    t1 = t1.next0_
                                return ReferentToken(org0, t0, t1)
                            return None
                        else: 
                            typ = OrgItemTypeToken.try_attach(t1, False, None)
                            if (typ is not None and types is not None): 
                                for ty in types: 
                                    if (OrgItemTypeToken.is_types_antagonistictt(ty, typ)): 
                                        typ = (None)
                                        break
                            if (typ is not None): 
                                if (typ.is_doubt_root_word and ((typ.end_token.next0_ == br.end_token or ((typ.end_token.next0_ is not None and typ.end_token.next0_.is_hiphen))))): 
                                    typ = (None)
                                elif (typ.morph.number == MorphNumber.PLURAL): 
                                    typ = (None)
                                elif (not typ.morph.case_.is_undefined and not typ.morph.case_.is_nominative): 
                                    typ = (None)
                                elif (typ.begin_token == typ.end_token): 
                                    ttt = typ.end_token.next0_
                                    if (ttt is not None and ttt.is_hiphen): 
                                        ttt = ttt.next0_
                                    if (ttt is not None): 
                                        if (ttt.is_value("БАНК", None)): 
                                            typ = (None)
                            ep = None
                            if (typ is None): 
                                ep = OrgItemEponymToken.try_attach(t1, False)
                            nu = OrgItemNumberToken.try_attach(t1, False, None)
                            if (nu is not None and not (isinstance(t1, NumberToken))): 
                                org0_.number = nu.number
                                tt1 = t1.previous
                                t1 = nu.end_token
                                not_empty += 2
                                continue
                            br_spec = False
                            if ((len(br.internal) == 0 and (isinstance(br.end_token.next0_, TextToken)) and ((not br.end_token.next0_.chars.is_all_lower and br.end_token.next0_.chars.is_letter))) and BracketHelper.can_be_end_of_sequence(br.end_token.next0_.next0_, True, None, False)): 
                                br_spec = True
                            if (typ is not None and ((pref or not typ.is_dep))): 
                                if (not_empty > 1): 
                                    rrr = self.__try_attach_org(typ.begin_token, ad, OrganizationAnalyzer.AttachType.NORMAL, None, False, level + 1, -1)
                                    if (rrr is not None): 
                                        t1 = typ.begin_token.previous
                                        br.end_token = t1
                                        break
                                if (((attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY or attach_typ == OrganizationAnalyzer.AttachType.HIGH)) and ((typ.root is None or not typ.root.is_pure_prefix))): 
                                    pref = False
                                elif (typ.name is None): 
                                    org0_.add_type(typ, False)
                                    if (pref): 
                                        tt0 = typ.end_token.next0_
                                    elif (typ.root is not None and typ.root.is_pure_prefix): 
                                        tt1 = typ.begin_token.previous
                                        break
                                elif (typ.end_token.next0_ != br.end_token): 
                                    org0_.add_type(typ, False)
                                    if (typ.typ == "банк"): 
                                        pref = False
                                    else: 
                                        org0_.add_type_str(typ.name.lower())
                                        org0_.add_type_str(typ.alt_typ)
                                        if (pref): 
                                            tt0 = typ.end_token.next0_
                                elif (br_spec): 
                                    org0_.add_type(typ, False)
                                    org0_.add_type_str(typ.name.lower())
                                    not_empty += 2
                                    tt0 = br.end_token.next0_
                                    t1 = tt0.next0_
                                    br.end_token = t1
                                    break
                                if (typ != mult_typ): 
                                    t1 = typ.end_token
                                    if (typ.geo is not None): 
                                        org0_.add_type(typ, False)
                            elif (ep is not None): 
                                for e0_ in ep.eponyms: 
                                    org0_.add_eponym(e0_)
                                not_empty += 3
                                t1 = ep.begin_token.previous
                                break
                            elif (t1 == t.next0_ and (isinstance(t1, TextToken)) and t1.chars.is_all_lower): 
                                return None
                            elif (t1.chars.is_letter or (isinstance(t1, NumberToken))): 
                                if (br_spec): 
                                    tt0 = br.begin_token
                                    t1 = br.end_token.next0_.next0_
                                    ss = MiscHelper.get_text_value(br.end_token, t1, GetTextAttr.NO)
                                    if (not Utils.isNullOrEmpty(ss)): 
                                        org0_.add_name(ss, True, br.end_token.next0_)
                                        br.end_token = t1
                                    break
                                pref = False
                                not_empty += 1
                can_has_num = False
                can_has_latin_name = False
                if (types is not None): 
                    for ty in types: 
                        if (ty.root is not None): 
                            if (ty.root.can_has_number): 
                                can_has_num = True
                            if (ty.root.can_has_latin_name): 
                                can_has_latin_name = True
                te = (Utils.ifNotNull(tt1, t1))
                if (te is not None and tt0 is not None and (tt0.begin_char < te.begin_char)): 
                    ttt = tt0
                    first_pass3833 = True
                    while True:
                        if first_pass3833: first_pass3833 = False
                        else: ttt = ttt.next0_
                        if (not (ttt != te and ttt is not None)): break
                        oin = OrgItemNameToken.try_attach(ttt, None, attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY, ttt == tt0)
                        if (oin is not None): 
                            if (oin.is_ignored_part and ttt == tt0): 
                                tt0 = oin.end_token.next0_
                                if (tt0 is None): 
                                    break
                                ttt = tt0.previous
                                continue
                            if (oin.is_std_tail): 
                                ei = OrgItemEngItem.try_attach(oin.begin_token, False)
                                if (ei is None and oin.begin_token.is_comma): 
                                    ei = OrgItemEngItem.try_attach(oin.begin_token.next0_, False)
                                if (ei is not None): 
                                    org0_.add_type_str(ei.full_value)
                                    if (ei.short_value is not None): 
                                        org0_.add_type_str(ei.short_value)
                                te = ttt.previous
                                break
                        if ((ttt != tt0 and (isinstance(ttt, ReferentToken)) and ttt.next0_ == te) and (isinstance(ttt.get_referent(), GeoReferent))): 
                            if (ttt.previous is not None and ttt.previous.get_morph_class_in_dictionary().is_adjective): 
                                continue
                            npt = NounPhraseHelper.try_parse(ttt.previous, NounPhraseParseAttr.REFERENTCANBENOUN, 0, None)
                            if (npt is not None and npt.end_token == ttt): 
                                pass
                            else: 
                                te = ttt.previous
                                if (te.morph.class0_.is_preposition and te.previous is not None): 
                                    te = te.previous
                            org0_._add_geo_object(ttt.get_referent())
                            break
                if (te is not None and tt0 is not None and (tt0.begin_char < te.begin_char)): 
                    if ((isinstance(te.previous, NumberToken)) and can_has_num): 
                        err = False
                        num1 = Utils.asObjectOrNull(te.previous, NumberToken)
                        if (org0_.number is not None and org0_.number != str(num1.value)): 
                            err = True
                        elif (te.previous.previous is None): 
                            err = True
                        elif (not te.previous.previous.is_hiphen and not te.previous.previous.chars.is_letter): 
                            err = True
                        elif (num1.value == "0"): 
                            err = True
                        if (not err): 
                            org0_.number = str(num1.value)
                            te = te.previous.previous
                            if (te is not None and ((te.is_hiphen or te.is_value("N", None) or te.is_value("№", None)))): 
                                te = te.previous
                s = (None if te is None else MiscHelper.get_text_value(tt0, te, GetTextAttr.NO))
                s1 = (None if te is None else MiscHelper.get_text_value(tt0, te, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE))
                if ((te is not None and (isinstance(te.previous, NumberToken)) and can_has_num) and org0_.number is None): 
                    org0_.number = str(te.previous.value)
                    tt11 = te.previous
                    if (tt11.previous is not None and tt11.previous.is_hiphen): 
                        tt11 = tt11.previous
                    if (tt11.previous is not None): 
                        s = MiscHelper.get_text_value(tt0, tt11.previous, GetTextAttr.NO)
                        s1 = MiscHelper.get_text_value(tt0, tt11.previous, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                if (not Utils.isNullOrEmpty(s)): 
                    if (tt0.morph.class0_.is_preposition and tt0 != br.begin_token.next0_): 
                        for ty in org0_.types: 
                            if (not " " in ty and str.islower(ty[0])): 
                                s = "{0} {1}".format(ty.upper(), s)
                                s1 = (None)
                                break
                    if (len(s) > OrganizationAnalyzer.MAX_ORG_NAME): 
                        return None
                    if (s1 is not None and s1 != s and len(s1) <= len(s)): 
                        org0_.add_name(s1, True, None)
                    org0_.add_name(s, True, tt0)
                    typ = OrganizationAnalyzer.__last_typ(types)
                    if (typ is not None and typ.root is not None and typ.root.canonic_text.startswith("ИНДИВИДУАЛЬН")): 
                        pers = typ.kit.process_referent("PERSON", tt0)
                        if (pers is not None and pers.end_token.next0_ == te): 
                            org0_.add_ext_referent(pers)
                            org0_.add_slot(OrganizationReferent.ATTR_OWNER, pers.referent, False, 0)
                    ok1 = False
                    for c in s: 
                        if (str.isalnum(c)): 
                            ok1 = True
                            break
                    if (not ok1): 
                        return None
                    if (br.begin_token.next0_.chars.is_all_lower): 
                        return None
                    if (len(org0_.types) == 0): 
                        ty = OrganizationAnalyzer.__last_typ(types)
                        if (ty is not None and ty.coef >= 4): 
                            pass
                        else: 
                            if (attach_typ == OrganizationAnalyzer.AttachType.NORMAL): 
                                return None
                            if (len(org0_.names) == 1 and (len(org0_.names[0]) < 2) and (br.length_char < 5)): 
                                return None
                elif (BracketHelper.can_be_start_of_sequence(t1, False, False)): 
                    br1 = BracketHelper.try_parse(t1, BracketParseAttr.NO, 100)
                    if (br1 is None): 
                        break
                    t = br1.begin_token
                    br = br1
                    continue
                elif (((org0_.number is not None or len(org0_.eponyms) > 0)) and t1 == br.end_token): 
                    pass
                elif (len(org0_.geo_objects) > 0 and len(org0_.types) > 2): 
                    pass
                else: 
                    return None
                t1 = br.end_token
                if (org0_.number is None and t1.next0_ is not None and (t1.whitespaces_after_count < 2)): 
                    num1 = (None if OrgItemTypeToken.is_decree_keyword(t0.previous, 1) else OrgItemNumberToken.try_attach(t1.next0_, False, typ))
                    if (num1 is not None): 
                        org0_.number = num1.number
                        t1 = num1.end_token
                    else: 
                        t1 = self.__attach_tail_attributes(org0_, t1.next0_, None, True, attach_typ, False)
                else: 
                    t1 = self.__attach_tail_attributes(org0_, t1.next0_, None, True, attach_typ, False)
                if (t1 is None): 
                    t1 = br.end_token
                ok0 = False
                if (types is not None): 
                    for ty in types: 
                        if (ty.name is not None): 
                            org0_.add_type_str(ty.name.lower())
                        if (attach_typ != OrganizationAnalyzer.AttachType.MULTIPLE and (ty.begin_char < t0.begin_char) and not ty.is_not_typ): 
                            t0 = ty.begin_token
                        if (not ty.is_doubt_root_word or ty.coef > 0 or ty.geo is not None): 
                            ok0 = True
                        elif (ty.typ == "движение" and ((not br.begin_token.next0_.chars.is_all_lower or not ty.chars.is_all_lower))): 
                            if (not br.begin_token.next0_.morph.case_.is_genitive): 
                                ok0 = True
                        elif (ty.typ == "АО"): 
                            if (ty.begin_token.chars.is_all_upper and (ty.whitespaces_after_count < 2) and BracketHelper.is_bracket(ty.end_token.next0_, True)): 
                                ok0 = True
                            else: 
                                tt2 = t1.next0_
                                first_pass3834 = True
                                while True:
                                    if first_pass3834: first_pass3834 = False
                                    else: tt2 = tt2.next0_
                                    if (not (tt2 is not None)): break
                                    if (tt2.is_comma): 
                                        continue
                                    if (tt2.is_value("ИМЕНОВАТЬ", None)): 
                                        ok0 = True
                                    if (tt2.is_value("В", None) and tt2.next0_ is not None): 
                                        if (tt2.next0_.is_value("ЛИЦО", None) or tt2.next0_.is_value("ДАЛЬШЕЙШЕМ", None) or tt2.next0_.is_value("ДАЛЕЕ", None)): 
                                            ok0 = True
                                    break
                if (len(org0_.eponyms) == 0 and (t1.whitespaces_after_count < 2)): 
                    ep = OrgItemEponymToken.try_attach(t1.next0_, False)
                    if (ep is not None): 
                        for e0_ in ep.eponyms: 
                            org0_.add_eponym(e0_)
                        ok0 = True
                        t1 = ep.end_token
                if (len(org0_.names) == 0): 
                    s = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                    s1 = (None if te is None else MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE))
                    org0_.add_name(s, True, br.begin_token.next0_)
                    org0_.add_name(s1, True, None)
                if (not ok0): 
                    if (OrgItemTypeToken.check_org_special_word_before(t0.previous)): 
                        ok0 = True
                if (not ok0 and attach_typ != OrganizationAnalyzer.AttachType.NORMAL): 
                    ok0 = True
                typ = OrganizationAnalyzer.__last_typ(types)
                if (typ is not None and typ.begin_token != typ.end_token): 
                    ok0 = True
                if (ok0): 
                    return ReferentToken(org0_, t0, t1)
                else: 
                    return ReferentToken._new736(org0_, t0, t1, org0_)
        num = None
        epon = None
        names = None
        pr = None
        own_org = None
        if (t1 is None): 
            t1 = t0
        elif (t is not None and t.previous is not None and t.previous.begin_char >= t0.begin_char): 
            t1 = t.previous
        br = (None)
        ok = False
        first_pass3835 = True
        while True:
            if first_pass3835: first_pass3835 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (isinstance(t.get_referent(), OrganizationReferent)): 
                pass
            rt = self.__attach_global_org(t, attach_typ, ad, None)
            if ((rt) is not None): 
                if (t == t0): 
                    if (not t.chars.is_all_lower): 
                        return rt
                    return None
                if (level == 0): 
                    rt = self.__try_attach_org(t, None, attach_typ, mult_typ, is_additional_attach, level + 1, -1)
                    if (rt is not None): 
                        return rt
            _num = OrgItemNumberToken.try_attach(t, typ is not None and typ.root is not None and typ.root.can_has_number, typ)
            if ((_num) is not None): 
                if ((typ is None or typ.root is None or not typ.root.can_has_number) or num is not None): 
                    break
                if (t.whitespaces_before_count > 2): 
                    if (typ.end_token.next0_ == t and MiscHelper.check_number_prefix(t) is not None): 
                        pass
                    else: 
                        break
                if (typ.root.canonic_text == "СУД" and typ.name is not None): 
                    if ((((typ.name.startswith("ВЕРХОВНЫЙ") or typ.name.startswith("АРБИТРАЖНЫЙ") or typ.name.startswith("ВЫСШИЙ")) or typ.name.startswith("КОНСТИТУЦИОН") or typ.name.startswith("ВЕРХОВНИЙ")) or typ.name.startswith("АРБІТРАЖНИЙ") or typ.name.startswith("ВИЩИЙ")) or typ.name.startswith("КОНСТИТУЦІЙН")): 
                        typ.coef = 3
                        break
                num = _num
                t = num.end_token
                t1 = t
                continue
            _epon = OrgItemEponymToken.try_attach(t, False)
            if ((_epon) is not None): 
                epon = _epon
                t = epon.end_token
                t1 = t
                continue
            typ = OrgItemTypeToken.try_attach(t, False, ad)
            if ((typ) is not None): 
                if (typ.morph.case_.is_genitive): 
                    if (typ.end_token.is_value("СЛУЖБА", None) or typ.end_token.is_value("УПРАВЛЕНИЕ", "УПРАВЛІННЯ") or typ.end_token.is_value("ХОЗЯЙСТВО", None)): 
                        typ = (None)
                if (typ is not None): 
                    if (not typ.is_doubt_root_word and attach_typ != OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
                        break
                    if (types is None and t0 == t): 
                        break
                    if (OrganizationAnalyzer.__last_typ(types) is not None and attach_typ != OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
                        if (OrgItemTypeToken.is_types_antagonistictt(typ, OrganizationAnalyzer.__last_typ(types))): 
                            if (names is not None and ((typ.morph.case_.is_genitive or typ.morph.case_.is_instrumental)) and (t.whitespaces_before_count < 2)): 
                                pass
                            else: 
                                break
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if ((br) is not None): 
                if (own_org is not None and not own_org.referent.is_from_global_ontos): 
                    break
                if (t.is_newline_before and ((attach_typ == OrganizationAnalyzer.AttachType.NORMAL or attach_typ == OrganizationAnalyzer.AttachType.NORMALAFTERDEP))): 
                    break
                typ = OrganizationAnalyzer.__last_typ(types)
                if ((org0_.find_slot(OrganizationReferent.ATTR_TYPE, "организация", True) is not None or org0_.find_slot(OrganizationReferent.ATTR_TYPE, "движение", True) is not None or org0_.find_slot(OrganizationReferent.ATTR_TYPE, "організація", True) is not None) or org0_.find_slot(OrganizationReferent.ATTR_TYPE, "рух", True) is not None): 
                    if (((typ is None or (typ.coef < 2))) and not spec_word_before): 
                        return None
                if (br.is_quote_type): 
                    if (br.open_char == '<' or br.whitespaces_before_count > 1): 
                        break
                    rt = self.__try_attach_org(t, None, OrganizationAnalyzer.AttachType.HIGH, None, False, level + 1, -1)
                    if (rt is None): 
                        break
                    org0 = Utils.asObjectOrNull(rt.referent, OrganizationReferent)
                    if (names is not None and len(names) == 1): 
                        if (((not names[0].is_noun_phrase and names[0].chars.is_all_upper)) or len(org0.names) > 0): 
                            if (not names[0].begin_token.morph.class0_.is_preposition): 
                                if (len(org0.names) == 0): 
                                    org0_.add_type_str(names[0].value)
                                else: 
                                    for n in org0.names: 
                                        org0_.add_name("{0} {1}".format(names[0].value, n), True, None)
                                        if (typ is not None and typ.root is not None and typ.root.typ != OrgItemTypeTyp.PREFIX): 
                                            org0_.add_name("{0} {1} {2}".format(typ.typ.upper(), MiscHelper.get_text_value_of_meta_token(names[0], GetTextAttr.NO), n), True, None)
                                    if (typ is not None): 
                                        typ.coef = 4
                                names = (None)
                    if (names is not None and len(names) > 0 and not spec_word_before): 
                        break
                    if (not org0_.can_be_equals(org0, ReferentsEqualType.FORMERGING)): 
                        break
                    org0_.merge_slots(org0, True)
                    t = rt.end_token
                    tmax = t
                    t1 = tmax
                    ok = True
                    continue
                elif (br.open_char == '('): 
                    if (t.next0_.get_referent() is not None and t.next0_.next0_ == br.end_token): 
                        r = t.next0_.get_referent()
                        if (r.type_name == OrganizationAnalyzer.GEONAME): 
                            org0_._add_geo_object(r)
                            t = br.end_token
                            t1 = t
                            tmax = t1
                            continue
                    elif (((isinstance(t.next0_, TextToken)) and t.next0_.chars.is_letter and not t.next0_.chars.is_all_lower) and t.next0_.next0_ == br.end_token): 
                        typ = OrgItemTypeToken.try_attach(t.next0_, True, None)
                        if (typ is not None): 
                            or0 = OrganizationReferent()
                            or0.add_type(typ, False)
                            if (or0.kind != OrganizationKind.UNDEFINED and org0_.kind != OrganizationKind.UNDEFINED): 
                                if (org0_.kind != or0.kind): 
                                    break
                            if (MiscHelper.test_acronym(t.next0_, t0, t.previous)): 
                                org0_.add_name(t.next0_.get_source_text(), True, None)
                            else: 
                                org0_.add_type(typ, False)
                            tmax = br.end_token
                            t = tmax
                            t1 = t
                            continue
                        else: 
                            nam = OrgItemNameToken.try_attach(t.next0_, None, attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY, True)
                            if (nam is not None and nam.is_empty_word): 
                                break
                            if (attach_typ == OrganizationAnalyzer.AttachType.NORMAL): 
                                org0 = OrganizationReferent()
                                org0.add_name(t.next0_.term, True, t.next0_)
                                if (not OrganizationReferent.can_be_second_definition(org0_, org0)): 
                                    break
                            org0_.add_name(t.next0_.term, True, t.next0_)
                            t = br.end_token
                            t1 = t
                            tmax = t1
                            continue
                break
            if (own_org is not None): 
                if (names is None and t.is_value("ПО", None)): 
                    pass
                elif (names is not None and t.is_comma_and): 
                    pass
                else: 
                    break
            typ = OrganizationAnalyzer.__last_typ(types)
            if (typ is not None and typ.root is not None and typ.root.is_pure_prefix): 
                if (pr is None and names is None): 
                    pr = OrgItemNameToken(t, t)
                    pr.morph.case_ = MorphCase.NOMINATIVE
            na = OrgItemNameToken.try_attach(t, pr, attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY, names is None)
            if (na is None and t is not None): 
                if (org0_.kind == OrganizationKind.CHURCH or ((typ is not None and typ.typ is not None and "фермер" in typ.typ))): 
                    prt = t.kit.process_referent("PERSON", t)
                    if (prt is not None): 
                        na = OrgItemNameToken._new2359(t, prt.end_token, True)
                        na.value = MiscHelper.get_text_value_of_meta_token(na, GetTextAttr.NO)
                        na.chars = CharsInfo._new2360(True)
                        na.morph = prt.morph
                        sur = prt.referent.get_string_value("LASTNAME")
                        if (sur is not None): 
                            tt = t
                            while tt is not None and tt.end_char <= prt.end_char: 
                                if (tt.is_value(sur, None)): 
                                    na.value = MiscHelper.get_text_value(tt, tt, GetTextAttr.NO)
                                    break
                                tt = tt.next0_
            if (na is None): 
                if (attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
                    if (t.is_char(',') or t.is_and): 
                        continue
                if (isinstance(t.get_referent(), OrganizationReferent)): 
                    own_org = (Utils.asObjectOrNull(t, ReferentToken))
                    continue
                if (t.is_value("ПРИ", None) and (isinstance(t.next0_, ReferentToken)) and (isinstance(t.next0_.get_referent(), OrganizationReferent))): 
                    t = t.next0_
                    own_org = (Utils.asObjectOrNull(t, ReferentToken))
                    continue
                if ((((names is None and t.is_char('/') and (isinstance(t.next0_, TextToken))) and not t.is_whitespace_after and t.next0_.chars.is_all_upper) and t.next0_.length_char >= 3 and (isinstance(t.next0_.next0_, TextToken))) and not t.next0_.is_whitespace_after and t.next0_.next0_.is_char('/')): 
                    na = OrgItemNameToken._new2361(t, t.next0_.next0_, t.next0_.get_source_text().upper(), t.next0_.chars)
                elif (names is None and typ is not None and ((typ.typ == "движение" or org0_.kind == OrganizationKind.PARTY))): 
                    tt1 = None
                    if (t.is_value("ЗА", None) or t.is_value("ПРОТИВ", None)): 
                        tt1 = t.next0_
                    elif (t.is_value("В", None) and t.next0_ is not None): 
                        if (t.next0_.is_value("ЗАЩИТА", None) or t.next0_.is_value("ПОДДЕРЖКА", None)): 
                            tt1 = t.next0_
                    elif (typ.chars.is_capital_upper and not MiscHelper.can_be_start_of_sentence(typ.begin_token)): 
                        mc = t.get_morph_class_in_dictionary()
                        if ((mc.is_adverb or mc.is_pronoun or mc.is_personal_pronoun) or mc.is_verb or mc.is_conjunction): 
                            pass
                        elif (t.chars.is_letter): 
                            tt1 = t
                        elif (typ.begin_token != typ.end_token): 
                            typ.coef = typ.coef + (3)
                    if (tt1 is not None): 
                        na = OrgItemNameToken.try_attach(tt1, pr, True, False)
                        if (na is not None): 
                            na.begin_token = t
                            typ.coef = typ.coef + (3)
                if (na is None): 
                    break
            if (num is not None or epon is not None): 
                break
            if (attach_typ == OrganizationAnalyzer.AttachType.MULTIPLE or attach_typ == OrganizationAnalyzer.AttachType.NORMAL or attach_typ == OrganizationAnalyzer.AttachType.NORMALAFTERDEP): 
                if (not na.is_std_tail and not na.chars.is_latin_letter and na.std_org_name_nouns == 0): 
                    if (t.morph.class0_.is_proper_name): 
                        break
                    cla = t.get_morph_class_in_dictionary()
                    if (cla.is_proper_surname or ((t.morph.language.is_ua and t.morph.class0_.is_proper_surname))): 
                        if (names is None and ((org0_.kind == OrganizationKind.AIRPORT or org0_.kind == OrganizationKind.SEAPORT))): 
                            pass
                        elif (typ is not None and typ.root is not None and typ.root.acronym == "ФОП"): 
                            pass
                        elif (typ is not None and "фермер" in typ.typ): 
                            pass
                        else: 
                            break
                    if (cla.is_undefined and na.chars.is_cyrillic_letter and na.chars.is_capital_upper): 
                        if ((t.previous is not None and not t.previous.morph.class0_.is_preposition and not t.previous.morph.class0_.is_conjunction) and t.previous.chars.is_all_lower): 
                            if ((t.next0_ is not None and (isinstance(t.next0_, TextToken)) and t.next0_.chars.is_letter) and not t.next0_.chars.is_all_lower): 
                                break
                    if (typ is not None and typ.typ == "союз" and not t.morph.case_.is_genitive): 
                        break
                    pit = t.kit.process_referent("PERSONPROPERTY", t)
                    if (pit is not None): 
                        if (pit.morph.number == MorphNumber.SINGULAR and pit.begin_token != pit.end_token): 
                            break
                    pit = t.kit.process_referent("DECREE", t)
                    if (pit is not None): 
                        nptt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                        if (nptt is not None and nptt.end_token.is_value("РЕШЕНИЕ", None)): 
                            pass
                        else: 
                            break
                    if (t.newlines_before_count > 1): 
                        break
            if (t.is_value("ИМЕНИ", "ІМЕНІ") or t.is_value("ИМ", "ІМ")): 
                break
            pr = na
            if (attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
                if (names is None): 
                    names = list()
                names.append(na)
                t = na.end_token
                t1 = t
                continue
            if (names is None): 
                if (tmax is not None): 
                    break
                if (t.previous is not None and t.is_newline_before and attach_typ != OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
                    if (typ is not None and typ.end_token.next0_ == t and typ.is_newline_before): 
                        pass
                    else: 
                        if (t.newlines_after_count > 1 or not t.chars.is_all_lower): 
                            break
                        if (t.morph.class0_.is_preposition and typ is not None and (((typ.typ == "комитет" or typ.typ == "комиссия" or typ.typ == "комітет") or typ.typ == "комісія"))): 
                            pass
                        elif (na.std_org_name_nouns > 0): 
                            pass
                        else: 
                            break
                elif (t.previous is not None and t.whitespaces_before_count > 1 and attach_typ != OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
                    if (t.whitespaces_before_count > 10): 
                        break
                    if (t.chars != t.previous.chars): 
                        break
                if (t.chars.is_all_lower and org0_.kind == OrganizationKind.JUSTICE): 
                    if (t.is_value("ПО", None) and t.next0_ is not None and t.next0_.is_value("ПРАВО", None)): 
                        pass
                    elif (t.is_value("З", None) and t.next0_ is not None and t.next0_.is_value("ПРАВ", None)): 
                        pass
                    else: 
                        break
                if (org0_.kind == OrganizationKind.FEDERATION): 
                    if (t.morph.class0_.is_preposition or t.morph.class0_.is_conjunction): 
                        break
                if (t.chars.is_all_lower and ((org0_.kind == OrganizationKind.AIRPORT or org0_.kind == OrganizationKind.SEAPORT or org0_.kind == OrganizationKind.HOTEL))): 
                    break
                if ((typ is not None and typ.length_char == 2 and ((typ.typ == "АО" or typ.typ == "СП"))) and not spec_word_before and attach_typ == OrganizationAnalyzer.AttachType.NORMAL): 
                    if (not na.chars.is_latin_letter): 
                        break
                if (t.chars.is_latin_letter and typ is not None and LanguageHelper.ends_with_ex(typ.typ, "служба", "сервис", "сервіс", None)): 
                    break
                if (typ is not None and ((typ.root is None or not typ.root.is_pure_prefix))): 
                    if (typ.chars.is_latin_letter and na.chars.is_latin_letter): 
                        if (not t.is_value("OF", None)): 
                            break
                    if ((na.is_in_dictionary and na.morph.language.is_cyrillic and na.chars.is_all_lower) and not na.morph.case_.is_undefined): 
                        if (na.preposition is None): 
                            if (not na.morph.case_.is_genitive): 
                                break
                            if (org0_.kind == OrganizationKind.PARTY and not spec_word_before): 
                                if (typ.typ == "лига"): 
                                    pass
                                else: 
                                    break
                            if (na.morph.number != MorphNumber.PLURAL): 
                                prr = t.kit.process_referent("PERSONPROPERTY", t)
                                if (prr is not None): 
                                    if (OrgItemEponymToken.try_attach(na.end_token.next0_, False) is not None): 
                                        pass
                                    else: 
                                        break
                    if (na.preposition is not None): 
                        if (org0_.kind == OrganizationKind.PARTY): 
                            if (na.preposition == "ЗА" or na.preposition == "ПРОТИВ"): 
                                pass
                            elif (na.preposition == "В"): 
                                if (na.value.startswith("ЗАЩИТ") and na.value.startswith("ПОДДЕРЖ")): 
                                    pass
                                else: 
                                    break
                            else: 
                                break
                        else: 
                            if (na.preposition == "В"): 
                                break
                            if (typ.is_doubt_root_word): 
                                if (LanguageHelper.ends_with_ex(typ.typ, "комитет", "комиссия", "комітет", "комісія") and ((t.is_value("ПО", None) or t.is_value("З", None)))): 
                                    pass
                                elif (names is None and na.std_org_name_nouns > 0): 
                                    pass
                                else: 
                                    break
                    elif (na.chars.is_capital_upper and na.chars.is_cyrillic_letter): 
                        prt = na.kit.process_referent("PERSON", na.begin_token)
                        if (prt is not None): 
                            if (org0_.kind == OrganizationKind.CHURCH): 
                                na.end_token = prt.end_token
                                na.is_std_name = True
                                na.value = MiscHelper.get_text_value_of_meta_token(na, GetTextAttr.NO)
                            elif ((typ is not None and typ.typ is not None and "фермер" in typ.typ) and names is None): 
                                na.end_token = prt.end_token
                            else: 
                                break
                if (na.is_empty_word): 
                    break
                if (na.is_std_tail): 
                    if (na.chars.is_latin_letter and na.chars.is_all_upper and (na.length_char < 4)): 
                        na.is_std_tail = False
                        na.value = na.get_source_text().upper()
                    else: 
                        break
                names = list()
            else: 
                na0 = names[len(names) - 1]
                if (na0.is_std_tail): 
                    break
                if (na.preposition is None): 
                    if ((not na.chars.is_latin_letter and na.chars.is_all_lower and not na.is_after_conjunction) and not na.morph.case_.is_genitive): 
                        break
            names.append(na)
            t = na.end_token
            t1 = t
        typ = OrganizationAnalyzer.__last_typ(types)
        do_higher_always = False
        if (typ is not None): 
            if (((attach_typ == OrganizationAnalyzer.AttachType.NORMAL or attach_typ == OrganizationAnalyzer.AttachType.NORMALAFTERDEP)) and typ.morph.number == MorphNumber.PLURAL): 
                return None
            if (LanguageHelper.ends_with_ex(typ.typ, "комитет", "комиссия", "комітет", "комісія")): 
                pass
            elif (typ.typ == "служба" and own_org is not None and typ.name is not None): 
                ki = own_org.referent.kind
                if (ki == OrganizationKind.PRESS or ki == OrganizationKind.MEDIA): 
                    typ.coef = typ.coef + (3)
                    do_higher_always = True
                else: 
                    own_org = (None)
            elif ((typ.typ == "служба" and own_org is not None and num is None) and OrganizationAnalyzer.__is_mvd_org(Utils.asObjectOrNull(own_org.referent, OrganizationReferent)) is not None and (((((isinstance(typ.begin_token.previous, NumberToken)) and (typ.whitespaces_before_count < 3))) or names is not None))): 
                typ.coef = typ.coef + (4)
                if (isinstance(typ.begin_token.previous, NumberToken)): 
                    t0 = typ.begin_token.previous
                    num = OrgItemNumberToken._new1823(t0, t0, typ.begin_token.previous.value)
            elif ((((typ.is_doubt_root_word or typ.typ == "организация" or typ.typ == "управление") or typ.typ == "служба" or typ.typ == "общество") or typ.typ == "союз" or typ.typ == "організація") or typ.typ == "керування" or typ.typ == "суспільство"): 
                own_org = (None)
            if (org0_.kind == OrganizationKind.GOVENMENT): 
                if (names is None and ((typ.name is None or Utils.compareStrings(typ.name, typ.typ, True) == 0))): 
                    if ((attach_typ != OrganizationAnalyzer.AttachType.EXTONTOLOGY and typ.typ != "следственный комитет" and typ.typ != "кабинет министров") and typ.typ != "слідчий комітет"): 
                        if (((typ.typ == "администрация" or typ.typ == "адміністрація")) and (isinstance(typ.end_token.next0_, TextToken))): 
                            rt1 = typ.kit.process_referent("PERSONPROPERTY", typ.end_token.next0_)
                            if (rt1 is not None and typ.end_token.next0_.morph.case_.is_genitive): 
                                geo_ = Utils.asObjectOrNull(rt1.referent.get_slot_value("REF"), GeoReferent)
                                if (geo_ is not None): 
                                    org0_.add_name("АДМИНИСТРАЦИЯ " + typ.end_token.next0_.term, True, None)
                                    org0_._add_geo_object(geo_)
                                    return ReferentToken(org0_, typ.begin_token, rt1.end_token)
                        if ((typ.coef < 5) or typ.chars.is_all_lower): 
                            return None
        elif (names is not None and names[0].chars.is_all_lower): 
            if (attach_typ != OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
                return None
        always = False
        name_ = None
        if (((num is not None or org0_.number is not None or epon is not None) or attach_typ == OrganizationAnalyzer.AttachType.HIGH or attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY) or own_org is not None): 
            cou0 = len(org0_.slots)
            if (names is not None): 
                if ((len(names) == 1 and names[0].chars.is_all_upper and attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY) and is_additional_attach): 
                    org0_.add_name(MiscHelper.get_text_value(names[0].begin_token, names[len(names) - 1].end_token, GetTextAttr.NO), True, names[0].begin_token)
                else: 
                    name_ = MiscHelper.get_text_value(names[0].begin_token, names[len(names) - 1].end_token, GetTextAttr.NO)
                    if ((names[0].is_noun_phrase and typ is not None and typ.root is not None) and not typ.root.is_pure_prefix and mult_typ is None): 
                        name_ = "{0} {1}".format(Utils.ifNotNull(typ.name, (typ.typ.upper() if typ is not None and typ.typ is not None else None)), name_)
            elif (typ is not None and typ.name is not None and ((typ.root is None or not typ.root.is_pure_prefix))): 
                if (typ.chars.is_all_lower and not typ.can_be_organization and (typ.name_words_count < 3)): 
                    org0_.add_type_str(typ.name.lower())
                else: 
                    name_ = typ.name
                if (typ != mult_typ): 
                    if (t1.end_char < typ.end_token.end_char): 
                        t1 = typ.end_token
            if (name_ is not None): 
                if (len(name_) > OrganizationAnalyzer.MAX_ORG_NAME): 
                    return None
                org0_.add_name(name_, True, None)
            if (num is not None): 
                org0_.number = num.number
            if (epon is not None): 
                for e0_ in epon.eponyms: 
                    org0_.add_eponym(e0_)
            ok = attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY
            if (typ is not None and typ.root is not None and typ.root.can_be_normal_dep): 
                ok = True
            for a in org0_.slots: 
                if (a.type_name == OrganizationReferent.ATTR_NUMBER): 
                    if (typ is not None and typ.typ == "корпус"): 
                        pass
                    else: 
                        ok = True
                elif (a.type_name == OrganizationReferent.ATTR_GEO): 
                    if (typ.root is not None and typ.root.can_be_single_geo): 
                        ok = True
                elif (a.type_name != OrganizationReferent.ATTR_TYPE and a.type_name != OrganizationReferent.ATTR_PROFILE): 
                    ok = True
                    break
            if (attach_typ == OrganizationAnalyzer.AttachType.NORMAL): 
                if (typ is None): 
                    ok = False
                elif ((typ.end_char - typ.begin_char) < 2): 
                    if (num is None and epon is None): 
                        ok = False
                    elif (epon is None): 
                        if (t1.is_whitespace_after or t1.next0_ is None): 
                            pass
                        elif (t1.next0_.is_char_of(".,;") and t1.next0_.is_whitespace_after): 
                            pass
                        else: 
                            ok = False
            if ((not ok and typ is not None and typ.can_be_dep_before_organization) and own_org is not None): 
                org0_.add_type_str(("підрозділ" if own_org.kit.base_language.is_ua else "подразделение"))
                org0_.higher = Utils.asObjectOrNull(own_org.referent, OrganizationReferent)
                t1 = (own_org)
                ok = True
            elif (typ is not None and own_org is not None and OrgOwnershipHelper.can_be_higher(Utils.asObjectOrNull(own_org.referent, OrganizationReferent), org0_, True)): 
                if (OrgItemTypeToken.is_types_antagonisticoo(Utils.asObjectOrNull(own_org.referent, OrganizationReferent), org0_)): 
                    if (org0_.kind == OrganizationKind.DEPARTMENT and not typ.can_be_dep_before_organization): 
                        pass
                    else: 
                        org0_.higher = Utils.asObjectOrNull(own_org.referent, OrganizationReferent)
                        if (t1.end_char < own_org.end_char): 
                            t1 = (own_org)
                        ok = True
                elif (typ.root is not None and ((typ.root.can_be_normal_dep or "Сбербанк" in str(own_org.referent)))): 
                    org0_.higher = Utils.asObjectOrNull(own_org.referent, OrganizationReferent)
                    if (t1.end_char < own_org.end_char): 
                        t1 = (own_org)
                    ok = True
        elif (names is not None): 
            if (typ is None): 
                if (names[0].is_std_name and spec_word_before): 
                    org0_.add_name(names[0].value, True, None)
                    t1 = names[0].end_token
                    t = self.__attach_tail_attributes(org0_, t1.next0_, None, True, attach_typ, False)
                    if (t is not None): 
                        t1 = t
                    return ReferentToken(org0_, t0, t1)
                return None
            if (typ.root is not None and typ.root.must_has_capital_name): 
                if (names[0].chars.is_all_lower): 
                    return None
            if (names[0].chars.is_latin_letter): 
                if (typ.root is not None and not typ.root.can_has_latin_name): 
                    if (not typ.chars.is_latin_letter): 
                        return None
                if (names[0].chars.is_all_lower and not typ.chars.is_latin_letter): 
                    return None
                tmp = io.StringIO()
                print(names[0].value, end="", file=tmp)
                t1 = names[0].end_token
                j = 1
                while j < len(names): 
                    if (not names[j].is_std_tail and ((names[j].is_newline_before or not names[j].chars.is_latin_letter))): 
                        tmax = names[j].begin_token.previous
                        if (typ.geo is None and org0_.find_slot(OrganizationReferent.ATTR_GEO, None, True) is not None): 
                            org0_.slots.remove(org0_.find_slot(OrganizationReferent.ATTR_GEO, None, True))
                        break
                    else: 
                        t1 = names[j].end_token
                        if (names[j].is_std_tail): 
                            ei = OrgItemEngItem.try_attach(names[j].begin_token, False)
                            if (ei is not None): 
                                org0_.add_type_str(ei.full_value)
                                if (ei.short_value is not None): 
                                    org0_.add_type_str(ei.short_value)
                            break
                        if (names[j - 1].end_token.is_char('.') and not names[j - 1].value.endswith(".")): 
                            print(".{0}".format(names[j].value), end="", file=tmp, flush=True)
                        else: 
                            print(" {0}".format(names[j].value), end="", file=tmp, flush=True)
                    j += 1
                if (tmp.tell() > OrganizationAnalyzer.MAX_ORG_NAME): 
                    return None
                nnn = Utils.toStringStringIO(tmp)
                if (nnn.startswith("OF ") or nnn.startswith("IN ")): 
                    Utils.insertStringIO(tmp, 0, (Utils.ifNotNull(typ.name, typ.typ)).upper() + " ")
                if (tmp.tell() < 3): 
                    if (tmp.tell() < 2): 
                        return None
                    if (types is not None and names[0].chars.is_all_upper): 
                        pass
                    else: 
                        return None
                ok = True
                org0_.add_name(Utils.toStringStringIO(tmp), True, None)
            elif (typ.root is not None and typ.root.is_pure_prefix): 
                tt = Utils.asObjectOrNull(typ.end_token, TextToken)
                if (tt is None): 
                    return None
                if (tt.is_newline_after): 
                    if (names[0].is_newline_after and typ.is_newline_before): 
                        pass
                    else: 
                        return None
                if (typ.begin_token == typ.end_token and tt.chars.is_all_lower): 
                    return None
                if (names[0].chars.is_all_lower): 
                    if (not names[0].morph.case_.is_genitive): 
                        return None
                t1 = names[0].end_token
                j = 1
                while j < len(names): 
                    if (names[j].is_newline_before or names[j].chars != names[0].chars): 
                        break
                    else: 
                        t1 = names[j].end_token
                    j += 1
                ok = True
                name_ = MiscHelper.get_text_value(names[0].begin_token, t1, GetTextAttr.NO)
                if (num is None and (isinstance(t1, NumberToken)) and t1.typ == NumberSpellingType.DIGIT): 
                    tt1 = t1.previous
                    if (tt1 is not None and tt1.is_hiphen): 
                        tt1 = tt1.previous
                    if (tt1 is not None and tt1.end_char > names[0].begin_char and (isinstance(tt1, TextToken))): 
                        name_ = MiscHelper.get_text_value(names[0].begin_token, tt1, GetTextAttr.NO)
                        org0_.number = str(t1.value)
                if (len(name_) > OrganizationAnalyzer.MAX_ORG_NAME): 
                    return None
                org0_.add_name(name_, True, names[0].begin_token)
            else: 
                if (typ.is_dep): 
                    return None
                if (typ.morph.number == MorphNumber.PLURAL and attach_typ != OrganizationAnalyzer.AttachType.MULTIPLE): 
                    return None
                tmp = io.StringIO()
                koef = typ.coef
                if (koef >= 4): 
                    always = True
                if (org0_.find_slot(OrganizationReferent.ATTR_GEO, None, True) is not None): 
                    koef += (1)
                if (spec_word_before): 
                    koef += (1)
                if (names[0].chars.is_all_lower and typ.chars.is_all_lower and not spec_word_before): 
                    if (koef >= 3): 
                        if (t is not None and (isinstance(t.get_referent(), GeoReferent))): 
                            pass
                        else: 
                            koef -= (3)
                if (typ.chars_root.is_capital_upper): 
                    koef += (0.5)
                if (len(types) > 1): 
                    koef += (len(types) - 1)
                if (typ.name is not None): 
                    to = typ.begin_token
                    while to != typ.end_token and to is not None: 
                        if (OrgItemTypeToken.is_std_adjective(to, False)): 
                            koef += (2)
                        if (to.chars.is_capital_upper): 
                            koef += (0.5)
                        to = to.next0_
                ki = org0_.kind
                if (attach_typ == OrganizationAnalyzer.AttachType.MULTIPLE and ((typ.name is None or len(typ.name) == len(typ.typ)))): 
                    pass
                elif ((((((ki == OrganizationKind.MEDIA or ki == OrganizationKind.PARTY or ki == OrganizationKind.PRESS) or ki == OrganizationKind.FACTORY or ki == OrganizationKind.AIRPORT) or ki == OrganizationKind.SEAPORT or ((typ.root is not None and typ.root.must_has_capital_name))) or ki == OrganizationKind.BANK or "предприятие" in typ.typ) or "организация" in typ.typ or "підприємство" in typ.typ) or "організація" in typ.typ): 
                    if (typ.name is not None): 
                        org0_.add_type_str(typ.name.lower())
                else: 
                    print(Utils.ifNotNull(typ.name, (typ.typ.upper() if typ is not None and typ.typ is not None else None)), end="", file=tmp)
                if (typ != mult_typ): 
                    t1 = typ.end_token
                j = 0
                first_pass3836 = True
                while True:
                    if first_pass3836: first_pass3836 = False
                    else: j += 1
                    if (not (j < len(names))): break
                    if (((names[j].is_newline_before and j > 0)) or names[j].is_noun_phrase != names[0].is_noun_phrase): 
                        break
                    elif (names[j].chars != names[0].chars and names[j].begin_token.chars != names[0].chars): 
                        break
                    else: 
                        if (j == 0 and names[j].preposition is None and names[j].is_in_dictionary): 
                            if (not names[j].morph.case_.is_genitive and ((typ.root is not None and not typ.root.can_has_single_name))): 
                                break
                        if (j == 0 and names[0].preposition == "ПО" and (((typ.typ == "комитет" or typ.typ == "комиссия" or typ.typ == "комітет") or typ.typ == "комісія"))): 
                            koef += 2.5
                        if ((j == 0 and names[j].whitespaces_before_count > 2 and names[j].newlines_before_count == 0) and names[j].begin_token.previous is not None): 
                            koef -= ((names[j].whitespaces_before_count) / (2))
                        if (names[j].is_std_name): 
                            koef += (4)
                        elif (names[j].std_org_name_nouns > 0 and ((ki == OrganizationKind.GOVENMENT or LanguageHelper.ends_with(typ.typ, "центр")))): 
                            koef += (names[j].std_org_name_nouns)
                        if (((ki == OrganizationKind.AIRPORT or ki == OrganizationKind.SEAPORT)) and j == 0): 
                            koef += 1
                        t1 = names[j].end_token
                        if (names[j].is_noun_phrase): 
                            if (not names[j].chars.is_all_lower): 
                                ca = names[j].morph.case_
                                if ((ca.is_dative or ca.is_genitive or ca.is_instrumental) or ca.is_prepositional): 
                                    koef += (0.5)
                                else: 
                                    continue
                            elif (((j == 0 or names[j].is_after_conjunction)) and names[j].morph.case_.is_genitive and names[j].preposition is None): 
                                koef += (0.5)
                            if (j == (len(names) - 1)): 
                                if (isinstance(names[j].end_token.next0_, TextToken)): 
                                    if (names[j].end_token.next0_.get_morph_class_in_dictionary().is_verb): 
                                        koef += 0.5
                        to = names[j].begin_token
                        while to is not None: 
                            if (isinstance(to, TextToken)): 
                                if (attach_typ == OrganizationAnalyzer.AttachType.NORMAL or attach_typ == OrganizationAnalyzer.AttachType.NORMALAFTERDEP): 
                                    if (to.chars.is_capital_upper): 
                                        koef += (0.5)
                                    elif ((j == 0 and ((to.chars.is_all_upper or to.chars.is_last_lower)) and to.length_char > 2) and typ.root is not None and typ.root.can_has_latin_name): 
                                        koef += (1)
                                elif (to.chars.is_all_upper or to.chars.is_capital_upper): 
                                    koef += (1)
                            if (to == names[j].end_token): 
                                break
                            to = to.next0_
                ttt = typ.begin_token.previous
                while ttt is not None: 
                    if (isinstance(ttt.get_referent(), OrganizationReferent)): 
                        koef += (1)
                        break
                    elif (not (isinstance(ttt, TextToken))): 
                        break
                    elif (ttt.chars.is_letter): 
                        break
                    ttt = ttt.previous
                oki = org0_.kind
                if (oki == OrganizationKind.GOVENMENT or oki == OrganizationKind.STUDY or oki == OrganizationKind.PARTY): 
                    koef += (len(names))
                if (attach_typ != OrganizationAnalyzer.AttachType.NORMAL and attach_typ != OrganizationAnalyzer.AttachType.NORMALAFTERDEP): 
                    koef += (3)
                br1 = None
                if ((t1.whitespaces_after_count < 2) and BracketHelper.can_be_start_of_sequence(t1.next0_, True, False)): 
                    br1 = BracketHelper.try_parse(t1.next0_, BracketParseAttr.NO, 100)
                    if (br1 is not None and (br1.length_char < 30)): 
                        sss = MiscHelper.get_text_value_of_meta_token(br1, GetTextAttr.NO)
                        if (sss is not None and len(sss) > 2): 
                            org0_.add_name(sss, True, br1.begin_token.next0_)
                            koef += (1)
                            t1 = br1.end_token
                        else: 
                            br1 = (None)
                if (koef >= 3 and t1.next0_ is not None): 
                    r = t1.next0_.get_referent()
                    if (r is not None and ((r.type_name == OrganizationAnalyzer.GEONAME or r.type_name == OrganizationReferent.OBJ_TYPENAME))): 
                        koef += (1)
                    elif (self.__is_geo(t1.next0_, False) is not None): 
                        koef += (1)
                    elif (t1.next0_.is_char('(') and self.__is_geo(t1.next0_.next0_, False) is not None): 
                        koef += (1)
                    elif (spec_word_before and t1.kit.process_referent("PERSON", t1.next0_) is not None): 
                        koef += (1)
                if (koef >= 4): 
                    ok = True
                if (not ok): 
                    if ((oki == OrganizationKind.PRESS or oki == OrganizationKind.FEDERATION or "агентство" in org0_.types) or ((oki == OrganizationKind.PARTY and OrgItemTypeToken.check_org_special_word_before(t0.previous)))): 
                        if (not names[0].is_newline_before and not names[0].morph.class0_.is_proper): 
                            if (names[0].morph.case_.is_genitive and names[0].is_in_dictionary): 
                                if (typ.chars.is_all_lower and not names[0].chars.is_all_lower): 
                                    ok = True
                                    t1 = names[0].end_token
                            elif (not names[0].is_in_dictionary and names[0].chars.is_all_upper): 
                                ok = True
                                Utils.setLengthStringIO(tmp, 0)
                                t1 = names[0].end_token
                if ((not ok and oki == OrganizationKind.FEDERATION and names[0].morph.case_.is_genitive) and koef > 0): 
                    if (self.__is_geo(names[len(names) - 1].end_token.next0_, False) is not None): 
                        ok = True
                if (not ok and typ is not None and typ.root is not None): 
                    if (len(names) == 1 and ((names[0].chars.is_all_upper or names[0].chars.is_last_lower))): 
                        if ((ki == OrganizationKind.BANK or ki == OrganizationKind.CULTURE or ki == OrganizationKind.HOTEL) or ki == OrganizationKind.MEDIA or ki == OrganizationKind.MEDICAL): 
                            ok = True
                if (ok): 
                    tt1 = t1
                    if (br1 is not None): 
                        tt1 = br1.begin_token.previous
                    if ((isinstance(tt1.get_referent(), GeoReferent)) and tt1.get_referent().is_state): 
                        if (names[0].begin_token != tt1): 
                            tt1 = t1.previous
                            org0_._add_geo_object(t1.get_referent())
                    s = MiscHelper.get_text_value(names[0].begin_token, tt1, GetTextAttr.NO)
                    if ((tt1 == names[0].end_token and typ is not None and typ.typ is not None) and "фермер" in typ.typ and names[0].value is not None): 
                        s = names[0].value
                    cla = tt1.get_morph_class_in_dictionary()
                    if ((names[0].begin_token == t1 and s is not None and t1.morph.case_.is_genitive) and t1.chars.is_capital_upper): 
                        if (cla.is_undefined or cla.is_proper_geo): 
                            if (ki == OrganizationKind.MEDICAL or ki == OrganizationKind.JUSTICE): 
                                geo_ = GeoReferent()
                                geo_.add_slot(GeoReferent.ATTR_NAME, t1.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), False, 0)
                                geo_.add_slot(GeoReferent.ATTR_TYPE, ("місто" if t1.kit.base_language.is_ua else "город"), False, 0)
                                rt = ReferentToken(geo_, t1, t1)
                                rt.data = (ad)
                                org0_._add_geo_object(rt)
                                s = (None)
                    if (s is not None): 
                        if (tmp.tell() == 0): 
                            if (names[0].morph.case_.is_genitive or names[0].preposition is not None): 
                                if (names[0].chars.is_all_lower): 
                                    print(Utils.ifNotNull(typ.name, typ.typ), end="", file=tmp)
                        if (tmp.tell() > 0): 
                            print(' ', end="", file=tmp)
                        print(s, end="", file=tmp)
                    if (tmp.tell() > OrganizationAnalyzer.MAX_ORG_NAME): 
                        return None
                    org0_.add_name(Utils.toStringStringIO(tmp), True, names[0].begin_token)
                    if (len(types) > 1 and types[0].name is not None): 
                        org0_.add_type_str(types[0].name.lower())
        else: 
            if (typ is None): 
                return None
            if (len(types) == 2 and types[0].coef > typ.coef): 
                typ = types[0]
            if ((typ.typ == "банк" and (isinstance(t, ReferentToken)) and not t.is_newline_before) and typ.morph.number == MorphNumber.SINGULAR): 
                if (typ.name is not None): 
                    if (typ.begin_token.chars.is_all_lower): 
                        org0_.add_type_str(typ.name.lower())
                    else: 
                        org0_.add_name(typ.name, True, None)
                        s0 = MiscHelper.get_text_value_of_meta_token(typ, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                        if (s0 != typ.name): 
                            org0_.add_name(s0, True, None)
                r = t.get_referent()
                if (r.type_name == OrganizationAnalyzer.GEONAME and t.morph.case_ != MorphCase.NOMINATIVE): 
                    org0_._add_geo_object(r)
                    if (len(types) == 1 and (t.whitespaces_after_count < 3)): 
                        typ1 = OrgItemTypeToken.try_attach(t.next0_, False, None)
                        if (typ1 is not None and typ1.root is not None and typ1.root.typ == OrgItemTypeTyp.PREFIX): 
                            org0_.add_type(typ1, False)
                            t = typ1.end_token
                    return ReferentToken(org0_, t0, t)
            if (((typ.root is not None and typ.root.is_pure_prefix)) and (typ.coef < 4)): 
                return None
            if (typ.root is not None and typ.root.must_has_capital_name): 
                return None
            if (typ.name is None): 
                if (((typ.typ.endswith("университет") or typ.typ.endswith("університет"))) and self.__is_geo(typ.end_token.next0_, False) is not None): 
                    always = True
                elif (((org0_.kind == OrganizationKind.JUSTICE or org0_.kind == OrganizationKind.AIRPORT or org0_.kind == OrganizationKind.SEAPORT)) and org0_.find_slot(OrganizationReferent.ATTR_GEO, None, True) is not None): 
                    pass
                elif (typ.coef >= 4): 
                    always = True
                elif (typ.chars.is_capital_upper): 
                    if (typ.end_token.next0_ is not None and ((typ.end_token.next0_.is_hiphen or typ.end_token.next0_.is_char_of(":")))): 
                        pass
                    else: 
                        li = (None if ad is None else ad.local_ontology.try_attach_by_item(org0_.create_ontology_item()))
                        if (li is not None and len(li) > 0): 
                            for ll in li: 
                                r = Utils.ifNotNull(ll.referent, Utils.asObjectOrNull(ll.tag, Referent))
                                if (r is not None): 
                                    if (org0_.can_be_equals(r, ReferentsEqualType.FORMERGING)): 
                                        ttt = typ.end_token
                                        nu = OrgItemNumberToken.try_attach(ttt.next0_, True, None)
                                        if (nu is not None): 
                                            if (r.number != nu.number): 
                                                ttt = (None)
                                            else: 
                                                org0_.number = nu.number
                                                ttt = nu.end_token
                                        elif (len(li) > 1): 
                                            ttt = (None)
                                        if (ttt is not None): 
                                            return ReferentToken(r, typ.begin_token, ttt)
                    return None
                else: 
                    cou = 0
                    tt = typ.begin_token.previous
                    first_pass3837 = True
                    while True:
                        if first_pass3837: first_pass3837 = False
                        else: tt = tt.previous; cou += 1
                        if (not (tt is not None and (cou < 200))): break
                        org0 = Utils.asObjectOrNull(tt.get_referent(), OrganizationReferent)
                        if (org0 is None): 
                            continue
                        if (not org0.can_be_equals(org0_, ReferentsEqualType.WITHINONETEXT)): 
                            continue
                        tt = (Utils.ifNotNull(self.__attach_tail_attributes(org0_, typ.end_token.next0_, ad, False, attach_typ, False), (typ.end_token if typ is not None else None)))
                        if (not org0.can_be_equals(org0_, ReferentsEqualType.WITHINONETEXT)): 
                            break
                        org0_.merge_slots(org0, True)
                        return ReferentToken(org0_, typ.begin_token, tt)
                    if (typ.root is not None and typ.root.can_be_single_geo and t1.next0_ is not None): 
                        ggg = self.__is_geo(t1.next0_, False)
                        if (ggg is not None): 
                            org0_._add_geo_object(ggg)
                            t1 = self.__get_geo_end_token(ggg, t1.next0_)
                            return ReferentToken(org0_, t0, t1)
                    return None
            if (typ.morph.number == MorphNumber.PLURAL or typ == mult_typ): 
                return None
            koef = typ.coef
            if (typ.name_words_count == 1 and typ.name is not None and len(typ.name) > len(typ.typ)): 
                koef += 1
            if (spec_word_before): 
                koef += (1)
            ok = False
            if (typ.chars_root.is_capital_upper): 
                koef += (0.5)
                if (typ.name_words_count == 1): 
                    koef += (0.5)
            if (epon is not None): 
                koef += (2)
            has_nonstd_words = False
            to = typ.begin_token
            while to != typ.end_token and to is not None: 
                if (OrgItemTypeToken.is_std_adjective(to, False)): 
                    if (typ.root is not None and typ.root.coeff > 0): 
                        koef += ((1 if OrgItemTypeToken.is_std_adjective(to, True) else math.floor(0.5)))
                else: 
                    has_nonstd_words = True
                if (to.chars.is_capital_upper and not to.morph.class0_.is_pronoun): 
                    koef += (0.5)
                to = to.next0_
            if (not has_nonstd_words and org0_.kind == OrganizationKind.GOVENMENT): 
                koef -= (2)
            if (typ.chars.is_all_lower and (typ.coef < 4)): 
                koef -= (2)
            if (koef > 1 and typ.name_words_count > 2): 
                koef += (2)
            ttt = typ.begin_token.previous
            while ttt is not None: 
                if (isinstance(ttt.get_referent(), OrganizationReferent)): 
                    koef += (1)
                    break
                elif (not (isinstance(ttt, TextToken))): 
                    break
                elif (ttt.chars.is_letter): 
                    break
                ttt = ttt.previous
            ttt = typ.end_token.next0_
            while ttt is not None: 
                if (isinstance(ttt.get_referent(), OrganizationReferent)): 
                    koef += (1)
                    break
                elif (not (isinstance(ttt, TextToken))): 
                    break
                elif (ttt.chars.is_letter): 
                    break
                ttt = ttt.next0_
            if (typ.whitespaces_before_count > 4 and typ.whitespaces_after_count > 4): 
                koef += (0.5)
            if (typ.can_be_organization): 
                for s in org0_.slots: 
                    if ((s.type_name == OrganizationReferent.ATTR_EPONYM or s.type_name == OrganizationReferent.ATTR_NAME or s.type_name == OrganizationReferent.ATTR_GEO) or s.type_name == OrganizationReferent.ATTR_NUMBER): 
                        koef += (3)
                        break
            org0_.add_type(typ, False)
            if (((org0_.kind == OrganizationKind.BANK or org0_.kind == OrganizationKind.JUSTICE)) and typ.name is not None and len(typ.name) > len(typ.typ)): 
                koef += (1)
            if (org0_.kind == OrganizationKind.JUSTICE and len(org0_.geo_objects) > 0): 
                always = True
            if (org0_.kind == OrganizationKind.AIRPORT or org0_.kind == OrganizationKind.SEAPORT): 
                for g in org0_.geo_objects: 
                    if (g.is_city): 
                        always = True
            if (koef > 3 or always): 
                ok = True
            if (((org0_.kind == OrganizationKind.PARTY or org0_.kind == OrganizationKind.JUSTICE)) and typ.morph.number == MorphNumber.SINGULAR): 
                if (org0_.find_slot(OrganizationReferent.ATTR_GEO, None, True) is not None and typ.name is not None and len(typ.name) > len(typ.typ)): 
                    ok = True
                elif (typ.coef >= 4): 
                    ok = True
                elif (typ.name_words_count > 2): 
                    ok = True
            if (ok): 
                if (typ.name is not None and not typ.is_not_typ): 
                    if (len(typ.name) > OrganizationAnalyzer.MAX_ORG_NAME or Utils.compareStrings(typ.name, typ.typ, True) == 0): 
                        return None
                    org0_.add_name(typ.name, True, None)
                t1 = typ.end_token
        if (not ok or len(org0_.slots) == 0): 
            return None
        if (attach_typ == OrganizationAnalyzer.AttachType.NORMAL or attach_typ == OrganizationAnalyzer.AttachType.NORMALAFTERDEP): 
            ok = always
            for s in org0_.slots: 
                if (s.type_name != OrganizationReferent.ATTR_TYPE and s.type_name != OrganizationReferent.ATTR_PROFILE): 
                    ok = True
                    break
            if (not ok): 
                return None
        if (tmax is not None and (t1.end_char < tmax.begin_char)): 
            t1 = tmax
        t = self.__attach_tail_attributes(org0_, t1.next0_, None, True, attach_typ, False)
        if (t is not None): 
            t1 = t
        if (own_org is not None and org0_.higher is None): 
            if (do_higher_always or OrgOwnershipHelper.can_be_higher(Utils.asObjectOrNull(own_org.referent, OrganizationReferent), org0_, False)): 
                org0_.higher = Utils.asObjectOrNull(own_org.referent, OrganizationReferent)
                if (own_org.begin_char > t1.begin_char): 
                    t1 = (own_org)
                    t = self.__attach_tail_attributes(org0_, t1.next0_, None, True, attach_typ, False)
                    if (t is not None): 
                        t1 = t
        if (((own_org is not None and typ is not None and typ.typ == "банк") and typ.geo is not None and org0_.higher == own_org.referent) and "Сбербанк" in str(own_org.referent)): 
            tt2 = t1.next0_
            if (tt2 is not None): 
                if (tt2.is_comma or tt2.is_value("В", None)): 
                    tt2 = tt2.next0_
            if (tt2 is not None and (isinstance(tt2.get_referent(), GeoReferent))): 
                s = org0_.find_slot(OrganizationReferent.ATTR_GEO, None, True)
                if (s is not None): 
                    org0_.slots.remove(s)
                if (org0_._add_geo_object(tt2)): 
                    t1 = tt2
        if (t1.is_newline_after and t0.is_newline_before): 
            typ1 = OrgItemTypeToken.try_attach(t1.next0_, False, None)
            if (typ1 is not None and typ1.is_newline_after): 
                if (self.__try_attach_org(t1.next0_, ad, OrganizationAnalyzer.AttachType.NORMAL, None, False, 0, -1) is None): 
                    org0_.add_type(typ1, False)
                    t1 = typ1.end_token
            if (t1.next0_ is not None and t1.next0_.is_char('(')): 
                typ1 = OrgItemTypeToken.try_attach(t1.next0_.next0_, False, None)
                if ((typ1) is not None): 
                    if (typ1.end_token.next0_ is not None and typ1.end_token.next0_.is_char(')') and typ1.end_token.next0_.is_newline_after): 
                        org0_.add_type(typ1, False)
                        t1 = typ1.end_token.next0_
        if (attach_typ == OrganizationAnalyzer.AttachType.NORMAL and ((typ is None or (typ.coef < 4)))): 
            if (org0_.find_slot(OrganizationReferent.ATTR_GEO, None, True) is None or ((typ is not None and typ.geo is not None))): 
                is_all_low = True
                t = t0
                while t != t1.next0_: 
                    if (t.chars.is_letter): 
                        if (not t.chars.is_all_lower): 
                            is_all_low = False
                    elif (not (isinstance(t, TextToken))): 
                        is_all_low = False
                    t = t.next0_
                if (is_all_low and not spec_word_before): 
                    return None
        res = ReferentToken(org0_, t0, t1)
        if (types is not None and len(types) > 0): 
            res.morph = types[0].morph
            if (types[0].is_not_typ and types[0].begin_token == t0 and (types[0].end_char < t1.end_char)): 
                res.begin_token = types[0].end_token.next0_
        else: 
            res.morph = t0.morph
        if ((org0_.number is None and t1.next0_ is not None and (t1.whitespaces_after_count < 2)) and typ is not None and ((typ.root is None or typ.root.can_has_number))): 
            num1 = OrgItemNumberToken.try_attach(t1.next0_, False, typ)
            if (num1 is None and t1.next0_.is_hiphen): 
                num1 = OrgItemNumberToken.try_attach(t1.next0_.next0_, False, typ)
            if (num1 is not None): 
                if (OrgItemTypeToken.is_decree_keyword(t0.previous, 2)): 
                    pass
                else: 
                    org0_.number = num1.number
                    t1 = num1.end_token
                    res.end_token = t1
        return res
    
    def __try_attach_org_before(self, t : 'Token', ad : 'OrgAnalyzerData') -> 'ReferentToken':
        if (t is None or t.previous is None): 
            return None
        min_end_char = t.previous.end_char
        max_end_char = t.end_char
        t0 = t.previous
        if ((isinstance(t0, ReferentToken)) and (isinstance(t0.get_referent(), OrganizationReferent)) and t0.previous is not None): 
            min_end_char = t0.previous.end_char
            t0 = t0.previous
        res = None
        while t0 is not None: 
            if (t0.whitespaces_after_count > 1): 
                break
            cou = 0
            tt0 = t0
            num = None
            num_et = None
            ttt = t0
            first_pass3838 = True
            while True:
                if first_pass3838: first_pass3838 = False
                else: ttt = ttt.previous
                if (not (ttt is not None)): break
                if (ttt.whitespaces_after_count > 1): 
                    break
                if (ttt.is_hiphen or ttt.is_char('.')): 
                    continue
                if (isinstance(ttt, NumberToken)): 
                    if (num is not None): 
                        break
                    num = str(ttt.value)
                    num_et = ttt
                    tt0 = ttt.previous
                    continue
                nn = OrgItemNumberToken.try_attach(ttt, False, None)
                if (nn is not None): 
                    num = nn.number
                    num_et = nn.end_token
                    tt0 = ttt.previous
                    continue
                cou += 1
                if (cou > 10): 
                    break
                if (ttt.is_value("НАПРАВЛЕНИЕ", "НАПРЯМОК")): 
                    if (num is not None or (((isinstance(ttt.previous, NumberToken)) and (ttt.whitespaces_before_count < 3)))): 
                        oo = OrganizationReferent()
                        oo.add_profile(OrgProfile.UNIT)
                        oo.add_type_str((("НАПРЯМОК" if ttt.morph.language.is_ua else "НАПРАВЛЕНИЕ")).lower())
                        rt0 = ReferentToken(oo, ttt, ttt)
                        if (num_et is not None and num is not None): 
                            oo.add_slot(OrganizationReferent.ATTR_NUMBER, num, False, 0)
                            rt0.end_token = num_et
                            return rt0
                        if (isinstance(ttt.previous, NumberToken)): 
                            rt0.begin_token = ttt.previous
                            oo.add_slot(OrganizationReferent.ATTR_NUMBER, str(ttt.previous.value), False, 0)
                            return rt0
                typ1 = OrgItemTypeToken.try_attach(ttt, True, None)
                if (typ1 is None): 
                    if (cou == 1): 
                        break
                    continue
                if (typ1.end_token == tt0): 
                    t0 = ttt
            rt = self.__try_attach_org(t0, ad, OrganizationAnalyzer.AttachType.NORMAL, None, False, 0, -1)
            if (rt is not None): 
                if (rt.end_char >= min_end_char and rt.end_char <= max_end_char): 
                    oo = Utils.asObjectOrNull(rt.referent, OrganizationReferent)
                    if (oo.higher is not None and oo.higher.higher is not None and oo.higher == rt.end_token.get_referent()): 
                        return rt
                    if (rt.begin_char < t.begin_char): 
                        return rt
                    res = rt
                else: 
                    break
            elif (not (isinstance(t0, TextToken))): 
                break
            elif (not t0.chars.is_letter): 
                if (not BracketHelper.is_bracket(t0, False)): 
                    break
            t0 = t0.previous
        if (res is not None): 
            return None
        typ = None
        t0 = t.previous
        first_pass3839 = True
        while True:
            if first_pass3839: first_pass3839 = False
            else: t0 = t0.previous
            if (not (t0 is not None)): break
            if (t0.whitespaces_after_count > 1): 
                break
            if (isinstance(t0, NumberToken)): 
                continue
            if (t0.is_char('.') or t0.is_hiphen): 
                continue
            if (not (isinstance(t0, TextToken))): 
                break
            if (not t0.chars.is_letter): 
                break
            ty = OrgItemTypeToken.try_attach(t0, True, ad)
            if (ty is not None): 
                nn = OrgItemNumberToken.try_attach(ty.end_token.next0_, True, ty)
                if (nn is not None): 
                    ty.end_token = nn.end_token
                    ty.number = nn.number
                elif ((isinstance(ty.end_token.next0_, NumberToken)) and (ty.whitespaces_after_count < 2)): 
                    ty.end_token = ty.end_token.next0_
                    ty.number = str(ty.end_token.value)
                if (ty.end_char >= min_end_char and ty.end_char <= max_end_char): 
                    typ = ty
                else: 
                    break
        if (typ is not None and typ.is_dep): 
            res = self.__try_attach_dep_before_org(typ, None)
        return res
    
    def __try_attach_dep_before_org(self, typ : 'OrgItemTypeToken', rt_org : 'ReferentToken') -> 'ReferentToken':
        if (typ is None): 
            return None
        org0_ = (None if rt_org is None else Utils.asObjectOrNull(rt_org.referent, OrganizationReferent))
        t = typ.end_token
        if (org0_ is None): 
            t = t.next0_
            if (t is not None and ((t.is_value("ПРИ", None) or t.is_value("AT", None) or t.is_value("OF", None)))): 
                t = t.next0_
            if (t is None): 
                return None
            org0_ = (Utils.asObjectOrNull(t.get_referent(), OrganizationReferent))
        else: 
            t = rt_org.end_token
        if (org0_ is None): 
            return None
        t1 = t
        if (isinstance(t1.next0_, ReferentToken)): 
            geo0 = Utils.asObjectOrNull(t1.next0_.get_referent(), GeoReferent)
            if (geo0 is not None and geo0.alpha2 == "RU"): 
                t1 = t1.next0_
        dep = OrganizationReferent()
        dep.add_type(typ, False)
        if (typ.name is not None): 
            nam = typ.name
            if (str.isdigit(nam[0])): 
                i = nam.find(' ')
                if (i > 0): 
                    dep.number = nam[0:0+i]
                    nam = nam[i + 1:].strip()
            dep.add_name(nam, True, None)
        ttt = (typ.root.canonic_text if typ.root is not None else typ.typ.upper())
        if ((((ttt == "ОТДЕЛЕНИЕ" or ttt == "ИНСПЕКЦИЯ" or ttt == "ВІДДІЛЕННЯ") or ttt == "ІНСПЕКЦІЯ")) and not t1.is_newline_after): 
            num = OrgItemNumberToken.try_attach(t1.next0_, False, typ)
            if (num is not None): 
                dep.number = num.number
                t1 = num.end_token
        if ("главное управление" in dep.types or "головне управління" in dep.types or "пограничное управление" in dep.type_name): 
            if (typ.begin_token == typ.end_token): 
                if (org0_.kind != OrganizationKind.GOVENMENT and org0_.kind != OrganizationKind.BANK): 
                    return None
        if (not OrgOwnershipHelper.can_be_higher(org0_, dep, False) and ((typ.root is None or not typ.root.can_be_normal_dep))): 
            if (len(dep.types) > 0 and dep.types[0] in org0_.types and dep.can_be_equals(org0_, ReferentsEqualType.FORMERGING)): 
                dep.merge_slots(org0_, False)
            elif (typ.typ == "управление" or typ.typ == "управління"): 
                dep.higher = org0_
            else: 
                return None
        else: 
            dep.higher = org0_
        res = ReferentToken(dep, typ.begin_token, t1)
        self.__correct_dep_attrs(res, typ, False)
        if (typ.root is not None and not typ.root.can_be_normal_dep and dep.number is None): 
            if (typ.name is not None and " " in typ.name): 
                pass
            elif (dep.find_slot(OrganizationReferent.ATTR_GEO, None, True) is not None): 
                pass
            elif (typ.root.coeff > 0 and typ.morph.number != MorphNumber.PLURAL): 
                pass
            elif (typ.typ == "управління" and typ.chars.is_capital_upper): 
                pass
            else: 
                return None
        return res
    
    def __try_attach_dep_after_org(self, typ : 'OrgItemTypeToken') -> 'ReferentToken':
        if (typ is None): 
            return None
        t = typ.begin_token.previous
        if (t is not None and t.is_char_of(":(")): 
            t = t.previous
        if (t is None): 
            return None
        org0_ = Utils.asObjectOrNull(t.get_referent(), OrganizationReferent)
        if (org0_ is None): 
            return None
        t1 = typ.end_token
        dep = OrganizationReferent()
        dep.add_type(typ, False)
        if (typ.name is not None): 
            dep.add_name(typ.name, True, None)
        if (OrgOwnershipHelper.can_be_higher(org0_, dep, False)): 
            dep.higher = org0_
        elif (OrgOwnershipHelper.can_be_higher(dep, org0_, False) and org0_.higher is None): 
            org0_.higher = dep
            t = t.next0_
        else: 
            t = t.next0_
        res = ReferentToken(dep, t, t1)
        self.__correct_dep_attrs(res, typ, False)
        if (dep.find_slot(OrganizationReferent.ATTR_GEO, None, True) is None): 
            return None
        return res
    
    def __try_attach_dep(self, typ : 'OrgItemTypeToken', attach_typ : 'AttachType', spec_word_before : bool) -> 'ReferentToken':
        from pullenti.ner.org.internal.OrgItemEponymToken import OrgItemEponymToken
        from pullenti.ner.org.internal.OrgItemNameToken import OrgItemNameToken
        if (typ is None): 
            return None
        after_org = None
        after_org_temp = False
        if ((typ.is_newline_after and typ.name is None and typ.typ != "курс") and ((typ.root is None or not typ.root.can_be_normal_dep))): 
            tt2 = typ.end_token.next0_
            if (not spec_word_before or tt2 is None): 
                return None
            if (BracketHelper.can_be_start_of_sequence(tt2, False, False)): 
                pass
            else: 
                return None
        if (typ.end_token.next0_ is not None and (typ.end_token.whitespaces_after_count < 2)): 
            na0 = OrgItemNameToken.try_attach(typ.end_token.next0_, None, False, True)
            in_br = False
            if (na0 is not None and ((na0.std_org_name_nouns > 0 or na0.is_std_name))): 
                spec_word_before = True
            else: 
                rt00 = self.__try_attach_org(typ.end_token.next0_, None, OrganizationAnalyzer.AttachType.NORMALAFTERDEP, None, False, 0, -1)
                if (rt00 is None and BracketHelper.can_be_start_of_sequence(typ.end_token.next0_, True, False)): 
                    rt00 = self.__try_attach_org(typ.end_token.next0_.next0_, None, OrganizationAnalyzer.AttachType.NORMALAFTERDEP, None, False, 0, -1)
                    if (rt00 is not None): 
                        in_br = True
                        if (rt00.end_token.next0_ is None): 
                            pass
                        elif (BracketHelper.can_be_end_of_sequence(rt00.end_token, True, None, False)): 
                            pass
                        elif (BracketHelper.can_be_end_of_sequence(rt00.end_token.next0_, True, None, False)): 
                            rt00.end_token = rt00.end_token.next0_
                        else: 
                            rt00 = (None)
                        if (rt00 is not None): 
                            rt00.begin_token = typ.end_token.next0_
                if (rt00 is not None): 
                    after_org = (Utils.asObjectOrNull(rt00.referent, OrganizationReferent))
                    spec_word_before = True
                    after_org_temp = True
                    if (after_org.contains_profile(OrgProfile.UNIT) and in_br): 
                        after_org = (None)
                        after_org_temp = False
                elif ((isinstance(typ.end_token.next0_, TextToken)) and typ.end_token.next0_.chars.is_all_upper): 
                    rrr = self.__try_attach_orgs(typ.end_token.next0_, None, 0)
                    if (rrr is not None and len(rrr) == 1): 
                        after_org = (Utils.asObjectOrNull(rrr[0].referent, OrganizationReferent))
                        spec_word_before = True
                        after_org_temp = True
        if (((((((typ.root is not None and typ.root.can_be_normal_dep and not spec_word_before) and typ.typ != "отделение" and typ.typ != "инспекция") and typ.typ != "филиал" and typ.typ != "аппарат") and typ.typ != "відділення" and typ.typ != "інспекція") and typ.typ != "філія" and typ.typ != "апарат") and typ.typ != "совет" and typ.typ != "рада") and (typ.typ.find(' ') < 0) and attach_typ != OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
            return None
        if (typ.morph.number == MorphNumber.PLURAL): 
            if (not typ.begin_token.is_value("ОСП", None)): 
                return None
        dep = None
        t0 = typ.begin_token
        t1 = typ.end_token
        dep = OrganizationReferent()
        dep.add_type_str(typ.typ.lower())
        dep.add_profile(OrgProfile.UNIT)
        if (typ.number is not None): 
            dep.number = typ.number
        elif (typ.typ == "курс" and not typ.is_newline_before): 
            nnn = NumberHelper.try_parse_roman_back(typ.begin_token.previous)
            if (nnn is not None and nnn.int_value is not None): 
                if (nnn.int_value >= 1 and nnn.int_value <= 6): 
                    dep.number = str(nnn.value)
                    t0 = nnn.begin_token
        t = typ.end_token.next0_
        t1 = typ.end_token
        if ((isinstance(t, TextToken)) and after_org is None and (((LanguageHelper.ends_with(typ.typ, "аппарат") or LanguageHelper.ends_with(typ.typ, "апарат") or LanguageHelper.ends_with(typ.typ, "совет")) or LanguageHelper.ends_with(typ.typ, "рада")))): 
            tt1 = t
            if (tt1.is_value("ПРИ", None)): 
                tt1 = tt1.next0_
            pr1 = t.kit.process_referent("PERSON", tt1)
            if (pr1 is not None and pr1.referent.type_name == "PERSONPROPERTY"): 
                dep.add_slot(OrganizationReferent.ATTR_OWNER, pr1.referent, True, 0)
                pr1.set_default_local_onto(t.kit.processor)
                dep.add_ext_referent(pr1)
                if (LanguageHelper.ends_with(typ.typ, "рат")): 
                    return ReferentToken(dep, t0, pr1.end_token)
                t1 = pr1.end_token
                t = t1.next0_
        before_org = None
        ttt = typ.begin_token.previous
        while ttt is not None: 
            if (isinstance(ttt.get_referent(), OrganizationReferent)): 
                before_org = ttt.get_referent()
                break
            elif (not (isinstance(ttt, TextToken))): 
                break
            elif (ttt.chars.is_letter): 
                break
            ttt = ttt.previous
        num = None
        names = None
        br = None
        br00 = None
        pr = None
        is_pure_org = False
        is_pure_dep = False
        if (typ.typ == "операционное управление" or typ.typ == "операційне управління"): 
            is_pure_dep = True
        after_org_tok = None
        br_name = None
        coef = typ.coef
        first_pass3840 = True
        while True:
            if first_pass3840: first_pass3840 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (after_org_temp): 
                break
            if (t.is_char(':')): 
                if (t.is_newline_after): 
                    break
                if (names is not None or typ.name is not None): 
                    break
                continue
            num = OrgItemNumberToken.try_attach(t, False, typ)
            if ((num) is not None): 
                if (t.is_newline_before or typ.number is not None): 
                    break
                if ((isinstance(typ.begin_token.previous, NumberToken)) and (typ.whitespaces_before_count < 2)): 
                    typ2 = OrgItemTypeToken.try_attach(num.end_token.next0_, True, None)
                    if (typ2 is not None and typ2.root is not None and ((typ2.root.can_has_number or typ2.is_dep))): 
                        typ.begin_token = typ.begin_token.previous
                        typ.number = typ.begin_token.value
                        dep.number = typ.number
                        num = (None)
                        coef += (1)
                        break
                t1 = num.end_token
                t = num.end_token.next0_
                break
            else: 
                ty0 = OrgItemTypeToken.try_attach(t, True, None)
                if ((ty0) is not None and ty0.morph.number != MorphNumber.PLURAL and not ty0.is_doubt_root_word): 
                    break
                else: 
                    br00 = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if ((br00) is not None and names is None): 
                        br = br00
                        if (not br.is_quote_type or br_name is not None): 
                            br = (None)
                        elif (t.is_newline_before and not spec_word_before): 
                            br = (None)
                        else: 
                            ok1 = True
                            tt = br.begin_token
                            while tt != br.end_token: 
                                if (isinstance(tt, ReferentToken)): 
                                    ok1 = False
                                    break
                                tt = tt.next0_
                            if (ok1): 
                                br_name = br
                                t1 = br.end_token
                                t = t1.next0_
                            else: 
                                br = (None)
                        break
                    else: 
                        r = t.get_referent()
                        if ((r is None and t.morph.class0_.is_preposition and t.next0_ is not None) and (isinstance(t.next0_.get_referent(), GeoReferent))): 
                            dep._add_geo_object(t.next0_.get_referent())
                            t = t.next0_
                            break
                        if (r is not None): 
                            if (isinstance(r, OrganizationReferent)): 
                                after_org = (Utils.asObjectOrNull(r, OrganizationReferent))
                                after_org_tok = t
                                break
                            if ((isinstance(r, GeoReferent)) and names is not None and t.previous is not None): 
                                is_name = False
                                if (t.previous.is_value("СУБЪЕКТ", None) or t.previous.is_value("СУБЄКТ", None)): 
                                    is_name = True
                                if (not is_name): 
                                    break
                            else: 
                                break
                        epo = OrgItemEponymToken.try_attach(t, True)
                        if (epo is not None): 
                            for e0_ in epo.eponyms: 
                                dep.add_eponym(e0_)
                            t1 = epo.end_token
                            break
                        if (not typ.chars.is_all_upper and t.chars.is_all_upper): 
                            na1 = OrgItemNameToken.try_attach(t, pr, attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY, False)
                            if (na1 is not None and ((na1.is_std_name or na1.std_org_name_nouns > 0))): 
                                pass
                            else: 
                                break
                        if ((isinstance(t, NumberToken)) and typ.root is not None and dep.number is None): 
                            if (t.whitespaces_before_count > 1): 
                                break
                            if ((isinstance(typ.begin_token.previous, NumberToken)) and (typ.whitespaces_before_count < 2)): 
                                typ2 = OrgItemTypeToken.try_attach(t.next0_, True, None)
                                if (typ2 is not None and typ2.root is not None and ((typ2.root.can_has_number or typ2.is_dep))): 
                                    typ.begin_token = typ.begin_token.previous
                                    typ.number = typ.begin_token.value
                                    dep.number = typ.number
                                    coef += (1)
                                    break
                            dep.number = str(t.value)
                            t1 = t
                            continue
                        if (is_pure_dep): 
                            break
                        if (not t.chars.is_all_lower): 
                            rtp = t.kit.process_referent("PERSON", t)
                            if (rtp is not None and rtp.referent.type_name == "PERSONPROPERTY"): 
                                if (rtp.morph.case_.is_genitive and t == typ.end_token.next0_ and (t.whitespaces_before_count < 4)): 
                                    rtp = (None)
                            if (rtp is not None): 
                                break
                        if (typ.typ == "генеральный штаб" or typ.typ == "генеральний штаб"): 
                            rtp = t.kit.process_referent("PERSONPROPERTY", t)
                            if (rtp is not None): 
                                break
                        na = OrgItemNameToken.try_attach(t, pr, attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY, names is None)
                        if (t.is_value("ПО", None) and t.next0_ is not None and t.next0_.is_value("РАЙОН", None)): 
                            na = OrgItemNameToken.try_attach(t.next0_.next0_, pr, attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY, True)
                        if (t.morph.class0_.is_preposition and ((t.is_value("ПРИ", None) or t.is_value("OF", None) or t.is_value("AT", None)))): 
                            if ((isinstance(t.next0_, ReferentToken)) and (isinstance(t.next0_.get_referent(), OrganizationReferent))): 
                                after_org = (Utils.asObjectOrNull(t.next0_.get_referent(), OrganizationReferent))
                                break
                            rt0 = self.__try_attach_org(t.next0_, None, OrganizationAnalyzer.AttachType.NORMALAFTERDEP, None, False, 0, -1)
                            if (rt0 is not None): 
                                after_org = (Utils.asObjectOrNull(rt0.referent, OrganizationReferent))
                                after_org_temp = True
                                break
                        if (na is None): 
                            break
                        if (names is None): 
                            if (t.is_newline_before): 
                                break
                            if (NumberHelper.try_parse_roman(t) is not None): 
                                break
                            rt0 = self.__try_attach_org(t, None, OrganizationAnalyzer.AttachType.NORMALAFTERDEP, None, False, 0, -1)
                            if (rt0 is not None): 
                                after_org = (Utils.asObjectOrNull(rt0.referent, OrganizationReferent))
                                after_org_temp = True
                                break
                            names = list()
                        else: 
                            if (t.whitespaces_before_count > 2 and na.chars != pr.chars): 
                                break
                            if (t.newlines_before_count > 2): 
                                break
                        names.append(na)
                        pr = na
                        t = na.end_token
                        t1 = t
        if (after_org is None): 
            ttt = t
            while ttt is not None: 
                if (isinstance(ttt.get_referent(), OrganizationReferent)): 
                    after_org = (Utils.asObjectOrNull(ttt.get_referent(), OrganizationReferent))
                    break
                elif (not (isinstance(ttt, TextToken))): 
                    break
                elif ((ttt.chars.is_letter and not ttt.is_value("ПРИ", None) and not ttt.is_value("В", None)) and not ttt.is_value("OF", None) and not ttt.is_value("AT", None)): 
                    break
                ttt = ttt.next0_
        if ((after_org is None and t is not None and t != t0) and (t.whitespaces_before_count < 2)): 
            rt0 = self.__try_attach_org(t, None, OrganizationAnalyzer.AttachType.NORMALAFTERDEP, None, False, 0, -1)
            if (rt0 is None and (((t.is_value("В", None) or t.is_value("ПРИ", None) or t.is_value("OF", None)) or t.is_value("AT", None)))): 
                rt0 = self.__try_attach_org(t.next0_, None, OrganizationAnalyzer.AttachType.NORMALAFTERDEP, None, False, 0, -1)
            if (rt0 is not None): 
                after_org = (Utils.asObjectOrNull(rt0.referent, OrganizationReferent))
                after_org_temp = True
        if (typ.chars.is_capital_upper): 
            coef += 0.5
        if (br is not None and names is None): 
            nam = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
            if (not Utils.isNullOrEmpty(nam)): 
                if (len(nam) > 100): 
                    return None
                coef += (3)
                na = OrgItemNameToken.try_attach(br.begin_token.next0_, None, False, True)
                if (na is not None and na.is_std_name): 
                    coef += (1)
                    if (typ.typ == "группа"): 
                        dep.slots.clear()
                        typ.typ = "группа компаний"
                        is_pure_org = True
                    elif (typ.typ == "група"): 
                        dep.slots.clear()
                        typ.typ = "група компаній"
                        is_pure_org = True
                if (is_pure_org): 
                    dep.add_type(typ, False)
                    dep.add_name(nam, True, None)
                else: 
                    dep.add_name_str(nam, typ, 1)
        elif (names is not None): 
            if (after_org is not None or attach_typ == OrganizationAnalyzer.AttachType.HIGH): 
                coef += (3)
                j = len(names)
            else: 
                j = 0
                while j < len(names): 
                    if (((names[j].is_newline_before and not typ.is_newline_before and not names[j].is_after_conjunction)) or ((names[j].chars != names[0].chars and names[j].std_org_name_nouns == 0))): 
                        break
                    else: 
                        if (names[j].chars == typ.chars and not typ.chars.is_all_lower): 
                            coef += (0.5)
                        if (names[j].is_std_name): 
                            coef += (2)
                        if (names[j].std_org_name_nouns > 0): 
                            if (not typ.chars.is_all_lower): 
                                coef += (names[j].std_org_name_nouns)
                    j += 1
            t1 = names[j - 1].end_token
            s = MiscHelper.get_text_value(names[0].begin_token, t1, GetTextAttr.NO)
            if (not Utils.isNullOrEmpty(s)): 
                if (len(s) > 150 and attach_typ != OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
                    return None
                dep.add_name_str(s, typ, 1)
            if (num is not None): 
                dep.number = num.number
                coef += (2)
                t1 = num.end_token
        elif (num is not None): 
            dep.number = num.number
            coef += (2)
            t1 = num.end_token
            if (typ is not None and ((typ.typ == "лаборатория" or typ.typ == "лабораторія"))): 
                coef += (1)
            if (typ.name is not None): 
                dep.add_name_str(None, typ, 1)
        elif (typ.name is not None): 
            if (typ.typ == "курс" and str.isdigit(typ.name[0])): 
                dep.number = typ.name[0:0+typ.name.find(' ')]
            else: 
                dep.add_name_str(None, typ, 1)
        elif (typ.typ == "кафедра" or typ.typ == "факультет"): 
            t = typ.end_token.next0_
            if (t is not None and t.is_char(':')): 
                t = t.next0_
            if ((t is not None and (isinstance(t, TextToken)) and not t.is_newline_before) and t.morph.class0_.is_adjective): 
                if (typ.morph.gender == t.morph.gender): 
                    s = t.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                    if (s is not None): 
                        dep.add_name_str("{0} {1}".format(s, typ.typ.upper()), None, 1)
                        coef += (2)
                        t1 = t
        elif (typ.typ == "курс"): 
            t = typ.end_token.next0_
            if (t is not None and t.is_char(':')): 
                t = t.next0_
            if (t is not None and not t.is_newline_before): 
                val = 0
                if (isinstance(t, NumberToken)): 
                    if (not t.morph.class0_.is_noun and t.int_value is not None): 
                        if (t.is_whitespace_after or t.next0_.is_char_of(";,")): 
                            val = t.int_value
                else: 
                    nt = NumberHelper.try_parse_roman(t)
                    if (nt is not None and nt.int_value is not None): 
                        val = nt.int_value
                        t = nt.end_token
                if (val > 0 and (val < 8)): 
                    dep.number = str(val)
                    t1 = t
                    coef += (4)
            if (dep.number is None): 
                t = typ.begin_token.previous
                if (t is not None and not t.is_newline_after): 
                    val = 0
                    if (isinstance(t, NumberToken)): 
                        if (not t.morph.class0_.is_noun and t.int_value is not None): 
                            if (t.is_whitespace_before or t.previous.is_char_of(",")): 
                                val = t.int_value
                    else: 
                        nt = NumberHelper.try_parse_roman_back(t)
                        if (nt is not None and nt.int_value is not None): 
                            val = nt.int_value
                            t = nt.begin_token
                    if (val > 0 and (val < 8)): 
                        dep.number = str(val)
                        t0 = t
                        coef += (4)
        elif (typ.root is not None and typ.root.can_be_normal_dep and after_org is not None): 
            coef += (3)
            if (not after_org_temp): 
                dep.higher = Utils.asObjectOrNull(after_org, OrganizationReferent)
            else: 
                dep._m_temp_parent_org = (Utils.asObjectOrNull(after_org, OrganizationReferent))
            if (after_org_tok is not None): 
                t1 = after_org_tok
        elif (typ.typ == "генеральный штаб" or typ.typ == "генеральний штаб"): 
            coef += (3)
        if (before_org is not None): 
            coef += (1)
        if (after_org is not None): 
            coef += (2)
            if (((typ.name is not None or ((typ.root is not None and typ.root.can_be_normal_dep)))) and OrgOwnershipHelper.can_be_higher(Utils.asObjectOrNull(after_org, OrganizationReferent), dep, False)): 
                coef += (1)
                if (not typ.chars.is_all_lower): 
                    coef += 0.5
        if (typ.typ == "курс" or typ.typ == "группа" or typ.typ == "група"): 
            if (dep.number is None): 
                coef = (0)
            elif (typ.typ == "курс"): 
                wrapn2363 = RefOutArgWrapper(0)
                inoutres2364 = Utils.tryParseInt(dep.number, wrapn2363)
                n = wrapn2363.value
                if (inoutres2364): 
                    if (n > 0 and (n < 9)): 
                        coef += (2)
        if (t1.next0_ is not None and t1.next0_.is_char('(')): 
            ttt = t1.next0_.next0_
            if ((ttt is not None and ttt.next0_ is not None and ttt.next0_.is_char(')')) and (isinstance(ttt, TextToken))): 
                if (ttt.term in dep._name_vars): 
                    coef += (2)
                    dep.add_name(ttt.term, True, ttt)
                    t1 = ttt.next0_
        ep = OrgItemEponymToken.try_attach(t1.next0_, False)
        if (ep is not None): 
            coef += (2)
            for e0_ in ep.eponyms: 
                dep.add_eponym(e0_)
            t1 = ep.end_token
        if (br_name is not None): 
            str1 = MiscHelper.get_text_value(br_name.begin_token.next0_, br_name.end_token.previous, GetTextAttr.NO)
            if (str1 is not None): 
                dep.add_name(str1, True, None)
        if (len(dep.slots) == 0): 
            return None
        res = ReferentToken(dep, t0, t1)
        self.__correct_dep_attrs(res, typ, after_org_temp)
        if (dep.number is not None): 
            coef += (2)
        if (is_pure_dep): 
            coef += (2)
        if (spec_word_before): 
            if (dep.find_slot(OrganizationReferent.ATTR_NAME, None, True) is not None): 
                coef += (2)
        if (coef > 3 or attach_typ == OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
            return res
        else: 
            return None
    
    def __correct_dep_attrs(self, res : 'ReferentToken', typ : 'OrgItemTypeToken', after_temp_org : bool=False) -> None:
        t0 = res.begin_token
        dep = Utils.asObjectOrNull(res.referent, OrganizationReferent)
        if ((((((((typ is not None and typ.root is not None and typ.root.can_has_number)) or "офис" in dep.types or "офіс" in dep.types) or "отдел" in dep.types or "отделение" in dep.types) or "инспекция" in dep.types or "лаборатория" in dep.types) or "управление" in dep.types or "управління" in dep.types) or "відділ" in dep.types or "відділення" in dep.types) or "інспекція" in dep.types or "лабораторія" in dep.types): 
            if (((isinstance(t0.previous, NumberToken)) and (t0.whitespaces_before_count < 3) and not t0.previous.morph.class0_.is_noun) and t0.previous.is_whitespace_before): 
                nn = str(t0.previous.value)
                if (dep.number is None or dep.number == nn): 
                    dep.number = nn
                    t0 = t0.previous
                    res.begin_token = t0
            if (MiscHelper.check_number_prefix(res.end_token.next0_) is not None and (res.end_token.whitespaces_after_count < 3) and dep.number is None): 
                num = OrgItemNumberToken.try_attach(res.end_token.next0_, False, typ)
                if (num is not None): 
                    dep.number = num.number
                    res.end_token = num.end_token
        if ("управление" in dep.types or "департамент" in dep.types or "управління" in dep.types): 
            for s in dep.slots: 
                if (s.type_name == OrganizationReferent.ATTR_GEO and (isinstance(s.value, GeoReferent))): 
                    g = Utils.asObjectOrNull(s.value, GeoReferent)
                    if (g.is_state and g.alpha2 == "RU"): 
                        dep.slots.remove(s)
                        break
        t1 = res.end_token
        if (t1.next0_ is None or after_temp_org): 
            return
        br = BracketHelper.try_parse(t1.next0_, BracketParseAttr.NO, 100)
        if (br is not None and (t1.whitespaces_after_count < 2) and br.is_quote_type): 
            g = self.__is_geo(br.begin_token.next0_, False)
            if (isinstance(g, ReferentToken)): 
                if (g.end_token.next0_ == br.end_token): 
                    dep._add_geo_object(g)
                    res.end_token = br.end_token
                    t1 = res.end_token
            elif ((isinstance(g, Referent)) and br.begin_token.next0_.next0_ == br.end_token): 
                dep._add_geo_object(g)
                res.end_token = br.end_token
                t1 = res.end_token
            elif (br.begin_token.next0_.is_value("О", None) or br.begin_token.next0_.is_value("ОБ", None)): 
                pass
            else: 
                nam = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                if (nam is not None): 
                    dep.add_name(nam, True, br.begin_token.next0_)
                    res.end_token = br.end_token
                    t1 = res.end_token
        prep = False
        if (t1.next0_ is not None): 
            if (t1.next0_.morph.class0_.is_preposition): 
                if (t1.next0_.is_value("В", None) or t1.next0_.is_value("ПО", None)): 
                    t1 = t1.next0_
                    prep = True
            if (t1.next0_ is not None and (t1.next0_.whitespaces_before_count < 3)): 
                if (t1.next0_.is_value("НА", None) and t1.next0_.next0_ is not None and t1.next0_.next0_.is_value("ТРАНСПОРТ", None)): 
                    t1 = t1.next0_.next0_
                    res.end_token = t1
        for k in range(2):
            if (t1.next0_ is None): 
                return
            geo_ = Utils.asObjectOrNull(t1.next0_.get_referent(), GeoReferent)
            ge = False
            if (geo_ is not None): 
                if (not dep._add_geo_object(geo_)): 
                    return
                res.end_token = t1.next0_
                ge = True
            else: 
                rgeo = t1.kit.process_referent("GEO", t1.next0_)
                if (rgeo is not None): 
                    if (not rgeo.morph.class0_.is_adjective): 
                        if (not dep._add_geo_object(rgeo)): 
                            return
                        res.end_token = rgeo.end_token
                        ge = True
            if (not ge): 
                return
            t1 = res.end_token
            if (t1.next0_ is None): 
                return
            is_and = False
            if (t1.next0_.is_and): 
                t1 = t1.next0_
            if (t1 is None): 
                return
    
    def __attach_global_org(self, t : 'Token', attach_typ : 'AttachType', ad : 'AnalyzerData', ext_geo : object=None) -> 'ReferentToken':
        from pullenti.ner.org.internal.OrgItemEponymToken import OrgItemEponymToken
        from pullenti.ner.org.internal.OrgItemNameToken import OrgItemNameToken
        if ((isinstance(t, TextToken)) and t.chars.is_latin_letter): 
            if (MiscHelper.is_eng_article(t)): 
                res11 = self.__attach_global_org(t.next0_, attach_typ, ad, ext_geo)
                if (res11 is not None): 
                    res11.begin_token = t
                    return res11
        rt00 = self.__try_attach_politic_party(t, Utils.asObjectOrNull(ad, OrganizationAnalyzer.OrgAnalyzerData), True)
        if (rt00 is not None): 
            return rt00
        if (not (isinstance(t, TextToken))): 
            if (t is not None and t.get_referent() is not None and t.get_referent().type_name == "URI"): 
                rt = self.__attach_global_org(t.begin_token, attach_typ, ad, None)
                if (rt is not None and rt.end_char == t.end_char): 
                    rt.begin_token = rt.end_token = t
                    return rt
            return None
        term = t.term
        if (t.chars.is_all_upper and term == "ВС"): 
            if (t.previous is not None): 
                if (t.previous.is_value("ПРЕЗИДИУМ", None) or t.previous.is_value("ПЛЕНУМ", None) or t.previous.is_value("СЕССИЯ", None)): 
                    org00 = OrganizationReferent()
                    org00.add_name("ВЕРХОВНЫЙ СОВЕТ", True, None)
                    org00.add_name("ВС", True, None)
                    org00.add_type_str("совет")
                    org00.add_profile(OrgProfile.STATE)
                    te = self.__attach_tail_attributes(org00, t.next0_, None, False, OrganizationAnalyzer.AttachType.NORMAL, True)
                    return ReferentToken(org00, t, Utils.ifNotNull(te, t))
            if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent))): 
                is_vc = False
                if (t.previous is not None and (isinstance(t.previous.get_referent(), OrganizationReferent)) and t.previous.get_referent().kind == OrganizationKind.MILITARY): 
                    is_vc = True
                elif (ad is not None): 
                    for r in ad.referents: 
                        if (r.find_slot(OrganizationReferent.ATTR_NAME, "ВООРУЖЕННЫЕ СИЛЫ", True) is not None): 
                            is_vc = True
                            break
                if (is_vc): 
                    org00 = OrganizationReferent()
                    org00.add_name("ВООРУЖЕННЫЕ СИЛЫ", True, None)
                    org00.add_name("ВС", True, None)
                    org00.add_type_str("армия")
                    org00.add_profile(OrgProfile.ARMY)
                    te = self.__attach_tail_attributes(org00, t.next0_, None, False, OrganizationAnalyzer.AttachType.NORMAL, True)
                    return ReferentToken(org00, t, Utils.ifNotNull(te, t))
        if ((t.chars.is_all_upper and ((term == "АН" or term == "ВАС")) and t.next0_ is not None) and (isinstance(t.next0_.get_referent(), GeoReferent))): 
            org00 = OrganizationReferent()
            if (term == "АН"): 
                org00.add_name("АКАДЕМИЯ НАУК", True, None)
                org00.add_type_str("академия")
                org00.add_profile(OrgProfile.SCIENCE)
            else: 
                org00.add_name("ВЫСШИЙ АРБИТРАЖНЫЙ СУД", True, None)
                org00.add_name("ВАС", True, None)
                org00.add_type_str("суд")
                org00.add_profile(OrgProfile.JUSTICE)
            te = self.__attach_tail_attributes(org00, t.next0_, None, False, OrganizationAnalyzer.AttachType.NORMAL, True)
            return ReferentToken(org00, t, Utils.ifNotNull(te, t))
        if (t.chars.is_all_upper and term == "ГД" and t.previous is not None): 
            rt = t.kit.process_referent("PERSONPROPERTY", t.previous)
            if (rt is not None and rt.referent is not None and rt.referent.type_name == "PERSONPROPERTY"): 
                org00 = OrganizationReferent()
                org00.add_name("ГОСУДАРСТВЕННАЯ ДУМА", True, None)
                org00.add_name("ГОСДУМА", True, None)
                org00.add_name("ГД", True, None)
                org00.add_type_str("парламент")
                org00.add_profile(OrgProfile.STATE)
                te = self.__attach_tail_attributes(org00, t.next0_, None, False, OrganizationAnalyzer.AttachType.NORMAL, True)
                return ReferentToken(org00, t, Utils.ifNotNull(te, t))
        if (t.chars.is_all_upper and term == "МЮ"): 
            ok = False
            if ((t.previous is not None and t.previous.is_value("В", None) and t.previous.previous is not None) and t.previous.previous.is_value("ЗАРЕГИСТРИРОВАТЬ", None)): 
                ok = True
            elif (t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent))): 
                ok = True
            if (ok): 
                org00 = OrganizationReferent()
                org00.add_type_str("министерство")
                org00.add_profile(OrgProfile.STATE)
                org00.add_name("МИНИСТЕРСТВО ЮСТИЦИИ", True, None)
                org00.add_name("МИНЮСТ", True, None)
                t1 = t
                if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent))): 
                    t1 = t.next0_
                    org00._add_geo_object(t1.get_referent())
                return ReferentToken(org00, t, t1)
        if (t.chars.is_all_upper and term == "ФС"): 
            if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent))): 
                org00 = OrganizationReferent()
                org00.add_type_str("парламент")
                org00.add_profile(OrgProfile.STATE)
                org00.add_name("ФЕДЕРАЛЬНОЕ СОБРАНИЕ", True, None)
                org00._add_geo_object(t.next0_.get_referent())
                return ReferentToken(org00, t, t.next0_)
        if (t.chars.is_all_upper and term == "МП"): 
            tt0 = t.previous
            if (tt0 is not None and tt0.is_char('(')): 
                tt0 = tt0.previous
            org0 = None
            prev = False
            if (tt0 is not None): 
                org0 = (Utils.asObjectOrNull(tt0.get_referent(), OrganizationReferent))
                if (org0 is not None): 
                    prev = True
            if (t.next0_ is not None and org0 is None): 
                org0 = (Utils.asObjectOrNull(t.next0_.get_referent(), OrganizationReferent))
            if (org0 is not None and org0.kind == OrganizationKind.CHURCH): 
                glob = OrganizationReferent()
                glob.add_type_str("патриархия")
                glob.add_name("МОСКОВСКАЯ ПАТРИАРХИЯ", True, None)
                glob.higher = org0
                glob.add_profile(OrgProfile.RELIGION)
                res = ReferentToken(glob, t, t)
                if (not prev): 
                    res.end_token = t.next0_
                else: 
                    res.begin_token = tt0
                    if (tt0 != t.previous and res.end_token.next0_ is not None and res.end_token.next0_.is_char(')')): 
                        res.end_token = res.end_token.next0_
                return res
        if (t.chars.is_all_upper and term == "ГШ"): 
            if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), OrganizationReferent)) and t.next0_.get_referent().kind == OrganizationKind.MILITARY): 
                org00 = OrganizationReferent()
                org00.add_type_str("генеральный штаб")
                org00.add_profile(OrgProfile.ARMY)
                org00.higher = Utils.asObjectOrNull(t.next0_.get_referent(), OrganizationReferent)
                return ReferentToken(org00, t, t.next0_)
        if (t.chars.is_all_upper and term == "ЗС"): 
            if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent))): 
                org00 = OrganizationReferent()
                org00.add_type_str("парламент")
                org00.add_profile(OrgProfile.STATE)
                org00.add_name("ЗАКОНОДАТЕЛЬНОЕ СОБРАНИЕ", True, None)
                org00._add_geo_object(t.next0_.get_referent())
                return ReferentToken(org00, t, t.next0_)
        if (t.chars.is_all_upper and term == "СФ"): 
            t.inner_bool = True
            if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent))): 
                org00 = OrganizationReferent()
                org00.add_type_str("совет")
                org00.add_profile(OrgProfile.STATE)
                org00.add_name("СОВЕТ ФЕДЕРАЦИИ", True, None)
                org00._add_geo_object(t.next0_.get_referent())
                return ReferentToken(org00, t, t.next0_)
            if (t.next0_ is not None): 
                if (t.next0_.is_value("ФС", None) or (((isinstance(t.next0_.get_referent(), OrganizationReferent)) and t.next0_.get_referent().find_slot(OrganizationReferent.ATTR_NAME, "ФЕДЕРАЛЬНОЕ СОБРАНИЕ", True) is not None))): 
                    org00 = OrganizationReferent()
                    org00.add_type_str("совет")
                    org00.add_profile(OrgProfile.STATE)
                    org00.add_name("СОВЕТ ФЕДЕРАЦИИ", True, None)
                    return ReferentToken(org00, t, t)
        if (t.chars.is_all_upper and term == "ФК"): 
            if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent))): 
                org00 = OrganizationReferent()
                org00.add_type_str("казначейство")
                org00.add_profile(OrgProfile.FINANCE)
                org00.add_name("ФЕДЕРАЛЬНОЕ КАЗНАЧЕЙСТВО", True, None)
                org00._add_geo_object(t.next0_.get_referent())
                return ReferentToken(org00, t, t.next0_)
            if (attach_typ == OrganizationAnalyzer.AttachType.NORMALAFTERDEP): 
                org00 = OrganizationReferent()
                org00.add_type_str("казначейство")
                org00.add_profile(OrgProfile.FINANCE)
                org00.add_name("ФЕДЕРАЛЬНОЕ КАЗНАЧЕЙСТВО", True, None)
                return ReferentToken(org00, t, t)
        if (t.chars.is_all_upper and ((term == "СК" or term == "CK"))): 
            if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent))): 
                tt = t.previous
                first_pass3841 = True
                while True:
                    if first_pass3841: first_pass3841 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (isinstance(tt, TextToken)): 
                        if (tt.is_comma_and): 
                            continue
                        if (isinstance(tt, NumberToken)): 
                            continue
                        if (not tt.chars.is_letter): 
                            continue
                        if ((tt.is_value("ЧАСТЬ", None) or tt.is_value("СТАТЬЯ", None) or tt.is_value("ПУНКТ", None)) or tt.is_value("СТ", None) or tt.is_value("П", None)): 
                            return None
                        break
                org00 = OrganizationReferent()
                org00.add_type_str("комитет")
                org00.add_profile(OrgProfile.UNIT)
                org00.add_name("СЛЕДСТВЕННЫЙ КОМИТЕТ", True, None)
                org00._add_geo_object(t.next0_.get_referent())
                return ReferentToken(org00, t, t.next0_)
            gt1 = OrgGlobal.GLOBAL_ORGS.try_attach(t.next0_, None, False)
            if (gt1 is None and t.next0_ is not None and t.kit.base_language.is_ua): 
                gt1 = OrgGlobal.GLOBAL_ORGS_UA.try_attach(t.next0_, None, False)
            ok = False
            if (gt1 is not None and gt1[0].item.referent.find_slot(OrganizationReferent.ATTR_NAME, "МВД", True) is not None): 
                ok = True
            if (ok): 
                org00 = OrganizationReferent()
                org00.add_type_str("комитет")
                org00.add_name("СЛЕДСТВЕННЫЙ КОМИТЕТ", True, None)
                org00.add_profile(OrgProfile.UNIT)
                return ReferentToken(org00, t, t)
        gt = OrgGlobal.GLOBAL_ORGS.try_attach(t, None, True)
        if (gt is None): 
            gt = OrgGlobal.GLOBAL_ORGS.try_attach(t, None, False)
        if (gt is None and t is not None and t.kit.base_language.is_ua): 
            gt = OrgGlobal.GLOBAL_ORGS_UA.try_attach(t, None, True)
            if (gt is None): 
                gt = OrgGlobal.GLOBAL_ORGS_UA.try_attach(t, None, False)
        if (gt is None): 
            return None
        for ot in gt: 
            org0 = Utils.asObjectOrNull(ot.item.referent, OrganizationReferent)
            if (org0 is None): 
                continue
            if (ot.begin_token == ot.end_token): 
                if (len(gt) == 1): 
                    if ((isinstance(ot.begin_token, TextToken)) and ot.begin_token.term == "МГТУ"): 
                        ty = OrgItemTypeToken.try_attach(ot.begin_token, False, None)
                        if (ty is not None): 
                            continue
                else: 
                    if (ad is None): 
                        return None
                    ok = False
                    for o in ad.referents: 
                        if (o.can_be_equals(org0, ReferentsEqualType.DIFFERENTTEXTS)): 
                            ok = True
                            break
                    if (not ok): 
                        return None
            if (((t.chars.is_all_lower and attach_typ != OrganizationAnalyzer.AttachType.EXTONTOLOGY and ext_geo is None) and not t.is_value("МИД", None) and not org0._types_contains("факультет")) and org0.kind != OrganizationKind.JUSTICE): 
                if (ot.begin_token == ot.end_token): 
                    continue
                if (ot.morph.number == MorphNumber.PLURAL): 
                    continue
                tyty = OrgItemTypeToken.try_attach(t, True, None)
                if (tyty is not None and tyty.end_token == ot.end_token): 
                    continue
                if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent))): 
                    pass
                elif (OrgItemTypeToken.check_org_special_word_before(t.previous)): 
                    pass
                else: 
                    continue
            if ((ot.begin_token == ot.end_token and (t.length_char < 6) and not t.chars.is_all_upper) and not t.chars.is_last_lower): 
                if (org0.find_slot(OrganizationReferent.ATTR_NAME, t.term, True) is None): 
                    if (t.is_value("МИД", None)): 
                        pass
                    else: 
                        continue
                elif (t.chars.is_all_lower): 
                    continue
                elif (t.length_char < 3): 
                    continue
                elif (t.length_char == 4): 
                    has_vow = False
                    for ch in t.term: 
                        if (LanguageHelper.is_cyrillic_vowel(ch) or LanguageHelper.is_latin_vowel(ch)): 
                            has_vow = True
                    if (has_vow): 
                        continue
            if (ot.begin_token == ot.end_token and term == "МЭР"): 
                continue
            if (ot.begin_token == ot.end_token): 
                if (t.previous is None or t.is_whitespace_before): 
                    pass
                elif ((isinstance(t.previous, TextToken)) and ((t.previous.is_char_of(",:") or BracketHelper.can_be_start_of_sequence(t.previous, False, False)))): 
                    pass
                elif (t.get_morph_class_in_dictionary().is_undefined and t.chars.is_capital_upper): 
                    pass
                else: 
                    continue
                if (t.next0_ is None or t.is_whitespace_after): 
                    pass
                elif ((isinstance(t.next0_, TextToken)) and ((t.next0_.is_char_of(",.") or BracketHelper.can_be_end_of_sequence(t.next0_, False, None, False)))): 
                    pass
                elif (t.get_morph_class_in_dictionary().is_undefined and t.chars.is_capital_upper): 
                    pass
                else: 
                    continue
                if (isinstance(t, TextToken)): 
                    has_name = False
                    for n in org0.names: 
                        if (t.is_value(n, None)): 
                            has_name = True
                            break
                    if (not has_name): 
                        continue
                    if (t.length_char < 3): 
                        ok1 = True
                        if (t.next0_ is not None and not t.is_newline_before): 
                            if (MiscHelper.check_number_prefix(t.next0_) is not None): 
                                ok1 = False
                            elif (t.next0_.is_hiphen or (isinstance(t.next0_, NumberToken))): 
                                ok1 = False
                        if (not ok1): 
                            continue
                rt = t.kit.process_referent("TRANSPORT", t)
                if (rt is not None): 
                    continue
            org0_ = None
            if (isinstance(t, TextToken)): 
                if ((t.is_value("ДЕПАРТАМЕНТ", None) or t.is_value("КОМИТЕТ", "КОМІТЕТ") or t.is_value("МИНИСТЕРСТВО", "МІНІСТЕРСТВО")) or t.is_value("КОМИССИЯ", "КОМІСІЯ")): 
                    nnn = OrgItemNameToken.try_attach(t.next0_, None, True, True)
                    if (nnn is not None and nnn.end_char > ot.end_char): 
                        org0_ = OrganizationReferent()
                        for p in org0.profiles: 
                            org0_.add_profile(p)
                        org0_.add_type_str(t.lemma.lower())
                        org0_.add_name(MiscHelper.get_text_value(t, nnn.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE), True, None)
                        ot.end_token = nnn.end_token
            if (org0_ is None): 
                org0_ = (Utils.asObjectOrNull(org0.clone(), OrganizationReferent))
                if (len(org0_.geo_objects) > 0): 
                    for s in org0_.slots: 
                        if (s.type_name == OrganizationReferent.ATTR_GEO and (isinstance(s.value, GeoReferent))): 
                            gg = s.value.clone()
                            gg.occurrence.clear()
                            rtg = ReferentToken(gg, t, t)
                            rtg.data = t.kit.get_analyzer_data_by_analyzer_name("GEO")
                            org0_.slots.remove(s)
                            org0_._add_geo_object(rtg)
                            break
                org0_.add_name(ot.termin.canonic_text, True, None)
            if (ext_geo is not None): 
                org0_._add_geo_object(ext_geo)
            org0_.is_from_global_ontos = True
            tt = ot.begin_token
            while tt is not None and (tt.end_char < ot.end_char): 
                if (isinstance(tt.get_referent(), GeoReferent)): 
                    org0_._add_geo_object(tt)
                    break
                tt = tt.next0_
            if ((isinstance(t.previous, TextToken)) and (t.whitespaces_before_count < 2) and t.previous.morph.class0_.is_adjective): 
                gg = t.kit.process_referent("GEO", t.previous)
                if (gg is not None and gg.morph.class0_.is_adjective): 
                    t = t.previous
                    org0_._add_geo_object(gg)
            t1 = None
            if (not "академия" in org0.types and attach_typ != OrganizationAnalyzer.AttachType.NORMALAFTERDEP and attach_typ != OrganizationAnalyzer.AttachType.EXTONTOLOGY): 
                t1 = self.__attach_tail_attributes(org0_, ot.end_token.next0_, None, False, OrganizationAnalyzer.AttachType.NORMAL, True)
            elif (((((("министерство" in org0.types or "парламент" in org0.types or "совет" in org0.types) or org0.kind == OrganizationKind.SCIENCE or org0.kind == OrganizationKind.GOVENMENT) or org0.kind == OrganizationKind.STUDY or org0.kind == OrganizationKind.JUSTICE) or org0.kind == OrganizationKind.MILITARY)) and (isinstance(ot.end_token.next0_, ReferentToken))): 
                geo_ = Utils.asObjectOrNull(ot.end_token.next0_.get_referent(), GeoReferent)
                if (geo_ is not None and geo_.is_state): 
                    org0_._add_geo_object(geo_)
                    t1 = ot.end_token.next0_
            if (t1 is None): 
                t1 = ot.end_token
            epp = OrgItemEponymToken.try_attach(t1.next0_, False)
            if (epp is not None): 
                exi = False
                for v in epp.eponyms: 
                    if (org0_.find_slot(OrganizationReferent.ATTR_EPONYM, v, True) is not None): 
                        exi = True
                        break
                if (not exi): 
                    for i in range(len(org0_.slots) - 1, -1, -1):
                        if (org0_.slots[i].type_name == OrganizationReferent.ATTR_EPONYM): 
                            del org0_.slots[i]
                    for vv in epp.eponyms: 
                        org0_.add_eponym(vv)
                t1 = epp.end_token
            if (t1.whitespaces_after_count < 2): 
                typ = OrgItemTypeToken.try_attach(t1.next0_, False, None)
                if (typ is not None): 
                    if (OrgItemTypeToken.is_type_accords(org0_, typ)): 
                        if (typ.chars.is_latin_letter and typ.root is not None and typ.root.can_be_normal_dep): 
                            pass
                        else: 
                            org0_.add_type(typ, False)
                            t1 = typ.end_token
            if (len(org0_.geo_objects) == 0 and t.previous is not None and t.previous.morph.class0_.is_adjective): 
                grt = t.kit.process_referent("GEO", t.previous)
                if (grt is not None and grt.end_token.next0_ == t): 
                    org0_._add_geo_object(grt)
                    t = t.previous
            if (org0_.find_slot(OrganizationReferent.ATTR_NAME, "ВТБ", True) is not None and t1.next0_ is not None): 
                tt = t1.next0_
                if (tt.is_hiphen and tt.next0_ is not None): 
                    tt = tt.next0_
                if (isinstance(tt, NumberToken)): 
                    org0_.number = str(tt.value)
                    t1 = tt
            if (not t.is_whitespace_before and not t1.is_whitespace_after): 
                if (BracketHelper.can_be_start_of_sequence(t.previous, True, False) and BracketHelper.can_be_end_of_sequence(t1.next0_, True, None, False)): 
                    t = t.previous
                    t1 = t1.next0_
            return ReferentToken(org0_, t, t1)
        return None
    
    @staticmethod
    def __try_attach_org_med_typ(t : 'Token') -> 'MetaToken':
        if (not (isinstance(t, TextToken))): 
            return None
        s = t.term
        if (((t is not None and s == "Г" and t.next0_ is not None) and t.next0_.is_char_of("\\/.") and t.next0_.next0_ is not None) and t.next0_.next0_.is_value("Б", None)): 
            t1 = t.next0_.next0_
            if (t.next0_.is_char('.') and t1.next0_ is not None and t1.next0_.is_char('.')): 
                t1 = t1.next0_
            return MetaToken._new2366(t, t1, "городская больница", MorphCollection._new2365(MorphGender.FEMINIE))
        if ((s == "ИН" and t.next0_ is not None and t.next0_.is_hiphen) and t.next0_.next0_ is not None and t.next0_.next0_.is_value("Т", None)): 
            return MetaToken._new2366(t, t.next0_.next0_, "институт", MorphCollection._new2365(MorphGender.MASCULINE))
        if ((s == "Б" and t.next0_ is not None and t.next0_.is_hiphen) and (isinstance(t.next0_.next0_, TextToken)) and ((t.next0_.next0_.is_value("ЦА", None) or t.next0_.next0_.is_value("ЦУ", None)))): 
            return MetaToken._new2366(t, t.next0_.next0_, "больница", MorphCollection._new2365(MorphGender.FEMINIE))
        if (s == "ГКБ"): 
            return MetaToken._new2366(t, t, "городская клиническая больница", MorphCollection._new2365(MorphGender.FEMINIE))
        if (t.is_value("ПОЛИКЛИНИКА", None)): 
            return MetaToken._new2366(t, t, "поликлиника", MorphCollection._new2365(MorphGender.FEMINIE))
        if (t.is_value("БОЛЬНИЦА", None)): 
            return MetaToken._new2366(t, t, "больница", MorphCollection._new2365(MorphGender.FEMINIE))
        if (t.is_value("ДЕТСКИЙ", None)): 
            mt = OrganizationAnalyzer.__try_attach_org_med_typ(t.next0_)
            if (mt is not None): 
                mt.begin_token = t
                mt.tag = ("{0} {1}".format(("детская" if mt.morph.gender == MorphGender.FEMINIE else "детский"), mt.tag))
                return mt
        return None
    
    def __try_attach_org_med(self, t : 'Token', ad : 'OrgAnalyzerData') -> 'ReferentToken':
        from pullenti.ner.org.internal.OrgItemEponymToken import OrgItemEponymToken
        if (t is None): 
            return None
        if (t.previous is None or t.previous.previous is None): 
            return None
        if ((t.previous.morph.class0_.is_preposition and t.previous.previous.is_value("ДОСТАВИТЬ", None)) or t.previous.previous.is_value("ПОСТУПИТЬ", None)): 
            pass
        else: 
            return None
        if (t.is_value("ТРАВМПУНКТ", None)): 
            t = t.next0_
        elif (t.is_value("ТРАВМ", None)): 
            if ((t.next0_ is not None and t.next0_.is_char('.') and t.next0_.next0_ is not None) and t.next0_.next0_.is_value("ПУНКТ", None)): 
                t = t.next0_.next0_.next0_
        if (isinstance(t, NumberToken)): 
            tt = OrganizationAnalyzer.__try_attach_org_med_typ(t.next0_)
            if (tt is not None): 
                org1 = OrganizationReferent()
                org1.add_type_str(tt.tag.lower())
                org1.number = str(t.value)
                return ReferentToken(org1, t, tt.end_token)
        typ = OrganizationAnalyzer.__try_attach_org_med_typ(t)
        adj = None
        if (typ is None and t.chars.is_capital_upper and t.morph.class0_.is_adjective): 
            typ = OrganizationAnalyzer.__try_attach_org_med_typ(t.next0_)
            if (typ is not None): 
                adj = t.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, typ.morph.gender, False)
        if (typ is None): 
            return None
        org0_ = OrganizationReferent()
        s = Utils.asObjectOrNull(typ.tag, str)
        org0_.add_type_str(s.lower())
        if (adj is not None): 
            org0_.add_name("{0} {1}".format(adj, s.upper()), True, None)
        t1 = typ.end_token
        epo = OrgItemEponymToken.try_attach(t1.next0_, False)
        if (epo is not None): 
            for v in epo.eponyms: 
                org0_.add_eponym(v)
            t1 = epo.end_token
        if (isinstance(t1.next0_, TextToken)): 
            if (t1.next0_.is_value("СКЛИФОСОФСКОГО", None) or t1.next0_.is_value("СЕРБСКОГО", None) or t1.next0_.is_value("БОТКИНА", None)): 
                org0_.add_eponym(t1.next0_.term)
                t1 = t1.next0_
        num = OrgItemNumberToken.try_attach(t1.next0_, False, None)
        if (num is not None): 
            org0_.number = num.number
            t1 = num.end_token
        if (len(org0_.slots) > 1): 
            return ReferentToken(org0_, t, t1)
        return None
    
    def __try_attach_prop_names(self, t : 'Token', ad : 'OrgAnalyzerData') -> 'ReferentToken':
        rt = self.__try_attach_org_sport_associations(t, ad)
        if (rt is None): 
            rt = self.__try_attach_org_names(t, ad)
        if (rt is None): 
            return None
        t0 = rt.begin_token.previous
        if ((isinstance(t0, TextToken)) and (t0.whitespaces_after_count < 2) and t0.morph.class0_.is_adjective): 
            rt0 = t0.kit.process_referent("GEO", t0)
            if (rt0 is not None and rt0.morph.class0_.is_adjective): 
                rt.begin_token = rt0.begin_token
                rt.referent._add_geo_object(rt0)
        if (rt.end_token.whitespaces_after_count < 2): 
            tt1 = self.__attach_tail_attributes(Utils.asObjectOrNull(rt.referent, OrganizationReferent), rt.end_token.next0_, ad, True, OrganizationAnalyzer.AttachType.NORMAL, True)
            if (tt1 is not None): 
                rt.end_token = tt1
        return rt
    
    def __try_attach_org_names(self, t : 'Token', ad : 'OrgAnalyzerData') -> 'ReferentToken':
        from pullenti.ner.org.internal.OrgItemEngItem import OrgItemEngItem
        from pullenti.ner.org.internal.OrgItemNameToken import OrgItemNameToken
        if (t is None): 
            return None
        t0 = t
        br = None
        tname1 = None
        prof = OrgProfile.UNDEFINED
        prof2 = OrgProfile.UNDEFINED
        typ = None
        ok = False
        uri = None
        if (not (isinstance(t, TextToken)) or not t.chars.is_letter): 
            if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 15)
                if ((br) is not None): 
                    t = t0.next0_
                else: 
                    return None
            elif (t.get_referent() is not None and t.get_referent().type_name == "URI"): 
                r = t.get_referent()
                s = r.get_string_value("SCHEME")
                if (s == "HTTP"): 
                    prof = OrgProfile.MEDIA
                    tname1 = t
            elif ((isinstance(t.get_referent(), GeoReferent)) and t.chars.is_letter): 
                if ((t.next0_ is not None and (t.next0_.whitespaces_after_count < 3) and t.next0_.chars.is_latin_letter) and ((t.next0_.is_value("POST", None) or t.next0_.is_value("TODAY", None)))): 
                    tname1 = t.next0_
                    if (OrganizationAnalyzer.__is_std_press_end(tname1)): 
                        prof = OrgProfile.MEDIA
                else: 
                    return None
            else: 
                return None
        elif (t.chars.is_all_upper and t.term == "ИА"): 
            prof = OrgProfile.MEDIA
            t = t.next0_
            typ = "информационное агенство"
            if (t is None or t.whitespaces_before_count > 2): 
                return None
            re = self.__try_attach_org_names(t, ad)
            if (re is not None): 
                re.begin_token = t0
                re.referent.add_type_str(typ)
                return re
            if (t.chars.is_latin_letter): 
                nam = OrgItemEngItem.try_attach(t, False)
                if (nam is not None): 
                    ok = True
                    tname1 = nam.end_token
                else: 
                    nam1 = OrgItemNameToken.try_attach(t, None, False, True)
                    if (nam1 is not None): 
                        ok = True
                        tname1 = nam1.end_token
        elif (((t.chars.is_latin_letter and t.next0_ is not None and t.next0_.is_char('.')) and not t.next0_.is_whitespace_after and t.next0_.next0_ is not None) and t.next0_.next0_.chars.is_latin_letter): 
            tname1 = t.next0_.next0_
            prof = OrgProfile.MEDIA
            if (tname1.next0_ is None): 
                pass
            elif (tname1.whitespaces_after_count > 0): 
                pass
            elif (tname1.next0_.is_char(',')): 
                pass
            elif (tname1.length_char > 1 and tname1.next0_.is_char_of(".") and tname1.next0_.is_whitespace_after): 
                pass
            elif (br is not None and br.end_token.previous == tname1): 
                pass
            else: 
                return None
        elif (t.chars.is_all_lower and br is None): 
            return None
        t00 = t0.previous
        if (t00 is not None and t00.morph.class0_.is_adjective): 
            t00 = t00.previous
        if (t00 is not None and t00.morph.class0_.is_preposition): 
            t00 = t00.previous
        tok = OrganizationAnalyzer.M_PROP_NAMES.try_parse(t, TerminParseAttr.NO)
        if (tok is None and t.chars.is_latin_letter and t.is_value("THE", None)): 
            tok = OrganizationAnalyzer.M_PROP_NAMES.try_parse(t.next0_, TerminParseAttr.NO)
        if (tok is not None and t.is_value("ВЕДУЩИЙ", None) and tok.begin_token == tok.end_token): 
            tok = (None)
        if (tok is not None): 
            prof = (Utils.valToEnum(tok.termin.tag, OrgProfile))
        if (br is not None): 
            t1 = br.end_token.previous
            tt = br.begin_token
            while tt is not None and tt.end_char <= br.end_char: 
                mc = tt.get_morph_class_in_dictionary()
                if (mc == MorphClass.VERB): 
                    return None
                if (mc == MorphClass.ADVERB): 
                    return None
                if (tt.is_char_of("?:")): 
                    return None
                if (tt == br.begin_token.next0_ or tt == br.end_token.previous): 
                    if (((tt.is_value("ЖУРНАЛ", None) or tt.is_value("ГАЗЕТА", None) or tt.is_value("ПРАВДА", None)) or tt.is_value("ИЗВЕСТИЯ", None) or tt.is_value("НОВОСТИ", None)) or tt.is_value("ВЕДОМОСТИ", None)): 
                        ok = True
                        prof = OrgProfile.MEDIA
                        prof2 = OrgProfile.PRESS
                tt = tt.next0_
            if (not ok and OrganizationAnalyzer.__is_std_press_end(t1)): 
                if (br.begin_token.next0_.chars.is_capital_upper and (br.length_char < 15)): 
                    ok = True
                    prof = OrgProfile.MEDIA
                    prof2 = OrgProfile.PRESS
            elif (t1.is_value("FM", None)): 
                ok = True
                prof = OrgProfile.MEDIA
                typ = "радиостанция"
            elif (((t1.is_value("РУ", None) or t1.is_value("RU", None) or t1.is_value("NET", None))) and t1.previous is not None and t1.previous.is_char('.')): 
                prof = OrgProfile.MEDIA
            b = br.begin_token.next0_
            if (b.is_value("THE", None)): 
                b = b.next0_
            if (OrganizationAnalyzer.__is_std_press_end(b) or b.is_value("ВЕЧЕРНИЙ", None)): 
                ok = True
                prof = OrgProfile.MEDIA
        if ((tok is None and not ok and tname1 is None) and prof == OrgProfile.UNDEFINED): 
            if (br is None or not t.chars.is_capital_upper): 
                return None
            tok1 = OrganizationAnalyzer.M_PROP_PREF.try_parse(t00, TerminParseAttr.NO)
            if (tok1 is not None): 
                pr = Utils.valToEnum(tok1.termin.tag, OrgProfile)
                if (prof != OrgProfile.UNDEFINED and prof != pr): 
                    return None
            else: 
                if (t.chars.is_letter and not t.chars.is_cyrillic_letter): 
                    tt = t.next0_
                    first_pass3842 = True
                    while True:
                        if first_pass3842: first_pass3842 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        if (isinstance(tt.get_referent(), GeoReferent)): 
                            continue
                        if (tt.whitespaces_before_count > 2): 
                            break
                        if (not tt.chars.is_letter or tt.chars.is_cyrillic_letter): 
                            break
                        if (OrganizationAnalyzer.__is_std_press_end(tt)): 
                            tname1 = tt
                            prof = OrgProfile.MEDIA
                            ok = True
                            break
                if (tname1 is None): 
                    return None
        if (tok is not None): 
            if (tok.begin_token.chars.is_all_lower and br is None): 
                pass
            elif (tok.begin_token != tok.end_token): 
                ok = True
            elif (MiscHelper.can_be_start_of_sentence(tok.begin_token)): 
                return None
            elif (br is None and BracketHelper.can_be_start_of_sequence(tok.begin_token.previous, False, False)): 
                return None
            elif (tok.chars.is_all_upper): 
                ok = True
        if (not ok): 
            cou = 0
            tt = t0.previous
            first_pass3843 = True
            while True:
                if first_pass3843: first_pass3843 = False
                else: tt = tt.previous; cou += 1
                if (not (tt is not None and (cou < 100))): break
                if (MiscHelper.can_be_start_of_sentence(tt.next0_)): 
                    break
                tok1 = OrganizationAnalyzer.M_PROP_PREF.try_parse(tt, TerminParseAttr.NO)
                if (tok1 is not None): 
                    pr = Utils.valToEnum(tok1.termin.tag, OrgProfile)
                    if (prof != OrgProfile.UNDEFINED and prof != pr): 
                        continue
                    if (tok1.termin.tag2 is not None and prof == OrgProfile.UNDEFINED): 
                        continue
                    prof = pr
                    ok = True
                    break
                org1 = Utils.asObjectOrNull(tt.get_referent(), OrganizationReferent)
                if (org1 is not None and org1.find_slot(OrganizationReferent.ATTR_PROFILE, None, True) is not None): 
                    if ((org1.contains_profile(prof) or prof == OrgProfile.UNDEFINED)): 
                        ok = True
                        prof = org1.profiles[0]
                        break
            cou = 0
            if (not ok): 
                tt = t.next0_
                first_pass3844 = True
                while True:
                    if first_pass3844: first_pass3844 = False
                    else: tt = tt.next0_; cou += 1
                    if (not (tt is not None and (cou < 10))): break
                    if (MiscHelper.can_be_start_of_sentence(tt) and prof != OrgProfile.SPORT): 
                        break
                    tok1 = OrganizationAnalyzer.M_PROP_PREF.try_parse(tt, TerminParseAttr.NO)
                    if (tok1 is not None): 
                        pr = Utils.valToEnum(tok1.termin.tag, OrgProfile)
                        if (prof != OrgProfile.UNDEFINED and prof != pr): 
                            continue
                        if (tok1.termin.tag2 is not None and prof == OrgProfile.UNDEFINED): 
                            continue
                        prof = pr
                        ok = True
                        break
                    org1 = Utils.asObjectOrNull(tt.get_referent(), OrganizationReferent)
                    if (org1 is not None and org1.find_slot(OrganizationReferent.ATTR_PROFILE, None, True) is not None): 
                        if ((org1.contains_profile(prof) or prof == OrgProfile.UNDEFINED)): 
                            ok = True
                            prof = org1.profiles[0]
                            break
            if (not ok): 
                return None
        if (prof == OrgProfile.UNDEFINED): 
            return None
        org0_ = OrganizationReferent()
        org0_.add_profile(prof)
        if (prof2 != OrgProfile.UNDEFINED): 
            org0_.add_profile(prof2)
        if (prof == OrgProfile.SPORT): 
            org0_.add_type_str("спортивный клуб")
        if (typ is not None): 
            org0_.add_type_str(typ)
        if (br is not None and ((tok is None or tok.end_token != br.end_token.previous))): 
            if (tok is not None): 
                nam = MiscHelper.get_text_value(tok.end_token.next0_, br.end_token, GetTextAttr.NO)
                if (nam is not None): 
                    nam = "{0} {1}".format(tok.termin.canonic_text, nam)
                else: 
                    nam = tok.termin.canonic_text
            else: 
                nam = MiscHelper.get_text_value(br.begin_token, br.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
            if (nam is not None): 
                org0_.add_name(nam, True, None)
        elif (tname1 is not None): 
            nam = MiscHelper.get_text_value(t, tname1, GetTextAttr.NO)
            if (nam is not None): 
                nam = nam.replace(". ", ".")
            org0_.add_name(nam, True, None)
        elif (tok is not None): 
            org0_.add_name(tok.termin.canonic_text, True, None)
            if (tok.termin.acronym is not None): 
                org0_.add_name(tok.termin.acronym, True, None)
            if (tok.termin.additional_vars is not None): 
                for v in tok.termin.additional_vars: 
                    org0_.add_name(v.canonic_text, True, None)
        else: 
            return None
        if ((((((prof) & (OrgProfile.MEDIA))) != (OrgProfile.UNDEFINED))) and t0.previous is not None): 
            if ((t0.previous.is_value("ЖУРНАЛ", None) or t0.previous.is_value("ИЗДАНИЕ", None) or t0.previous.is_value("ИЗДАТЕЛЬСТВО", None)) or t0.previous.is_value("АГЕНТСТВО", None)): 
                t0 = t0.previous
                org0_.add_type_str(t0.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False).lower())
                if (not t0.previous.is_value("АГЕНТСТВО", None)): 
                    org0_.add_profile(OrgProfile.PRESS)
        res = ReferentToken(org0_, t0, t)
        if (br is not None): 
            res.end_token = br.end_token
        elif (tok is not None): 
            res.end_token = tok.end_token
        elif (tname1 is not None): 
            res.end_token = tname1
        else: 
            return None
        return res
    
    @staticmethod
    def __is_std_press_end(t : 'Token') -> bool:
        if (not (isinstance(t, TextToken))): 
            return False
        str0_ = t.term
        if ((((((((str0_ == "NEWS" or str0_ == "PRESS" or str0_ == "PRESSE") or str0_ == "ПРЕСС" or str0_ == "НЬЮС") or str0_ == "TIMES" or str0_ == "TIME") or str0_ == "ТАЙМС" or str0_ == "POST") or str0_ == "ПОСТ" or str0_ == "TODAY") or str0_ == "ТУДЕЙ" or str0_ == "DAILY") or str0_ == "ДЕЙЛИ" or str0_ == "ИНФОРМ") or str0_ == "INFORM"): 
            return True
        return False
    
    def __try_attach_org_sport_associations(self, t : 'Token', ad : 'OrgAnalyzerData') -> 'ReferentToken':
        if (t is None): 
            return None
        cou = 0
        typ = None
        t1 = None
        geo_ = None
        if (isinstance(t.get_referent(), GeoReferent)): 
            rt = Utils.asObjectOrNull(t, ReferentToken)
            if (rt.end_token.is_value("ФЕДЕРАЦИЯ", None) or rt.begin_token.is_value("ФЕДЕРАЦИЯ", None)): 
                typ = "федерация"
                geo_ = (Utils.asObjectOrNull(t.get_referent(), GeoReferent))
            t1 = t
            if (t.previous is not None and t.previous.morph.class0_.is_adjective): 
                if (OrganizationAnalyzer.M_SPORTS.try_parse(t.previous, TerminParseAttr.NO) is not None): 
                    cou += 1
                    t = t.previous
        else: 
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            if (npt is None): 
                return None
            if (npt.morph.number == MorphNumber.PLURAL): 
                return None
            if (((npt.noun.is_value("АССОЦИАЦИЯ", None) or npt.noun.is_value("ФЕДЕРАЦИЯ", None) or npt.noun.is_value("СОЮЗ", None)) or npt.noun.is_value("СБОРНАЯ", None) or npt.noun.is_value("КОМАНДА", None)) or npt.noun.is_value("КЛУБ", None)): 
                typ = npt.noun.get_normal_case_text(MorphClass.NOUN, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False).lower()
            elif ((isinstance(t, TextToken)) and t.chars.is_all_upper and t.term == "ФК"): 
                typ = "команда"
            else: 
                return None
            if (typ == "команда"): 
                cou -= 1
            for a in npt.adjectives: 
                tok = OrganizationAnalyzer.M_SPORTS.try_parse(a.begin_token, TerminParseAttr.NO)
                if (tok is not None): 
                    cou += 1
                elif (a.begin_token.is_value("ОЛИМПИЙСКИЙ", None)): 
                    cou += 1
            if (t1 is None): 
                t1 = npt.end_token
        t11 = t1
        propname = None
        del_word = None
        tt = t1.next0_
        first_pass3845 = True
        while True:
            if first_pass3845: first_pass3845 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.whitespaces_before_count > 3): 
                break
            if (tt.is_comma_and): 
                continue
            if (tt.morph.class0_.is_preposition and not tt.morph.class0_.is_adverb and not tt.morph.class0_.is_verb): 
                continue
            if (isinstance(tt.get_referent(), GeoReferent)): 
                t1 = tt
                geo_ = (Utils.asObjectOrNull(tt.get_referent(), GeoReferent))
                if (typ == "сборная"): 
                    cou += 1
                continue
            if (tt.is_value("СТРАНА", None) and (isinstance(tt, TextToken))): 
                t11 = tt
                t1 = t11
                del_word = tt.term
                continue
            tok = OrganizationAnalyzer.M_SPORTS.try_parse(tt, TerminParseAttr.NO)
            if (tok is not None): 
                cou += 1
                tt = tok.end_token
                t11 = tt
                t1 = t11
                continue
            if (tt.chars.is_all_lower or tt.get_morph_class_in_dictionary().is_verb): 
                pass
            else: 
                tok = OrganizationAnalyzer.M_PROP_NAMES.try_parse(tt, TerminParseAttr.NO)
            if (tok is not None): 
                propname = tok.termin.canonic_text
                cou += 1
                tt = tok.end_token
                t1 = tt
                if (cou == 0 and typ == "команда"): 
                    cou += 1
                continue
            if (BracketHelper.can_be_start_of_sequence(tt, True, False)): 
                br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                if (br is None): 
                    break
                tok = OrganizationAnalyzer.M_PROP_NAMES.try_parse(tt.next0_, TerminParseAttr.NO)
                if (tok is not None or cou > 0): 
                    propname = MiscHelper.get_text_value(tt.next0_, br.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                    cou += 1
                    t1 = br.end_token
                    tt = t1
                    continue
                break
            npt1 = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
            if (npt1 is None): 
                break
            tok = OrganizationAnalyzer.M_SPORTS.try_parse(npt1.noun.begin_token, TerminParseAttr.NO)
            if (tok is None): 
                break
            cou += 1
            tt = tok.end_token
            t11 = tt
            t1 = t11
        if (cou <= 0): 
            return None
        org0_ = OrganizationReferent()
        org0_.add_type_str(typ)
        if (typ == "федерация"): 
            org0_.add_type_str("ассоциация")
        name_ = MiscHelper.get_text_value(t, t11, Utils.valToEnum((GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE) | (GetTextAttr.IGNOREGEOREFERENT), GetTextAttr))
        if (name_ is not None and del_word is not None): 
            if (" " + del_word in name_): 
                name_ = name_.replace(" " + del_word, "")
        if (name_ is not None): 
            name_ = name_.replace(" РОССИЯ", "").replace(" РОССИИ", "")
        if (propname is not None): 
            org0_.add_name(propname, True, None)
            if (name_ is not None): 
                org0_.add_type_str(name_.lower())
        elif (name_ is not None): 
            org0_.add_name(name_, True, None)
        if (geo_ is not None): 
            org0_._add_geo_object(geo_)
        org0_.add_profile(OrgProfile.SPORT)
        return ReferentToken(org0_, t, t1)
    
    M_SPORTS = None
    
    M_PROP_NAMES = None
    
    M_PROP_PREF = None
    
    @staticmethod
    def __init_sport() -> None:
        OrganizationAnalyzer.M_SPORTS = TerminCollection()
        for s in ["акробатика;акробатический;акробат", "бадминтон;бадминтонный;бадминтонист", "баскетбол;баскетбольный;баскетболист", "бейсбол;бейсбольный;бейсболист", "биатлон;биатлонный;биатлонист", "бильярд;бильярдный;бильярдист", "бобслей;бобслейный;бобслеист", "боулинг", "боевое искуство", "бокс;боксерский;боксер", "борьба;борец", "водное поло", "волейбол;волейбольный;волейболист", "гандбол;гандбольный;гандболист", "гольф;гольфный;гольфист", "горнолыжный спорт", "слалом;;слаломист", "сквош", "гребля", "дзюдо;дзюдоистский;дзюдоист", "карате;;каратист", "керлинг;;керлингист", "коньки;конькобежный;конькобежец", "легкая атлетика;легкоатлетический;легкоатлет", "лыжных гонок", "мотоцикл;мотоциклетный;мотоциклист", "тяжелая атлетика;тяжелоатлетический;тяжелоатлет", "ориентирование", "плавание;;пловец", "прыжки", "регби;;регбист", "пятиборье", "гимнастика;гимнастический;гимнаст", "самбо;;самбист", "сумо;;сумист", "сноуборд;сноубордический;сноубордист", "софтбол;софтбольный;софтболист", "стрельба;стрелковый", "спорт;спортивный", "теннис;теннисный;теннисист", "триатлон", "тхэквондо", "ушу;;ушуист", "фехтование;фехтовальный;фехтовальщик", "фигурное катание;;фигурист", "фристайл;фристальный", "футбол;футбольный;футболист", "мини-футбол", "хоккей;хоккейный;хоккеист", "хоккей на траве", "шахматы;шахматный;шахматист", "шашки;шашечный"]: 
            pp = Utils.splitString(s.upper(), ';', False)
            t = Termin()
            t.init_by_normal_text(pp[0], MorphLang.RU)
            if (len(pp) > 1 and not Utils.isNullOrEmpty(pp[1])): 
                t.add_variant(pp[1], True)
            if (len(pp) > 2 and not Utils.isNullOrEmpty(pp[2])): 
                t.add_variant(pp[2], True)
            OrganizationAnalyzer.M_SPORTS.add(t)
        for s in ["байдарка", "каноэ", "лук", "трава", "коньки", "трамплин", "двоеборье", "батут", "вода", "шпага", "сабля", "лыжи", "скелетон"]: 
            OrganizationAnalyzer.M_SPORTS.add(Termin._new2352(s.upper(), s))
        OrganizationAnalyzer.M_PROP_NAMES = TerminCollection()
        for s in ["СПАРТАК", "ЦСКА", "ЗЕНИТ!", "ТЕРЕК", "КРЫЛЬЯ СОВЕТОВ", "ДИНАМО", "АНЖИ", "КУБАНЬ", "АЛАНИЯ", "ТОРПЕДО", "АРСЕНАЛ!", "ЛОКОМОТИВ", "МЕТАЛЛУРГ!", "РОТОР", "СКА", "СОКОЛ!", "ХИМИК!", "ШИННИК", "РУБИН", "ШАХТЕР", "САЛАВАТ ЮЛАЕВ", "ТРАКТОР!", "АВАНГАРД!", "АВТОМОБИЛИСТ!", "АТЛАНТ!", "ВИТЯЗЬ!", "НАЦИОНАЛЬНАЯ ХОККЕЙНАЯ ЛИГА;НХЛ", "КОНТИНЕНТАЛЬНАЯ ХОККЕЙНАЯ ЛИГА;КХЛ", "СОЮЗ ЕВРОПЕЙСКИХ ФУТБОЛЬНЫХ АССОЦИАЦИЙ;УЕФА;UEFA", "Женская теннисная ассоциация;WTA", "Международная федерация бокса;IBF", "Всемирная боксерская организация;WBO", "РЕАЛ", "МАНЧЕСТЕР ЮНАЙТЕД", "манчестер сити", "БАРСЕЛОНА!", "БАВАРИЯ!", "ЧЕЛСИ", "ЛИВЕРПУЛЬ!", "ЮВЕНТУС", "НАПОЛИ", "БОЛОНЬЯ", "ФУЛХЭМ", "ЭВЕРТОН", "ФИЛАДЕЛЬФИЯ", "ПИТТСБУРГ", "ИНТЕР!", "Аякс", "ФЕРРАРИ;FERRARI", "РЕД БУЛЛ;RED BULL", "МАКЛАРЕН;MCLAREN", "МАКЛАРЕН-МЕРСЕДЕС;MCLAREN-MERCEDES"]: 
            ss = s.upper()
            is_bad = False
            if (ss.endswith("!")): 
                is_bad = True
                ss = ss[0:0+len(ss) - 1]
            pp = Utils.splitString(ss, ';', False)
            t = Termin._new100(pp[0], OrgProfile.SPORT)
            if (not is_bad): 
                t.tag2 = (ss)
            if (len(pp) > 1): 
                if (len(pp[1]) < 4): 
                    t.acronym = pp[1]
                else: 
                    t.add_variant(pp[1], False)
            OrganizationAnalyzer.M_PROP_NAMES.add(t)
        for s in ["ИТАР ТАСС;ТАСС;Телеграфное агентство советского союза", "Интерфакс;Interfax", "REGNUM", "ЛЕНТА.РУ;Lenta.ru", "Частный корреспондент;ЧасКор", "РИА Новости;Новости!;АПН", "Росбалт;RosBalt", "УНИАН", "ИНФОРОС;inforos", "Эхо Москвы", "Сноб!", "Серебряный дождь", "Вечерняя Москва;Вечерка", "Московский Комсомолец;Комсомолка", "Коммерсантъ;Коммерсант", "Афиша", "Аргументы и факты;АИФ", "Викиновости", "РосБизнесКонсалтинг;РБК", "Газета.ру", "Русский Репортер!", "Ведомости", "Вести!", "Рамблер Новости", "Живой Журнал;ЖЖ;livejournal;livejournal.ru", "Новый Мир", "Новая газета", "Правда!", "Известия!", "Бизнес!", "Русская жизнь!", "НТВ Плюс", "НТВ", "ВГТРК", "ТНТ", "Муз ТВ;МузТВ", "АСТ", "Эксмо", "Астрель", "Терра!", "Финанс!", "Собеседник!", "Newsru.com", "Nature!", "Россия сегодня;Russia Today;RT!", "БЕЛТА", "Ассошиэйтед Пресс;Associated Press", "France Press;France Presse;Франс пресс;Agence France Presse;AFP", "СИНЬХУА", "Gallup", "Cable News Network;CNN", "CBS News", "ABC News", "GoogleNews;Google News", "FoxNews;Fox News", "Reuters;Рейтер", "British Broadcasting Corporation;BBC;БиБиСи;BBC News", "MSNBC", "Голос Америки", "Аль Джазира;Al Jazeera", "Радио Свобода", "Радио Свободная Европа", "Guardian;Гардиан", "Daily Telegraph", "Times;Таймс!", "Independent!", "Financial Times", "Die Welt", "Bild!", "La Pepublica;Република!", "Le Monde", "People Daily", "BusinessWeek", "Economist!", "Forbes;Форбс", "Los Angeles Times", "New York Times", "Wall Street Journal;WSJ", "Washington Post", "Le Figaro;Фигаро", "Bloomberg", "DELFI!"]: 
            ss = s.upper()
            is_bad = False
            if (ss.endswith("!")): 
                is_bad = True
                ss = ss[0:0+len(ss) - 1]
            pp = Utils.splitString(ss, ';', False)
            t = Termin._new100(pp[0], OrgProfile.MEDIA)
            if (not is_bad): 
                t.tag2 = (ss)
            ii = 1
            while ii < len(pp): 
                if ((len(pp[ii]) < 4) and t.acronym is None): 
                    t.acronym = pp[ii]
                else: 
                    t.add_variant(pp[ii], False)
                ii += 1
            OrganizationAnalyzer.M_PROP_NAMES.add(t)
        for s in ["Машина времени!", "ДДТ", "Биттлз;Bittles", "ABBA;АББА", "Океан Эльзы;Океан Эльзи", "Аквариум!", "Крематорий!", "Наутилус;Наутилус Помпилиус!", "Пусси Райот;Пусси Риот;Pussy Riot", "Кино!", "Алиса!", "Агата Кристи!", "Чайф", "Ария!", "Земфира!", "Браво!", "Черный кофе!", "Воскресение!", "Урфин Джюс", "Сплин!", "Пикник!", "Мумий Троль", "Коррозия металла", "Арсенал!", "Ночные снайперы!", "Любэ", "Ласковый май!", "Noize MC", "Linkin Park", "ac dc", "green day!", "Pink Floyd;Пинк Флойд", "Depeche Mode", "Bon Jovi", "Nirvana;Нирвана!", "Queen;Квин!", "Nine Inch Nails", "Radioheads", "Pet Shop Boys", "Buggles"]: 
            ss = s.upper()
            is_bad = False
            if (ss.endswith("!")): 
                is_bad = True
                ss = ss[0:0+len(ss) - 1]
            pp = Utils.splitString(ss, ';', False)
            t = Termin._new100(pp[0], OrgProfile.MUSIC)
            if (not is_bad): 
                t.tag2 = (ss)
            ii = 1
            while ii < len(pp): 
                if ((len(pp[ii]) < 4) and t.acronym is None): 
                    t.acronym = pp[ii]
                else: 
                    t.add_variant(pp[ii], False)
                ii += 1
            OrganizationAnalyzer.M_PROP_NAMES.add(t)
        OrganizationAnalyzer.M_PROP_PREF = TerminCollection()
        for s in ["ФАНАТ", "БОЛЕЛЬЩИК", "гонщик", "вратарь", "нападающий", "голкипер", "полузащитник", "полу-защитник", "центрфорвард", "центр-форвард", "форвард", "игрок", "легионер", "спортсмен"]: 
            OrganizationAnalyzer.M_PROP_PREF.add(Termin._new100(s.upper(), OrgProfile.SPORT))
        for s in ["защитник", "капитан", "пилот", "игра", "поле", "стадион", "гонка", "чемпионат", "турнир", "заезд", "матч", "кубок", "олипмиада", "финал", "полуфинал", "победа", "поражение", "разгром", "дивизион", "олипмиада", "финал", "полуфинал", "играть", "выигрывать", "выиграть", "проигрывать", "проиграть", "съиграть"]: 
            OrganizationAnalyzer.M_PROP_PREF.add(Termin._new102(s.upper(), OrgProfile.SPORT, s))
        for s in ["корреспондент", "фотокорреспондент", "репортер", "журналист", "тележурналист", "телеоператор", "главный редактор", "главред", "телеведущий", "редколлегия", "обозреватель", "сообщать", "сообщить", "передавать", "передать", "писать", "написать", "издавать", "пояснить", "пояснять", "разъяснить", "разъяснять", "сказать", "говорить", "спрашивать", "спросить", "отвечать", "ответить", "выяснять", "выяснить", "цитировать", "процитировать", "рассказать", "рассказывать", "информировать", "проинформировать", "поведать", "напечатать", "напоминать", "напомнить", "узнать", "узнавать", "репортаж", "интервью", "информации", "сведение", "ИА", "информагенство", "информагентство", "информационный", "газета", "журнал"]: 
            OrganizationAnalyzer.M_PROP_PREF.add(Termin._new100(s.upper(), OrgProfile.MEDIA))
        for s in ["сообщение", "статья", "номер", "журнал", "издание", "издательство", "агентство", "цитата", "редактор", "комментатор", "по данным", "оператор", "вышедший", "отчет", "вопрос", "читатель", "слушатель", "телезритель", "источник", "собеедник"]: 
            OrganizationAnalyzer.M_PROP_PREF.add(Termin._new102(s.upper(), OrgProfile.MEDIA, s))
        for s in ["музыкант", "певец", "певица", "ударник", "гитарист", "клавишник", "солист", "солистка", "исполнитель", "исполнительница", "исполнять", "исполнить", "концерт", "гастроль", "выступление", "известный", "известнейший", "популярный", "популярнейший", "рокгруппа", "панкгруппа", "группа", "альбом", "пластинка", "грампластинка", "концертный", "музыка", "песня", "сингл", "хит", "суперхит", "запись", "студия"]: 
            OrganizationAnalyzer.M_PROP_PREF.add(Termin._new100(s.upper(), OrgProfile.MEDIA))
    
    def __try_attach_army(self, t : 'Token', ad : 'OrgAnalyzerData') -> 'ReferentToken':
        if (not (isinstance(t, NumberToken)) or t.whitespaces_after_count > 2): 
            return None
        typ = OrgItemTypeToken.try_attach(t.next0_, True, ad)
        if (typ is None): 
            return None
        if (typ.root is not None and OrgProfile.ARMY in typ.root.profiles): 
            rt = self.__try_attach_org(t.next0_, ad, OrganizationAnalyzer.AttachType.HIGH, None, False, 0, -1)
            if (rt is not None): 
                if (rt.begin_token == typ.begin_token): 
                    rt.begin_token = t
                    rt.referent.number = str(t.value)
                return rt
            org0_ = OrganizationReferent()
            org0_.add_type(typ, True)
            org0_.number = str(t.value)
            return ReferentToken(org0_, t, typ.end_token)
        return None