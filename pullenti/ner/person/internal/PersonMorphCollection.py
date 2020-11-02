# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.person.internal.PersonItemToken import PersonItemToken

class PersonMorphCollection:
    
    class PersonMorphVariant:
        
        def __init__(self) -> None:
            self.value = None;
            self.short_value = None;
            self.gender = MorphGender.UNDEFINED
        
        def __str__(self) -> str:
            from pullenti.morph.MorphGender import MorphGender
            res = io.StringIO()
            print(self.value, end="", file=res)
            if (self.short_value is not None): 
                print(" ({0})".format(self.short_value), end="", file=res, flush=True)
            if (self.gender != MorphGender.UNDEFINED): 
                print(" {0}".format(Utils.enumToString(self.gender)), end="", file=res, flush=True)
            return Utils.toStringStringIO(res)
        
        @staticmethod
        def _new2587(_arg1 : str, _arg2 : 'MorphGender', _arg3 : str) -> 'PersonMorphVariant':
            res = PersonMorphCollection.PersonMorphVariant()
            res.value = _arg1
            res.gender = _arg2
            res.short_value = _arg3
            return res
    
    class SortComparer(object):
        
        def compare(self, x : 'PersonMorphVariant', y : 'PersonMorphVariant') -> int:
            if (x.value.find('-') > 0): 
                if ((y.value.find('-') < 0) and (len(y.value) < (len(x.value) - 1))): 
                    return -1
            elif (y.value.find('-') > 0 and (len(y.value) - 1) > len(x.value)): 
                return 1
            if (len(x.value) < len(y.value)): 
                return -1
            if (len(x.value) > len(y.value)): 
                return 1
            return 0
    
    def __init__(self) -> None:
        self.head = None;
        self.items = list()
        self.number = 0
    
    def check_latin_variant(self, latin : str) -> bool:
        for it in self.items: 
            if (MiscHelper.can_be_equal_cyr_and_latss(latin, it.value)): 
                return True
        return False
    
    def correct(self) -> None:
        for it in self.items: 
            if (it.value.find(' ') > 0): 
                it.value = it.value.replace(" ", "")
        i = 0
        while i < (len(self.items) - 1): 
            k = 0
            while k < (len(self.items) - 1): 
                if (PersonMorphCollection.M_COMPARER.compare(self.items[k], self.items[k + 1]) > 0): 
                    it = self.items[k + 1]
                    self.items[k + 1] = self.items[k]
                    self.items[k] = it
                k += 1
            i += 1
    
    M_COMPARER = None
    
    @property
    def has_lastname_standard_tail(self) -> bool:
        for it in self.items: 
            if (PersonItemToken.MorphPersonItem.ends_with_std_surname(it.value)): 
                return True
        return False
    
    def add(self, val : str, shortval : str, gen : 'MorphGender', add_other_gender_var : bool=False) -> None:
        if (val is None): 
            return
        if (self.head is None): 
            if (len(val) > 3): 
                self.head = val[0:0+3]
            else: 
                self.head = val
        if (gen == MorphGender.MASCULINE or gen == MorphGender.FEMINIE): 
            for it in self.items: 
                if (it.value == val and it.gender == gen): 
                    return
            self.items.append(PersonMorphCollection.PersonMorphVariant._new2587(val, gen, shortval))
            if (add_other_gender_var): 
                g0 = (MorphGender.MASCULINE if gen == MorphGender.FEMINIE else MorphGender.FEMINIE)
                v = MorphologyService.get_wordform(val, MorphBaseInfo._new193(MorphClass._new2568(True), g0))
                if (v is not None): 
                    self.items.append(PersonMorphCollection.PersonMorphVariant._new2587(v, g0, shortval))
        else: 
            self.add(val, shortval, MorphGender.MASCULINE, False)
            self.add(val, shortval, MorphGender.FEMINIE, False)
    
    def remove(self, val : str, gen : 'MorphGender') -> bool:
        ret = False
        for i in range(len(self.items) - 1, -1, -1):
            if (val is not None and self.items[i].value != val): 
                continue
            if (gen != MorphGender.UNDEFINED and self.items[i].gender != gen): 
                continue
            del self.items[i]
            ret = True
        return ret
    
    def add_prefix_str(self, prefix : str) -> None:
        self.head = "{0}{1}".format(prefix, self.head)
        for it in self.items: 
            it.value = "{0}{1}".format(prefix, it.value)
            if (it.short_value is not None): 
                it.value = "{0}{1}".format(prefix, it.short_value)
    
    @staticmethod
    def add_prefix(prefix : 'PersonMorphCollection', body : 'PersonMorphCollection') -> 'PersonMorphCollection':
        res = PersonMorphCollection()
        res.head = "{0}-{1}".format(prefix.head, body.head)
        for pv in prefix.items: 
            for bv in body.items: 
                g = bv.gender
                if (g == MorphGender.UNDEFINED): 
                    g = pv.gender
                elif (pv.gender != MorphGender.UNDEFINED and pv.gender != g): 
                    g = MorphGender.UNDEFINED
                res.add("{0}-{1}".format(pv.value, bv.value), None, g, False)
        return res
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.number > 0): 
            print("Num={0};".format(self.number), end="", file=res, flush=True)
        for it in self.items: 
            print("{0}; ".format(str(it)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def values(self) -> typing.List[str]:
        res = list()
        for it in self.items: 
            if (not it.value in res): 
                res.append(it.value)
            if (it.short_value is not None and not it.short_value in res): 
                res.append(it.short_value)
        return res
    
    @property
    def gender(self) -> 'MorphGender':
        res = MorphGender.UNDEFINED
        for it in self.items: 
            res = (Utils.valToEnum((res) | (it.gender), MorphGender))
        if (res == MorphGender.FEMINIE or res == MorphGender.MASCULINE): 
            return res
        else: 
            return MorphGender.UNDEFINED
    
    def __contains_item(self, v : str, g : 'MorphGender') -> bool:
        for it in self.items: 
            if (it.value == v and it.gender == g): 
                return True
        return False
    
    @staticmethod
    def is_equals(col1 : 'PersonMorphCollection', col2 : 'PersonMorphCollection') -> bool:
        if (col1.head != col2.head): 
            return False
        for v in col1.items: 
            if (not col2.__contains_item(v.value, v.gender)): 
                return False
        for v in col2.items: 
            if (not col1.__contains_item(v.value, v.gender)): 
                return False
        return True
    
    @staticmethod
    def __intersect2(col1 : 'PersonMorphCollection', col2 : 'PersonMorphCollection') -> bool:
        if (col1.head != col2.head): 
            return False
        ret = False
        vals1 = col1.values
        vals2 = col2.values
        uni = list()
        for v in vals1: 
            if (v in vals2): 
                uni.append(v)
                continue
        for v in vals1: 
            if (not v in uni): 
                col1.remove(v, MorphGender.UNDEFINED)
                ret = True
        for v in vals2: 
            if (not v in uni): 
                col2.remove(v, MorphGender.UNDEFINED)
                ret = True
        if (col1.gender != MorphGender.UNDEFINED): 
            if (col2.remove(None, (MorphGender.MASCULINE if col1.gender == MorphGender.FEMINIE else MorphGender.FEMINIE))): 
                ret = True
        if (col2.gender != MorphGender.UNDEFINED): 
            if (col1.remove(None, (MorphGender.MASCULINE if col2.gender == MorphGender.FEMINIE else MorphGender.FEMINIE))): 
                ret = True
        return ret
    
    @staticmethod
    def intersect(list0_ : typing.List['PersonMorphCollection']) -> bool:
        ret = False
        while True:
            ch = False
            i = 0
            while i < (len(list0_) - 1): 
                j = i + 1
                while j < len(list0_): 
                    if (PersonMorphCollection.__intersect2(list0_[i], list0_[j])): 
                        ch = True
                    if (PersonMorphCollection.is_equals(list0_[i], list0_[j])): 
                        del list0_[j]
                        j -= 1
                        ch = True
                    j += 1
                i += 1
            if (ch): 
                ret = True
            else: 
                break
        return ret
    
    @staticmethod
    def set_gender(list0_ : typing.List['PersonMorphCollection'], gen : 'MorphGender') -> None:
        for li in list0_: 
            li.remove(None, (MorphGender.FEMINIE if gen == MorphGender.MASCULINE else MorphGender.MASCULINE))
    
    # static constructor for class PersonMorphCollection
    @staticmethod
    def _static_ctor():
        PersonMorphCollection.M_COMPARER = PersonMorphCollection.SortComparer()

PersonMorphCollection._static_ctor()