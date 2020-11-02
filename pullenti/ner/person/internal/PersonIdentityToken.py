# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.Token import Token
from pullenti.ner.TextToken import TextToken
from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
from pullenti.ner.person.internal.FioTemplateType import FioTemplateType
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.NumberToken import NumberToken
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
from pullenti.ner.person.internal.PersonMorphCollection import PersonMorphCollection

class PersonIdentityToken(MetaToken):
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.coef = 0
        self.firstname = None;
        self.lastname = None;
        self.middlename = None;
        self.ontology_person = None;
        self.typ = FioTemplateType.UNDEFINED
    
    @property
    def probable_gender(self) -> 'MorphGender':
        if (self.morph.gender == MorphGender.FEMINIE or self.morph.gender == MorphGender.MASCULINE): 
            return self.morph.gender
        fem = 0
        mus = 0
        for i in range(2):
            col = (self.firstname if i == 0 else self.lastname)
            if (col is None): 
                continue
            isf = False
            ism = False
            for v in col.items: 
                if (((v.gender) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                    ism = True
                if (((v.gender) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                    isf = True
            if (ism): 
                mus += 1
            if (isf): 
                fem += 1
        if (mus > fem): 
            return MorphGender.MASCULINE
        if (fem > mus): 
            return MorphGender.FEMINIE
        return MorphGender.UNDEFINED
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0} {1}: {2}".format(self.coef, Utils.enumToString(self.typ), ("" if self.lastname is None else str(self.lastname))), end="", file=res, flush=True)
        print(" {0} {1}; {2}".format(("" if self.firstname is None else str(self.firstname)), ("" if self.middlename is None else str(self.middlename)), str(self.morph)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def create_lastname(pit : 'PersonItemToken', inf : 'MorphBaseInfo') -> 'PersonMorphCollection':
        res = PersonMorphCollection()
        if (pit.lastname is None): 
            PersonIdentityToken.__set_value(res, pit.begin_token, inf)
        else: 
            PersonIdentityToken.__set_value2(res, pit.lastname, inf)
        return res
    
    @staticmethod
    def try_attach_latin_surname(pit : 'PersonItemToken', ontos : 'IntOntologyCollection') -> 'PersonReferent':
        if (pit is None): 
            return None
        if (pit.lastname is not None and ((pit.lastname.is_in_dictionary or pit.lastname.is_lastname_has_std_tail))): 
            p = PersonReferent()
            p.add_slot(PersonReferent.ATTR_LASTNAME, pit.lastname.vars0_[0].value, False, 0)
            return p
        return None
    
    @staticmethod
    def try_attach_onto_for_single(pit : 'PersonItemToken', ontos : 'IntOntologyCollection') -> 'PersonReferent':
        if ((pit is None or ontos is None or pit.value is None) or pit.typ == PersonItemToken.ItemType.INITIAL): 
            return None
        if (len(ontos.items) > 30): 
            return None
        p0 = None
        cou = 0
        fi = False
        sur = True
        for p in ontos.items: 
            if (isinstance(p.referent, PersonReferent)): 
                p00 = None
                if (pit.firstname is not None): 
                    for v in pit.firstname.vars0_: 
                        if (p.referent.find_slot(PersonReferent.ATTR_FIRSTNAME, v.value, True) is not None): 
                            p00 = (Utils.asObjectOrNull(p.referent, PersonReferent))
                            fi = True
                            break
                if (pit.lastname is not None): 
                    for v in pit.lastname.vars0_: 
                        if (p.referent.find_slot(PersonReferent.ATTR_LASTNAME, v.value, True) is not None): 
                            p00 = (Utils.asObjectOrNull(p.referent, PersonReferent))
                            sur = True
                            break
                if (p00 is None): 
                    if (p.referent.find_slot(PersonReferent.ATTR_FIRSTNAME, pit.value, True) is not None): 
                        p00 = (Utils.asObjectOrNull(p.referent, PersonReferent))
                        fi = True
                    elif (p.referent.find_slot(PersonReferent.ATTR_LASTNAME, pit.value, True) is not None): 
                        p00 = (Utils.asObjectOrNull(p.referent, PersonReferent))
                        sur = True
                if (p00 is not None): 
                    p0 = p00
                    cou += 1
        if (p0 is not None and cou == 1): 
            if (fi): 
                li = list()
                li.append(pit)
                king = PersonIdentityToken.__try_attach_king(li, 0, pit.morph, False)
                if (king is not None): 
                    return None
            return p0
        return None
    
    @staticmethod
    def try_attach_onto_for_duble(pit0 : 'PersonItemToken', pit1 : 'PersonItemToken', ontos : 'IntOntologyCollection') -> 'PersonReferent':
        if ((pit0 is None or pit0.firstname is None or pit1 is None) or pit1.middlename is None or ontos is None): 
            return None
        if (len(ontos.items) > 100): 
            return None
        p0 = None
        cou = 0
        for p in ontos.items: 
            if (p.referent is not None): 
                for v in pit0.firstname.vars0_: 
                    if (p.referent.find_slot(PersonReferent.ATTR_FIRSTNAME, v.value, True) is None): 
                        continue
                    if (p.referent.find_slot(PersonReferent.ATTR_MIDDLENAME, pit1.middlename.vars0_[0].value, True) is None): 
                        continue
                    p0 = (Utils.asObjectOrNull(p.referent, PersonReferent))
                    cou += 1
                    break
        if (p0 is not None and cou == 1): 
            return p0
        return None
    
    @staticmethod
    def try_attach_onto_ext(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo', ontos : 'ExtOntology') -> 'PersonIdentityToken':
        if (ind >= len(pits) or pits[ind].typ == PersonItemToken.ItemType.INITIAL or ontos is None): 
            return None
        if (len(ontos.items) > 1000): 
            return None
        otl = ontos.attach_token(PersonReferent.OBJ_TYPENAME, pits[ind].begin_token)
        return PersonIdentityToken.__try_attach_onto(pits, ind, inf, otl, False, False)
    
    @staticmethod
    def try_attach_onto_int(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo', ontos : 'IntOntologyCollection') -> 'PersonIdentityToken':
        if (ind >= len(pits) or pits[ind].typ == PersonItemToken.ItemType.INITIAL): 
            return None
        if (len(ontos.items) > 1000): 
            return None
        otl = ontos.try_attach(pits[ind].begin_token, None, False)
        res = PersonIdentityToken.__try_attach_onto(pits, ind, inf, otl, False, False)
        if (res is not None): 
            return res
        return None
    
    @staticmethod
    def __try_attach_onto(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo', otl : typing.List['IntOntologyToken'], is_local : bool, is_attr_before : bool) -> 'PersonIdentityToken':
        if (otl is None or len(otl) == 0): 
            return None
        res = list()
        onto_persons = list()
        if (otl is not None): 
            for ot in otl: 
                if (ot.end_token == pits[ind].end_token): 
                    pers = Utils.asObjectOrNull(ot.item.referent, PersonReferent)
                    if (pers is None): 
                        continue
                    if (pers in onto_persons): 
                        continue
                    if (ot.termin.ignore_terms_order): 
                        if (ind != 0): 
                            continue
                        pit = PersonIdentityToken.try_attach_identity(pits, inf)
                        if (pit is None): 
                            continue
                        p = PersonReferent()
                        p._add_identity(pit.lastname)
                        pit.ontology_person = p
                        onto_persons.append(pers)
                        res.append(pit)
                        continue
                    if (inf.gender == MorphGender.MASCULINE): 
                        if (pers.is_female): 
                            continue
                    elif (inf.gender == MorphGender.FEMINIE): 
                        if (pers.is_male): 
                            continue
                    inf0 = MorphBaseInfo._new2485(inf.case_, inf.gender)
                    if (not ot.morph.case_.is_undefined and inf0.case_ == MorphCase.ALL_CASES and ot.begin_token == ot.end_token): 
                        inf0.case_ = ot.morph.case_
                    if (pers.is_male): 
                        inf0.gender = MorphGender.MASCULINE
                    elif (pers.is_female): 
                        inf0.gender = MorphGender.FEMINIE
                    vars0_ = list()
                    if (ind > 1): 
                        pit = PersonIdentityToken.__try_attachiisurname(pits, ind - 2, inf0)
                        if ((pit) is not None): 
                            vars0_.append(pit)
                        pit = PersonIdentityToken.__try_attach_name_secname_surname(pits, ind - 2, inf0, False)
                        if ((pit) is not None): 
                            vars0_.append(pit)
                    if (ind > 0): 
                        pit = PersonIdentityToken.__try_attachiisurname(pits, ind - 1, inf0)
                        if ((pit) is not None): 
                            vars0_.append(pit)
                        pit = PersonIdentityToken.__try_attach_name_surname(pits, ind - 1, inf0, False, is_attr_before)
                        if ((pit) is not None): 
                            vars0_.append(pit)
                    if ((ind + 2) < len(pits)): 
                        pit = PersonIdentityToken.__try_attach_surnameii(pits, ind, inf0)
                        if ((pit) is not None): 
                            vars0_.append(pit)
                        pit = PersonIdentityToken.__try_attach_surname_name_secname(pits, ind, inf0, False, False)
                        if ((pit) is not None): 
                            vars0_.append(pit)
                    if ((ind + 1) < len(pits)): 
                        pit = PersonIdentityToken.__try_attach_surname_name(pits, ind, inf0, False)
                        if ((pit) is not None): 
                            pit0 = None
                            for v in vars0_: 
                                if (v.typ == FioTemplateType.SURNAMENAMESECNAME): 
                                    pit0 = v
                                    break
                            if (pit0 is None or (pit0.coef < pit.coef)): 
                                vars0_.append(pit)
                    pit = PersonIdentityToken.__try_attach_asian(pits, ind, inf0, 3, False)
                    if ((pit) is not None): 
                        vars0_.append(pit)
                    else: 
                        pit = PersonIdentityToken.__try_attach_asian(pits, ind, inf0, 2, False)
                        if ((pit) is not None): 
                            vars0_.append(pit)
                    pit = (None)
                    for v in vars0_: 
                        if (v.coef < 0): 
                            continue
                        p = PersonReferent()
                        if (v.ontology_person is not None): 
                            p = v.ontology_person
                        else: 
                            if (v.typ == FioTemplateType.ASIANNAME): 
                                pers._add_identity(v.lastname)
                            else: 
                                p._add_fio_identity(v.lastname, v.firstname, v.middlename)
                            v.ontology_person = p
                        if (not pers.can_be_equals(p, ReferentsEqualType.WITHINONETEXT)): 
                            if (pit is not None and v.coef >= pit.coef): 
                                pit = (None)
                        elif (pit is None): 
                            pit = v
                        elif (pit.coef < v.coef): 
                            pit = v
                    if (pit is None): 
                        pit = PersonIdentityToken.__try_attach_single_surname(pits, ind, inf0)
                        if (pit is None or (pit.coef < 2)): 
                            continue
                        p = PersonReferent()
                        p._add_fio_identity(pit.lastname, None, None)
                        pit.ontology_person = p
                    onto_persons.append(pers)
                    res.append(pit)
        if (len(res) == 0): 
            return None
        if (len(res) == 1): 
            res[0].ontology_person.merge_slots(onto_persons[0], True)
            return res[0]
        return None
    
    @staticmethod
    def create_typ(pits : typing.List['PersonItemToken'], typ_ : 'FioTemplateType', inf : 'MorphBaseInfo') -> 'PersonIdentityToken':
        if (typ_ == FioTemplateType.SURNAMENAMESECNAME): 
            return PersonIdentityToken.__try_attach_surname_name_secname(pits, 0, inf, False, True)
        return None
    
    @staticmethod
    def sort(li : typing.List['PersonIdentityToken']) -> None:
        if (li is not None and len(li) > 1): 
            k = 0
            while k < len(li): 
                ch = False
                i = 0
                while i < (len(li) - 1): 
                    if (li[i].coef < li[i + 1].coef): 
                        ch = True
                        v = li[i]
                        li[i] = li[i + 1]
                        li[i + 1] = v
                    i += 1
                if (not ch): 
                    break
                k += 1
    
    @staticmethod
    def try_attach_for_ext_onto(pits : typing.List['PersonItemToken']) -> typing.List['PersonIdentityToken']:
        pit = None
        if (len(pits) == 3): 
            if (pits[0].typ == PersonItemToken.ItemType.VALUE and pits[1].typ == PersonItemToken.ItemType.INITIAL and pits[2].typ == PersonItemToken.ItemType.VALUE): 
                pit = PersonIdentityToken._new2486(pits[0].begin_token, pits[2].end_token, FioTemplateType.NAMEISURNAME)
                PersonIdentityToken.manage_firstname(pit, pits[0], None)
                PersonIdentityToken.manage_lastname(pit, pits[2], None)
                PersonIdentityToken.__manage_middlename(pit, pits[1], None)
                pit.coef = (2)
            elif (pits[0].typ == PersonItemToken.ItemType.VALUE and pits[1].typ == PersonItemToken.ItemType.VALUE and pits[2].typ == PersonItemToken.ItemType.VALUE): 
                ok = False
                if (pits[0].firstname is None and pits[1].middlename is None and ((pits[1].firstname is not None or pits[2].middlename is not None))): 
                    ok = True
                elif (pits[0].firstname is not None and ((pits[0].firstname.is_lastname_has_std_tail or pits[0].firstname.is_in_dictionary))): 
                    ok = True
                if (ok): 
                    pit = PersonIdentityToken._new2486(pits[0].begin_token, pits[2].end_token, FioTemplateType.SURNAMENAMESECNAME)
                    PersonIdentityToken.manage_firstname(pit, pits[1], None)
                    PersonIdentityToken.manage_lastname(pit, pits[0], None)
                    PersonIdentityToken.__manage_middlename(pit, pits[2], None)
                    pit.coef = (2)
        elif (len(pits) == 2 and pits[0].typ == PersonItemToken.ItemType.VALUE and pits[1].typ == PersonItemToken.ItemType.VALUE): 
            nam = None
            sur = None
            for i in range(2):
                if (((pits[i].firstname is not None and pits[i].firstname.is_in_dictionary)) or ((pits[i ^ 1].lastname is not None and ((pits[i ^ 1].lastname.is_in_dictionary or pits[i ^ 1].lastname.is_lastname_has_std_tail))))): 
                    nam = pits[i]
                    sur = pits[i ^ 1]
                    break
            if (nam is not None): 
                pit = PersonIdentityToken._new2486(pits[0].begin_token, pits[1].end_token, (FioTemplateType.NAMESURNAME if nam == pits[0] else FioTemplateType.SURNAMENAME))
                PersonIdentityToken.manage_firstname(pit, nam, None)
                PersonIdentityToken.manage_lastname(pit, sur, None)
                pit.coef = (2)
        if (pit is None): 
            return None
        res = list()
        res.append(pit)
        return res
    
    @staticmethod
    def try_attach(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo', first_tok : 'Token', king : bool, is_attr_before : bool) -> typing.List['PersonIdentityToken']:
        res = list()
        ty = FioTemplateType.UNDEFINED
        if (first_tok is not None): 
            t = first_tok.previous
            while t is not None: 
                pf = Utils.asObjectOrNull(t.get_referent(), PersonReferent)
                if (pf is not None): 
                    ty = pf._m_person_identity_typ
                    break
                if (t.is_newline_before): 
                    break
                if (t.chars.is_letter and not t.is_and): 
                    break
                t = t.previous
        pit = PersonIdentityToken.__try_attach_global(pits, ind, inf)
        if ((pit) is not None): 
            res.append(pit)
            return res
        pit = PersonIdentityToken.__try_attach_surnameii(pits, ind, inf)
        if ((pit) is not None): 
            res.append(pit)
        pit = PersonIdentityToken.__try_attachiisurname(pits, ind, inf)
        if ((pit) is not None): 
            res.append(pit)
        pit = PersonIdentityToken.__try_attach_asian(pits, ind, inf, 3, ty == FioTemplateType.ASIANNAME)
        if ((pit) is not None): 
            res.append(pit)
        else: 
            pit = PersonIdentityToken.__try_attach_name_surname(pits, ind, inf, ty == FioTemplateType.NAMESURNAME, is_attr_before)
            if ((pit) is not None): 
                res.append(pit)
            pit1 = PersonIdentityToken.__try_attach_surname_name(pits, ind, inf, ty == FioTemplateType.SURNAMENAME)
            if ((pit1) is not None): 
                res.append(pit1)
                if (pit is not None and (pit.coef + (1)) >= pit1.coef and ty != FioTemplateType.SURNAMENAME): 
                    pit1.coef -= (0.5)
            pit = PersonIdentityToken.__try_attach_name_secname_surname(pits, ind, inf, ty == FioTemplateType.NAMESECNAMESURNAME)
            if ((pit) is not None): 
                res.append(pit)
            pit = PersonIdentityToken.__try_attach_surname_name_secname(pits, ind, inf, ty == FioTemplateType.SURNAMENAMESECNAME, False)
            if ((pit) is not None): 
                res.append(pit)
            pit = PersonIdentityToken.__try_attach_asian(pits, ind, inf, 2, ty == FioTemplateType.ASIANNAME)
            if ((pit) is not None): 
                res.append(pit)
        if (king): 
            pit = PersonIdentityToken.__try_attach_name_secname(pits, ind, inf, ty == FioTemplateType.NAMESECNAME)
            if ((pit) is not None): 
                res.append(pit)
                for r in res: 
                    if (r.typ == FioTemplateType.NAMESURNAME): 
                        r.coef = (pit.coef - (1))
        pit = PersonIdentityToken.__try_attach_king(pits, ind, inf, ty == FioTemplateType.KING or king)
        if ((pit) is not None): 
            res.append(pit)
        if (inf.gender == MorphGender.MASCULINE or inf.gender == MorphGender.FEMINIE): 
            for p in res: 
                if (p.morph.gender == MorphGender.UNDEFINED or (p.morph.gender) == ((MorphGender.FEMINIE) | (MorphGender.MASCULINE))): 
                    p.morph.gender = inf.gender
                    if (p.morph.case_.is_undefined): 
                        p.morph.case_ = inf.case_
        for r in res: 
            tt = r.begin_token
            while tt != r.end_token: 
                if (tt.is_newline_after): 
                    r.coef -= (1)
                tt = tt.next0_
            ttt = r.begin_token.previous
            if (ttt is not None and ttt.morph.class0_ == MorphClass.VERB): 
                tte = r.end_token.next0_
                if (tte is None or tte.is_char('.') or tte.is_newline_before): 
                    pass
                else: 
                    continue
                r.coef += (1)
            if (r.coef >= 0 and ind == 0 and r.end_token == pits[len(pits) - 1].end_token): 
                r.coef += PersonIdentityToken.__calc_coef_after(pits[len(pits) - 1].end_token.next0_)
        if (ty != FioTemplateType.UNDEFINED and ind == 0): 
            for r in res: 
                if (r.typ == ty): 
                    r.coef += (1.5)
                elif (((r.typ == FioTemplateType.SURNAMENAME and ty == FioTemplateType.SURNAMENAMESECNAME)) or ((r.typ == FioTemplateType.SURNAMENAMESECNAME and ty == FioTemplateType.SURNAMENAME))): 
                    r.coef += (0.5)
        PersonIdentityToken.sort(res)
        return res
    
    @staticmethod
    def manage_lastname(res : 'PersonIdentityToken', pit : 'PersonItemToken', inf : 'MorphBaseInfo') -> None:
        if (pit.lastname is None): 
            res.lastname = PersonMorphCollection()
            PersonIdentityToken.__set_value(res.lastname, pit.begin_token, inf)
            if (pit.is_in_dictionary): 
                res.coef -= 1
            tt = Utils.asObjectOrNull(pit.begin_token, TextToken)
            if ((tt is not None and not tt.chars.is_latin_letter and tt.chars.is_capital_upper) and tt.length_char > 2 and not tt.chars.is_latin_letter): 
                ok = True
                for wf in tt.morph.items: 
                    if (wf.is_in_dictionary): 
                        ok = False
                        break
                if (ok): 
                    res.coef += (1)
        else: 
            res.coef += 1
            if (not PersonIdentityToken.__is_accords(pit.lastname, inf)): 
                res.coef -= 1
            res.lastname = PersonMorphCollection()
            PersonIdentityToken.__set_value2(res.lastname, pit.lastname, inf)
            if (pit.lastname.term is not None): 
                if (res.morph.case_.is_undefined or res.morph.case_.is_nominative): 
                    if (not pit.lastname.is_in_dictionary and not pit.lastname.term in res.lastname.values): 
                        if (inf.case_.is_nominative or inf.case_.is_undefined): 
                            if (pit.lastname.morph.class0_.is_adjective and inf.gender == MorphGender.FEMINIE): 
                                pass
                            else: 
                                res.lastname.add(pit.lastname.term, None, pit.morph.gender, False)
            if (pit.is_in_dictionary): 
                res.coef -= 1
            if (pit.lastname.is_in_dictionary or pit.lastname.is_in_ontology): 
                res.coef += 1
            if (pit.lastname.is_lastname_has_hiphen): 
                res.coef += (1)
            if (pit.middlename is not None and pit.middlename.morph.gender == MorphGender.FEMINIE): 
                res.coef -= 1
        if (pit.firstname is not None and not pit.chars.is_latin_letter): 
            res.coef -= 1
        if (isinstance(pit.begin_token, ReferentToken)): 
            res.coef -= 1
    
    @staticmethod
    def manage_firstname(res : 'PersonIdentityToken', pit : 'PersonItemToken', inf : 'MorphBaseInfo') -> None:
        if (pit.firstname is None): 
            if (pit.lastname is not None): 
                res.coef -= 1
            res.firstname = PersonMorphCollection()
            PersonIdentityToken.__set_value(res.firstname, pit.begin_token, inf)
            if (pit.is_in_dictionary): 
                res.coef -= 1
        else: 
            res.coef += 1
            if (not PersonIdentityToken.__is_accords(pit.firstname, inf)): 
                res.coef -= 1
            res.firstname = PersonMorphCollection()
            PersonIdentityToken.__set_value2(res.firstname, pit.firstname, inf)
            if (pit.is_in_dictionary and not pit.firstname.is_in_dictionary): 
                res.coef -= 1
        if (pit.middlename is not None and pit.middlename != pit.firstname): 
            res.coef -= 1
        if (pit.lastname is not None and ((pit.lastname.is_in_dictionary or pit.lastname.is_in_ontology))): 
            res.coef -= 1
        if (isinstance(pit.begin_token, ReferentToken)): 
            res.coef -= (2)
    
    @staticmethod
    def __manage_middlename(res : 'PersonIdentityToken', pit : 'PersonItemToken', inf : 'MorphBaseInfo') -> None:
        mm = PersonMorphCollection()
        res.middlename = (mm)
        if (pit.middlename is None): 
            PersonIdentityToken.__set_value(mm, pit.begin_token, inf)
        else: 
            res.coef += 1
            if (not PersonIdentityToken.__is_accords(pit.middlename, inf)): 
                res.coef -= 1
            PersonIdentityToken.__set_value2(mm, pit.middlename, inf)
    
    @staticmethod
    def __try_attach_single_surname(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo') -> 'PersonIdentityToken':
        if (ind >= len(pits) or pits[ind].lastname is None): 
            return None
        res = PersonIdentityToken(pits[ind].begin_token, pits[ind].end_token)
        if (ind == 0 and len(pits) == 1): 
            res.coef += 1
        else: 
            if (ind > 0 and ((not pits[ind - 1].is_in_dictionary or pits[ind - 1].typ == PersonItemToken.ItemType.INITIAL or pits[ind - 1].firstname is not None))): 
                res.coef -= 1
            if (((ind + 1) < len(pits)) and ((not pits[ind + 1].is_in_dictionary or pits[ind + 1].typ == PersonItemToken.ItemType.INITIAL or pits[ind + 1].firstname is not None))): 
                res.coef -= 1
        res.morph = PersonIdentityToken.__accord_morph(inf, pits[ind].lastname, None, None, pits[ind].end_token.next0_)
        PersonIdentityToken.manage_lastname(res, pits[ind], inf)
        return res
    
    @staticmethod
    def __try_attach_name_surname(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo', prev_has_this_typ : bool=False, is_attr_before : bool=False) -> 'PersonIdentityToken':
        if ((ind + 1) >= len(pits) or pits[ind + 1].typ != PersonItemToken.ItemType.VALUE or pits[ind].typ != PersonItemToken.ItemType.VALUE): 
            return None
        if (pits[ind + 1].lastname is None): 
            if (not prev_has_this_typ): 
                if (pits[ind].chars.is_latin_letter): 
                    pass
                else: 
                    if (pits[ind].firstname is None or pits[ind + 1].middlename is not None): 
                        return None
                    if (pits[ind + 1].is_newline_after): 
                        pass
                    elif (pits[ind + 1].end_token.next0_ is not None and pits[ind + 1].end_token.next0_.is_char_of(",.)")): 
                        pass
                    else: 
                        return None
        if (pits[ind].is_newline_after or pits[ind].is_hiphen_after): 
            return None
        if (pits[ind + 1].middlename is not None and pits[ind + 1].middlename.is_in_dictionary and pits[ind + 1].middlename.morph.gender == MorphGender.FEMINIE): 
            return None
        if (PersonIdentityToken.__is_both_surnames(pits[ind], pits[ind + 1])): 
            if (len(pits) == 2 and ind == 0 and is_attr_before): 
                pass
            else: 
                return None
        res = PersonIdentityToken._new2486(pits[ind].begin_token, pits[ind + 1].end_token, FioTemplateType.NAMESURNAME)
        res.coef -= (ind)
        res.morph = PersonIdentityToken.__accord_morph(inf, pits[ind + 1].lastname, pits[ind].firstname, None, pits[ind + 1].end_token.next0_)
        if (res.morph.gender == MorphGender.MASCULINE or res.morph.gender == MorphGender.FEMINIE): 
            if (pits[ind + 1].lastname is not None and not pits[ind + 1].lastname.morph.case_.is_undefined): 
                if ((pits[ind].lastname is not None and pits[ind].lastname.is_lastname_has_std_tail and pits[ind + 1].firstname is not None) and pits[ind + 1].firstname.is_in_dictionary): 
                    res.coef -= (1)
                else: 
                    res.coef += (1)
            inf = (res.morph)
        PersonIdentityToken.manage_firstname(res, pits[ind], inf)
        PersonIdentityToken.manage_lastname(res, pits[ind + 1], inf)
        if (pits[ind].firstname is not None and (isinstance(pits[ind + 1].begin_token, ReferentToken))): 
            res.coef += 1
        if (pits[ind].begin_token.get_morph_class_in_dictionary().is_verb): 
            if (pits[ind].begin_token.chars.is_capital_upper and not MiscHelper.can_be_start_of_sentence(pits[ind].begin_token)): 
                pass
            else: 
                res.coef -= (1)
        if (pits[ind].firstname is not None and ((pits[ind + 1].is_newline_after or ((pits[ind + 1].end_token.next0_ is not None and ((pits[ind + 1].end_token.next0_.is_char_of(",."))))))) and not pits[ind + 1].is_newline_before): 
            if (pits[ind + 1].firstname is None and pits[ind + 1].middlename is None): 
                res.coef += 1
            elif (pits[ind + 1].chars.is_latin_letter and (ind + 2) == len(pits)): 
                res.coef += 1
        if (pits[ind + 1].middlename is not None): 
            info = pits[ind].kit.statistics.get_word_info(pits[ind + 1].begin_token)
            if (info is not None and info.not_capital_before_count > 0): 
                pass
            else: 
                res.coef -= (1 + ind)
                if (res.morph.gender == MorphGender.MASCULINE or res.morph.gender == MorphGender.FEMINIE): 
                    if (pits[ind + 1].lastname is not None and ((pits[ind + 1].lastname.is_in_dictionary or pits[ind + 1].lastname.is_in_ontology))): 
                        pass
                    else: 
                        for v in pits[ind + 1].middlename.vars0_: 
                            if (((v.gender) & (res.morph.gender)) != (MorphGender.UNDEFINED)): 
                                res.coef -= (1)
                                break
        if (pits[ind].chars != pits[ind + 1].chars): 
            if (pits[ind].chars.is_capital_upper and pits[ind + 1].chars.is_all_upper): 
                pass
            elif (pits[ind].chars.is_all_upper and pits[ind + 1].chars.is_capital_upper and pits[ind].firstname is None): 
                res.coef -= (10)
            else: 
                res.coef -= (1)
            if (pits[ind].firstname is None or not pits[ind].firstname.is_in_dictionary or pits[ind].chars.is_all_upper): 
                res.coef -= (1)
        elif (pits[ind].chars.is_all_upper): 
            res.coef -= (0.5)
        if (pits[ind].is_in_dictionary): 
            if (pits[ind + 1].is_in_dictionary): 
                res.coef -= (2)
                if (pits[ind + 1].is_newline_after): 
                    res.coef += 1
                elif (pits[ind + 1].end_token.next0_ is not None and pits[ind + 1].end_token.next0_.is_char_of(".,:")): 
                    res.coef += 1
                if (pits[ind].is_in_dictionary and pits[ind].firstname is None): 
                    res.coef -= 1
            elif (pits[ind].firstname is None or not pits[ind].firstname.is_in_dictionary): 
                if (inf.case_.is_undefined): 
                    res.coef -= (1)
                else: 
                    for mi in pits[ind].begin_token.morph.items: 
                        if (not ((mi.case_) & inf.case_).is_undefined): 
                            if ((isinstance(mi, MorphWordForm)) and mi.is_in_dictionary): 
                                res.coef -= (1)
                                break
        if (not pits[ind].chars.is_latin_letter): 
            npt = NounPhraseHelper.try_parse(pits[ind].begin_token, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None and npt.end_char >= pits[ind + 1].begin_char): 
                if (pits[ind].begin_token.get_morph_class_in_dictionary().is_adjective): 
                    res.coef -= (2)
                elif (pits[ind + 1].begin_token.get_morph_class_in_dictionary().is_noun): 
                    res.coef -= (2)
        PersonIdentityToken.__correct_coef_after_lastname(res, pits, ind + 2)
        if (ind > 0 and res.coef > 0 and pits[ind].is_hiphen_before): 
            b1 = pits[ind].kit.statistics.get_bigramm_info(pits[ind - 1].begin_token, pits[ind].begin_token)
            if (b1 is not None and b1.second_count == b1.pair_count): 
                res0 = PersonIdentityToken._new2486(pits[ind].begin_token, pits[ind + 1].end_token, FioTemplateType.NAMESURNAME)
                PersonIdentityToken.manage_firstname(res0, pits[ind - 1], inf)
                res.firstname = PersonMorphCollection.add_prefix(res0.firstname, res.firstname)
                res.coef += 1
                res.begin_token = pits[ind - 1].begin_token
        if (BracketHelper.can_be_start_of_sequence(res.begin_token.previous, False, False) and BracketHelper.can_be_end_of_sequence(res.end_token.next0_, False, None, False)): 
            res.coef -= (2)
        bi = pits[0].begin_token.kit.statistics.get_initial_info(pits[ind].value, pits[ind + 1].begin_token)
        if (bi is not None and bi.pair_count > 0): 
            res.coef += (2)
        if ((not pits[0].is_in_dictionary and pits[1].lastname is not None and pits[1].lastname.is_lastname_has_std_tail) and not pits[1].is_in_dictionary): 
            res.coef += 0.5
        if (res.firstname is not None and pits[ind].begin_token.is_value("СЛАВА", None)): 
            res.coef -= (3)
        elif (PersonIdentityToken.check_latin_after(res) is not None): 
            res.coef += (2)
        if (pits[0].firstname is None or ((pits[0].firstname is not None and not pits[0].firstname.is_in_dictionary))): 
            if (pits[0].begin_token.get_morph_class_in_dictionary().is_proper_geo and pits[1].lastname is not None and pits[1].lastname.is_in_ontology): 
                res.coef -= (2)
        if (ind == 0 and len(pits) == 2 and pits[0].chars.is_latin_letter): 
            if (pits[0].firstname is not None): 
                if (not is_attr_before and (isinstance(pits[0].begin_token.previous, TextToken)) and pits[0].begin_token.previous.chars.is_capital_upper): 
                    res.coef -= (1)
                else: 
                    res.coef += (1)
            if (pits[0].chars.is_all_upper and pits[1].chars.is_capital_upper): 
                res.coef = (0)
        return res
    
    @staticmethod
    def __try_attach_name_secname_surname(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo', prev_has_this_typ : bool=False) -> 'PersonIdentityToken':
        if ((ind + 2) >= len(pits) or pits[ind].typ != PersonItemToken.ItemType.VALUE or pits[ind + 2].typ != PersonItemToken.ItemType.VALUE): 
            return None
        if (pits[ind].is_newline_after): 
            if ((len(pits) == 3 and pits[0].firstname is not None and pits[1].middlename is not None) and pits[2].lastname is not None): 
                pass
            else: 
                return None
        if (pits[ind + 2].lastname is None and not prev_has_this_typ and not pits[ind].morph.language.is_en): 
            return None
        ok = False
        need_test_name_surname = False
        add_coef = 0
        if (pits[ind + 1].typ == PersonItemToken.ItemType.INITIAL): 
            ok = True
        elif (pits[ind + 1].typ == PersonItemToken.ItemType.VALUE and pits[ind + 1].middlename is not None): 
            ok = True
        elif (pits[ind + 1].typ == PersonItemToken.ItemType.VALUE and pits[ind + 2].firstname is None): 
            b1 = pits[0].kit.statistics.get_bigramm_info(pits[ind + 1].begin_token, pits[ind + 2].begin_token)
            b2 = pits[0].kit.statistics.get_bigramm_info(pits[ind].begin_token, pits[ind + 2].begin_token)
            if (b1 is not None): 
                if (b1.pair_count == b1.first_count and b1.pair_count == b1.second_count): 
                    ok = True
                    b3 = pits[0].kit.statistics.get_bigramm_info(pits[ind].begin_token, pits[ind + 1].begin_token)
                    if (b3 is not None): 
                        if (b3.second_count > b3.pair_count): 
                            ok = False
                        elif (b3.second_count == b3.pair_count and pits[ind + 2].is_hiphen_before): 
                            ok = False
                elif (b2 is not None and (b2.pair_count + b1.pair_count) == b1.second_count): 
                    ok = True
            elif ((ind + 3) == len(pits) and pits[ind + 2].lastname is not None and not pits[ind + 2].is_in_dictionary): 
                ok = True
            if (not ok): 
                b1 = pits[0].kit.statistics.get_initial_info(pits[ind].value, pits[ind + 2].begin_token)
                if (b1 is not None and b1.pair_count > 0): 
                    ok = True
                    add_coef = 2
            if (not ok): 
                wi = pits[0].kit.statistics.get_word_info(pits[ind + 2].end_token)
                if (wi is not None and wi.lower_count == 0): 
                    if (wi.male_verbs_after_count > 0 or wi.female_verbs_after_count > 0): 
                        ok = True
                        add_coef = 2
                        need_test_name_surname = True
                        if (pits[ind + 1].firstname is not None and pits[ind + 1].middlename is None): 
                            if (pits[ind].firstname is None and pits[ind].value is not None and pits[ind].is_in_dictionary): 
                                ok = False
                        if (pits[ind + 1].lastname is not None and ((pits[ind + 1].lastname.is_in_dictionary or pits[ind + 1].lastname.is_in_ontology))): 
                            ok = False
            if (not ok): 
                if ((ind == 0 and len(pits) == 3 and pits[0].chars.is_latin_letter) and pits[1].chars.is_latin_letter and pits[2].chars.is_latin_letter): 
                    if (pits[0].firstname is not None and pits[2].lastname is not None): 
                        ok = True
        if (not ok): 
            return None
        if (PersonIdentityToken.__is_both_surnames(pits[ind], pits[ind + 2])): 
            return None
        ok = False
        i = ind
        while i < (ind + 3): 
            if (pits[i].typ == PersonItemToken.ItemType.INITIAL): 
                ok = True
            elif (not pits[i].is_in_dictionary): 
                cla = pits[i].begin_token.get_morph_class_in_dictionary()
                if (cla.is_proper_name or cla.is_proper_surname or cla.is_proper_secname): 
                    ok = True
                elif (cla.is_undefined): 
                    ok = True
            i += 1
        if (not ok): 
            return None
        res = PersonIdentityToken(pits[ind].begin_token, pits[ind + 2].end_token)
        res.typ = (FioTemplateType.NAMEISURNAME if pits[ind + 1].typ == PersonItemToken.ItemType.INITIAL else FioTemplateType.NAMESECNAMESURNAME)
        res.coef -= (ind)
        res.morph = PersonIdentityToken.__accord_morph(inf, pits[ind + 2].lastname, pits[ind].firstname, pits[ind + 1].middlename, pits[ind + 2].end_token.next0_)
        if (res.morph.gender == MorphGender.MASCULINE or res.morph.gender == MorphGender.FEMINIE): 
            res.coef += (1)
            inf = (res.morph)
        PersonIdentityToken.manage_firstname(res, pits[ind], inf)
        PersonIdentityToken.manage_lastname(res, pits[ind + 2], inf)
        if (pits[ind + 1].middlename is not None and len(pits[ind + 1].middlename.vars0_) > 0): 
            res.coef += 1
            res.middlename = (pits[ind + 1].middlename.vars0_[0].value)
            if (len(pits[ind + 1].middlename.vars0_) > 1): 
                res.middlename = (PersonMorphCollection())
                PersonIdentityToken.__set_value2(Utils.asObjectOrNull(res.middlename, PersonMorphCollection), pits[ind + 1].middlename, inf)
            if (pits[ind + 2].lastname is not None): 
                if (pits[ind + 2].lastname.is_in_dictionary or pits[ind + 2].lastname.is_lastname_has_std_tail or pits[ind + 2].lastname.is_has_std_postfix): 
                    res.coef += 1
        elif (pits[ind + 1].typ == PersonItemToken.ItemType.INITIAL): 
            res.middlename = (pits[ind + 1].value)
            res.coef += 1
            if (pits[ind + 2].lastname is not None): 
                pass
            else: 
                npt = NounPhraseHelper.try_parse(pits[ind + 2].begin_token, Utils.valToEnum((NounPhraseParseAttr.PARSEPREPOSITION) | (NounPhraseParseAttr.PARSEPRONOUNS) | (NounPhraseParseAttr.PARSEADVERBS), NounPhraseParseAttr), 0, None)
                if (npt is not None and npt.end_char > pits[ind + 2].end_char): 
                    res.coef -= (2)
        elif (pits[ind + 1].firstname is not None and pits[ind + 2].middlename is not None and len(pits) == 3): 
            res.coef -= (2)
        else: 
            PersonIdentityToken.__manage_middlename(res, pits[ind + 1], inf)
            res.coef += (0.5)
        if (pits[ind].chars != pits[ind + 2].chars): 
            res.coef -= (1)
            if (pits[ind].chars.is_all_upper): 
                res.coef -= (1)
        elif (pits[ind + 1].typ != PersonItemToken.ItemType.INITIAL and pits[ind].chars != pits[ind + 1].chars): 
            res.coef -= (1)
        PersonIdentityToken.__correct_coef_after_lastname(res, pits, ind + 3)
        res.coef += (add_coef)
        if (pits[ind].is_in_dictionary and pits[ind + 1].is_in_dictionary and pits[ind + 2].is_in_dictionary): 
            res.coef -= 1
        return res
    
    @staticmethod
    def __try_attach_name_secname(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo', prev_has_this_typ : bool=False) -> 'PersonIdentityToken':
        if ((ind != 0 or (ind + 2) != len(pits) or pits[ind].typ != PersonItemToken.ItemType.VALUE) or pits[ind + 1].typ != PersonItemToken.ItemType.VALUE): 
            return None
        if (pits[ind].is_newline_after): 
            return None
        if (pits[ind].firstname is None or pits[ind + 1].middlename is None): 
            return None
        res = PersonIdentityToken(pits[ind].begin_token, pits[ind + 1].end_token)
        res.typ = FioTemplateType.NAMESECNAME
        res.morph = PersonIdentityToken.__accord_morph(inf, None, pits[ind].firstname, pits[ind + 1].middlename, pits[ind + 1].end_token.next0_)
        if (res.morph.gender == MorphGender.MASCULINE or res.morph.gender == MorphGender.FEMINIE): 
            res.coef += (1)
            inf = (res.morph)
        PersonIdentityToken.manage_firstname(res, pits[ind], inf)
        PersonIdentityToken.__manage_middlename(res, pits[ind + 1], inf)
        res.coef = (2)
        return res
    
    @staticmethod
    def __correct_coef_after_lastname(res : 'PersonIdentityToken', pits : typing.List['PersonItemToken'], ind : int) -> None:
        from pullenti.ner.person.internal.PersonHelper import PersonHelper
        if (not pits[ind - 1].is_newline_after): 
            pat = PersonAttrToken.try_attach(pits[ind - 1].begin_token, None, PersonAttrToken.PersonAttrAttachAttrs.ONLYKEYWORD)
            if (pat is not None): 
                res.coef -= (1)
        if (ind >= len(pits)): 
            if (PersonIdentityToken.check_latin_after(res) is not None): 
                res.coef += (2)
            te = pits[ind - 1].end_token
            stat = te.kit.statistics.get_word_info(te)
            if (stat is not None): 
                if (stat.has_before_person_attr): 
                    res.coef += 1
            te = pits[ind - 1].end_token.next0_
            if (te is None): 
                return
            if (PersonHelper.is_person_say_or_attr_after(te)): 
                res.coef += 1
                if (res.chars.is_latin_letter and res.typ == FioTemplateType.NAMESURNAME): 
                    res.coef += (2)
            if (not te.chars.is_letter and not te.chars.is_all_lower): 
                return
            wi = te.kit.statistics.get_word_info(te)
            if (wi is not None): 
                if (wi.lower_count > 0): 
                    res.coef -= 1
                elif ((wi.female_verbs_after_count + wi.male_verbs_after_count) > 0): 
                    res.coef += 1
            return
        if (ind == 0): 
            return
        if (pits[ind].typ == PersonItemToken.ItemType.VALUE and ((pits[ind].firstname is None or ind == (len(pits) - 1)))): 
            b1 = pits[0].kit.statistics.get_bigramm_info(pits[ind - 1].begin_token, pits[ind].begin_token)
            if ((b1 is not None and b1.first_count == b1.pair_count and b1.second_count == b1.pair_count) and b1.pair_count > 0): 
                ok = False
                if (b1.pair_count > 1 and pits[ind].whitespaces_before_count == 1): 
                    ok = True
                elif (pits[ind].is_hiphen_before and pits[ind].lastname is not None): 
                    ok = True
                if (ok): 
                    res1 = PersonIdentityToken(pits[ind].begin_token, pits[ind].end_token)
                    PersonIdentityToken.manage_lastname(res1, pits[ind], res.morph)
                    res.lastname = PersonMorphCollection.add_prefix(res.lastname, res1.lastname)
                    res.end_token = pits[ind].end_token
                    res.coef += 1
                    ind += 1
                    if (ind >= len(pits)): 
                        return
        if (pits[ind - 1].whitespaces_before_count > pits[ind - 1].whitespaces_after_count): 
            res.coef -= (1)
        elif (pits[ind - 1].whitespaces_before_count == pits[ind - 1].whitespaces_after_count): 
            if (pits[ind].lastname is not None or pits[ind].firstname is not None): 
                if (not pits[ind].is_in_dictionary): 
                    res.coef -= (1)
    
    @staticmethod
    def __correct_coef_for_lastname(pit : 'PersonIdentityToken', it : 'PersonItemToken') -> None:
        if (it.begin_token != it.end_token): 
            return
        tt = Utils.asObjectOrNull(it.begin_token, TextToken)
        if (tt is None): 
            return
        in_dic = False
        has_std = False
        for wf in tt.morph.items: 
            if (wf.class0_.is_proper_surname): 
                pass
            elif (wf.is_in_dictionary): 
                in_dic = True
        if (it.lastname is not None): 
            has_std = it.lastname.is_lastname_has_std_tail
        if (not has_std and in_dic): 
            pit.coef -= 1.5
    
    @staticmethod
    def __try_attach_surname_name(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo', prev_has_this_typ : bool=False) -> 'PersonIdentityToken':
        if ((ind + 1) >= len(pits) or pits[ind + 1].typ != PersonItemToken.ItemType.VALUE or pits[ind].typ != PersonItemToken.ItemType.VALUE): 
            return None
        if (pits[ind].lastname is None and not prev_has_this_typ): 
            return None
        if (PersonIdentityToken.__is_both_surnames(pits[ind], pits[ind + 1])): 
            return None
        res = PersonIdentityToken._new2486(pits[ind].begin_token, pits[ind + 1].end_token, FioTemplateType.SURNAMENAME)
        res.coef -= (ind)
        if (pits[ind].is_newline_after): 
            res.coef -= 1
            if (pits[ind].whitespaces_after_count > 15): 
                res.coef -= 1
        res.morph = PersonIdentityToken.__accord_morph(inf, pits[ind].lastname, pits[ind + 1].firstname, None, pits[ind + 1].end_token.next0_)
        if (res.morph.gender == MorphGender.MASCULINE or res.morph.gender == MorphGender.FEMINIE): 
            if (pits[ind].lastname is not None and not pits[ind].lastname.morph.case_.is_undefined): 
                res.coef += (1)
            inf = (res.morph)
        PersonIdentityToken.manage_lastname(res, pits[ind], inf)
        PersonIdentityToken.manage_firstname(res, pits[ind + 1], inf)
        PersonIdentityToken.__correct_coef_for_lastname(res, pits[ind])
        if (pits[ind].chars != pits[ind + 1].chars): 
            res.coef -= (1)
            if (pits[ind + 1].firstname is None or not pits[ind + 1].firstname.is_in_dictionary or pits[ind + 1].chars.is_all_upper): 
                res.coef -= (1)
        elif (pits[ind].chars.is_all_upper): 
            res.coef -= (0.5)
        if (pits[ind + 1].is_in_dictionary and ((pits[ind + 1].firstname is None or not pits[ind + 1].firstname.is_in_dictionary))): 
            res.coef -= (1)
        PersonIdentityToken.__correct_coef_after_name(res, pits, ind + 2)
        npt = NounPhraseHelper.try_parse(pits[ind + 1].end_token, NounPhraseParseAttr.NO, 0, None)
        if (npt is not None and npt.end_token != pits[ind + 1].end_token): 
            res.coef -= (1)
        if (ind == 0): 
            PersonIdentityToken.__correct_coefsns(res, pits, ind + 2)
        if (pits[ind].end_token.next0_.is_hiphen): 
            res.coef -= (2)
        if (BracketHelper.can_be_start_of_sequence(res.begin_token.previous, False, False) and BracketHelper.can_be_end_of_sequence(res.end_token.next0_, False, None, False)): 
            res.coef -= (2)
        if (pits[ind].is_in_dictionary): 
            mc = pits[ind].begin_token.get_morph_class_in_dictionary()
            if (mc.is_pronoun or mc.is_personal_pronoun): 
                return None
        if (((len(pits) == 2 and ind == 0 and pits[0].chars.is_all_upper) and pits[1].chars.is_capital_upper and not pits[1].is_in_dictionary) and (res.coef < 0)): 
            res.coef = (0)
        return res
    
    @staticmethod
    def __correct_coefsns(res : 'PersonIdentityToken', pits : typing.List['PersonItemToken'], ind_after : int) -> None:
        if (ind_after >= len(pits)): 
            return
        if (pits[0].lastname is None or not pits[0].lastname.is_lastname_has_std_tail): 
            stat = pits[0].kit.statistics.get_word_info(pits[1].begin_token)
            stata = pits[0].kit.statistics.get_word_info(pits[2].begin_token)
            statb = pits[0].kit.statistics.get_word_info(pits[0].begin_token)
            if (stat is not None and stata is not None and statb is not None): 
                if (stat.like_chars_after_words is not None and stat.like_chars_before_words is not None): 
                    coua = 0
                    coub = 0
                    wrapcoua2493 = RefOutArgWrapper(0)
                    Utils.tryGetValue(stat.like_chars_after_words, stata, wrapcoua2493)
                    coua = wrapcoua2493.value
                    wrapcoub2492 = RefOutArgWrapper(0)
                    Utils.tryGetValue(stat.like_chars_before_words, statb, wrapcoub2492)
                    coub = wrapcoub2492.value
                    if (coua == stat.total_count and (coub < stat.total_count)): 
                        res.coef -= (2)
            return
        if (pits[1].firstname is None): 
            return
        middle = None
        if (ind_after > 2 and pits[2].middlename is not None): 
            middle = pits[2].middlename
        inf = MorphBaseInfo()
        mi1 = PersonIdentityToken.__accord_morph(inf, pits[0].lastname, pits[1].firstname, middle, None)
        if (mi1.case_.is_undefined): 
            res.coef -= (1)
        if (pits[ind_after].lastname is None or not pits[ind_after].lastname.is_lastname_has_std_tail): 
            return
        mi2 = PersonIdentityToken.__accord_morph(inf, pits[ind_after].lastname, pits[1].firstname, middle, pits[ind_after].end_token.next0_)
        if (not mi2.case_.is_undefined): 
            res.coef -= (1)
    
    @staticmethod
    def __try_attach_surname_name_secname(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo', prev_has_this_typ : bool=False, always : bool=False) -> 'PersonIdentityToken':
        if ((ind + 2) >= len(pits) or pits[ind + 1].typ != PersonItemToken.ItemType.VALUE or pits[ind].typ != PersonItemToken.ItemType.VALUE): 
            return None
        if (pits[ind].lastname is None and not prev_has_this_typ): 
            if (ind > 0): 
                return None
            if (len(pits) == 3 and not always): 
                tt1 = pits[2].end_token.next0_
                if (tt1 is not None and tt1.is_comma): 
                    tt1 = tt1.next0_
                if (tt1 is not None and not tt1.is_newline_before and PersonAttrToken.try_attach(tt1, None, PersonAttrToken.PersonAttrAttachAttrs.ONLYKEYWORD) is not None): 
                    pass
                else: 
                    return None
        if (not always): 
            if (PersonIdentityToken.__is_both_surnames(pits[ind], pits[ind + 2])): 
                return None
            if (PersonIdentityToken.__is_both_surnames(pits[ind], pits[ind + 1])): 
                if (len(pits) == 3 and ind == 0 and pits[2].middlename is not None): 
                    pass
                else: 
                    return None
        res = PersonIdentityToken._new2486(pits[ind].begin_token, pits[ind + 2].end_token, FioTemplateType.SURNAMENAMESECNAME)
        if (pits[ind + 2].middlename is None): 
            if ((ind + 2) == (len(pits) - 1) and prev_has_this_typ): 
                res.coef += (1)
            elif (pits[ind + 1].firstname is not None and pits[ind + 2].firstname is not None): 
                pass
            elif (not always): 
                return None
        res.coef -= (ind)
        if (pits[ind].is_newline_after): 
            if (pits[ind].is_newline_before and pits[ind + 2].is_newline_after): 
                pass
            else: 
                res.coef -= 1
                if (pits[ind].whitespaces_after_count > 15): 
                    res.coef -= 1
        if (pits[ind + 1].is_newline_after): 
            if (pits[ind].is_newline_before and pits[ind + 2].is_newline_after): 
                pass
            else: 
                res.coef -= 1
                if (pits[ind + 1].whitespaces_after_count > 15): 
                    res.coef -= 1
        res.morph = PersonIdentityToken.__accord_morph(inf, pits[ind].lastname, pits[ind + 1].firstname, pits[ind + 2].middlename, pits[ind + 2].end_token.next0_)
        if (res.morph.gender == MorphGender.MASCULINE or res.morph.gender == MorphGender.FEMINIE): 
            res.coef += 1.5
            inf = (res.morph)
        PersonIdentityToken.manage_lastname(res, pits[ind], inf)
        PersonIdentityToken.__correct_coef_for_lastname(res, pits[ind])
        PersonIdentityToken.manage_firstname(res, pits[ind + 1], inf)
        if (pits[ind + 2].middlename is not None and len(pits[ind + 2].middlename.vars0_) > 0): 
            res.coef += 1
            res.middlename = (pits[ind + 2].middlename.vars0_[0].value)
            if (len(pits[ind + 2].middlename.vars0_) > 1): 
                res.middlename = (PersonMorphCollection())
                PersonIdentityToken.__set_value2(Utils.asObjectOrNull(res.middlename, PersonMorphCollection), pits[ind + 2].middlename, inf)
            if (pits[ind + 1].firstname is not None and len(pits) == 3 and not pits[ind].is_in_dictionary): 
                res.coef += 1
        else: 
            PersonIdentityToken.__manage_middlename(res, pits[ind + 2], inf)
        if (pits[ind].chars != pits[ind + 1].chars or pits[ind].chars != pits[ind + 2].chars): 
            res.coef -= (1)
            if (pits[ind].chars.is_all_upper and pits[ind + 1].chars.is_capital_upper and pits[ind + 2].chars.is_capital_upper): 
                res.coef += (2)
        tt = Utils.asObjectOrNull(pits[ind].begin_token, TextToken)
        if (tt is not None): 
            if (tt.is_value("УВАЖАЕМЫЙ", None) or tt.is_value("ДОРОГОЙ", None)): 
                res.coef -= (2)
        PersonIdentityToken.__correct_coef_after_name(res, pits, ind + 3)
        if (ind == 0): 
            PersonIdentityToken.__correct_coefsns(res, pits, ind + 3)
        if (pits[ind].is_in_dictionary and pits[ind + 1].is_in_dictionary and pits[ind + 2].is_in_dictionary): 
            res.coef -= 1
        return res
    
    @staticmethod
    def __correct_coef_after_name(res : 'PersonIdentityToken', pits : typing.List['PersonItemToken'], ind : int) -> None:
        if (ind >= len(pits)): 
            return
        if (ind == 0): 
            return
        if (pits[ind - 1].whitespaces_before_count > pits[ind - 1].whitespaces_after_count): 
            res.coef -= (1)
        elif (pits[ind - 1].whitespaces_before_count == pits[ind - 1].whitespaces_after_count): 
            if (pits[ind].lastname is not None or pits[ind].firstname is not None or pits[ind].middlename is not None): 
                res.coef -= (1)
        t = pits[ind - 1].end_token.next0_
        if (t is not None and t.next0_ is not None and t.next0_.is_char(',')): 
            t = t.next0_
        if (t is not None): 
            if (PersonAttrToken.try_attach(t, None, PersonAttrToken.PersonAttrAttachAttrs.ONLYKEYWORD) is not None): 
                res.coef += (1)
    
    @staticmethod
    def __calc_coef_after(tt : 'Token') -> float:
        if (tt is not None and tt.is_comma): 
            tt = tt.next0_
        attr = PersonAttrToken.try_attach(tt, None, PersonAttrToken.PersonAttrAttachAttrs.ONLYKEYWORD)
        if (attr is not None and attr.age is not None): 
            return 3
        if (tt is not None and tt.get_referent() is not None and tt.get_referent().type_name == "DATE"): 
            co = 1
            if (tt.next0_ is not None and tt.next0_.is_value("Р", None)): 
                co += (2)
            return co
        return 0
    
    @staticmethod
    def __try_attach_surnameii(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo') -> 'PersonIdentityToken':
        if ((ind + 1) >= len(pits) or pits[ind + 1].typ != PersonItemToken.ItemType.INITIAL or pits[ind].typ == PersonItemToken.ItemType.INITIAL): 
            return None
        if (pits[ind].is_newline_after): 
            return None
        if (pits[ind].lastname is None): 
            return None
        res = PersonIdentityToken._new2486(pits[ind].begin_token, pits[ind + 1].end_token, FioTemplateType.SURNAMEI)
        res.coef -= (ind)
        PersonIdentityToken.manage_lastname(res, pits[ind], inf)
        if (pits[ind].is_asian_item(False) and pits[ind].lastname is not None and pits[ind].lastname.is_china_surname): 
            pass
        elif (pits[ind].firstname is not None and pits[ind].firstname.is_in_dictionary): 
            if (pits[ind].lastname is None or not pits[ind].lastname.is_lastname_has_std_tail): 
                if ((ind == 0 and len(pits) == 3 and not pits[1].is_newline_after) and not pits[2].is_whitespace_after): 
                    pass
                else: 
                    res.coef -= (2)
        res.morph = (pits[ind].morph if pits[ind].lastname is None else pits[ind].lastname.morph)
        if (res.lastname.gender != MorphGender.UNDEFINED): 
            res.morph.gender = res.lastname.gender
        if (pits[ind].whitespaces_after_count < 2): 
            res.coef += (0.5)
        res.firstname = PersonMorphCollection()
        res.firstname.add(pits[ind + 1].value, None, MorphGender.UNDEFINED, False)
        i1 = ind + 2
        if ((i1 < len(pits)) and pits[i1].typ == PersonItemToken.ItemType.INITIAL): 
            res.typ = FioTemplateType.SURNAMEII
            res.end_token = pits[i1].end_token
            res.middlename = (pits[i1].value)
            if (pits[i1].whitespaces_before_count < 2): 
                res.coef += (0.5)
            i1 += 1
        if (i1 >= len(pits)): 
            if (pits[0].lastname is not None and ((pits[0].lastname.is_in_dictionary or pits[0].lastname.is_in_ontology)) and pits[0].firstname is None): 
                res.coef += 1
            return res
        if (pits[ind].whitespaces_after_count > pits[i1].whitespaces_before_count): 
            res.coef -= 1
        elif (pits[ind].whitespaces_after_count == pits[i1].whitespaces_before_count and pits[i1].lastname is not None): 
            if ((i1 + 3) == len(pits) and pits[i1 + 1].typ == PersonItemToken.ItemType.INITIAL and pits[i1 + 2].typ == PersonItemToken.ItemType.INITIAL): 
                pass
            else: 
                if (pits[i1].is_in_dictionary and pits[i1].begin_token.get_morph_class_in_dictionary().is_noun): 
                    pass
                else: 
                    res.coef -= 1
                ok = True
                tt = pits[ind].begin_token.previous
                while tt is not None: 
                    if (tt.is_newline_before): 
                        break
                    elif (tt.get_referent() is not None and not (isinstance(tt.get_referent(), PersonReferent))): 
                        ok = False
                        break
                    elif ((isinstance(tt, TextToken)) and tt.chars.is_letter): 
                        ok = False
                        break
                    tt = tt.previous
                if (ok): 
                    res.coef += 1
        return res
    
    @staticmethod
    def __try_attachiisurname(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo') -> 'PersonIdentityToken':
        if ((ind + 1) >= len(pits) or pits[ind].typ != PersonItemToken.ItemType.INITIAL): 
            return None
        if (ind > 0): 
            if (pits[ind - 1].typ == PersonItemToken.ItemType.INITIAL): 
                return None
        if (pits[ind].is_newline_after): 
            return None
        res = PersonIdentityToken._new2486(pits[ind].begin_token, pits[ind + 1].end_token, FioTemplateType.ISURNAME)
        res.coef -= (ind)
        res.firstname = PersonMorphCollection()
        res.firstname.add(pits[ind].value, None, MorphGender.UNDEFINED, False)
        i1 = ind + 1
        if (pits[i1].typ == PersonItemToken.ItemType.INITIAL): 
            res.typ = FioTemplateType.IISURNAME
            res.middlename = (pits[i1].value)
            if (pits[i1].whitespaces_before_count < 2): 
                res.coef += (0.5)
            i1 += 1
        if (i1 >= len(pits) or pits[i1].typ != PersonItemToken.ItemType.VALUE): 
            return None
        if (pits[i1].is_newline_before): 
            return None
        res.end_token = pits[i1].end_token
        prev = None
        if (not pits[ind].is_newline_before): 
            if (ind > 0): 
                prev = pits[ind - 1]
            else: 
                prev = PersonItemToken.try_attach(pits[ind].begin_token.previous, None, (PersonItemToken.ParseAttr.CANBELATIN if pits[i1].chars.is_latin_letter else PersonItemToken.ParseAttr.NO), None)
                if (prev is not None): 
                    if (PersonAttrToken.try_attach_word(prev.begin_token) is not None): 
                        prev = (None)
                        res.coef += 1
        PersonIdentityToken.manage_lastname(res, pits[i1], inf)
        if (pits[i1].lastname is not None and pits[i1].lastname.is_in_ontology): 
            res.coef += 1
        if (pits[i1].firstname is not None and pits[i1].firstname.is_in_dictionary): 
            if (pits[i1].lastname is None or ((not pits[i1].lastname.is_lastname_has_std_tail and not pits[i1].lastname.is_in_ontology))): 
                res.coef -= (2)
        if (prev is not None): 
            mc = prev.begin_token.get_morph_class_in_dictionary()
            if (mc.is_preposition or mc.is_adverb or mc.is_verb): 
                res.coef += (ind)
                if (pits[i1].lastname is not None): 
                    if (pits[i1].lastname.is_in_dictionary or pits[i1].lastname.is_in_ontology): 
                        res.coef += (1)
            if (prev.lastname is not None and ((prev.lastname.is_lastname_has_std_tail or prev.lastname.is_in_dictionary))): 
                res.coef -= (1)
        res.morph = (pits[i1].morph if pits[i1].lastname is None else pits[i1].lastname.morph)
        if (res.lastname.gender != MorphGender.UNDEFINED): 
            res.morph.gender = res.lastname.gender
        if (pits[i1].whitespaces_before_count < 2): 
            if (not pits[ind].is_newline_before and (pits[ind].whitespaces_before_count < 2) and prev is not None): 
                pass
            else: 
                res.coef += (0.5)
        if (prev is None): 
            if (pits[ind].is_newline_before and pits[i1].is_newline_after): 
                res.coef += (1)
            elif (pits[i1].end_token.next0_ is not None and ((pits[i1].end_token.next0_.is_char_of(";,.") or pits[i1].end_token.next0_.morph.class0_.is_conjunction))): 
                res.coef += (1)
            return res
        if (prev.whitespaces_after_count < pits[i1].whitespaces_before_count): 
            res.coef -= 1
        elif (prev.whitespaces_after_count == pits[i1].whitespaces_before_count and prev.lastname is not None): 
            res.coef -= 1
        return res
    
    @staticmethod
    def __try_attach_king(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo', prev_has_this_typ : bool=False) -> 'PersonIdentityToken':
        if (ind > 0 or ind >= len(pits)): 
            return None
        if (pits[0].firstname is None or pits[0].is_newline_after): 
            return None
        if (pits[0].begin_token.is_value("ТОМ", None)): 
            return None
        i = 0
        if (len(pits) > 1 and ((pits[1].firstname is not None or pits[1].middlename is not None))): 
            i += 1
        if (pits[i].is_newline_after): 
            return None
        if (pits[i].end_token.whitespaces_after_count > 2): 
            return None
        num = 0
        roman = False
        ok = False
        t = pits[i].end_token.next0_
        if (isinstance(t, NumberToken)): 
            if (t.chars.is_all_lower or t.int_value is None): 
                return None
            num = t.int_value
            if (not t.morph.class0_.is_adjective): 
                return None
        else: 
            if (((i + 2) < len(pits)) and pits[i + 1].typ == PersonItemToken.ItemType.INITIAL): 
                return None
            nt = NumberHelper.try_parse_roman(t)
            if (nt is not None and nt.int_value is not None): 
                num = nt.int_value
                roman = True
                t = nt.end_token
        if (num < 1): 
            if (pits[0].firstname is not None and prev_has_this_typ): 
                if (len(pits) == 1): 
                    ok = True
                elif (len(pits) == 2 and pits[0].end_token.next0_.is_hiphen): 
                    ok = True
            if (not ok): 
                return None
        res = PersonIdentityToken._new2486(pits[0].begin_token, pits[0].end_token, FioTemplateType.KING)
        res.morph = PersonIdentityToken.__accord_morph(inf, None, pits[0].firstname, ((Utils.ifNotNull(pits[1].middlename, pits[1].firstname)) if len(pits) == 2 else None), pits[(1 if len(pits) == 2 else 0)].end_token.next0_)
        if (res.morph.gender == MorphGender.MASCULINE or res.morph.gender == MorphGender.FEMINIE): 
            inf = (res.morph)
        if (inf.gender != MorphGender.FEMINIE and inf.gender != MorphGender.MASCULINE and not roman): 
            return None
        PersonIdentityToken.manage_firstname(res, pits[0], inf)
        if (num > 0): 
            res.lastname = PersonMorphCollection()
            res.lastname.number = num
            res.end_token = t
        if (i > 0): 
            PersonIdentityToken.__manage_middlename(res, pits[1], inf)
            res.end_token = pits[1].end_token
        res.coef = ((3 if num > 0 else 2))
        return res
    
    @staticmethod
    def __try_attach_asian(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo', cou : int, prev_has_this_typ : bool=False) -> 'PersonIdentityToken':
        if (ind > 0 or ind >= len(pits) or ((len(pits) != cou and len(pits) != (cou * 2)))): 
            return None
        if (pits[0].lastname is not None and pits[0].lastname.is_china_surname and pits[0].chars.is_capital_upper): 
            if (cou == 3): 
                if (not pits[1].is_asian_item(False)): 
                    return None
                if (not pits[2].is_asian_item(True)): 
                    return None
            elif (cou == 2): 
                if (pits[1].typ != PersonItemToken.ItemType.VALUE): 
                    return None
        elif (cou == 3): 
            if (not pits[0].is_asian_item(False)): 
                return None
            if (not pits[1].is_asian_item(False)): 
                return None
            if (not pits[2].is_asian_item(True)): 
                return None
        else: 
            if (not pits[0].is_asian_item(False)): 
                return None
            if (not pits[1].is_asian_item(True)): 
                return None
        cou -= 1
        is_chine_sur = pits[0].lastname is not None and pits[0].lastname.is_china_surname
        res = PersonIdentityToken._new2486(pits[0].begin_token, pits[cou].end_token, FioTemplateType.ASIANNAME)
        if (pits[cou].lastname is not None): 
            res.morph = PersonIdentityToken.__accord_morph(inf, pits[cou].lastname, None, None, pits[cou].end_token.next0_)
        if (not res.morph.case_.is_undefined): 
            inf = (res.morph)
        if (is_chine_sur): 
            res.typ = FioTemplateType.ASIANSURNAMENAME
            res.coef = (2)
            if (pits[1].is_asian_item(True)): 
                res.coef += (1)
            PersonIdentityToken.manage_lastname(res, pits[0], inf)
            tr = PersonReferent._del_surname_end(pits[0].value)
            if (tr != pits[0].value): 
                res.lastname.add(tr, None, MorphGender.MASCULINE, False)
            res.firstname = PersonMorphCollection()
            pref = (pits[1].value if cou == 2 else "")
            if (pits[cou].is_asian_item(False)): 
                res.firstname.add(pref + pits[cou].value, None, MorphGender.MASCULINE, False)
                res.firstname.add(pref + pits[cou].value, None, MorphGender.FEMINIE, False)
                if (len(pref) > 0): 
                    res.firstname.add(pref + "-" + pits[cou].value, None, MorphGender.MASCULINE, False)
                    res.firstname.add(pref + "-" + pits[cou].value, None, MorphGender.FEMINIE, False)
            else: 
                v = PersonReferent._del_surname_end(pits[cou].value)
                res.firstname.add(pref + v, None, MorphGender.MASCULINE, False)
                if (len(pref) > 0): 
                    res.firstname.add(pref + "-" + v, None, MorphGender.MASCULINE, False)
                ss = pits[cou].end_token.get_normal_case_text(MorphClass.NOUN, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                if (ss != v and len(ss) <= len(v)): 
                    res.firstname.add(pref + ss, None, MorphGender.MASCULINE, False)
                    if (len(pref) > 0): 
                        res.firstname.add(pref + "-" + ss, None, MorphGender.MASCULINE, False)
                inf.gender = MorphGender.MASCULINE
        else: 
            if (inf.gender == MorphGender.MASCULINE): 
                PersonIdentityToken.manage_lastname(res, pits[cou], inf)
            else: 
                res.lastname = PersonMorphCollection()
                if (pits[cou].is_asian_item(False)): 
                    res.lastname.add(pits[cou].value, None, MorphGender.MASCULINE, False)
                    res.lastname.add(pits[cou].value, None, MorphGender.FEMINIE, False)
                else: 
                    v = PersonReferent._del_surname_end(pits[cou].value)
                    res.lastname.add(v, None, MorphGender.MASCULINE, False)
                    ss = pits[cou].end_token.get_normal_case_text(MorphClass.NOUN, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                    if (ss != v and len(ss) <= len(v)): 
                        res.lastname.add(ss, None, MorphGender.MASCULINE, False)
                    inf.gender = MorphGender.MASCULINE
            if (cou == 2): 
                res.coef = (2)
                if ((res.whitespaces_after_count < 2) and len(pits) > 3): 
                    res.coef -= 1
                res.lastname.add_prefix_str("{0} {1} ".format(pits[0].value, pits[1].value))
            else: 
                res.coef = (1)
                res.lastname.add_prefix_str(pits[0].value + " ")
            i = 0
            while i < len(pits): 
                if (pits[i].is_in_dictionary): 
                    mc = pits[i].begin_token.get_morph_class_in_dictionary()
                    if ((mc.is_conjunction or mc.is_pronoun or mc.is_preposition) or mc.is_personal_pronoun): 
                        res.coef -= 0.5
                i += 1
        if (pits[0].value == pits[1].value): 
            res.coef -= 0.5
        if (cou == 2): 
            if (pits[0].value == pits[2].value): 
                res.coef -= 0.5
            if (pits[1].value == pits[2].value): 
                res.coef -= 0.5
        if (not pits[cou].is_whitespace_after): 
            t = pits[cou].end_token.next0_
            if (t is not None and t.is_hiphen): 
                res.coef -= 0.5
            if (BracketHelper.can_be_end_of_sequence(t, False, None, False)): 
                res.coef -= 0.5
        if (BracketHelper.can_be_start_of_sequence(pits[0].begin_token.previous, False, False)): 
            res.coef -= 0.5
        return res
    
    @staticmethod
    def try_attach_identity(pits : typing.List['PersonItemToken'], inf : 'MorphBaseInfo') -> 'PersonIdentityToken':
        if (len(pits) == 1): 
            if (pits[0].typ != PersonItemToken.ItemType.REFERENT): 
                return None
        else: 
            if (len(pits) != 2 and len(pits) != 3): 
                return None
            for p in pits: 
                if (p.typ != PersonItemToken.ItemType.VALUE): 
                    return None
                if (p.chars != pits[0].chars): 
                    return None
        begin = Utils.asObjectOrNull(pits[0].begin_token, TextToken)
        end = Utils.asObjectOrNull(pits[len(pits) - 1].end_token, TextToken)
        if (begin is None or end is None): 
            return None
        res = PersonIdentityToken(begin, end)
        res.lastname = PersonMorphCollection()
        s = MiscHelper.get_text_value(begin, end, GetTextAttr.NO)
        if (len(s) > 100): 
            return None
        tmp = io.StringIO()
        t = begin
        first_pass3862 = True
        while True:
            if first_pass3862: first_pass3862 = False
            else: t = t.next0_
            if (not (t is not None and t.previous != end)): break
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is None): 
                continue
            if (tt.is_hiphen): 
                print('-', end="", file=tmp)
                continue
            if (tmp.tell() > 0): 
                if (Utils.getCharAtStringIO(tmp, tmp.tell() - 1) != '-'): 
                    print(' ', end="", file=tmp)
            if (tt.length_char < 3): 
                print(tt.term, end="", file=tmp)
                continue
            sss = tt.term
            for wff in tt.morph.items: 
                wf = Utils.asObjectOrNull(wff, MorphWordForm)
                if (wf is not None and wf.normal_case is not None and (len(wf.normal_case) < len(sss))): 
                    sss = wf.normal_case
            print(sss, end="", file=tmp)
        ss = Utils.toStringStringIO(tmp)
        if (inf.case_.is_nominative): 
            res.lastname.add(s, None, MorphGender.UNDEFINED, False)
            if (s != ss): 
                res.lastname.add(ss, None, MorphGender.UNDEFINED, False)
        else: 
            if (s != ss): 
                res.lastname.add(ss, None, MorphGender.UNDEFINED, False)
            res.lastname.add(s, None, MorphGender.UNDEFINED, False)
        for p in pits: 
            if (p != pits[0]): 
                if (p.is_newline_before): 
                    res.coef -= (1)
                elif (p.whitespaces_before_count > 1): 
                    res.coef -= (0.5)
            res.coef += (0.5)
            if (p.length_char > 4): 
                if (p.is_in_dictionary): 
                    res.coef -= (1.5)
                if (p.lastname is not None and ((p.lastname.is_in_dictionary or p.lastname.is_in_ontology))): 
                    res.coef -= (1)
                if (p.firstname is not None and p.firstname.is_in_dictionary): 
                    res.coef -= (1)
                if (p.middlename is not None): 
                    res.coef -= (1)
                if (p.chars.is_all_upper): 
                    res.coef -= (0.5)
            elif (p.chars.is_all_upper): 
                res.coef -= (1)
        if (len(pits) == 2 and pits[1].lastname is not None and ((pits[1].lastname.is_lastname_has_std_tail or pits[1].lastname.is_in_dictionary))): 
            res.coef -= 0.5
        return res
    
    @staticmethod
    def __try_attach_global(pits : typing.List['PersonItemToken'], ind : int, inf : 'MorphBaseInfo') -> 'PersonIdentityToken':
        if (ind > 0 or pits[0].typ != PersonItemToken.ItemType.VALUE): 
            return None
        if ((len(pits) == 4 and pits[0].value == "АУН" and pits[1].value == "САН") and pits[2].value == "СУ" and pits[3].value == "ЧЖИ"): 
            res = PersonIdentityToken(pits[0].begin_token, pits[3].end_token)
            res.ontology_person = PersonReferent()
            res.ontology_person.add_slot(PersonReferent.ATTR_IDENTITY, "АУН САН СУ ЧЖИ", False, 0)
            res.ontology_person.is_female = True
            res.coef = (10)
            return res
        if (len(pits) == 2 and pits[0].firstname is not None and pits[0].firstname.is_in_dictionary): 
            if (pits[0].begin_token.is_value("ИВАН", None) and pits[1].begin_token.is_value("ГРОЗНЫЙ", None)): 
                res = PersonIdentityToken(pits[0].begin_token, pits[1].end_token)
                res.ontology_person = PersonReferent()
                res.ontology_person.add_slot(PersonReferent.ATTR_FIRSTNAME, "ИВАН", False, 0)
                res.ontology_person.add_slot(PersonReferent.ATTR_NICKNAME, "ГРОЗНЫЙ", False, 0)
                res.ontology_person.is_male = True
                res.coef = (10)
                return res
            if (pits[0].begin_token.is_value("ЮРИЙ", None) and pits[1].begin_token.is_value("ДОЛГОРУКИЙ", None)): 
                res = PersonIdentityToken(pits[0].begin_token, pits[1].end_token)
                res.ontology_person = PersonReferent()
                res.ontology_person.add_slot(PersonReferent.ATTR_FIRSTNAME, "ЮРИЙ", False, 0)
                res.ontology_person.add_slot(PersonReferent.ATTR_NICKNAME, "ДОЛГОРУКИЙ", False, 0)
                res.ontology_person.is_male = True
                res.coef = (10)
                return res
            if (pits[1].begin_token.is_value("ВЕЛИКИЙ", None)): 
                res = PersonIdentityToken(pits[0].begin_token, pits[1].end_token)
                res.ontology_person = PersonReferent()
                if (pits[0].firstname.morph.gender == MorphGender.FEMINIE): 
                    res.ontology_person.is_female = True
                elif (pits[0].firstname.morph.gender == MorphGender.MASCULINE or ((pits[1].morph.gender) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                    res.ontology_person.is_male = True
                else: 
                    return None
                PersonIdentityToken.manage_firstname(res, pits[0], pits[1].morph)
                res.ontology_person._add_fio_identity(None, res.firstname, None)
                res.ontology_person.add_slot(PersonReferent.ATTR_NICKNAME, ("ВЕЛИКИЙ" if res.ontology_person.is_male else "ВЕЛИКАЯ"), False, 0)
                res.coef = (10)
                return res
            if (pits[1].begin_token.is_value("СВЯТОЙ", None)): 
                res = PersonIdentityToken(pits[0].begin_token, pits[1].end_token)
                res.ontology_person = PersonReferent()
                if (pits[0].firstname.morph.gender == MorphGender.FEMINIE): 
                    res.ontology_person.is_female = True
                elif (pits[0].firstname.morph.gender == MorphGender.MASCULINE or ((pits[1].morph.gender) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                    res.ontology_person.is_male = True
                else: 
                    return None
                PersonIdentityToken.manage_firstname(res, pits[0], pits[1].morph)
                res.ontology_person._add_fio_identity(None, res.firstname, None)
                res.ontology_person.add_slot(PersonReferent.ATTR_NICKNAME, ("СВЯТОЙ" if res.ontology_person.is_male else "СВЯТАЯ"), False, 0)
                res.coef = (10)
                return res
            if (pits[1].begin_token.is_value("ПРЕПОДОБНЫЙ", None)): 
                res = PersonIdentityToken(pits[0].begin_token, pits[1].end_token)
                res.ontology_person = PersonReferent()
                if (pits[0].firstname.morph.gender == MorphGender.FEMINIE): 
                    res.ontology_person.is_female = True
                elif (pits[0].firstname.morph.gender == MorphGender.MASCULINE or ((pits[1].morph.gender) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                    res.ontology_person.is_male = True
                else: 
                    return None
                PersonIdentityToken.manage_firstname(res, pits[0], pits[1].morph)
                res.ontology_person._add_fio_identity(None, res.firstname, None)
                res.ontology_person.add_slot(PersonReferent.ATTR_NICKNAME, ("ПРЕПОДОБНЫЙ" if res.ontology_person.is_male else "ПРЕПОДОБНАЯ"), False, 0)
                res.coef = (10)
                return res
            if (pits[1].begin_token.is_value("БЛАЖЕННЫЙ", None)): 
                res = PersonIdentityToken(pits[0].begin_token, pits[1].end_token)
                res.ontology_person = PersonReferent()
                if (pits[0].firstname.morph.gender == MorphGender.FEMINIE): 
                    res.ontology_person.is_female = True
                elif (pits[0].firstname.morph.gender == MorphGender.MASCULINE or ((pits[1].morph.gender) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                    res.ontology_person.is_male = True
                else: 
                    return None
                PersonIdentityToken.manage_firstname(res, pits[0], pits[1].morph)
                res.ontology_person._add_fio_identity(None, res.firstname, None)
                res.ontology_person.add_slot(PersonReferent.ATTR_NICKNAME, ("БЛАЖЕННЫЙ" if res.ontology_person.is_male else "БЛАЖЕННАЯ"), False, 0)
                res.coef = (10)
                return res
        if (len(pits) == 2 and pits[1].firstname is not None and pits[1].firstname.is_in_dictionary): 
            if (pits[0].begin_token.is_value("СВЯТОЙ", None)): 
                res = PersonIdentityToken(pits[0].begin_token, pits[1].end_token)
                res.ontology_person = PersonReferent()
                if (pits[1].firstname.morph.gender == MorphGender.FEMINIE or pits[0].morph.gender == MorphGender.FEMINIE): 
                    res.ontology_person.is_female = True
                elif (pits[1].firstname.morph.gender == MorphGender.MASCULINE or ((pits[0].morph.gender) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                    res.ontology_person.is_male = True
                else: 
                    return None
                PersonIdentityToken.manage_firstname(res, pits[1], pits[0].morph)
                res.ontology_person._add_fio_identity(None, res.firstname, None)
                res.ontology_person.add_slot(PersonReferent.ATTR_NICKNAME, ("СВЯТОЙ" if res.ontology_person.is_male else "СВЯТАЯ"), False, 0)
                res.coef = (10)
                return res
            if (pits[0].begin_token.is_value("ПРЕПОДОБНЫЙ", None)): 
                res = PersonIdentityToken(pits[0].begin_token, pits[1].end_token)
                res.ontology_person = PersonReferent()
                if (pits[1].firstname.morph.gender == MorphGender.FEMINIE): 
                    res.ontology_person.is_female = True
                elif (pits[1].firstname.morph.gender == MorphGender.MASCULINE or ((pits[0].morph.gender) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                    res.ontology_person.is_male = True
                else: 
                    return None
                PersonIdentityToken.manage_firstname(res, pits[1], pits[0].morph)
                res.ontology_person._add_fio_identity(None, res.firstname, None)
                res.ontology_person.add_slot(PersonReferent.ATTR_NICKNAME, ("ПРЕПОДОБНЫЙ" if res.ontology_person.is_male else "ПРЕПОДОБНАЯ"), False, 0)
                res.coef = (10)
                return res
            if (pits[0].begin_token.is_value("БЛАЖЕННЫЙ", None)): 
                res = PersonIdentityToken(pits[0].begin_token, pits[1].end_token)
                res.ontology_person = PersonReferent()
                if (pits[1].firstname.morph.gender == MorphGender.FEMINIE): 
                    res.ontology_person.is_female = True
                elif (pits[1].firstname.morph.gender == MorphGender.MASCULINE or ((pits[0].morph.gender) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                    res.ontology_person.is_male = True
                else: 
                    return None
                PersonIdentityToken.manage_firstname(res, pits[1], pits[0].morph)
                res.ontology_person._add_fio_identity(None, res.firstname, None)
                res.ontology_person.add_slot(PersonReferent.ATTR_NICKNAME, ("БЛАЖЕННЫЙ" if res.ontology_person.is_male else "БЛАЖЕННАЯ"), False, 0)
                res.coef = (10)
                return res
        return None
    
    @staticmethod
    def __accord_morph(inf : 'MorphBaseInfo', p1 : 'MorphPersonItem', p2 : 'MorphPersonItem', p3 : 'MorphPersonItem', next0__ : 'Token') -> 'MorphCollection':
        res = MorphCollection()
        pp = list()
        if (p1 is not None): 
            pp.append(p1)
        if (p2 is not None): 
            pp.append(p2)
        if (p3 is not None): 
            pp.append(p3)
        if (len(pp) == 0): 
            return res
        if (inf is not None and p1 is not None and ((p1.is_lastname_has_std_tail or p1.is_in_dictionary))): 
            if (((inf.case_) & p1.morph.case_).is_undefined): 
                inf = (None)
        if (inf is not None and p2 is not None and p2.is_in_dictionary): 
            if (((inf.case_) & p2.morph.case_).is_undefined): 
                inf = (None)
        for i in range(2):
            g = (MorphGender.MASCULINE if i == 0 else MorphGender.FEMINIE)
            if (inf is not None and inf.gender != MorphGender.UNDEFINED and ((inf.gender) & (g)) == (MorphGender.UNDEFINED)): 
                continue
            cas = MorphCase.ALL_CASES
            for p in pp: 
                ca = MorphCase()
                for v in p.vars0_: 
                    if (v.gender != MorphGender.UNDEFINED): 
                        if (((v.gender) & (g)) == (MorphGender.UNDEFINED)): 
                            continue
                    if (inf is not None and not inf.case_.is_undefined and not v.case_.is_undefined): 
                        if (((inf.case_) & v.case_).is_undefined): 
                            continue
                    if (not v.case_.is_undefined): 
                        ca |= v.case_
                    else: 
                        ca = MorphCase.ALL_CASES
                cas &= ca
            if (not cas.is_undefined): 
                if (inf is not None and not inf.case_.is_undefined and not ((inf.case_) & cas).is_undefined): 
                    cas &= inf.case_
                res.add_item(MorphBaseInfo._new2499(g, cas))
        verb_gend = MorphGender.UNDEFINED
        if ((next0__ is not None and (isinstance(next0__, TextToken)) and next0__.chars.is_all_lower) and next0__.morph.class0_ == MorphClass.VERB and next0__.morph.number == MorphNumber.SINGULAR): 
            if (next0__.morph.gender == MorphGender.FEMINIE or next0__.morph.gender == MorphGender.MASCULINE): 
                verb_gend = next0__.morph.gender
                npt = NounPhraseHelper.try_parse(next0__.next0_, NounPhraseParseAttr.NO, 0, None)
                if ((npt is not None and npt.morph.case_.is_nominative and npt.morph.gender == verb_gend) and npt.morph.number == MorphNumber.SINGULAR): 
                    verb_gend = MorphGender.UNDEFINED
        if (verb_gend != MorphGender.UNDEFINED and res.items_count > 1): 
            cou = 0
            for it in res.items: 
                if (it.case_.is_nominative and it.gender == verb_gend): 
                    cou += 1
            if (cou == 1): 
                for i in range(res.items_count - 1, -1, -1):
                    if (not res.get_indexer_item(i).case_.is_nominative or res.get_indexer_item(i).gender != verb_gend): 
                        res.remove_item(i)
        return res
    
    @staticmethod
    def __is_accords(mt : 'MorphPersonItem', inf : 'MorphBaseInfo') -> bool:
        if (inf is None): 
            return True
        if (len(mt.vars0_) == 0): 
            return True
        for wf in mt.vars0_: 
            ok = True
            if (not inf.case_.is_undefined and not wf.case_.is_undefined): 
                if (((wf.case_) & inf.case_).is_undefined): 
                    ok = False
            if (inf.gender != MorphGender.UNDEFINED and wf.gender != MorphGender.UNDEFINED): 
                if (((inf.gender) & (wf.gender)) == (MorphGender.UNDEFINED)): 
                    ok = False
            if (ok): 
                return True
        return False
    
    @staticmethod
    def __is_both_surnames(p1 : 'PersonItemToken', p2 : 'PersonItemToken') -> bool:
        if (p1 is None or p2 is None): 
            return False
        if (p1.lastname is None or p2.lastname is None): 
            return False
        if (not p1.lastname.is_in_dictionary and not p1.lastname.is_in_ontology and not p1.lastname.is_lastname_has_std_tail): 
            return False
        if (p1.firstname is not None or p2.middlename is not None): 
            return False
        if (not p2.lastname.is_in_dictionary and not p2.lastname.is_in_ontology and not p2.lastname.is_lastname_has_std_tail): 
            return False
        if (p2.firstname is not None or p2.middlename is not None): 
            return False
        if (not (isinstance(p1.end_token, TextToken)) or not (isinstance(p2.end_token, TextToken))): 
            return False
        v1 = p1.end_token.term
        v2 = p2.end_token.term
        if (v1[len(v1) - 1] == v2[len(v2) - 1]): 
            return False
        return True
    
    @staticmethod
    def __get_value(mt : 'MorphPersonItem', inf : 'MorphBaseInfo') -> str:
        for wf in mt.vars0_: 
            if (inf is not None): 
                if (not inf.case_.is_undefined and not wf.case_.is_undefined): 
                    if (((wf.case_) & inf.case_).is_undefined): 
                        continue
                if (inf.gender != MorphGender.UNDEFINED and wf.gender != MorphGender.UNDEFINED): 
                    if (((inf.gender) & (wf.gender)) == (MorphGender.UNDEFINED)): 
                        continue
            return wf.value
        return mt.term
    
    @staticmethod
    def __set_value2(res : 'PersonMorphCollection', mt : 'MorphPersonItem', inf : 'MorphBaseInfo') -> None:
        ok = False
        for wf in mt.vars0_: 
            if (inf is not None): 
                if (not inf.case_.is_undefined and not wf.case_.is_undefined): 
                    if (((wf.case_) & inf.case_).is_undefined): 
                        continue
                if (inf.gender != MorphGender.UNDEFINED and wf.gender != MorphGender.UNDEFINED): 
                    if (((inf.gender) & (wf.gender)) == (MorphGender.UNDEFINED)): 
                        continue
                ok = True
            res.add(wf.value, wf.short_value, wf.gender, False)
        if (len(res.values) == 0): 
            if ((inf is not None and not inf.case_.is_undefined and len(mt.vars0_) > 0) and mt.is_lastname_has_std_tail): 
                for wf in mt.vars0_: 
                    res.add(wf.value, wf.short_value, wf.gender, False)
            res.add(mt.term, None, inf.gender, False)
    
    @staticmethod
    def __set_value(res : 'PersonMorphCollection', t : 'Token', inf : 'MorphBaseInfo') -> None:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None and (isinstance(t, MetaToken)) and t.begin_token == t.end_token): 
            tt = (Utils.asObjectOrNull(t.begin_token, TextToken))
        if (tt is None): 
            return
        for wf in tt.morph.items: 
            if (wf.class0_.is_verb): 
                continue
            if (wf.contains_attr("к.ф.", None)): 
                continue
            if (inf is not None and inf.gender != MorphGender.UNDEFINED and wf.gender != MorphGender.UNDEFINED): 
                if (((wf.gender) & (inf.gender)) == (MorphGender.UNDEFINED)): 
                    continue
            if (inf is not None and not inf.case_.is_undefined and not wf.case_.is_undefined): 
                if (((wf.case_) & inf.case_).is_undefined): 
                    continue
            str0_ = (tt.term if t.chars.is_latin_letter else wf.normal_case)
            res.add(str0_, None, wf.gender, False)
        res.add(tt.term, None, (MorphGender.UNDEFINED if inf is None else inf.gender), False)
    
    @staticmethod
    def correctxfml(pli0 : typing.List['PersonIdentityToken'], pli1 : typing.List['PersonIdentityToken'], attrs : typing.List['PersonAttrToken']) -> bool:
        p0 = None
        p1 = None
        for p in pli0: 
            if (p.typ == FioTemplateType.SURNAMENAMESECNAME): 
                p0 = p
                break
        for p in pli1: 
            if (p.typ == FioTemplateType.NAMESECNAMESURNAME): 
                p1 = p
                break
        if (p0 is None or p1 is None): 
            for p in pli0: 
                if (p.typ == FioTemplateType.SURNAMENAME): 
                    p0 = p
                    break
            for p in pli1: 
                if (p.typ == FioTemplateType.NAMESURNAME): 
                    p1 = p
                    break
        if (p0 is None or p1 is None): 
            return False
        if (p1.coef > p0.coef): 
            return False
        tt = p1.begin_token
        while tt != p1.end_token: 
            if (tt.is_newline_after): 
                return False
            tt = tt.next0_
        if (not p1.end_token.is_newline_after): 
            if (PersonItemToken.try_attach(p1.end_token.next0_, None, PersonItemToken.ParseAttr.NO, None) is not None): 
                return False
        if (p0.lastname is None or p1.lastname is None): 
            return False
        if (p1.lastname.has_lastname_standard_tail): 
            if (not p0.lastname.has_lastname_standard_tail): 
                p1.coef = (p0.coef + (0.1))
                return True
        if (attrs is None or len(attrs) == 0): 
            if (not p1.lastname.has_lastname_standard_tail and p0.lastname.has_lastname_standard_tail): 
                return False
        t = p1.end_token.next0_
        if (t is not None and not t.chars.is_capital_upper and not t.chars.is_all_upper): 
            npt = NounPhraseHelper.try_parse(p1.end_token, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None and npt.end_token != npt.begin_token): 
                return False
            cl1 = p0.begin_token.get_morph_class_in_dictionary()
            cl2 = p1.end_token.get_morph_class_in_dictionary()
            if (cl2.is_noun and not cl1.is_noun): 
                return False
            p1.coef = (p0.coef + (0.1))
            return True
        return False
    
    @staticmethod
    def check_latin_after(pit : 'PersonIdentityToken') -> 'PersonIdentityToken':
        if (pit is None): 
            return None
        t = pit.end_token.next0_
        if (t is None or not t.is_char('(')): 
            return None
        t = t.next0_
        p1 = PersonItemToken.try_attach_latin(t)
        if (p1 is None): 
            return None
        p2 = PersonItemToken.try_attach_latin(p1.end_token.next0_)
        if (p2 is None): 
            return None
        if (p2.end_token.next0_ is None): 
            return None
        p3 = None
        et = p2.end_token.next0_
        if (p2.end_token.next0_.is_char(')')): 
            pass
        else: 
            p3 = PersonItemToken.try_attach_latin(et)
            if (p3 is None): 
                return None
            et = p3.end_token.next0_
            if (et is None or not et.is_char(')')): 
                return None
        sur = None
        nam = None
        sec = None
        if (pit.typ == FioTemplateType.NAMESURNAME and pit.firstname is not None and pit.lastname is not None): 
            eq = 0
            if (p1.typ == PersonItemToken.ItemType.VALUE): 
                if (pit.firstname.check_latin_variant(p1.value)): 
                    eq += 1
                nam = p1
                if (p2.typ == PersonItemToken.ItemType.VALUE and p3 is None): 
                    sur = p2
                    if (pit.lastname.check_latin_variant(p2.value)): 
                        eq += 1
                elif (p2.typ == PersonItemToken.ItemType.INITIAL and p3 is not None): 
                    if (pit.lastname.check_latin_variant(p3.value)): 
                        eq += 1
                    sur = p3
            if (eq == 0): 
                return None
        elif ((pit.typ == FioTemplateType.NAMESECNAMESURNAME and pit.firstname is not None and pit.middlename is not None) and pit.lastname is not None and p3 is not None): 
            eq = 0
            if (p1.typ == PersonItemToken.ItemType.VALUE): 
                if (pit.firstname.check_latin_variant(p1.value)): 
                    eq += 1
                nam = p1
                if (p2.typ == PersonItemToken.ItemType.VALUE): 
                    sec = p2
                    if (isinstance(pit.middlename, PersonMorphCollection)): 
                        if (pit.middlename.check_latin_variant(p2.value)): 
                            eq += 1
                if (p3.typ == PersonItemToken.ItemType.VALUE): 
                    sur = p3
                    if (pit.lastname.check_latin_variant(p3.value)): 
                        eq += 1
            if (eq == 0): 
                return None
        if (nam is None or sur is None): 
            return None
        res = PersonIdentityToken._new2486(t, et, pit.typ)
        res.lastname = PersonMorphCollection()
        res.lastname.add(sur.value, None, MorphGender.UNDEFINED, False)
        res.firstname = PersonMorphCollection()
        res.firstname.add(nam.value, None, MorphGender.UNDEFINED, False)
        if (sec is not None): 
            res.middlename = (PersonMorphCollection())
            res.middlename.add(sec.value, None, MorphGender.UNDEFINED, False)
        return res
    
    @staticmethod
    def _new2486(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FioTemplateType') -> 'PersonIdentityToken':
        res = PersonIdentityToken(_arg1, _arg2)
        res.typ = _arg3
        return res