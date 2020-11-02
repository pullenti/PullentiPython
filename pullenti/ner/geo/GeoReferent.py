# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.geo.internal.MetaGeo import MetaGeo
from pullenti.ner.core.Termin import Termin
from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.metadata.ReferentClass import ReferentClass

class GeoReferent(Referent):
    """ Сущность, описывающая территорию как административную единицу.
    Это страны, автономные образования, области, административные районы,
    населённые пункты, территории и пр.
    
    """
    
    def __init__(self) -> None:
        super().__init__(GeoReferent.OBJ_TYPENAME)
        self.__m_tmp_bits = 0
        self.__m_higher = None;
        self.instance_of = MetaGeo._global_meta
    
    OBJ_TYPENAME = "GEO"
    """ Имя типа сущности TypeName ("GEO") """
    
    ATTR_NAME = "NAME"
    """ Имя атрибута - наименование """
    
    ATTR_TYPE = "TYPE"
    """ Имя атрибута - тип """
    
    ATTR_ALPHA2 = "ALPHA2"
    """ Имя атрибута - для страны 2-х значный идентификатор """
    
    ATTR_HIGHER = "HIGHER"
    """ Имя атрибута - вышележащий географический объект """
    
    ATTR_REF = "REF"
    """ Имя атрибута - дополнительная ссылка """
    
    ATTR_FIAS = "FIAS"
    """ Имя атрибута - код ФИАС (определяется анализатором FiasAnalyzer) """
    
    ATTR_BTI = "BTI"
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        return self.__to_string(short_variant, lang, True, lev)
    
    def __to_string(self, short_variant : bool, lang : 'MorphLang', out_cladr : bool, lev : int) -> str:
        if (self.is_union and not self.is_state): 
            res = io.StringIO()
            print(self.get_string_value(GeoReferent.ATTR_TYPE), end="", file=res)
            for s in self.slots: 
                if (s.type_name == GeoReferent.ATTR_REF and (isinstance(s.value, Referent))): 
                    print("; {0}".format(s.value.to_string(True, lang, 0)), end="", file=res, flush=True)
            return Utils.toStringStringIO(res)
        name = MiscHelper.convert_first_char_upper_and_other_lower(self.__get_name(lang is not None and lang.is_en))
        if (not short_variant): 
            if (not self.is_state): 
                if (self.is_city and self.is_region): 
                    pass
                else: 
                    typ = self.get_string_value(GeoReferent.ATTR_TYPE)
                    if (typ is not None): 
                        if (not self.is_city): 
                            i = typ.rfind(' ')
                            if (i > 0): 
                                typ = typ[i + 1:]
                        name = "{0} {1}".format(typ, name)
        if (not short_variant and out_cladr): 
            kladr = self.get_slot_value(GeoReferent.ATTR_FIAS)
            if (isinstance(kladr, Referent)): 
                name = "{0} (ФИАС: {1})".format(name, Utils.ifNotNull(kladr.get_string_value("GUID"), "?"))
            bti = self.get_string_value(GeoReferent.ATTR_BTI)
            if (bti is not None): 
                name = "{0} (БТИ {1})".format(name, bti)
        if (not short_variant and self.higher is not None and (lev < 10)): 
            if (((self.higher.is_city and self.is_region)) or ((self.find_slot(GeoReferent.ATTR_TYPE, "город", True) is None and self.find_slot(GeoReferent.ATTR_TYPE, "місто", True) is None and self.is_city))): 
                return "{0}; {1}".format(name, self.higher.__to_string(False, lang, False, lev + 1))
        return name
    
    def __get_name(self, cyr : bool) -> str:
        name = None
        for i in range(2):
            for s in self.slots: 
                if (s.type_name == GeoReferent.ATTR_NAME): 
                    v = str(s.value)
                    if (Utils.isNullOrEmpty(v)): 
                        continue
                    if (i == 0): 
                        if (not LanguageHelper.is_cyrillic_char(v[0])): 
                            if (cyr): 
                                continue
                        elif (not cyr): 
                            continue
                    if (name is None): 
                        name = v
                    elif (len(name) > len(v)): 
                        if ((len(v) < 4) and (len(name) < 20)): 
                            pass
                        elif (name[len(name) - 1] == 'В'): 
                            pass
                        else: 
                            name = v
                    elif ((len(name) < 4) and len(v) >= 4 and (len(v) < 10)): 
                        name = v
            if (name is not None): 
                break
        if (name == "МОЛДОВА"): 
            name = "МОЛДАВИЯ"
        elif (name == "БЕЛАРУСЬ"): 
            name = "БЕЛОРУССИЯ"
        elif (name == "АПСНЫ"): 
            name = "АБХАЗИЯ"
        return Utils.ifNotNull(name, "?")
    
    def to_sort_string(self) -> str:
        typ = "GEO4"
        if (self.is_state): 
            typ = "GEO1"
        elif (self.is_region): 
            typ = "GEO2"
        elif (self.is_city): 
            typ = "GEO3"
        return typ + self.__get_name(False)
    
    def get_compare_strings(self) -> typing.List[str]:
        res = list()
        for s in self.slots: 
            if (s.type_name == GeoReferent.ATTR_NAME): 
                res.append(str(s.value))
        if (len(res) > 0): 
            return res
        else: 
            return super().get_compare_strings()
    
    def _add_name(self, v : str) -> None:
        if (v is not None): 
            if (v.find('-') > 0): 
                v = v.replace(" - ", "-")
            self.add_slot(GeoReferent.ATTR_NAME, v.upper(), False, 0)
    
    def _add_typ(self, v : str) -> None:
        if (v is not None): 
            if (v == "ТЕРРИТОРИЯ" and self.is_state): 
                return
            self.add_slot(GeoReferent.ATTR_TYPE, v.lower(), False, 0)
    
    def _add_typ_city(self, lang : 'MorphLang') -> None:
        if (lang.is_en): 
            self.add_slot(GeoReferent.ATTR_TYPE, "city", False, 0)
        elif (lang.is_ua): 
            self.add_slot(GeoReferent.ATTR_TYPE, "місто", False, 0)
        else: 
            self.add_slot(GeoReferent.ATTR_TYPE, "город", False, 0)
    
    def _add_typ_reg(self, lang : 'MorphLang') -> None:
        if (lang.is_en): 
            self.add_slot(GeoReferent.ATTR_TYPE, "region", False, 0)
        elif (lang.is_ua): 
            self.add_slot(GeoReferent.ATTR_TYPE, "регіон", False, 0)
        else: 
            self.add_slot(GeoReferent.ATTR_TYPE, "регион", False, 0)
    
    def _add_typ_state(self, lang : 'MorphLang') -> None:
        if (lang.is_en): 
            self.add_slot(GeoReferent.ATTR_TYPE, "country", False, 0)
        elif (lang.is_ua): 
            self.add_slot(GeoReferent.ATTR_TYPE, "держава", False, 0)
        else: 
            self.add_slot(GeoReferent.ATTR_TYPE, "государство", False, 0)
    
    def _add_typ_union(self, lang : 'MorphLang') -> None:
        if (lang.is_en): 
            self.add_slot(GeoReferent.ATTR_TYPE, "union", False, 0)
        elif (lang.is_ua): 
            self.add_slot(GeoReferent.ATTR_TYPE, "союз", False, 0)
        else: 
            self.add_slot(GeoReferent.ATTR_TYPE, "союз", False, 0)
    
    def _add_typ_ter(self, lang : 'MorphLang') -> None:
        if (lang.is_en): 
            self.add_slot(GeoReferent.ATTR_TYPE, "territory", False, 0)
        elif (lang.is_ua): 
            self.add_slot(GeoReferent.ATTR_TYPE, "територія", False, 0)
        else: 
            self.add_slot(GeoReferent.ATTR_TYPE, "территория", False, 0)
    
    def add_slot(self, attr_name : str, attr_value : object, clear_old_value : bool, stat_count : int=0) -> 'Slot':
        self.__m_tmp_bits = (0)
        return super().add_slot(attr_name, attr_value, clear_old_value, stat_count)
    
    def upload_slot(self, slot : 'Slot', new_val : object) -> None:
        self.__m_tmp_bits = (0)
        super().upload_slot(slot, new_val)
    
    __bit_iscity = 2
    
    __bit_isregion = 4
    
    __bit_isstate = 8
    
    __bit_isbigcity = 0x10
    
    __bit_isterritory = 0x20
    
    def __recalc_tmp_bits(self) -> None:
        self.__m_tmp_bits = (1)
        self.__m_higher = (None)
        hi = Utils.asObjectOrNull(self.get_slot_value(GeoReferent.ATTR_HIGHER), GeoReferent)
        if (hi == self or hi is None): 
            pass
        else: 
            li = None
            err = False
            r = Utils.asObjectOrNull(hi.get_slot_value(GeoReferent.ATTR_HIGHER), Referent)
            while r is not None: 
                if (r == hi or r == self): 
                    err = True
                    break
                if (li is None): 
                    li = list()
                elif (r in li): 
                    err = True
                    break
                li.append(r)
                r = (Utils.asObjectOrNull(r.get_slot_value(GeoReferent.ATTR_HIGHER), Referent))
            if (not err): 
                self.__m_higher = hi
        is_state_ = -1
        is_reg = -1
        for t in self.slots: 
            if (t.type_name == GeoReferent.ATTR_TYPE): 
                val = Utils.asObjectOrNull(t.value, str)
                if (val == "территория" or val == "територія" or val == "territory"): 
                    self.__m_tmp_bits = (1 | GeoReferent.__bit_isterritory)
                    return
                if (GeoReferent.__is_city(val)): 
                    self.__m_tmp_bits |= (GeoReferent.__bit_iscity)
                    if ((val == "город" or val == "місто" or val == "city") or val == "town"): 
                        self.__m_tmp_bits |= (GeoReferent.__bit_isbigcity)
                    continue
                if ((val == "государство" or val == "держава" or val == "империя") or val == "імперія" or val == "country"): 
                    self.__m_tmp_bits |= (GeoReferent.__bit_isstate)
                    is_reg = 0
                    continue
                if (GeoReferent.__is_region(val)): 
                    if (is_state_ < 0): 
                        is_state_ = 0
                    if (is_reg < 0): 
                        is_reg = 1
            elif (t.type_name == GeoReferent.ATTR_ALPHA2): 
                self.__m_tmp_bits = (1 | GeoReferent.__bit_isstate)
                if (self.find_slot(GeoReferent.ATTR_TYPE, "город", True) is not None or self.find_slot(GeoReferent.ATTR_TYPE, "місто", True) is not None or self.find_slot(GeoReferent.ATTR_TYPE, "city", True) is not None): 
                    self.__m_tmp_bits |= (GeoReferent.__bit_isbigcity | GeoReferent.__bit_iscity)
                return
        if (is_state_ != 0): 
            if ((is_state_ < 0) and (((self.__m_tmp_bits) & GeoReferent.__bit_iscity)) != 0): 
                pass
            else: 
                self.__m_tmp_bits |= (GeoReferent.__bit_isstate)
        if (is_reg != 0): 
            if ((is_state_ < 0) and (((self.__m_tmp_bits) & GeoReferent.__bit_iscity)) != 0): 
                pass
            else: 
                self.__m_tmp_bits |= (GeoReferent.__bit_isregion)
    
    @property
    def typs(self) -> typing.List[str]:
        """ Тип(ы) """
        res = list()
        for s in self.slots: 
            if (s.type_name == GeoReferent.ATTR_TYPE): 
                res.append(s.value)
        return res
    
    @property
    def is_city(self) -> bool:
        """ Это может быть населенным пунктом """
        if ((((self.__m_tmp_bits) & 1)) == 0): 
            self.__recalc_tmp_bits()
        return (((self.__m_tmp_bits) & GeoReferent.__bit_iscity)) != 0
    
    @property
    def is_big_city(self) -> bool:
        """ Это именно город, а не деревня или поселок """
        if ((((self.__m_tmp_bits) & 1)) == 0): 
            self.__recalc_tmp_bits()
        return (((self.__m_tmp_bits) & GeoReferent.__bit_isbigcity)) != 0
    
    @property
    def is_state(self) -> bool:
        """ Это может быть отдельным государством """
        if ((((self.__m_tmp_bits) & 1)) == 0): 
            self.__recalc_tmp_bits()
        return (((self.__m_tmp_bits) & GeoReferent.__bit_isstate)) != 0
    
    @property
    def is_region(self) -> bool:
        """ Это может быть регионом в составе другого образования """
        if ((((self.__m_tmp_bits) & 1)) == 0): 
            self.__recalc_tmp_bits()
        return (((self.__m_tmp_bits) & GeoReferent.__bit_isregion)) != 0
    
    @property
    def is_territory(self) -> bool:
        """ Просто территория (например, территория аэропорта Шереметьево) """
        if ((((self.__m_tmp_bits) & 1)) == 0): 
            self.__recalc_tmp_bits()
        return (((self.__m_tmp_bits) & GeoReferent.__bit_isterritory)) != 0
    
    @property
    def is_union(self) -> bool:
        """ Союз России и Белоруссии """
        for s in self.slots: 
            if (s.type_name == GeoReferent.ATTR_TYPE): 
                v = Utils.asObjectOrNull(s.value, str)
                if (v.endswith("союз")): 
                    return True
        return False
    
    @staticmethod
    def __is_city(v : str) -> bool:
        if ((((((((((("поселок" in v or "селение" in v or "село" in v) or "деревня" in v or "станица" in v) or "пункт" in v or "станция" in v) or "аул" in v or "хутор" in v) or "местечко" in v or "урочище" in v) or "усадьба" in v or "аал" in v) or "выселки" in v or "арбан" in v) or "місто" in v or "селище" in v) or "сіло" in v or "станиця" in v) or "станція" in v or "city" in v) or "municipality" in v or "town" in v): 
            return True
        if ("город" in v or "місто" in v): 
            if (not GeoReferent.__is_region(v)): 
                return True
        return False
    
    @staticmethod
    def __is_region(v : str) -> bool:
        if (((((((((((("район" in v or "штат" in v or "область" in v) or "волость" in v or "провинция" in v) or "регион" in v or "округ" in v) or "край" in v or "префектура" in v) or "улус" in v or "провінція" in v) or "регіон" in v or "образование" in v) or "утворення" in v or "автономия" in v) or "автономія" in v or "district" in v) or "county" in v or "state" in v) or "area" in v or "borough" in v) or "parish" in v or "region" in v) or "province" in v or "prefecture" in v): 
            return True
        if ("городск" in v or "міськ" in v): 
            if ("образование" in v or "освіта" in v): 
                return True
        return False
    
    @property
    def alpha2(self) -> str:
        """ 2-х символьный идентификатор страны (ISO 3166) """
        return self.get_string_value(GeoReferent.ATTR_ALPHA2)
    @alpha2.setter
    def alpha2(self, value) -> str:
        self.add_slot(GeoReferent.ATTR_ALPHA2, value, True, 0)
        return value
    
    @property
    def higher(self) -> 'GeoReferent':
        """ Вышестоящий объект """
        if ((((self.__m_tmp_bits) & 1)) == 0): 
            self.__recalc_tmp_bits()
        return self.__m_higher
    @higher.setter
    def higher(self, value) -> 'GeoReferent':
        if (value == self): 
            return value
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
        self.add_slot(GeoReferent.ATTR_HIGHER, None, True, 0)
        if (value is not None): 
            self.add_slot(GeoReferent.ATTR_HIGHER, value, True, 0)
        return value
    
    @staticmethod
    def __check_round_dep(d : 'GeoReferent') -> bool:
        if (d is None): 
            return True
        d0 = d
        li = list()
        d = d.higher
        while d is not None: 
            if (d == d0): 
                return True
            if (d in li): 
                return True
            li.append(d)
            d = d.higher
        return False
    
    @property
    def top_higher(self) -> 'GeoReferent':
        if (GeoReferent.__check_round_dep(self)): 
            return self
        hi = self
        while hi is not None: 
            if (hi.higher is None): 
                return hi
            hi = hi.higher
        return self
    
    @property
    def parent_referent(self) -> 'Referent':
        return self.higher
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType') -> bool:
        geo_ = Utils.asObjectOrNull(obj, GeoReferent)
        if (geo_ is None): 
            return False
        if (geo_.alpha2 is not None and geo_.alpha2 == self.alpha2): 
            return True
        if (self.is_city != geo_.is_city): 
            return False
        if (self.is_union != geo_.is_union): 
            return False
        if (self.is_union): 
            for s in self.slots: 
                if (s.type_name == GeoReferent.ATTR_REF): 
                    if (obj.find_slot(GeoReferent.ATTR_REF, s.value, True) is None): 
                        return False
            for s in obj.slots: 
                if (s.type_name == GeoReferent.ATTR_REF): 
                    if (self.find_slot(GeoReferent.ATTR_REF, s.value, True) is None): 
                        return False
            return True
        ref1 = Utils.asObjectOrNull(self.get_slot_value(GeoReferent.ATTR_REF), Referent)
        ref2 = Utils.asObjectOrNull(geo_.get_slot_value(GeoReferent.ATTR_REF), Referent)
        if (ref1 is not None and ref2 is not None): 
            if (ref1 != ref2): 
                return False
        r = self.is_region or self.is_state
        r1 = geo_.is_region or geo_.is_state
        if (r != r1): 
            if (self.is_territory != geo_.is_territory): 
                return False
            return False
        eq_names = False
        for s in self.slots: 
            if (s.type_name == GeoReferent.ATTR_NAME): 
                if (geo_.find_slot(s.type_name, s.value, True) is not None): 
                    eq_names = True
                    break
        if (not eq_names): 
            return False
        if (self.is_region and geo_.is_region): 
            typs1 = self.typs
            typs2 = geo_.typs
            ok = False
            for t in typs1: 
                if (t in typs2): 
                    ok = True
                else: 
                    for tt in typs2: 
                        if (LanguageHelper.ends_with(tt, t) or LanguageHelper.ends_with(t, tt)): 
                            ok = True
            if (not ok): 
                return False
        if (self.higher is not None and geo_.higher is not None): 
            if (GeoReferent.__check_round_dep(self) or GeoReferent.__check_round_dep(geo_)): 
                return False
            if (self.higher.can_be_equals(geo_.higher, typ)): 
                pass
            elif (geo_.higher.higher is not None and self.higher.can_be_equals(geo_.higher.higher, typ)): 
                pass
            elif (self.higher.higher is not None and self.higher.higher.can_be_equals(geo_.higher, typ)): 
                pass
            else: 
                return False
        return True
    
    def _merge_slots2(self, obj : 'Referent', lang : 'MorphLang') -> None:
        merge_statistic = True
        for s in obj.slots: 
            if (s.type_name == GeoReferent.ATTR_NAME or s.type_name == GeoReferent.ATTR_TYPE): 
                nam = s.value
                if (LanguageHelper.is_latin_char(nam[0])): 
                    if (not lang.is_en): 
                        continue
                elif (lang.is_en): 
                    continue
                if (LanguageHelper.ends_with(nam, " ССР")): 
                    continue
            self.add_slot(s.type_name, s.value, False, (s.count if merge_statistic else 0))
        if (self.find_slot(GeoReferent.ATTR_NAME, None, True) is None and obj.find_slot(GeoReferent.ATTR_NAME, None, True) is not None): 
            for s in obj.slots: 
                if (s.type_name == GeoReferent.ATTR_NAME): 
                    self.add_slot(s.type_name, s.value, False, (s.count if merge_statistic else 0))
        if (self.find_slot(GeoReferent.ATTR_TYPE, None, True) is None and obj.find_slot(GeoReferent.ATTR_TYPE, None, True) is not None): 
            for s in obj.slots: 
                if (s.type_name == GeoReferent.ATTR_TYPE): 
                    self.add_slot(s.type_name, s.value, False, (s.count if merge_statistic else 0))
        if (self.is_territory): 
            if (((self.alpha2 is not None or self.find_slot(GeoReferent.ATTR_TYPE, "государство", True) is not None or self.find_slot(GeoReferent.ATTR_TYPE, "держава", True) is not None) or self.find_slot(GeoReferent.ATTR_TYPE, "империя", True) is not None or self.find_slot(GeoReferent.ATTR_TYPE, "імперія", True) is not None) or self.find_slot(GeoReferent.ATTR_TYPE, "state", True) is not None): 
                s = self.find_slot(GeoReferent.ATTR_TYPE, "территория", True)
                if (s is not None): 
                    self.slots.remove(s)
        if (self.is_state): 
            for s in self.slots: 
                if (s.type_name == GeoReferent.ATTR_TYPE and ((str(s.value) == "регион" or str(s.value) == "регіон" or str(s.value) == "region"))): 
                    self.slots.remove(s)
                    break
        if (self.is_city): 
            s = Utils.ifNotNull(self.find_slot(GeoReferent.ATTR_TYPE, "город", True), Utils.ifNotNull(self.find_slot(GeoReferent.ATTR_TYPE, "місто", True), self.find_slot(GeoReferent.ATTR_TYPE, "city", True)))
            if (s is not None): 
                for ss in self.slots: 
                    if (ss.type_name == GeoReferent.ATTR_TYPE and ss != s and GeoReferent.__is_city(ss.value)): 
                        self.slots.remove(s)
                        break
        has = False
        i = 0
        while i < len(self.slots): 
            if (self.slots[i].type_name == GeoReferent.ATTR_HIGHER): 
                if (not has): 
                    has = True
                else: 
                    del self.slots[i]
                    i -= 1
            i += 1
        self._merge_ext_referents(obj)
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        is_city_ = self.is_city
        oi = IntOntologyItem(self)
        for a in self.slots: 
            if (a.type_name == GeoReferent.ATTR_NAME): 
                s = str(a.value)
                t = Termin()
                t.init_by_normal_text(s, None)
                if (is_city_): 
                    t.add_std_abridges()
                oi.termins.append(t)
        return oi
    
    def _check_abbr(self, abbr : str) -> bool:
        if (len(abbr) != 2): 
            return False
        nameq = False
        typeq = False
        nameq2 = False
        typeq2 = False
        for s in self.slots: 
            if (s.type_name == GeoReferent.ATTR_NAME): 
                val = Utils.asObjectOrNull(s.value, str)
                ch = val[0]
                if (ch == abbr[0]): 
                    nameq = True
                    ii = val.find(' ')
                    if (ii > 0): 
                        if (abbr[1] == val[ii + 1]): 
                            if (Utils.indexOfList(val, ' ', ii + 1) < 0): 
                                return True
                if (ch == abbr[1]): 
                    nameq2 = True
            elif (s.type_name == GeoReferent.ATTR_TYPE): 
                ty = s.value
                if (ty == "государство" or ty == "держава" or ty == "country"): 
                    continue
                ch = str.upper(ty[0])
                if (ch == abbr[1]): 
                    typeq = True
                if (ch == abbr[0]): 
                    typeq2 = True
        if (typeq and nameq): 
            return True
        if (typeq2 and nameq2): 
            return True
        return False
    
    def _add_org_referent(self, org0_ : 'Referent') -> None:
        # Добавляем ссылку на организацию, также добавляем имена
        if (org0_ is None): 
            return
        nam = False
        self.add_slot(GeoReferent.ATTR_REF, org0_, False, 0)
        geo_ = None
        spec_typ = None
        num = org0_.get_string_value("NUMBER")
        for s in org0_.slots: 
            if (s.type_name == "NAME"): 
                if (num is None): 
                    self._add_name(Utils.asObjectOrNull(s.value, str))
                else: 
                    self._add_name("{0}-{1}".format(s.value, num))
                nam = True
            elif (s.type_name == "TYPE"): 
                v = Utils.asObjectOrNull(s.value, str)
                if (v == "СЕЛЬСКИЙ СОВЕТ"): 
                    self._add_typ("сельский округ")
                elif (v == "ГОРОДСКОЙ СОВЕТ"): 
                    self._add_typ("городской округ")
                elif (v == "ПОСЕЛКОВЫЙ СОВЕТ"): 
                    self._add_typ("поселковый округ")
                elif (v == "аэропорт"): 
                    spec_typ = v.upper()
            elif (s.type_name == "GEO" and (isinstance(s.value, GeoReferent))): 
                geo_ = (Utils.asObjectOrNull(s.value, GeoReferent))
        if (not nam): 
            for s in org0_.slots: 
                if (s.type_name == "EPONYM"): 
                    if (num is None): 
                        self._add_name(s.value.upper())
                    else: 
                        self._add_name("{0}-{1}".format(s.value.upper(), num))
                    nam = True
        if (not nam and num is not None): 
            for s in org0_.slots: 
                if (s.type_name == "TYPE"): 
                    self._add_name("{0}-{1}".format(s.value.upper(), num))
                    nam = True
        if (geo_ is not None and not nam): 
            for n in geo_.get_string_values(GeoReferent.ATTR_NAME): 
                self._add_name(n)
                if (spec_typ is not None): 
                    self._add_name("{0} {1}".format(n, spec_typ))
                    self._add_name("{0} {1}".format(spec_typ, n))
                nam = True
        if (not nam): 
            self._add_name(org0_.to_string(True, MorphLang.UNKNOWN, 0).upper())