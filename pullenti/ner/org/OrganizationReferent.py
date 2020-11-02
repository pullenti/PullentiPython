# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import math
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.org.internal.MetaOrganization import MetaOrganization
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.org.OrganizationKind import OrganizationKind

class OrganizationReferent(Referent):
    """ Сущность - организация
    
    """
    
    def __init__(self) -> None:
        super().__init__(OrganizationReferent.OBJ_TYPENAME)
        self.__m_number_calc = False
        self.__m_number = None;
        self.__m_parent = None;
        self.__m_parent_calc = False
        self.__m_name_single_normal_real = None;
        self.__m_name_vars = None;
        self.__m_name_hashs = None;
        self.__m_level = 0
        self._m_temp_parent_org = None;
        self.is_from_global_ontos = False
        self._ext_ontology_attached = False
        self.__m_kind = OrganizationKind.UNDEFINED
        self.__m_kind_calc = False
        self.instance_of = MetaOrganization._global_meta
    
    OBJ_TYPENAME = "ORGANIZATION"
    """ Имя типа сущности TypeName ("ORGANIZATION") """
    
    ATTR_NAME = "NAME"
    """ Имя атрибута - наименование """
    
    ATTR_TYPE = "TYPE"
    """ Имя атрибута - тип """
    
    ATTR_NUMBER = "NUMBER"
    """ Имя атрибута - номер """
    
    ATTR_EPONYM = "EPONYM"
    """ Имя атрибута - эпоним (имени кого) """
    
    ATTR_HIGHER = "HIGHER"
    """ Имя атрибута - вышестоящая организация (OrganizationReferent) """
    
    ATTR_OWNER = "OWNER"
    """ Имя атрибута - владелец (PersonReferent) """
    
    ATTR_GEO = "GEO"
    """ Имя атрибута - географический объект (GeoReferent) """
    
    ATTR_MISC = "MISC"
    """ Имя атрибута - разное """
    
    ATTR_PROFILE = "PROFILE"
    """ Имя атрибута - профиль (OrgProfile) """
    
    ATTR_MARKER = "MARKER"
    """ Имя атрибута - маркер """
    
    SHOW_NUMBER_ON_FIRST_POSITION = False
    """ При выводе в ToString() первым ставить номер, если есть """
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        from pullenti.ner.org.internal.OrgItemTypeToken import OrgItemTypeToken
        res = io.StringIO()
        is_dep = self.kind == OrganizationKind.DEPARTMENT
        name = None
        altname = None
        names_count = 0
        len0_ = 0
        no_type = False
        for s in self.slots: 
            if (s.type_name == OrganizationReferent.ATTR_NAME): 
                n = str(s.value)
                names_count += 1
                len0_ += len(n)
        if (names_count > 0): 
            len0_ = math.floor(len0_ / names_count)
            if (len0_ > 10): 
                len0_ -= ((math.floor(len0_ / 7)))
            cou = 0
            altcou = 0
            for s in self.slots: 
                if (s.type_name == OrganizationReferent.ATTR_NAME): 
                    n = str(s.value)
                    if (len(n) >= len0_): 
                        if (s.count > cou): 
                            name = n
                            cou = s.count
                        elif (s.count == cou): 
                            if (name is None): 
                                name = n
                            elif (len(name) < len(n)): 
                                name = n
                    elif (s.count > altcou): 
                        altname = n
                        altcou = s.count
                    elif (s.count == altcou): 
                        if (altname is None): 
                            altname = n
                        elif (len(altname) > len(n)): 
                            altname = n
        if (name is not None): 
            if (altname is not None): 
                if (altname in name.replace(" ", "")): 
                    altname = (None)
            if (altname is not None and ((len(altname) > 30 or len(altname) > (math.floor(len(name) / 2))))): 
                altname = (None)
            if (altname is None): 
                for s in self.slots: 
                    if (s.type_name == OrganizationReferent.ATTR_NAME): 
                        if (MiscHelper.can_be_equal_cyr_and_latss(name, s.value)): 
                            altname = (s.value)
                            break
        else: 
            for s in self.slots: 
                if (s.type_name == OrganizationReferent.ATTR_TYPE): 
                    nam = Utils.asObjectOrNull(s.value, str)
                    if (OrgItemTypeToken._get_kind(nam, None, self) == OrganizationKind.UNDEFINED): 
                        continue
                    if (name is None or len(nam) > len(name)): 
                        name = nam
                    no_type = True
            if (name is None): 
                for s in self.slots: 
                    if (s.type_name == OrganizationReferent.ATTR_TYPE): 
                        nam = Utils.asObjectOrNull(s.value, str)
                        if (name is None or len(nam) > len(name)): 
                            name = nam
                        no_type = True
        out_own_in_name = False
        if (name is not None): 
            print(MiscHelper.convert_first_char_upper_and_other_lower(name), end="", file=res)
            if (((not is_dep and names_count == 0 and self.higher is not None) and self.higher.higher is None and self.number is None) and len(self.eponyms) == 0): 
                out_own_in_name = True
        if (self.number is not None): 
            if (OrganizationReferent.SHOW_NUMBER_ON_FIRST_POSITION): 
                Utils.insertStringIO(res, 0, "{0} ".format(self.number))
            else: 
                print(" №{0}".format(self.number), end="", file=res, flush=True)
        fams = None
        for r in self.slots: 
            if (r.type_name == OrganizationReferent.ATTR_EPONYM and r.value is not None): 
                if (fams is None): 
                    fams = list()
                fams.append(str(r.value))
        if (fams is not None): 
            fams.sort()
            print(" имени ", end="", file=res)
            i = 0
            while i < len(fams): 
                if (i > 0 and ((i + 1) < len(fams))): 
                    print(", ", end="", file=res)
                elif (i > 0): 
                    print(" и ", end="", file=res)
                print(fams[i], end="", file=res)
                i += 1
        if (altname is not None and not is_dep): 
            print(" ({0})".format(MiscHelper.convert_first_char_upper_and_other_lower(altname)), end="", file=res, flush=True)
        if (not short_variant and self.owner is not None): 
            print("; {0}".format(self.owner.to_string(True, lang, lev + 1)), end="", file=res, flush=True)
        if (not short_variant): 
            if (not no_type and not is_dep): 
                typ = None
                for t in self.types: 
                    if (OrgItemTypeToken._get_kind(t, None, self) == OrganizationKind.UNDEFINED): 
                        continue
                    if (typ is None or len(typ) > len(t)): 
                        typ = t
                if (typ is None): 
                    for t in self.types: 
                        if (typ is None or len(typ) > len(t)): 
                            typ = t
                if (name is not None and not Utils.isNullOrEmpty(typ) and not str.isupper(typ[0])): 
                    if (typ.upper() in name.upper()): 
                        typ = (None)
                if (typ is not None): 
                    print(", {0}".format(typ), end="", file=res, flush=True)
            for ss in self.slots: 
                if (ss.type_name == OrganizationReferent.ATTR_GEO and ss.value is not None): 
                    print(", {0}".format(str(ss.value)), end="", file=res, flush=True)
        if (not short_variant): 
            if (is_dep or out_own_in_name): 
                for ss in self.slots: 
                    if (ss.type_name == OrganizationReferent.ATTR_HIGHER and (isinstance(ss.value, Referent)) and (lev < 20)): 
                        hi = Utils.asObjectOrNull(ss.value, OrganizationReferent)
                        if (hi is not None): 
                            tmp = list()
                            tmp.append(self)
                            while hi is not None: 
                                if (hi in tmp): 
                                    break
                                else: 
                                    tmp.append(hi)
                                hi = hi.higher
                            if (hi is not None): 
                                continue
                        print(';', end="", file=res)
                        print(" {0}".format(ss.value.to_string(short_variant, lang, lev + 1)), end="", file=res, flush=True)
                        break
        if (res.tell() == 0): 
            if (self.inn is not None): 
                print("ИНН: {0}".format(self.inn), end="", file=res, flush=True)
            if (self.ogrn is not None): 
                print(" ОГРН: {0}".format(self.inn), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def to_sort_string(self) -> str:
        return Utils.enumToString(self.kind) + self.to_string(True, MorphLang.UNKNOWN, 0)
    
    def get_compare_strings(self) -> typing.List[str]:
        res = list()
        for s in self.slots: 
            if (s.type_name == OrganizationReferent.ATTR_NAME or s.type_name == OrganizationReferent.ATTR_EPONYM): 
                str0_ = str(s.value)
                if (not str0_ in res): 
                    res.append(str0_)
                if (str0_.find(' ') > 0 or str0_.find('-') > 0): 
                    str0_ = str0_.replace(" ", "").replace("-", "")
                    if (not str0_ in res): 
                        res.append(str0_)
            elif (s.type_name == OrganizationReferent.ATTR_NUMBER): 
                res.append("{0} {1}".format(Utils.enumToString(self.kind), str(s.value)))
        if (len(res) == 0): 
            for s in self.slots: 
                if (s.type_name == OrganizationReferent.ATTR_TYPE): 
                    t = str(s.value)
                    if (not t in res): 
                        res.append(t)
        if (self.inn is not None): 
            res.append("ИНН:" + self.inn)
        if (self.ogrn is not None): 
            res.append("ОГРН:" + self.ogrn)
        if (len(res) > 0): 
            return res
        else: 
            return super().get_compare_strings()
    
    def _check_correction(self) -> bool:
        if (len(self.slots) < 1): 
            return False
        s = self.to_string(True, MorphLang.UNKNOWN, 0).lower()
        if ("прокуратура" in s or "штаб" in s or "кабинет" in s): 
            return True
        if (len(self.slots) == 1): 
            if (self.slots[0].type_name != OrganizationReferent.ATTR_NAME): 
                if (self.kind == OrganizationKind.GOVENMENT or self.kind == OrganizationKind.JUSTICE): 
                    return True
                return False
        if (self.find_slot(OrganizationReferent.ATTR_TYPE, None, True) is None and self.find_slot(OrganizationReferent.ATTR_NAME, None, True) is None): 
            return False
        if (s == "государственная гражданская служба" or s == "здравоохранения"): 
            return False
        if ("колония" in self.types): 
            if (self.number is None): 
                return False
        if ("конгресс" in s): 
            if (self.find_slot(OrganizationReferent.ATTR_GEO, None, True) is None): 
                return False
        nams = self.names
        if (len(nams) == 1 and len(nams[0]) == 1 and (len(self.types) < 3)): 
            return False
        if ("ВА" in nams): 
            if (self.kind == OrganizationKind.BANK): 
                return False
        return True
    
    @property
    def inn(self) -> str:
        """ Номер ИНН """
        return self.__get_misc_value("ИНН:")
    @inn.setter
    def inn(self, value) -> str:
        if (value is not None): 
            self.add_slot(OrganizationReferent.ATTR_MISC, "ИНН:" + value, False, 0)
        return value
    
    @property
    def ogrn(self) -> str:
        """ Номер ОГРН """
        return self.__get_misc_value("ОГРН")
    @ogrn.setter
    def ogrn(self, value) -> str:
        if (value is not None): 
            self.add_slot(OrganizationReferent.ATTR_MISC, "ОГРН:" + value, False, 0)
        return value
    
    def __get_misc_value(self, pref : str) -> str:
        for s in self.slots: 
            if (s.type_name == OrganizationReferent.ATTR_MISC): 
                if (isinstance(s.value, Referent)): 
                    r = Utils.asObjectOrNull(s.value, Referent)
                    if (r.type_name == "URI"): 
                        val = r.get_string_value("SCHEME")
                        if (val == pref): 
                            return r.get_string_value("VALUE")
                elif (isinstance(s.value, str)): 
                    str0_ = Utils.asObjectOrNull(s.value, str)
                    if (str0_.startswith(pref) and len(str0_) > (len(pref) + 1)): 
                        return str0_[len(pref) + 1:]
        return None
    
    __m_empty_names = None
    
    @property
    def names(self) -> typing.List[str]:
        """ Список имён организации """
        res = None
        for s in self.slots: 
            if (s.type_name == OrganizationReferent.ATTR_NAME): 
                if (res is None): 
                    res = list()
                res.append(str(s.value))
        return Utils.ifNotNull(res, OrganizationReferent.__m_empty_names)
    
    def __correct_name(self, name : str, num : int) -> str:
        num.value = 0
        if (name is None or (len(name) < 1)): 
            return None
        if (str.isdigit(name[0]) and name.find(' ') > 0): 
            wrapi2386 = RefOutArgWrapper(0)
            inoutres2387 = Utils.tryParseInt(name[0:0+name.find(' ')], wrapi2386)
            i = wrapi2386.value
            if (inoutres2387): 
                if (i > 1): 
                    num.value = i
                    name = name[name.find(' '):].strip()
        elif (str.isdigit(name[len(name) - 1])): 
            for i in range(len(name) - 1, -1, -1):
                if (not str.isdigit(name[i])): 
                    break
            else: i = -1
            if (i >= 0 and name[i] == '.'): 
                pass
            else: 
                inoutres2388 = Utils.tryParseInt(name[i + 1:], num)
                if (i > 0 and inoutres2388 and num.value > 0): 
                    if (i < 1): 
                        return None
                    name = name[0:0+i].strip()
                    if (len(name) > 0 and name[len(name) - 1] == '-'): 
                        name = name[0:0+len(name) - 1].strip()
        return self.__correct_name0(name)
    
    def __correct_name0(self, name : str) -> str:
        name = name.upper()
        if (len(name) > 2 and not str.isalnum(name[len(name) - 1]) and Utils.isWhitespace(name[len(name) - 2])): 
            name = (name[0:0+len(name) - 2] + name[len(name) - 1:])
        if (" НА СТ." in name): 
            name = name.replace(" НА СТ.", " НА СТАНЦИИ")
        return self.__correct_type(name)
    
    def __correct_type(self, name : str) -> str:
        if (name is None): 
            return None
        if (name.endswith(" полок")): 
            name = (name[0:0+len(name) - 5] + "полк")
        elif (name == "полок"): 
            name = "полк"
        tmp = io.StringIO()
        not_empty = False
        i = 0
        first_pass3846 = True
        while True:
            if first_pass3846: first_pass3846 = False
            else: i += 1
            if (not (i < len(name))): break
            ch = name[i]
            if (str.isalnum(ch)): 
                not_empty = True
            elif (ch != '&' and ch != ',' and ch != '.'): 
                ch = ' '
            if (Utils.isWhitespace(ch)): 
                if (tmp.tell() == 0): 
                    continue
                if (Utils.getCharAtStringIO(tmp, tmp.tell() - 1) != ' ' and Utils.getCharAtStringIO(tmp, tmp.tell() - 1) != '.'): 
                    print(' ', end="", file=tmp)
                continue
            is_sp_before = tmp.tell() == 0 or Utils.getCharAtStringIO(tmp, tmp.tell() - 1) == ' '
            if (ch == '&' and not is_sp_before): 
                print(' ', end="", file=tmp)
            if (((ch == ',' or ch == '.')) and is_sp_before and tmp.tell() > 0): 
                Utils.setLengthStringIO(tmp, tmp.tell() - 1)
            print(ch, end="", file=tmp)
        if (not not_empty): 
            return None
        while tmp.tell() > 0:
            ch = Utils.getCharAtStringIO(tmp, tmp.tell() - 1)
            if ((ch == ' ' or ch == ',' or ch == '.') or Utils.isWhitespace(ch)): 
                Utils.setLengthStringIO(tmp, tmp.tell() - 1)
            else: 
                break
        return Utils.toStringStringIO(tmp)
    
    def add_name(self, name : str, remove_long_gov_names : bool=True, t : 'Token'=None) -> None:
        wrapnum2389 = RefOutArgWrapper(0)
        s = self.__correct_name(name, wrapnum2389)
        num = wrapnum2389.value
        if (s is None): 
            if (num > 0 and self.number is None): 
                self.number = str(num)
            return
        if (s == "УПРАВЛЕНИЕ"): 
            pass
        i = s.find(' ')
        if (i == 2 and s[1] == 'К' and ((i + 3) < len(s))): 
            self.add_slot(OrganizationReferent.ATTR_TYPE, s[0:0+2], False, 0)
            s = s[3:].strip()
        if (self.kind == OrganizationKind.BANK or "БАНК" in s): 
            if (s.startswith("КБ ")): 
                self.add_type_str("коммерческий банк")
                s = s[3:]
            elif (s.startswith("АКБ ")): 
                self.add_type_str("акционерный коммерческий банк")
                s = s[3:]
        if (num > 0): 
            if (len(s) > 10): 
                self.number = str(num)
            else: 
                s = "{0}{1}".format(s, num)
        cou = 1
        if (t is not None and not t.chars.is_letter and BracketHelper.is_bracket(t, False)): 
            t = t.next0_
        if (((isinstance(t, TextToken)) and (s.find(' ') < 0) and len(s) > 3) and s == t.term): 
            mt = MorphologyService.process(s, t.morph.language, None)
            if (mt is not None and len(mt) == 1): 
                snorm = mt[0].get_lemma()
                if (snorm == s): 
                    if (self.__m_name_single_normal_real is None): 
                        self.__m_name_single_normal_real = s
                        for ii in range(len(self.slots) - 1, -1, -1):
                            if (self.slots[ii].type_name == OrganizationReferent.ATTR_NAME and (Utils.asObjectOrNull(self.slots[ii].value, str)) != s): 
                                mt = MorphologyService.process(Utils.asObjectOrNull(self.slots[ii].value, str), t.morph.language, None)
                                if (mt is not None and len(mt) == 1): 
                                    if (mt[0].get_lemma() == self.__m_name_single_normal_real): 
                                        cou += self.slots[ii].count
                                        del self.slots[ii]
                                        self.__m_name_vars = (None)
                                        self.__m_name_hashs = (None)
                elif (snorm == self.__m_name_single_normal_real and snorm is not None): 
                    s = snorm
        for a in self.slots: 
            if (a.type_name == OrganizationReferent.ATTR_NAME): 
                n = str(a.value)
                if (s == n): 
                    a.count = a.count + cou
                    return
            elif (a.type_name == OrganizationReferent.ATTR_TYPE): 
                n = str(a.value)
                if (Utils.compareStrings(s, n, True) == 0): 
                    return
                if (s.startswith(n + " ")): 
                    s = s[len(n) + 1:]
        self.add_slot(OrganizationReferent.ATTR_NAME, s, False, 1)
        if (LanguageHelper.ends_with(s, " ПО")): 
            s = (s[0:0+len(s) - 2] + "ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ")
            self.add_slot(OrganizationReferent.ATTR_NAME, s, False, 0)
        self._correct_data(remove_long_gov_names)
    
    def add_name_str(self, name : str, typ : 'OrgItemTypeToken', cou : int=1) -> None:
        if (typ is not None and typ.alt_typ is not None and not typ.is_not_typ): 
            self.add_type_str(typ.alt_typ)
        if (name is None): 
            if (typ.is_not_typ): 
                return
            if (typ.name is not None and Utils.compareStrings(typ.name, typ.typ, True) != 0 and ((len(typ.name) > len(typ.typ) or self.find_slot(OrganizationReferent.ATTR_NAME, None, True) is None))): 
                num = 0
                wrapnum2390 = RefOutArgWrapper(0)
                s = self.__correct_name(typ.name, wrapnum2390)
                num = wrapnum2390.value
                self.add_slot(OrganizationReferent.ATTR_NAME, s, False, cou)
                if (num > 0 and typ.is_dep and self.number is None): 
                    self.number = str(num)
            elif (typ.alt_typ is not None): 
                self.add_slot(OrganizationReferent.ATTR_NAME, self.__correct_name0(typ.alt_typ), False, cou)
        else: 
            s = self.__correct_name0(name)
            if (typ is None or typ.is_not_typ): 
                self.add_slot(OrganizationReferent.ATTR_NAME, s, False, cou)
            else: 
                self.add_slot(OrganizationReferent.ATTR_NAME, "{0} {1}".format(typ.typ.upper(), s), False, cou)
                if (typ.name is not None): 
                    num = 0
                    wrapnum2391 = RefOutArgWrapper(0)
                    ss = self.__correct_name(typ.name, wrapnum2391)
                    num = wrapnum2391.value
                    if (ss is not None): 
                        self.add_type_str(ss)
                        self.add_slot(OrganizationReferent.ATTR_NAME, "{0} {1}".format(ss, s), False, cou)
                        if (num > 0 and typ.is_dep and self.number is None): 
                            self.number = str(num)
            if (LanguageHelper.ends_with_ex(name, " ОБЛАСТИ", " РАЙОНА", " КРАЯ", " РЕСПУБЛИКИ")): 
                ii = name.rfind(' ')
                self.add_name_str(name[0:0+ii], typ, cou)
        self._correct_data(True)
    
    @property
    def profiles(self) -> typing.List['OrgProfile']:
        """ Профиль деятельности (список OrgProfile) """
        res = list()
        for s in self.slots: 
            if (s.type_name == OrganizationReferent.ATTR_PROFILE): 
                try: 
                    str0_ = Utils.asObjectOrNull(s.value, str)
                    if (str0_ == "Politics"): 
                        str0_ = "Policy"
                    elif (str0_ == "PartOf"): 
                        str0_ = "Unit"
                    v = Utils.valToEnum(str0_, OrgProfile)
                    res.append(v)
                except Exception as ex2392: 
                    pass
        return res
    
    def add_profile(self, prof : 'OrgProfile') -> None:
        if (prof != OrgProfile.UNDEFINED): 
            self.add_slot(OrganizationReferent.ATTR_PROFILE, Utils.enumToString(prof), False, 0)
    
    def contains_profile(self, prof : 'OrgProfile') -> bool:
        return self.find_slot(OrganizationReferent.ATTR_PROFILE, Utils.enumToString(prof), True) is not None
    
    @property
    def types(self) -> typing.List[str]:
        """ Список типов и префиксов организации (ЗАО, компания, институт ...) """
        res = list()
        for s in self.slots: 
            if (s.type_name == OrganizationReferent.ATTR_TYPE): 
                res.append(str(s.value))
        return res
    
    def _types_contains(self, substr : str) -> bool:
        for s in self.slots: 
            if (s.type_name == OrganizationReferent.ATTR_TYPE): 
                val = Utils.asObjectOrNull(s.value, str)
                if (val is not None and substr in val): 
                    return True
        return False
    
    def add_type(self, typ : 'OrgItemTypeToken', final_add : bool=False) -> None:
        from pullenti.ner.org.internal.OrgItemTypeToken import OrgItemTypeToken
        if (typ is None): 
            return
        for p in typ.profiles: 
            self.add_profile(p)
        if (typ.is_not_typ): 
            return
        tt = typ.begin_token
        while tt is not None and tt.end_char <= typ.end_char: 
            tok = OrgItemTypeToken._m_markers.try_parse(tt, TerminParseAttr.NO)
            if (tok is not None): 
                self.add_slot(OrganizationReferent.ATTR_MARKER, tok.termin.canonic_text, False, 0)
            tt = tt.next0_
        if (typ.typ == "следственный комитет"): 
            self.add_type_str("комитет")
            self.add_name(typ.typ, True, None)
        else: 
            self.add_type_str(typ.typ)
            if (typ.number is not None): 
                self.number = typ.number
            if (typ.typ == "АКБ"): 
                self.add_type_str("банк")
            if (typ.name is not None and typ.name != "ПОЛОК"): 
                if (typ.name_is_name): 
                    self.add_name(typ.name, True, None)
                elif (typ.typ == "министерство" and Utils.startsWithString(typ.name, typ.typ + " ", True)): 
                    self.add_name(typ.name, True, None)
                elif (typ.typ.endswith("электростанция") and Utils.endsWithString(typ.name, " " + typ.typ, True)): 
                    self.add_name(typ.name, True, None)
                elif (self.find_slot(OrganizationReferent.ATTR_NAME, None, True) is not None and self.find_slot(OrganizationReferent.ATTR_NAME, typ.name, True) is None): 
                    self.add_type_str(typ.name.lower())
                elif (final_add): 
                    ss = typ.name.lower()
                    if (LanguageHelper.is_latin(ss) and ss.endswith(" " + typ.typ)): 
                        if (typ.root is not None and ((typ.root.can_has_latin_name or typ.root.can_has_single_name)) and not typ.root.must_be_partof_name): 
                            sl = self.find_slot(OrganizationReferent.ATTR_NAME, typ.name, True)
                            if (sl is not None): 
                                self.slots.remove(sl)
                            self.add_name(ss[0:0+len(ss) - len(typ.typ) - 1].upper(), True, None)
                            self.add_name(ss.upper(), True, None)
                            ss = (None)
                    if (ss is not None): 
                        self.add_type_str(ss)
                if (typ.alt_name is not None): 
                    self.add_name(typ.alt_name, True, None)
        if (typ.alt_typ is not None): 
            self.add_type_str(typ.alt_typ)
        if (typ.number is not None): 
            self.number = typ.number
        if (typ.root is not None): 
            if (typ.root.acronym is not None): 
                if (self.find_slot(OrganizationReferent.ATTR_TYPE, typ.root.acronym, True) is None): 
                    self.add_slot(OrganizationReferent.ATTR_TYPE, typ.root.acronym, False, 0)
            if (typ.root.canonic_text is not None and typ.root.canonic_text != "СБЕРЕГАТЕЛЬНЫЙ БАНК" and typ.root.canonic_text != typ.root.acronym): 
                self.add_type_str(typ.root.canonic_text.lower())
        if (typ.geo is not None): 
            if ((isinstance(typ.geo.referent, GeoReferent)) and typ.geo.referent.is_region and self.kind == OrganizationKind.STUDY): 
                pass
            else: 
                self._add_geo_object(typ.geo)
        if (typ.geo2 is not None): 
            self._add_geo_object(typ.geo2)
        if (final_add): 
            if (self.kind == OrganizationKind.BANK): 
                self.add_slot(OrganizationReferent.ATTR_TYPE, "банк", False, 0)
    
    def add_type_str(self, typ : str) -> None:
        if (typ is None): 
            return
        typ = self.__correct_type(typ)
        if (typ is None): 
            return
        ok = True
        for n in self.names: 
            if (Utils.startsWithString(n, typ, True)): 
                ok = False
                break
        if (not ok): 
            return
        self.add_slot(OrganizationReferent.ATTR_TYPE, typ, False, 0)
        self._correct_data(True)
    
    def __get_sorted_types(self, for_ontos : bool) -> typing.List[str]:
        res = list(self.types)
        res.sort()
        i = 0
        first_pass3847 = True
        while True:
            if first_pass3847: first_pass3847 = False
            else: i += 1
            if (not (i < len(res))): break
            if (str.islower(res[i][0])): 
                into = False
                for r in res: 
                    if (r != res[i] and res[i] in r): 
                        into = True
                        break
                if (not into and not for_ontos): 
                    v = res[i].upper()
                    for n in self.names: 
                        if (v in n): 
                            into = True
                            break
                if (into): 
                    del res[i]
                    i -= 1
                    continue
        return res
    
    @property
    def number(self) -> str:
        """ Номер (если есть) """
        if (not self.__m_number_calc): 
            self.__m_number = self.get_string_value(OrganizationReferent.ATTR_NUMBER)
            self.__m_number_calc = True
        return self.__m_number
    @number.setter
    def number(self, value) -> str:
        self.add_slot(OrganizationReferent.ATTR_NUMBER, value, True, 0)
        return value
    
    @property
    def owner(self) -> 'Referent':
        """ Типа владелец - (Аппарат Президента) """
        return Utils.asObjectOrNull(self.get_slot_value(OrganizationReferent.ATTR_OWNER), Referent)
    @owner.setter
    def owner(self, value) -> 'Referent':
        self.add_slot(OrganizationReferent.ATTR_OWNER, Utils.asObjectOrNull(value, Referent), True, 0)
        return value
    
    @property
    def higher(self) -> 'OrganizationReferent':
        """ Вышестоящая организация """
        if (self.__m_parent_calc): 
            return self.__m_parent
        self.__m_parent_calc = True
        self.__m_parent = (Utils.asObjectOrNull(self.get_slot_value(OrganizationReferent.ATTR_HIGHER), OrganizationReferent))
        if (self.__m_parent == self or self.__m_parent is None): 
            self.__m_parent = None
            return self.__m_parent
        sl = self.__m_parent.find_slot(OrganizationReferent.ATTR_HIGHER, None, True)
        if (sl is None): 
            return self.__m_parent
        li = list()
        li.append(self)
        li.append(self.__m_parent)
        oo = Utils.asObjectOrNull(sl.value, OrganizationReferent)
        while oo is not None: 
            if (oo in li): 
                self.__m_parent = None
                return self.__m_parent
            li.append(oo)
            oo = (Utils.asObjectOrNull(oo.get_slot_value(OrganizationReferent.ATTR_HIGHER), OrganizationReferent))
        return self.__m_parent
    @higher.setter
    def higher(self, value) -> 'OrganizationReferent':
        if (value is not None): 
            d = value
            li = list()
            while d is not None: 
                if (d == self): 
                    return value
                elif (str(d) == str(self)): 
                    return value
                if (d in li): 
                    return value
                li.append(d)
                d = d.higher
        self.add_slot(OrganizationReferent.ATTR_HIGHER, None, True, 0)
        if (value is not None): 
            self.add_slot(OrganizationReferent.ATTR_HIGHER, value, True, 0)
        self.__m_parent_calc = False
        return value
    
    @property
    def parent_referent(self) -> 'Referent':
        hi = self.higher
        if (hi is not None): 
            return hi
        return self.owner
    
    __m_empry_eponyms = None
    
    @property
    def eponyms(self) -> typing.List[str]:
        """ Список объектов, которым посвящена организации (имени кого) """
        res = None
        for s in self.slots: 
            if (s.type_name == OrganizationReferent.ATTR_EPONYM): 
                if (res is None): 
                    res = list()
                res.append(str(s.value))
        return Utils.ifNotNull(res, OrganizationReferent.__m_empry_eponyms)
    
    def add_eponym(self, rod_padez_surname : str) -> None:
        if (rod_padez_surname is None): 
            return
        rod_padez_surname = MiscHelper.convert_first_char_upper_and_other_lower(rod_padez_surname)
        if (self.find_slot(OrganizationReferent.ATTR_EPONYM, rod_padez_surname, True) is None): 
            self.add_slot(OrganizationReferent.ATTR_EPONYM, rod_padez_surname, False, 0)
    
    __m_empty_geos = None
    
    @property
    def geo_objects(self) -> typing.List['GeoReferent']:
        """ Список географических объектов (GeoReferent) """
        res = None
        for s in self.slots: 
            if (s.type_name == OrganizationReferent.ATTR_GEO and (isinstance(s.value, GeoReferent))): 
                if (res is None): 
                    res = list()
                res.append(Utils.asObjectOrNull(s.value, GeoReferent))
        return Utils.ifNotNull(res, OrganizationReferent.__m_empty_geos)
    
    def _add_geo_object(self, r : object) -> bool:
        if (isinstance(r, GeoReferent)): 
            geo_ = Utils.asObjectOrNull(r, GeoReferent)
            for s in self.slots: 
                if (s.type_name == OrganizationReferent.ATTR_GEO and (isinstance(s.value, GeoReferent))): 
                    gg = Utils.asObjectOrNull(s.value, GeoReferent)
                    if (gg.can_be_equals(geo_, ReferentsEqualType.WITHINONETEXT) or gg.higher == geo_): 
                        return True
                    if (self.find_slot(OrganizationReferent.ATTR_TYPE, "посольство", True) is not None): 
                        break
                    if (geo_.is_state != gg.is_state): 
                        if (gg.is_state): 
                            if (self.kind == OrganizationKind.GOVENMENT): 
                                return False
                            if (not geo_.is_city): 
                                return False
                    if (geo_.is_city == gg.is_city): 
                        sovm = False
                        for t in self.types: 
                            if ("совместн" in t or "альянс" in t): 
                                sovm = True
                        if (not sovm): 
                            return False
                    if (geo_.higher == gg): 
                        self.upload_slot(s, geo_)
                        return True
            self.add_slot(OrganizationReferent.ATTR_GEO, r, False, 0)
            return True
        elif (isinstance(r, ReferentToken)): 
            if (isinstance(r.get_referent(), GeoReferent)): 
                if (not self._add_geo_object(r.get_referent())): 
                    return False
                self.add_ext_referent(Utils.asObjectOrNull(r, ReferentToken))
                return True
            if (isinstance(r.get_referent(), AddressReferent)): 
                return self._add_geo_object(r.begin_token.get_referent())
        return False
    
    @property
    def _name_vars(self) -> typing.List[tuple]:
        if (self.__m_name_vars is not None): 
            return self.__m_name_vars
        self.__m_name_vars = dict()
        self.__m_name_hashs = list()
        name_abbr = None
        ki = self.kind
        for n in self.names: 
            if (not n in self.__m_name_vars): 
                self.__m_name_vars[n] = False
        for n in self.names: 
            if (ki == OrganizationKind.BANK): 
                if (not "БАНК" in n): 
                    a = (n + "БАНК")
                    if (not a in self.__m_name_vars): 
                        self.__m_name_vars[a] = False
            a = MiscHelper.get_abbreviation(n)
            if ((a) is not None and len(a) > 1): 
                if (not a in self.__m_name_vars): 
                    self.__m_name_vars[a] = True
                if (name_abbr is None): 
                    name_abbr = list()
                if (not a in name_abbr): 
                    name_abbr.append(a)
                for geo_ in self.geo_objects: 
                    aa = "{0}{1}".format(a, geo_.to_string(True, MorphLang.UNKNOWN, 0)[0])
                    if (not aa in self.__m_name_vars): 
                        self.__m_name_vars[aa] = True
                    if (not aa in name_abbr): 
                        name_abbr.append(aa)
            a = MiscHelper.get_tail_abbreviation(n)
            if ((a) is not None): 
                if (not a in self.__m_name_vars): 
                    self.__m_name_vars[a] = True
            i = n.find(' ')
            if (i > 0 and (Utils.indexOfList(n, ' ', i + 1) < 0)): 
                a = n.replace(" ", "")
                if (not a in self.__m_name_vars): 
                    self.__m_name_vars[a] = False
        for e0_ in self.eponyms: 
            for ty in self.types: 
                na = "{0} {1}".format(ty, e0_).upper()
                if (not na in self.__m_name_vars): 
                    self.__m_name_vars[na] = False
        new_vars = list()
        for n in self.types: 
            a = MiscHelper.get_abbreviation(n)
            if (a is None): 
                continue
            for v in self.__m_name_vars.keys(): 
                if (not v.startswith(a)): 
                    new_vars.append(a + v)
                    new_vars.append(a + " " + v)
        for v in new_vars: 
            if (not v in self.__m_name_vars): 
                self.__m_name_vars[v] = True
        for kp in self.__m_name_vars.items(): 
            if (not kp[1]): 
                s = MiscHelper.get_absolute_normal_value(kp[0], False)
                if (s is not None and len(s) > 4): 
                    if (not s in self.__m_name_hashs): 
                        self.__m_name_hashs.append(s)
        return self.__m_name_vars
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType') -> bool:
        ret = self.can_be_equals_ex(obj, False, typ)
        return ret
    
    def can_be_general_for(self, obj : 'Referent') -> bool:
        if (self.__m_level > 10): 
            return False
        self.__m_level += 1
        b = self.can_be_equals_ex(obj, True, ReferentsEqualType.DIFFERENTTEXTS)
        self.__m_level -= 1
        if (not b): 
            return False
        geos1 = self.geo_objects
        geos2 = obj.geo_objects
        if (len(geos1) == 0 and len(geos2) > 0): 
            if (self.__check_eq_eponyms(Utils.asObjectOrNull(obj, OrganizationReferent))): 
                return False
            return True
        elif (len(geos1) == len(geos2)): 
            if (self.__check_eq_eponyms(Utils.asObjectOrNull(obj, OrganizationReferent))): 
                return False
            if (self.higher is not None and obj.higher is not None): 
                self.__m_level += 1
                b = self.higher.can_be_general_for(obj.higher)
                self.__m_level -= 1
                if (b): 
                    return True
        return False
    
    def __check_eq_eponyms(self, org0_ : 'OrganizationReferent') -> bool:
        if (self.find_slot(OrganizationReferent.ATTR_EPONYM, None, True) is None and org0_.find_slot(OrganizationReferent.ATTR_EPONYM, None, True) is None): 
            return False
        eps = self.eponyms
        eps1 = org0_.eponyms
        for e0_ in eps: 
            if (e0_ in eps1): 
                return True
            if (not LanguageHelper.ends_with(e0_, "а")): 
                if (e0_ + "а" in eps1): 
                    return True
        for e0_ in eps1: 
            if (e0_ in eps): 
                return True
            if (not LanguageHelper.ends_with(e0_, "а")): 
                if (e0_ + "а" in eps): 
                    return True
        if (self.find_slot(OrganizationReferent.ATTR_EPONYM, None, True) is not None and org0_.find_slot(OrganizationReferent.ATTR_EPONYM, None, True) is not None): 
            return False
        s = org0_.to_string(True, MorphLang.UNKNOWN, 0)
        for e0_ in self.eponyms: 
            if (e0_ in s): 
                return True
        s = self.to_string(True, MorphLang.UNKNOWN, 0)
        for e0_ in org0_.eponyms: 
            if (e0_ in s): 
                return True
        return False
    
    def can_be_equals_ex(self, obj : 'Referent', ignore_geo_objects : bool, typ : 'ReferentsEqualType') -> bool:
        if (self.__m_level > 10): 
            return False
        self.__m_level += 1
        ret = self.__can_be_equals(obj, ignore_geo_objects, typ, 0)
        self.__m_level -= 1
        if (not ret): 
            pass
        return ret
    
    def __can_be_equals(self, obj : 'Referent', ignore_geo_objects : bool, typ : 'ReferentsEqualType', lev : int) -> bool:
        from pullenti.ner.org.internal.OrgItemTypeToken import OrgItemTypeToken
        org0_ = Utils.asObjectOrNull(obj, OrganizationReferent)
        if (org0_ is None): 
            return False
        if (org0_ == self): 
            return True
        if (lev > 4): 
            return False
        empty = True
        geo_not_equals = False
        k1 = self.kind
        k2 = org0_.kind
        geos1 = self.geo_objects
        geos2 = org0_.geo_objects
        if (len(geos1) > 0 and len(geos2) > 0): 
            geo_not_equals = True
            for g1 in geos1: 
                eq = False
                for g2 in geos2: 
                    if (g1.can_be_equals(g2, typ)): 
                        geo_not_equals = False
                        eq = True
                        break
                if (not eq): 
                    return False
            if (len(geos2) > len(geos1)): 
                for g1 in geos2: 
                    eq = False
                    for g2 in geos1: 
                        if (g1.can_be_equals(g2, typ)): 
                            geo_not_equals = False
                            eq = True
                            break
                    if (not eq): 
                        return False
        if (self.find_slot(OrganizationReferent.ATTR_MARKER, None, True) is not None and org0_.find_slot(OrganizationReferent.ATTR_MARKER, None, True) is not None): 
            mrks1 = self.get_string_values(OrganizationReferent.ATTR_MARKER)
            mrks2 = obj.get_string_values(OrganizationReferent.ATTR_MARKER)
            for m in mrks1: 
                if (not m in mrks2): 
                    return False
            for m in mrks2: 
                if (not m in mrks1): 
                    return False
        inn_ = self.inn
        inn2 = org0_.inn
        if (inn_ is not None and inn2 is not None): 
            return inn_ == inn2
        ogrn_ = self.ogrn
        ogrn2 = org0_.ogrn
        if (ogrn_ is not None and ogrn2 is not None): 
            return ogrn_ == ogrn2
        hi1 = Utils.ifNotNull(self.higher, self._m_temp_parent_org)
        hi2 = Utils.ifNotNull(org0_.higher, org0_._m_temp_parent_org)
        hi_eq = False
        if (hi1 is not None and hi2 is not None): 
            if (org0_.find_slot(OrganizationReferent.ATTR_HIGHER, hi1, False) is None): 
                if (hi1.__can_be_equals(hi2, ignore_geo_objects, typ, lev + 1)): 
                    pass
                else: 
                    return False
            hi_eq = True
        if (self.owner is not None or org0_.owner is not None): 
            if (self.owner is None or org0_.owner is None): 
                return False
            if (not self.owner.can_be_equals(org0_.owner, typ)): 
                return False
            if (self.find_slot(OrganizationReferent.ATTR_TYPE, "индивидуальное предприятие", True) is not None or org0_.find_slot(OrganizationReferent.ATTR_TYPE, "индивидуальное предприятие", True) is not None): 
                return True
            hi_eq = True
        if (typ == ReferentsEqualType.DIFFERENTTEXTS and not hi_eq): 
            if (self.higher is not None or org0_.higher is not None): 
                return False
        if (OrgItemTypeToken.is_types_antagonisticoo(self, org0_)): 
            return False
        if (typ == ReferentsEqualType.DIFFERENTTEXTS): 
            if (k1 == OrganizationKind.DEPARTMENT or k2 == OrganizationKind.DEPARTMENT): 
                if (hi1 is None and hi2 is not None): 
                    return False
                if (hi1 is not None and hi2 is None): 
                    return False
            elif (k1 != k2): 
                return False
        eq_eponyms = self.__check_eq_eponyms(org0_)
        eq_number = False
        if (self.number is not None or org0_.number is not None): 
            if (org0_.number != self.number): 
                if (((org0_.number is None or self.number is None)) and eq_eponyms): 
                    pass
                elif (typ == ReferentsEqualType.FORMERGING and ((org0_.number is None or self.number is None))): 
                    pass
                else: 
                    return False
            else: 
                empty = False
                for a in self.slots: 
                    if (a.type_name == OrganizationReferent.ATTR_TYPE): 
                        if (obj.find_slot(a.type_name, a.value, True) is not None or obj.find_slot(OrganizationReferent.ATTR_NAME, a.value.upper(), True) is not None): 
                            eq_number = True
                            break
        if (typ == ReferentsEqualType.DIFFERENTTEXTS): 
            if (self.number is not None or org0_.number is not None): 
                if (not eq_number and not eq_eponyms): 
                    return False
        if (k1 != OrganizationKind.UNDEFINED and k2 != OrganizationKind.UNDEFINED): 
            if (k1 != k2): 
                oo = False
                for ty1 in self.types: 
                    if (ty1 in org0_.types): 
                        oo = True
                        break
                if (not oo): 
                    has_pr = False
                    for p in self.profiles: 
                        if (org0_.contains_profile(p)): 
                            has_pr = True
                            break
                    if (not has_pr): 
                        return False
        else: 
            if (k1 == OrganizationKind.UNDEFINED): 
                k1 = k2
            if ((k1 == OrganizationKind.BANK or k1 == OrganizationKind.MEDICAL or k1 == OrganizationKind.PARTY) or k1 == OrganizationKind.CULTURE): 
                if (len(self.types) > 0 and len(org0_.types) > 0): 
                    if (typ != ReferentsEqualType.FORMERGING): 
                        return False
                    ok = False
                    for s in self.slots: 
                        if (s.type_name == OrganizationReferent.ATTR_NAME): 
                            if (org0_.find_slot(s.type_name, s.value, True) is not None): 
                                ok = True
                    if (not ok): 
                        return False
        if ((k1 == OrganizationKind.GOVENMENT or k2 == OrganizationKind.GOVENMENT or k1 == OrganizationKind.MILITARY) or k2 == OrganizationKind.MILITARY): 
            typs = org0_.types
            ok = False
            for ty in self.types: 
                if (ty in typs): 
                    ok = True
                    break
            if (not ok): 
                return False
        if (typ == ReferentsEqualType.FORMERGING): 
            pass
        elif (self.find_slot(OrganizationReferent.ATTR_NAME, None, True) is not None or org0_.find_slot(OrganizationReferent.ATTR_NAME, None, True) is not None): 
            if (((eq_number or eq_eponyms)) and ((self.find_slot(OrganizationReferent.ATTR_NAME, None, True) is None or org0_.find_slot(OrganizationReferent.ATTR_NAME, None, True) is None))): 
                pass
            else: 
                empty = False
                max_len = 0
                for v in self._name_vars.items(): 
                    if (typ == ReferentsEqualType.DIFFERENTTEXTS and v[1]): 
                        continue
                    wrapb2393 = RefOutArgWrapper(False)
                    inoutres2394 = Utils.tryGetValue(org0_._name_vars, v[0], wrapb2393)
                    b = wrapb2393.value
                    if (not inoutres2394): 
                        continue
                    if (typ == ReferentsEqualType.DIFFERENTTEXTS and b): 
                        continue
                    if (b and v[1]): 
                        continue
                    if (b and len(self.names) > 1 and (len(v[0]) < 4)): 
                        continue
                    if (v[1] and len(org0_.names) > 1 and (len(v[0]) < 4)): 
                        continue
                    if (len(v[0]) > max_len): 
                        max_len = len(v[0])
                if (typ != ReferentsEqualType.DIFFERENTTEXTS): 
                    for v in self.__m_name_hashs: 
                        if (v in org0_.__m_name_hashs): 
                            if (len(v) > max_len): 
                                max_len = len(v)
                if ((max_len < 2) and ((k1 == OrganizationKind.GOVENMENT or typ == ReferentsEqualType.FORMERGING)) and typ != ReferentsEqualType.DIFFERENTTEXTS): 
                    if (len(geos1) == len(geos2)): 
                        nams = (org0_._name_vars.keys() if typ == ReferentsEqualType.FORMERGING else org0_.names)
                        nams0 = (self._name_vars.keys() if typ == ReferentsEqualType.FORMERGING else self.names)
                        for n in nams0: 
                            for nn in nams: 
                                if (n.startswith(nn)): 
                                    max_len = len(nn)
                                    break
                                elif (nn.startswith(n)): 
                                    max_len = len(n)
                                    break
                if (max_len < 2): 
                    return False
                if (max_len < 4): 
                    ok = False
                    if (not ok): 
                        if (len(self.names) == 1 and (len(self.names[0]) < 4)): 
                            ok = True
                        elif (len(org0_.names) == 1 and (len(org0_.names[0]) < 4)): 
                            ok = True
                    if (not ok): 
                        return False
        if (eq_eponyms): 
            return True
        if (self.find_slot(OrganizationReferent.ATTR_EPONYM, None, True) is not None or obj.find_slot(OrganizationReferent.ATTR_EPONYM, None, True) is not None): 
            if (typ == ReferentsEqualType.FORMERGING and ((self.find_slot(OrganizationReferent.ATTR_EPONYM, None, True) is None or obj.find_slot(OrganizationReferent.ATTR_EPONYM, None, True) is None))): 
                pass
            else: 
                ok = False
                eps = self.eponyms
                eps1 = org0_.eponyms
                for e0_ in eps: 
                    if (e0_ in eps1): 
                        ok = True
                        break
                    if (not LanguageHelper.ends_with(e0_, "а")): 
                        if (e0_ + "а" in eps1): 
                            ok = True
                            break
                if (not ok): 
                    for e0_ in eps1: 
                        if (e0_ in eps): 
                            ok = True
                            break
                        if (not LanguageHelper.ends_with(e0_, "а")): 
                            if (e0_ + "а" in eps): 
                                ok = True
                                break
                if (ok): 
                    return True
                if (self.find_slot(OrganizationReferent.ATTR_EPONYM, None, True) is None or obj.find_slot(OrganizationReferent.ATTR_EPONYM, None, True) is None): 
                    s = obj.to_string(True, MorphLang.UNKNOWN, 0)
                    for e0_ in self.eponyms: 
                        if (e0_ in s): 
                            ok = True
                            break
                    if (not ok): 
                        s = self.to_string(True, MorphLang.UNKNOWN, 0)
                        for e0_ in org0_.eponyms: 
                            if (e0_ in s): 
                                ok = True
                                break
                    if (ok): 
                        return True
                    elif (empty): 
                        return False
                else: 
                    return False
        if (geo_not_equals): 
            if (k1 == OrganizationKind.BANK or k1 == OrganizationKind.GOVENMENT or k1 == OrganizationKind.DEPARTMENT): 
                return False
        if (k1 != OrganizationKind.DEPARTMENT): 
            if (not empty): 
                return True
            if (hi_eq): 
                typs = org0_.types
                for ty in self.types: 
                    if (ty in typs): 
                        return True
        if (typ == ReferentsEqualType.DIFFERENTTEXTS): 
            return str(self) == str(org0_)
        if (empty): 
            if (((len(geos1) > 0 and len(geos2) > 0)) or k1 == OrganizationKind.DEPARTMENT or k1 == OrganizationKind.JUSTICE): 
                typs = org0_.types
                for ty in self.types: 
                    if (ty in typs): 
                        return True
            full_not_eq = False
            for s in self.slots: 
                if (org0_.find_slot(s.type_name, s.value, True) is None): 
                    full_not_eq = True
                    break
            for s in org0_.slots: 
                if (self.find_slot(s.type_name, s.value, True) is None): 
                    full_not_eq = True
                    break
            if (not full_not_eq): 
                return True
        elif (k1 == OrganizationKind.DEPARTMENT): 
            return True
        if (typ == ReferentsEqualType.FORMERGING): 
            return True
        return False
    
    def add_slot(self, attr_name : str, attr_value : object, clear_old_value : bool, stat_count : int=0) -> 'Slot':
        if (attr_name == OrganizationReferent.ATTR_NAME or attr_name == OrganizationReferent.ATTR_TYPE): 
            self.__m_name_vars = (None)
            self.__m_name_hashs = (None)
        elif (attr_name == OrganizationReferent.ATTR_HIGHER): 
            self.__m_parent_calc = False
        elif (attr_name == OrganizationReferent.ATTR_NUMBER): 
            self.__m_number_calc = False
        self.__m_kind_calc = False
        sl = super().add_slot(attr_name, attr_value, clear_old_value, stat_count)
        return sl
    
    def upload_slot(self, slot : 'Slot', new_val : object) -> None:
        self.__m_parent_calc = False
        super().upload_slot(slot, new_val)
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool) -> None:
        own_this = self.higher
        own_obj = obj.higher
        super().merge_slots(obj, merge_statistic)
        for i in range(len(self.slots) - 1, -1, -1):
            if (self.slots[i].type_name == OrganizationReferent.ATTR_HIGHER): 
                del self.slots[i]
        if (own_this is None): 
            own_this = own_obj
        if (own_this is not None): 
            self.higher = own_this
        if (obj.is_from_global_ontos): 
            self.is_from_global_ontos = True
        self._correct_data(True)
    
    def _correct_data(self, remove_long_gov_names : bool) -> None:
        for i in range(len(self.slots) - 1, -1, -1):
            if (self.slots[i].type_name == OrganizationReferent.ATTR_TYPE): 
                ty = str(self.slots[i]).upper()
                del0_ = False
                for s in self.slots: 
                    if (s.type_name == OrganizationReferent.ATTR_NAME): 
                        na = str(s.value)
                        if (LanguageHelper.ends_with(ty, na)): 
                            del0_ = True
                if (del0_): 
                    del self.slots[i]
        for t in self.types: 
            n = self.find_slot(OrganizationReferent.ATTR_NAME, t.upper(), True)
            if (n is not None): 
                self.slots.remove(n)
        for t in self.names: 
            if (t.find('.') > 0): 
                n = self.find_slot(OrganizationReferent.ATTR_NAME, t.replace('.', ' '), True)
                if (n is None): 
                    self.add_slot(OrganizationReferent.ATTR_NAME, t.replace('.', ' '), False, 0)
        eps = self.eponyms
        if (len(eps) > 1): 
            for e0_ in eps: 
                for ee in eps: 
                    if (e0_ != ee and e0_.startswith(ee)): 
                        s = self.find_slot(OrganizationReferent.ATTR_EPONYM, ee, True)
                        if (s is not None): 
                            self.slots.remove(s)
        typs = self.types
        epons = self.eponyms
        for t in typs: 
            for e0_ in epons: 
                n = self.find_slot(OrganizationReferent.ATTR_NAME, "{0} {1}".format(t.upper(), e0_.upper()), True)
                if (n is not None): 
                    self.slots.remove(n)
        if (remove_long_gov_names and self.kind == OrganizationKind.GOVENMENT): 
            nams = self.names
            for i in range(len(self.slots) - 1, -1, -1):
                if (self.slots[i].type_name == OrganizationReferent.ATTR_NAME): 
                    n = str(self.slots[i].value)
                    for nn in nams: 
                        if (n.startswith(nn) and len(n) > len(nn)): 
                            del self.slots[i]
                            break
        if ("фронт" in self.types): 
            uni = False
            for ty in self.types: 
                if ("объединение" in ty): 
                    uni = True
            if (uni or OrgProfile.UNION in self.profiles): 
                ss = self.find_slot(OrganizationReferent.ATTR_PROFILE, "ARMY", True)
                if (ss is not None): 
                    self.slots.remove(ss)
                    self.add_profile(OrgProfile.UNION)
                ss = self.find_slot(OrganizationReferent.ATTR_TYPE, "фронт", True)
                if ((ss) is not None): 
                    self.slots.remove(ss)
        self.__m_name_vars = (None)
        self.__m_name_hashs = (None)
        self.__m_kind_calc = False
        self._ext_ontology_attached = False
    
    def _final_correction(self) -> None:
        typs = self.types
        if (self.contains_profile(OrgProfile.EDUCATION) and self.contains_profile(OrgProfile.SCIENCE)): 
            if ("академия" in typs or "академія" in typs or "academy" in typs): 
                is_sci = False
                for n in self.names: 
                    if ("НАУЧН" in n or "НАУК" in n or "SCIENC" in n): 
                        is_sci = True
                        break
                s = None
                if (is_sci): 
                    s = self.find_slot(OrganizationReferent.ATTR_PROFILE, Utils.enumToString(OrgProfile.EDUCATION), True)
                else: 
                    s = self.find_slot(OrganizationReferent.ATTR_PROFILE, Utils.enumToString(OrgProfile.SCIENCE), True)
                if (s is not None): 
                    self.slots.remove(s)
        if (self.find_slot(OrganizationReferent.ATTR_PROFILE, None, True) is None): 
            if ("служба" in typs and self.higher is not None): 
                self.add_profile(OrgProfile.UNIT)
        if (len(typs) > 0 and LanguageHelper.is_latin(typs[0])): 
            if (self.find_slot(OrganizationReferent.ATTR_NAME, None, True) is None and len(typs) > 1): 
                nam = typs[0]
                for v in typs: 
                    if (len(v) > len(nam)): 
                        nam = v
                if (nam.find(' ') > 0): 
                    self.add_slot(OrganizationReferent.ATTR_NAME, nam.upper(), False, 0)
                    s = self.find_slot(OrganizationReferent.ATTR_TYPE, nam, True)
                    if (s is not None): 
                        self.slots.remove(s)
            if ((self.find_slot(OrganizationReferent.ATTR_NAME, None, True) is None and self.find_slot(OrganizationReferent.ATTR_GEO, None, True) is not None and self.find_slot(OrganizationReferent.ATTR_NUMBER, None, True) is None) and len(typs) > 0): 
                geo_ = Utils.asObjectOrNull(self.get_slot_value(OrganizationReferent.ATTR_GEO), GeoReferent)
                if (geo_ is not None): 
                    nam = geo_.get_string_value(GeoReferent.ATTR_NAME)
                    if (nam is not None and LanguageHelper.is_latin(nam)): 
                        nn = False
                        for t in typs: 
                            if (nam in t.upper()): 
                                self.add_slot(OrganizationReferent.ATTR_NAME, t.upper(), False, 0)
                                nn = True
                                if (len(typs) > 1): 
                                    s = self.find_slot(OrganizationReferent.ATTR_TYPE, t, True)
                                    if (s is not None): 
                                        self.slots.remove(s)
                                break
                        if (not nn): 
                            self.add_slot(OrganizationReferent.ATTR_NAME, "{0} {1}".format(nam, typs[0]).upper(), False, 0)
        self.__m_name_vars = (None)
        self.__m_name_hashs = (None)
        self.__m_kind_calc = False
        self._ext_ontology_attached = False
    
    def _get_pure_names(self) -> typing.List[str]:
        vars0_ = list()
        typs = self.types
        for a in self.slots: 
            if (a.type_name == OrganizationReferent.ATTR_NAME): 
                s = str(a.value).upper()
                if (not s in vars0_): 
                    vars0_.append(s)
                for t in typs: 
                    if (Utils.startsWithString(s, t, True)): 
                        if ((len(s) < (len(t) + 4)) or s[len(t)] != ' '): 
                            continue
                        ss = s[len(t) + 1:]
                        if (not ss in vars0_): 
                            vars0_.append(ss)
        return vars0_
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        return self.create_ontology_item_ex(2, False, False)
    
    def create_ontology_item_ex(self, min_len : int, only_names : bool=False, pure_names : bool=False) -> 'IntOntologyItem':
        oi = IntOntologyItem(self)
        vars0_ = list()
        typs = self.types
        for a in self.slots: 
            if (a.type_name == OrganizationReferent.ATTR_NAME): 
                s = str(a.value).upper()
                if (not s in vars0_): 
                    vars0_.append(s)
                if (not pure_names): 
                    sp = 0
                    jj = 0
                    while jj < len(s): 
                        if (s[jj] == ' '): 
                            sp += 1
                        jj += 1
                    if (sp == 1): 
                        s = s.replace(" ", "")
                        if (not s in vars0_): 
                            vars0_.append(s)
        if (not pure_names): 
            for v in self._name_vars.keys(): 
                if (not v in vars0_): 
                    vars0_.append(v)
        if (not only_names): 
            if (self.number is not None): 
                for a in self.slots: 
                    if (a.type_name == OrganizationReferent.ATTR_TYPE): 
                        s = str(a.value).upper()
                        if (not s in vars0_): 
                            vars0_.append(s)
            if (len(vars0_) == 0): 
                for t in self.types: 
                    up = t.upper()
                    if (not up in vars0_): 
                        vars0_.append(up)
            if (self.inn is not None): 
                vars0_.insert(0, "ИНН:" + self.inn)
            if (self.ogrn is not None): 
                vars0_.insert(0, "ОГРН:" + self.ogrn)
        max0_ = 20
        cou = 0
        for v in vars0_: 
            if (len(v) >= min_len): 
                if (pure_names): 
                    term = Termin()
                    term.init_by_normal_text(v, None)
                else: 
                    term = Termin(v)
                oi.termins.append(term)
                cou += 1
                if (cou >= max0_): 
                    break
        if (len(oi.termins) == 0): 
            return None
        return oi
    
    @property
    def kind(self) -> 'OrganizationKind':
        """ Категория организации (некоторая экспертная оценка на основе названия и типов) """
        from pullenti.ner.org.internal.OrgItemTypeToken import OrgItemTypeToken
        if (not self.__m_kind_calc): 
            self.__m_kind = OrgItemTypeToken.check_kind(self)
            if (self.__m_kind == OrganizationKind.UNDEFINED): 
                for p in self.profiles: 
                    if (p == OrgProfile.UNIT): 
                        self.__m_kind = OrganizationKind.DEPARTMENT
                        break
            self.__m_kind_calc = True
        return self.__m_kind
    
    def get_string_value(self, attr_name : str) -> str:
        if (attr_name == "KIND"): 
            ki = self.kind
            if (ki == OrganizationKind.UNDEFINED): 
                return None
            return Utils.enumToString(ki)
        return super().get_string_value(attr_name)
    
    @staticmethod
    def can_be_second_definition(master : 'OrganizationReferent', slave : 'OrganizationReferent') -> bool:
        # Проверка, что организация slave может быть дополнительным описанием основной организации
        if (master is None or slave is None): 
            return False
        mtypes = master.types
        stypes = slave.types
        ok = False
        for t in mtypes: 
            if (t in stypes): 
                ok = True
                break
        if (ok): 
            return True
        if (master.kind != OrganizationKind.UNDEFINED and slave.kind != OrganizationKind.UNDEFINED): 
            if (master.kind != slave.kind): 
                return False
        if (len(stypes) > 0): 
            return False
        if (len(slave.names) == 1): 
            acr = slave.names[0]
            if (LanguageHelper.ends_with(acr, "АН")): 
                return True
            for n in master.names: 
                if (OrganizationReferent.__check_acronym(acr, n) or OrganizationReferent.__check_acronym(n, acr)): 
                    return True
                if (OrganizationReferent.__check_latin_accords(n, acr)): 
                    return True
                for t in mtypes: 
                    if (OrganizationReferent.__check_acronym(acr, t.upper() + n)): 
                        return True
        return False
    
    @staticmethod
    def __check_latin_accords(rus_name : str, lat_name : str) -> bool:
        if (not LanguageHelper.is_cyrillic_char(rus_name[0]) or not LanguageHelper.is_latin_char(lat_name[0])): 
            return False
        ru = Utils.splitString(rus_name, ' ', False)
        la = Utils.splitString(lat_name, ' ', False)
        i = 0
        j = 0
        while (i < len(ru)) and (j < len(la)):
            if (Utils.compareStrings(la[j], "THE", True) == 0 or Utils.compareStrings(la[j], "OF", True) == 0): 
                j += 1
                continue
            if (MiscHelper.can_be_equal_cyr_and_latss(ru[i], la[j])): 
                return True
            i += 1
            j += 1
        if ((i < len(ru)) or (j < len(la))): 
            return False
        if (i >= 2): 
            return True
        return False
    
    @staticmethod
    def __check_acronym(acr : str, text : str) -> bool:
        i = 0
        j = 0
        i = 0
        while i < len(acr): 
            while j < len(text): 
                if (text[j] == acr[i]): 
                    break
                j += 1
            if (j >= len(text)): 
                break
            j += 1
            i += 1
        return i >= len(acr)
    
    @staticmethod
    def can_be_higher(higher_ : 'OrganizationReferent', lower : 'OrganizationReferent') -> bool:
        # Проверка на отношения "вышестоящий - нижестоящий"
        from pullenti.ner.org.internal.OrgOwnershipHelper import OrgOwnershipHelper
        return OrgOwnershipHelper.can_be_higher(higher_, lower, False)
    
    # static constructor for class OrganizationReferent
    @staticmethod
    def _static_ctor():
        OrganizationReferent.__m_empty_names = list()
        OrganizationReferent.__m_empry_eponyms = list()
        OrganizationReferent.__m_empty_geos = list()

OrganizationReferent._static_ctor()