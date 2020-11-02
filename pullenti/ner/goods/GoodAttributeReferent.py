# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.core.Termin import Termin
from pullenti.ner.Referent import Referent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.goods.GoodAttrType import GoodAttrType
from pullenti.ner.goods.internal.AttrMeta import AttrMeta

class GoodAttributeReferent(Referent):
    """ Атрибут товара
    
    """
    
    def __init__(self) -> None:
        super().__init__(GoodAttributeReferent.OBJ_TYPENAME)
        self.instance_of = AttrMeta.GLOBAL_META
    
    OBJ_TYPENAME = "GOODATTR"
    """ Имя типа сущности TypeName ("GOODATTR") """
    
    ATTR_TYPE = "TYPE"
    """ Имя атрибута - тип атрибута (GoodAttrType) """
    
    ATTR_VALUE = "VALUE"
    """ Имя атрибута - значение атрибута """
    
    ATTR_ALTVALUE = "ALTVALUE"
    """ Имя атрибута - альтернативное значение атрибута """
    
    ATTR_UNIT = "UNIT"
    """ Имя атрибута - единица измерения """
    
    ATTR_NAME = "NAME"
    """ Имя атрибута - наименование атрибута """
    
    ATTR_REF = "REF"
    """ Имя атрибута - сслыка на сущность (Referent) """
    
    @property
    def typ(self) -> 'GoodAttrType':
        """ Тип атрибута """
        str0_ = self.get_string_value(GoodAttributeReferent.ATTR_TYPE)
        if (str0_ is None): 
            return GoodAttrType.UNDEFINED
        try: 
            return Utils.valToEnum(str0_, GoodAttrType)
        except Exception as ex1339: 
            pass
        return GoodAttrType.UNDEFINED
    @typ.setter
    def typ(self, value) -> 'GoodAttrType':
        self.add_slot(GoodAttributeReferent.ATTR_TYPE, Utils.enumToString(value).upper(), True, 0)
        return value
    
    @property
    def values(self) -> typing.List[str]:
        """ Значения (список string) """
        res = list()
        for s in self.slots: 
            if (s.type_name == GoodAttributeReferent.ATTR_VALUE and (isinstance(s.value, str))): 
                v = Utils.asObjectOrNull(s.value, str)
                if (v.find('(') > 0): 
                    if (self.typ == GoodAttrType.NUMERIC): 
                        v = v[0:0+v.find('(')].strip()
                res.append(v)
        return res
    
    @property
    def alt_values(self) -> typing.List[str]:
        """ Альтернативное представление значений (список string). Например, для значение ИКЕЯ здесь
        будут варианты написаний на латинице типа IKEA, IKEYA ... """
        res = list()
        for s in self.slots: 
            if (s.type_name == GoodAttributeReferent.ATTR_ALTVALUE and (isinstance(s.value, str))): 
                res.append(Utils.asObjectOrNull(s.value, str))
        return res
    
    @property
    def units(self) -> typing.List[str]:
        """ Единицы измерения (список string) """
        res = list()
        for s in self.slots: 
            if (s.type_name == GoodAttributeReferent.ATTR_UNIT and (isinstance(s.value, str))): 
                res.append(Utils.asObjectOrNull(s.value, str))
        return res
    
    @property
    def ref(self) -> 'Referent':
        """ Ссылка на внешнюю сущность """
        return Utils.asObjectOrNull(self.get_slot_value(GoodAttributeReferent.ATTR_REF), Referent)
    @ref.setter
    def ref(self, value) -> 'Referent':
        self.add_slot(GoodAttributeReferent.ATTR_REF, value, True, 0)
        return value
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        typ_ = self.typ
        nam = self.get_string_value(GoodAttributeReferent.ATTR_NAME)
        if (not short_variant): 
            if (typ_ != GoodAttrType.UNDEFINED): 
                print("{0}{1}: ".format(AttrMeta.GLOBAL_META.typ_attr.convert_inner_value_to_outer_value(Utils.enumToString(typ_), lang), ("" if nam is None else " ({0})".format(nam.lower()))), end="", file=res, flush=True)
        s = self.get_string_value(GoodAttributeReferent.ATTR_VALUE)
        if (s is not None): 
            if (typ_ == GoodAttrType.KEYWORD or typ_ == GoodAttrType.CHARACTER): 
                print(s.lower(), end="", file=res)
            elif (typ_ == GoodAttrType.NUMERIC): 
                vals = self.values
                units_ = self.units
                i = 0
                while i < len(vals): 
                    if (i > 0): 
                        print(" x ", end="", file=res)
                    print(vals[i], end="", file=res)
                    if (len(vals) == len(units_)): 
                        print(units_[i].lower(), end="", file=res)
                    elif (len(units_) > 0): 
                        print(units_[0].lower(), end="", file=res)
                    i += 1
            else: 
                print(s, end="", file=res)
        re = self.ref
        if (re is not None): 
            print(re.to_string(short_variant, lang, 0), end="", file=res)
        return Utils.toStringStringIO(res)
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        a = Utils.asObjectOrNull(obj, GoodAttributeReferent)
        if (a is None): 
            return False
        if (a.typ != self.typ): 
            return False
        u1 = self.get_string_value(GoodAttributeReferent.ATTR_UNIT)
        u2 = a.get_string_value(GoodAttributeReferent.ATTR_UNIT)
        if (u1 is not None and u2 is not None): 
            if (u1 != u2): 
                if (len(u1) == (len(u2) + 1) and u1 == (u2 + ".")): 
                    pass
                elif (len(u2) == (len(u1) + 1) and u2 == (u1 + ".")): 
                    pass
                return False
        nam1 = self.get_string_value(GoodAttributeReferent.ATTR_NAME)
        nam2 = a.get_string_value(GoodAttributeReferent.ATTR_NAME)
        if (nam1 is not None or nam2 is not None): 
            if (nam1 != nam2): 
                return False
        eq = False
        if (self.ref is not None or a.ref is not None): 
            if (self.ref is None or a.ref is None): 
                return False
            if (not self.ref.can_be_equals(a.ref, typ_)): 
                return False
            eq = True
        if (self.typ != GoodAttrType.NUMERIC): 
            for s in self.slots: 
                if (s.type_name == GoodAttributeReferent.ATTR_VALUE or s.type_name == GoodAttributeReferent.ATTR_ALTVALUE): 
                    if (a.find_slot(GoodAttributeReferent.ATTR_VALUE, s.value, True) is not None or a.find_slot(GoodAttributeReferent.ATTR_ALTVALUE, s.value, True) is not None): 
                        eq = True
                        break
        else: 
            vals1 = self.values
            vals2 = a.values
            if (len(vals1) != len(vals2)): 
                return False
            for v in vals1: 
                if (not v in vals2): 
                    return False
        if (not eq): 
            return False
        return True
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().merge_slots(obj, merge_statistic)
        for i in range(len(self.slots) - 1, -1, -1):
            if (self.slots[i].type_name == GoodAttributeReferent.ATTR_ALTVALUE): 
                if (self.find_slot(GoodAttributeReferent.ATTR_VALUE, self.slots[i].value, True) is not None): 
                    del self.slots[i]
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        re = IntOntologyItem(self)
        for s in self.slots: 
            if (s.type_name == GoodAttributeReferent.ATTR_VALUE or s.type_name == GoodAttributeReferent.ATTR_ALTVALUE): 
                re.termins.append(Termin(Utils.asObjectOrNull(s.value, str)))
        return re