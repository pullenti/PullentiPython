# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
import xml.etree
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.person.internal.PersonAttrTerminType import PersonAttrTerminType
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.person.PersonPropertyKind import PersonPropertyKind
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.person.internal.PersonAttrTerminType2 import PersonAttrTerminType2
from pullenti.ner.person.internal.EpNerPersonInternalResourceHelper import EpNerPersonInternalResourceHelper
from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper


class PersonAttrToken(ReferentToken):
    
    class PersonAttrAttachAttrs(IntEnum):
        NO = 0
        AFTERZAMESTITEL = 1
        ONLYKEYWORD = 2
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(None, begin, end, None)
        self.typ = PersonAttrTerminType.PREFIX
        self.gender = MorphGender.UNDEFINED
        self.value = None;
        self._king_surname = None;
        self.age = None;
        self.higher_prop_ref = None;
        self.add_outer_org_as_ref = False
        self.anafor = None;
        self.__m_can_be_independent_property = False
        self.can_be_single_person = False
        self.can_has_person_after = 0
        self.can_be_same_surname = False
        self.is_doubt = False
    
    @property
    def prop_ref(self) -> 'PersonPropertyReferent':
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        return Utils.asObjectOrNull(self.referent, PersonPropertyReferent)
    @prop_ref.setter
    def prop_ref(self, value_) -> 'PersonPropertyReferent':
        self.referent = (value_)
        return value_
    
    @property
    def can_be_independent_property(self) -> bool:
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        if (self.prop_ref is None): 
            return False
        if (self.morph.number == MorphNumber.PLURAL): 
            return False
        if (self.higher_prop_ref is not None and self.higher_prop_ref.can_be_independent_property): 
            return True
        if (self.can_be_single_person): 
            return True
        if (self.typ != PersonAttrTerminType.POSITION): 
            return False
        if (not self.__m_can_be_independent_property): 
            if (self.prop_ref.kind == PersonPropertyKind.BOSS): 
                return True
            return False
        if (self.prop_ref.findSlot(PersonPropertyReferent.ATTR_REF, None, True) is not None): 
            if (self.prop_ref.name != "член"): 
                return True
        return False
    @can_be_independent_property.setter
    def can_be_independent_property(self, value_) -> bool:
        self.__m_can_be_independent_property = value_
        return value_
    
    def __str__(self) -> str:
        if (self.referent is not None): 
            return super().__str__()
        res = io.StringIO()
        print("{0}: {1}".format(Utils.enumToString(self.typ), Utils.ifNotNull(self.value, "")), end="", file=res, flush=True)
        if (self.prop_ref is not None): 
            print(" Ref: {0}".format(str(self.prop_ref)), end="", file=res, flush=True)
        if (self.gender != MorphGender.UNDEFINED): 
            print("; {0}".format(Utils.enumToString(self.gender)), end="", file=res, flush=True)
        if (self.can_has_person_after >= 0): 
            print("; MayBePersonAfter={0}".format(self.can_has_person_after), end="", file=res, flush=True)
        if (self.can_be_same_surname): 
            print("; CanHasLikeSurname", end="", file=res)
        if (self.__m_can_be_independent_property): 
            print("; CanBeIndependent", end="", file=res)
        if (self.is_doubt): 
            print("; Doubt", end="", file=res)
        if (self.age is not None): 
            print("; Age={0}".format(self.age), end="", file=res, flush=True)
        if (not self.morph.case_.is_undefined): 
            print("; {0}".format(str(self.morph.case_)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def saveToLocalOntology(self) -> None:
        ad = self.data
        if (ad is None or self.prop_ref is None or self.higher_prop_ref is None): 
            super().saveToLocalOntology()
            return
        li = list()
        pr = self
        while pr is not None and pr.prop_ref is not None: 
            li.insert(0, pr)
            pr = pr.higher_prop_ref
        i = 0
        while i < len(li): 
            li[i].data = ad
            li[i].higher_prop_ref = (None)
            li[i].saveToLocalOntology()
            if ((i + 1) < len(li)): 
                li[i + 1].prop_ref.higher = li[i].prop_ref
            i += 1
    
    @staticmethod
    def tryAttach(t : 'Token', loc_onto : 'IntOntologyCollection', attrs : 'PersonAttrAttachAttrs'=PersonAttrAttachAttrs.NO) -> 'PersonAttrToken':
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        from pullenti.ner.Referent import Referent
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.person.PersonAnalyzer import PersonAnalyzer
        if (t is None): 
            return None
        olev = None
        lev = 0
        wrapolev2259 = RefOutArgWrapper(None)
        inoutres2260 = Utils.tryGetValue(t.kit.misc_data, "pat", wrapolev2259)
        olev = wrapolev2259.value
        if (not inoutres2260): 
            lev = 1
            t.kit.misc_data["pat"] = lev
        else: 
            lev = (olev)
            if (lev > 2): 
                return None
            lev += 1
            t.kit.misc_data["pat"] = (lev)
        res = PersonAttrToken.__TryAttach(t, loc_onto, attrs)
        lev -= 1
        if (lev < 0): 
            lev = 0
        t.kit.misc_data["pat"] = (lev)
        if (res is None): 
            if (t.morph.class0_.is_noun): 
                aterr = Utils.asObjectOrNull(t.kit.processor.findAnalyzer("GEO"), GeoAnalyzer)
                if (aterr is not None): 
                    rt = aterr.processCitizen(t)
                    if (rt is not None): 
                        res = PersonAttrToken._new2256(rt.begin_token, rt.end_token, rt.morph)
                        res.prop_ref = PersonPropertyReferent()
                        res.prop_ref.addSlot(PersonPropertyReferent.ATTR_NAME, ("громадянин" if t.kit.base_language.is_ua else "гражданин"), True, 0)
                        res.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, rt.referent, True, 0)
                        res.prop_ref.addExtReferent(rt)
                        res.typ = PersonAttrTerminType.POSITION
                        if ((res.end_token.next0_ is not None and res.end_token.next0_.isValue("ПО", None) and res.end_token.next0_.next0_ is not None) and res.end_token.next0_.next0_.isValue("ПРОИСХОЖДЕНИЕ", None)): 
                            res.end_token = res.end_token.next0_.next0_
                        return res
            if (((((isinstance(t, TextToken))) and (Utils.asObjectOrNull(t, TextToken)).term == "АК" and t.next0_ is not None) and t.next0_.isChar('.') and t.next0_.next0_ is not None) and not t.next0_.next0_.chars.is_all_lower): 
                res = PersonAttrToken._new2257(t, t.next0_, PersonAttrTerminType.POSITION)
                res.prop_ref = PersonPropertyReferent._new2258("академик")
                return res
            if ((isinstance(t, TextToken)) and t.next0_ is not None): 
                if (((t.isValue("ВИЦЕ", "ВІЦЕ") or t.isValue("ЭКС", "ЕКС") or t.isValue("ГЕН", None)) or t.isValue("VICE", None) or t.isValue("EX", None)) or t.isValue("DEPUTY", None)): 
                    tt = t.next0_
                    if (tt.is_hiphen or tt.isChar('.')): 
                        tt = tt.next0_
                    res = PersonAttrToken.__TryAttach(tt, loc_onto, attrs)
                    if (res is not None and res.prop_ref is not None): 
                        res.begin_token = t
                        if (t.isValue("ГЕН", None)): 
                            res.prop_ref.name = "генеральный {0}".format(res.prop_ref.name)
                        else: 
                            res.prop_ref.name = "{0}-{1}".format((Utils.asObjectOrNull(t, TextToken)).term.lower(), res.prop_ref.name)
                        return res
            if (t.isValue("ГВАРДИИ", "ГВАРДІЇ")): 
                res = PersonAttrToken.__TryAttach(t.next0_, loc_onto, attrs)
                if (res is not None): 
                    if (res.prop_ref is not None and res.prop_ref.kind == PersonPropertyKind.MILITARYRANK): 
                        res.begin_token = t
                        return res
            tt1 = t
            if (tt1.morph.class0_.is_preposition and tt1.next0_ is not None): 
                tt1 = tt1.next0_
            if ((tt1.next0_ is not None and tt1.isValue("НАЦИОНАЛЬНОСТЬ", "НАЦІОНАЛЬНІСТЬ")) or tt1.isValue("ПРОФЕССИЯ", "ПРОФЕСІЯ") or tt1.isValue("СПЕЦИАЛЬНОСТЬ", "СПЕЦІАЛЬНІСТЬ")): 
                tt1 = tt1.next0_
                if (tt1 is not None): 
                    if (tt1.is_hiphen or tt1.isChar(':')): 
                        tt1 = tt1.next0_
                res = PersonAttrToken.__TryAttach(tt1, loc_onto, attrs)
                if (res is not None): 
                    res.begin_token = t
                    return res
            return None
        if (res.typ == PersonAttrTerminType.OTHER and res.age is not None and res.value is None): 
            res1 = PersonAttrToken.__TryAttach(res.end_token.next0_, loc_onto, attrs)
            if (res1 is not None): 
                res1.begin_token = res.begin_token
                res1.age = res.age
                res = res1
        if (res.begin_token.isValue("ГЛАВА", None)): 
            if (isinstance(t.previous, NumberToken)): 
                return None
        elif (res.begin_token.isValue("АДВОКАТ", None)): 
            if (t.previous is not None): 
                if (t.previous.isValue("РЕЕСТР", "РЕЄСТР") or t.previous.isValue("УДОСТОВЕРЕНИЕ", "ПОСВІДЧЕННЯ")): 
                    return None
        mc = res.begin_token.getMorphClassInDictionary()
        if (mc.is_adjective): 
            npt = NounPhraseHelper.tryParse(res.begin_token, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.end_char > res.end_char): 
                if (PersonAttrToken.M_TERMINS.tryParse(npt.end_token, TerminParseAttr.NO) is None): 
                    return None
        if (res.typ == PersonAttrTerminType.PREFIX and (((((res.value == "ГРАЖДАНИН" or res.value == "ГРАЖДАНКА" or res.value == "УРОЖЕНЕЦ") or res.value == "УРОЖЕНКА" or res.value == "ГРОМАДЯНИН") or res.value == "ГРОМАДЯНКА" or res.value == "УРОДЖЕНЕЦЬ") or res.value == "УРОДЖЕНКА")) and res.end_token.next0_ is not None): 
            tt = res.end_token.next0_
            if (((tt is not None and tt.isChar('(') and tt.next0_ is not None) and tt.next0_.isValue("КА", None) and tt.next0_.next0_ is not None) and tt.next0_.next0_.isChar(')')): 
                res.end_token = tt.next0_.next0_
                tt = res.end_token.next0_
            r = (None if tt is None else tt.getReferent())
            if (r is not None and r.type_name == PersonAttrToken.OBJ_NAME_GEO): 
                res.end_token = tt
                res.prop_ref = PersonPropertyReferent()
                res.prop_ref.addSlot(PersonPropertyReferent.ATTR_NAME, res.value.lower(), True, 0)
                res.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, r, True, 0)
                res.typ = PersonAttrTerminType.POSITION
                ttt = tt.next0_
                while ttt is not None: 
                    if (not ttt.is_comma_and or ttt.next0_ is None): 
                        break
                    ttt = ttt.next0_
                    r = ttt.getReferent()
                    if (r is None or r.type_name != PersonAttrToken.OBJ_NAME_GEO): 
                        break
                    res.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                    tt = ttt
                    res.end_token = tt
                    if (ttt.previous.is_and): 
                        break
                    ttt = ttt.next0_
            elif ((tt is not None and tt.is_and and tt.next0_ is not None) and tt.next0_.isValue("ЖИТЕЛЬ", None)): 
                aaa = PersonAttrToken.__TryAttach(tt.next0_, loc_onto, attrs)
                if (aaa is not None and aaa.prop_ref is not None): 
                    aaa.begin_token = res.begin_token
                    aaa.value = res.value
                    aaa.prop_ref.name = aaa.value.lower()
                    res = aaa
        if (res.typ == PersonAttrTerminType.KING or res.typ == PersonAttrTerminType.POSITION): 
            if (res.begin_token == res.end_token and res.chars.is_capital_upper and res.whitespaces_after_count == 1): 
                pit = PersonItemToken.tryAttach(t, loc_onto, PersonItemToken.ParseAttr.IGNOREATTRS, None)
                if (pit is not None and pit.lastname is not None and pit.lastname.is_lastname_has_std_tail): 
                    rt1 = t.kit.processReferent("PERSON", t.next0_)
                    if (rt1 is not None and (isinstance(rt1.referent, PersonReferent))): 
                        pass
                    else: 
                        return None
        if (res.prop_ref is None): 
            return res
        if (res.chars.is_latin_letter): 
            tt = res.end_token.next0_
            if (tt is not None and tt.is_hiphen): 
                tt = tt.next0_
            if (tt is not None and tt.isValue("ELECT", None)): 
                res.end_token = tt
        if (not res.begin_token.chars.is_all_lower): 
            pat = PersonItemToken.tryAttach(res.begin_token, loc_onto, PersonItemToken.ParseAttr.IGNOREATTRS, None)
            if (pat is not None and pat.lastname is not None): 
                if (pat.lastname.is_in_dictionary or pat.lastname.is_in_ontology): 
                    if (PersonAttrToken.checkKind(res.prop_ref) != PersonPropertyKind.KING): 
                        return None
        s = str(res.prop_ref)
        if (s == "глава книги"): 
            return None
        if (s == "глава" and res.prop_ref.findSlot(PersonPropertyReferent.ATTR_REF, None, True) is None): 
            return None
        if (((s == "королева" or s == "король" or s == "князь")) and res.chars.is_capital_upper): 
            pits = PersonItemToken.tryAttachList(res.end_token.next0_, loc_onto, PersonItemToken.ParseAttr.NO, 10)
            if (pits is not None and len(pits) > 0): 
                if (pits[0].typ == PersonItemToken.ItemType.INITIAL): 
                    return None
                if (pits[0].firstname is not None): 
                    if (len(pits) == 1): 
                        return None
                    if (len(pits) == 2 and pits[1].middlename is not None): 
                        return None
            if (not MiscHelper.canBeStartOfSentence(t)): 
                return None
        if (s == "друг" or s.startswith("друг ")): 
            if (t.previous is not None): 
                if (t.previous.isValue("ДРУГ", None)): 
                    return None
                if (t.previous.morph.class0_.is_preposition and t.previous.previous is not None and t.previous.previous.isValue("ДРУГ", None)): 
                    return None
            if (t.next0_ is not None): 
                if (t.next0_.isValue("ДРУГ", None)): 
                    return None
                if (t.next0_.morph.class0_.is_preposition and t.next0_.next0_ is not None and t.next0_.next0_.isValue("ДРУГ", None)): 
                    return None
        if (res.chars.is_latin_letter and ((res.is_doubt or s == "senior")) and (res.whitespaces_after_count < 2)): 
            if (res.prop_ref is not None and len(res.prop_ref.slots) == 1): 
                tt2 = res.end_token.next0_
                if (MiscHelper.isEngAdjSuffix(tt2)): 
                    tt2 = tt2.next0_.next0_
                res2 = PersonAttrToken.__TryAttach(tt2, loc_onto, attrs)
                if ((res2 is not None and res2.chars.is_latin_letter and res2.typ == res.typ) and res2.prop_ref is not None): 
                    res2.prop_ref.name = "{0} {1}".format(Utils.ifNotNull(res.prop_ref.name, ""), Utils.ifNotNull(res2.prop_ref.name, "")).strip()
                    res2.begin_token = res.begin_token
                    res = res2
        if (res.prop_ref.name == "министр"): 
            rt1 = res.kit.processReferent("ORGANIZATION", res.end_token.next0_)
            if (rt1 is not None and rt1.referent.findSlot("TYPE", "министерство", True) is not None): 
                t1 = rt1.end_token
                if (isinstance(t1.getReferent(), GeoReferent)): 
                    t1 = t1.previous
                if (rt1.begin_char < t1.end_char): 
                    add_str = MiscHelper.getTextValue(rt1.begin_token, t1, GetTextAttr.NO)
                    if (add_str is not None): 
                        res.prop_ref.name = res.prop_ref.name + (" " + add_str.lower())
                        res.end_token = t1
        p = res.prop_ref
        while p is not None: 
            if (p.name is not None and " - " in p.name): 
                p.name = p.name.replace(" - ", "-")
            p = p.higher
        if (res.begin_token.morph.class0_.is_adjective): 
            r = res.kit.processReferent("GEO", res.begin_token)
            if (r is not None): 
                res.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, r.referent, False, 0)
                res.prop_ref.addExtReferent(r)
                i = res.prop_ref.name.find(' ')
                if (i > 0): 
                    res.prop_ref.name = res.prop_ref.name[i:].strip()
        contains_geo = False
        for ss in res.prop_ref.slots: 
            if (isinstance(ss.value, Referent)): 
                if ((Utils.asObjectOrNull(ss.value, Referent)).type_name == PersonAttrToken.OBJ_NAME_GEO): 
                    contains_geo = True
                    break
        if (not contains_geo and (res.end_token.whitespaces_after_count < 2)): 
            if ((isinstance(res.end_token.next0_, ReferentToken)) and res.end_token.next0_.getReferent().type_name == PersonAttrToken.OBJ_NAME_GEO): 
                res.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, res.end_token.next0_.getReferent(), False, 0)
                res.end_token = res.end_token.next0_
        if (res.end_token.whitespaces_after_count < 2): 
            te = res.end_token.next0_
            if (te is not None and te.isValue("В", None)): 
                te = te.next0_
                if ((isinstance(te, ReferentToken)) and ((te.getReferent().type_name == PersonAttrToken.OBJ_NAME_DATE or te.getReferent().type_name == PersonAttrToken.OBJ_NAME_DATE_RANGE))): 
                    res.end_token = te
            elif (te is not None and te.isChar('(')): 
                te = te.next0_
                if (((isinstance(te, ReferentToken)) and ((te.getReferent().type_name == PersonAttrToken.OBJ_NAME_DATE or te.getReferent().type_name == PersonAttrToken.OBJ_NAME_DATE_RANGE)) and te.next0_ is not None) and te.next0_.isChar(')')): 
                    res.end_token = te.next0_
                elif (isinstance(te, NumberToken)): 
                    rt1 = te.kit.processReferent("DATE", te)
                    if (rt1 is not None and rt1.end_token.next0_ is not None and rt1.end_token.next0_.isChar(')')): 
                        res.end_token = rt1.end_token.next0_
        if (res.prop_ref is not None and res.prop_ref.name == "отец"): 
            is_king = False
            tt = res.end_token.next0_
            if ((isinstance(tt, TextToken)) and tt.getMorphClassInDictionary().is_proper_name): 
                if (not ((res.morph.case_) & tt.morph.case_).is_undefined): 
                    if (not tt.morph.case_.is_genitive): 
                        is_king = True
            if (is_king): 
                res.prop_ref.name = "священник"
        if (res.prop_ref is not None and res.prop_ref.kind == PersonPropertyKind.KING): 
            t1 = res.end_token.next0_
            if (res.prop_ref.name == "отец"): 
                if (t1 is None or not t1.chars.is_capital_upper): 
                    return None
                if (((res.morph.case_) & t1.morph.case_).is_undefined): 
                    return None
                res.prop_ref.name = "священник"
                return res
            if (t1 is not None and t1.chars.is_capital_upper and t1.morph.class0_.is_adjective): 
                res._king_surname = PersonItemToken.tryAttach(t1, loc_onto, PersonItemToken.ParseAttr.IGNOREATTRS, None)
                if ((res._king_surname) is not None): 
                    res.end_token = t1
                    if ((t1.next0_ is not None and t1.next0_.is_and and t1.next0_.next0_ is not None) and t1.next0_.next0_.isValue("ВСЕЯ", None)): 
                        t1 = t1.next0_.next0_.next0_
                        geo_ = Utils.asObjectOrNull(((None if t1 is None else t1.getReferent())), GeoReferent)
                        if (geo_ is not None): 
                            res.end_token = t1
                            res.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, geo_, False, 0)
        if (res.can_has_person_after > 0 and res.prop_ref.findSlot(PersonPropertyReferent.ATTR_REF, None, True) is None): 
            npt = NounPhraseHelper.tryParse(res.begin_token, NounPhraseParseAttr.NO, 0)
            tt0 = res.begin_token
            if ((isinstance(tt0, TextToken)) and tt0.morph.class0_.is_personal_pronoun and ((tt0.isValue("ОН", None) or tt0.isValue("ОНА", None)))): 
                pass
            else: 
                tt0 = tt0.previous
                if ((isinstance(tt0, TextToken)) and tt0.morph.class0_.is_personal_pronoun and ((tt0.isValue("ОН", None) or tt0.isValue("ОНА", None)))): 
                    pass
                elif ((isinstance(tt0, TextToken)) and tt0.morph.class0_.is_pronoun and tt0.isValue("СВОЙ", None)): 
                    pass
                else: 
                    tt0 = (None)
            if (tt0 is not None): 
                gen = MorphGender.UNDEFINED
                cou = 0
                for wf in tt0.morph.items: 
                    if (wf.class0_.is_personal_pronoun or wf.class0_.is_pronoun): 
                        gen = wf.gender
                        if (((gen)) == MorphGender.NEUTER): 
                            gen = MorphGender.MASCULINE
                        break
                tt = tt0.previous
                first_pass3099 = True
                while True:
                    if first_pass3099: first_pass3099 = False
                    else: tt = tt.previous; cou += 1
                    if (not (tt is not None and (cou < 200))): break
                    pr = Utils.asObjectOrNull(tt.getReferent(), PersonPropertyReferent)
                    if (pr is not None): 
                        if ((((tt.morph.gender) & (gen))) == (MorphGender.UNDEFINED)): 
                            continue
                        break
                    p = Utils.asObjectOrNull(tt.getReferent(), PersonReferent)
                    if (p is None): 
                        continue
                    if (gen == MorphGender.FEMINIE): 
                        if (p.is_male and not p.is_female): 
                            continue
                    elif (gen == MorphGender.MASCULINE): 
                        if (p.is_female and not p.is_male): 
                            continue
                    else: 
                        break
                    res.begin_token = tt0
                    res.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, p, False, 0)
                    res.can_be_independent_property = True
                    if (res.morph.number != MorphNumber.PLURAL): 
                        res.can_be_single_person = True
                    npt = NounPhraseHelper.tryParse(tt0, NounPhraseParseAttr.NO, 0)
                    if (npt is not None and npt.begin_token != npt.end_token): 
                        res.morph = npt.morph
                    break
            elif (res.whitespaces_after_count == 1): 
                pa = Utils.asObjectOrNull(res.kit.processor.findAnalyzer("PERSON"), PersonAnalyzer)
                if (pa is not None): 
                    t1 = res.end_token.next0_
                    pr = PersonAnalyzer._tryAttachPerson(t1, Utils.asObjectOrNull(res.kit.getAnalyzerData(pa), PersonAnalyzer.PersonAnalyzerData), False, 0, True)
                    if (pr is not None and res.can_has_person_after == 1): 
                        if (pr.begin_token == t1): 
                            if (not pr.morph.case_.is_genitive and not pr.morph.case_.is_undefined): 
                                pr = (None)
                            elif (not pr.morph.case_.is_undefined and not ((res.morph.case_) & pr.morph.case_).is_undefined): 
                                if (PersonAnalyzer._tryAttachPerson(pr.end_token.next0_, Utils.asObjectOrNull(res.kit.getAnalyzerData(pa), PersonAnalyzer.PersonAnalyzerData), False, 0, True) is not None): 
                                    pass
                                else: 
                                    pr = (None)
                        elif (pr.begin_token.previous == t1): 
                            pr = (None)
                            res.prop_ref.name = "{0} {1}".format(res.prop_ref.name, t1.getSourceText().lower())
                            res.end_token = t1
                        else: 
                            pr = (None)
                    if (pr is not None): 
                        res.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, pr, False, 0)
                        res.end_token = pr.end_token
                        res.can_be_independent_property = True
                        if (res.morph.number != MorphNumber.PLURAL): 
                            res.can_be_single_person = True
        if (res.prop_ref.higher is None and res.prop_ref.kind == PersonPropertyKind.BOSS and res.prop_ref.findSlot(PersonPropertyReferent.ATTR_REF, None, True) is None): 
            tok = PersonAttrToken.M_TERMINS.tryParse(res.begin_token, TerminParseAttr.NO)
            if (tok is not None and tok.end_token == res.end_token): 
                cou = 0
                refs = list()
                tt = tok.begin_token.previous
                first_pass3100 = True
                while True:
                    if first_pass3100: first_pass3100 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.whitespaces_after_count > 15): 
                        break
                    if (tt.is_newline_after): 
                        cou += 10
                    cou += 1
                    if ((cou) > 1000): 
                        break
                    if (not ((isinstance(tt, ReferentToken)))): 
                        continue
                    li = tt.getReferents()
                    if (li is None): 
                        continue
                    breaks = False
                    for r in li: 
                        if (((r.type_name == "ORGANIZATION" or r.type_name == "GEO")) and r.parent_referent is None): 
                            if (not r in refs): 
                                if (res.prop_ref.canHasRef(r)): 
                                    refs.append(r)
                        elif (isinstance(r, PersonPropertyReferent)): 
                            if ((Utils.asObjectOrNull(r, PersonPropertyReferent)).findSlot(PersonPropertyReferent.ATTR_REF, None, True) is not None): 
                                breaks = True
                        elif (isinstance(r, PersonReferent)): 
                            breaks = True
                    if (len(refs) > 1 or breaks): 
                        break
                if (len(refs) == 1): 
                    res.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, refs[0], False, 0)
                    res.add_outer_org_as_ref = True
        if (res.chars.is_latin_letter and res.prop_ref is not None and res.prop_ref.findSlot(PersonPropertyReferent.ATTR_REF, None, True) is None): 
            if (res.begin_token.previous is not None and res.begin_token.previous.isValue("S", None)): 
                if (MiscHelper.isEngAdjSuffix(res.begin_token.previous.previous) and (isinstance(res.begin_token.previous.previous.previous, ReferentToken))): 
                    res.begin_token = res.begin_token.previous.previous.previous
                    res.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, res.begin_token.getReferent(), False, 0)
        if (res.chars.is_latin_letter and res.prop_ref is not None and (res.whitespaces_after_count < 2)): 
            rnext = PersonAttrToken.tryAttach(res.end_token.next0_, loc_onto, PersonAttrToken.PersonAttrAttachAttrs.NO)
            if ((rnext is not None and rnext.chars.is_latin_letter and rnext.prop_ref is not None) and len(rnext.prop_ref.slots) == 1 and rnext.can_has_person_after > 0): 
                res.end_token = rnext.end_token
                res.prop_ref.name = "{0} {1}".format(res.prop_ref.name, rnext.prop_ref.name)
        return res
    
    @staticmethod
    def __TryAttach(t : 'Token', loc_onto : 'IntOntologyCollection', attrs : 'PersonAttrAttachAttrs') -> 'PersonAttrToken':
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.mail.internal.MailLine import MailLine
        from pullenti.ner.MorphCollection import MorphCollection
        from pullenti.morph.MorphCase import MorphCase
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.TerminToken import TerminToken
        from pullenti.ner.person.internal.PersonAttrTermin import PersonAttrTermin
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.core.BracketHelper import BracketHelper
        if (t is None): 
            return None
        if (t.morph.class0_.is_pronoun and (((t.isValue("ЕГО", "ЙОГО") or t.isValue("ЕЕ", "ЇЇ") or t.isValue("HIS", None)) or t.isValue("HER", None)))): 
            res1 = PersonAttrToken.tryAttach(t.next0_, loc_onto, attrs)
            if (res1 is not None and res1.prop_ref is not None): 
                k = 0
                tt2 = t.previous
                first_pass3101 = True
                while True:
                    if first_pass3101: first_pass3101 = False
                    else: tt2 = tt2.previous; k += 1
                    if (not (tt2 is not None and (k < 10))): break
                    r = tt2.getReferent()
                    if (r is None): 
                        continue
                    if (r.type_name == PersonAttrToken.OBJ_NAME_ORG or (isinstance(r, PersonReferent))): 
                        ok = False
                        if (t.isValue("ЕЕ", "ЇЇ") or t.isValue("HER", None)): 
                            if (tt2.morph.gender == MorphGender.FEMINIE): 
                                ok = True
                        elif ((((tt2.morph.gender) & (((MorphGender.MASCULINE) | (MorphGender.NEUTER))))) != (MorphGender.UNDEFINED)): 
                            ok = True
                        if (ok): 
                            res1.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                            res1.begin_token = t
                            return res1
                        break
            return None
        nta = NumberHelper.tryParseAge(t)
        if (nta is not None): 
            if (nta.morph.class0_.is_adjective or ((t.previous is not None and t.previous.is_comma)) or ((nta.end_token.next0_ is not None and nta.end_token.next0_.isCharOf(",.")))): 
                return PersonAttrToken._new2261(t, nta.end_token, PersonAttrTerminType.OTHER, str(nta.value), nta.morph)
        if (t.is_newline_before): 
            li = MailLine.parse(t, 0)
            if (li is not None and li.typ == MailLine.Types.BESTREGARDS): 
                return PersonAttrToken._new2263(li.begin_token, li.end_token, PersonAttrTerminType.BESTREGARDS, MorphCollection._new2262(MorphCase.NOMINATIVE))
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            nt = Utils.asObjectOrNull(t, NumberToken)
            if (nt is not None): 
                if (((nt.value == (1) or nt.value == (2) or nt.value == (3))) and nt.morph.class0_.is_adjective): 
                    pat0 = PersonAttrToken.__TryAttach(t.next0_, loc_onto, attrs)
                    if (pat0 is not None and pat0.prop_ref is not None): 
                        pat0.begin_token = t
                        for s in pat0.prop_ref.slots: 
                            if (s.type_name == PersonPropertyReferent.ATTR_NAME): 
                                if ("глава" in str(s.value)): 
                                    return None
                                pat0.prop_ref.uploadSlot(s, "{0} {1}".format(((("первая" if nt.value == (1) else ("вторая" if nt.value == (2) else "третья"))) if pat0.morph.gender == MorphGender.FEMINIE or t.morph.gender == MorphGender.FEMINIE else (("первый" if nt.value == (1) else ("второй" if nt.value == (2) else "третий")))), s.value))
                        return pat0
            rr = None
            if (t is not None): 
                rr = t.getReferent()
            if (rr is not None and (((isinstance(rr, GeoReferent)) or rr.type_name == "ORGANIZATION"))): 
                ttt = t.next0_
                if (MiscHelper.isEngAdjSuffix(ttt)): 
                    ttt = ttt.next0_.next0_
                if ((isinstance(ttt, TextToken)) and ttt.morph.language.is_en and (ttt.whitespaces_before_count < 2)): 
                    res0 = PersonAttrToken.__TryAttach(ttt, loc_onto, attrs)
                    if (res0 is not None and res0.prop_ref is not None): 
                        res0.begin_token = t
                        res0.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, t.getReferent(), False, 0)
                        return res0
            if ((isinstance(rr, PersonReferent)) and MiscHelper.isEngAdjSuffix(t.next0_)): 
                res0 = PersonAttrToken.__TryAttach(t.next0_.next0_.next0_, loc_onto, attrs)
                if (res0 is not None and res0.prop_ref is not None and res0.chars.is_latin_letter): 
                    res0.begin_token = t
                    res0.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, t.getReferent(), False, 0)
                    return res0
            return None
        if (MiscHelper.isEngArticle(tt)): 
            res0 = PersonAttrToken.__TryAttach(t.next0_, loc_onto, attrs)
            if (res0 is not None): 
                res0.begin_token = t
                return res0
        if ((tt.term == "Г" or tt.term == "ГР" or tt.term == "М") or tt.term == "Д"): 
            if (tt.next0_ is not None and tt.next0_.is_hiphen and (isinstance(tt.next0_.next0_, TextToken))): 
                pref = tt.term
                tail = (Utils.asObjectOrNull(tt.next0_.next0_, TextToken)).term
                vars0_ = None
                if (pref == "Г"): 
                    vars0_ = PersonAttrToken.__getStdForms(tail, "ГОСПОДИН", "ГОСПОЖА")
                elif (pref == "ГР"): 
                    vars0_ = PersonAttrToken.__getStdForms(tail, "ГРАЖДАНИН", "ГРАЖДАНКА")
                elif (pref == "М"): 
                    vars0_ = PersonAttrToken.__getStdForms(tail, "МИСТЕР", None)
                elif (pref == "Д"): 
                    if (PersonAttrToken.__findGradeLast(tt.next0_.next0_.next0_, tt) is not None): 
                        pass
                    else: 
                        vars0_ = PersonAttrToken.__getStdForms(tail, "ДОКТОР", None)
                if (vars0_ is not None): 
                    res = PersonAttrToken._new2257(tt, tt.next0_.next0_, PersonAttrTerminType.PREFIX)
                    for v in vars0_: 
                        res.morph.addItem(v)
                        if (res.value is None): 
                            res.value = v.normal_case
                            res.gender = v.gender
                    return res
        if (tt.term == "ГР" or tt.term == "ГРАЖД"): 
            t1 = tt
            if (tt.next0_ is not None and tt.next0_.isChar('.')): 
                t1 = tt.next0_
            if (isinstance(t1.next0_, NumberToken)): 
                return None
            return PersonAttrToken._new2265(tt, t1, PersonAttrTerminType.PREFIX, ("ГРОМАДЯНИН" if tt.morph.language.is_ua else "ГРАЖДАНИН"))
        npt0 = None
        step = 0
        while step < 2: 
            toks = PersonAttrToken.M_TERMINS.tryParseAll(t, TerminParseAttr.NO)
            if (toks is None and t.isValue("ВРИО", None)): 
                toks = list()
                toks.append(TerminToken._new633(t, t, PersonAttrToken.M_TERMIN_VRIO))
            elif (toks is None and (isinstance(t, TextToken)) and t.morph.language.is_en): 
                str0_ = (Utils.asObjectOrNull(t, TextToken)).term
                if (str0_.endswith("MAN") or str0_.endswith("PERSON") or str0_.endswith("MIST")): 
                    toks = list()
                    toks.append(TerminToken._new633(t, t, PersonAttrTermin._new2267(str0_, t.morph.language, PersonAttrTerminType.POSITION)))
                elif (str0_ == "MODEL" and (t.whitespaces_after_count < 2)): 
                    rt = t.kit.processReferent("PERSON", t.next0_)
                    if (rt is not None and (isinstance(rt.referent, PersonReferent))): 
                        toks = list()
                        toks.append(TerminToken._new633(t, t, PersonAttrTermin._new2267(str0_, t.morph.language, PersonAttrTerminType.POSITION)))
            if ((toks is None and step == 0 and t.chars.is_latin_letter) and (t.whitespaces_after_count < 2)): 
                npt1 = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
                if (npt1 is not None and npt1.begin_token != npt1.end_token): 
                    pits = PersonItemToken.tryAttachList(t, loc_onto, Utils.valToEnum((PersonItemToken.ParseAttr.CANBELATIN) | (PersonItemToken.ParseAttr.IGNOREATTRS), PersonItemToken.ParseAttr), 10)
                    if (pits is not None and len(pits) > 1 and pits[0].firstname is not None): 
                        npt1 = (None)
                    k = 0
                    if (npt1 is not None): 
                        tt2 = npt1.begin_token
                        while tt2 is not None and tt2.end_char <= npt1.end_char: 
                            toks1 = PersonAttrToken.M_TERMINS.tryParseAll(tt2, TerminParseAttr.NO)
                            if (toks1 is not None): 
                                step = 1
                                toks = toks1
                                npt0 = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, toks1[0].end_char)
                                if (not (Utils.asObjectOrNull(toks[0].termin, PersonAttrTermin)).is_doubt): 
                                    if (toks[0].morph.number == MorphNumber.PLURAL): 
                                        pass
                                    else: 
                                        break
                            k += 1
                            if (k >= 3 and t.chars.is_all_lower): 
                                if (not MiscHelper.isEngArticle(t.previous)): 
                                    break
                            tt2 = tt2.next0_
                elif (((npt1 is None or npt1.end_token == t)) and t.chars.is_capital_upper): 
                    mc = t.getMorphClassInDictionary()
                    if ((mc.is_misc or mc.is_preposition or mc.is_conjunction) or mc.is_personal_pronoun or mc.is_pronoun): 
                        pass
                    else: 
                        tt1 = None
                        if ((t.next0_ is not None and t.next0_.is_hiphen and not t.is_whitespace_after) and not t.next0_.is_whitespace_after): 
                            tt1 = t.next0_.next0_
                        elif (npt1 is None): 
                            tt1 = t.next0_
                        toks1 = PersonAttrToken.M_TERMINS.tryParseAll(tt1, TerminParseAttr.NO)
                        if (toks1 is not None and (Utils.asObjectOrNull(toks1[0].termin, PersonAttrTermin)).typ == PersonAttrTerminType.POSITION and (tt1.whitespaces_before_count < 2)): 
                            step = 1
                            toks = toks1
            if (toks is not None): 
                for tok in toks: 
                    if (((tok.morph.class0_.is_preposition or tok.morph.containsAttr("к.ф.", MorphClass()))) and tok.end_token == tok.begin_token): 
                        continue
                    pat = Utils.asObjectOrNull(tok.termin, PersonAttrTermin)
                    if ((isinstance(tok.end_token, TextToken)) and pat.canonic_text.startswith((Utils.asObjectOrNull(tok.end_token, TextToken)).term)): 
                        if (tok.length_char < len(pat.canonic_text)): 
                            if (tok.end_token.next0_ is not None and tok.end_token.next0_.isChar('.')): 
                                tok.end_token = tok.end_token.next0_
                    if (pat.typ == PersonAttrTerminType.PREFIX): 
                        if (step == 0 or ((pat.canonic_text != "ГРАЖДАНИН" and pat.canonic_text != "ГРОМАДЯНИН"))): 
                            return PersonAttrToken._new2271(tok.begin_token, tok.end_token, PersonAttrTerminType.PREFIX, pat.canonic_text, tok.morph, pat.gender)
                    if (pat.typ == PersonAttrTerminType.BESTREGARDS): 
                        end = tok.end_token
                        if (end.next0_ is not None and end.next0_.isCharOf(",")): 
                            end = end.next0_
                        return PersonAttrToken._new2263(tok.begin_token, end, PersonAttrTerminType.BESTREGARDS, MorphCollection._new2262(MorphCase.NOMINATIVE))
                    if (pat.typ == PersonAttrTerminType.POSITION or pat.typ == PersonAttrTerminType.PREFIX or pat.typ == PersonAttrTerminType.KING): 
                        res = PersonAttrToken.__createAttrPosition(tok, loc_onto, attrs)
                        if (res is not None): 
                            if (pat.typ == PersonAttrTerminType.KING): 
                                res.typ = pat.typ
                            if (pat.gender != MorphGender.UNDEFINED and res.gender == MorphGender.UNDEFINED): 
                                res.gender = pat.gender
                            if (pat.can_has_person_after > 0): 
                                if (res.end_token.isValue(pat.canonic_text, None)): 
                                    res.can_has_person_after = pat.can_has_person_after
                                else: 
                                    for ii in range(len(pat.canonic_text) - 1, 0, -1):
                                        if (not str.isalpha(pat.canonic_text[ii])): 
                                            if (res.end_token.isValue(pat.canonic_text[ii + 1:], None)): 
                                                res.can_has_person_after = pat.can_has_person_after
                                            break
                            if (pat.can_be_same_surname): 
                                res.can_be_same_surname = True
                            if (pat.can_be_independant): 
                                res.can_be_independent_property = True
                            if (pat.is_doubt): 
                                res.is_doubt = True
                                if (res.prop_ref is not None and ((res.prop_ref.findSlot(PersonPropertyReferent.ATTR_REF, None, True) is not None))): 
                                    res.is_doubt = False
                            if ((t.end_char < res.begin_char) and res.prop_ref is not None): 
                                tt1 = res.begin_token.previous
                                if (tt1.is_hiphen): 
                                    res.prop_ref.name = "{0} {1}".format(res.prop_ref.name, MiscHelper.getTextValue(t, tt1.previous, GetTextAttr.NO).lower())
                                else: 
                                    res.prop_ref.name = "{0} {1}".format(MiscHelper.getTextValue(t, tt1, GetTextAttr.NO).lower(), res.prop_ref.name)
                                res.begin_token = t
                        if (res is not None): 
                            pit = PersonItemToken.tryAttach(t, None, PersonItemToken.ParseAttr.IGNOREATTRS, None)
                            if (pit is not None and pit.typ == PersonItemToken.ItemType.INITIAL): 
                                ok = False
                                pit = PersonItemToken.tryAttach(pit.end_token.next0_, None, PersonItemToken.ParseAttr.IGNOREATTRS, None)
                                if (pit is not None and pit.typ == PersonItemToken.ItemType.INITIAL): 
                                    pit = PersonItemToken.tryAttach(pit.end_token.next0_, None, PersonItemToken.ParseAttr.IGNOREATTRS, None)
                                    if (pit is not None and pit.typ == PersonItemToken.ItemType.INITIAL): 
                                        ok = True
                                if (not ok): 
                                    if (PersonAttrToken.__TryAttach(tok.end_token.next0_, loc_onto, attrs) is not None): 
                                        ok = True
                                if (not ok): 
                                    return None
                            if (npt0 is not None): 
                                ttt1 = (npt0.adjectives[0].begin_token if len(npt0.adjectives) > 0 else npt0.begin_token)
                                if (ttt1.begin_char < res.begin_char): 
                                    res.begin_token = ttt1
                                res.anafor = npt0.anafor
                                empty_adj = None
                                i = 0
                                while i < len(npt0.adjectives): 
                                    j = 0
                                    while j < len(PersonAttrToken.M_EMPTY_ADJS): 
                                        if (npt0.adjectives[i].isValue(PersonAttrToken.M_EMPTY_ADJS[j], None)): 
                                            break
                                        j += 1
                                    if (j < len(PersonAttrToken.M_EMPTY_ADJS)): 
                                        empty_adj = PersonAttrToken.M_EMPTY_ADJS[j].lower()
                                        del npt0.adjectives[i]
                                        break
                                    i += 1
                                na0 = npt0.getNormalCaseText(MorphClass(), True, MorphGender.UNDEFINED, False).lower()
                                na1 = res.prop_ref.name
                                i = 1
                                while i < (len(na0) - 1): 
                                    if (na1.startswith(na0[i:])): 
                                        res.prop_ref.name = "{0} {1}".format(na0[0:0+i].strip(), na1)
                                        break
                                    i += 1
                                if (empty_adj is not None): 
                                    res1 = PersonAttrToken._new2274(res.begin_token, res.end_token, npt0.morph, res)
                                    res1.prop_ref = PersonPropertyReferent()
                                    res1.prop_ref.name = empty_adj
                                    res1.prop_ref.higher = res.prop_ref
                                    res1.can_be_independent_property = res.can_be_independent_property
                                    res1.typ = res.typ
                                    if (res.begin_token != res.end_token): 
                                        res.begin_token = res.begin_token.next0_
                                    res = res1
                            if (res is not None): 
                                res.morph.removeNotInDictionaryItems()
                            return res
            if (step > 0 or t.chars.is_latin_letter): 
                break
            if (t.morph.class0_.is_adjective or t.chars.is_latin_letter): 
                pass
            elif (t.next0_ is not None and t.next0_.is_hiphen): 
                pass
            else: 
                break
            npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
            if (npt is None or npt.end_token == t): 
                break
            if (npt.end_token.isValue("ВИЦЕ", "ВІЦЕ")): 
                break
            t = npt.end_token
            npt0 = npt
            step += 1
        if ((isinstance(t, TextToken)) and (((t.isValue("ВИЦЕ", "ВІЦЕ") or t.isValue("ЭКС", "ЕКС") or t.isValue("VICE", None)) or t.isValue("EX", None) or t.isValue("DEPUTY", None))) and t.next0_ is not None): 
            te = t.next0_
            if (te.is_hiphen): 
                te = te.next0_
            ppp = PersonAttrToken.__TryAttach(te, loc_onto, attrs)
            if (ppp is not None): 
                if (t.begin_char < ppp.begin_char): 
                    ppp.begin_token = t
                    if (ppp.prop_ref is not None and ppp.prop_ref.name is not None): 
                        ppp.prop_ref.name = "{0}-{1}".format((Utils.asObjectOrNull(t, TextToken)).term.lower(), ppp.prop_ref.name)
                return ppp
            if ((te is not None and te.previous.is_hiphen and not te.is_whitespace_after) and not te.is_whitespace_before): 
                if (BracketHelper.isBracket(te, False)): 
                    br = BracketHelper.tryParse(te, BracketParseAttr.NO, 100)
                    if (br is not None and (isinstance(te, TextToken))): 
                        ppp = PersonAttrToken._new2256(t, br.end_token, br.end_token.previous.morph)
                        ppp.prop_ref = PersonPropertyReferent()
                        ppp.prop_ref.name = "{0}-{1}".format((Utils.asObjectOrNull(t, TextToken)).term, MiscHelper.getTextValue(te.next0_, br.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)).lower()
                        return ppp
        if ((isinstance(t, TextToken)) and t.chars.is_latin_letter): 
            if (t.isValue("STATE", None)): 
                tt1 = t.next0_
                if (MiscHelper.isEngAdjSuffix(tt1)): 
                    tt1 = tt1.next0_.next0_
                res1 = PersonAttrToken.__TryAttach(tt1, loc_onto, attrs)
                if (res1 is not None and res1.prop_ref is not None): 
                    res1.begin_token = t
                    res1.prop_ref.name = "{0} {1}".format((Utils.asObjectOrNull(t, TextToken)).term.lower(), res1.prop_ref.name)
                    return res1
        return None
    
    M_EMPTY_ADJS = None
    
    M_STD_FORMS = None
    
    @staticmethod
    def __getStdForms(tail : str, w1 : str, w2 : str) -> typing.List['MorphWordForm']:
        from pullenti.morph.Morphology import Morphology
        from pullenti.morph.MorphLang import MorphLang
        res = list()
        li1 = None
        li2 = None
        wrapli12278 = RefOutArgWrapper(None)
        inoutres2279 = Utils.tryGetValue(PersonAttrToken.M_STD_FORMS, w1, wrapli12278)
        li1 = wrapli12278.value
        if (not inoutres2279): 
            li1 = Morphology.getAllWordforms(w1, MorphLang())
            PersonAttrToken.M_STD_FORMS[w1] = li1
        for v in li1: 
            if (LanguageHelper.endsWith(v.normal_case, tail)): 
                res.append(v)
        if (w2 is not None): 
            wrapli22276 = RefOutArgWrapper(None)
            inoutres2277 = Utils.tryGetValue(PersonAttrToken.M_STD_FORMS, w2, wrapli22276)
            li2 = wrapli22276.value
            if (not inoutres2277): 
                li2 = Morphology.getAllWordforms(w2, MorphLang())
                PersonAttrToken.M_STD_FORMS[w2] = li2
        if (li2 is not None): 
            for v in li2: 
                if (LanguageHelper.endsWith(v.normal_case, tail)): 
                    res.append(v)
        return (res if len(res) > 0 else None)
    
    @staticmethod
    def __createAttrPosition(tok : 'TerminToken', loc_onto : 'IntOntologyCollection', attrs : 'PersonAttrAttachAttrs') -> 'PersonAttrToken':
        from pullenti.ner.person.internal.PersonAttrTermin import PersonAttrTermin
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
        from pullenti.ner.person.internal.PersonIdentityToken import PersonIdentityToken
        from pullenti.morph.MorphBaseInfo import MorphBaseInfo
        from pullenti.morph.MorphCase import MorphCase
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.person.PersonReferent import PersonReferent
        ty2 = (Utils.asObjectOrNull(tok.termin, PersonAttrTermin)).typ2
        if (ty2 == PersonAttrTerminType2.ABBR): 
            pr0 = PersonPropertyReferent()
            pr0.name = tok.termin.canonic_text
            return PersonAttrToken._new2280(tok.begin_token, tok.end_token, pr0, PersonAttrTerminType.POSITION)
        if (ty2 == PersonAttrTerminType2.IO or ty2 == PersonAttrTerminType2.IO2): 
            k = 0
            first_pass3102 = True
            while True:
                if first_pass3102: first_pass3102 = False
                else: k += 1
                if (k > 0): 
                    if (ty2 == PersonAttrTerminType2.IO): 
                        return None
                    if ((((tok.morph.number) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
                        return None
                    break
                tt = tok.end_token.next0_
                if (tt is not None and tt.morph.class0_.is_preposition): 
                    tt = tt.next0_
                res_pat = PersonAttrToken._new2257(tok.begin_token, tok.end_token, PersonAttrTerminType.POSITION)
                res_pat.prop_ref = PersonPropertyReferent()
                if (tt is not None and (isinstance(tt.getReferent(), PersonPropertyReferent))): 
                    res_pat.end_token = tt
                    res_pat.prop_ref.higher = Utils.asObjectOrNull(tt.getReferent(), PersonPropertyReferent)
                else: 
                    aa = attrs
                    if (ty2 == PersonAttrTerminType2.IO2): 
                        aa = (Utils.valToEnum((aa) | (PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL), PersonAttrToken.PersonAttrAttachAttrs))
                    pat = PersonAttrToken.tryAttach(tt, loc_onto, aa)
                    if (pat is None): 
                        if (not ((isinstance(tt, TextToken)))): 
                            continue
                        npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
                        if (npt is None or npt.end_token == tok.end_token.next0_): 
                            continue
                        pat = PersonAttrToken.tryAttach(npt.end_token, loc_onto, PersonAttrToken.PersonAttrAttachAttrs.NO)
                        if (pat is None or pat.begin_token != tt): 
                            continue
                    if (pat.typ != PersonAttrTerminType.POSITION): 
                        continue
                    res_pat.end_token = pat.end_token
                    res_pat.prop_ref.higher = pat.prop_ref
                    res_pat.higher_prop_ref = pat
                nam = tok.termin.canonic_text
                ts = res_pat.end_token.next0_
                te = None
                first_pass3103 = True
                while True:
                    if first_pass3103: first_pass3103 = False
                    else: ts = ts.next0_
                    if (not (ts is not None)): break
                    if (ts.morph.class0_.is_preposition): 
                        if (ts.isValue("В", None) or ts.isValue("ПО", None)): 
                            if (isinstance(ts.next0_, ReferentToken)): 
                                r = ts.next0_.getReferent()
                                if (r.type_name == PersonAttrToken.OBJ_NAME_GEO or r.type_name == PersonAttrToken.OBJ_NAME_ORG): 
                                    res_pat.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                                    res_pat.end_token = ts.next0_
                                else: 
                                    te = ts.next0_
                                ts = ts.next0_
                                continue
                            rt11 = ts.kit.processReferent("NAMEDENTITY", ts.next0_)
                            if (rt11 is not None): 
                                res_pat.prop_ref.addSlot(PersonPropertyReferent.ATTR_REF, rt11, False, 0)
                                res_pat.end_token = rt11.end_token
                                ts = rt11.end_token
                                continue
                        if (ts.isValue("ПО", None) and ts.next0_ is not None): 
                            nnn = NounPhraseHelper.tryParse(ts.next0_, NounPhraseParseAttr.NO, 0)
                            if (nnn is not None): 
                                te = nnn.end_token
                                ts = te
                            elif ((isinstance(ts.next0_, TextToken)) and ((not ts.next0_.chars.is_all_lower and not ts.next0_.chars.is_capital_upper))): 
                                te = ts.next0_
                                ts = te
                            else: 
                                break
                            if ((ts.next0_ is not None and ts.next0_.is_and and (ts.whitespaces_after_count < 2)) and nnn is not None): 
                                nnn2 = NounPhraseHelper.tryParse(ts.next0_.next0_, NounPhraseParseAttr.NO, 0)
                                if (nnn2 is not None and not ((nnn2.morph.case_) & nnn.morph.case_).is_undefined): 
                                    te = nnn2.end_token
                                    ts = te
                            continue
                        break
                    if (ts != res_pat.end_token.next0_ and ts.chars.is_all_lower): 
                        nnn = NounPhraseHelper.tryParse(ts, NounPhraseParseAttr.NO, 0)
                        if (nnn is None): 
                            break
                        te = nnn.end_token
                        ts = te
                        continue
                    break
                if (te is not None): 
                    s = MiscHelper.getTextValue(res_pat.end_token.next0_, te, GetTextAttr.NO)
                    if (not Utils.isNullOrEmpty(s)): 
                        nam = "{0} {1}".format(nam, s)
                        res_pat.end_token = te
                wrapnam2282 = RefOutArgWrapper(nam)
                res_pat.begin_token = PersonAttrToken.__analizeVise(res_pat.begin_token, wrapnam2282)
                nam = wrapnam2282.value
                res_pat.prop_ref.name = nam.lower()
                res_pat.morph = tok.morph
                return res_pat
        if (ty2 == PersonAttrTerminType2.ADJ): 
            pat = PersonAttrToken.__TryAttach(tok.end_token.next0_, loc_onto, attrs)
            if (pat is None or pat.typ != PersonAttrTerminType.POSITION): 
                return None
            if (tok.begin_char == tok.end_char and not tok.begin_token.morph.class0_.is_undefined): 
                return None
            pat.begin_token = tok.begin_token
            pat.prop_ref.name = "{0} {1}".format(tok.termin.canonic_text.lower(), pat.prop_ref.name)
            pat.morph = tok.morph
            return pat
        if (ty2 == PersonAttrTerminType2.IGNOREDADJ): 
            pat = PersonAttrToken.__TryAttach(tok.end_token.next0_, loc_onto, attrs)
            if (pat is None or pat.typ != PersonAttrTerminType.POSITION): 
                return None
            pat.begin_token = tok.begin_token
            pat.morph = tok.morph
            return pat
        if (ty2 == PersonAttrTerminType2.GRADE): 
            gr = PersonAttrToken.__createAttrGrade(tok)
            if (gr is not None): 
                return gr
            if (tok.begin_token.isValue("КАНДИДАТ", None)): 
                tt = tok.end_token.next0_
                if (tt is not None and tt.isValue("В", None)): 
                    tt = tt.next0_
                elif ((tt is not None and tt.isValue("НА", None) and tt.next0_ is not None) and ((tt.next0_.isValue("ПОСТ", None) or tt.next0_.isValue("ДОЛЖНОСТЬ", None)))): 
                    tt = tt.next0_.next0_
                else: 
                    tt = (None)
                if (tt is not None): 
                    pat2 = PersonAttrToken.__TryAttach(tt, loc_onto, PersonAttrToken.PersonAttrAttachAttrs.NO)
                    if (pat2 is not None): 
                        res0 = PersonAttrToken._new2257(tok.begin_token, pat2.end_token, PersonAttrTerminType.POSITION)
                        res0.prop_ref = PersonPropertyReferent._new2258("кандидат")
                        res0.prop_ref.higher = pat2.prop_ref
                        res0.higher_prop_ref = pat2
                        res0.morph = tok.morph
                        return res0
            if (not tok.begin_token.isValue("ДОКТОР", None) and not tok.begin_token.isValue("КАНДИДАТ", None)): 
                return None
        name = tok.termin.canonic_text.lower()
        t0 = tok.begin_token
        t1 = tok.end_token
        wrapname2294 = RefOutArgWrapper(name)
        t0 = PersonAttrToken.__analizeVise(t0, wrapname2294)
        name = wrapname2294.value
        pr = PersonPropertyReferent()
        if ((t1.next0_ is not None and t1.next0_.is_hiphen and not t1.is_whitespace_after) and not t1.next0_.is_whitespace_after): 
            if (t1.next0_.next0_.chars == t1.chars or PersonAttrToken.M_TERMINS.tryParse(t1.next0_.next0_, TerminParseAttr.NO) is not None or ((t1.next0_.next0_.chars.is_all_lower and t1.next0_.next0_.chars.is_cyrillic_letter))): 
                npt = NounPhraseHelper.tryParse(t1, NounPhraseParseAttr.NO, 0)
                if (npt is not None and npt.end_token == t1.next0_.next0_): 
                    name = npt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False).lower()
                    t1 = npt.end_token
        tname0 = t1.next0_
        tname1 = None
        category = None
        npt0 = None
        t = t1.next0_
        first_pass3104 = True
        while True:
            if first_pass3104: first_pass3104 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if ((((attrs) & (PersonAttrToken.PersonAttrAttachAttrs.ONLYKEYWORD))) != (PersonAttrToken.PersonAttrAttachAttrs.NO)): 
                break
            if (MiscHelper.checkNumberPrefix(t) is not None): 
                break
            if (t.is_newline_before): 
                ok = False
                if (t.getReferent() is not None): 
                    if (t.getReferent().type_name == PersonAttrToken.OBJ_NAME_ORG or (isinstance(t.getReferent(), GeoReferent))): 
                        if (pr.findSlot(PersonPropertyReferent.ATTR_REF, None, True) is None): 
                            ok = True
                if (t.newlines_before_count > 1 and not t.chars.is_all_lower): 
                    if (not ok): 
                        break
                    if ((t.newlines_after_count < 3) and tok.begin_token.is_newline_before): 
                        pass
                    else: 
                        break
                if (tok.is_newline_before): 
                    if (PersonAttrToken.M_TERMINS.tryParse(t, TerminParseAttr.NO) is not None): 
                        break
                    else: 
                        ok = True
                if (not ok): 
                    npt00 = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.PARSEPREPOSITION, 0)
                    if (npt00 is not None and npt00.end_token.next0_ is not None and not PersonAttrToken.__isPerson(t)): 
                        tt1 = npt00.end_token
                        zap = False
                        and0_ = False
                        ttt = tt1.next0_
                        while ttt is not None: 
                            if (not ttt.is_comma_and): 
                                break
                            npt00 = NounPhraseHelper.tryParse(ttt.next0_, NounPhraseParseAttr.NO, 0)
                            if (npt00 is None): 
                                break
                            tt1 = npt00.end_token
                            if (ttt.isChar(',')): 
                                zap = True
                            else: 
                                and0_ = True
                                break
                            ttt = npt00.end_token
                            ttt = ttt.next0_
                        if (zap and not and0_): 
                            pass
                        elif (tt1.next0_ is None): 
                            pass
                        else: 
                            if (PersonAttrToken.__isPerson(tt1.next0_)): 
                                ok = True
                            elif (isinstance(tt1.next0_.getReferent(), GeoReferent)): 
                                if (PersonAttrToken.__isPerson(tt1.next0_.next0_)): 
                                    ok = True
                                else: 
                                    wrapccc2285 = RefOutArgWrapper(None)
                                    ttt = PersonAttrToken.__tryAttachCategory(tt1.next0_.next0_, wrapccc2285)
                                    ccc = wrapccc2285.value
                                    if (ttt is not None): 
                                        ok = True
                            if (ok): 
                                tname1 = tt1
                                t1 = tname1
                                t = t1
                                continue
                    break
            if (t.isChar('(')): 
                br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    t = br.end_token
                    ok = True
                    ttt = br.begin_token
                    while ttt != br.end_token: 
                        if (ttt.chars.is_letter): 
                            if (not ttt.chars.is_all_lower): 
                                ok = False
                                break
                        ttt = ttt.next0_
                    if (not ok): 
                        break
                    continue
                else: 
                    break
            pat = None
            if ((((attrs) & (PersonAttrToken.PersonAttrAttachAttrs.ONLYKEYWORD))) == (PersonAttrToken.PersonAttrAttachAttrs.NO)): 
                pat = PersonAttrToken.__TryAttach(t, loc_onto, PersonAttrToken.PersonAttrAttachAttrs.ONLYKEYWORD)
            if (pat is not None): 
                if (pat.morph.number == MorphNumber.PLURAL and not pat.morph.case_.is_nominative): 
                    pass
                elif (((isinstance(tok.termin, PersonAttrTermin)) and (Utils.asObjectOrNull(tok.termin, PersonAttrTermin)).is_doubt and pat.prop_ref is not None) and len(pat.prop_ref.slots) == 1 and tok.chars.is_latin_letter == pat.chars.is_latin_letter): 
                    t = pat.end_token
                    tname1 = t
                    t1 = tname1
                    continue
                elif ((not tok.morph.case_.is_genitive and (isinstance(tok.termin, PersonAttrTermin)) and (Utils.asObjectOrNull(tok.termin, PersonAttrTermin)).can_has_person_after == 1) and pat.morph.case_.is_genitive): 
                    rr = None
                    if (not "IgnorePersons" in t.kit.misc_data): 
                        t.kit.misc_data["IgnorePersons"] = None
                        rr = t.kit.processReferent("PERSON", t)
                        if ("IgnorePersons" in t.kit.misc_data): 
                            del t.kit.misc_data["IgnorePersons"]
                    if (rr is not None and rr.morph.case_.is_genitive): 
                        pr.addExtReferent(rr)
                        pr.addSlot(PersonPropertyReferent.ATTR_REF, rr.referent, False, 0)
                        t = rr.end_token
                        t1 = t
                    else: 
                        t = pat.end_token
                        tname1 = t
                        t1 = tname1
                    continue
                else: 
                    break
            te = t
            if (te.next0_ is not None and te.isCharOf(",в") and (((attrs) & (PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL))) == (PersonAttrToken.PersonAttrAttachAttrs.NO)): 
                te = te.next0_
                if (te.isValue("ОРГАНИЗАЦИЯ", None) and (isinstance(te.next0_, ReferentToken)) and te.next0_.getReferent().type_name == PersonAttrToken.OBJ_NAME_ORG): 
                    te = te.next0_
            elif (te.next0_ is not None and te.morph.class0_.is_preposition): 
                if ((((attrs) & (PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL))) == (PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL)): 
                    break
                if (((te.isValue("ИЗ", None) or te.isValue("ПРИ", None) or te.isValue("ПО", None)) or te.isValue("НА", None) or te.isValue("ОТ", None)) or te.isValue("OF", None)): 
                    te = te.next0_
            elif ((te.is_hiphen and te.next0_ is not None and not te.is_whitespace_before) and not te.is_whitespace_after and te.previous.chars == te.next0_.chars): 
                continue
            elif (te.isValue("REPRESENT", None) and (isinstance(te.next0_, ReferentToken))): 
                te = te.next0_
            r = te.getReferent()
            if ((te.chars.is_latin_letter and te.length_char > 1 and not t0.chars.is_latin_letter) and not te.chars.is_all_lower): 
                if (r is None or r.type_name != PersonAttrToken.OBJ_NAME_ORG): 
                    wrapcategory2286 = RefOutArgWrapper(None)
                    tt = PersonAttrToken.__tryAttachCategory(t, wrapcategory2286)
                    category = wrapcategory2286.value
                    if (tt is not None and name is not None): 
                        t1 = tt
                        t = t1
                        continue
                    while te is not None: 
                        if (te.chars.is_letter): 
                            if (not te.chars.is_latin_letter): 
                                break
                            t = te
                            tname1 = t
                            t1 = tname1
                        te = te.next0_
                    continue
            if (r is not None): 
                if ((r.type_name == PersonAttrToken.OBJ_NAME_GEO and te.previous is not None and te.previous.isValue("ДЕЛО", "СПРАВІ")) and te.previous.previous is not None and te.previous.previous.isValue("ПО", None)): 
                    t = te
                    tname1 = t
                    t1 = tname1
                    continue
                if ((r.type_name == PersonAttrToken.OBJ_NAME_GEO or r.type_name == PersonAttrToken.OBJ_NAME_ADDR or r.type_name == PersonAttrToken.OBJ_NAME_ORG) or r.type_name == PersonAttrToken.OBJ_NAME_TRANSPORT): 
                    if (t0.previous is not None and t0.previous.isValue("ОТ", None) and t.is_newline_before): 
                        break
                    t1 = te
                    pr.addSlot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                    posol = ((r.type_name == PersonAttrToken.OBJ_NAME_GEO or r.type_name == PersonAttrToken.OBJ_NAME_ORG)) and LanguageHelper.endsWithEx(name, "посол", "представитель", None, None)
                    if (posol): 
                        t = t1
                        continue
                    if ((((r.type_name == PersonAttrToken.OBJ_NAME_GEO and t1.next0_ is not None and t1.next0_.morph.class0_.is_preposition) and t1.next0_.next0_ is not None and not t1.next0_.isValue("О", None)) and not t1.next0_.isValue("ОБ", None) and (((attrs) & (PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL))) == (PersonAttrToken.PersonAttrAttachAttrs.NO)) and not (Utils.asObjectOrNull(tok.termin, PersonAttrTermin)).is_boss): 
                        r1 = t1.next0_.next0_.getReferent()
                        if ((r1) is not None): 
                            if (r1.type_name == PersonAttrToken.OBJ_NAME_ORG): 
                                pr.addSlot(PersonPropertyReferent.ATTR_REF, r1, False, 0)
                                t1 = t1.next0_.next0_
                                t = t1
                    if (r.type_name == PersonAttrToken.OBJ_NAME_ORG): 
                        t = te.next0_
                        while t is not None: 
                            if (not t.is_comma_and or not ((isinstance(t.next0_, ReferentToken)))): 
                                break
                            r = t.next0_.getReferent()
                            if (r is None): 
                                break
                            if (r.type_name != PersonAttrToken.OBJ_NAME_ORG): 
                                break
                            pr.addSlot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                            t = t.next0_
                            t1 = t
                            if (t.previous.is_and): 
                                t = t.next0_
                                break
                            t = t.next0_
                        first_pass3105 = True
                        while True:
                            if first_pass3105: first_pass3105 = False
                            else: t = t.next0_
                            if (not (t is not None)): break
                            if (t.is_newline_before): 
                                break
                            if (t.isValue("В", None) or t.isValue("ОТ", None) or t.is_and): 
                                continue
                            if (t.morph.language.is_ua): 
                                if (t.isValue("ВІД", None)): 
                                    continue
                            if (((isinstance(t, TextToken)) and t.chars.is_letter and not t.chars.is_all_lower) and t.previous.isValue("ОТ", "ВІД")): 
                                tname0 = t.previous
                                t1 = t
                                tname1 = t1
                                continue
                            if ((isinstance(t, TextToken)) and BracketHelper.canBeStartOfSequence(t, False, False) and t.previous.isValue("ОТ", "ВІД")): 
                                br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                                if (br is not None and (br.length_char < 100)): 
                                    tname0 = t.previous
                                    t = br.end_token
                                    t1 = t
                                    tname1 = t1
                                    continue
                            r = t.getReferent()
                            if (r is None): 
                                break
                            if (r.type_name != PersonAttrToken.OBJ_NAME_GEO): 
                                if (r.type_name == PersonAttrToken.OBJ_NAME_ORG and t.previous is not None and ((t.previous.isValue("ОТ", None) or t.previous.isValue("ВІД", None)))): 
                                    pass
                                else: 
                                    break
                            pr.addSlot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                            t1 = t
                if ((t1.next0_ is not None and (t1.whitespaces_after_count < 2) and t1.next0_.chars.is_latin_letter) and not t1.next0_.chars.is_all_lower and MiscHelper.checkNumberPrefix(t1.next0_) is None): 
                    t = t1.next0_
                    while t is not None: 
                        if (not ((isinstance(t, TextToken)))): 
                            break
                        if (not t.chars.is_letter): 
                            break
                        if (not t.chars.is_latin_letter): 
                            break
                        if (t.kit.base_language.is_en): 
                            break
                        tname1 = t
                        t1 = tname1
                        t = t.next0_
                t = t1
                if (((tname0 == t and tname1 is None and t.next0_ is not None) and (((attrs) & (PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL))) == (PersonAttrToken.PersonAttrAttachAttrs.NO) and name != "президент") and t.next0_.isValue("ПО", None)): 
                    tname0 = t.next0_
                    continue
                break
            if (category is None): 
                wrapcategory2287 = RefOutArgWrapper(None)
                tt = PersonAttrToken.__tryAttachCategory(t, wrapcategory2287)
                category = wrapcategory2287.value
                if (tt is not None and name is not None): 
                    t1 = tt
                    t = t1
                    continue
            if (name == "премьер"): 
                break
            if (isinstance(t, TextToken)): 
                if (t.isValue("ИМЕНИ", "ІМЕНІ")): 
                    break
            if (not t.chars.is_all_lower): 
                pit = PersonItemToken.tryAttach(t, loc_onto, Utils.valToEnum((PersonItemToken.ParseAttr.CANBELATIN) | (PersonItemToken.ParseAttr.IGNOREATTRS), PersonItemToken.ParseAttr), None)
                if (pit is not None): 
                    if (pit.referent is not None): 
                        break
                    if (pit.lastname is not None and ((pit.lastname.is_in_dictionary or pit.lastname.is_in_ontology))): 
                        break
                    if (pit.firstname is not None and pit.firstname.is_in_dictionary): 
                        break
                    pits = PersonItemToken.tryAttachList(t, loc_onto, Utils.valToEnum((PersonItemToken.ParseAttr.NO) | (PersonItemToken.ParseAttr.IGNOREATTRS), PersonItemToken.ParseAttr), 6)
                    if (pits is not None and len(pits) > 0): 
                        if (len(pits) == 2): 
                            if (pits[1].lastname is not None and pits[1].lastname.is_in_dictionary): 
                                break
                            if (pits[1].typ == PersonItemToken.ItemType.INITIAL and pits[0].lastname is not None): 
                                break
                        if (len(pits) == 3): 
                            if (pits[2].lastname is not None): 
                                if (pits[1].middlename is not None): 
                                    break
                                if (pits[0].firstname is not None and pits[0].firstname.is_in_dictionary): 
                                    break
                            if (pits[1].typ == PersonItemToken.ItemType.INITIAL and pits[2].typ == PersonItemToken.ItemType.INITIAL and pits[0].lastname is not None): 
                                break
                        if (pits[0].typ == PersonItemToken.ItemType.INITIAL): 
                            break
            test_person = False
            if (not t.chars.is_all_lower): 
                if ("TestAttr" in t.kit.misc_data): 
                    pass
                else: 
                    pits = PersonItemToken.tryAttachList(t, None, PersonItemToken.ParseAttr.IGNOREATTRS, 10)
                    if (pits is not None and len(pits) > 1): 
                        nnn = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
                        iii = 1
                        if (nnn is not None and len(nnn.adjectives) > 0): 
                            iii += len(nnn.adjectives)
                        test_person = True
                        t.kit.misc_data["TestAttr"] = None
                        li = PersonIdentityToken.tryAttach(pits, 0, MorphBaseInfo._new2288(MorphCase.ALL_CASES), None, False, False)
                        del t.kit.misc_data["TestAttr"]
                        if (len(li) > 0 and li[0].coef > 1): 
                            t.kit.misc_data["TestAttr"] = None
                            li1 = PersonIdentityToken.tryAttach(pits, iii, MorphBaseInfo._new2288(MorphCase.ALL_CASES), None, False, False)
                            del t.kit.misc_data["TestAttr"]
                            if (len(li1) == 0): 
                                break
                            if (li1[0].coef <= li[0].coef): 
                                break
                        else: 
                            t.kit.misc_data["TestAttr"] = None
                            li1 = PersonIdentityToken.tryAttach(pits, 1, MorphBaseInfo._new2288(MorphCase.ALL_CASES), None, False, False)
                            del t.kit.misc_data["TestAttr"]
                            if (len(li1) > 0 and li1[0].coef >= 1 and li1[0].begin_token == t): 
                                continue
            if (BracketHelper.canBeStartOfSequence(t, True, False)): 
                br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                if ((br is not None and t.next0_.getReferent() is not None and t.next0_.getReferent().type_name == PersonAttrToken.OBJ_NAME_ORG) and t.next0_.next0_ == br.end_token): 
                    pr.addSlot(PersonPropertyReferent.ATTR_REF, t.next0_.getReferent(), False, 0)
                    t1 = br.end_token
                    break
                elif (br is not None and (br.length_char < 40)): 
                    tname1 = br.end_token
                    t1 = tname1
                    t = t1
                    continue
            if ((isinstance(t, NumberToken)) and t.previous.isValue("ГЛАВА", None)): 
                break
            npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
            test = False
            if (npt is not None): 
                if (PersonAttrToken.__existsInDoctionary(npt.end_token) and ((npt.morph.case_.is_genitive or npt.morph.case_.is_instrumental))): 
                    test = True
                elif (npt.begin_token == npt.end_token and t.length_char > 1 and ((t.chars.is_all_upper or t.chars.is_last_lower))): 
                    test = True
            elif (t.chars.is_all_upper or t.chars.is_last_lower): 
                test = True
            if (test): 
                rto = t.kit.processReferent("ORGANIZATION", t)
                if (rto is not None): 
                    str0_ = str(rto.referent).upper()
                    if (str0_.startswith("ГОСУДАРСТВЕННАЯ ГРАЖДАНСКАЯ СЛУЖБА")): 
                        rto = (None)
                if (rto is not None and rto.end_char >= t.end_char and rto.begin_char == t.begin_char): 
                    pr.addSlot(PersonPropertyReferent.ATTR_REF, rto.referent, False, 0)
                    pr.addExtReferent(rto)
                    t1 = rto.end_token
                    t = t1
                    if ((((attrs) & (PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL))) != (PersonAttrToken.PersonAttrAttachAttrs.NO)): 
                        break
                    npt0 = npt
                    if (t.next0_ is not None and t.next0_.is_and): 
                        rto2 = t.kit.processReferent("ORGANIZATION", t.next0_.next0_)
                        if (rto2 is not None and rto2.begin_char == t.next0_.next0_.begin_char): 
                            pr.addSlot(PersonPropertyReferent.ATTR_REF, rto2.referent, False, 0)
                            pr.addExtReferent(rto2)
                            t1 = rto2.end_token
                            t = t1
                    continue
                if (npt is not None): 
                    tname1 = npt.end_token
                    t1 = tname1
                    t = t1
                    npt0 = npt
                    continue
            if (t.morph.class0_.is_preposition): 
                npt = NounPhraseHelper.tryParse(t.next0_, NounPhraseParseAttr.NO, 0)
                if (npt is None and t.next0_ is not None and t.next0_.morph.class0_.is_adverb): 
                    npt = NounPhraseHelper.tryParse(t.next0_.next0_, NounPhraseParseAttr.NO, 0)
                if (npt is not None and PersonAttrToken.__existsInDoctionary(npt.end_token)): 
                    ok = False
                    if ((t.isValue("ПО", None) and npt.morph.case_.is_dative and not npt.noun.isValue("ИМЯ", "ІМЯ")) and not npt.noun.isValue("ПРОЗВИЩЕ", "ПРІЗВИСЬКО") and not npt.noun.isValue("ПРОЗВАНИЕ", "ПРОЗВАННЯ")): 
                        ok = True
                        if (npt.noun.isValue("РАБОТА", "РОБОТА") or npt.noun.isValue("ПОДДЕРЖКА", "ПІДТРИМКА") or npt.noun.isValue("СОПРОВОЖДЕНИЕ", "СУПРОВІД")): 
                            npt2 = NounPhraseHelper.tryParse(npt.end_token.next0_, NounPhraseParseAttr.PARSEPREPOSITION, 0)
                            if (npt2 is not None): 
                                npt = npt2
                    elif (npt.noun.isValue("ОТСТАВКА", None) or npt.noun.isValue("ВІДСТАВКА", None)): 
                        ok = True
                    elif (name == "кандидат" and t.isValue("В", None)): 
                        ok = True
                    if (ok): 
                        tname1 = npt.end_token
                        t1 = tname1
                        t = t1
                        npt0 = npt
                        continue
                if (t.isValue("OF", None)): 
                    continue
            elif (t.is_and and npt0 is not None): 
                npt = NounPhraseHelper.tryParse(t.next0_, NounPhraseParseAttr.NO, 0)
                if (npt is not None and not ((npt.morph.class0_) & npt0.morph.class0_).is_undefined): 
                    if (npt0.chars == npt.chars): 
                        tname1 = npt.end_token
                        t1 = tname1
                        t = t1
                        npt0 = (None)
                        continue
            elif (t.is_comma_and and ((not t.is_newline_after or tok.is_newline_before)) and npt0 is not None): 
                npt = NounPhraseHelper.tryParse(t.next0_, NounPhraseParseAttr.NO, 0)
                if (npt is not None and not ((npt.morph.class0_) & npt0.morph.class0_).is_undefined): 
                    if (npt0.chars == npt.chars and npt.end_token.next0_ is not None and npt.end_token.next0_.is_and): 
                        npt1 = NounPhraseHelper.tryParse(npt.end_token.next0_.next0_, NounPhraseParseAttr.NO, 0)
                        if (npt1 is not None and not ((npt1.morph.class0_) & npt.morph.class0_ & npt0.morph.class0_).is_undefined): 
                            if (npt0.chars == npt1.chars): 
                                tname1 = npt1.end_token
                                t1 = tname1
                                t = t1
                                npt0 = (None)
                                continue
            elif (t.morph.class0_.is_adjective and BracketHelper.canBeStartOfSequence(t.next0_, True, False)): 
                br = BracketHelper.tryParse(t.next0_, BracketParseAttr.NO, 100)
                if (br is not None and (br.length_char < 100)): 
                    tname1 = br.end_token
                    t1 = tname1
                    t = t1
                    npt0 = (None)
                    continue
            if (t.chars.is_latin_letter and t.previous.chars.is_cyrillic_letter): 
                while t is not None: 
                    if (not t.chars.is_latin_letter or t.is_newline_before): 
                        break
                    else: 
                        tname1 = t
                        t1 = tname1
                    t = t.next0_
                break
            if (((t.chars.is_all_upper or ((not t.chars.is_all_lower and not t.chars.is_capital_upper)))) and t.length_char > 1 and not t0.chars.is_all_upper): 
                tname1 = t
                t1 = tname1
                continue
            if (t.chars.is_last_lower and t.length_char > 2 and not t0.chars.is_all_upper): 
                tname1 = t
                t1 = tname1
                continue
            if (((t.chars.is_letter and (isinstance(t.next0_, ReferentToken)) and (isinstance(t.next0_.getReferent(), PersonReferent))) and not t.morph.class0_.is_preposition and not t.morph.class0_.is_conjunction) and not t.morph.class0_.is_verb): 
                tname1 = t
                t1 = tname1
                break
            if (isinstance(t, NumberToken)): 
                if ((Utils.asObjectOrNull(t, NumberToken)).begin_token.isValue("МИЛЛИОНОВ", None) or (Utils.asObjectOrNull(t, NumberToken)).begin_token.isValue("МІЛЬЙОНІВ", None)): 
                    tname1 = t
                    t1 = tname1
                    break
            if (test_person): 
                if (t.next0_ is None): 
                    break
                te = t.next0_
                if (((te.isCharOf(",в") or te.isValue("ИЗ", None))) and te.next0_ is not None): 
                    te = te.next0_
                r = te.getReferent()
                if ((r) is not None): 
                    if (r.type_name == PersonAttrToken.OBJ_NAME_GEO or r.type_name == PersonAttrToken.OBJ_NAME_ORG or r.type_name == PersonAttrToken.OBJ_NAME_TRANSPORT): 
                        tname1 = t
                        t1 = tname1
                        continue
                break
            if (t.morph.language.is_en): 
                break
            if (t.morph.class0_.is_noun and t.getMorphClassInDictionary().is_undefined and (t.whitespaces_before_count < 2)): 
                tname1 = t
                t1 = tname1
                continue
            break
        if (tname1 is not None): 
            if (pr.findSlot(PersonPropertyReferent.ATTR_REF, None, True) is None and (((((tname1.isValue("КОМПАНИЯ", "КОМПАНІЯ") or tname1.isValue("ФИРМА", "ФІРМА") or tname1.isValue("ПРЕДПРИЯТИЕ", "ПІДПРИЄМСТВО")) or tname1.isValue("ПРЕЗИДИУМ", "ПРЕЗИДІЯ") or tname1.isValue("ЧАСТЬ", "ЧАСТИНА")) or tname1.isValue("ФЕДЕРАЦИЯ", "ФЕДЕРАЦІЯ") or tname1.isValue("ВЕДОМСТВО", "ВІДОМСТВО")) or tname1.isValue("БАНК", None) or tname1.isValue("КОРПОРАЦИЯ", "КОРПОРАЦІЯ")))): 
                if (tname1 == tname0 or ((tname0.isValue("ЭТОТ", "ЦЕЙ") and tname0.next0_ == tname1))): 
                    org0_ = None
                    cou = 0
                    tt0 = t0.previous
                    first_pass3106 = True
                    while True:
                        if first_pass3106: first_pass3106 = False
                        else: tt0 = tt0.previous
                        if (not (tt0 is not None)): break
                        if (tt0.is_newline_after): 
                            cou += 10
                        cou += 1
                        if ((cou) > 500): 
                            break
                        rs0 = tt0.getReferents()
                        if (rs0 is None): 
                            continue
                        has_org = False
                        for r0 in rs0: 
                            if (r0.type_name == PersonAttrToken.OBJ_NAME_ORG): 
                                has_org = True
                                if (tname1.isValue("БАНК", None)): 
                                    if (r0.findSlot("TYPE", "банк", True) is None): 
                                        continue
                                if (tname1.isValue("ЧАСТЬ", "ЧАСТИНА")): 
                                    ok1 = False
                                    for s in r0.slots: 
                                        if (s.type_name == "TYPE"): 
                                            if ((s.value).endswith("часть") or (s.value).endswith("частина")): 
                                                ok1 = True
                                    if (not ok1): 
                                        continue
                                org0_ = r0
                                break
                        if (org0_ is not None or has_org): 
                            break
                    if (org0_ is not None): 
                        pr.addSlot(PersonPropertyReferent.ATTR_REF, org0_, False, 0)
                        tname1 = (None)
        if (tname1 is not None): 
            s = MiscHelper.getTextValue(tname0, tname1, GetTextAttr.NO)
            if (s is not None): 
                name = "{0} {1}".format(name, s.lower())
        if (category is not None): 
            name = "{0} {1}".format(name, category)
        else: 
            wrapcategory2291 = RefOutArgWrapper(None)
            tt = PersonAttrToken.__tryAttachCategory(t1.next0_, wrapcategory2291)
            category = wrapcategory2291.value
            if (tt is not None): 
                name = "{0} {1}".format(name, category)
                t1 = tt
        pr.name = name
        res = PersonAttrToken._new2292(t0, t1, PersonAttrTerminType.POSITION, pr, tok.morph)
        res.can_be_independent_property = (Utils.asObjectOrNull(tok.termin, PersonAttrTermin)).can_be_unique_identifier
        i = name.find("заместитель ")
        if (i < 0): 
            i = name.find("заступник ")
        if (i >= 0): 
            i += 11
            res1 = PersonAttrToken._new2263(t0, t1, PersonAttrTerminType.POSITION, tok.morph)
            res1.prop_ref = PersonPropertyReferent()
            res1.prop_ref.name = name[0:0+i]
            res1.prop_ref.higher = res.prop_ref
            res1.higher_prop_ref = res
            res.prop_ref.name = name[i + 1:]
            return res1
        return res
    
    @staticmethod
    def __existsInDoctionary(t : 'Token') -> bool:
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphWordForm import MorphWordForm
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return False
        for wf in tt.morph.items: 
            if ((Utils.asObjectOrNull(wf, MorphWordForm)).is_in_dictionary): 
                return True
        return False
    
    @staticmethod
    def __isPerson(t : 'Token') -> bool:
        from pullenti.ner.person.PersonReferent import PersonReferent
        if (t is None): 
            return False
        if (isinstance(t, ReferentToken)): 
            return isinstance(t.getReferent(), PersonReferent)
        if (not t.chars.is_letter or t.chars.is_all_lower): 
            return False
        rt00 = t.kit.processReferent("PERSON", t)
        return rt00 is not None and (isinstance(rt00.referent, PersonReferent))
    
    @staticmethod
    def __analizeVise(t0 : 'Token', name : str) -> 'Token':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        if (t0 is None): 
            return None
        if (t0.previous is not None and t0.previous.is_hiphen and (isinstance(t0.previous.previous, TextToken))): 
            if (t0.previous.previous.isValue("ВИЦЕ", "ВІЦЕ")): 
                t0 = t0.previous.previous
                name.value = (((("віце-" if t0.kit.base_language.is_ua else "вице-"))) + name.value)
            if (t0.previous is not None and t0.previous.previous is not None): 
                if (t0.previous.previous.isValue("ЭКС", "ЕКС")): 
                    t0 = t0.previous.previous
                    name.value = (((("екс-" if t0.kit.base_language.is_ua else "экс-"))) + name.value)
                elif (t0.previous.previous.chars == t0.chars and not t0.is_whitespace_before and not t0.previous.is_whitespace_before): 
                    npt00 = NounPhraseHelper.tryParse(t0.previous.previous, NounPhraseParseAttr.NO, 0)
                    if (npt00 is not None): 
                        name.value = npt00.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False).lower()
                        t0 = t0.previous.previous
        return t0
    
    @staticmethod
    def __tryAttachCategory(t : 'Token', cat : str) -> 'Token':
        from pullenti.ner.NumberToken import NumberToken
        cat.value = (None)
        if (t is None or t.next0_ is None): 
            return None
        tt = None
        num = -1
        if (isinstance(t, NumberToken)): 
            num = ((Utils.asObjectOrNull(t, NumberToken)).value)
            tt = t
        else: 
            npt = NumberHelper.tryParseRoman(t)
            if (npt is not None): 
                num = (npt.value)
                tt = npt.end_token
        if ((num < 0) and ((t.isValue("ВЫСШИЙ", None) or t.isValue("ВЫСШ", None) or t.isValue("ВИЩИЙ", None)))): 
            num = 0
            tt = t
            if (tt.next0_ is not None and tt.next0_.isChar('.')): 
                tt = tt.next0_
        if (tt is None or tt.next0_ is None or (num < 0)): 
            return None
        tt = tt.next0_
        if (tt.isValue("КАТЕГОРИЯ", None) or tt.isValue("КАТЕГОРІЯ", None) or tt.isValue("КАТ", None)): 
            if (tt.next0_ is not None and tt.next0_.isChar('.')): 
                tt = tt.next0_
            if (num == 0): 
                cat.value = ("вищої категорії" if tt.kit.base_language.is_ua else "высшей категории")
            else: 
                cat.value = ("{0} категорії".format(num) if tt.kit.base_language.is_ua else "{0} категории".format(num))
            return tt
        if (tt.isValue("РАЗРЯД", None) or tt.isValue("РОЗРЯД", None)): 
            if (num == 0): 
                cat.value = ("вищого розряду" if tt.kit.base_language.is_ua else "высшего разряда")
            else: 
                cat.value = ("{0} розряду".format(num) if tt.kit.base_language.is_ua else "{0} разряда".format(num))
            return tt
        if (tt.isValue("КЛАСС", None) or tt.isValue("КЛАС", None)): 
            if (num == 0): 
                cat.value = ("вищого класу" if tt.kit.base_language.is_ua else "высшего класса")
            else: 
                cat.value = ("{0} класу".format(num) if tt.kit.base_language.is_ua else "{0} класса".format(num))
            return tt
        if (tt.isValue("РАНГ", None)): 
            if (num == 0): 
                return None
            else: 
                cat.value = "{0} ранга".format(num)
            return tt
        if (tt.isValue("СОЗЫВ", None) or tt.isValue("СКЛИКАННЯ", None)): 
            if (num == 0): 
                return None
            else: 
                cat.value = ("{0} скликання".format(num) if tt.kit.base_language.is_ua else "{0} созыва".format(num))
            return tt
        return None
    
    OBJ_NAME_GEO = "GEO"
    
    OBJ_NAME_ADDR = "ADDRESS"
    
    OBJ_NAME_ORG = "ORGANIZATION"
    
    OBJ_NAME_TRANSPORT = "TRANSPORT"
    
    OBJ_NAME_DATE = "DATE"
    
    OBJ_NAME_DATE_RANGE = "DATERANGE"
    
    @staticmethod
    def __createAttrGrade(tok : 'TerminToken') -> 'PersonAttrToken':
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        t1 = PersonAttrToken.__findGradeLast(tok.end_token.next0_, tok.begin_token)
        if (t1 is None): 
            return None
        pr = PersonPropertyReferent()
        pr.name = "{0} наук".format(tok.termin.canonic_text.lower())
        return PersonAttrToken._new2295(tok.begin_token, t1, PersonAttrTerminType.POSITION, pr, tok.morph, False)
    
    @staticmethod
    def __findGradeLast(t : 'Token', t0 : 'Token') -> 'Token':
        i = 0
        t1 = None
        while t is not None: 
            if (t.isValue("НАУК", None)): 
                t1 = t
                i += 1
                break
            if (t.isValue("Н", None)): 
                if (t0.length_char > 1 or t0.chars != t.chars): 
                    return None
                if ((t.next0_ is not None and t.next0_.is_hiphen and t.next0_.next0_ is not None) and t.next0_.next0_.isValue("К", None)): 
                    t1 = t.next0_.next0_
                    break
                if (t.next0_ is not None and t.next0_.isChar('.')): 
                    t1 = t.next0_
                    break
            if (not t.chars.is_all_lower and t0.chars.is_all_lower): 
                break
            i += 1
            if ((i) > 2): 
                break
            if (t.next0_ is not None and t.next0_.isChar('.')): 
                t = t.next0_
            if (t.next0_ is not None and t.next0_.is_hiphen): 
                t = t.next0_
            t = t.next0_
        if (t1 is None or i == 0): 
            return None
        return t1
    
    @staticmethod
    def checkKind(pr : 'PersonPropertyReferent') -> 'PersonPropertyKind':
        from pullenti.ner.Referent import Referent
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.ner.person.internal.PersonAttrTermin import PersonAttrTermin
        if (pr is None): 
            return PersonPropertyKind.UNDEFINED
        n = pr.getStringValue(PersonPropertyReferent.ATTR_NAME)
        if (n is None): 
            return PersonPropertyKind.UNDEFINED
        n = n.upper()
        for nn in Utils.splitString(n, ' ' + '-', False): 
            li = PersonAttrToken.M_TERMINS.tryAttachStr(nn, MorphLang.RU)
            if (li is None or len(li) == 0): 
                li = PersonAttrToken.M_TERMINS.tryAttachStr(n, MorphLang.UA)
            if (li is not None and len(li) > 0): 
                pat = Utils.asObjectOrNull(li[0], PersonAttrTermin)
                if (pat.is_boss): 
                    return PersonPropertyKind.BOSS
                if (pat.is_kin): 
                    return PersonPropertyKind.KIN
                if (pat.typ == PersonAttrTerminType.KING): 
                    if (n != "ДОН"): 
                        return PersonPropertyKind.KING
                if (pat.is_military_rank): 
                    if (nn == "ВИЦЕ"): 
                        continue
                    if (nn == "КАПИТАН" or nn == "CAPTAIN" or nn == "КАПІТАН"): 
                        org0_ = Utils.asObjectOrNull(pr.getSlotValue(PersonPropertyReferent.ATTR_REF), Referent)
                        if (org0_ is not None and org0_.type_name == "ORGANIZATION"): 
                            continue
                    return PersonPropertyKind.MILITARYRANK
                if (pat.is_nation): 
                    return PersonPropertyKind.NATIONALITY
        return PersonPropertyKind.UNDEFINED
    
    @staticmethod
    def tryAttachWord(t : 'Token') -> 'TerminToken':
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.MorphCollection import MorphCollection
        from pullenti.ner.person.internal.PersonAttrTermin import PersonAttrTermin
        tok = PersonAttrToken.M_TERMINS.tryParse(t, TerminParseAttr.NO)
        if ((tok is not None and tok.begin_token == tok.end_token and t.length_char == 1) and t.isValue("Д", None)): 
            if (BracketHelper.isBracket(t.next0_, True) and not t.is_whitespace_after): 
                return None
        if (tok is not None and tok.termin.canonic_text == "ГРАФ"): 
            tok.morph = MorphCollection(t.morph)
            tok.morph.removeItems(MorphGender.MASCULINE, False)
        if (tok is not None): 
            pat = Utils.asObjectOrNull(tok.termin, PersonAttrTermin)
            if (pat.typ2 != PersonAttrTerminType2.UNDEFINED and pat.typ2 != PersonAttrTerminType2.GRADE): 
                return None
        return tok
    
    @staticmethod
    def tryAttachPositionWord(t : 'Token') -> 'TerminToken':
        from pullenti.ner.person.internal.PersonAttrTermin import PersonAttrTermin
        tok = PersonAttrToken.M_TERMINS.tryParse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        pat = Utils.asObjectOrNull(tok.termin, PersonAttrTermin)
        if (pat is None): 
            return None
        if (pat.typ != PersonAttrTerminType.POSITION): 
            return None
        if (pat.typ2 != PersonAttrTerminType2.IO2 and pat.typ2 != PersonAttrTerminType2.UNDEFINED): 
            return None
        return tok
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.person.internal.PersonAttrTermin import PersonAttrTermin
        from pullenti.morph.MorphLang import MorphLang
        if (PersonAttrToken.M_TERMINS is not None): 
            return
        PersonAttrToken.M_TERMINS = TerminCollection()
        PersonAttrToken.M_TERMINS.add(PersonAttrTermin._new2296("ТОВАРИЩ", PersonAttrTerminType.PREFIX))
        PersonAttrToken.M_TERMINS.add(PersonAttrTermin._new2267("ТОВАРИШ", MorphLang.UA, PersonAttrTerminType.PREFIX))
        for s in ["ГОСПОДИН", "ГРАЖДАНИН", "УРОЖЕНЕЦ", "МИСТЕР", "СЭР", "СЕНЬОР", "МОНСЕНЬОР", "СИНЬОР", "МЕСЬЕ", "МСЬЕ", "ДОН", "МАЭСТРО", "МЭТР"]: 
            t = PersonAttrTermin._new2298(s, PersonAttrTerminType.PREFIX, MorphGender.MASCULINE)
            if (s == "ГРАЖДАНИН"): 
                t.addAbridge("ГР.")
                t.addAbridge("ГРАЖД.")
                t.addAbridge("ГР-Н")
            PersonAttrToken.M_TERMINS.add(t)
        for s in ["ПАН", "ГРОМАДЯНИН", "УРОДЖЕНЕЦЬ", "МІСТЕР", "СЕР", "СЕНЬЙОР", "МОНСЕНЬЙОР", "МЕСЬЄ", "МЕТР", "МАЕСТРО"]: 
            t = PersonAttrTermin._new2299(s, MorphLang.UA, PersonAttrTerminType.PREFIX, MorphGender.MASCULINE)
            if (s == "ГРОМАДЯНИН"): 
                t.addAbridge("ГР.")
                t.addAbridge("ГР-Н")
            PersonAttrToken.M_TERMINS.add(t)
        for s in ["ГОСПОЖА", "ПАНИ", "ГРАЖДАНКА", "УРОЖЕНКА", "СЕНЬОРА", "СЕНЬОРИТА", "СИНЬОРА", "СИНЬОРИТА", "МИСС", "МИССИС", "МАДАМ", "МАДЕМУАЗЕЛЬ", "ФРАУ", "ФРОЙЛЯЙН", "ЛЕДИ", "ДОННА"]: 
            t = PersonAttrTermin._new2298(s, PersonAttrTerminType.PREFIX, MorphGender.FEMINIE)
            if (s == "ГРАЖДАНКА"): 
                t.addAbridge("ГР.")
                t.addAbridge("ГРАЖД.")
                t.addAbridge("ГР-КА")
            PersonAttrToken.M_TERMINS.add(t)
        for s in ["ПАНІ", "ГРОМАДЯНКА", "УРОДЖЕНКА", "СЕНЬЙОРА", "СЕНЬЙОРА", "МІС", "МІСІС", "МАДАМ", "МАДЕМУАЗЕЛЬ", "ФРАУ", "ФРОЙЛЯЙН", "ЛЕДІ"]: 
            t = PersonAttrTermin._new2299(s, MorphLang.UA, PersonAttrTerminType.PREFIX, MorphGender.FEMINIE)
            if (s == "ГРОМАДЯНКА"): 
                t.addAbridge("ГР.")
                t.addAbridge("ГР-КА")
            PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2299("MISTER", MorphLang.EN, PersonAttrTerminType.PREFIX, MorphGender.MASCULINE)
        t.addAbridge("MR")
        t.addAbridge("MR.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2299("MISSIS", MorphLang.EN, PersonAttrTerminType.PREFIX, MorphGender.FEMINIE)
        t.addAbridge("MRS")
        t.addAbridge("MSR.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2299("MISS", MorphLang.EN, PersonAttrTerminType.PREFIX, MorphGender.FEMINIE)
        t.addAbridge("MS")
        t.addAbridge("MS.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2296("БЕЗРАБОТНЫЙ", PersonAttrTerminType.POSITION)
        t.addVariant("НЕ РАБОТАЮЩИЙ", False)
        t.addVariant("НЕ РАБОТАЕТ", False)
        t.addVariant("ВРЕМЕННО НЕ РАБОТАЮЩИЙ", False)
        t.addVariant("ВРЕМЕННО НЕ РАБОТАЕТ", False)
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2267("БЕЗРОБІТНИЙ", MorphLang.UA, PersonAttrTerminType.POSITION)
        t.addVariant("НЕ ПРАЦЮЮЧИЙ", False)
        t.addVariant("НЕ ПРАЦЮЄ", False)
        t.addVariant("ТИМЧАСОВО НЕ ПРАЦЮЮЧИЙ", False)
        t.addVariant("ТИМЧАСОВО НЕ ПРАЦЮЄ", False)
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2307("ЗАМЕСТИТЕЛЬ", "заместитель", PersonAttrTerminType2.IO2, PersonAttrTerminType.POSITION)
        t.addVariant("ЗАМЕСТИТЕЛЬНИЦА", False)
        t.addAbridge("ЗАМ.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2308("ЗАСТУПНИК", MorphLang.UA, "заступник", PersonAttrTerminType2.IO2, PersonAttrTerminType.POSITION)
        t.addVariant("ЗАСТУПНИЦЯ", False)
        t.addAbridge("ЗАМ.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2307("УПОЛНОМОЧЕННЫЙ", "уполномоченный", PersonAttrTerminType2.IO2, PersonAttrTerminType.POSITION)
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2308("УПОВНОВАЖЕНИЙ", MorphLang.UA, "уповноважений", PersonAttrTerminType2.IO2, PersonAttrTerminType.POSITION)
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2307("ЭКС-УПОЛНОМОЧЕННЫЙ", "экс-уполномоченный", PersonAttrTerminType2.IO2, PersonAttrTerminType.POSITION)
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2308("ЕКС-УПОВНОВАЖЕНИЙ", MorphLang.UA, "екс-уповноважений", PersonAttrTerminType2.IO2, PersonAttrTerminType.POSITION)
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2313("ИСПОЛНЯЮЩИЙ ОБЯЗАННОСТИ", PersonAttrTerminType2.IO, PersonAttrTerminType.POSITION)
        t.addAbridge("И.О.")
        t.acronym = "ИО"
        t.canonic_text = t.acronym
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2314("ВИКОНУЮЧИЙ ОБОВЯЗКИ", MorphLang.UA, PersonAttrTerminType2.IO, PersonAttrTerminType.POSITION)
        t.addAbridge("В.О.")
        t.acronym = "ВО"
        t.canonic_text = t.acronym
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2313("ВРЕМЕННО ИСПОЛНЯЮЩИЙ ОБЯЗАННОСТИ", PersonAttrTerminType2.IO, PersonAttrTerminType.POSITION)
        t.addAbridge("ВР.И.О.")
        t.acronym = "ВРИО"
        t.canonic_text = t.acronym
        PersonAttrToken.M_TERMIN_VRIO = t
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2296("ЗАВЕДУЮЩИЙ", PersonAttrTerminType.POSITION)
        t.addAbridge("ЗАВЕД.")
        t.addAbridge("ЗАВ.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2267("ЗАВІДУВАЧ", MorphLang.UA, PersonAttrTerminType.POSITION)
        t.addAbridge("ЗАВІД.")
        t.addAbridge("ЗАВ.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2296("СОТРУДНИК", PersonAttrTerminType.POSITION)
        t.addAbridge("СОТРУДН.")
        t.addAbridge("СОТР.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2267("СПІВРОБІТНИК", MorphLang.UA, PersonAttrTerminType.POSITION)
        t.addAbridge("СПІВРОБ.")
        t.addAbridge("СПІВ.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2296("АКАДЕМИК", PersonAttrTerminType.POSITION)
        t.addAbridge("АКАД.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2267("АКАДЕМІК", MorphLang.UA, PersonAttrTerminType.POSITION)
        t.addAbridge("АКАД.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2296("ЧЛЕН-КОРРЕСПОНДЕНТ", PersonAttrTerminType.POSITION)
        t.addAbridge("ЧЛ.-КОРР.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2267("ЧЛЕН-КОРЕСПОНДЕНТ", MorphLang.UA, PersonAttrTerminType.POSITION)
        t.addAbridge("ЧЛ.-КОР.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2296("ДОЦЕНТ", PersonAttrTerminType.POSITION)
        t.addAbridge("ДОЦ.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2296("ПРОФЕССОР", PersonAttrTerminType.POSITION)
        t.addAbridge("ПРОФ.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2267("ПРОФЕСОР", MorphLang.UA, PersonAttrTerminType.POSITION)
        t.addAbridge("ПРОФ.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2267("PROFESSOR", MorphLang.EN, PersonAttrTerminType.POSITION)
        t.addAbridge("PROF.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2313("КАНДИДАТ", PersonAttrTerminType2.GRADE, PersonAttrTerminType.POSITION)
        t.addAbridge("КАНД.")
        t.addAbridge("КАН.")
        t.addAbridge("К-Т")
        t.addAbridge("К.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2313("ДОКТОР", PersonAttrTerminType2.GRADE, PersonAttrTerminType.POSITION)
        t.addAbridge("ДОКТ.")
        t.addAbridge("ДОК.")
        t.addAbridge("Д-Р")
        t.addAbridge("Д.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2267("DOCTOR", MorphLang.EN, PersonAttrTerminType.PREFIX)
        t.addAbridge("DR")
        t.addAbridge("DR.")
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2296("ДОКТОРАНТ", PersonAttrTerminType.POSITION)
        PersonAttrToken.M_TERMINS.add(t)
        t = PersonAttrTermin._new2267("ДОКТОРАНТ", MorphLang.UA, PersonAttrTerminType.POSITION)
        PersonAttrToken.M_TERMINS.add(t)
        for s in ["КФН", "КТН", "КХН"]: 
            t = PersonAttrTermin._new2333(s, "кандидат наук", PersonAttrTerminType.POSITION, PersonAttrTerminType2.ABBR)
            PersonAttrToken.M_TERMINS.add(t)
        for s in ["ГЛАВНЫЙ", "МЛАДШИЙ", "СТАРШИЙ", "ВЕДУЩИЙ", "НАУЧНЫЙ"]: 
            t = PersonAttrTermin._new2313(s, PersonAttrTerminType2.ADJ, PersonAttrTerminType.POSITION)
            t.addAllAbridges(0, 0, 2)
            PersonAttrToken.M_TERMINS.add(t)
        for s in ["ГОЛОВНИЙ", "МОЛОДШИЙ", "СТАРШИЙ", "ПРОВІДНИЙ", "НАУКОВИЙ"]: 
            t = PersonAttrTermin._new2335(s, PersonAttrTerminType2.ADJ, PersonAttrTerminType.POSITION, MorphLang.UA)
            t.addAllAbridges(0, 0, 2)
            PersonAttrToken.M_TERMINS.add(t)
        for s in ["НЫНЕШНИЙ", "НОВЫЙ", "CURRENT", "NEW"]: 
            t = PersonAttrTermin._new2313(s, PersonAttrTerminType2.IGNOREDADJ, PersonAttrTerminType.POSITION)
            PersonAttrToken.M_TERMINS.add(t)
        for s in ["НИНІШНІЙ", "НОВИЙ"]: 
            t = PersonAttrTermin._new2335(s, PersonAttrTerminType2.IGNOREDADJ, PersonAttrTerminType.POSITION, MorphLang.UA)
            PersonAttrToken.M_TERMINS.add(t)
        for s in ["ТОГДАШНИЙ", "БЫВШИЙ", "ПРЕДЫДУЩИЙ", "FORMER", "PREVIOUS", "THEN"]: 
            t = PersonAttrTermin._new2313(s, PersonAttrTerminType2.IO, PersonAttrTerminType.POSITION)
            PersonAttrToken.M_TERMINS.add(t)
        for s in ["ТОДІШНІЙ", "КОЛИШНІЙ"]: 
            t = PersonAttrTermin._new2335(s, PersonAttrTerminType2.IO, PersonAttrTerminType.POSITION, MorphLang.UA)
            PersonAttrToken.M_TERMINS.add(t)
        dat = EpNerPersonInternalResourceHelper.getBytes("attr_ru.dat")
        if (dat is None): 
            raise Utils.newException("Not found resource file attr_ru.dat in Person analyzer", None)
        PersonAttrToken.__loadAttrs(PersonAttrToken.M_TERMINS, dat, MorphLang.RU)
        dat = EpNerPersonInternalResourceHelper.getBytes("attr_en.dat")
        if ((dat) is None): 
            raise Utils.newException("Not found resource file attr_en.dat in Person analyzer", None)
        PersonAttrToken.__loadAttrs(PersonAttrToken.M_TERMINS, dat, MorphLang.EN)
        PersonAttrToken.__loadAttrs(PersonAttrToken.M_TERMINS, EpNerPersonInternalResourceHelper.getBytes("attr_ua.dat"), MorphLang.UA)
    
    M_TERMINS = None
    
    M_TERMIN_VRIO = None
    
    @staticmethod
    def __deflate(zip0_ : bytearray) -> bytearray:
        with io.BytesIO() as unzip: 
            data_ = io.BytesIO(zip0_)
            data_.seek(0, io.SEEK_SET)
            MorphSerializeHelper.deflateGzip(data_, unzip)
            data_.close()
            return bytearray(unzip.getvalue())
    
    @staticmethod
    def __loadAttrs(termins : 'TerminCollection', dat : bytearray, lang : 'MorphLang') -> None:
        from pullenti.ner.person.internal.PersonAttrTermin import PersonAttrTermin
        if (dat is None or len(dat) == 0): 
            return
        with io.BytesIO(PersonAttrToken.__deflate(dat)) as tmp: 
            tmp.seek(0, io.SEEK_SET)
            xml0_ = None # new XmlDocument
            xml0_ = xml.etree.ElementTree.parse(tmp)
            for x in xml0_.getroot(): 
                a = Utils.getXmlAttrByName(x.attrib, "v")
                if (a is None): 
                    continue
                val = a[1]
                if (val is None): 
                    continue
                attrs = ("" if Utils.getXmlAttrByName(x.attrib, "a") is None else (Utils.ifNotNull(Utils.getXmlAttrByName(x.attrib, "a")[1], "")))
                if (val == "ОТЕЦ"): 
                    pass
                pat = PersonAttrTermin._new2340(val, PersonAttrTerminType.POSITION, lang)
                for ch in attrs: 
                    if (ch == 'p'): 
                        pat.can_has_person_after = 1
                    elif (ch == 'P'): 
                        pat.can_has_person_after = 2
                    elif (ch == 's'): 
                        pat.can_be_same_surname = True
                    elif (ch == 'm'): 
                        pat.gender = MorphGender.MASCULINE
                    elif (ch == 'f'): 
                        pat.gender = MorphGender.FEMINIE
                    elif (ch == 'b'): 
                        pat.is_boss = True
                    elif (ch == 'r'): 
                        pat.is_military_rank = True
                    elif (ch == 'n'): 
                        pat.is_nation = True
                    elif (ch == 'c'): 
                        pat.typ = PersonAttrTerminType.KING
                    elif (ch == 'q'): 
                        pat.typ = PersonAttrTerminType.KING
                    elif (ch == 'k'): 
                        pat.is_kin = True
                    elif (ch == 'a'): 
                        pat.typ2 = PersonAttrTerminType2.IO2
                    elif (ch == '1'): 
                        pat.can_be_independant = True
                    elif (ch == '?'): 
                        pat.is_doubt = True
                if (Utils.getXmlAttrByName(x.attrib, "alt") is not None): 
                    val = Utils.getXmlAttrByName(x.attrib, "alt")[1]
                    pat.addVariant(val, False)
                    if (val.find('.') > 0): 
                        pat.addAbridge(val)
                if (len(x) > 0): 
                    for xx in x: 
                        if (xx.tag == "alt"): 
                            val = Utils.getXmlInnerText(xx)
                            pat.addVariant(val, False)
                            if (val.find('.') > 0): 
                                pat.addAbridge(val)
                termins.add(pat)
    
    @staticmethod
    def _new2256(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.morph = _arg3
        return res
    
    @staticmethod
    def _new2257(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2261(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType', _arg4 : str, _arg5 : 'MorphCollection') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.age = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new2263(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType', _arg4 : 'MorphCollection') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new2265(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType', _arg4 : str) -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new2271(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType', _arg4 : str, _arg5 : 'MorphCollection', _arg6 : 'MorphGender') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.morph = _arg5
        res.gender = _arg6
        return res
    
    @staticmethod
    def _new2274(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : 'PersonAttrToken') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.morph = _arg3
        res.higher_prop_ref = _arg4
        return res
    
    @staticmethod
    def _new2280(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonPropertyReferent', _arg4 : 'PersonAttrTerminType') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.prop_ref = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new2292(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType', _arg4 : 'PersonPropertyReferent', _arg5 : 'MorphCollection') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.prop_ref = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new2295(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType', _arg4 : 'PersonPropertyReferent', _arg5 : 'MorphCollection', _arg6 : bool) -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.prop_ref = _arg4
        res.morph = _arg5
        res.can_be_independent_property = _arg6
        return res
    
    # static constructor for class PersonAttrToken
    @staticmethod
    def _static_ctor():
        PersonAttrToken.M_EMPTY_ADJS = ["УСПЕШНЫЙ", "ИЗВЕСТНЫЙ", "ЗНАМЕНИТЫЙ", "ИЗВЕСТНЕЙШИЙ", "ПОПУЛЯРНЫЙ", "ГЕНИАЛЬНЫЙ", "ТАЛАНТЛИВЫЙ", "МОЛОДОЙ", "УСПІШНИЙ", "ВІДОМИЙ", "ЗНАМЕНИТИЙ", "ВІДОМИЙ", "ПОПУЛЯРНИЙ", "ГЕНІАЛЬНИЙ", "ТАЛАНОВИТИЙ", "МОЛОДИЙ"]
        PersonAttrToken.M_STD_FORMS = dict()

PersonAttrToken._static_ctor()