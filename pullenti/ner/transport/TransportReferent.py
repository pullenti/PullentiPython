# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.transport.internal.MetaTransport import MetaTransport
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.transport.TransportKind import TransportKind
from pullenti.ner.geo.GeoReferent import GeoReferent

class TransportReferent(Referent):
    """ Сущность - транспортное средство
    
    """
    
    def __init__(self) -> None:
        super().__init__(TransportReferent.OBJ_TYPENAME)
        self.instance_of = MetaTransport._global_meta
    
    OBJ_TYPENAME = "TRANSPORT"
    """ Имя типа сущности TypeName ("TRANSPORT") """
    
    ATTR_TYPE = "TYPE"
    """ Имя атрибута - тип """
    
    ATTR_BRAND = "BRAND"
    """ Имя атрибута - марка (производитель, бренд) """
    
    ATTR_MODEL = "MODEL"
    """ Имя атрибута - модель """
    
    ATTR_CLASS = "CLASS"
    """ Имя атрибута - класс """
    
    ATTR_NAME = "NAME"
    """ Имя атрибута - собственное имя (если есть, например, у кораблей) """
    
    ATTR_NUMBER = "NUMBER"
    """ Имя атрибута - номер """
    
    ATTR_NUMBER_REGION = "NUMBER_REG"
    """ Имя атрибута - номер региона """
    
    ATTR_KIND = "KIND"
    """ Имя атрибута - категория (TransportKind) """
    
    ATTR_GEO = "GEO"
    """ Имя атрибута - географический объект (GeoReferent) """
    
    ATTR_ORG = "ORG"
    """ Имя атрибута - организация (OrganizationReferent) """
    
    ATTR_DATE = "DATE"
    """ Имя атрибута - дата выпуска """
    
    ATTR_ROUTEPOINT = "ROUTEPOINT"
    """ Имя атрибута - пункт назначения """
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        str0_ = None
        for s in self.slots: 
            if (s.type_name == TransportReferent.ATTR_TYPE): 
                n = s.value
                if (str0_ is None or (len(n) < len(str0_))): 
                    str0_ = n
        if (str0_ is not None): 
            print(str0_, end="", file=res)
        elif (self.kind == TransportKind.AUTO): 
            print("автомобиль", end="", file=res)
        elif (self.kind == TransportKind.FLY): 
            print("самолет", end="", file=res)
        elif (self.kind == TransportKind.SHIP): 
            print("судно", end="", file=res)
        elif (self.kind == TransportKind.SPACE): 
            print("космический корабль", end="", file=res)
        else: 
            print(Utils.enumToString(self.kind), end="", file=res)
        str0_ = self.get_string_value(TransportReferent.ATTR_BRAND)
        if ((str0_) is not None): 
            print(" {0}".format(MiscHelper.convert_first_char_upper_and_other_lower(str0_)), end="", file=res, flush=True)
        str0_ = self.get_string_value(TransportReferent.ATTR_MODEL)
        if ((str0_) is not None): 
            print(" {0}".format(MiscHelper.convert_first_char_upper_and_other_lower(str0_)), end="", file=res, flush=True)
        str0_ = self.get_string_value(TransportReferent.ATTR_NAME)
        if ((str0_) is not None): 
            print(" \"{0}\"".format(MiscHelper.convert_first_char_upper_and_other_lower(str0_)), end="", file=res, flush=True)
            for s in self.slots: 
                if (s.type_name == TransportReferent.ATTR_NAME and str0_ != (s.value)): 
                    if (LanguageHelper.is_cyrillic_char(str0_[0]) != LanguageHelper.is_cyrillic_char(s.value[0])): 
                        print(" ({0})".format(MiscHelper.convert_first_char_upper_and_other_lower(s.value)), end="", file=res, flush=True)
                        break
        str0_ = self.get_string_value(TransportReferent.ATTR_CLASS)
        if ((str0_) is not None): 
            print(" класса \"{0}\"".format(MiscHelper.convert_first_char_upper_and_other_lower(str0_)), end="", file=res, flush=True)
        str0_ = self.get_string_value(TransportReferent.ATTR_NUMBER)
        if ((str0_) is not None): 
            print(", номер {0}".format(str0_), end="", file=res, flush=True)
            str0_ = self.get_string_value(TransportReferent.ATTR_NUMBER_REGION)
            if ((str0_) is not None): 
                print(str0_, end="", file=res)
        if (self.find_slot(TransportReferent.ATTR_ROUTEPOINT, None, True) is not None): 
            print(" (".format(), end="", file=res, flush=True)
            fi = True
            for s in self.slots: 
                if (s.type_name == TransportReferent.ATTR_ROUTEPOINT): 
                    if (fi): 
                        fi = False
                    else: 
                        print(" - ", end="", file=res)
                    if (isinstance(s.value, Referent)): 
                        print(s.value.to_string(True, lang, 0), end="", file=res)
                    else: 
                        print(s.value, end="", file=res)
            print(")", end="", file=res)
        if (not short_variant): 
            str0_ = self.get_string_value(TransportReferent.ATTR_GEO)
            if ((str0_) is not None): 
                print("; {0}".format(str0_), end="", file=res, flush=True)
            str0_ = self.get_string_value(TransportReferent.ATTR_ORG)
            if ((str0_) is not None): 
                print("; {0}".format(str0_), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def kind(self) -> 'TransportKind':
        """ Категория транспорта (авто, авиа, аква ...) """
        return self.__get_kind(self.get_string_value(TransportReferent.ATTR_KIND))
    @kind.setter
    def kind(self, value) -> 'TransportKind':
        if (value != TransportKind.UNDEFINED): 
            self.add_slot(TransportReferent.ATTR_KIND, Utils.enumToString(value), True, 0)
        return value
    
    def __get_kind(self, s : str) -> 'TransportKind':
        if (s is None): 
            return TransportKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, TransportKind)
            if (isinstance(res, TransportKind)): 
                return Utils.valToEnum(res, TransportKind)
        except Exception as ex2701: 
            pass
        return TransportKind.UNDEFINED
    
    def _add_geo(self, r : object) -> None:
        if (isinstance(r, GeoReferent)): 
            self.add_slot(TransportReferent.ATTR_GEO, r, False, 0)
        elif (isinstance(r, ReferentToken)): 
            if (isinstance(r.get_referent(), GeoReferent)): 
                self.add_slot(TransportReferent.ATTR_GEO, r.get_referent(), False, 0)
                self.add_ext_referent(Utils.asObjectOrNull(r, ReferentToken))
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        tr = Utils.asObjectOrNull(obj, TransportReferent)
        if (tr is None): 
            return False
        k1 = self.kind
        k2 = tr.kind
        if (k1 != k2): 
            if (k1 == TransportKind.SPACE and tr.find_slot(TransportReferent.ATTR_TYPE, "КОРАБЛЬ", True) is not None): 
                pass
            elif (k2 == TransportKind.SPACE and self.find_slot(TransportReferent.ATTR_TYPE, "КОРАБЛЬ", True) is not None): 
                k1 = TransportKind.SPACE
            else: 
                return False
        sl = self.find_slot(TransportReferent.ATTR_ORG, None, True)
        if (sl is not None and tr.find_slot(TransportReferent.ATTR_ORG, None, True) is not None): 
            if (tr.find_slot(TransportReferent.ATTR_ORG, sl.value, False) is None): 
                return False
        sl = self.find_slot(TransportReferent.ATTR_GEO, None, True)
        if (sl is not None and tr.find_slot(TransportReferent.ATTR_GEO, None, True) is not None): 
            if (tr.find_slot(TransportReferent.ATTR_GEO, sl.value, True) is None): 
                return False
        s1 = self.get_string_value(TransportReferent.ATTR_NUMBER)
        s2 = tr.get_string_value(TransportReferent.ATTR_NUMBER)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == ReferentsEqualType.DIFFERENTTEXTS): 
                    return False
            else: 
                if (s1 != s2): 
                    return False
                s1 = self.get_string_value(TransportReferent.ATTR_NUMBER_REGION)
                s2 = tr.get_string_value(TransportReferent.ATTR_NUMBER_REGION)
                if (s1 is not None or s2 is not None): 
                    if (s1 is None or s2 is None): 
                        if (typ == ReferentsEqualType.DIFFERENTTEXTS): 
                            return False
                    elif (s1 != s2): 
                        return False
        s1 = self.get_string_value(TransportReferent.ATTR_BRAND)
        s2 = tr.get_string_value(TransportReferent.ATTR_BRAND)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == ReferentsEqualType.DIFFERENTTEXTS): 
                    return False
            elif (s1 != s2): 
                return False
        s1 = self.get_string_value(TransportReferent.ATTR_MODEL)
        s2 = tr.get_string_value(TransportReferent.ATTR_MODEL)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == ReferentsEqualType.DIFFERENTTEXTS): 
                    return False
            elif (s1 != s2): 
                return False
        for s in self.slots: 
            if (s.type_name == TransportReferent.ATTR_NAME): 
                if (tr.find_slot(TransportReferent.ATTR_NAME, s.value, True) is not None): 
                    return True
        if (s1 is not None and s2 is not None): 
            return True
        return False
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().merge_slots(obj, merge_statistic)
        kinds = list()
        for s in self.slots: 
            if (s.type_name == TransportReferent.ATTR_KIND): 
                ki = self.__get_kind(s.value)
                if (not ki in kinds): 
                    kinds.append(ki)
        if (len(kinds) > 0): 
            if (TransportKind.SPACE in kinds): 
                for i in range(len(self.slots) - 1, -1, -1):
                    if (self.slots[i].type_name == TransportReferent.ATTR_KIND and self.__get_kind(self.slots[i].value) != TransportKind.SPACE): 
                        del self.slots[i]
    
    def _check(self, on_attach : bool, brandisdoubt : bool) -> bool:
        ki = self.kind
        if (ki == TransportKind.UNDEFINED): 
            return False
        if (self.find_slot(TransportReferent.ATTR_NUMBER, None, True) is not None): 
            if (self.find_slot(TransportReferent.ATTR_NUMBER_REGION, None, True) is None and (len(self.slots) < 3)): 
                return False
            return True
        model = self.get_string_value(TransportReferent.ATTR_MODEL)
        has_num = False
        if (model is not None): 
            for s in model: 
                if (not str.isalpha(s)): 
                    has_num = True
                    break
        if (ki == TransportKind.AUTO): 
            if (self.find_slot(TransportReferent.ATTR_BRAND, None, True) is not None): 
                if (on_attach): 
                    return True
                if (not has_num and self.find_slot(TransportReferent.ATTR_TYPE, None, True) is None): 
                    return False
                if (brandisdoubt and model is None and not has_num): 
                    return False
                return True
            if (model is not None and on_attach): 
                return True
            return False
        if (model is not None): 
            if (not has_num and ki == TransportKind.FLY and self.find_slot(TransportReferent.ATTR_BRAND, None, True) is None): 
                return False
            return True
        if (self.find_slot(TransportReferent.ATTR_NAME, None, True) is not None): 
            nam = self.get_string_value(TransportReferent.ATTR_NAME)
            if (ki == TransportKind.FLY and nam.startswith("Аэрофлот")): 
                return False
            return True
        if (ki == TransportKind.TRAIN): 
            pass
        return False