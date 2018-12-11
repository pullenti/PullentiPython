# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.keyword.KeywordType import KeywordType
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.core.Termin import Termin
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.keyword.internal.KeywordMeta import KeywordMeta
from pullenti.ner.Referent import Referent

class KeywordReferent(Referent):
    """ Оформление ключевых слов и комбинаций """
    
    def __init__(self) -> None:
        super().__init__(KeywordReferent.OBJ_TYPENAME)
        self.rank = 0
        self.instance_of = KeywordMeta.GLOBAL_META
    
    OBJ_TYPENAME = "KEYWORD"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_VALUE = "VALUE"
    
    ATTR_NORMAL = "NORMAL"
    
    ATTR_REF = "REF"
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        rank_ = self.rank
        val = self.getStringValue(KeywordReferent.ATTR_VALUE)
        if (val is None): 
            r = Utils.asObjectOrNull(self.getSlotValue(KeywordReferent.ATTR_REF), Referent)
            if (r is not None): 
                val = r.toString(True, lang, lev + 1)
            else: 
                val = self.getStringValue(KeywordReferent.ATTR_NORMAL)
        if (short_variant): 
            return Utils.ifNotNull(val, "?")
        norm = self.getStringValue(KeywordReferent.ATTR_NORMAL)
        if (norm is None): 
            return Utils.ifNotNull(val, "?")
        else: 
            return "{0} [{1}]".format(Utils.ifNotNull(val, "?"), norm)
    
    @property
    def typ(self) -> 'KeywordType':
        str0_ = self.getStringValue(KeywordReferent.ATTR_TYPE)
        if (str0_ is None): 
            return KeywordType.UNDEFINED
        try: 
            return Utils.valToEnum(str0_, KeywordType)
        except Exception as ex: 
            return KeywordType.UNDEFINED
    @typ.setter
    def typ(self, value) -> 'KeywordType':
        self.addSlot(KeywordReferent.ATTR_TYPE, Utils.enumToString(value), True, 0)
        return value
    
    @property
    def child_words(self) -> int:
        return self.__getChildWords(self, 0)
    
    def __getChildWords(self, root : 'KeywordReferent', lev : int) -> int:
        if (lev > 5): 
            return 0
        res = 0
        for s in self.slots: 
            if (s.type_name == KeywordReferent.ATTR_REF and (isinstance(s.value, KeywordReferent))): 
                if (s.value == root): 
                    return 0
                res += (s.value).__getChildWords(root, lev + 1)
        if (res == 0): 
            res = 1
        return res
    
    def canBeEquals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        kw = Utils.asObjectOrNull(obj, KeywordReferent)
        if (kw is None): 
            return False
        ki = self.typ
        if (ki != kw.typ): 
            return False
        if (ki == KeywordType.REFERENT): 
            re = Utils.asObjectOrNull(self.getSlotValue(KeywordReferent.ATTR_REF), Referent)
            if (re is None): 
                return False
            re2 = Utils.asObjectOrNull(kw.getSlotValue(KeywordReferent.ATTR_REF), Referent)
            if (re2 is None): 
                return False
            if (re.canBeEquals(re2, typ_)): 
                return True
        for s in self.slots: 
            if (s.type_name == KeywordReferent.ATTR_NORMAL or s.type_name == KeywordReferent.ATTR_VALUE): 
                if (kw.findSlot(KeywordReferent.ATTR_NORMAL, s.value, True) is not None): 
                    return True
                if (kw.findSlot(KeywordReferent.ATTR_VALUE, s.value, True) is not None): 
                    return True
        return False
    
    def mergeSlots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        r1 = self.rank + (obj).rank
        super().mergeSlots(obj, merge_statistic)
        if (len(self.slots) > 50): 
            pass
        self.rank = r1
    
    def _union(self, kw1 : 'KeywordReferent', kw2 : 'KeywordReferent', word2 : str) -> None:
        self.typ = kw1.typ
        tmp = list()
        tmp2 = io.StringIO()
        for v in kw1.getStringValues(KeywordReferent.ATTR_VALUE): 
            self.addSlot(KeywordReferent.ATTR_VALUE, "{0} {1}".format(v, word2), False, 0)
        norms1 = kw1.getStringValues(KeywordReferent.ATTR_NORMAL)
        if (len(norms1) == 0 and kw1.child_words == 1): 
            norms1 = kw1.getStringValues(KeywordReferent.ATTR_VALUE)
        norms2 = kw2.getStringValues(KeywordReferent.ATTR_NORMAL)
        if (len(norms2) == 0 and kw2.child_words == 1): 
            norms2 = kw2.getStringValues(KeywordReferent.ATTR_VALUE)
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
                self.addSlot(KeywordReferent.ATTR_NORMAL, Utils.toStringStringIO(tmp2), False, 0)
        self.addSlot(KeywordReferent.ATTR_REF, kw1, False, 0)
        self.addSlot(KeywordReferent.ATTR_REF, kw2, False, 0)
    
    def createOntologyItem(self) -> 'IntOntologyItem':
        res = IntOntologyItem(self)
        for s in self.slots: 
            if (s.type_name == KeywordReferent.ATTR_NORMAL or s.type_name == KeywordReferent.ATTR_VALUE): 
                res.termins.append(Termin(s.value))
        return res
    
    @staticmethod
    def _new1502(_arg1 : 'KeywordType') -> 'KeywordReferent':
        res = KeywordReferent()
        res.typ = _arg1
        return res