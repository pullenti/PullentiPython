# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import xml.etree.ElementTree
import typing
from enum import IntEnum
from pullenti.ntopy.Utils import Utils
from pullenti.ner.core.Termin import Termin
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner._org.OrgProfile import OrgProfile



class OrgItemTermin(Termin):
    
    class Types(IntEnum):
        UNDEFINED = 0
        ORG = 1
        PREFIX = 2
        DEP = 3
        DEPADD = 4
    
    def __init__(self, s : str, lang_ : 'MorphLang'=MorphLang(), p1 : 'OrgProfile'=OrgProfile.UNDEFINED, p2 : 'OrgProfile'=OrgProfile.UNDEFINED) -> None:
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
        super().__init__(s, lang_, False)
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
    def _new1694(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : float, _arg5 : 'Types', _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2, _arg3)
        res.coeff = _arg4
        res.typ = _arg5
        res.is_top = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new1697(_arg1 : str, _arg2 : 'Types', _arg3 : 'OrgProfile', _arg4 : float) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.coeff = _arg4
        return res
    
    @staticmethod
    def _new1698(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : 'OrgProfile', _arg5 : float) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res._profile = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new1699(_arg1 : str, _arg2 : 'Types', _arg3 : 'OrgProfile', _arg4 : float, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.coeff = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1702(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new1703(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_be_normal_dep = _arg5
        return res
    
    @staticmethod
    def _new1704(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1705(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        return res
    
    @staticmethod
    def _new1706(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1708(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_top = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1710(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_top = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new1711(_arg1 : str, _arg2 : float, _arg3 : 'Types') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1713(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new1716(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1718(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res.can_be_normal_dep = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1720(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1721(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1722(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1724(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_number = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1731(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'Types', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1732(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1733(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1734(_arg1 : str, _arg2 : float, _arg3 : 'MorphLang', _arg4 : 'Types', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.lang = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1742(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1743(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new1744(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_doubt_word = _arg5
        return res
    
    @staticmethod
    def _new1747(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new1752(_arg1 : str, _arg2 : 'Types', _arg3 : str, _arg4 : 'OrgProfile', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res._profile = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1755(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1756(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgProfile', _arg5 : 'Types', _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res._profile = _arg4
        res.typ = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1759(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : 'OrgProfile', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new1765(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'Types', _arg5 : 'OrgProfile', _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res._profile = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1766(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTermin':
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
    def _new1772(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1780(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : 'OrgProfile', _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res._profile = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new1784(_arg1 : str, _arg2 : 'Types', _arg3 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.is_doubt_word = _arg3
        return res
    
    @staticmethod
    def _new1795(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : str, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.acronym = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1796(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : str, _arg7 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.acronym = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1797(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new1807(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1808(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTermin':
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
    def _new1811(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_top = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new1812(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTermin':
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
    def _new1814(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new1815(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1816(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1817(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new1818(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1819(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.must_be_partof_name = _arg4
        return res
    
    @staticmethod
    def _new1820(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.canonic_text = _arg4
        return res
    
    @staticmethod
    def _new1822(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.must_be_partof_name = _arg5
        return res
    
    @staticmethod
    def _new1823(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.canonic_text = _arg5
        return res
    
    @staticmethod
    def _new1829(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1830(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        return res
    
    @staticmethod
    def _new1833(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1835(_arg1 : str, _arg2 : 'Types', _arg3 : float, _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_be_single_geo = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new1836(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.typ = _arg3
        res.coeff = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1837(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1838(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1841(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.is_doubt_word = _arg5
        return res
    
    @staticmethod
    def _new1845(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new1850(_arg1 : str, _arg2 : 'Types') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        return res
    
    @staticmethod
    def _new1851(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1853(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new1858(_arg1 : str, _arg2 : 'Types', _arg3 : float, _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_number = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new1861(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_number = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1862(_arg1 : str, _arg2 : str, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.acronym = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        return res
    
    @staticmethod
    def _new1863(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.acronym = _arg3
        res.typ = _arg4
        res.can_be_normal_dep = _arg5
        return res
    
    @staticmethod
    def _new1868(_arg1 : str, _arg2 : 'Types', _arg3 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_be_normal_dep = _arg3
        return res
    
    @staticmethod
    def _new1869(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        return res
    
    @staticmethod
    def _new1873(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_be_normal_dep = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new1874(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1878(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new1879(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        res.is_doubt_word = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1880(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_number = _arg4
        res.is_doubt_word = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        return res
    
    @staticmethod
    def _new1887(_arg1 : str, _arg2 : 'Types', _arg3 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        return res
    
    @staticmethod
    def _new1888(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new1889(_arg1 : str, _arg2 : 'Types', _arg3 : 'OrgProfile', _arg4 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1890(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : 'OrgProfile', _arg5 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res._profile = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new1895(_arg1 : str, _arg2 : 'Types', _arg3 : str, _arg4 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new1896(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : str, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1900(_arg1 : str, _arg2 : 'Types', _arg3 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        return res
    
    @staticmethod
    def _new1917(_arg1 : str, _arg2 : 'Types', _arg3 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new1918(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1992(_arg1 : str, _arg2 : 'Types', _arg3 : str, _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.acronym_can_be_lower = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1993(_arg1 : str, _arg2 : 'Types', _arg3 : str, _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new1994(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1995(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new1998(_arg1 : str, _arg2 : 'Types', _arg3 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        return res
    
    @staticmethod
    def _new2000(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : str, _arg5 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.acronym = _arg4
        res.acronym_smart = _arg5
        return res
    
    @staticmethod
    def _new2011(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : str, _arg6 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.acronym = _arg5
        res.acronym_smart = _arg6
        return res
    
    @staticmethod
    def _new2028(_arg1 : str, _arg2 : 'Types', _arg3 : str, _arg4 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.acronym_smart = _arg4
        return res
    
    @staticmethod
    def _new2035(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new2041(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : str, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2044(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool, _arg5 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.can_has_number = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new2045(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        res.acronym = _arg6
        return res
    
    @staticmethod
    def _new2050(_arg1 : str, _arg2 : 'Types', _arg3 : str, _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2061(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : str, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2062(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : str, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2063(_arg1 : str, _arg2 : 'Types', _arg3 : 'OrgProfile', _arg4 : bool, _arg5 : float) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.can_has_latin_name = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new2064(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2065(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new2066(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2067(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new2070(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        return res
    
    @staticmethod
    def _new2071(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_normal_dep = _arg5
        return res
    
    @staticmethod
    def _new2072(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res.is_doubt_word = _arg5
        return res
    
    @staticmethod
    def _new2074(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.is_doubt_word = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2075(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res.is_doubt_word = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2076(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2077(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.is_doubt_word = _arg6
        return res
    
    @staticmethod
    def _new2078(_arg1 : str, _arg2 : 'Types', _arg3 : float, _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_single_name = _arg4
        return res
    
    @staticmethod
    def _new2079(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : float, _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new2090(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2091(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new2092(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : str, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.acronym = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        res.can_be_single_geo = _arg8
        return res
    
    @staticmethod
    def _new2099(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2100(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2101(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : 'Types', _arg5 : float, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2, _arg3)
        res.typ = _arg4
        res.coeff = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new2106(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : 'Types', _arg5 : float, _arg6 : bool, _arg7 : str) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2, _arg3)
        res.typ = _arg4
        res.coeff = _arg5
        res.can_has_latin_name = _arg6
        res.acronym = _arg7
        return res
    
    @staticmethod
    def _new2107(_arg1 : str, _arg2 : 'Types', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.can_has_single_name = _arg4
        res.must_has_capital_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2108(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2109(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2110(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTermin':
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
    def _new2114(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new2115(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : str, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new2117(_arg1 : str, _arg2 : float, _arg3 : 'Types', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2118(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        res.can_has_number = _arg8
        return res
    
    @staticmethod
    def _new2124(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'Types', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2129(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'Types', _arg5 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2144(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : bool, _arg5 : float) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1, _arg2, _arg3)
        res.can_has_latin_name = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new2149(_arg1 : str, _arg2 : bool, _arg3 : float) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.can_has_latin_name = _arg2
        res.coeff = _arg3
        return res
    
    @staticmethod
    def _new2153(_arg1 : str, _arg2 : 'Types', _arg3 : float, _arg4 : bool) -> 'OrgItemTermin':
        res = OrgItemTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_latin_name = _arg4
        return res