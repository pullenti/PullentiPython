# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import xml.etree
import typing
from enum import IntEnum
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.Termin import Termin
from pullenti.ner.org.OrgProfile import OrgProfile

class OrgItemTermin(Termin):
    
    class Types(IntEnum):
        UNDEFINED = 0
        ORG = 1
        PREFIX = 2
        DEP = 3
        DEPADD = 4
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, s : str, lang_ : 'MorphLang'=None, p1 : 'OrgProfile'=OrgProfile.UNDEFINED, p2 : 'OrgProfile'=OrgProfile.UNDEFINED) -> None:
        super().__init__(s, lang_, False)
        self.__m_typ = OrgItemTermin.Types.UNDEFINED
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
    def typ(self) -> 'Types':
        if (self.is_pure_prefix): 
            return OrgItemTermin.Types.PREFIX
        return self.__m_typ
    @typ.setter
    def typ(self, value) -> 'Types':
        if (value == OrgItemTermin.Types.PREFIX): 
            self.is_pure_prefix = True
            self.__m_typ = OrgItemTermin.Types.ORG
        else: 
            self.__m_typ = value
            if (self.__m_typ == OrgItemTermin.Types.DEP or self.__m_typ == OrgItemTermin.Types.DEPADD): 
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
    
    def __copy_from(self, it : 'OrgItemTermin') -> None:
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
    def deserialize_src(xml0_ : xml.etree.ElementTree.Element, set0_ : 'OrgItemTermin') -> typing.List['OrgItemTermin']:
        res = list()
        is_set = xml0_.tag == "set"
        if (is_set): 
            set0_ = OrgItemTermin(None)
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
                        it = OrgItemTermin(s, lang_)
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
    def _new1821(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : float, _arg5 : 'Types', _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2, _arg3)
        res.coeff = _arg4
        res.typ = _arg5
        res.is_top = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new1824(_arg1 : str, _arg2 : 'Types', _arg3 : 'OrgProfile', _arg4 : float) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.coeff = _arg4
        return res
    
    @staticmethod
    def _new1825(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : 'OrgProfile', _arg5 : float) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res._profile = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new1826(_arg1 : str, _arg2 : 'Types', _arg3 : 'OrgProfile', _arg4 : float, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.coeff = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1829(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new1830(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_be_normal_dep = _arg5
        return res
    
    @staticmethod
    def _new1831(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1832(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        return res
    
    @staticmethod
    def _new1833(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1835(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_top = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1837(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_top = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new1838(_arg1 : str, _arg2 : float, _arg3 : 'Types') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1840(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new1843(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1845(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res.can_be_normal_dep = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1847(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1848(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1849(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1851(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_number = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1858(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'Types', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1859(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1860(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1863(_arg1 : str, _arg2 : float, _arg3 : 'MorphLang', _arg4 : 'Types', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.lang = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1872(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1873(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new1874(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_doubt_word = _arg5
        return res
    
    @staticmethod
    def _new1877(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new1882(_arg1 : str, _arg2 : 'Types', _arg3 : str, _arg4 : 'OrgProfile', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res._profile = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1885(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1886(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgProfile', _arg5 : 'Types', _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res._profile = _arg4
        res.typ = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1889(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : 'OrgProfile', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new1895(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'Types', _arg5 : 'OrgProfile', _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res._profile = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1896(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_single_name = _arg6
        res.can_has_latin_name = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new1902(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1910(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : 'OrgProfile', _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res._profile = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new1914(_arg1 : str, _arg2 : 'Types', _arg3 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.is_doubt_word = _arg3
        return res
    
    @staticmethod
    def _new1917(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str, _arg5 : bool, _arg6 : 'OrgProfile', _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        res.can_has_latin_name = _arg7
        return res
    
    @staticmethod
    def _new1926(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : str, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.acronym = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1927(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : str, _arg7 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.acronym = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1928(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new1938(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1939(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new1942(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_top = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        res.can_be_single_geo = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new1943(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_top = _arg5
        res.can_has_single_name = _arg6
        res.can_has_latin_name = _arg7
        res.can_be_single_geo = _arg8
        return res
    
    @staticmethod
    def _new1947(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new1948(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1949(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1950(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1951(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1952(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.must_be_partof_name = _arg4
        return res
    
    @staticmethod
    def _new1953(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.canonic_text = _arg4
        return res
    
    @staticmethod
    def _new1955(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.must_be_partof_name = _arg5
        return res
    
    @staticmethod
    def _new1956(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.canonic_text = _arg5
        return res
    
    @staticmethod
    def _new1962(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1963(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        return res
    
    @staticmethod
    def _new1966(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1968(_arg1 : str, _arg2 : 'Types', _arg3 : float, _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_be_single_geo = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new1969(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.typ = _arg3
        res.coeff = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1970(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1971(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1973(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_doubt_word = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1974(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.is_doubt_word = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1975(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1976(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : str, _arg5 : 'Types', _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.acronym = _arg4
        res.typ = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1980(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new1985(_arg1 : str, _arg2 : 'Types') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        return res
    
    @staticmethod
    def _new1986(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1988(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new1993(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.is_doubt_word = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new1994(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt_word = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1995(_arg1 : str, _arg2 : 'Types', _arg3 : float, _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_number = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new1997(_arg1 : str, _arg2 : str, _arg3 : 'Types', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.acronym = _arg2
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_number = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1998(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_number = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1999(_arg1 : str, _arg2 : str, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.acronym = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        return res
    
    @staticmethod
    def _new2000(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.acronym = _arg3
        res.typ = _arg4
        res.can_be_normal_dep = _arg5
        return res
    
    @staticmethod
    def _new2005(_arg1 : str, _arg2 : 'Types', _arg3 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_be_normal_dep = _arg3
        return res
    
    @staticmethod
    def _new2006(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        return res
    
    @staticmethod
    def _new2012(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_be_normal_dep = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new2013(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2017(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new2018(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        res.is_doubt_word = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2019(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_number = _arg4
        res.is_doubt_word = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        return res
    
    @staticmethod
    def _new2026(_arg1 : str, _arg2 : 'Types', _arg3 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        return res
    
    @staticmethod
    def _new2027(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new2028(_arg1 : str, _arg2 : 'Types', _arg3 : 'OrgProfile', _arg4 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new2029(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : 'OrgProfile', _arg5 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res._profile = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new2034(_arg1 : str, _arg2 : 'Types', _arg3 : str, _arg4 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new2035(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : str, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2039(_arg1 : str, _arg2 : 'Types', _arg3 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        return res
    
    @staticmethod
    def _new2056(_arg1 : str, _arg2 : 'Types', _arg3 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new2058(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new2147(_arg1 : str, _arg2 : 'Types', _arg3 : str, _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.acronym_can_be_lower = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new2148(_arg1 : str, _arg2 : 'Types', _arg3 : str, _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new2149(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new2150(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new2153(_arg1 : str, _arg2 : 'Types', _arg3 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        return res
    
    @staticmethod
    def _new2155(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : str, _arg5 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.acronym = _arg4
        res.acronym_smart = _arg5
        return res
    
    @staticmethod
    def _new2166(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : str, _arg6 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.acronym = _arg5
        res.acronym_smart = _arg6
        return res
    
    @staticmethod
    def _new2184(_arg1 : str, _arg2 : 'Types', _arg3 : str, _arg4 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.acronym_smart = _arg4
        return res
    
    @staticmethod
    def _new2191(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new2197(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : str, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2200(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool, _arg5 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.can_has_number = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new2201(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        res.acronym = _arg6
        return res
    
    @staticmethod
    def _new2206(_arg1 : str, _arg2 : 'Types', _arg3 : str, _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2217(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : str, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2218(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : str, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2219(_arg1 : str, _arg2 : 'Types', _arg3 : 'OrgProfile', _arg4 : bool, _arg5 : float) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.can_has_latin_name = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new2220(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2221(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new2222(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2223(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new2226(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2227(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_normal_dep = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2228(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res.is_doubt_word = _arg5
        return res
    
    @staticmethod
    def _new2230(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.is_doubt_word = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2231(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res.is_doubt_word = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2232(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2233(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.is_doubt_word = _arg6
        return res
    
    @staticmethod
    def _new2234(_arg1 : str, _arg2 : 'Types', _arg3 : float, _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_single_name = _arg4
        return res
    
    @staticmethod
    def _new2235(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : float, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new2245(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new2246(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2247(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new2248(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : str, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.acronym = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        res.can_be_single_geo = _arg8
        return res
    
    @staticmethod
    def _new2255(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2256(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2257(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : float, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2258(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : 'Types', _arg5 : float, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2, _arg3)
        res.typ = _arg4
        res.coeff = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new2263(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : 'Types', _arg5 : float, _arg6 : bool, _arg7 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2, _arg3)
        res.typ = _arg4
        res.coeff = _arg5
        res.can_has_latin_name = _arg6
        res.acronym = _arg7
        return res
    
    @staticmethod
    def _new2264(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.can_has_single_name = _arg4
        res.must_has_capital_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2265(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2266(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2267(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new2271(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new2272(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new2274(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2275(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        res.can_has_number = _arg8
        return res
    
    @staticmethod
    def _new2282(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2287(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2288(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2292(_arg1 : str, _arg2 : float, _arg3 : bool, _arg4 : 'Types', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.can_be_normal_dep = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new2303(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : bool, _arg5 : float) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2, _arg3)
        res.can_has_latin_name = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new2308(_arg1 : str, _arg2 : bool, _arg3 : float) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.can_has_latin_name = _arg2
        res.coeff = _arg3
        return res
    
    @staticmethod
    def _new2312(_arg1 : str, _arg2 : 'Types', _arg3 : float, _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_latin_name = _arg4
        return res