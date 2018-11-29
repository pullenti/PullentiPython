# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.ner.definition.DefinitionKind import DefinitionKind
from pullenti.morph.MorphLang import MorphLang


class DefinitionReferent(Referent):
    """ Сущность, моделирующая определение (утверждение, тезис) """
    
    def __init__(self) -> None:
        from pullenti.ner.definition.internal.MetaDefin import MetaDefin
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
        return self.getStringValue(DefinitionReferent.ATTR_TERMIN)
    
    @property
    def termin_add(self) -> str:
        """ Дополнительный атрибут термина ("как наука", "в широком смысле" ...) """
        return self.getStringValue(DefinitionReferent.ATTR_TERMIN_ADD)
    
    @property
    def value(self) -> str:
        """ Собственно определение (правая часть) """
        return self.getStringValue(DefinitionReferent.ATTR_VALUE)
    
    @property
    def kind(self) -> 'DefinitionKind':
        """ Тип определение """
        s = self.getStringValue(DefinitionReferent.ATTR_KIND)
        if (s is None): 
            return DefinitionKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, DefinitionKind)
            if (isinstance(res, DefinitionKind)): 
                return Utils.valToEnum(res, DefinitionKind)
        except Exception as ex1109: 
            pass
        return DefinitionKind.UNDEFINED
    @kind.setter
    def kind(self, value_) -> 'DefinitionKind':
        self.addSlot(DefinitionReferent.ATTR_KIND, Utils.enumToString(value_), True, 0)
        return value_
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=MorphLang(), lev : int=0) -> str:
        misc = self.getStringValue(DefinitionReferent.ATTR_TERMIN_ADD)
        if (misc is None): 
            misc = self.getStringValue(DefinitionReferent.ATTR_MISC)
        return "[{0}] {1}{2} = {3}".format(Utils.enumToString(self.kind), Utils.ifNotNull(self.termin, "?"), ("" if misc is None else " ({0})".format(misc)), Utils.ifNotNull(self.value, "?"))
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType') -> bool:
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
    def _new1105(_arg1 : 'DefinitionKind') -> 'DefinitionReferent':
        res = DefinitionReferent()
        res.kind = _arg1
        return res