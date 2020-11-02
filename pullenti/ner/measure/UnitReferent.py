# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.measure.internal.UnitMeta import UnitMeta

class UnitReferent(Referent):
    """ Единица измерения вместе с множителем
    
    """
    
    def __init__(self) -> None:
        super().__init__(UnitReferent.OBJ_TYPENAME)
        self._m_unit = None;
        self.instance_of = UnitMeta.GLOBAL_META
    
    OBJ_TYPENAME = "MEASUREUNIT"
    """ Имя типа сущности TypeName ("MEASUREUNIT") """
    
    ATTR_FULLNAME = "FULLNAME"
    """ Имя атрибута - полное имя единицы (например, километр) """
    
    ATTR_NAME = "NAME"
    """ Имя атрибута - краткое имя единицы (например, км) """
    
    ATTR_POW = "POW"
    """ Имя атрибута - степень, в которую нужно возвести """
    
    ATTR_BASEFACTOR = "BASEFACTOR"
    """ Имя атрибута - множитель для базовой единицы (чтобы приводить к единому знаменателю) """
    
    ATTR_BASEUNIT = "BASEUNIT"
    """ Имя атрибута - базовая единица """
    
    ATTR_UNKNOWN = "UNKNOWN"
    """ Имя атрибута - признак неизвестной (движку) метрики """
    
    @property
    def parent_referent(self) -> 'Referent':
        return Utils.asObjectOrNull(self.get_slot_value(UnitReferent.ATTR_BASEUNIT), Referent)
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        nam = None
        for l_ in range(2):
            for s in self.slots: 
                if (((s.type_name == UnitReferent.ATTR_NAME and short_variant)) or ((s.type_name == UnitReferent.ATTR_FULLNAME and not short_variant))): 
                    val = Utils.asObjectOrNull(s.value, str)
                    if (lang is not None and l_ == 0): 
                        if (lang.is_ru != LanguageHelper.is_cyrillic(val)): 
                            continue
                    nam = val
                    break
            if (nam is not None): 
                break
        if (nam is None): 
            nam = self.get_string_value(UnitReferent.ATTR_NAME)
        pow0_ = self.get_string_value(UnitReferent.ATTR_POW)
        if (Utils.isNullOrEmpty(pow0_) or lev > 0): 
            return Utils.ifNotNull(nam, "?")
        res = ("{0}{1}".format(nam, pow0_) if (pow0_[0] != '-') else "{0}<{1}>".format(nam, pow0_))
        if (not short_variant and self.is_unknown): 
            res = ("(?)" + res)
        return res
    
    @property
    def is_unknown(self) -> bool:
        """ Признак того, что это неизвестная метрика """
        return self.get_string_value(UnitReferent.ATTR_UNKNOWN) == "true"
    @is_unknown.setter
    def is_unknown(self, value) -> bool:
        self.add_slot(UnitReferent.ATTR_UNKNOWN, ("true" if value else None), True, 0)
        return value
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        ur = Utils.asObjectOrNull(obj, UnitReferent)
        if (ur is None): 
            return False
        for s in self.slots: 
            if (ur.find_slot(s.type_name, s.value, True) is None): 
                return False
        for s in ur.slots: 
            if (self.find_slot(s.type_name, s.value, True) is None): 
                return False
        return True