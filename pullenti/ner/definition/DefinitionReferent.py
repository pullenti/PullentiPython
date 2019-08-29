# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.ner.definition.DefinitionKind import DefinitionKind
from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.definition.internal.MetaDefin import MetaDefin

class DefinitionReferent(Referent):
    """ Сущность, моделирующая определение (утверждение, тезис) """
    
    def __init__(self) -> None:
        super().__init__(DefinitionReferent.OBJ_TYPENAME)
        self.instance_of = MetaDefin._global_meta
    
    OBJ_TYPENAME = "THESIS"
    
    ATTR_TERMIN = "TERMIN"
    
    ATTR_TERMIN_ADD = "TERMINADD"
    
    ATTR_VALUE = "VALUE"
    
    ATTR_MISC = "MISC"
    
    ATTR_KIND = "KIND"
    
    ATTR_DECREE = "DECREE"
    
    @property
    def termin(self) -> str:
        """ Термин """
        return self.get_string_value(DefinitionReferent.ATTR_TERMIN)
    
    @property
    def termin_add(self) -> str:
        """ Дополнительный атрибут термина ("как наука", "в широком смысле" ...) """
        return self.get_string_value(DefinitionReferent.ATTR_TERMIN_ADD)
    
    @property
    def value(self) -> str:
        """ Собственно определение (правая часть) """
        return self.get_string_value(DefinitionReferent.ATTR_VALUE)
    
    @property
    def kind(self) -> 'DefinitionKind':
        """ Тип определение """
        s = self.get_string_value(DefinitionReferent.ATTR_KIND)
        if (s is None): 
            return DefinitionKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, DefinitionKind)
            if (isinstance(res, DefinitionKind)): 
                return Utils.valToEnum(res, DefinitionKind)
        except Exception as ex1125: 
            pass
        return DefinitionKind.UNDEFINED
    @kind.setter
    def kind(self, value_) -> 'DefinitionKind':
        self.add_slot(DefinitionReferent.ATTR_KIND, Utils.enumToString(value_), True, 0)
        return value_
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        misc = self.get_string_value(DefinitionReferent.ATTR_TERMIN_ADD)
        if (misc is None): 
            misc = self.get_string_value(DefinitionReferent.ATTR_MISC)
        return "[{0}] {1}{2} = {3}".format(Utils.enumToString(self.kind), Utils.ifNotNull(self.termin, "?"), ("" if misc is None else " ({0})".format(misc)), Utils.ifNotNull(self.value, "?"))
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType') -> bool:
        dr = Utils.asObjectOrNull(obj, DefinitionReferent)
        if (dr is None): 
            return False
        if (self.termin != dr.termin): 
            return False
        if (self.value != dr.value): 
            return False
        if (self.termin_add != dr.termin_add): 
            return False
        return True
    
    @staticmethod
    def _new1121(_arg1 : 'DefinitionKind') -> 'DefinitionReferent':
        res = DefinitionReferent()
        res.kind = _arg1
        return res