# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.LanguageHelper import LanguageHelper

class MorphWordForm(MorphBaseInfo):
    """ Словоформа (вариант морфанализа лексемы)
    
    словоформа
    """
    
    @property
    def is_in_dictionary(self) -> bool:
        """ Находится ли словоформа в словаре (если false, то восстановлена по аналогии) """
        return self.undef_coef == (0)
    
    def copy_from_word_form(self, src : 'MorphWordForm') -> None:
        super().copy_from(src)
        self.undef_coef = src.undef_coef
        self.normal_case = src.normal_case
        self.normal_full = src.normal_full
        self.misc = src.misc
    
    def __init__(self, v : 'MorphRuleVariant'=None, word : str=None, mi : 'MorphMiscInfo'=None) -> None:
        super().__init__()
        self.normal_full = None;
        self.normal_case = None;
        self.misc = None;
        self.undef_coef = 0
        if (v is None): 
            return
        self.copy_from(v)
        self.misc = mi
        if (v.normal_tail is not None and word is not None): 
            word_begin = word
            if (LanguageHelper.ends_with(word, v.tail)): 
                word_begin = word[0:0+len(word) - len(v.tail)]
            if (len(v.normal_tail) > 0): 
                self.normal_case = (word_begin + v.normal_tail)
            else: 
                self.normal_case = word_begin
        if (v.full_normal_tail is not None and word is not None): 
            word_begin = word
            if (LanguageHelper.ends_with(word, v.tail)): 
                word_begin = word[0:0+len(word) - len(v.tail)]
            if (len(v.full_normal_tail) > 0): 
                self.normal_full = (word_begin + v.full_normal_tail)
            else: 
                self.normal_full = word_begin
    
    def __str__(self) -> str:
        return self.to_string_ex(False)
    
    def to_string_ex(self, ignore_normals : bool) -> str:
        res = io.StringIO()
        if (not ignore_normals): 
            print(Utils.ifNotNull(self.normal_case, ""), end="", file=res)
            if (self.normal_full is not None and self.normal_full != self.normal_case): 
                print("\\{0}".format(self.normal_full), end="", file=res, flush=True)
            if (res.tell() > 0): 
                print(' ', end="", file=res)
        print(super().__str__(), end="", file=res)
        s = (None if self.misc is None else str(self.misc))
        if (not Utils.isNullOrEmpty(s)): 
            print(" {0}".format(s), end="", file=res, flush=True)
        if (self.undef_coef > (0)): 
            print(" (? {0})".format(self.undef_coef), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def contains_attr(self, attr_value : str, cla : 'MorphClass'=None) -> bool:
        if (self.misc is not None and self.misc.attrs is not None): 
            return attr_value in self.misc.attrs
        return False
    
    def _has_morph_equals(self, list0_ : typing.List['MorphWordForm']) -> bool:
        for mr in list0_: 
            if ((self.class0_ == mr.class0_ and self.number == mr.number and self.gender == mr.gender) and self.normal_case == mr.normal_case and self.normal_full == mr.normal_full): 
                mr.case_ = (mr.case_) | self.case_
                return True
        for mr in list0_: 
            if ((self.class0_ == mr.class0_ and self.number == mr.number and self.case_ == mr.case_) and self.normal_case == mr.normal_case and self.normal_full == mr.normal_full): 
                mr.gender = Utils.valToEnum((mr.gender) | (self.gender), MorphGender)
                return True
        for mr in list0_: 
            if ((self.class0_ == mr.class0_ and self.gender == mr.gender and self.case_ == mr.case_) and self.normal_case == mr.normal_case and self.normal_full == mr.normal_full): 
                mr.number = Utils.valToEnum((mr.number) | (self.number), MorphNumber)
                return True
        return False
    
    @staticmethod
    def _new5(_arg1 : str, _arg2 : 'MorphClass', _arg3 : int) -> 'MorphWordForm':
        res = MorphWordForm()
        res.normal_case = _arg1
        res.class0_ = _arg2
        res.undef_coef = _arg3
        return res
    
    @staticmethod
    def _new604(_arg1 : 'MorphCase', _arg2 : 'MorphNumber', _arg3 : 'MorphGender') -> 'MorphWordForm':
        res = MorphWordForm()
        res.case_ = _arg1
        res.number = _arg2
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new605(_arg1 : 'MorphClass', _arg2 : 'MorphMiscInfo') -> 'MorphWordForm':
        res = MorphWordForm()
        res.class0_ = _arg1
        res.misc = _arg2
        return res
    
    @staticmethod
    def _new2930(_arg1 : 'MorphClass', _arg2 : 'MorphNumber', _arg3 : 'MorphGender', _arg4 : 'MorphCase') -> 'MorphWordForm':
        res = MorphWordForm()
        res.class0_ = _arg1
        res.number = _arg2
        res.gender = _arg3
        res.case_ = _arg4
        return res