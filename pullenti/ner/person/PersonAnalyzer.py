# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.Token import Token
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.Morphology import Morphology
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.person.internal.ShortNameHelper import ShortNameHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.person.PersonPropertyKind import PersonPropertyKind
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.person.internal.FioTemplateType import FioTemplateType
from pullenti.ner.person.internal.MetaPersonProperty import MetaPersonProperty
from pullenti.ner.person.internal.MetaPersonIdentity import MetaPersonIdentity
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
from pullenti.ner.mail.internal.MailLine import MailLine
from pullenti.ner.person.internal.MetaPerson import MetaPerson
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.ner.person.internal.PersonAttrTerminType import PersonAttrTerminType
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.person.internal.PersonMorphCollection import PersonMorphCollection
from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology

class PersonAnalyzer(Analyzer):
    """ Семантический анализатор выделения персон """
    
    class PersonAnalyzerData(AnalyzerDataWithOntology):
        
        def __init__(self) -> None:
            super().__init__()
            self.nominative_case_always = False
            self.text_starts_with_lastname_firstname_middlename = False
            self.need_second_step = False
            self.can_be_person_prop_begin_chars = dict()
        
        def registerReferent(self, referent : 'Referent') -> 'Referent':
            from pullenti.ner.Referent import Referent
            from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
            from pullenti.ner.core.AnalyzerData import AnalyzerData
            from pullenti.ner.ReferentToken import ReferentToken
            from pullenti.ner.person.PersonReferent import PersonReferent
            from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
            if (isinstance(referent, PersonReferent)): 
                exist_props = None
                i = 0
                first_pass3121 = True
                while True:
                    if first_pass3121: first_pass3121 = False
                    else: i += 1
                    if (not (i < len(referent.slots))): break
                    a = referent.slots[i]
                    if (a.type_name == PersonReferent.ATTR_ATTR): 
                        pat = Utils.asObjectOrNull(a.value, PersonAttrToken)
                        if (pat is None or pat.prop_ref is None): 
                            if (isinstance(a.value, PersonPropertyReferent)): 
                                if (exist_props is None): 
                                    exist_props = list()
                                exist_props.append(Utils.asObjectOrNull(a.value, PersonPropertyReferent))
                            continue
                        if (pat.prop_ref is not None): 
                            for ss in pat.prop_ref.slots: 
                                if (ss.type_name == PersonPropertyReferent.ATTR_REF): 
                                    if (isinstance(ss.value, ReferentToken)): 
                                        if ((ss.value).referent == referent): 
                                            pat.prop_ref.slots.remove(ss)
                                            break
                        if (exist_props is not None): 
                            for pp in exist_props: 
                                if (pp.canBeEquals(pat.prop_ref, Referent.EqualType.WITHINONETEXT)): 
                                    if (pat.prop_ref.canBeGeneralFor(pp)): 
                                        pat.prop_ref.mergeSlots(pp, True)
                                        break
                        pat.data = (self)
                        pat.saveToLocalOntology()
                        if (pat.prop_ref is not None): 
                            if (referent.findSlot(a.type_name, pat.prop_ref, True) is not None): 
                                del referent.slots[i]
                                i -= 1
                            else: 
                                referent.uploadSlot(a, pat.referent)
            if (isinstance(referent, PersonPropertyReferent)): 
                i = 0
                first_pass3122 = True
                while True:
                    if first_pass3122: first_pass3122 = False
                    else: i += 1
                    if (not (i < len(referent.slots))): break
                    a = referent.slots[i]
                    if (a.type_name == PersonPropertyReferent.ATTR_REF or a.type_name == PersonPropertyReferent.ATTR_HIGHER): 
                        pat = Utils.asObjectOrNull(a.value, ReferentToken)
                        if (pat is not None): 
                            pat.data = (self)
                            pat.saveToLocalOntology()
                            if (pat.referent is not None): 
                                referent.uploadSlot(a, pat.referent)
                        elif (isinstance(a.value, PersonPropertyReferent)): 
                            if (a.value == referent): 
                                del referent.slots[i]
                                i -= 1
                                continue
                            referent.uploadSlot(a, self.registerReferent(Utils.asObjectOrNull(a.value, PersonPropertyReferent)))
            res = super().registerReferent(referent)
            return res
    
    def __init__(self) -> None:
        super().__init__()
        self.nominative_case_always = False
        self.text_starts_with_lastname_firstname_middlename = False
        self.__m_level = 0
    
    ANALYZER_NAME = "PERSON"
    
    @property
    def name(self) -> str:
        return PersonAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Персоны"
    
    @property
    def description(self) -> str:
        return "Персоны и их атрибуты"
    
    def clone(self) -> 'Analyzer':
        return PersonAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaPerson._global_meta, MetaPersonProperty._global_meta, MetaPersonIdentity._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaPerson.MAN_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("man.png")
        res[MetaPerson.WOMEN_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("women.png")
        res[MetaPerson.PERSON_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("person.png")
        res[MetaPerson.GENERAL_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("general.png")
        res[MetaPersonProperty.PERSON_PROP_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("personproperty.png")
        res[MetaPersonProperty.PERSON_PROP_BOSS_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("boss.png")
        res[MetaPersonProperty.PERSON_PROP_KING_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("king.png")
        res[MetaPersonProperty.PERSON_PROP_KIN_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("kin.png")
        res[MetaPersonProperty.PERSON_PROP_MILITARY_ID] = EpNerCoreInternalResourceHelper.getBytes("militaryrank.png")
        res[MetaPersonProperty.PERSON_PROP_NATION_ID] = EpNerCoreInternalResourceHelper.getBytes("nationality.png")
        res[MetaPersonIdentity.IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("identity.png")
        return res
    
    def createReferent(self, type0_ : str) -> 'Referent':
        if (type0_ == PersonReferent.OBJ_TYPENAME): 
            return PersonReferent()
        if (type0_ == PersonPropertyReferent.OBJ_TYPENAME): 
            return PersonPropertyReferent()
        if (type0_ == PersonIdentityReferent.OBJ_TYPENAME): 
            return PersonIdentityReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["ORGANIZATION", "GEO", "ADDRESS", "TRANSPORT"]
    
    @property
    def progress_weight(self) -> int:
        return 35
    
    def createAnalyzerData(self) -> 'AnalyzerData':
        return PersonAnalyzer.PersonAnalyzerData()
    
    def process(self, kit : 'AnalysisKit') -> None:
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        from pullenti.ner.person.internal.PersonIdToken import PersonIdToken
        ad = Utils.asObjectOrNull(kit.getAnalyzerData(self), PersonAnalyzer.PersonAnalyzerData)
        ad.nominative_case_always = self.nominative_case_always
        ad.text_starts_with_lastname_firstname_middlename = self.text_starts_with_lastname_firstname_middlename
        ad.need_second_step = False
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
                    if (not self._onProgress(cur, max0_, kit)): 
                        return
                rts = self.__tryAttachPersons(t, ad, step)
                if (rts is not None): 
                    if (not MetaToken.check(rts)): 
                        pass
                    else: 
                        for rt in rts: 
                            if (rt.referent is None): 
                                t = rt.end_token
                            else: 
                                pats = list()
                                for s in rt.referent.slots: 
                                    if (isinstance(s.value, PersonAttrToken)): 
                                        pat = Utils.asObjectOrNull(s.value, PersonAttrToken)
                                        pats.append(pat)
                                        if (pat.prop_ref is None): 
                                            continue
                                        for ss in pat.prop_ref.slots: 
                                            if (ss.type_name == PersonPropertyReferent.ATTR_REF and (isinstance(ss.value, ReferentToken))): 
                                                rt1 = Utils.asObjectOrNull(ss.value, ReferentToken)
                                                rt1.referent = ad.registerReferent(rt1.referent)
                                                ss.value = rt1.referent
                                                rr = ReferentToken._new746(rt1.referent, rt1.begin_token, rt1.end_token, rt1.morph)
                                                kit.embedToken(rr)
                                                if (rr.begin_token == rt.begin_token): 
                                                    rt.begin_token = rr
                                                if (rr.end_token == rt.end_token): 
                                                    rt.end_token = rr
                                                if (rr.begin_token == pat.begin_token): 
                                                    pat.begin_token = rr
                                                if (rr.end_token == pat.end_token): 
                                                    pat.end_token = rr
                                    elif (isinstance(s.value, ReferentToken)): 
                                        rt0 = Utils.asObjectOrNull(s.value, ReferentToken)
                                        if (rt0.referent is not None): 
                                            for s1 in rt0.referent.slots: 
                                                if (isinstance(s1.value, PersonAttrToken)): 
                                                    pat = Utils.asObjectOrNull(s1.value, PersonAttrToken)
                                                    if (pat.prop_ref is None): 
                                                        continue
                                                    for ss in pat.prop_ref.slots: 
                                                        if (ss.type_name == PersonPropertyReferent.ATTR_REF and (isinstance(ss.value, ReferentToken))): 
                                                            rt1 = Utils.asObjectOrNull(ss.value, ReferentToken)
                                                            rt1.referent = ad.registerReferent(rt1.referent)
                                                            ss.value = rt1.referent
                                                            rr = ReferentToken._new746(rt1.referent, rt1.begin_token, rt1.end_token, rt1.morph)
                                                            kit.embedToken(rr)
                                                            if (rr.begin_token == rt0.begin_token): 
                                                                rt0.begin_token = rr
                                                            if (rr.end_token == rt0.end_token): 
                                                                rt0.end_token = rr
                                                            if (rr.begin_token == pat.begin_token): 
                                                                pat.begin_token = rr
                                                            if (rr.end_token == pat.end_token): 
                                                                pat.end_token = rr
                                                    pat.prop_ref = Utils.asObjectOrNull(ad.registerReferent(pat.prop_ref), PersonPropertyReferent)
                                                    rt2 = ReferentToken._new746(pat.prop_ref, pat.begin_token, pat.end_token, pat.morph)
                                                    kit.embedToken(rt2)
                                                    if (rt2.begin_token == rt0.begin_token): 
                                                        rt0.begin_token = rt2
                                                    if (rt2.end_token == rt0.end_token): 
                                                        rt0.end_token = rt2
                                                    s1.value = pat.prop_ref
                                        rt0.referent = ad.registerReferent(rt0.referent)
                                        if (rt0.begin_char == rt.begin_char): 
                                            rt.begin_token = rt0
                                        if (rt0.end_char == rt.end_char): 
                                            rt.end_token = rt0
                                        kit.embedToken(rt0)
                                        s.value = rt0.referent
                                rt.referent = ad.registerReferent(rt.referent)
                                for p in pats: 
                                    if (p.prop_ref is not None): 
                                        rr = ReferentToken._new746(p.prop_ref, p.begin_token, p.end_token, p.morph)
                                        kit.embedToken(rr)
                                        if (rr.begin_token == rt.begin_token): 
                                            rt.begin_token = rr
                                        if (rr.end_token == rt.end_token): 
                                            rt.end_token = rr
                                kit.embedToken(rt)
                                t = (rt)
                elif (step == 0): 
                    rt = PersonIdToken.tryAttach(t)
                    if (rt is not None): 
                        rt.referent = ad.registerReferent(rt.referent)
                        tt = t.previous
                        if (tt is not None and tt.isCharOf(":,")): 
                            tt = tt.previous
                        pers = (None if tt is None else Utils.asObjectOrNull(tt.getReferent(), PersonReferent))
                        if (pers is not None): 
                            pers.addSlot(PersonReferent.ATTR_IDDOC, rt.referent, False, 0)
                        kit.embedToken(rt)
                        t = (rt)
                t = t.next0_
            if (len(ad.referents) == 0 and not ad.need_second_step): 
                break
            step += 1
        props = dict()
        for r in ad.referents: 
            p = Utils.asObjectOrNull(r, PersonReferent)
            if (p is None): 
                continue
            for s in p.slots: 
                if (s.type_name == PersonReferent.ATTR_ATTR and (isinstance(s.value, PersonPropertyReferent))): 
                    pr = Utils.asObjectOrNull(s.value, PersonPropertyReferent)
                    li = [ ]
                    wrapli2460 = RefOutArgWrapper(None)
                    inoutres2461 = Utils.tryGetValue(props, pr, wrapli2460)
                    li = wrapli2460.value
                    if (not inoutres2461): 
                        li = list()
                        props[pr] = li
                    if (not p in li): 
                        li.append(p)
        t = kit.first_token
        first_pass3123 = True
        while True:
            if first_pass3123: first_pass3123 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (isinstance(t, ReferentToken)): 
                if (t.chars.is_latin_letter and MiscHelper.isEngAdjSuffix(t.next0_)): 
                    pass
                else: 
                    continue
            if (not t.begin_char in ad.can_be_person_prop_begin_chars): 
                continue
            pat = PersonAttrToken.tryAttach(t, ad.local_ontology, PersonAttrToken.PersonAttrAttachAttrs.NO)
            if (pat is None): 
                continue
            if (pat.prop_ref is None or ((pat.typ != PersonAttrTerminType.POSITION and pat.typ != PersonAttrTerminType.KING))): 
                t = pat.end_token
                continue
            pers = list()
            for kp in props.items(): 
                if (kp[0].canBeEquals(pat.prop_ref, Referent.EqualType.WITHINONETEXT)): 
                    for pp in kp[1]: 
                        if (not pp in pers): 
                            pers.append(pp)
                    if (len(pers) > 1): 
                        break
            if (len(pers) == 1): 
                tt = pat.end_token.next0_
                if (tt is not None and ((tt.isChar('_') or tt.is_newline_before or tt.is_table_control_char))): 
                    pass
                else: 
                    pat.data = (ad)
                    pat.saveToLocalOntology()
                    kit.embedToken(pat)
                    rt = ReferentToken._new746(pers[0], pat, pat, pat.morph)
                    kit.embedToken(rt)
                    t = (rt)
                    continue
            if (pat.prop_ref is not None): 
                if (pat.can_be_independent_property or len(pers) > 0): 
                    rt = ReferentToken._new746(ad.registerReferent(pat.prop_ref), pat.begin_token, pat.end_token, pat.morph)
                    kit.embedToken(rt)
                    t = (rt)
                    continue
    
    def _processReferent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        if (begin is None or self.__m_level > 2): 
            return None
        self.__m_level += 1
        ad = Utils.asObjectOrNull(begin.kit.getAnalyzerData(self), PersonAnalyzer.PersonAnalyzerData)
        rt = PersonAnalyzer._tryAttachPerson(begin, ad, False, -1, False)
        self.__m_level -= 1
        if (rt is not None and rt.referent is None): 
            rt = (None)
        if (rt is not None): 
            rt.data = begin.kit.getAnalyzerData(self)
            return rt
        self.__m_level += 1
        pat = PersonAttrToken.tryAttach(begin, None, PersonAttrToken.PersonAttrAttachAttrs.NO)
        self.__m_level -= 1
        if (pat is None or pat.prop_ref is None): 
            return None
        rt = ReferentToken._new746(pat.prop_ref, pat.begin_token, pat.end_token, pat.morph)
        rt.data = (ad)
        return rt
    
    def __tryAttachPersons(self, t : 'Token', ad : 'PersonAnalyzerData', step : int) -> typing.List['ReferentToken']:
        rt = PersonAnalyzer._tryAttachPerson(t, ad, False, step, False)
        if (rt is None): 
            return None
        res = list()
        res.append(rt)
        names = None
        tt = rt.end_token.next0_
        while tt is not None: 
            if (not tt.is_comma_and): 
                break
            pits = PersonItemToken.tryAttachList(tt.next0_, None, PersonItemToken.ParseAttr.NO, 10)
            if (pits is None or len(pits) != 1): 
                break
            rt1 = PersonAnalyzer._tryAttachPerson(t, ad, False, step, False)
            if (rt1 is not None): 
                break
            if (pits[0].firstname is None or len(pits[0].firstname.vars0_) == 0): 
                break
            if (names is None): 
                names = list()
            names.append(pits[0])
            if (tt.is_and): 
                break
            tt = tt.next0_
            tt = tt.next0_
        if (names is not None): 
            for n in names: 
                pers = PersonReferent()
                bi = MorphBaseInfo._new2465(MorphNumber.SINGULAR, t.kit.base_language)
                bi.class0_ = MorphClass._new2427(True)
                if (n.firstname.vars0_[0].gender == MorphGender.FEMINIE): 
                    pers.is_female = True
                    bi.gender = MorphGender.FEMINIE
                elif (n.firstname.vars0_[0].gender == MorphGender.MASCULINE): 
                    pers.is_male = True
                    bi.gender = MorphGender.MASCULINE
                for v in n.firstname.vars0_: 
                    pers.addSlot(PersonReferent.ATTR_FIRSTNAME, v.value, False, 0)
                for s in rt.referent.slots: 
                    if (s.type_name == PersonReferent.ATTR_ATTR): 
                        pers.addSlot(s.type_name, s.value, False, 0)
                    elif (s.type_name == PersonReferent.ATTR_LASTNAME): 
                        sur = Utils.asObjectOrNull(s.value, str)
                        if (bi.gender != MorphGender.UNDEFINED): 
                            sur0 = Morphology.getWordform(sur, bi)
                            if (sur0 is not None): 
                                pers.addSlot(PersonReferent.ATTR_LASTNAME, sur0, False, 0)
                        pers.addSlot(PersonReferent.ATTR_LASTNAME, sur, False, 0)
                res.append(ReferentToken._new746(pers, n.begin_token, n.end_token, n.morph))
        return res
    
    @staticmethod
    def _tryAttachPerson(t : 'Token', ad : 'PersonAnalyzerData', for_ext_ontos : bool, step : int, for_attribute : bool=False) -> 'ReferentToken':
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        from pullenti.ner.person.internal.PersonHelper import PersonHelper
        from pullenti.ner.person.internal.PersonIdentityToken import PersonIdentityToken
        attrs = None
        mi = MorphBaseInfo()
        mi.case_ = (MorphCase.NOMINATIVE if (for_ext_ontos or ((ad is not None and ad.nominative_case_always))) else MorphCase.ALL_CASES)
        mi.gender = Utils.valToEnum((MorphGender.MASCULINE) | (MorphGender.FEMINIE), MorphGender)
        t0 = t
        and0_ = False
        and_was_terminated = False
        can_attach_to_previous_person = True
        is_king = False
        after_be_predicate = False
        first_pass3124 = True
        while True:
            if first_pass3124: first_pass3124 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (attrs is not None and t.next0_ is not None): 
                if (and0_): 
                    break
                if (t.isChar(',')): 
                    t = t.next0_
                elif (t.is_and and t.is_whitespace_after and t.chars.is_all_lower): 
                    t = t.next0_
                    and0_ = True
                elif (t.is_hiphen and t.is_newline_after): 
                    t = t.next0_
                    and0_ = True
                elif (t.is_hiphen and t.whitespaces_after_count == 1 and t.whitespaces_before_count == 1): 
                    t = t.next0_
                    and0_ = True
                elif ((t.is_hiphen and t.next0_ is not None and t.next0_.is_hiphen) and t.next0_.whitespaces_after_count == 1 and t.whitespaces_before_count == 1): 
                    t = t.next0_.next0_
                    and0_ = True
                elif (t.isChar(':')): 
                    if (not attrs[len(attrs) - 1].morph.case_.is_nominative and not attrs[len(attrs) - 1].morph.case_.is_undefined): 
                        pass
                    else: 
                        mi.case_ = MorphCase.NOMINATIVE
                        mi.gender = Utils.valToEnum((MorphGender.MASCULINE) | (MorphGender.FEMINIE), MorphGender)
                    t = t.next0_
                    if (not BracketHelper.canBeStartOfSequence(t, False, False)): 
                        can_attach_to_previous_person = False
                elif (t.isChar('_')): 
                    cou = 0
                    te = t
                    while te is not None: 
                        if (not te.isChar('_') or ((te.is_whitespace_before and te != t))): 
                            break
                        else: 
                            cou += 1
                        te = te.next0_
                    if (cou > 2 and ((not t.is_newline_before or ((te is not None and not te.is_newline_before))))): 
                        mi.case_ = MorphCase.NOMINATIVE
                        mi.gender = Utils.valToEnum((MorphGender.MASCULINE) | (MorphGender.FEMINIE), MorphGender)
                        can_attach_to_previous_person = False
                        t = te
                        if (t is not None and t.isChar('/') and t.next0_ is not None): 
                            t = t.next0_
                        break
                elif ((t.isValue("ЯВЛЯТЬСЯ", None) or t.isValue("БЫТЬ", None) or t.isValue("Є", None)) or t.isValue("IS", None)): 
                    mi.case_ = MorphCase.NOMINATIVE
                    mi.gender = Utils.valToEnum((MorphGender.MASCULINE) | (MorphGender.FEMINIE), MorphGender)
                    after_be_predicate = True
                    continue
                elif (((t.isValue("LIKE", None) or t.isValue("AS", None))) and attrs is not None): 
                    t = t.next0_
                    break
            if (t.chars.is_latin_letter and step == 0): 
                tt2 = t
                if (MiscHelper.isEngArticle(t)): 
                    tt2 = t.next0_
                pit0 = PersonItemToken.tryAttach(tt2, (None if ad is None else ad.local_ontology), PersonItemToken.ParseAttr.CANBELATIN, None)
                if (pit0 is not None and MiscHelper.isEngAdjSuffix(pit0.end_token.next0_) and ad is not None): 
                    pp = PersonIdentityToken.tryAttachOntoForSingle(pit0, ad.local_ontology)
                    if (pp is None): 
                        pp = PersonIdentityToken.tryAttachLatinSurname(pit0, ad.local_ontology)
                    if (pp is not None): 
                        return PersonHelper._createReferentToken(pp, pit0.begin_token, pit0.end_token, pit0.morph, attrs, ad, for_attribute, after_be_predicate)
            a = None
            if ((step < 1) or t.inner_bool): 
                a = PersonAttrToken.tryAttach(t, (None if ad is None else ad.local_ontology), PersonAttrToken.PersonAttrAttachAttrs.NO)
                if (step == 0 and a is not None): 
                    t.inner_bool = True
            if (a is None): 
                break
            if (after_be_predicate): 
                return None
            if (not t.chars.is_all_lower and a.begin_token == a.end_token): 
                pit = PersonItemToken.tryAttach(t, (None if ad is None else ad.local_ontology), PersonItemToken.ParseAttr.CANBELATIN, None)
                if (pit is not None and pit.lastname is not None and ((pit.lastname.is_in_ontology or pit.lastname.is_in_dictionary))): 
                    break
            if (ad is not None and not a.begin_char in ad.can_be_person_prop_begin_chars): 
                ad.can_be_person_prop_begin_chars[a.begin_char] = True
            if (attrs is None): 
                if (a.is_doubt): 
                    if (a.is_newline_after): 
                        break
                attrs = list()
            elif (not a.morph.case_.is_undefined and not mi.case_.is_undefined): 
                if (((a.morph.case_) & mi.case_).is_undefined): 
                    attrs.clear()
                    mi.case_ = (MorphCase.NOMINATIVE if for_ext_ontos else MorphCase.ALL_CASES)
                    mi.gender = Utils.valToEnum((MorphGender.MASCULINE) | (MorphGender.FEMINIE), MorphGender)
                    is_king = False
            attrs.append(a)
            if (len(attrs) > 5): 
                return ReferentToken(None, attrs[0].begin_token, a.end_token)
            if (a.typ == PersonAttrTerminType.KING): 
                is_king = True
            if (a.typ == PersonAttrTerminType.BESTREGARDS): 
                mi.case_ = MorphCase.NOMINATIVE
            if (and0_): 
                and_was_terminated = True
            if (a.can_has_person_after == 0): 
                if (a.gender != MorphGender.UNDEFINED): 
                    if (a.typ != PersonAttrTerminType.POSITION): 
                        mi.gender = Utils.valToEnum((mi.gender) & (a.gender), MorphGender)
                    elif (a.gender == MorphGender.FEMINIE): 
                        mi.gender = Utils.valToEnum((mi.gender) & (a.gender), MorphGender)
                if (not a.morph.case_.is_undefined): 
                    mi.case_ = (mi.case_) & a.morph.case_
            t = a.end_token
        if (attrs is not None and and0_ and not and_was_terminated): 
            if ((t is not None and t.previous is not None and t.previous.is_hiphen) and (t.whitespaces_before_count < 2)): 
                pass
            else: 
                return None
        if (attrs is not None): 
            if (t is not None and BracketHelper.canBeEndOfSequence(t, False, None, False)): 
                t = t.next0_
        while t is not None and t.is_table_control_char:
            t = t.next0_
        if (t is None): 
            if (attrs is not None): 
                attr = attrs[len(attrs) - 1]
                if (attr.can_be_single_person and attr.prop_ref is not None): 
                    return ReferentToken(attr.prop_ref, attr.begin_token, attr.end_token)
            return None
        if (attrs is not None and t.isChar('(')): 
            pr = PersonAnalyzer._tryAttachPerson(t.next0_, ad, for_ext_ontos, step, for_attribute)
            if (pr is not None and pr.end_token.next0_ is not None and pr.end_token.next0_.isChar(')')): 
                res = PersonHelper._createReferentToken(Utils.asObjectOrNull(pr.referent, PersonReferent), t, pr.end_token.next0_, attrs[0].morph, attrs, ad, True, after_be_predicate)
                if (res is not None): 
                    res.end_token = pr.end_token.next0_
                return res
        tt0 = t0.previous
        if (mi.case_ == MorphCase.ALL_CASES and tt0 is not None): 
            if (tt0 is not None and tt0.is_comma_and): 
                tt0 = tt0.previous
                if (tt0 is not None and (isinstance(tt0.getReferent(), PersonReferent))): 
                    if (not tt0.morph.case_.is_undefined): 
                        mi.case_ = (mi.case_) & tt0.morph.case_
        if ((attrs is not None and t is not None and t.previous is not None) and t.previous.isChar(',')): 
            if (attrs[0].typ != PersonAttrTerminType.BESTREGARDS and not attrs[0].chars.is_latin_letter): 
                if (attrs[0].is_newline_before): 
                    pass
                else: 
                    return None
        if (step == 1): 
            pass
        for k in range(2):
            pits = None
            if ((step < 1) or t.inner_bool): 
                attr = PersonItemToken.ParseAttr.NO
                if (k == 0): 
                    attr = (Utils.valToEnum((attr) | (PersonItemToken.ParseAttr.ALTVAR), PersonItemToken.ParseAttr))
                if (for_ext_ontos or t.chars.is_latin_letter): 
                    attr = (Utils.valToEnum((attr) | (PersonItemToken.ParseAttr.CANBELATIN), PersonItemToken.ParseAttr))
                pits = PersonItemToken.tryAttachList(t, (None if ad is None else ad.local_ontology), attr, 10)
                if (pits is not None and step == 0): 
                    t.inner_bool = True
            if (pits is None): 
                continue
            if (not for_ext_ontos): 
                pass
            if ((step == 0 and len(pits) == 1 and attrs is not None) and attrs[len(attrs) - 1].end_token == t.previous and pits[0].end_token == t): 
                stat = t.kit.statistics.getWordInfo(t)
                if (stat is not None): 
                    stat.has_before_person_attr = True
                if (ad is not None): 
                    ad.need_second_step = True
            if (pits is not None and len(pits) == 1 and pits[0].firstname is not None): 
                if (pits[0].end_token.next0_ is not None and pits[0].end_token.next0_.is_and and (isinstance(pits[0].end_token.next0_.next0_, ReferentToken))): 
                    pr = Utils.asObjectOrNull(pits[0].end_token.next0_.next0_.getReferent(), PersonReferent)
                    if (pr is not None): 
                        if (len(pits[0].firstname.vars0_) < 1): 
                            return None
                        v = pits[0].firstname.vars0_[0]
                        pers = PersonReferent()
                        bi = MorphBaseInfo._new2468(v.gender, MorphNumber.SINGULAR, pits[0].kit.base_language)
                        bi.class0_ = MorphClass._new2427(True)
                        if (v.gender == MorphGender.MASCULINE): 
                            pers.is_male = True
                        elif (v.gender == MorphGender.FEMINIE): 
                            pers.is_female = True
                        for s in pr.slots: 
                            if (s.type_name == PersonReferent.ATTR_LASTNAME): 
                                str0_ = Utils.asObjectOrNull(s.value, str)
                                str0 = Morphology.getWordform(str0_, bi)
                                pers.addSlot(s.type_name, str0, False, 0)
                                if (str0 != str0_): 
                                    pers.addSlot(s.type_name, str0_, False, 0)
                        if (len(pers.slots) == 0): 
                            return None
                        pers.addSlot(PersonReferent.ATTR_FIRSTNAME, v.value, False, 0)
                        return PersonHelper._createReferentToken(pers, pits[0].begin_token, pits[0].end_token, pits[0].firstname.morph, attrs, ad, for_attribute, after_be_predicate)
                attr = (attrs[len(attrs) - 1] if attrs is not None and len(attrs) > 0 else None)
                if ((attr is not None and attr.prop_ref is not None and attr.prop_ref.kind == PersonPropertyKind.KIN) and (isinstance(attr.prop_ref.getSlotValue(PersonPropertyReferent.ATTR_REF), PersonReferent)) and attr.gender != MorphGender.UNDEFINED): 
                    pr = Utils.asObjectOrNull(attr.prop_ref.getSlotValue(PersonPropertyReferent.ATTR_REF), PersonReferent)
                    pers = PersonReferent()
                    bi = MorphBaseInfo._new2470(MorphNumber.SINGULAR, attr.gender, attr.kit.base_language)
                    bi.class0_ = MorphClass._new2427(True)
                    for s in pr.slots: 
                        if (s.type_name == PersonReferent.ATTR_LASTNAME): 
                            sur = Utils.asObjectOrNull(s.value, str)
                            sur0 = Morphology.getWordform(sur, bi)
                            pers.addSlot(s.type_name, sur0, False, 0)
                            if (sur0 != sur): 
                                pers.addSlot(s.type_name, sur, False, 0)
                    v = pits[0].firstname.vars0_[0]
                    pers.addSlot(PersonReferent.ATTR_FIRSTNAME, v.value, False, 0)
                    if (attr.gender == MorphGender.MASCULINE): 
                        pers.is_male = True
                    elif (attr.gender == MorphGender.FEMINIE): 
                        pers.is_female = True
                    return PersonHelper._createReferentToken(pers, pits[0].begin_token, pits[0].end_token, pits[0].firstname.morph, attrs, ad, for_attribute, after_be_predicate)
            if (mi.case_.is_undefined): 
                if (pits[0].is_newline_before and pits[len(pits) - 1].end_token.is_newline_after): 
                    mi.case_ = MorphCase.NOMINATIVE
            if (ad is not None): 
                if (len(pits) == 1): 
                    pass
                if (for_attribute and len(pits) > 1): 
                    tmp = list()
                    pit0 = None
                    i = 0
                    while i < len(pits): 
                        tmp.append(pits[i])
                        pit = PersonIdentityToken.tryAttachOntoInt(tmp, 0, mi, ad.local_ontology)
                        if (pit is not None): 
                            pit0 = pit
                        i += 1
                    if (pit0 is not None): 
                        return PersonHelper._createReferentToken(pit0.ontology_person, pit0.begin_token, pit0.end_token, pit0.morph, attrs, ad, for_attribute, after_be_predicate)
                i = 0
                while (i < len(pits)) and (i < 3): 
                    pit = PersonIdentityToken.tryAttachOntoInt(pits, i, mi, ad.local_ontology)
                    if (pit is not None): 
                        return PersonHelper._createReferentToken(pit.ontology_person, pit.begin_token, pit.end_token, pit.morph, (attrs if pit.begin_token == pits[0].begin_token else None), ad, for_attribute, after_be_predicate)
                    i += 1
                if (len(pits) == 1 and not for_ext_ontos): 
                    pp = PersonIdentityToken.tryAttachOntoForSingle(pits[0], ad.local_ontology)
                    if (pp is not None): 
                        return PersonHelper._createReferentToken(pp, pits[0].begin_token, pits[0].end_token, pits[0].morph, attrs, ad, for_attribute, after_be_predicate)
                if ((len(pits) == 1 and not for_ext_ontos and attrs is not None) and pits[0].chars.is_latin_letter and attrs[0].chars.is_latin_letter): 
                    pp = PersonIdentityToken.tryAttachLatinSurname(pits[0], ad.local_ontology)
                    if (pp is not None): 
                        return PersonHelper._createReferentToken(pp, pits[0].begin_token, pits[0].end_token, pits[0].morph, attrs, ad, for_attribute, after_be_predicate)
                if (len(pits) == 2 and not for_ext_ontos): 
                    pp = PersonIdentityToken.tryAttachOntoForDuble(pits[0], pits[1], ad.local_ontology)
                    if (pp is not None): 
                        return PersonHelper._createReferentToken(pp, pits[0].begin_token, pits[1].end_token, pits[0].morph, attrs, ad, for_attribute, after_be_predicate)
            if (pits[0].begin_token.kit.ontology is not None): 
                i = 0
                while i < len(pits): 
                    pit = PersonIdentityToken.tryAttachOntoExt(pits, i, mi, pits[0].begin_token.kit.ontology)
                    if (pit is not None): 
                        return PersonHelper._createReferentToken(pit.ontology_person, pit.begin_token, pit.end_token, pit.morph, attrs, ad, for_attribute, after_be_predicate)
                    i += 1
            pli0 = PersonIdentityToken.tryAttach(pits, 0, mi, t0, is_king, attrs is not None)
            if (t.previous is None and ((ad is not None and ad.text_starts_with_lastname_firstname_middlename)) and len(pits) == 3): 
                exi = False
                for pit in pli0: 
                    if (pit.typ == FioTemplateType.SURNAMENAMESECNAME): 
                        pit.coef += (10)
                        exi = True
                if (not exi): 
                    pit = PersonIdentityToken.createTyp(pits, FioTemplateType.SURNAMENAMESECNAME, mi)
                    if (pit is not None): 
                        pit.coef = (10)
                        pli0.append(pit)
            if (for_ext_ontos): 
                te = False
                if (pli0 is None or len(pli0) == 0): 
                    te = True
                else: 
                    PersonIdentityToken.sort(pli0)
                    if (pli0[0].coef < 2): 
                        te = True
                if (te): 
                    pli0 = PersonIdentityToken.tryAttachForExtOnto(pits)
            if (for_ext_ontos and pli0 is not None): 
                et = pits[len(pits) - 1].end_token
                for pit in pli0: 
                    if (pit.end_token == et): 
                        pit.coef += (1)
            pli = pli0
            pli1 = None
            if (not for_ext_ontos and ((attrs is None or attrs[len(attrs) - 1].typ == PersonAttrTerminType.POSITION))): 
                if ((len(pits) == 4 and pits[0].firstname is not None and pits[1].firstname is None) and pits[2].firstname is not None and pits[3].firstname is None): 
                    pass
                else: 
                    pli1 = PersonIdentityToken.tryAttach(pits, 1, mi, t0, is_king, attrs is not None)
                    if (pli0 is not None and pli1 is not None and len(pli1) > 0): 
                        PersonIdentityToken.correctXFML(pli0, pli1, attrs)
            if (pli is None): 
                pli = pli1
            elif (pli1 is not None): 
                pli.extend(pli1)
            if (((pli is None or len(pli) == 0)) and len(pits) == 1 and pits[0].firstname is not None): 
                if (is_king): 
                    first = PersonIdentityToken(pits[0].begin_token, pits[0].end_token)
                    PersonIdentityToken.manageFirstname(first, pits[0], mi)
                    first.coef = (2)
                    if (first.morph.gender == MorphGender.UNDEFINED and first.firstname is not None): 
                        first.morph.gender = first.firstname.gender
                    pli.append(first)
                    sur = (None if (attrs is None or len(attrs) == 0) else attrs[len(attrs) - 1]._king_surname)
                    if (sur is not None): 
                        PersonIdentityToken.manageLastname(first, sur, mi)
                elif (attrs is not None): 
                    for a in attrs: 
                        if (a.can_be_same_surname and a.referent is not None): 
                            pr0 = Utils.asObjectOrNull(a.referent.getSlotValue(PersonPropertyReferent.ATTR_REF), PersonReferent)
                            if (pr0 is not None): 
                                first = PersonIdentityToken(pits[0].begin_token, pits[0].end_token)
                                PersonIdentityToken.manageFirstname(first, pits[0], mi)
                                first.coef = (2)
                                pli.append(first)
                                first.lastname = PersonMorphCollection()
                                for v in pr0.slots: 
                                    if (v.type_name == PersonReferent.ATTR_LASTNAME): 
                                        first.lastname.add(v.value, None, (MorphGender.MASCULINE if pr0.is_male else ((MorphGender.FEMINIE if pr0.is_female else MorphGender.UNDEFINED))), True)
            if (pli is not None and len(pli) > 0): 
                PersonIdentityToken.sort(pli)
                best = pli[0]
                min_coef = 2
                if ((best.coef < min_coef) and ((attrs is not None or for_ext_ontos))): 
                    pit = PersonIdentityToken.tryAttachIdentity(pits, mi)
                    if (pit is not None and pit.coef > best.coef and pit.coef > 0): 
                        pers = PersonReferent()
                        pers._addIdentity(pit.lastname)
                        return PersonHelper._createReferentToken(pers, pit.begin_token, pit.end_token, pit.morph, attrs, ad, for_attribute, after_be_predicate)
                    if ((best.kit.base_language.is_en and best.typ == FioTemplateType.NAMESURNAME and attrs is not None) and attrs[0].typ == PersonAttrTerminType.BESTREGARDS): 
                        best.coef += (10)
                    if (best.coef >= 0): 
                        best.coef += ((1 if best.chars.is_all_upper else 2))
                if (best.coef >= 0 and (best.coef < min_coef)): 
                    tee = best.end_token.next0_
                    tee1 = None
                    if (tee is not None and tee.isChar('(')): 
                        br = BracketHelper.tryParse(tee, BracketParseAttr.NO, 100)
                        if (br is not None and (br.length_char < 100)): 
                            tee1 = br.begin_token.next0_
                            tee = br.end_token.next0_
                    if (isinstance(tee, TextToken)): 
                        if (tee.isCharOf(":,") or tee.is_hiphen or (tee).is_verb_be): 
                            tee = tee.next0_
                    att = PersonAttrToken.tryAttach(tee, (None if ad is None else ad.local_ontology), PersonAttrToken.PersonAttrAttachAttrs.NO)
                    if (att is None and tee1 is not None): 
                        att = PersonAttrToken.tryAttach(tee1, (None if ad is None else ad.local_ontology), PersonAttrToken.PersonAttrAttachAttrs.NO)
                    if (att is not None): 
                        if (tee == best.end_token.next0_ and not att.morph.case_.is_nominative and not att.morph.case_.is_undefined): 
                            pass
                        else: 
                            best.coef += (2)
                    elif (tee is not None and tee.isValue("АГЕНТ", None)): 
                        best.coef += (1)
                    if (for_attribute): 
                        best.coef += (1)
                if (best.coef >= min_coef): 
                    gender = MorphGender.UNDEFINED
                    i = 0
                    while i < len(pli): 
                        if (pli[i].coef != best.coef): 
                            del pli[i:i+len(pli) - i]
                            break
                        elif (pli[i].probable_gender != MorphGender.UNDEFINED): 
                            gender = (Utils.valToEnum((gender) | (pli[i].probable_gender), MorphGender))
                        i += 1
                    if (len(pli) > 1): 
                        return None
                    if (gender != MorphGender.FEMINIE and gender != MorphGender.MASCULINE): 
                        if ((pli[0].is_newline_before and pli[0].is_newline_after and pli[0].lastname is not None) and pli[0].lastname.has_lastname_standard_tail): 
                            if (len(pli[0].lastname.values) == 2): 
                                pli[0].lastname.remove(None, MorphGender.MASCULINE)
                                gender = MorphGender.FEMINIE
                                if (pli[0].firstname is not None and len(pli[0].firstname.values) == 2): 
                                    pli[0].firstname.remove(None, MorphGender.MASCULINE)
                    if (gender == MorphGender.UNDEFINED): 
                        if (pli[0].firstname is not None and pli[0].lastname is not None): 
                            g = pli[0].firstname.gender
                            if (pli[0].lastname.gender != MorphGender.UNDEFINED): 
                                g = (Utils.valToEnum((g) & (pli[0].lastname.gender), MorphGender))
                            if (g == MorphGender.FEMINIE or g == MorphGender.MASCULINE): 
                                gender = g
                            elif (pli[0].firstname.gender == MorphGender.MASCULINE or pli[0].firstname.gender == MorphGender.FEMINIE): 
                                gender = pli[0].firstname.gender
                            elif (pli[0].lastname.gender == MorphGender.MASCULINE or pli[0].lastname.gender == MorphGender.FEMINIE): 
                                gender = pli[0].lastname.gender
                    pers = PersonReferent()
                    if (gender == MorphGender.MASCULINE): 
                        pers.is_male = True
                    elif (gender == MorphGender.FEMINIE): 
                        pers.is_female = True
                    for v in pli: 
                        if (v.ontology_person is not None): 
                            for s in v.ontology_person.slots: 
                                pers.addSlot(s.type_name, s.value, False, 0)
                        elif (v.typ == FioTemplateType.ASIANNAME): 
                            pers._addIdentity(v.lastname)
                        else: 
                            pers._addFioIdentity(v.lastname, v.firstname, v.middlename)
                            if (v.typ == FioTemplateType.ASIANSURNAMENAME): 
                                pers.addSlot("NAMETYPE", "china", False, 0)
                    if (not for_ext_ontos): 
                        pers._m_person_identity_typ = pli[0].typ
                    if (pli[0].begin_token != pits[0].begin_token and attrs is not None): 
                        if (pits[0].whitespaces_before_count > 2): 
                            attrs = (None)
                        else: 
                            s = pits[0].getSourceText()
                            pat = attrs[len(attrs) - 1]
                            if (pat.typ == PersonAttrTerminType.POSITION and not Utils.isNullOrEmpty(s) and not pat.is_newline_before): 
                                if (pat.value is None and pat.prop_ref is not None): 
                                    while pat is not None: 
                                        if (pat.prop_ref is None): 
                                            break
                                        elif (pat.higher_prop_ref is None): 
                                            str0_ = s.lower()
                                            if (pat.prop_ref.name is not None and not LanguageHelper.endsWith(pat.prop_ref.name, str0_)): 
                                                pat.prop_ref.name = pat.prop_ref.name + (" " + str0_)
                                            if (pat.add_outer_org_as_ref): 
                                                pat.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, None, True, 0)
                                                pat.add_outer_org_as_ref = False
                                            break
                                        pat = pat.higher_prop_ref
                                elif (pat.value is not None): 
                                    pat.value = "{0} {1}".format(pat.value, s.lower())
                                pat.end_token = pits[0].end_token
                    latin = PersonIdentityToken.checkLatinAfter(pli[0])
                    if (latin is not None): 
                        pers._addFioIdentity(latin.lastname, latin.firstname, latin.middlename)
                    return PersonHelper._createReferentToken(pers, pli[0].begin_token, (latin.end_token if latin is not None else pli[0].end_token), pli[0].morph, attrs, ad, for_attribute, after_be_predicate)
        if (attrs is not None): 
            attr = attrs[len(attrs) - 1]
            if (attr.can_be_single_person and attr.prop_ref is not None): 
                return ReferentToken._new746(attr.prop_ref, attr.begin_token, attr.end_token, attr.morph)
        return None
    
    def processOntologyItem(self, begin : 'Token') -> 'ReferentToken':
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        if (begin is None): 
            return None
        rt = PersonAnalyzer._tryAttachPerson(begin, None, True, -1, False)
        if (rt is None): 
            pat = PersonAttrToken.tryAttach(begin, None, PersonAttrToken.PersonAttrAttachAttrs.NO)
            if (pat is not None and pat.prop_ref is not None): 
                return ReferentToken(pat.prop_ref, pat.begin_token, pat.end_token)
            return None
        t = rt.end_token.next0_
        while t is not None: 
            if (t.isChar(';') and t.next0_ is not None): 
                rt1 = PersonAnalyzer._tryAttachPerson(t.next0_, None, True, -1, False)
                if (rt1 is not None and rt1.referent.type_name == rt.referent.type_name): 
                    rt.referent.mergeSlots(rt1.referent, True)
                    rt.end_token = rt1.end_token
                    t = rt.end_token
                elif (rt1 is not None): 
                    t = rt1.end_token
            t = t.next0_
        return rt
    
    M_INITED = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        from pullenti.ner.person.internal.PersonPropAnalyzer import PersonPropAnalyzer
        from pullenti.ner.person.internal.PersonIdToken import PersonIdToken
        if (PersonAnalyzer.M_INITED): 
            return
        PersonAnalyzer.M_INITED = True
        try: 
            MetaPerson.initialize()
            MetaPersonIdentity.initialize()
            MetaPersonProperty.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            PersonItemToken._initialize()
            PersonAttrToken.initialize()
            ShortNameHelper.initialize()
            PersonIdToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
            MailLine.initialize()
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        ProcessorService.registerAnalyzer(PersonAnalyzer())
        ProcessorService.registerAnalyzer(PersonPropAnalyzer())