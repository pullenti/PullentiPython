# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
import xml.etree.ElementTree
from enum import IntEnum
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
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
from pullenti.ner.person.internal.ResourceHelper import ResourceHelper
from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper


class PersonAttrToken(ReferentToken):
    
    class PersonAttrAttachAttrs(IntEnum):
        NO = 0
        AFTERZAMESTITEL = 1
        ONLYKEYWORD = 2
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        self.typ = PersonAttrTerminType.PREFIX
        self.gender = MorphGender.UNDEFINED
        self.value = None
        self._king_surname = None
        self.age = None
        self.higher_prop_ref = None
        self.add_outer_org_as_ref = False
        self.anafor = None
        self.__m_can_be_independent_property = False
        self.can_be_single_person = False
        self.can_has_person_after = 0
        self.can_be_same_surname = False
        self.is_doubt = False
        super().__init__(None, begin, end, None)
    
    @property
    def prop_ref(self) -> 'PersonPropertyReferent':
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        return (self.referent if isinstance(self.referent, PersonPropertyReferent) else None)
    
    @prop_ref.setter
    def prop_ref(self, value_) -> 'PersonPropertyReferent':
        self.referent = value_
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
        if (self.prop_ref.find_slot(PersonPropertyReferent.ATTR_REF, None, True) is not None): 
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
        res = Utils.newStringIO(None)
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
        if (not self.morph.case.is_undefined): 
            print("; {0}".format(str(self.morph.case)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def save_to_local_ontology(self) -> None:
        ad = self.data
        if (ad is None or self.prop_ref is None or self.higher_prop_ref is None): 
            super().save_to_local_ontology()
            return
        li = list()
        pr = self
        while pr is not None and pr.prop_ref is not None: 
            li.insert(0, pr)
            pr = pr.higher_prop_ref
        for i in range(len(li)):
            li[i].data = ad
            li[i].higher_prop_ref = None
            li[i].save_to_local_ontology()
            if ((i + 1) < len(li)): 
                li[i + 1].prop_ref.higher = li[i].prop_ref
    
    @staticmethod
    def try_attach(t : 'Token', loc_onto : 'IntOntologyCollection', attrs : 'PersonAttrAttachAttrs'=PersonAttrAttachAttrs.NO) -> 'PersonAttrToken':
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
        inoutarg2065 = RefOutArgWrapper(None)
        inoutres2066 = Utils.tryGetValue(t.kit.misc_data, "pat", inoutarg2065)
        olev = inoutarg2065.value
        if (not inoutres2066): 
            lev = 1
            t.kit.misc_data["pat"] = lev
        else: 
            lev = olev
            if (lev > 2): 
                return None
            lev += 1
            t.kit.misc_data["pat"] = lev
        res = PersonAttrToken.__try_attach(t, loc_onto, attrs)
        lev -= 1
        if (lev < 0): 
            lev = 0
        t.kit.misc_data["pat"] = lev
        if (res is None): 
            if (t.morph.class0.is_noun): 
                aterr = (t.kit.processor.find_analyzer("GEO") if isinstance(t.kit.processor.find_analyzer("GEO"), GeoAnalyzer) else None)
                if (aterr is not None): 
                    rt = aterr.process_citizen(t)
                    if (rt is not None): 
                        res = PersonAttrToken._new2062(rt.begin_token, rt.end_token, rt.morph)
                        res.prop_ref = PersonPropertyReferent()
                        res.prop_ref.add_slot(PersonPropertyReferent.ATTR_NAME, ("громадянин" if t.kit.base_language.is_ua else "гражданин"), True, 0)
                        res.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, rt.referent, True, 0)
                        res.prop_ref.add_ext_referent(rt)
                        res.typ = PersonAttrTerminType.POSITION
                        if ((res.end_token.next0 is not None and res.end_token.next0.is_value("ПО", None) and res.end_token.next0.next0 is not None) and res.end_token.next0.next0.is_value("ПРОИСХОЖДЕНИЕ", None)): 
                            res.end_token = res.end_token.next0.next0
                        return res
            if (((((isinstance(t, TextToken))) and (t if isinstance(t, TextToken) else None).term == "АК" and t.next0 is not None) and t.next0.is_char('.') and t.next0.next0 is not None) and not t.next0.next0.chars.is_all_lower): 
                res = PersonAttrToken._new2063(t, t.next0, PersonAttrTerminType.POSITION)
                res.prop_ref = PersonPropertyReferent._new2064("академик")
                return res
            if (isinstance(t, TextToken) and t.next0 is not None): 
                if (((t.is_value("ВИЦЕ", "ВІЦЕ") or t.is_value("ЭКС", "ЕКС") or t.is_value("ГЕН", None)) or t.is_value("VICE", None) or t.is_value("EX", None)) or t.is_value("DEPUTY", None)): 
                    tt = t.next0
                    if (tt.is_hiphen or tt.is_char('.')): 
                        tt = tt.next0
                    res = PersonAttrToken.__try_attach(tt, loc_onto, attrs)
                    if (res is not None and res.prop_ref is not None): 
                        res.begin_token = t
                        if (t.is_value("ГЕН", None)): 
                            res.prop_ref.name = "генеральный {0}".format(res.prop_ref.name)
                        else: 
                            res.prop_ref.name = "{0}-{1}".format((t if isinstance(t, TextToken) else None).term.lower(), res.prop_ref.name)
                        return res
            if (t.is_value("ГВАРДИИ", "ГВАРДІЇ")): 
                res = PersonAttrToken.__try_attach(t.next0, loc_onto, attrs)
                if (res is not None): 
                    if (res.prop_ref is not None and res.prop_ref.kind == PersonPropertyKind.MILITARYRANK): 
                        res.begin_token = t
                        return res
            tt1 = t
            if (tt1.morph.class0.is_preposition and tt1.next0 is not None): 
                tt1 = tt1.next0
            if ((tt1.next0 is not None and tt1.is_value("НАЦИОНАЛЬНОСТЬ", "НАЦІОНАЛЬНІСТЬ")) or tt1.is_value("ПРОФЕССИЯ", "ПРОФЕСІЯ") or tt1.is_value("СПЕЦИАЛЬНОСТЬ", "СПЕЦІАЛЬНІСТЬ")): 
                tt1 = tt1.next0
                if (tt1.is_hiphen or tt1.is_char(':')): 
                    tt1 = tt1.next0
                res = PersonAttrToken.__try_attach(tt1, loc_onto, attrs)
                if (res is not None): 
                    res.begin_token = t
                    return res
            return None
        if (res.typ == PersonAttrTerminType.OTHER and res.age is not None and res.value is None): 
            res1 = PersonAttrToken.__try_attach(res.end_token.next0, loc_onto, attrs)
            if (res1 is not None): 
                res1.begin_token = res.begin_token
                res1.age = res.age
                res = res1
        if (res.begin_token.is_value("ГЛАВА", None)): 
            if (isinstance(t.previous, NumberToken)): 
                return None
        elif (res.begin_token.is_value("АДВОКАТ", None)): 
            if (t.previous is not None): 
                if (t.previous.is_value("РЕЕСТР", "РЕЄСТР") or t.previous.is_value("УДОСТОВЕРЕНИЕ", "ПОСВІДЧЕННЯ")): 
                    return None
        mc = res.begin_token.get_morph_class_in_dictionary()
        if (mc.is_adjective): 
            npt = NounPhraseHelper.try_parse(res.begin_token, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.end_char > res.end_char): 
                if (PersonAttrToken.__m_termins.try_parse(npt.end_token, TerminParseAttr.NO) is None): 
                    return None
        if (res.typ == PersonAttrTerminType.PREFIX and (((((res.value == "ГРАЖДАНИН" or res.value == "ГРАЖДАНКА" or res.value == "УРОЖЕНЕЦ") or res.value == "УРОЖЕНКА" or res.value == "ГРОМАДЯНИН") or res.value == "ГРОМАДЯНКА" or res.value == "УРОДЖЕНЕЦЬ") or res.value == "УРОДЖЕНКА")) and res.end_token.next0 is not None): 
            tt = res.end_token.next0
            if (((tt is not None and tt.is_char('(') and tt.next0 is not None) and tt.next0.is_value("КА", None) and tt.next0.next0 is not None) and tt.next0.next0.is_char(')')): 
                res.end_token = tt.next0.next0
                tt = res.end_token.next0
            r = (None if tt is None else tt.get_referent())
            if (r is not None and r.type_name == PersonAttrToken.__obj_name_geo): 
                res.end_token = tt
                res.prop_ref = PersonPropertyReferent()
                res.prop_ref.add_slot(PersonPropertyReferent.ATTR_NAME, res.value.lower(), True, 0)
                res.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, r, True, 0)
                res.typ = PersonAttrTerminType.POSITION
            elif ((tt is not None and tt.is_and and tt.next0 is not None) and tt.next0.is_value("ЖИТЕЛЬ", None)): 
                aaa = PersonAttrToken.__try_attach(tt.next0, loc_onto, attrs)
                if (aaa is not None and aaa.prop_ref is not None): 
                    aaa.begin_token = res.begin_token
                    aaa.value = res.value
                    aaa.prop_ref.name = aaa.value.lower()
                    res = aaa
        if (res.typ == PersonAttrTerminType.KING or res.typ == PersonAttrTerminType.POSITION): 
            if (res.begin_token == res.end_token and res.chars.is_capital_upper and res.whitespaces_after_count == 1): 
                pit = PersonItemToken.try_attach(t, loc_onto, PersonItemToken.ParseAttr.IGNOREATTRS, None)
                if (pit is not None and pit.lastname is not None and pit.lastname.is_lastname_has_std_tail): 
                    rt1 = t.kit.process_referent("PERSON", t.next0)
                    if (rt1 is not None and isinstance(rt1.referent, PersonReferent)): 
                        pass
                    else: 
                        return None
        if (res.prop_ref is None): 
            return res
        if (res.chars.is_latin_letter): 
            tt = res.end_token.next0
            if (tt is not None and tt.is_hiphen): 
                tt = tt.next0
            if (tt is not None and tt.is_value("ELECT", None)): 
                res.end_token = tt
        if (not res.begin_token.chars.is_all_lower): 
            pat = PersonItemToken.try_attach(res.begin_token, loc_onto, PersonItemToken.ParseAttr.IGNOREATTRS, None)
            if (pat is not None and pat.lastname is not None): 
                if (pat.lastname.is_in_dictionary or pat.lastname.is_in_ontology): 
                    if (PersonAttrToken.check_kind(res.prop_ref) != PersonPropertyKind.KING): 
                        return None
        s = str(res.prop_ref)
        if (s == "глава книги"): 
            return None
        if (s == "глава" and res.prop_ref.find_slot(PersonPropertyReferent.ATTR_REF, None, True) is None): 
            return None
        if (((s == "королева" or s == "король" or s == "князь")) and res.chars.is_capital_upper): 
            pits = PersonItemToken.try_attach_list(res.end_token.next0, loc_onto, PersonItemToken.ParseAttr.NO, 10)
            if (pits is not None and len(pits) > 0): 
                if (pits[0].typ == PersonItemToken.ItemType.INITIAL): 
                    return None
                if (pits[0].firstname is not None): 
                    if (len(pits) == 1): 
                        return None
                    if (len(pits) == 2 and pits[1].middlename is not None): 
                        return None
            if (not MiscHelper.can_be_start_of_sentence(t)): 
                return None
        if (s == "друг" or s.startswith("друг ")): 
            if (t.previous is not None): 
                if (t.previous.is_value("ДРУГ", None)): 
                    return None
                if (t.previous.morph.class0.is_preposition and t.previous.previous is not None and t.previous.previous.is_value("ДРУГ", None)): 
                    return None
            if (t.next0 is not None): 
                if (t.next0.is_value("ДРУГ", None)): 
                    return None
                if (t.next0.morph.class0.is_preposition and t.next0.next0 is not None and t.next0.next0.is_value("ДРУГ", None)): 
                    return None
        if (res.chars.is_latin_letter and ((res.is_doubt or s == "senior")) and (res.whitespaces_after_count < 2)): 
            if (res.prop_ref is not None and len(res.prop_ref.slots) == 1): 
                tt2 = res.end_token.next0
                if (MiscHelper.is_eng_adj_suffix(tt2)): 
                    tt2 = tt2.next0.next0
                res2 = PersonAttrToken.__try_attach(tt2, loc_onto, attrs)
                if ((res2 is not None and res2.chars.is_latin_letter and res2.typ == res.typ) and res2.prop_ref is not None): 
                    res2.prop_ref.name = "{0} {1}".format(Utils.ifNotNull(res.prop_ref.name, ""), Utils.ifNotNull(res2.prop_ref.name, "")).strip()
                    res2.begin_token = res.begin_token
                    res = res2
        if (res.prop_ref.name == "министр"): 
            rt1 = res.kit.process_referent("ORGANIZATION", res.end_token.next0)
            if (rt1 is not None and rt1.referent.find_slot("TYPE", "министерство", True) is not None): 
                t1 = rt1.end_token
                if (isinstance(t1.get_referent(), GeoReferent)): 
                    t1 = t1.previous
                if (rt1.begin_char < t1.end_char): 
                    add_str = MiscHelper.get_text_value(rt1.begin_token, t1, GetTextAttr.NO)
                    if (add_str is not None): 
                        res.prop_ref.name += (" " + add_str.lower())
                        res.end_token = t1
        p = res.prop_ref
        while p is not None: 
            if (p.name is not None and " - " in p.name): 
                p.name = p.name.replace(" - ", "-")
            p = p.higher
        if (res.begin_token.morph.class0.is_adjective): 
            r = res.kit.process_referent("GEO", res.begin_token)
            if (r is not None): 
                res.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, r.referent, False, 0)
                res.prop_ref.add_ext_referent(r)
                i = res.prop_ref.name.find(' ')
                if (i > 0): 
                    res.prop_ref.name = res.prop_ref.name[i : ].strip()
        contains_geo = False
        for ss in res.prop_ref.slots: 
            if (isinstance(ss.value, Referent)): 
                if ((ss.value if isinstance(ss.value, Referent) else None).type_name == PersonAttrToken.__obj_name_geo): 
                    contains_geo = True
                    break
        if (not contains_geo and (res.end_token.whitespaces_after_count < 2)): 
            if (isinstance(res.end_token.next0, ReferentToken) and res.end_token.next0.get_referent().type_name == PersonAttrToken.__obj_name_geo): 
                res.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, res.end_token.next0.get_referent(), False, 0)
                res.end_token = res.end_token.next0
        if (res.end_token.whitespaces_after_count < 2): 
            te = res.end_token.next0
            if (te is not None and te.is_value("В", None)): 
                te = te.next0
                if (isinstance(te, ReferentToken) and ((te.get_referent().type_name == PersonAttrToken.__obj_name_date or te.get_referent().type_name == PersonAttrToken.__obj_name_date_range))): 
                    res.end_token = te
            elif (te is not None and te.is_char('(')): 
                te = te.next0
                if ((isinstance(te, ReferentToken) and ((te.get_referent().type_name == PersonAttrToken.__obj_name_date or te.get_referent().type_name == PersonAttrToken.__obj_name_date_range)) and te.next0 is not None) and te.next0.is_char(')')): 
                    res.end_token = te.next0
                elif (isinstance(te, NumberToken)): 
                    rt1 = te.kit.process_referent("DATE", te)
                    if (rt1 is not None and rt1.end_token.next0 is not None and rt1.end_token.next0.is_char(')')): 
                        res.end_token = rt1.end_token.next0
        if (res.prop_ref is not None and res.prop_ref.name == "отец"): 
            is_king = False
            tt = res.end_token.next0
            if (isinstance(tt, TextToken) and tt.get_morph_class_in_dictionary().is_proper_name): 
                if (not (res.morph.case & tt.morph.case).is_undefined): 
                    if (not tt.morph.case.is_genitive): 
                        is_king = True
            if (is_king): 
                res.prop_ref.name = "священник"
        if (res.prop_ref is not None and res.prop_ref.kind == PersonPropertyKind.KING): 
            t1 = res.end_token.next0
            if (res.prop_ref.name == "отец"): 
                if (t1 is None or not t1.chars.is_capital_upper): 
                    return None
                if ((res.morph.case & t1.morph.case).is_undefined): 
                    return None
                res.prop_ref.name = "священник"
                return res
            if (t1 is not None and t1.chars.is_capital_upper and t1.morph.class0.is_adjective): 
                res._king_surname = PersonItemToken.try_attach(t1, loc_onto, PersonItemToken.ParseAttr.IGNOREATTRS, None)
                if ((res._king_surname) is not None): 
                    res.end_token = t1
                    if ((t1.next0 is not None and t1.next0.is_and and t1.next0.next0 is not None) and t1.next0.next0.is_value("ВСЕЯ", None)): 
                        t1 = t1.next0.next0.next0
                        geo_ = (((None if t1 is None else t1.get_referent())) if isinstance(((None if t1 is None else t1.get_referent())), GeoReferent) else None)
                        if (geo_ is not None): 
                            res.end_token = t1
                            res.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, geo_, False, 0)
        if (res.can_has_person_after > 0 and res.prop_ref.find_slot(PersonPropertyReferent.ATTR_REF, None, True) is None): 
            npt = NounPhraseHelper.try_parse(res.begin_token, NounPhraseParseAttr.NO, 0)
            tt0 = res.begin_token
            if (isinstance(tt0, TextToken) and tt0.morph.class0.is_personal_pronoun and ((tt0.is_value("ОН", None) or tt0.is_value("ОНА", None)))): 
                pass
            else: 
                tt0 = tt0.previous
                if (isinstance(tt0, TextToken) and tt0.morph.class0.is_personal_pronoun and ((tt0.is_value("ОН", None) or tt0.is_value("ОНА", None)))): 
                    pass
                elif (isinstance(tt0, TextToken) and tt0.morph.class0.is_pronoun and tt0.is_value("СВОЙ", None)): 
                    pass
                else: 
                    tt0 = None
            if (tt0 is not None): 
                gen = MorphGender.UNDEFINED
                cou = 0
                for wf in tt0.morph.items: 
                    if (wf.class0.is_personal_pronoun or wf.class0.is_pronoun): 
                        gen = wf.gender
                        if (((gen)) == MorphGender.NEUTER): 
                            gen = MorphGender.MASCULINE
                        break
                tt = tt0.previous
                first_pass2851 = True
                while True:
                    if first_pass2851: first_pass2851 = False
                    else: tt = tt.previous; cou += 1
                    if (not (tt is not None and (cou < 200))): break
                    pr = (tt.get_referent() if isinstance(tt.get_referent(), PersonPropertyReferent) else None)
                    if (pr is not None): 
                        if (((tt.morph.gender & gen)) == MorphGender.UNDEFINED): 
                            continue
                        break
                    p = (tt.get_referent() if isinstance(tt.get_referent(), PersonReferent) else None)
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
                    res.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, p, False, 0)
                    res.can_be_independent_property = True
                    if (res.morph.number != MorphNumber.PLURAL): 
                        res.can_be_single_person = True
                    npt = NounPhraseHelper.try_parse(tt0, NounPhraseParseAttr.NO, 0)
                    if (npt is not None and npt.begin_token != npt.end_token): 
                        res.morph = npt.morph
                    break
            elif (res.whitespaces_after_count == 1): 
                pa = (res.kit.processor.find_analyzer("PERSON") if isinstance(res.kit.processor.find_analyzer("PERSON"), PersonAnalyzer) else None)
                if (pa is not None): 
                    t1 = res.end_token.next0
                    pr = PersonAnalyzer._try_attach_person(t1, (res.kit.get_analyzer_data(pa) if isinstance(res.kit.get_analyzer_data(pa), PersonAnalyzer.PersonAnalyzerData) else None), False, 0, True)
                    if (pr is not None and res.can_has_person_after == 1): 
                        if (pr.begin_token == t1): 
                            if (not pr.morph.case.is_genitive and not pr.morph.case.is_undefined): 
                                pr = None
                            elif (not pr.morph.case.is_undefined and not (res.morph.case & pr.morph.case).is_undefined): 
                                if (PersonAnalyzer._try_attach_person(pr.end_token.next0, (res.kit.get_analyzer_data(pa) if isinstance(res.kit.get_analyzer_data(pa), PersonAnalyzer.PersonAnalyzerData) else None), False, 0, True) is not None): 
                                    pass
                                else: 
                                    pr = None
                        elif (pr.begin_token.previous == t1): 
                            pr = None
                            res.prop_ref.name = "{0} {1}".format(res.prop_ref.name, t1.get_source_text().lower())
                            res.end_token = t1
                        else: 
                            pr = None
                    if (pr is not None): 
                        res.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, pr, False, 0)
                        res.end_token = pr.end_token
                        res.can_be_independent_property = True
                        if (res.morph.number != MorphNumber.PLURAL): 
                            res.can_be_single_person = True
        if (res.prop_ref.higher is None and res.prop_ref.kind == PersonPropertyKind.BOSS and res.prop_ref.find_slot(PersonPropertyReferent.ATTR_REF, None, True) is None): 
            tok = PersonAttrToken.__m_termins.try_parse(res.begin_token, TerminParseAttr.NO)
            if (tok is not None and tok.end_token == res.end_token): 
                cou = 0
                refs = list()
                tt = tok.begin_token.previous
                first_pass2852 = True
                while True:
                    if first_pass2852: first_pass2852 = False
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
                    li = tt.get_referents()
                    if (li is None): 
                        continue
                    breaks = False
                    for r in li: 
                        if (((r.type_name == "ORGANIZATION" or r.type_name == "GEO")) and r.parent_referent is None): 
                            if (not r in refs): 
                                if (res.prop_ref.can_has_ref(r)): 
                                    refs.append(r)
                        elif (isinstance(r, PersonPropertyReferent)): 
                            if ((r if isinstance(r, PersonPropertyReferent) else None).find_slot(PersonPropertyReferent.ATTR_REF, None, True) is not None): 
                                breaks = True
                        elif (isinstance(r, PersonReferent)): 
                            breaks = True
                    if (len(refs) > 1 or breaks): 
                        break
                if (len(refs) == 1): 
                    res.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, refs[0], False, 0)
                    res.add_outer_org_as_ref = True
        if (res.chars.is_latin_letter and res.prop_ref is not None and res.prop_ref.find_slot(PersonPropertyReferent.ATTR_REF, None, True) is None): 
            if (res.begin_token.previous is not None and res.begin_token.previous.is_value("S", None)): 
                if (MiscHelper.is_eng_adj_suffix(res.begin_token.previous.previous) and isinstance(res.begin_token.previous.previous.previous, ReferentToken)): 
                    res.begin_token = res.begin_token.previous.previous.previous
                    res.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, res.begin_token.get_referent(), False, 0)
        if (res.chars.is_latin_letter and res.prop_ref is not None and (res.whitespaces_after_count < 2)): 
            rnext = PersonAttrToken.try_attach(res.end_token.next0, loc_onto, PersonAttrToken.PersonAttrAttachAttrs.NO)
            if ((rnext is not None and rnext.chars.is_latin_letter and rnext.prop_ref is not None) and len(rnext.prop_ref.slots) == 1 and rnext.can_has_person_after > 0): 
                res.end_token = rnext.end_token
                res.prop_ref.name = "{0} {1}".format(res.prop_ref.name, rnext.prop_ref.name)
        return res
    
    @staticmethod
    def __try_attach(t : 'Token', loc_onto : 'IntOntologyCollection', attrs : 'PersonAttrAttachAttrs') -> 'PersonAttrToken':
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
        if (t.morph.class0.is_pronoun and (((t.is_value("ЕГО", "ЙОГО") or t.is_value("ЕЕ", "ЇЇ") or t.is_value("HIS", None)) or t.is_value("HER", None)))): 
            res1 = PersonAttrToken.try_attach(t.next0, loc_onto, attrs)
            if (res1 is not None and res1.prop_ref is not None): 
                k = 0
                tt2 = t.previous
                first_pass2853 = True
                while True:
                    if first_pass2853: first_pass2853 = False
                    else: tt2 = tt2.previous; k += 1
                    if (not (tt2 is not None and (k < 10))): break
                    r = tt2.get_referent()
                    if (r is None): 
                        continue
                    if (r.type_name == PersonAttrToken.__obj_name_org or isinstance(r, PersonReferent)): 
                        ok = False
                        if (t.is_value("ЕЕ", "ЇЇ") or t.is_value("HER", None)): 
                            if (tt2.morph.gender == MorphGender.FEMINIE): 
                                ok = True
                        elif (((tt2.morph.gender & ((MorphGender.MASCULINE | MorphGender.NEUTER)))) != MorphGender.UNDEFINED): 
                            ok = True
                        if (ok): 
                            res1.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                            res1.begin_token = t
                            return res1
                        break
            return None
        nta = NumberHelper.try_parse_age(t)
        if (nta is not None): 
            if (nta.morph.class0.is_adjective or ((t.previous is not None and t.previous.is_comma)) or ((nta.end_token.next0 is not None and nta.end_token.next0.is_char_of(",.")))): 
                return PersonAttrToken._new2067(t, nta.end_token, PersonAttrTerminType.OTHER, str(nta.value), nta.morph)
        if (t.is_newline_before): 
            li = MailLine.parse(t, 0)
            if (li is not None and li.typ == MailLine.Types.BESTREGARDS): 
                return PersonAttrToken._new2069(li.begin_token, li.end_token, PersonAttrTerminType.BESTREGARDS, MorphCollection._new2068(MorphCase.NOMINATIVE))
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None): 
            nt = (t if isinstance(t, NumberToken) else None)
            if (nt is not None): 
                if (((nt.value == 1 or nt.value == 2)) and nt.morph.class0.is_adjective): 
                    pat0 = PersonAttrToken.__try_attach(t.next0, loc_onto, attrs)
                    if (pat0 is not None and pat0.prop_ref is not None): 
                        pat0.begin_token = t
                        for s in pat0.prop_ref.slots: 
                            if (s.type_name == PersonPropertyReferent.ATTR_NAME): 
                                if ("глава" in str(s.value)): 
                                    return None
                                pat0.prop_ref.upload_slot(s, "{0} {1}".format(((("первая" if nt.value == 1 else "вторая")) if pat0.morph.gender == MorphGender.FEMINIE or t.morph.gender == MorphGender.FEMINIE else (("первый" if nt.value == 1 else "второй"))), s.value))
                        return pat0
            rr = None
            if (t is not None): 
                rr = t.get_referent()
            if (rr is not None and ((isinstance(rr, GeoReferent) or rr.type_name == "ORGANIZATION"))): 
                ttt = t.next0
                if (MiscHelper.is_eng_adj_suffix(ttt)): 
                    ttt = ttt.next0.next0
                if (isinstance(ttt, TextToken) and ttt.morph.language.is_en and (ttt.whitespaces_before_count < 2)): 
                    res0 = PersonAttrToken.__try_attach(ttt, loc_onto, attrs)
                    if (res0 is not None and res0.prop_ref is not None): 
                        res0.begin_token = t
                        res0.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, t.get_referent(), False, 0)
                        return res0
            if (isinstance(rr, PersonReferent) and MiscHelper.is_eng_adj_suffix(t.next0)): 
                res0 = PersonAttrToken.__try_attach(t.next0.next0.next0, loc_onto, attrs)
                if (res0 is not None and res0.prop_ref is not None and res0.chars.is_latin_letter): 
                    res0.begin_token = t
                    res0.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, t.get_referent(), False, 0)
                    return res0
            return None
        if (MiscHelper.is_eng_article(tt)): 
            res0 = PersonAttrToken.__try_attach(t.next0, loc_onto, attrs)
            if (res0 is not None): 
                res0.begin_token = t
                return res0
        if ((tt.term == "Г" or tt.term == "ГР" or tt.term == "М") or tt.term == "Д"): 
            if (tt.next0 is not None and tt.next0.is_hiphen and isinstance(tt.next0.next0, TextToken)): 
                pref = tt.term
                tail = (tt.next0.next0 if isinstance(tt.next0.next0, TextToken) else None).term
                vars0 = None
                if (pref == "Г"): 
                    vars0 = PersonAttrToken.__get_std_forms(tail, "ГОСПОДИН", "ГОСПОЖА")
                elif (pref == "ГР"): 
                    vars0 = PersonAttrToken.__get_std_forms(tail, "ГРАЖДАНИН", "ГРАЖДАНКА")
                elif (pref == "М"): 
                    vars0 = PersonAttrToken.__get_std_forms(tail, "МИСТЕР", None)
                elif (pref == "Д"): 
                    if (PersonAttrToken.__find_grade_last(tt.next0.next0.next0, tt) is not None): 
                        pass
                    else: 
                        vars0 = PersonAttrToken.__get_std_forms(tail, "ДОКТОР", None)
                if (vars0 is not None): 
                    res = PersonAttrToken._new2063(tt, tt.next0.next0, PersonAttrTerminType.PREFIX)
                    for v in vars0: 
                        res.morph.add_item(v)
                        if (res.value is None): 
                            res.value = v.normal_case
                            res.gender = v.gender
                    return res
        if (tt.term == "ГР" or tt.term == "ГРАЖД"): 
            t1 = tt
            if (tt.next0 is not None and tt.next0.is_char('.')): 
                t1 = tt.next0
            if (isinstance(t1.next0, NumberToken)): 
                return None
            return PersonAttrToken._new2071(tt, t1, PersonAttrTerminType.PREFIX, ("ГРОМАДЯНИН" if tt.morph.language.is_ua else "ГРАЖДАНИН"))
        npt0 = None
        step = 0
        while step < 2: 
            toks = PersonAttrToken.__m_termins.try_parse_all(t, TerminParseAttr.NO)
            if (toks is None and t.is_value("ВРИО", None)): 
                toks = list()
                toks.append(TerminToken._new597(t, t, PersonAttrToken.__m_termin_vrio))
            elif (toks is None and isinstance(t, TextToken) and t.morph.language.is_en): 
                str0 = (t if isinstance(t, TextToken) else None).term
                if (str0.endswith("MAN") or str0.endswith("PERSON") or str0.endswith("MIST")): 
                    toks = list()
                    toks.append(TerminToken._new597(t, t, PersonAttrTermin._new2073(str0, t.morph.language, PersonAttrTerminType.POSITION)))
                elif (str0 == "MODEL" and (t.whitespaces_after_count < 2)): 
                    rt = t.kit.process_referent("PERSON", t.next0)
                    if (rt is not None and isinstance(rt.referent, PersonReferent)): 
                        toks = list()
                        toks.append(TerminToken._new597(t, t, PersonAttrTermin._new2073(str0, t.morph.language, PersonAttrTerminType.POSITION)))
            if ((toks is None and step == 0 and t.chars.is_latin_letter) and (t.whitespaces_after_count < 2)): 
                npt1 = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
                if (npt1 is not None and npt1.begin_token != npt1.end_token): 
                    pits = PersonItemToken.try_attach_list(t, loc_onto, Utils.valToEnum(PersonItemToken.ParseAttr.CANBELATIN | PersonItemToken.ParseAttr.IGNOREATTRS, PersonItemToken.ParseAttr), 10)
                    if (pits is not None and len(pits) > 1 and pits[0].firstname is not None): 
                        npt1 = None
                    k = 0
                    if (npt1 is not None): 
                        tt2 = npt1.begin_token
                        while tt2 is not None and tt2.end_char <= npt1.end_char: 
                            toks1 = PersonAttrToken.__m_termins.try_parse_all(tt2, TerminParseAttr.NO)
                            if (toks1 is not None): 
                                step = 1
                                toks = toks1
                                npt0 = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, toks1[0].end_char)
                                if (not (toks[0].termin if isinstance(toks[0].termin, PersonAttrTermin) else None).is_doubt): 
                                    if (toks[0].morph.number == MorphNumber.PLURAL): 
                                        pass
                                    else: 
                                        break
                            k += 1
                            if (k >= 3 and t.chars.is_all_lower): 
                                if (not MiscHelper.is_eng_article(t.previous)): 
                                    break
                            tt2 = tt2.next0
                elif (((npt1 is None or npt1.end_token == t)) and t.chars.is_capital_upper): 
                    mc = t.get_morph_class_in_dictionary()
                    if ((mc.is_misc or mc.is_preposition or mc.is_conjunction) or mc.is_personal_pronoun or mc.is_pronoun): 
                        pass
                    else: 
                        tt1 = None
                        if ((t.next0 is not None and t.next0.is_hiphen and not t.is_whitespace_after) and not t.next0.is_whitespace_after): 
                            tt1 = t.next0.next0
                        elif (npt1 is None): 
                            tt1 = t.next0
                        toks1 = PersonAttrToken.__m_termins.try_parse_all(tt1, TerminParseAttr.NO)
                        if (toks1 is not None and (toks1[0].termin if isinstance(toks1[0].termin, PersonAttrTermin) else None).typ == PersonAttrTerminType.POSITION and (tt1.whitespaces_before_count < 2)): 
                            step = 1
                            toks = toks1
            if (toks is not None): 
                for tok in toks: 
                    if (((tok.morph.class0.is_preposition or tok.morph.contains_attr("к.ф.", MorphClass()))) and tok.end_token == tok.begin_token): 
                        continue
                    pat = (tok.termin if isinstance(tok.termin, PersonAttrTermin) else None)
                    if (isinstance(tok.end_token, TextToken) and pat.canonic_text.startswith((tok.end_token if isinstance(tok.end_token, TextToken) else None).term)): 
                        if (tok.length_char < len(pat.canonic_text)): 
                            if (tok.end_token.next0 is not None and tok.end_token.next0.is_char('.')): 
                                tok.end_token = tok.end_token.next0
                    if (pat.typ == PersonAttrTerminType.PREFIX): 
                        if (step == 0 or ((pat.canonic_text != "ГРАЖДАНИН" and pat.canonic_text != "ГРОМАДЯНИН"))): 
                            return PersonAttrToken._new2077(tok.begin_token, tok.end_token, PersonAttrTerminType.PREFIX, pat.canonic_text, tok.morph, pat.gender)
                    if (pat.typ == PersonAttrTerminType.BESTREGARDS): 
                        end = tok.end_token
                        if (end.next0 is not None and end.next0.is_char_of(",")): 
                            end = end.next0
                        return PersonAttrToken._new2069(tok.begin_token, end, PersonAttrTerminType.BESTREGARDS, MorphCollection._new2068(MorphCase.NOMINATIVE))
                    if (pat.typ == PersonAttrTerminType.POSITION or pat.typ == PersonAttrTerminType.PREFIX or pat.typ == PersonAttrTerminType.KING): 
                        res = PersonAttrToken.__create_attr_position(tok, loc_onto, attrs)
                        if (res is not None): 
                            if (pat.typ == PersonAttrTerminType.KING): 
                                res.typ = pat.typ
                            if (pat.gender != MorphGender.UNDEFINED and res.gender == MorphGender.UNDEFINED): 
                                res.gender = pat.gender
                            if (pat.can_has_person_after > 0): 
                                if (res.end_token.is_value(pat.canonic_text, None)): 
                                    res.can_has_person_after = pat.can_has_person_after
                                else: 
                                    for ii in range(len(pat.canonic_text) - 1, 0, -1):
                                        if (not pat.canonic_text[ii].isalpha()): 
                                            if (res.end_token.is_value(pat.canonic_text[ii + 1 : ], None)): 
                                                res.can_has_person_after = pat.can_has_person_after
                                            break
                            if (pat.can_be_same_surname): 
                                res.can_be_same_surname = True
                            if (pat.can_be_independant): 
                                res.can_be_independent_property = True
                            if (pat.is_doubt): 
                                res.is_doubt = True
                                if (res.prop_ref is not None and ((res.prop_ref.find_slot(PersonPropertyReferent.ATTR_REF, None, True) is not None))): 
                                    res.is_doubt = False
                            if ((t.end_char < res.begin_char) and res.prop_ref is not None): 
                                tt1 = res.begin_token.previous
                                if (tt1.is_hiphen): 
                                    res.prop_ref.name = "{0} {1}".format(res.prop_ref.name, MiscHelper.get_text_value(t, tt1.previous, GetTextAttr.NO).lower())
                                else: 
                                    res.prop_ref.name = "{0} {1}".format(MiscHelper.get_text_value(t, tt1, GetTextAttr.NO).lower(), res.prop_ref.name)
                                res.begin_token = t
                        if (res is not None): 
                            pit = PersonItemToken.try_attach(t, None, PersonItemToken.ParseAttr.IGNOREATTRS, None)
                            if (pit is not None and pit.typ == PersonItemToken.ItemType.INITIAL): 
                                ok = False
                                pit = PersonItemToken.try_attach(pit.end_token.next0, None, PersonItemToken.ParseAttr.IGNOREATTRS, None)
                                if (pit is not None and pit.typ == PersonItemToken.ItemType.INITIAL): 
                                    pit = PersonItemToken.try_attach(pit.end_token.next0, None, PersonItemToken.ParseAttr.IGNOREATTRS, None)
                                    if (pit is not None and pit.typ == PersonItemToken.ItemType.INITIAL): 
                                        ok = True
                                if (not ok): 
                                    if (PersonAttrToken.__try_attach(tok.end_token.next0, loc_onto, attrs) is not None): 
                                        ok = True
                                if (not ok): 
                                    return None
                            if (npt0 is not None): 
                                ttt1 = (npt0.adjectives[0].begin_token if len(npt0.adjectives) > 0 else npt0.begin_token)
                                if (ttt1.begin_char < res.begin_char): 
                                    res.begin_token = ttt1
                                res.anafor = npt0.anafor
                                empty_adj = None
                                for i in range(len(npt0.adjectives)):
                                    j = 0
                                    while j < len(PersonAttrToken.__m_empty_adjs): 
                                        if (npt0.adjectives[i].is_value(PersonAttrToken.__m_empty_adjs[j], None)): 
                                            break
                                        j += 1
                                    if (j < len(PersonAttrToken.__m_empty_adjs)): 
                                        empty_adj = PersonAttrToken.__m_empty_adjs[j].lower()
                                        del npt0.adjectives[i]
                                        break
                                na0 = npt0.get_normal_case_text(MorphClass(), True, MorphGender.UNDEFINED, False).lower()
                                na1 = res.prop_ref.name
                                i = 1
                                while i < (len(na0) - 1): 
                                    if (na1.startswith(na0[i : ])): 
                                        res.prop_ref.name = "{0} {1}".format(na0[0 : (i)].strip(), na1)
                                        break
                                    i += 1
                                if (empty_adj is not None): 
                                    res1 = PersonAttrToken._new2080(res.begin_token, res.end_token, npt0.morph, res)
                                    res1.prop_ref = PersonPropertyReferent()
                                    res1.prop_ref.name = empty_adj
                                    res1.prop_ref.higher = res.prop_ref
                                    res1.can_be_independent_property = res.can_be_independent_property
                                    res1.typ = res.typ
                                    if (res.begin_token != res.end_token): 
                                        res.begin_token = res.begin_token.next0
                                    res = res1
                            if (res is not None): 
                                res.morph.remove_not_in_dictionary_items()
                            return res
            if (step > 0 or t.chars.is_latin_letter): 
                break
            if (t.morph.class0.is_adjective or t.chars.is_latin_letter): 
                pass
            elif (t.next0 is not None and t.next0.is_hiphen): 
                pass
            else: 
                break
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
            if (npt is None or npt.end_token == t): 
                break
            if (npt.end_token.is_value("ВИЦЕ", "ВІЦЕ")): 
                break
            t = npt.end_token
            npt0 = npt
            step += 1
        if (isinstance(t, TextToken) and (((t.is_value("ВИЦЕ", "ВІЦЕ") or t.is_value("ЭКС", "ЕКС") or t.is_value("VICE", None)) or t.is_value("EX", None) or t.is_value("DEPUTY", None))) and t.next0 is not None): 
            te = t.next0
            if (te.is_hiphen): 
                te = te.next0
            ppp = PersonAttrToken.__try_attach(te, loc_onto, attrs)
            if (ppp is not None): 
                if (t.begin_char < ppp.begin_char): 
                    ppp.begin_token = t
                    if (ppp.prop_ref is not None and ppp.prop_ref.name is not None): 
                        ppp.prop_ref.name = "{0}-{1}".format((t if isinstance(t, TextToken) else None).term.lower(), ppp.prop_ref.name)
                return ppp
            if ((te is not None and te.previous.is_hiphen and not te.is_whitespace_after) and not te.is_whitespace_before): 
                if (BracketHelper.is_bracket(te, False)): 
                    br = BracketHelper.try_parse(te, BracketParseAttr.NO, 100)
                    if (br is not None and isinstance(te, TextToken)): 
                        ppp = PersonAttrToken._new2062(t, br.end_token, br.end_token.previous.morph)
                        ppp.prop_ref = PersonPropertyReferent()
                        ppp.prop_ref.name = "{0}-{1}".format((t if isinstance(t, TextToken) else None).term, MiscHelper.get_text_value(te.next0, br.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)).lower()
                        return ppp
        if (isinstance(t, TextToken) and t.chars.is_latin_letter): 
            if (t.is_value("STATE", None)): 
                tt1 = t.next0
                if (MiscHelper.is_eng_adj_suffix(tt1)): 
                    tt1 = tt1.next0.next0
                res1 = PersonAttrToken.__try_attach(tt1, loc_onto, attrs)
                if (res1 is not None and res1.prop_ref is not None): 
                    res1.begin_token = t
                    res1.prop_ref.name = "{0} {1}".format((t if isinstance(t, TextToken) else None).term.lower(), res1.prop_ref.name)
                    return res1
        return None
    
    __m_empty_adjs = None
    
    __m_std_forms = None
    
    @staticmethod
    def __get_std_forms(tail : str, w1 : str, w2 : str) -> typing.List['MorphWordForm']:
        from pullenti.morph.Morphology import Morphology
        from pullenti.morph.MorphLang import MorphLang
        res = list()
        li1 = None
        li2 = None
        inoutarg2084 = RefOutArgWrapper(None)
        inoutres2085 = Utils.tryGetValue(PersonAttrToken.__m_std_forms, w1, inoutarg2084)
        li1 = inoutarg2084.value
        if (not inoutres2085): 
            li1 = Morphology.get_all_wordforms(w1, MorphLang())
            PersonAttrToken.__m_std_forms[w1] = li1
        for v in li1: 
            if (LanguageHelper.ends_with(v.normal_case, tail)): 
                res.append(v)
        if (w2 is not None): 
            inoutarg2082 = RefOutArgWrapper(None)
            inoutres2083 = Utils.tryGetValue(PersonAttrToken.__m_std_forms, w2, inoutarg2082)
            li2 = inoutarg2082.value
            if (not inoutres2083): 
                li2 = Morphology.get_all_wordforms(w2, MorphLang())
                PersonAttrToken.__m_std_forms[w2] = li2
        if (li2 is not None): 
            for v in li2: 
                if (LanguageHelper.ends_with(v.normal_case, tail)): 
                    res.append(v)
        return (res if len(res) > 0 else None)
    
    @staticmethod
    def __create_attr_position(tok : 'TerminToken', loc_onto : 'IntOntologyCollection', attrs : 'PersonAttrAttachAttrs') -> 'PersonAttrToken':
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
        ty2 = (tok.termin if isinstance(tok.termin, PersonAttrTermin) else None).typ2
        if (ty2 == PersonAttrTerminType2.ABBR): 
            pr0 = PersonPropertyReferent()
            pr0.name = tok.termin.canonic_text
            return PersonAttrToken._new2086(tok.begin_token, tok.end_token, pr0, PersonAttrTerminType.POSITION)
        if (ty2 == PersonAttrTerminType2.IO or ty2 == PersonAttrTerminType2.IO2): 
            k = 0
            first_pass2854 = True
            while True:
                if first_pass2854: first_pass2854 = False
                else: k += 1
                if (k > 0): 
                    if (ty2 == PersonAttrTerminType2.IO): 
                        return None
                    if (((tok.morph.number & MorphNumber.PLURAL)) != MorphNumber.UNDEFINED): 
                        return None
                    break
                tt = tok.end_token.next0
                if (tt is not None and tt.morph.class0.is_preposition): 
                    tt = tt.next0
                res_pat = PersonAttrToken._new2063(tok.begin_token, tok.end_token, PersonAttrTerminType.POSITION)
                res_pat.prop_ref = PersonPropertyReferent()
                if (tt is not None and isinstance(tt.get_referent(), PersonPropertyReferent)): 
                    res_pat.end_token = tt
                    res_pat.prop_ref.higher = (tt.get_referent() if isinstance(tt.get_referent(), PersonPropertyReferent) else None)
                else: 
                    aa = attrs
                    if (ty2 == PersonAttrTerminType2.IO2): 
                        aa = Utils.valToEnum(aa | PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL, PersonAttrToken.PersonAttrAttachAttrs)
                    pat = PersonAttrToken.try_attach(tt, loc_onto, aa)
                    if (pat is None): 
                        if (not ((isinstance(tt, TextToken)))): 
                            continue
                        npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0)
                        if (npt is None or npt.end_token == tok.end_token.next0): 
                            continue
                        pat = PersonAttrToken.try_attach(npt.end_token, loc_onto, PersonAttrToken.PersonAttrAttachAttrs.NO)
                        if (pat is None or pat.begin_token != tt): 
                            continue
                    if (pat.typ != PersonAttrTerminType.POSITION): 
                        continue
                    res_pat.end_token = pat.end_token
                    res_pat.prop_ref.higher = pat.prop_ref
                    res_pat.higher_prop_ref = pat
                nam = tok.termin.canonic_text
                ts = res_pat.end_token.next0
                te = None
                first_pass2855 = True
                while True:
                    if first_pass2855: first_pass2855 = False
                    else: ts = ts.next0
                    if (not (ts is not None)): break
                    if (ts.morph.class0.is_preposition): 
                        if (ts.is_value("В", None) or ts.is_value("ПО", None)): 
                            if (isinstance(ts.next0, ReferentToken)): 
                                r = ts.next0.get_referent()
                                if (r.type_name == PersonAttrToken.__obj_name_geo or r.type_name == PersonAttrToken.__obj_name_org): 
                                    res_pat.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                                    res_pat.end_token = ts.next0
                                else: 
                                    te = ts.next0
                                ts = ts.next0
                                continue
                            rt11 = ts.kit.process_referent("NAMEDENTITY", ts.next0)
                            if (rt11 is not None): 
                                res_pat.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, rt11, False, 0)
                                res_pat.end_token = rt11.end_token
                                ts = rt11.end_token
                                continue
                        nnn = NounPhraseHelper.try_parse(ts.next0, NounPhraseParseAttr.NO, 0)
                        if (nnn is None): 
                            break
                        if (ts.is_value("ПО", None)): 
                            te = nnn.end_token
                            ts = te
                            continue
                        break
                    if (ts != res_pat.end_token.next0 and ts.chars.is_all_lower): 
                        nnn = NounPhraseHelper.try_parse(ts, NounPhraseParseAttr.NO, 0)
                        if (nnn is None): 
                            break
                        te = nnn.end_token
                        ts = te
                        continue
                    break
                if (te is not None): 
                    s = MiscHelper.get_text_value(res_pat.end_token.next0, te, GetTextAttr.NO)
                    if (not Utils.isNullOrEmpty(s)): 
                        nam = "{0} {1}".format(nam, s)
                        res_pat.end_token = te
                inoutarg2088 = RefOutArgWrapper(nam)
                res_pat.begin_token = PersonAttrToken.__analize_vise(res_pat.begin_token, inoutarg2088)
                nam = inoutarg2088.value
                res_pat.prop_ref.name = nam.lower()
                res_pat.morph = tok.morph
                return res_pat
        if (ty2 == PersonAttrTerminType2.ADJ): 
            pat = PersonAttrToken.__try_attach(tok.end_token.next0, loc_onto, attrs)
            if (pat is None or pat.typ != PersonAttrTerminType.POSITION): 
                return None
            if (tok.begin_char == tok.end_char and not tok.begin_token.morph.class0.is_undefined): 
                return None
            pat.begin_token = tok.begin_token
            pat.prop_ref.name = "{0} {1}".format(tok.termin.canonic_text.lower(), pat.prop_ref.name)
            pat.morph = tok.morph
            return pat
        if (ty2 == PersonAttrTerminType2.IGNOREDADJ): 
            pat = PersonAttrToken.__try_attach(tok.end_token.next0, loc_onto, attrs)
            if (pat is None or pat.typ != PersonAttrTerminType.POSITION): 
                return None
            pat.begin_token = tok.begin_token
            pat.morph = tok.morph
            return pat
        if (ty2 == PersonAttrTerminType2.GRADE): 
            gr = PersonAttrToken.__create_attr_grade(tok)
            if (gr is not None): 
                return gr
            if (tok.begin_token.is_value("КАНДИДАТ", None)): 
                tt = tok.end_token.next0
                if (tt is not None and tt.is_value("В", None)): 
                    tt = tt.next0
                elif ((tt is not None and tt.is_value("НА", None) and tt.next0 is not None) and ((tt.next0.is_value("ПОСТ", None) or tt.next0.is_value("ДОЛЖНОСТЬ", None)))): 
                    tt = tt.next0.next0
                else: 
                    tt = None
                if (tt is not None): 
                    pat2 = PersonAttrToken.__try_attach(tt, loc_onto, PersonAttrToken.PersonAttrAttachAttrs.NO)
                    if (pat2 is not None): 
                        res0 = PersonAttrToken._new2063(tok.begin_token, pat2.end_token, PersonAttrTerminType.POSITION)
                        res0.prop_ref = PersonPropertyReferent._new2064("кандидат")
                        res0.prop_ref.higher = pat2.prop_ref
                        res0.higher_prop_ref = pat2
                        res0.morph = tok.morph
                        return res0
            if (not tok.begin_token.is_value("ДОКТОР", None) and not tok.begin_token.is_value("КАНДИДАТ", None)): 
                return None
        name = tok.termin.canonic_text.lower()
        t0 = tok.begin_token
        t1 = tok.end_token
        inoutarg2100 = RefOutArgWrapper(name)
        t0 = PersonAttrToken.__analize_vise(t0, inoutarg2100)
        name = inoutarg2100.value
        pr = PersonPropertyReferent()
        if ((t1.next0 is not None and t1.next0.is_hiphen and not t1.is_whitespace_after) and not t1.next0.is_whitespace_after): 
            if (t1.next0.next0.chars == t1.chars or PersonAttrToken.__m_termins.try_parse(t1.next0.next0, TerminParseAttr.NO) is not None or ((t1.next0.next0.chars.is_all_lower and t1.next0.next0.chars.is_cyrillic_letter))): 
                npt = NounPhraseHelper.try_parse(t1, NounPhraseParseAttr.NO, 0)
                if (npt is not None and npt.end_token == t1.next0.next0): 
                    name = npt.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False).lower()
                    t1 = npt.end_token
        tname0 = t1.next0
        tname1 = None
        category = None
        npt0 = None
        t = t1.next0
        first_pass2856 = True
        while True:
            if first_pass2856: first_pass2856 = False
            else: t = t.next0
            if (not (t is not None)): break
            if (((attrs & PersonAttrToken.PersonAttrAttachAttrs.ONLYKEYWORD)) != PersonAttrToken.PersonAttrAttachAttrs.NO): 
                break
            if (MiscHelper.check_number_prefix(t) is not None): 
                break
            if (t.is_newline_before): 
                ok = False
                if (t.get_referent() is not None): 
                    if (t.get_referent().type_name == PersonAttrToken.__obj_name_org or isinstance(t.get_referent(), GeoReferent)): 
                        if (pr.find_slot(PersonPropertyReferent.ATTR_REF, None, True) is None): 
                            ok = True
                if (t.newlines_before_count > 1 and not t.chars.is_all_lower): 
                    if (not ok): 
                        break
                    if ((t.newlines_after_count < 3) and tok.begin_token.is_newline_before): 
                        pass
                    else: 
                        break
                if (tok.is_newline_before): 
                    if (PersonAttrToken.__m_termins.try_parse(t, TerminParseAttr.NO) is not None): 
                        break
                    else: 
                        ok = True
                if (not ok): 
                    npt00 = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSEPREPOSITION, 0)
                    if (npt00 is not None and npt00.end_token.next0 is not None and not PersonAttrToken.__is_person(t)): 
                        tt1 = npt00.end_token
                        zap = False
                        and0 = False
                        ttt = tt1.next0
                        while ttt is not None: 
                            if (not ttt.is_comma_and): 
                                break
                            npt00 = NounPhraseHelper.try_parse(ttt.next0, NounPhraseParseAttr.NO, 0)
                            if (npt00 is None): 
                                break
                            tt1 = npt00.end_token
                            if (ttt.is_char(',')): 
                                zap = True
                            else: 
                                and0 = True
                                break
                            ttt = npt00.end_token
                            ttt = ttt.next0
                        if (zap and not and0): 
                            pass
                        elif (tt1.next0 is None): 
                            pass
                        else: 
                            if (PersonAttrToken.__is_person(tt1.next0)): 
                                ok = True
                            elif (isinstance(tt1.next0.get_referent(), GeoReferent)): 
                                if (PersonAttrToken.__is_person(tt1.next0.next0)): 
                                    ok = True
                                else: 
                                    inoutarg2091 = RefOutArgWrapper(None)
                                    ttt = PersonAttrToken.__try_attach_category(tt1.next0.next0, inoutarg2091)
                                    ccc = inoutarg2091.value
                                    if (ttt is not None): 
                                        ok = True
                            if (ok): 
                                tname1 = tt1
                                t1 = tname1
                                t = t1
                                continue
                    break
            if (t.is_char('(')): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    t = br.end_token
                    ok = True
                    ttt = br.begin_token
                    while ttt != br.end_token: 
                        if (ttt.chars.is_letter): 
                            if (not ttt.chars.is_all_lower): 
                                ok = False
                                break
                        ttt = ttt.next0
                    if (not ok): 
                        break
                    continue
                else: 
                    break
            pat = None
            if (((attrs & PersonAttrToken.PersonAttrAttachAttrs.ONLYKEYWORD)) == PersonAttrToken.PersonAttrAttachAttrs.NO): 
                pat = PersonAttrToken.__try_attach(t, loc_onto, PersonAttrToken.PersonAttrAttachAttrs.ONLYKEYWORD)
            if (pat is not None): 
                if (pat.morph.number == MorphNumber.PLURAL and not pat.morph.case.is_nominative): 
                    pass
                elif ((isinstance(tok.termin, PersonAttrTermin) and (tok.termin if isinstance(tok.termin, PersonAttrTermin) else None).is_doubt and pat.prop_ref is not None) and len(pat.prop_ref.slots) == 1 and tok.chars.is_latin_letter == pat.chars.is_latin_letter): 
                    t = pat.end_token
                    tname1 = t
                    t1 = tname1
                    continue
                elif ((not tok.morph.case.is_genitive and isinstance(tok.termin, PersonAttrTermin) and (tok.termin if isinstance(tok.termin, PersonAttrTermin) else None).can_has_person_after == 1) and pat.morph.case.is_genitive): 
                    rr = None
                    if (not "IgnorePersons" in t.kit.misc_data): 
                        t.kit.misc_data["IgnorePersons"] = None
                        rr = t.kit.process_referent("PERSON", t)
                        if ("IgnorePersons" in t.kit.misc_data): 
                            del t.kit.misc_data["IgnorePersons"]
                    if (rr is not None and rr.morph.case.is_genitive): 
                        pr.add_ext_referent(rr)
                        pr.add_slot(PersonPropertyReferent.ATTR_REF, rr.referent, False, 0)
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
            if (te.next0 is not None and te.is_char_of(",в") and ((attrs & PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL)) == PersonAttrToken.PersonAttrAttachAttrs.NO): 
                te = te.next0
            elif (te.next0 is not None and te.morph.class0.is_preposition): 
                if (((attrs & PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL)) == PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL): 
                    break
                if (((te.is_value("ИЗ", None) or te.is_value("ПРИ", None) or te.is_value("ПО", None)) or te.is_value("НА", None) or te.is_value("ОТ", None)) or te.is_value("OF", None)): 
                    te = te.next0
            elif ((te.is_hiphen and te.next0 is not None and not te.is_whitespace_before) and not te.is_whitespace_after and te.previous.chars == te.next0.chars): 
                continue
            elif (te.is_value("REPRESENT", None) and isinstance(te.next0, ReferentToken)): 
                te = te.next0
            r = te.get_referent()
            if ((te.chars.is_latin_letter and te.length_char > 1 and not t0.chars.is_latin_letter) and not te.chars.is_all_lower): 
                if (r is None or r.type_name != PersonAttrToken.__obj_name_org): 
                    inoutarg2092 = RefOutArgWrapper(None)
                    tt = PersonAttrToken.__try_attach_category(t, inoutarg2092)
                    category = inoutarg2092.value
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
                        te = te.next0
                    continue
            if (r is not None): 
                if ((r.type_name == PersonAttrToken.__obj_name_geo and te.previous is not None and te.previous.is_value("ДЕЛО", "СПРАВІ")) and te.previous.previous is not None and te.previous.previous.is_value("ПО", None)): 
                    t = te
                    tname1 = t
                    t1 = tname1
                    continue
                if ((r.type_name == PersonAttrToken.__obj_name_geo or r.type_name == PersonAttrToken.__obj_name_addr or r.type_name == PersonAttrToken.__obj_name_org) or r.type_name == PersonAttrToken.__obj_name_transport): 
                    if (t0.previous is not None and t0.previous.is_value("ОТ", None) and t.is_newline_before): 
                        break
                    t1 = te
                    pr.add_slot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                    posol = ((r.type_name == PersonAttrToken.__obj_name_geo or r.type_name == PersonAttrToken.__obj_name_org)) and LanguageHelper.ends_with_ex(name, "посол", "представитель", None, None)
                    if (posol): 
                        t = t1
                        continue
                    if ((((r.type_name == PersonAttrToken.__obj_name_geo and t1.next0 is not None and t1.next0.morph.class0.is_preposition) and t1.next0.next0 is not None and not t1.next0.is_value("О", None)) and not t1.next0.is_value("ОБ", None) and ((attrs & PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL)) == PersonAttrToken.PersonAttrAttachAttrs.NO) and not (tok.termin if isinstance(tok.termin, PersonAttrTermin) else None).is_boss): 
                        r1 = t1.next0.next0.get_referent()
                        if ((r1) is not None): 
                            if (r1.type_name == PersonAttrToken.__obj_name_org): 
                                pr.add_slot(PersonPropertyReferent.ATTR_REF, r1, False, 0)
                                t1 = t1.next0.next0
                                t = t1
                    if (r.type_name == PersonAttrToken.__obj_name_org): 
                        t = te.next0
                        while t is not None: 
                            if (not t.is_comma_and or not ((isinstance(t.next0, ReferentToken)))): 
                                break
                            r = t.next0.get_referent()
                            if (r is None): 
                                break
                            if (r.type_name != PersonAttrToken.__obj_name_org): 
                                break
                            pr.add_slot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                            t = t.next0
                            t1 = t
                            if (t.previous.is_and): 
                                t = t.next0
                                break
                            t = t.next0
                        first_pass2857 = True
                        while True:
                            if first_pass2857: first_pass2857 = False
                            else: t = t.next0
                            if (not (t is not None)): break
                            if (t.is_newline_before): 
                                break
                            if (t.is_value("В", None) or t.is_value("ОТ", None) or t.is_and): 
                                continue
                            if (t.morph.language.is_ua): 
                                if (t.is_value("ВІД", None)): 
                                    continue
                            if ((isinstance(t, TextToken) and t.chars.is_letter and not t.chars.is_all_lower) and t.previous.is_value("ОТ", "ВІД")): 
                                tname0 = t.previous
                                t1 = t
                                tname1 = t1
                                continue
                            if (isinstance(t, TextToken) and BracketHelper.can_be_start_of_sequence(t, False, False) and t.previous.is_value("ОТ", "ВІД")): 
                                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                                if (br is not None and (br.length_char < 100)): 
                                    tname0 = t.previous
                                    t = br.end_token
                                    t1 = t
                                    tname1 = t1
                                    continue
                            r = t.get_referent()
                            if (r is None): 
                                break
                            if (r.type_name != PersonAttrToken.__obj_name_geo): 
                                if (r.type_name == PersonAttrToken.__obj_name_org and t.previous is not None and ((t.previous.is_value("ОТ", None) or t.previous.is_value("ВІД", None)))): 
                                    pass
                                else: 
                                    break
                            pr.add_slot(PersonPropertyReferent.ATTR_REF, r, False, 0)
                            t1 = t
                if ((t1.next0 is not None and (t1.whitespaces_after_count < 2) and t1.next0.chars.is_latin_letter) and not t1.next0.chars.is_all_lower and MiscHelper.check_number_prefix(t1.next0) is None): 
                    t = t1.next0
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
                        t = t.next0
                t = t1
                if (((tname0 == t and tname1 is None and t.next0 is not None) and ((attrs & PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL)) == PersonAttrToken.PersonAttrAttachAttrs.NO and name != "президент") and t.next0.is_value("ПО", None)): 
                    tname0 = t.next0
                    continue
                break
            if (category is None): 
                inoutarg2093 = RefOutArgWrapper(None)
                tt = PersonAttrToken.__try_attach_category(t, inoutarg2093)
                category = inoutarg2093.value
                if (tt is not None and name is not None): 
                    t1 = tt
                    t = t1
                    continue
            if (name == "премьер"): 
                break
            if (isinstance(t, TextToken)): 
                if (t.is_value("ИМЕНИ", "ІМЕНІ")): 
                    break
            if (not t.chars.is_all_lower): 
                pit = PersonItemToken.try_attach(t, loc_onto, Utils.valToEnum(PersonItemToken.ParseAttr.CANBELATIN | PersonItemToken.ParseAttr.IGNOREATTRS, PersonItemToken.ParseAttr), None)
                if (pit is not None): 
                    if (pit.referent is not None): 
                        break
                    if (pit.lastname is not None and ((pit.lastname.is_in_dictionary or pit.lastname.is_in_ontology))): 
                        break
                    if (pit.firstname is not None and pit.firstname.is_in_dictionary): 
                        break
                    pits = PersonItemToken.try_attach_list(t, loc_onto, Utils.valToEnum(PersonItemToken.ParseAttr.NO | PersonItemToken.ParseAttr.IGNOREATTRS, PersonItemToken.ParseAttr), 6)
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
                    pits = PersonItemToken.try_attach_list(t, None, PersonItemToken.ParseAttr.IGNOREATTRS, 10)
                    if (pits is not None and len(pits) > 1): 
                        nnn = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
                        iii = 1
                        if (nnn is not None and len(nnn.adjectives) > 0): 
                            iii += len(nnn.adjectives)
                        test_person = True
                        t.kit.misc_data["TestAttr"] = None
                        li = PersonIdentityToken.try_attach(pits, 0, MorphBaseInfo._new2094(MorphCase.ALL_CASES), None, False, False)
                        del t.kit.misc_data["TestAttr"]
                        if (len(li) > 0 and li[0].coef > 1): 
                            t.kit.misc_data["TestAttr"] = None
                            li1 = PersonIdentityToken.try_attach(pits, iii, MorphBaseInfo._new2094(MorphCase.ALL_CASES), None, False, False)
                            del t.kit.misc_data["TestAttr"]
                            if (len(li1) == 0): 
                                break
                            if (li1[0].coef <= li[0].coef): 
                                break
                        else: 
                            t.kit.misc_data["TestAttr"] = None
                            li1 = PersonIdentityToken.try_attach(pits, 1, MorphBaseInfo._new2094(MorphCase.ALL_CASES), None, False, False)
                            del t.kit.misc_data["TestAttr"]
                            if (len(li1) > 0 and li1[0].coef >= 1 and li1[0].begin_token == t): 
                                continue
            if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if ((br is not None and t.next0.get_referent() is not None and t.next0.get_referent().type_name == PersonAttrToken.__obj_name_org) and t.next0.next0 == br.end_token): 
                    pr.add_slot(PersonPropertyReferent.ATTR_REF, t.next0.get_referent(), False, 0)
                    t1 = br.end_token
                    break
                elif (br is not None and (br.length_char < 40)): 
                    tname1 = br.end_token
                    t1 = tname1
                    t = t1
                    continue
            if (isinstance(t, NumberToken) and t.previous.is_value("ГЛАВА", None)): 
                break
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
            test = False
            if (npt is not None): 
                if (PersonAttrToken.__exists_in_doctionary(npt.end_token) and ((npt.morph.case.is_genitive or npt.morph.case.is_instrumental))): 
                    test = True
                elif (npt.begin_token == npt.end_token and t.length_char > 1 and ((t.chars.is_all_upper or t.chars.is_last_lower))): 
                    test = True
            elif (t.chars.is_all_upper or t.chars.is_last_lower): 
                test = True
            if (test): 
                rto = t.kit.process_referent("ORGANIZATION", t)
                if (rto is not None): 
                    str0 = str(rto.referent).upper()
                    if (str0.startswith("ГОСУДАРСТВЕННАЯ ГРАЖДАНСКАЯ СЛУЖБА")): 
                        rto = None
                if (rto is not None and rto.end_char >= t.end_char and rto.begin_char == t.begin_char): 
                    pr.add_slot(PersonPropertyReferent.ATTR_REF, rto.referent, False, 0)
                    pr.add_ext_referent(rto)
                    t1 = rto.end_token
                    t = t1
                    if (((attrs & PersonAttrToken.PersonAttrAttachAttrs.AFTERZAMESTITEL)) != PersonAttrToken.PersonAttrAttachAttrs.NO): 
                        break
                    npt0 = npt
                    if (t.next0 is not None and t.next0.is_and): 
                        rto2 = t.kit.process_referent("ORGANIZATION", t.next0.next0)
                        if (rto2 is not None and rto2.begin_char == t.next0.next0.begin_char): 
                            pr.add_slot(PersonPropertyReferent.ATTR_REF, rto2.referent, False, 0)
                            pr.add_ext_referent(rto2)
                            t1 = rto2.end_token
                            t = t1
                    continue
                if (npt is not None): 
                    tname1 = npt.end_token
                    t1 = tname1
                    t = t1
                    npt0 = npt
                    continue
            if (t.morph.class0.is_preposition): 
                npt = NounPhraseHelper.try_parse(t.next0, NounPhraseParseAttr.NO, 0)
                if (npt is None and t.next0 is not None and t.next0.morph.class0.is_adverb): 
                    npt = NounPhraseHelper.try_parse(t.next0.next0, NounPhraseParseAttr.NO, 0)
                if (npt is not None and PersonAttrToken.__exists_in_doctionary(npt.end_token)): 
                    ok = False
                    if ((t.is_value("ПО", None) and npt.morph.case.is_dative and not npt.noun.is_value("ИМЯ", "ІМЯ")) and not npt.noun.is_value("ПРОЗВИЩЕ", "ПРІЗВИСЬКО") and not npt.noun.is_value("ПРОЗВАНИЕ", "ПРОЗВАННЯ")): 
                        ok = True
                        if (npt.noun.is_value("РАБОТА", "РОБОТА") or npt.noun.is_value("ПОДДЕРЖКА", "ПІДТРИМКА") or npt.noun.is_value("СОПРОВОЖДЕНИЕ", "СУПРОВІД")): 
                            npt2 = NounPhraseHelper.try_parse(npt.end_token.next0, NounPhraseParseAttr.PARSEPREPOSITION, 0)
                            if (npt2 is not None): 
                                npt = npt2
                    elif (npt.noun.is_value("ОТСТАВКА", None) or npt.noun.is_value("ВІДСТАВКА", None)): 
                        ok = True
                    elif (name == "кандидат" and t.is_value("В", None)): 
                        ok = True
                    if (ok): 
                        tname1 = npt.end_token
                        t1 = tname1
                        t = t1
                        npt0 = npt
                        continue
                if (t.is_value("OF", None)): 
                    continue
            elif (t.is_and and npt0 is not None): 
                npt = NounPhraseHelper.try_parse(t.next0, NounPhraseParseAttr.NO, 0)
                if (npt is not None and not (npt.morph.class0 & npt0.morph.class0).is_undefined): 
                    if (npt0.chars == npt.chars): 
                        tname1 = npt.end_token
                        t1 = tname1
                        t = t1
                        npt0 = None
                        continue
            elif (t.is_char(',') and not t.is_newline_after and npt0 is not None): 
                npt = NounPhraseHelper.try_parse(t.next0, NounPhraseParseAttr.NO, 0)
                if (npt is not None and not (npt.morph.class0 & npt0.morph.class0).is_undefined): 
                    if (npt0.chars == npt.chars and npt.end_token.next0 is not None and npt.end_token.next0.is_and): 
                        npt1 = NounPhraseHelper.try_parse(npt.end_token.next0.next0, NounPhraseParseAttr.NO, 0)
                        if (npt1 is not None and not (npt1.morph.class0 & npt.morph.class0 & npt0.morph.class0).is_undefined): 
                            if (npt0.chars == npt1.chars): 
                                tname1 = npt1.end_token
                                t1 = tname1
                                t = t1
                                npt0 = None
                                continue
            elif (t.morph.class0.is_adjective and BracketHelper.can_be_start_of_sequence(t.next0, True, False)): 
                br = BracketHelper.try_parse(t.next0, BracketParseAttr.NO, 100)
                if (br is not None and (br.length_char < 100)): 
                    tname1 = br.end_token
                    t1 = tname1
                    t = t1
                    npt0 = None
                    continue
            if (t.chars.is_latin_letter and t.previous.chars.is_cyrillic_letter): 
                while t is not None: 
                    if (not t.chars.is_latin_letter or t.is_newline_before): 
                        break
                    else: 
                        tname1 = t
                        t1 = tname1
                    t = t.next0
                break
            if (((t.chars.is_all_upper or ((not t.chars.is_all_lower and not t.chars.is_capital_upper)))) and t.length_char > 1 and not t0.chars.is_all_upper): 
                tname1 = t
                t1 = tname1
                continue
            if (t.chars.is_last_lower and t.length_char > 2 and not t0.chars.is_all_upper): 
                tname1 = t
                t1 = tname1
                continue
            if (((t.chars.is_letter and isinstance(t.next0, ReferentToken) and isinstance(t.next0.get_referent(), PersonReferent)) and not t.morph.class0.is_preposition and not t.morph.class0.is_conjunction) and not t.morph.class0.is_verb): 
                tname1 = t
                t1 = tname1
                break
            if (isinstance(t, NumberToken)): 
                if ((t if isinstance(t, NumberToken) else None).begin_token.is_value("МИЛЛИОНОВ", None) or (t if isinstance(t, NumberToken) else None).begin_token.is_value("МІЛЬЙОНІВ", None)): 
                    tname1 = t
                    t1 = tname1
                    break
            if (test_person): 
                if (t.next0 is None): 
                    break
                te = t.next0
                if (((te.is_char_of(",в") or te.is_value("ИЗ", None))) and te.next0 is not None): 
                    te = te.next0
                r = te.get_referent()
                if ((r) is not None): 
                    if (r.type_name == PersonAttrToken.__obj_name_geo or r.type_name == PersonAttrToken.__obj_name_org or r.type_name == PersonAttrToken.__obj_name_transport): 
                        tname1 = t
                        t1 = tname1
                        continue
                break
            if (t.morph.language.is_en): 
                break
            if (t.morph.class0.is_noun and t.get_morph_class_in_dictionary().is_undefined and (t.whitespaces_before_count < 2)): 
                tname1 = t
                t1 = tname1
                continue
            break
        if (tname1 is not None): 
            if (pr.find_slot(PersonPropertyReferent.ATTR_REF, None, True) is None and (((((tname1.is_value("КОМПАНИЯ", "КОМПАНІЯ") or tname1.is_value("ФИРМА", "ФІРМА") or tname1.is_value("ПРЕДПРИЯТИЕ", "ПІДПРИЄМСТВО")) or tname1.is_value("ПРЕЗИДИУМ", "ПРЕЗИДІЯ") or tname1.is_value("ЧАСТЬ", "ЧАСТИНА")) or tname1.is_value("ФЕДЕРАЦИЯ", "ФЕДЕРАЦІЯ") or tname1.is_value("ВЕДОМСТВО", "ВІДОМСТВО")) or tname1.is_value("БАНК", None) or tname1.is_value("КОРПОРАЦИЯ", "КОРПОРАЦІЯ")))): 
                if (tname1 == tname0 or ((tname0.is_value("ЭТОТ", "ЦЕЙ") and tname0.next0 == tname1))): 
                    org_ = None
                    cou = 0
                    tt0 = t0.previous
                    first_pass2858 = True
                    while True:
                        if first_pass2858: first_pass2858 = False
                        else: tt0 = tt0.previous
                        if (not (tt0 is not None)): break
                        if (tt0.is_newline_after): 
                            cou += 10
                        cou += 1
                        if ((cou) > 500): 
                            break
                        rs0 = tt0.get_referents()
                        if (rs0 is None): 
                            continue
                        has_org = False
                        for r0 in rs0: 
                            if (r0.type_name == PersonAttrToken.__obj_name_org): 
                                has_org = True
                                if (tname1.is_value("БАНК", None)): 
                                    if (r0.find_slot("TYPE", "банк", True) is None): 
                                        continue
                                if (tname1.is_value("ЧАСТЬ", "ЧАСТИНА")): 
                                    ok1 = False
                                    for s in r0.slots: 
                                        if (s.type_name == "TYPE"): 
                                            if ((s.value).endswith("часть") or (s.value).endswith("частина")): 
                                                ok1 = True
                                    if (not ok1): 
                                        continue
                                org_ = r0
                                break
                        if (org_ is not None or has_org): 
                            break
                    if (org_ is not None): 
                        pr.add_slot(PersonPropertyReferent.ATTR_REF, org_, False, 0)
                        tname1 = None
        if (tname1 is not None): 
            s = MiscHelper.get_text_value(tname0, tname1, GetTextAttr.NO)
            if (s is not None): 
                name = "{0} {1}".format(name, s.lower())
        if (category is not None): 
            name = "{0} {1}".format(name, category)
        else: 
            inoutarg2097 = RefOutArgWrapper(None)
            tt = PersonAttrToken.__try_attach_category(t1.next0, inoutarg2097)
            category = inoutarg2097.value
            if (tt is not None): 
                name = "{0} {1}".format(name, category)
                t1 = tt
        pr.name = name
        res = PersonAttrToken._new2098(t0, t1, PersonAttrTerminType.POSITION, pr, tok.morph)
        res.can_be_independent_property = (tok.termin if isinstance(tok.termin, PersonAttrTermin) else None).can_be_unique_identifier
        i = name.find("заместитель ")
        if (i < 0): 
            i = name.find("заступник ")
        if (i >= 0): 
            i += 11
            res1 = PersonAttrToken._new2069(t0, t1, PersonAttrTerminType.POSITION, tok.morph)
            res1.prop_ref = PersonPropertyReferent()
            res1.prop_ref.name = name[0 : (i)]
            res1.prop_ref.higher = res.prop_ref
            res1.higher_prop_ref = res
            res.prop_ref.name = name[i + 1 : ]
            return res1
        return res
    
    @staticmethod
    def __exists_in_doctionary(t : 'Token') -> bool:
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphWordForm import MorphWordForm
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None): 
            return False
        for wf in tt.morph.items: 
            if ((wf if isinstance(wf, MorphWordForm) else None).is_in_dictionary): 
                return True
        return False
    
    @staticmethod
    def __is_person(t : 'Token') -> bool:
        from pullenti.ner.person.PersonReferent import PersonReferent
        if (t is None): 
            return False
        if (isinstance(t, ReferentToken)): 
            return isinstance(t.get_referent(), PersonReferent)
        if (not t.chars.is_letter or t.chars.is_all_lower): 
            return False
        rt00 = t.kit.process_referent("PERSON", t)
        return rt00 is not None and isinstance(rt00.referent, PersonReferent)
    
    @staticmethod
    def __analize_vise(t0 : 'Token', name : str) -> 'Token':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        if (t0 is None): 
            return None
        if (t0.previous is not None and t0.previous.is_hiphen and isinstance(t0.previous.previous, TextToken)): 
            if (t0.previous.previous.is_value("ВИЦЕ", "ВІЦЕ")): 
                t0 = t0.previous.previous
                name.value = (((("віце-" if t0.kit.base_language.is_ua else "вице-"))) + name.value)
            if (t0.previous is not None and t0.previous.previous is not None): 
                if (t0.previous.previous.is_value("ЭКС", "ЕКС")): 
                    t0 = t0.previous.previous
                    name.value = (((("екс-" if t0.kit.base_language.is_ua else "экс-"))) + name.value)
                elif (t0.previous.previous.chars == t0.chars and not t0.is_whitespace_before and not t0.previous.is_whitespace_before): 
                    npt00 = NounPhraseHelper.try_parse(t0.previous.previous, NounPhraseParseAttr.NO, 0)
                    if (npt00 is not None): 
                        name.value = npt00.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False).lower()
                        t0 = t0.previous.previous
        return t0
    
    @staticmethod
    def __try_attach_category(t : 'Token', cat : str) -> 'Token':
        from pullenti.ner.NumberToken import NumberToken
        cat.value = None
        if (t is None or t.next0 is None): 
            return None
        tt = None
        num = -1
        if (isinstance(t, NumberToken)): 
            num = (t if isinstance(t, NumberToken) else None).value
            tt = t
        else: 
            npt = NumberHelper.try_parse_roman(t)
            if (npt is not None): 
                num = npt.value
                tt = npt.end_token
        if ((num < 0) and ((t.is_value("ВЫСШИЙ", None) or t.is_value("ВЫСШ", None) or t.is_value("ВИЩИЙ", None)))): 
            num = 0
            tt = t
            if (tt.next0 is not None and tt.next0.is_char('.')): 
                tt = tt.next0
        if (tt is None or tt.next0 is None or (num < 0)): 
            return None
        tt = tt.next0
        if (tt.is_value("КАТЕГОРИЯ", None) or tt.is_value("КАТЕГОРІЯ", None) or tt.is_value("КАТ", None)): 
            if (tt.next0 is not None and tt.next0.is_char('.')): 
                tt = tt.next0
            if (num == 0): 
                cat.value = ("вищої категорії" if tt.kit.base_language.is_ua else "высшей категории")
            else: 
                cat.value = ("{0} категорії".format(num) if tt.kit.base_language.is_ua else "{0} категории".format(num))
            return tt
        if (tt.is_value("РАЗРЯД", None) or tt.is_value("РОЗРЯД", None)): 
            if (num == 0): 
                cat.value = ("вищого розряду" if tt.kit.base_language.is_ua else "высшего разряда")
            else: 
                cat.value = ("{0} розряду".format(num) if tt.kit.base_language.is_ua else "{0} разряда".format(num))
            return tt
        if (tt.is_value("КЛАСС", None) or tt.is_value("КЛАС", None)): 
            if (num == 0): 
                cat.value = ("вищого класу" if tt.kit.base_language.is_ua else "высшего класса")
            else: 
                cat.value = ("{0} класу".format(num) if tt.kit.base_language.is_ua else "{0} класса".format(num))
            return tt
        if (tt.is_value("РАНГ", None)): 
            if (num == 0): 
                return None
            else: 
                cat.value = "{0} ранга".format(num)
            return tt
        if (tt.is_value("СОЗЫВ", None) or tt.is_value("СКЛИКАННЯ", None)): 
            if (num == 0): 
                return None
            else: 
                cat.value = ("{0} скликання".format(num) if tt.kit.base_language.is_ua else "{0} созыва".format(num))
            return tt
        return None
    
    __obj_name_geo = "GEO"
    
    __obj_name_addr = "ADDRESS"
    
    __obj_name_org = "ORGANIZATION"
    
    __obj_name_transport = "TRANSPORT"
    
    __obj_name_date = "DATE"
    
    __obj_name_date_range = "DATERANGE"
    
    @staticmethod
    def __create_attr_grade(tok : 'TerminToken') -> 'PersonAttrToken':
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        t1 = PersonAttrToken.__find_grade_last(tok.end_token.next0, tok.begin_token)
        if (t1 is None): 
            return None
        pr = PersonPropertyReferent()
        pr.name = "{0} наук".format(tok.termin.canonic_text.lower())
        return PersonAttrToken._new2101(tok.begin_token, t1, PersonAttrTerminType.POSITION, pr, tok.morph, False)
    
    @staticmethod
    def __find_grade_last(t : 'Token', t0 : 'Token') -> 'Token':
        i = 0
        t1 = None
        while t is not None: 
            if (t.is_value("НАУК", None)): 
                t1 = t
                i += 1
                break
            if (t.is_value("Н", None)): 
                if (t0.length_char > 1 or t0.chars != t.chars): 
                    return None
                if ((t.next0 is not None and t.next0.is_hiphen and t.next0.next0 is not None) and t.next0.next0.is_value("К", None)): 
                    t1 = t.next0.next0
                    break
                if (t.next0 is not None and t.next0.is_char('.')): 
                    t1 = t.next0
                    break
            if (not t.chars.is_all_lower and t0.chars.is_all_lower): 
                break
            i += 1
            if ((i) > 2): 
                break
            if (t.next0 is not None and t.next0.is_char('.')): 
                t = t.next0
            if (t.next0 is not None and t.next0.is_hiphen): 
                t = t.next0
            t = t.next0
        if (t1 is None or i == 0): 
            return None
        return t1
    
    @staticmethod
    def check_kind(pr : 'PersonPropertyReferent') -> 'PersonPropertyKind':
        from pullenti.ner.Referent import Referent
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.ner.person.internal.PersonAttrTermin import PersonAttrTermin
        if (pr is None): 
            return PersonPropertyKind.UNDEFINED
        n = pr.get_string_value(PersonPropertyReferent.ATTR_NAME)
        if (n is None): 
            return PersonPropertyKind.UNDEFINED
        n = n.upper()
        for nn in Utils.splitString(n, ' ' + '-', False): 
            li = PersonAttrToken.__m_termins.try_attach_str(nn, MorphLang.RU)
            if (li is None or len(li) == 0): 
                li = PersonAttrToken.__m_termins.try_attach_str(n, MorphLang.UA)
            if (li is not None and len(li) > 0): 
                pat = (li[0] if isinstance(li[0], PersonAttrTermin) else None)
                if (pat.is_boss): 
                    return PersonPropertyKind.BOSS
                if (pat.is_kin): 
                    return PersonPropertyKind.KIN
                if (pat.typ == PersonAttrTerminType.KING): 
                    if (n != "ДОН"): 
                        return PersonPropertyKind.KING
                if (pat.is_military_rank): 
                    if (nn == "КАПИТАН" or nn == "CAPTAIN" or nn == "КАПІТАН"): 
                        org_ = (pr.get_value(PersonPropertyReferent.ATTR_REF) if isinstance(pr.get_value(PersonPropertyReferent.ATTR_REF), Referent) else None)
                        if (org_ is not None and org_.type_name == "ORGANIZATION"): 
                            continue
                    return PersonPropertyKind.MILITARYRANK
                if (pat.is_nation): 
                    return PersonPropertyKind.NATIONALITY
        return PersonPropertyKind.UNDEFINED
    
    @staticmethod
    def try_attach_word(t : 'Token') -> 'TerminToken':
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.MorphCollection import MorphCollection
        from pullenti.ner.person.internal.PersonAttrTermin import PersonAttrTermin
        tok = PersonAttrToken.__m_termins.try_parse(t, TerminParseAttr.NO)
        if ((tok is not None and tok.begin_token == tok.end_token and t.length_char == 1) and t.is_value("Д", None)): 
            if (BracketHelper.is_bracket(t.next0, True) and not t.is_whitespace_after): 
                return None
        if (tok is not None and tok.termin.canonic_text == "ГРАФ"): 
            tok.morph = MorphCollection(t.morph)
            tok.morph.remove_items(MorphGender.MASCULINE, False)
        if (tok is not None): 
            pat = (tok.termin if isinstance(tok.termin, PersonAttrTermin) else None)
            if (pat.typ2 != PersonAttrTerminType2.UNDEFINED and pat.typ2 != PersonAttrTerminType2.GRADE): 
                return None
        return tok
    
    @staticmethod
    def try_attach_position_word(t : 'Token') -> 'TerminToken':
        from pullenti.ner.person.internal.PersonAttrTermin import PersonAttrTermin
        tok = PersonAttrToken.__m_termins.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        pat = (tok.termin if isinstance(tok.termin, PersonAttrTermin) else None)
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
        if (PersonAttrToken.__m_termins is not None): 
            return
        PersonAttrToken.__m_termins = TerminCollection()
        PersonAttrToken.__m_termins.add(PersonAttrTermin._new2102("ТОВАРИЩ", PersonAttrTerminType.PREFIX))
        PersonAttrToken.__m_termins.add(PersonAttrTermin._new2073("ТОВАРИШ", MorphLang.UA, PersonAttrTerminType.PREFIX))
        for s in ["ГОСПОДИН", "ГРАЖДАНИН", "УРОЖЕНЕЦ", "МИСТЕР", "СЭР", "СЕНЬОР", "МОНСЕНЬОР", "СИНЬОР", "МЕСЬЕ", "МСЬЕ", "ДОН", "МАЭСТРО", "МЭТР"]: 
            t = PersonAttrTermin._new2104(s, PersonAttrTerminType.PREFIX, MorphGender.MASCULINE)
            if (s == "ГРАЖДАНИН"): 
                t.add_abridge("ГР.")
                t.add_abridge("ГРАЖД.")
                t.add_abridge("ГР-Н")
            PersonAttrToken.__m_termins.add(t)
        for s in ["ПАН", "ГРОМАДЯНИН", "УРОДЖЕНЕЦЬ", "МІСТЕР", "СЕР", "СЕНЬЙОР", "МОНСЕНЬЙОР", "МЕСЬЄ", "МЕТР", "МАЕСТРО"]: 
            t = PersonAttrTermin._new2105(s, MorphLang.UA, PersonAttrTerminType.PREFIX, MorphGender.MASCULINE)
            if (s == "ГРОМАДЯНИН"): 
                t.add_abridge("ГР.")
                t.add_abridge("ГР-Н")
            PersonAttrToken.__m_termins.add(t)
        for s in ["ГОСПОЖА", "ПАНИ", "ГРАЖДАНКА", "УРОЖЕНКА", "СЕНЬОРА", "СЕНЬОРИТА", "СИНЬОРА", "СИНЬОРИТА", "МИСС", "МИССИС", "МАДАМ", "МАДЕМУАЗЕЛЬ", "ФРАУ", "ФРОЙЛЯЙН", "ЛЕДИ", "ДОННА"]: 
            t = PersonAttrTermin._new2104(s, PersonAttrTerminType.PREFIX, MorphGender.FEMINIE)
            if (s == "ГРАЖДАНКА"): 
                t.add_abridge("ГР.")
                t.add_abridge("ГРАЖД.")
                t.add_abridge("ГР-КА")
            PersonAttrToken.__m_termins.add(t)
        for s in ["ПАНІ", "ГРОМАДЯНКА", "УРОДЖЕНКА", "СЕНЬЙОРА", "СЕНЬЙОРА", "МІС", "МІСІС", "МАДАМ", "МАДЕМУАЗЕЛЬ", "ФРАУ", "ФРОЙЛЯЙН", "ЛЕДІ"]: 
            t = PersonAttrTermin._new2105(s, MorphLang.UA, PersonAttrTerminType.PREFIX, MorphGender.FEMINIE)
            if (s == "ГРОМАДЯНКА"): 
                t.add_abridge("ГР.")
                t.add_abridge("ГР-КА")
            PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2105("MISTER", MorphLang.EN, PersonAttrTerminType.PREFIX, MorphGender.MASCULINE)
        t.add_abridge("MR")
        t.add_abridge("MR.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2105("MISSIS", MorphLang.EN, PersonAttrTerminType.PREFIX, MorphGender.FEMINIE)
        t.add_abridge("MRS")
        t.add_abridge("MSR.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2105("MISS", MorphLang.EN, PersonAttrTerminType.PREFIX, MorphGender.FEMINIE)
        t.add_abridge("MS")
        t.add_abridge("MS.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2102("БЕЗРАБОТНЫЙ", PersonAttrTerminType.POSITION)
        t.add_variant("НЕ РАБОТАЮЩИЙ", False)
        t.add_variant("НЕ РАБОТАЕТ", False)
        t.add_variant("ВРЕМЕННО НЕ РАБОТАЮЩИЙ", False)
        t.add_variant("ВРЕМЕННО НЕ РАБОТАЕТ", False)
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2073("БЕЗРОБІТНИЙ", MorphLang.UA, PersonAttrTerminType.POSITION)
        t.add_variant("НЕ ПРАЦЮЮЧИЙ", False)
        t.add_variant("НЕ ПРАЦЮЄ", False)
        t.add_variant("ТИМЧАСОВО НЕ ПРАЦЮЮЧИЙ", False)
        t.add_variant("ТИМЧАСОВО НЕ ПРАЦЮЄ", False)
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2113("ЗАМЕСТИТЕЛЬ", "заместитель", PersonAttrTerminType2.IO2, PersonAttrTerminType.POSITION)
        t.add_variant("ЗАМЕСТИТЕЛЬНИЦА", False)
        t.add_abridge("ЗАМ.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2114("ЗАСТУПНИК", MorphLang.UA, "заступник", PersonAttrTerminType2.IO2, PersonAttrTerminType.POSITION)
        t.add_variant("ЗАСТУПНИЦЯ", False)
        t.add_abridge("ЗАМ.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2113("УПОЛНОМОЧЕННЫЙ", "уполномоченный", PersonAttrTerminType2.IO2, PersonAttrTerminType.POSITION)
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2114("УПОВНОВАЖЕНИЙ", MorphLang.UA, "уповноважений", PersonAttrTerminType2.IO2, PersonAttrTerminType.POSITION)
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2113("ЭКС-УПОЛНОМОЧЕННЫЙ", "экс-уполномоченный", PersonAttrTerminType2.IO2, PersonAttrTerminType.POSITION)
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2114("ЕКС-УПОВНОВАЖЕНИЙ", MorphLang.UA, "екс-уповноважений", PersonAttrTerminType2.IO2, PersonAttrTerminType.POSITION)
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2119("ИСПОЛНЯЮЩИЙ ОБЯЗАННОСТИ", PersonAttrTerminType2.IO, PersonAttrTerminType.POSITION)
        t.add_abridge("И.О.")
        t.acronym = "ИО"
        t.canonic_text = t.acronym
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2120("ВИКОНУЮЧИЙ ОБОВЯЗКИ", MorphLang.UA, PersonAttrTerminType2.IO, PersonAttrTerminType.POSITION)
        t.add_abridge("В.О.")
        t.acronym = "ВО"
        t.canonic_text = t.acronym
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2119("ВРЕМЕННО ИСПОЛНЯЮЩИЙ ОБЯЗАННОСТИ", PersonAttrTerminType2.IO, PersonAttrTerminType.POSITION)
        t.add_abridge("ВР.И.О.")
        t.acronym = "ВРИО"
        t.canonic_text = t.acronym
        PersonAttrToken.__m_termin_vrio = t
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2102("ЗАВЕДУЮЩИЙ", PersonAttrTerminType.POSITION)
        t.add_abridge("ЗАВЕД.")
        t.add_abridge("ЗАВ.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2073("ЗАВІДУВАЧ", MorphLang.UA, PersonAttrTerminType.POSITION)
        t.add_abridge("ЗАВІД.")
        t.add_abridge("ЗАВ.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2102("СОТРУДНИК", PersonAttrTerminType.POSITION)
        t.add_abridge("СОТРУДН.")
        t.add_abridge("СОТР.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2073("СПІВРОБІТНИК", MorphLang.UA, PersonAttrTerminType.POSITION)
        t.add_abridge("СПІВРОБ.")
        t.add_abridge("СПІВ.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2102("АКАДЕМИК", PersonAttrTerminType.POSITION)
        t.add_abridge("АКАД.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2073("АКАДЕМІК", MorphLang.UA, PersonAttrTerminType.POSITION)
        t.add_abridge("АКАД.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2102("ЧЛЕН-КОРРЕСПОНДЕНТ", PersonAttrTerminType.POSITION)
        t.add_abridge("ЧЛ.-КОРР.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2073("ЧЛЕН-КОРЕСПОНДЕНТ", MorphLang.UA, PersonAttrTerminType.POSITION)
        t.add_abridge("ЧЛ.-КОР.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2102("ДОЦЕНТ", PersonAttrTerminType.POSITION)
        t.add_abridge("ДОЦ.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2102("ПРОФЕССОР", PersonAttrTerminType.POSITION)
        t.add_abridge("ПРОФ.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2073("ПРОФЕСОР", MorphLang.UA, PersonAttrTerminType.POSITION)
        t.add_abridge("ПРОФ.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2073("PROFESSOR", MorphLang.EN, PersonAttrTerminType.POSITION)
        t.add_abridge("PROF.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2119("КАНДИДАТ", PersonAttrTerminType2.GRADE, PersonAttrTerminType.POSITION)
        t.add_abridge("КАНД.")
        t.add_abridge("КАН.")
        t.add_abridge("К-Т")
        t.add_abridge("К.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2119("ДОКТОР", PersonAttrTerminType2.GRADE, PersonAttrTerminType.POSITION)
        t.add_abridge("ДОКТ.")
        t.add_abridge("ДОК.")
        t.add_abridge("Д-Р")
        t.add_abridge("Д.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2073("DOCTOR", MorphLang.EN, PersonAttrTerminType.PREFIX)
        t.add_abridge("DR")
        t.add_abridge("DR.")
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2102("ДОКТОРАНТ", PersonAttrTerminType.POSITION)
        PersonAttrToken.__m_termins.add(t)
        t = PersonAttrTermin._new2073("ДОКТОРАНТ", MorphLang.UA, PersonAttrTerminType.POSITION)
        PersonAttrToken.__m_termins.add(t)
        for s in ["КФН", "КТН", "КХН"]: 
            t = PersonAttrTermin._new2139(s, "кандидат наук", PersonAttrTerminType.POSITION, PersonAttrTerminType2.ABBR)
            PersonAttrToken.__m_termins.add(t)
        for s in ["ГЛАВНЫЙ", "МЛАДШИЙ", "СТАРШИЙ", "ВЕДУЩИЙ", "НАУЧНЫЙ"]: 
            t = PersonAttrTermin._new2119(s, PersonAttrTerminType2.ADJ, PersonAttrTerminType.POSITION)
            t.add_all_abridges(0, 0, 2)
            PersonAttrToken.__m_termins.add(t)
        for s in ["ГОЛОВНИЙ", "МОЛОДШИЙ", "СТАРШИЙ", "ПРОВІДНИЙ", "НАУКОВИЙ"]: 
            t = PersonAttrTermin._new2141(s, PersonAttrTerminType2.ADJ, PersonAttrTerminType.POSITION, MorphLang.UA)
            t.add_all_abridges(0, 0, 2)
            PersonAttrToken.__m_termins.add(t)
        for s in ["НЫНЕШНИЙ", "НОВЫЙ", "CURRENT", "NEW"]: 
            t = PersonAttrTermin._new2119(s, PersonAttrTerminType2.IGNOREDADJ, PersonAttrTerminType.POSITION)
            PersonAttrToken.__m_termins.add(t)
        for s in ["НИНІШНІЙ", "НОВИЙ"]: 
            t = PersonAttrTermin._new2141(s, PersonAttrTerminType2.IGNOREDADJ, PersonAttrTerminType.POSITION, MorphLang.UA)
            PersonAttrToken.__m_termins.add(t)
        for s in ["ТОГДАШНИЙ", "БЫВШИЙ", "ПРЕДЫДУЩИЙ", "FORMER", "PREVIOUS", "THEN"]: 
            t = PersonAttrTermin._new2119(s, PersonAttrTerminType2.IO, PersonAttrTerminType.POSITION)
            PersonAttrToken.__m_termins.add(t)
        for s in ["ТОДІШНІЙ", "КОЛИШНІЙ"]: 
            t = PersonAttrTermin._new2141(s, PersonAttrTerminType2.IO, PersonAttrTerminType.POSITION, MorphLang.UA)
            PersonAttrToken.__m_termins.add(t)
        dat = ResourceHelper.get_bytes("attr_ru.dat")
        if (dat is None): 
            raise Utils.newException("Not found resource file attr_ru.dat in Person analyzer", None)
        PersonAttrToken.__load_attrs(PersonAttrToken.__m_termins, dat, MorphLang.RU)
        dat = ResourceHelper.get_bytes("attr_en.dat")
        if ((dat) is None): 
            raise Utils.newException("Not found resource file attr_en.dat in Person analyzer", None)
        PersonAttrToken.__load_attrs(PersonAttrToken.__m_termins, dat, MorphLang.EN)
        PersonAttrToken.__load_attrs(PersonAttrToken.__m_termins, ResourceHelper.get_bytes("attr_ua.dat"), MorphLang.UA)
    
    __m_termins = None
    
    __m_termin_vrio = None
    
    @staticmethod
    def __deflate(zip0 : bytearray) -> bytearray:
        with io.BytesIO() as unzip: 
            data_ = io.BytesIO(zip0)
            data_.seek(0, io.SEEK_SET)
            MorphSerializeHelper.deflate_gzip(data_, unzip)
            data_.close()
            return unzip.getvalue()
    
    @staticmethod
    def __load_attrs(termins : 'TerminCollection', dat : bytearray, lang : 'MorphLang') -> None:
        from pullenti.ner.person.internal.PersonAttrTermin import PersonAttrTermin
        if (dat is None or len(dat) == 0): 
            return
        with io.BytesIO(PersonAttrToken.__deflate(dat)) as tmp: 
            tmp.seek(0, io.SEEK_SET)
            xml0 = None # new XmlDocument
            xml0 = xml.etree.ElementTree.parse(tmp)
            for x in xml0.getroot(): 
                a = Utils.getXmlAttrByName(x.attrib, "v")
                if (a is None): 
                    continue
                val = a[1]
                if (val is None): 
                    continue
                attrs = ("" if Utils.getXmlAttrByName(x.attrib, "a") is None else (Utils.ifNotNull(Utils.getXmlAttrByName(x.attrib, "a")[1], "")))
                if (val == "ОТЕЦ"): 
                    pass
                pat = PersonAttrTermin._new2146(val, PersonAttrTerminType.POSITION, lang)
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
                    pat.add_variant(val, False)
                    if (val.find('.') > 0): 
                        pat.add_abridge(val)
                if (len(x) > 0): 
                    for xx in x: 
                        if (xx.tag == "alt"): 
                            val = Utils.getXmlInnerText(xx)
                            pat.add_variant(val, False)
                            if (val.find('.') > 0): 
                                pat.add_abridge(val)
                termins.add(pat)

    
    @staticmethod
    def _new2062(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.morph = _arg3
        return res
    
    @staticmethod
    def _new2063(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2067(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType', _arg4 : str, _arg5 : 'MorphCollection') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.age = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new2069(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType', _arg4 : 'MorphCollection') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new2071(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType', _arg4 : str) -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new2077(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType', _arg4 : str, _arg5 : 'MorphCollection', _arg6 : 'MorphGender') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.morph = _arg5
        res.gender = _arg6
        return res
    
    @staticmethod
    def _new2080(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : 'PersonAttrToken') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.morph = _arg3
        res.higher_prop_ref = _arg4
        return res
    
    @staticmethod
    def _new2086(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonPropertyReferent', _arg4 : 'PersonAttrTerminType') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.prop_ref = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new2098(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType', _arg4 : 'PersonPropertyReferent', _arg5 : 'MorphCollection') -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.prop_ref = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new2101(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonAttrTerminType', _arg4 : 'PersonPropertyReferent', _arg5 : 'MorphCollection', _arg6 : bool) -> 'PersonAttrToken':
        res = PersonAttrToken(_arg1, _arg2)
        res.typ = _arg3
        res.prop_ref = _arg4
        res.morph = _arg5
        res.can_be_independent_property = _arg6
        return res
    
    # static constructor for class PersonAttrToken
    @staticmethod
    def _static_ctor():
        PersonAttrToken.__m_empty_adjs = ["УСПЕШНЫЙ", "ИЗВЕСТНЫЙ", "ЗНАМЕНИТЫЙ", "ИЗВЕСТНЕЙШИЙ", "ПОПУЛЯРНЫЙ", "ГЕНИАЛЬНЫЙ", "ТАЛАНТЛИВЫЙ", "МОЛОДОЙ", "УСПІШНИЙ", "ВІДОМИЙ", "ЗНАМЕНИТИЙ", "ВІДОМИЙ", "ПОПУЛЯРНИЙ", "ГЕНІАЛЬНИЙ", "ТАЛАНОВИТИЙ", "МОЛОДИЙ"]
        PersonAttrToken.__m_std_forms = dict()

PersonAttrToken._static_ctor()