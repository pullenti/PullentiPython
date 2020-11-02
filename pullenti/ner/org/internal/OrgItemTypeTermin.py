# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.Termin import Termin
from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.org.internal.OrgItemTypeTyp import OrgItemTypeTyp

class OrgItemTypeTermin(Termin):
    
    def __init__(self, s : str, lang_ : 'MorphLang'=None, p1 : 'OrgProfile'=OrgProfile.UNDEFINED, p2 : 'OrgProfile'=OrgProfile.UNDEFINED) -> None:
        super().__init__(s, lang_, False)
        self.__m_typ = OrgItemTypeTyp.UNDEFINED
        self.must_be_partof_name = False
        self.is_pure_prefix = False
        self.can_be_normal_dep = False
        self.can_has_number = False
        self.can_has_single_name = False
        self.can_has_latin_name = False
        self.must_has_capital_name = False
        self.is_top = False
        self.can_be_single_geo = False
        self.is_doubt_word = False
        self.coeff = 0
        self.profiles = list()
        if (p1 != OrgProfile.UNDEFINED): 
            self.profiles.append(p1)
        if (p2 != OrgProfile.UNDEFINED): 
            self.profiles.append(p2)
    
    @property
    def typ(self) -> 'OrgItemTypeTyp':
        if (self.is_pure_prefix): 
            return OrgItemTypeTyp.PREFIX
        return self.__m_typ
    @typ.setter
    def typ(self, value) -> 'OrgItemTypeTyp':
        if (value == OrgItemTypeTyp.PREFIX): 
            self.is_pure_prefix = True
            self.__m_typ = OrgItemTypeTyp.ORG
        else: 
            self.__m_typ = value
            if (self.__m_typ == OrgItemTypeTyp.DEP or self.__m_typ == OrgItemTypeTyp.DEPADD): 
                if (not OrgProfile.UNIT in self.profiles): 
                    self.profiles.append(OrgProfile.UNIT)
        return value
    
    @property
    def _profile(self) -> 'OrgProfile':
        return OrgProfile.UNDEFINED
    @_profile.setter
    def _profile(self, value) -> 'OrgProfile':
        self.profiles.append(value)
        return value
    
    def __copy_from(self, it : 'OrgItemTypeTermin') -> None:
        self.profiles.extend(it.profiles)
        self.is_pure_prefix = it.is_pure_prefix
        self.can_be_normal_dep = it.can_be_normal_dep
        self.can_has_number = it.can_has_number
        self.can_has_single_name = it.can_has_single_name
        self.can_has_latin_name = it.can_has_latin_name
        self.must_be_partof_name = it.must_be_partof_name
        self.must_has_capital_name = it.must_has_capital_name
        self.is_top = it.is_top
        self.can_be_normal_dep = it.can_be_normal_dep
        self.can_be_single_geo = it.can_be_single_geo
        self.is_doubt_word = it.is_doubt_word
        self.coeff = it.coeff
    
    @staticmethod
    def deserialize_src(xml0_ : xml.etree.ElementTree.Element, set0_ : 'OrgItemTypeTermin') -> typing.List['OrgItemTypeTermin']:
        res = list()
        is_set = xml0_.tag == "set"
        if (is_set): 
            set0_ = OrgItemTypeTermin(None)
            res.append(set0_)
        if (xml0_.attrib is None): 
            return res
        for a in xml0_.attrib.items(): 
            nam = a[0]
            if (not nam.startswith("name")): 
                continue
            lang_ = MorphLang.RU
            if (nam == "nameUa"): 
                lang_ = MorphLang.UA
            elif (nam == "nameEn"): 
                lang_ = MorphLang.EN
            it = None
            for s in Utils.splitString(a[1], ';', False): 
                if (not Utils.isNullOrEmpty(s)): 
                    if (it is None): 
                        it = OrgItemTypeTermin(s, lang_)
                        res.append(it)
                        if (set0_ is not None): 
                            it.__copy_from(set0_)
                    else: 
                        it.add_variant(s, False)
        for a in xml0_.attrib.items(): 
            nam = a[0]
            if (nam.startswith("name")): 
                continue
            if (nam.startswith("abbr")): 
                lang_ = MorphLang.RU
                if (nam == "abbrUa"): 
                    lang_ = MorphLang.UA
                elif (nam == "abbrEn"): 
                    lang_ = MorphLang.EN
                for r in res: 
                    if (r.lang == lang_): 
                        r.acronym = a[1]
                continue
            if (nam == "profile"): 
                li = list()
                for s in Utils.splitString(a[1], ';', False): 
                    try: 
                        p = Utils.valToEnum(s, OrgProfile)
                        if (p != OrgProfile.UNDEFINED): 
                            li.append(p)
                    except Exception as ex: 
                        pass
                for r in res: 
                    r.profiles = li
                continue
            if (nam == "coef"): 
                v = float(a[1])
                for r in res: 
                    r.coeff = v
                continue
            if (nam == "partofname"): 
                for r in res: 
                    r.must_be_partof_name = a[1] == "true"
                continue
            if (nam == "top"): 
                for r in res: 
                    r.is_top = a[1] == "true"
                continue
            if (nam == "geo"): 
                for r in res: 
                    r.can_be_single_geo = a[1] == "true"
                continue
            if (nam == "purepref"): 
                for r in res: 
                    r.is_pure_prefix = a[1] == "true"
                continue
            if (nam == "number"): 
                for r in res: 
                    r.can_has_number = a[1] == "true"
                continue
            raise Utils.newException("Unknown Org Type Tag: " + a[0], None)
        return res
    
    @staticmethod
    def _new1827(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : float, _arg5 : 'OrgItemTypeTyp', _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.coeff = _arg4
        res.typ = _arg5
        res.is_top = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new1830(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile', _arg4 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.coeff = _arg4
        return res
    
    @staticmethod
    def _new1831(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res._profile = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new1832(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile', _arg4 : float, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.coeff = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1835(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new1836(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_be_normal_dep = _arg5
        return res
    
    @staticmethod
    def _new1837(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1838(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        return res
    
    @staticmethod
    def _new1839(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1843(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_top = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1845(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_top = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new1846(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1848(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new1851(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1853(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res.can_be_normal_dep = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1855(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1856(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1857(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1859(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_number = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1866(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1867(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1868(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1871(_arg1 : str, _arg2 : float, _arg3 : 'MorphLang', _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.lang = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1880(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1881(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new1882(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_doubt_word = _arg5
        return res
    
    @staticmethod
    def _new1885(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new1890(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : 'OrgProfile', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res._profile = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1893(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1894(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgProfile', _arg5 : 'OrgItemTypeTyp', _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res._profile = _arg4
        res.typ = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1897(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new1903(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : 'OrgProfile', _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res._profile = _arg5
        res.can_be_single_geo = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new1904(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_single_name = _arg6
        res.can_has_latin_name = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new1910(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1918(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile', _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res._profile = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new1922(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.is_doubt_word = _arg3
        return res
    
    @staticmethod
    def _new1925(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : 'OrgProfile', _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        res.can_has_latin_name = _arg7
        return res
    
    @staticmethod
    def _new1934(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : str, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.acronym = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1935(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : str, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.acronym = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1936(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new1946(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1947(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new1950(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_top = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        res.can_be_single_geo = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new1951(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_top = _arg5
        res.can_has_single_name = _arg6
        res.can_has_latin_name = _arg7
        res.can_be_single_geo = _arg8
        return res
    
    @staticmethod
    def _new1955(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new1956(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1957(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1958(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1959(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1960(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.must_be_partof_name = _arg4
        return res
    
    @staticmethod
    def _new1961(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.canonic_text = _arg4
        return res
    
    @staticmethod
    def _new1963(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.must_be_partof_name = _arg5
        return res
    
    @staticmethod
    def _new1964(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.canonic_text = _arg5
        return res
    
    @staticmethod
    def _new1970(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1971(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        return res
    
    @staticmethod
    def _new1974(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1976(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : float, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_be_single_geo = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new1977(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.typ = _arg3
        res.coeff = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1978(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1979(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1981(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_doubt_word = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1982(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.is_doubt_word = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1983(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1984(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : str, _arg5 : 'OrgItemTypeTyp', _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.acronym = _arg4
        res.typ = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1989(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new1994(_arg1 : str, _arg2 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        return res
    
    @staticmethod
    def _new1995(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1997(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new2002(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.is_doubt_word = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new2003(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt_word = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2004(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : float, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_number = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new2006(_arg1 : str, _arg2 : str, _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.acronym = _arg2
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_number = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2007(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_number = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2008(_arg1 : str, _arg2 : str, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.acronym = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        return res
    
    @staticmethod
    def _new2010(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.acronym = _arg3
        res.typ = _arg4
        res.can_be_normal_dep = _arg5
        return res
    
    @staticmethod
    def _new2015(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_be_normal_dep = _arg3
        return res
    
    @staticmethod
    def _new2016(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        return res
    
    @staticmethod
    def _new2022(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_be_normal_dep = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new2023(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2027(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new2028(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        res.is_doubt_word = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2029(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_number = _arg4
        res.is_doubt_word = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        return res
    
    @staticmethod
    def _new2036(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        return res
    
    @staticmethod
    def _new2037(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new2038(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile', _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new2039(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res._profile = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new2044(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new2045(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2049(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        return res
    
    @staticmethod
    def _new2066(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new2068(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new2158(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.acronym_can_be_lower = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new2159(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new2160(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new2161(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new2164(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        return res
    
    @staticmethod
    def _new2166(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : str, _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.acronym = _arg4
        res.acronym_smart = _arg5
        return res
    
    @staticmethod
    def _new2177(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : str, _arg6 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.acronym = _arg5
        res.acronym_smart = _arg6
        return res
    
    @staticmethod
    def _new2195(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.acronym_smart = _arg4
        return res
    
    @staticmethod
    def _new2203(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new2209(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2212(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.can_has_number = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new2213(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        res.acronym = _arg6
        return res
    
    @staticmethod
    def _new2218(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2229(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2230(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2231(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile', _arg4 : bool, _arg5 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.can_has_latin_name = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new2232(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2233(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new2234(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2235(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new2238(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2240(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_normal_dep = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2241(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res.is_doubt_word = _arg5
        return res
    
    @staticmethod
    def _new2243(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.is_doubt_word = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2244(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res.is_doubt_word = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2245(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2246(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.is_doubt_word = _arg6
        return res
    
    @staticmethod
    def _new2247(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : float, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_single_name = _arg4
        return res
    
    @staticmethod
    def _new2248(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new2258(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new2259(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2260(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new2261(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : str, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.acronym = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        res.can_be_single_geo = _arg8
        return res
    
    @staticmethod
    def _new2268(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2269(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2270(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2271(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : 'OrgItemTypeTyp', _arg5 : float, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.typ = _arg4
        res.coeff = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new2276(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : 'OrgItemTypeTyp', _arg5 : float, _arg6 : bool, _arg7 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.typ = _arg4
        res.coeff = _arg5
        res.can_has_latin_name = _arg6
        res.acronym = _arg7
        return res
    
    @staticmethod
    def _new2277(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.can_has_single_name = _arg4
        res.must_has_capital_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2278(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2279(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2280(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new2284(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new2285(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new2287(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2288(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        res.can_has_number = _arg8
        return res
    
    @staticmethod
    def _new2291(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new2292(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new2298(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2303(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2304(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2308(_arg1 : str, _arg2 : float, _arg3 : bool, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.can_be_normal_dep = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new2321(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : bool, _arg5 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.can_has_latin_name = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new2326(_arg1 : str, _arg2 : bool, _arg3 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.can_has_latin_name = _arg2
        res.coeff = _arg3
        return res
    
    @staticmethod
    def _new2330(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : float, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_latin_name = _arg4
        return res