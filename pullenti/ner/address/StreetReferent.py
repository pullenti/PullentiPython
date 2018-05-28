# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
import io
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.ner.address.StreetKind import StreetKind

from pullenti.ner.core.IntOntologyItem import IntOntologyItem


class StreetReferent(Referent):
    """ Улица, проспект, площадь, шоссе и т.п. """
    
    def __init__(self) -> None:
        from pullenti.ner.address.internal.MetaStreet import MetaStreet
        super().__init__(StreetReferent.OBJ_TYPENAME)
        self.instance_of = MetaStreet._global_meta
    
    OBJ_TYPENAME = "STREET"
    
    ATTR_TYP = "TYP"
    
    ATTR_NAME = "NAME"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_SECNUMBER = "SECNUMBER"
    
    ATTR_GEO = "GEO"
    
    ATTR_FIAS = "FIAS"
    
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
        from pullenti.ner.geo.GeoReferent import GeoReferent
        res = list()
        for a in self.slots: 
            if (a.type_name == StreetReferent.ATTR_GEO and isinstance(a.value, GeoReferent)): 
                res.append(a.value if isinstance(a.value, GeoReferent) else None)
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
        from pullenti.ner.geo.GeoReferent import GeoReferent
        return (self.get_value(StreetReferent.ATTR_GEO) if isinstance(self.get_value(StreetReferent.ATTR_GEO), GeoReferent) else None)
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        tmp = Utils.newStringIO(None)
        nam = self.get_string_value(StreetReferent.ATTR_NAME)
        typs_ = self.typs
        if (len(typs_) > 0): 
            for i in range(len(typs_)):
                if (nam is not None and typs_[i].upper() in nam): 
                    continue
                if (tmp.tell() > 0): 
                    print('/', end="", file=tmp)
                print(typs_[i], end="", file=tmp)
        else: 
            print(("вулиця" if lang.is_ua else "улица"), end="", file=tmp)
        if (self.number is not None): 
            print(" {0}".format(self.number), end="", file=tmp, flush=True)
            if (self.sec_number is not None): 
                print(" {0}".format(self.sec_number), end="", file=tmp, flush=True)
        if (nam is not None): 
            print(" {0}".format(MiscHelper.convert_first_char_upper_and_other_lower(nam)), end="", file=tmp, flush=True)
        if (not short_variant): 
            kladr = self.get_value(StreetReferent.ATTR_FIAS)
            if (isinstance(kladr, Referent)): 
                print(" (ФИАС: {0}".format(Utils.ifNotNull((kladr if isinstance(kladr, Referent) else None).get_string_value("GUID"), "?")), end="", file=tmp, flush=True)
                for s in self.slots: 
                    if (s.type_name == StreetReferent.ATTR_FIAS and isinstance(s.value, Referent) and s.value != kladr): 
                        print(", {0}".format(Utils.ifNotNull((s.value if isinstance(s.value, Referent) else None).get_string_value("GUID"), "?")), end="", file=tmp, flush=True)
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
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        return self.__can_be_equals(obj, typ, False)
    
    def __can_be_equals(self, obj : 'Referent', typ : 'EqualType', ignore_geo : bool) -> bool:
        stri = (obj if isinstance(obj, StreetReferent) else None)
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
        if (attr_name == StreetReferent.ATTR_NAME and isinstance(attr_value, str)): 
            str0 = (attr_value if isinstance(attr_value, str) else None)
            if (str0.find('.') > 0): 
                i = 1
                while i < (len(str0) - 1): 
                    if (str0[i] == '.' and str0[i + 1] != ' '): 
                        str0 = (str0[0 : (i + 1)] + " " + str0[i + 1 : ])
                    i += 1
            attr_value = str0
        return super().add_slot(attr_name, attr_value, clear_old_value, stat_count)
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().merge_slots(obj, merge_statistic)
    
    def can_be_general_for(self, obj : 'Referent') -> bool:
        if (not self.__can_be_equals(obj, Referent.EqualType.WITHINONETEXT, True)): 
            return False
        geos1 = self.geos
        geos2 = (obj if isinstance(obj, StreetReferent) else None).geos
        if (len(geos2) == 0 or len(geos1) > 0): 
            return False
        return True
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        from pullenti.ner.core.Termin import Termin
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