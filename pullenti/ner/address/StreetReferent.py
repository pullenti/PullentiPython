# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.Referent import Referent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.address.internal.MetaStreet import MetaStreet
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.geo.GeoReferent import GeoReferent

class StreetReferent(Referent):
    """ Сущность: улица, проспект, площадь, шоссе и т.п. Выделяется анализатором AddressAnalyzer.
    
    """
    
    def __init__(self) -> None:
        super().__init__(StreetReferent.OBJ_TYPENAME)
        self.instance_of = MetaStreet._global_meta
    
    OBJ_TYPENAME = "STREET"
    """ Имя типа сущности TypeName ("STREET") """
    
    ATTR_TYP = "TYP"
    """ Имя атрибута - тип (улица, переулок, площадь...) """
    
    ATTR_NAME = "NAME"
    """ Имя атрибута - наименование (м.б. несколько вариантов) """
    
    ATTR_NUMBER = "NUMBER"
    """ Имя атрибута - номер """
    
    ATTR_SECNUMBER = "SECNUMBER"
    """ Имя атрибута - дополнительный номер """
    
    ATTR_GEO = "GEO"
    """ Имя атрибута - географический объект """
    
    ATTR_FIAS = "FIAS"
    """ Имя атрибута - код ФИАС (определяется анализатором FiasAnalyzer) """
    
    ATTR_BTI = "BTI"
    
    ATTR_OKM = "OKM"
    
    @property
    def typs(self) -> typing.List[str]:
        """ Тип(ы) """
        res = list()
        for s in self.slots: 
            if (s.type_name == StreetReferent.ATTR_TYP): 
                res.append(s.value)
        return res
    
    @property
    def names(self) -> typing.List[str]:
        """ Наименования """
        res = list()
        for s in self.slots: 
            if (s.type_name == StreetReferent.ATTR_NAME): 
                res.append(s.value)
        return res
    
    @property
    def number(self) -> str:
        """ Номер улицы (16-я Парковая) """
        return self.get_string_value(StreetReferent.ATTR_NUMBER)
    @number.setter
    def number(self, value) -> str:
        self.add_slot(StreetReferent.ATTR_NUMBER, value, True, 0)
        return value
    
    @property
    def sec_number(self) -> str:
        """ Дополнительный номер (3-я 1 Мая) """
        return self.get_string_value(StreetReferent.ATTR_SECNUMBER)
    @sec_number.setter
    def sec_number(self, value) -> str:
        self.add_slot(StreetReferent.ATTR_SECNUMBER, value, True, 0)
        return value
    
    @property
    def geos(self) -> typing.List['GeoReferent']:
        """ Ссылка на географические объекты """
        res = list()
        for a in self.slots: 
            if (a.type_name == StreetReferent.ATTR_GEO and (isinstance(a.value, GeoReferent))): 
                res.append(Utils.asObjectOrNull(a.value, GeoReferent))
        return res
    
    @property
    def city(self) -> 'GeoReferent':
        """ Город """
        for g in self.geos: 
            if (g.is_city): 
                return g
            elif (g.higher is not None and g.higher.is_city): 
                return g.higher
        return None
    
    @property
    def parent_referent(self) -> 'Referent':
        return Utils.asObjectOrNull(self.get_slot_value(StreetReferent.ATTR_GEO), GeoReferent)
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        tmp = io.StringIO()
        nam = self.get_string_value(StreetReferent.ATTR_NAME)
        typs_ = self.typs
        if (len(typs_) > 0): 
            i = 0
            first_pass3509 = True
            while True:
                if first_pass3509: first_pass3509 = False
                else: i += 1
                if (not (i < len(typs_))): break
                if (nam is not None and typs_[i].upper() in nam): 
                    continue
                if (tmp.tell() > 0): 
                    print('/', end="", file=tmp)
                print(typs_[i], end="", file=tmp)
        else: 
            print(("вулиця" if lang is not None and lang.is_ua else "улица"), end="", file=tmp)
        if (self.number is not None): 
            print(" {0}".format(self.number), end="", file=tmp, flush=True)
            if (self.sec_number is not None): 
                print(" {0}".format(self.sec_number), end="", file=tmp, flush=True)
        if (nam is not None): 
            print(" {0}".format(MiscHelper.convert_first_char_upper_and_other_lower(nam)), end="", file=tmp, flush=True)
        if (not short_variant): 
            kladr = self.get_slot_value(StreetReferent.ATTR_FIAS)
            if (isinstance(kladr, Referent)): 
                print(" (ФИАС: {0}".format(Utils.ifNotNull(kladr.get_string_value("GUID"), "?")), end="", file=tmp, flush=True)
                for s in self.slots: 
                    if (s.type_name == StreetReferent.ATTR_FIAS and (isinstance(s.value, Referent)) and s.value != kladr): 
                        print(", {0}".format(Utils.ifNotNull(s.value.get_string_value("GUID"), "?")), end="", file=tmp, flush=True)
                print(')', end="", file=tmp)
            bti = self.get_string_value(StreetReferent.ATTR_BTI)
            if (bti is not None): 
                print(" (БТИ {0})".format(bti), end="", file=tmp, flush=True)
            okm = self.get_string_value(StreetReferent.ATTR_OKM)
            if (okm is not None): 
                print(" (ОКМ УМ {0})".format(okm), end="", file=tmp, flush=True)
        if (not short_variant and self.city is not None): 
            print("; {0}".format(self.city.to_string(True, lang, lev + 1)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @property
    def kind(self) -> 'StreetKind':
        """ Классификатор """
        for t in self.typs: 
            if ("дорога" in t): 
                return StreetKind.ROAD
            elif ("метро" in t): 
                return StreetKind.METRO
        return StreetKind.UNDEFINED
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        return self.__can_be_equals(obj, typ, False)
    
    def __can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType', ignore_geo : bool) -> bool:
        stri = Utils.asObjectOrNull(obj, StreetReferent)
        if (stri is None): 
            return False
        if (self.kind != stri.kind): 
            return False
        typs1 = self.typs
        typs2 = stri.typs
        ok = False
        if (len(typs1) > 0 and len(typs2) > 0): 
            for t in typs1: 
                if (t in typs2): 
                    ok = True
                    break
            if (not ok): 
                return False
        num = self.number
        num1 = stri.number
        if (num is not None or num1 is not None): 
            if (num is None or num1 is None): 
                return False
            sec = self.sec_number
            sec1 = stri.sec_number
            if (sec is None and sec1 is None): 
                if (num != num1): 
                    return False
            elif (num == num1): 
                if (sec != sec1): 
                    return False
            elif (sec == num1 and sec1 == num): 
                pass
            else: 
                return False
        names1 = self.names
        names2 = stri.names
        if (len(names1) > 0 or len(names2) > 0): 
            ok = False
            for n in names1: 
                if (n in names2): 
                    ok = True
                    break
            if (not ok): 
                return False
        if (ignore_geo): 
            return True
        geos1 = self.geos
        geos2 = stri.geos
        if (len(geos1) > 0 and len(geos2) > 0): 
            ok = False
            for g1 in geos1: 
                for g2 in geos2: 
                    if (g1.can_be_equals(g2, typ)): 
                        ok = True
                        break
            if (not ok): 
                if (self.city is not None and stri.city is not None): 
                    ok = self.city.can_be_equals(stri.city, typ)
            if (not ok): 
                return False
        return True
    
    def add_slot(self, attr_name : str, attr_value : object, clear_old_value : bool, stat_count : int=0) -> 'Slot':
        if (attr_name == StreetReferent.ATTR_NAME and (isinstance(attr_value, str))): 
            str0_ = Utils.asObjectOrNull(attr_value, str)
            if (str0_.find('.') > 0): 
                i = 1
                while i < (len(str0_) - 1): 
                    if (str0_[i] == '.' and str0_[i + 1] != ' '): 
                        str0_ = (str0_[0:0+i + 1] + " " + str0_[i + 1:])
                    i += 1
            attr_value = (str0_)
        return super().add_slot(attr_name, attr_value, clear_old_value, stat_count)
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().merge_slots(obj, merge_statistic)
    
    def can_be_general_for(self, obj : 'Referent') -> bool:
        if (not self.__can_be_equals(obj, ReferentsEqualType.WITHINONETEXT, True)): 
            return False
        geos1 = self.geos
        geos2 = obj.geos
        if (len(geos2) == 0 or len(geos1) > 0): 
            return False
        return True
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        oi = IntOntologyItem(self)
        names_ = self.names
        for n in names_: 
            oi.termins.append(Termin(n))
        return oi
    
    def _correct(self) -> None:
        names_ = self.names
        for i in range(len(names_) - 1, -1, -1):
            ss = names_[i]
            jj = ss.find(' ')
            if (jj < 0): 
                continue
            if (ss.rfind(' ') != jj): 
                continue
            pp = Utils.splitString(ss, ' ', False)
            if (len(pp) == 2): 
                ss2 = "{0} {1}".format(pp[1], pp[0])
                if (not ss2 in names_): 
                    self.add_slot(StreetReferent.ATTR_NAME, ss2, False, 0)