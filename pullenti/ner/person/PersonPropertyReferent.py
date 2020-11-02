# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.Referent import Referent
from pullenti.ner.person.internal.MetaPersonProperty import MetaPersonProperty

class PersonPropertyReferent(Referent):
    """ Сущность - свойство персоны (должность, звание...)
    
    """
    
    def __init__(self) -> None:
        super().__init__(PersonPropertyReferent.OBJ_TYPENAME)
        self.instance_of = MetaPersonProperty._global_meta
    
    OBJ_TYPENAME = "PERSONPROPERTY"
    """ Имя типа сущности TypeName ("PERSONPROPERTY") """
    
    ATTR_NAME = "NAME"
    """ Имя атрибута - наименование """
    
    ATTR_ATTR = "ATTR"
    """ Имя атрибута - дополнительный атрибут """
    
    ATTR_REF = "REF"
    """ Имя атрибута - ссылка на сущность (GeoReferent, PersonReferent или OrganizationReferent) """
    
    ATTR_HIGHER = "HIGHER"
    """ Имя атрибута - для составной должности ссылка на обобщающую должность """
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        if (self.name is not None): 
            print(self.name, end="", file=res)
        for r in self.slots: 
            if (r.type_name == PersonPropertyReferent.ATTR_ATTR and r.value is not None): 
                print(", {0}".format(str(r.value)), end="", file=res, flush=True)
        for r in self.slots: 
            if (r.type_name == PersonPropertyReferent.ATTR_REF and (isinstance(r.value, Referent)) and (lev < 10)): 
                print("; {0}".format(r.value.to_string(short_variant, lang, lev + 1)), end="", file=res, flush=True)
        hi = self.higher
        if (hi is not None and hi != self and self.__check_correct_higher(hi, 0)): 
            print("; {0}".format(hi.to_string(short_variant, lang, lev + 1)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def get_compare_strings(self) -> typing.List[str]:
        res = list()
        for s in self.slots: 
            if (s.type_name == PersonPropertyReferent.ATTR_NAME): 
                res.append(str(s.value))
        if (len(res) > 0): 
            return res
        else: 
            return super().get_compare_strings()
    
    @property
    def name(self) -> str:
        """ Наименование свойства """
        return self.get_string_value(PersonPropertyReferent.ATTR_NAME)
    @name.setter
    def name(self, value) -> str:
        self.add_slot(PersonPropertyReferent.ATTR_NAME, value, True, 0)
        return value
    
    @property
    def higher(self) -> 'PersonPropertyReferent':
        """ Вышестоящая должность """
        return self.__get_higher(0)
    @higher.setter
    def higher(self, value) -> 'PersonPropertyReferent':
        if (self.__check_correct_higher(value, 0)): 
            self.add_slot(PersonPropertyReferent.ATTR_HIGHER, value, True, 0)
        return value
    
    def __get_higher(self, lev : int) -> 'PersonPropertyReferent':
        hi = Utils.asObjectOrNull(self.get_slot_value(PersonPropertyReferent.ATTR_HIGHER), PersonPropertyReferent)
        if (hi is None): 
            return None
        if (not self.__check_correct_higher(hi, lev + 1)): 
            return None
        return hi
    
    def __check_correct_higher(self, hi : 'PersonPropertyReferent', lev : int) -> bool:
        if (hi is None): 
            return True
        if (hi == self): 
            return False
        if (lev > 20): 
            return False
        hii = hi.__get_higher(lev + 1)
        if (hii is None): 
            return True
        if (hii == self): 
            return False
        li = list()
        li.append(self)
        pr = hi
        while pr is not None: 
            if (pr in li): 
                return False
            else: 
                li.append(pr)
            pr = pr.__get_higher(lev + 1)
        return True
    
    @property
    def parent_referent(self) -> 'Referent':
        return self.higher
    
    __m_bosses0 = None
    
    __m_bosses1 = None
    
    __tmp_stack = 0
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType') -> bool:
        pr = Utils.asObjectOrNull(obj, PersonPropertyReferent)
        if (pr is None): 
            return False
        n1 = self.name
        n2 = pr.name
        if (n1 is None or n2 is None): 
            return False
        eq_bosses = False
        if (n1 != n2): 
            if (typ == ReferentsEqualType.DIFFERENTTEXTS): 
                return False
            if (n1 in PersonPropertyReferent.__m_bosses0 and n2 in PersonPropertyReferent.__m_bosses1): 
                eq_bosses = True
            elif (n1 in PersonPropertyReferent.__m_bosses1 and n2 in PersonPropertyReferent.__m_bosses0): 
                eq_bosses = True
            else: 
                if (not n1.startswith(n2 + " ") and not n2.startswith(n1 + " ")): 
                    return False
                eq_bosses = True
            hi = self.higher
            while hi is not None: 
                PersonPropertyReferent.__tmp_stack += 1
                if (PersonPropertyReferent.__tmp_stack > 20): 
                    pass
                elif (hi.can_be_equals(pr, typ)): 
                    PersonPropertyReferent.__tmp_stack -= 1
                    return False
                PersonPropertyReferent.__tmp_stack -= 1
                hi = hi.higher
            hi = pr.higher
            while hi is not None: 
                PersonPropertyReferent.__tmp_stack += 1
                if (PersonPropertyReferent.__tmp_stack > 20): 
                    pass
                elif (hi.can_be_equals(self, typ)): 
                    PersonPropertyReferent.__tmp_stack -= 1
                    return False
                PersonPropertyReferent.__tmp_stack -= 1
                hi = hi.higher
        if (self.higher is not None and pr.higher is not None): 
            PersonPropertyReferent.__tmp_stack += 1
            if (PersonPropertyReferent.__tmp_stack > 20): 
                pass
            elif (not self.higher.can_be_equals(pr.higher, typ)): 
                PersonPropertyReferent.__tmp_stack -= 1
                return False
            PersonPropertyReferent.__tmp_stack -= 1
        if (self.find_slot("@GENERAL", None, True) is not None or pr.find_slot("@GENERAL", None, True) is not None): 
            return str(self) == str(pr)
        if (self.find_slot(PersonPropertyReferent.ATTR_REF, None, True) is not None or pr.find_slot(PersonPropertyReferent.ATTR_REF, None, True) is not None): 
            refs1 = list()
            refs2 = list()
            for s in self.slots: 
                if (s.type_name == PersonPropertyReferent.ATTR_REF): 
                    refs1.append(s.value)
            for s in pr.slots: 
                if (s.type_name == PersonPropertyReferent.ATTR_REF): 
                    refs2.append(s.value)
            eq = False
            noeq = False
            i = 0
            first_pass3877 = True
            while True:
                if first_pass3877: first_pass3877 = False
                else: i += 1
                if (not (i < len(refs1))): break
                if (refs1[i] in refs2): 
                    eq = True
                    continue
                noeq = True
                if (isinstance(refs1[i], Referent)): 
                    for rr in refs2: 
                        if (isinstance(rr, Referent)): 
                            if (rr.can_be_equals(Utils.asObjectOrNull(refs1[i], Referent), typ)): 
                                noeq = False
                                eq = True
                                break
            i = 0
            first_pass3878 = True
            while True:
                if first_pass3878: first_pass3878 = False
                else: i += 1
                if (not (i < len(refs2))): break
                if (refs2[i] in refs1): 
                    eq = True
                    continue
                noeq = True
                if (isinstance(refs2[i], Referent)): 
                    for rr in refs1: 
                        if (isinstance(rr, Referent)): 
                            if (rr.can_be_equals(Utils.asObjectOrNull(refs2[i], Referent), typ)): 
                                noeq = False
                                eq = True
                                break
            if (eq and not noeq): 
                pass
            elif (noeq and ((eq or len(refs1) == 0 or len(refs2) == 0))): 
                if (typ == ReferentsEqualType.DIFFERENTTEXTS or n1 != n2): 
                    return False
                if (self.higher is not None or pr.higher is not None): 
                    return False
            else: 
                return False
        elif (not eq_bosses and n1 != n2): 
            return False
        return True
    
    def can_be_general_for(self, obj : 'Referent') -> bool:
        pr = Utils.asObjectOrNull(obj, PersonPropertyReferent)
        if (pr is None): 
            return False
        n1 = self.name
        n2 = pr.name
        if (n1 is None or n2 is None): 
            return False
        if (self.find_slot(PersonPropertyReferent.ATTR_REF, None, True) is not None or self.higher is not None): 
            if (n1 != n2 and n1.startswith(n2)): 
                return self.can_be_equals(obj, ReferentsEqualType.DIFFERENTTEXTS)
            return False
        if (n1 == n2): 
            if (pr.find_slot(PersonPropertyReferent.ATTR_REF, None, True) is not None or pr.higher is not None): 
                return True
            return False
        if (n2.startswith(n1)): 
            if (n2.startswith(n1 + " ")): 
                return self.can_be_equals(obj, ReferentsEqualType.WITHINONETEXT)
        return False
    
    @property
    def kind(self) -> 'PersonPropertyKind':
        """ Категория свойства """
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        return PersonAttrToken.check_kind(self)
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        oi = IntOntologyItem(self)
        for a in self.slots: 
            if (a.type_name == PersonPropertyReferent.ATTR_NAME): 
                oi.termins.append(Termin(str(a.value)))
        return oi
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        nam = self.name
        nam1 = obj.name
        super().merge_slots(obj, merge_statistic)
        if (nam != nam1 and nam1 is not None and nam is not None): 
            s = None
            if (nam.startswith(nam1)): 
                s = self.find_slot(PersonPropertyReferent.ATTR_NAME, nam1, True)
            elif (nam1.startswith(nam)): 
                s = self.find_slot(PersonPropertyReferent.ATTR_NAME, nam, True)
            elif (nam in PersonPropertyReferent.__m_bosses0 and nam1 in PersonPropertyReferent.__m_bosses1): 
                s = self.find_slot(PersonPropertyReferent.ATTR_NAME, nam, True)
            elif (nam1 in PersonPropertyReferent.__m_bosses0 and nam in PersonPropertyReferent.__m_bosses1): 
                s = self.find_slot(PersonPropertyReferent.ATTR_NAME, nam1, True)
            if (s is not None): 
                self.slots.remove(s)
    
    def can_has_ref(self, r : 'Referent') -> bool:
        # Проверка, что этот референт может выступать в качестве ATTR_REF
        nam = self.name
        if (nam is None or r is None): 
            return False
        if (isinstance(r, GeoReferent)): 
            g = Utils.asObjectOrNull(r, GeoReferent)
            if (LanguageHelper.ends_with_ex(nam, "президент", "губернатор", None, None)): 
                return g.is_state or g.is_region
            if (nam == "мэр" or nam == "градоначальник"): 
                return g.is_city
            if (nam == "глава"): 
                return True
            return False
        if (r.type_name == "ORGANIZATION"): 
            if ((LanguageHelper.ends_with(nam, "губернатор") or nam == "мэр" or nam == "градоначальник") or nam == "президент"): 
                return False
            if ("министр" in nam): 
                if (r.find_slot(None, "министерство", True) is None): 
                    return False
            if (nam.endswith("директор")): 
                if ((r.find_slot(None, "суд", True)) is not None): 
                    return False
            return True
        return False
    
    @staticmethod
    def _new2442(_arg1 : str) -> 'PersonPropertyReferent':
        res = PersonPropertyReferent()
        res.name = _arg1
        return res
    
    # static constructor for class PersonPropertyReferent
    @staticmethod
    def _static_ctor():
        PersonPropertyReferent.__m_bosses0 = list(["глава", "руководитель"])
        PersonPropertyReferent.__m_bosses1 = list(["президент", "генеральный директор", "директор", "председатель"])

PersonPropertyReferent._static_ctor()