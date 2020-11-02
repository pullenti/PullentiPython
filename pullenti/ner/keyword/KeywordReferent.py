# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.keyword.KeywordType import KeywordType
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.Referent import Referent
from pullenti.ner.keyword.internal.KeywordMeta import KeywordMeta

class KeywordReferent(Referent):
    """ Ключевая комбинация
    
    """
    
    def __init__(self) -> None:
        super().__init__(KeywordReferent.OBJ_TYPENAME)
        self.rank = 0
        self.instance_of = KeywordMeta.GLOBAL_META
    
    OBJ_TYPENAME = "KEYWORD"
    """ Имя типа сущности TypeName ("KEYWORD") """
    
    ATTR_TYPE = "TYPE"
    """ Имя атрибута - тип (KeywordType) """
    
    ATTR_VALUE = "VALUE"
    """ Имя атрибута - значение """
    
    ATTR_NORMAL = "NORMAL"
    """ Имя атрибута - нормализованное значение """
    
    ATTR_REF = "REF"
    """ Имя атрибута - ссылка на сущность, если это она """
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        if (lev > 10): 
            return "?"
        rank_ = self.rank
        val = self.get_string_value(KeywordReferent.ATTR_VALUE)
        if (val is None): 
            r = Utils.asObjectOrNull(self.get_slot_value(KeywordReferent.ATTR_REF), Referent)
            if (r is not None): 
                val = r.to_string(True, lang, lev + 1)
            else: 
                val = self.get_string_value(KeywordReferent.ATTR_NORMAL)
        if (short_variant): 
            return Utils.ifNotNull(val, "?")
        norm = self.get_string_value(KeywordReferent.ATTR_NORMAL)
        if (norm is None): 
            return Utils.ifNotNull(val, "?")
        else: 
            return "{0} [{1}]".format(Utils.ifNotNull(val, "?"), norm)
    
    @property
    def typ(self) -> 'KeywordType':
        """ Тип ключевой комбинации """
        str0_ = self.get_string_value(KeywordReferent.ATTR_TYPE)
        if (str0_ is None): 
            return KeywordType.UNDEFINED
        try: 
            return Utils.valToEnum(str0_, KeywordType)
        except Exception as ex: 
            return KeywordType.UNDEFINED
    @typ.setter
    def typ(self, value_) -> 'KeywordType':
        self.add_slot(KeywordReferent.ATTR_TYPE, Utils.enumToString(value_), True, 0)
        return value_
    
    @property
    def value(self) -> str:
        """ Ненормализованное значение """
        return self.get_string_value(KeywordReferent.ATTR_VALUE)
    @value.setter
    def value(self, value_) -> str:
        self.add_slot(KeywordReferent.ATTR_VALUE, value_, False, 0)
        return value_
    
    @property
    def normal_value(self) -> str:
        """ Нормализованное значение """
        return self.get_string_value(KeywordReferent.ATTR_NORMAL)
    @normal_value.setter
    def normal_value(self, value_) -> str:
        self.add_slot(KeywordReferent.ATTR_NORMAL, value_, False, 0)
        return value_
    
    @property
    def child_words(self) -> int:
        return self.__get_child_words(self, 0)
    
    def __get_child_words(self, root : 'KeywordReferent', lev : int) -> int:
        if (lev > 5): 
            return 0
        res = 0
        for s in self.slots: 
            if (s.type_name == KeywordReferent.ATTR_REF and (isinstance(s.value, KeywordReferent))): 
                if (s.value == root): 
                    return 0
                res += s.value.__get_child_words(root, lev + 1)
        if (res == 0): 
            res = 1
        return res
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        kw = Utils.asObjectOrNull(obj, KeywordReferent)
        if (kw is None): 
            return False
        ki = self.typ
        if (ki != kw.typ): 
            return False
        if (ki == KeywordType.REFERENT): 
            re = Utils.asObjectOrNull(self.get_slot_value(KeywordReferent.ATTR_REF), Referent)
            if (re is None): 
                return False
            re2 = Utils.asObjectOrNull(kw.get_slot_value(KeywordReferent.ATTR_REF), Referent)
            if (re2 is None): 
                return False
            if (re.can_be_equals(re2, typ_)): 
                return True
        for s in self.slots: 
            if (s.type_name == KeywordReferent.ATTR_NORMAL or s.type_name == KeywordReferent.ATTR_VALUE): 
                if (kw.find_slot(KeywordReferent.ATTR_NORMAL, s.value, True) is not None): 
                    return True
                if (kw.find_slot(KeywordReferent.ATTR_VALUE, s.value, True) is not None): 
                    return True
        return False
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        r1 = self.rank + obj.rank
        super().merge_slots(obj, merge_statistic)
        if (len(self.slots) > 50): 
            pass
        self.rank = r1
    
    def _union(self, kw1 : 'KeywordReferent', kw2 : 'KeywordReferent', word2 : str) -> None:
        self.typ = kw1.typ
        tmp = list()
        tmp2 = io.StringIO()
        for v in kw1.get_string_values(KeywordReferent.ATTR_VALUE): 
            self.add_slot(KeywordReferent.ATTR_VALUE, "{0} {1}".format(v, word2), False, 0)
        norms1 = kw1.get_string_values(KeywordReferent.ATTR_NORMAL)
        if (len(norms1) == 0 and kw1.child_words == 1): 
            norms1 = kw1.get_string_values(KeywordReferent.ATTR_VALUE)
        norms2 = kw2.get_string_values(KeywordReferent.ATTR_NORMAL)
        if (len(norms2) == 0 and kw2.child_words == 1): 
            norms2 = kw2.get_string_values(KeywordReferent.ATTR_VALUE)
        for n1 in norms1: 
            for n2 in norms2: 
                tmp.clear()
                tmp.extend(Utils.splitString(n1, ' ', False))
                for n in Utils.splitString(n2, ' ', False): 
                    if (not n in tmp): 
                        tmp.append(n)
                tmp.sort()
                Utils.setLengthStringIO(tmp2, 0)
                i = 0
                while i < len(tmp): 
                    if (i > 0): 
                        print(' ', end="", file=tmp2)
                    print(tmp[i], end="", file=tmp2)
                    i += 1
                self.add_slot(KeywordReferent.ATTR_NORMAL, Utils.toStringStringIO(tmp2), False, 0)
        self.add_slot(KeywordReferent.ATTR_REF, kw1, False, 0)
        self.add_slot(KeywordReferent.ATTR_REF, kw2, False, 0)
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        res = IntOntologyItem(self)
        for s in self.slots: 
            if (s.type_name == KeywordReferent.ATTR_NORMAL or s.type_name == KeywordReferent.ATTR_VALUE): 
                res.termins.append(Termin(s.value))
        return res
    
    @staticmethod
    def _new1591(_arg1 : 'KeywordType') -> 'KeywordReferent':
        res = KeywordReferent()
        res.typ = _arg1
        return res