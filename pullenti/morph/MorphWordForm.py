# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from pullenti.ntopy.Utils import Utils
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphPerson import MorphPerson


class MorphWordForm(MorphBaseInfo):
    """ Словоформа (вариант морфанализа лексемы) """
    
    @property
    def is_in_dictionary(self) -> bool:
        """ Находится ли словоформа в словаре (если false, то восстановлена по аналогии) """
        return self.undef_coef == 0
    
    def clone(self) -> object:
        res = MorphWordForm()
        self.copy_to_word_form(res)
        return res
    
    def copy_to_word_form(self, dst : 'MorphWordForm') -> None:
        super().copy_to(dst)
        dst.undef_coef = self.undef_coef
        dst.normal_case = self.normal_case
        dst.normal_full = self.normal_full
        dst.misc = self.misc
        dst.tag = self.tag
    
    def __init__(self, v : 'MorphRuleVariant'=None, word : str=None) -> None:
        self.normal_full = None
        self.normal_case = None
        self.misc = None
        self.undef_coef = 0
        self.tag = None
        super().__init__(None)
        if (v is None): 
            return
        v.copy_to(self)
        self.misc = v.misc_info
        self.tag = v
        if (v.normal_tail is not None and word is not None): 
            word_begin = word
            if (LanguageHelper.ends_with(word, v.tail)): 
                word_begin = word[0 : (len(word) - len(v.tail))]
            if (len(v.normal_tail) > 0): 
                self.normal_case = (word_begin + v.normal_tail)
            else: 
                self.normal_case = word_begin
        if (v.full_normal_tail is not None and word is not None): 
            word_begin = word
            if (LanguageHelper.ends_with(word, v.tail)): 
                word_begin = word[0 : (len(word) - len(v.tail))]
            if (len(v.full_normal_tail) > 0): 
                self.normal_full = (word_begin + v.full_normal_tail)
            else: 
                self.normal_full = word_begin
    
    def __str__(self) -> str:
        res = Utils.newStringIO(Utils.ifNotNull(self.normal_case, ""))
        if (self.normal_full is not None and self.normal_full != self.normal_case): 
            print("\\{0}".format(self.normal_full), end="", file=res, flush=True)
        if (res.tell() > 0): 
            print(' ', end="", file=res)
        print(super().__str__(), end="", file=res)
        s = (None if self.misc is None else str(self.misc))
        if (not Utils.isNullOrEmpty(s)): 
            print(" {0}".format(s), end="", file=res, flush=True)
        if (self.undef_coef > 0): 
            print(" (? {0})".format(self.undef_coef), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def _has_morph_equals(list0 : typing.List['MorphWordForm'], mv : 'MorphWordForm') -> bool:
        for mr in list0: 
            if ((mv.class0 == mr.class0 and mv.number == mr.number and mv.gender == mr.gender) and mv.normal_case == mr.normal_case and mv.normal_full == mr.normal_full): 
                mr.case |= mv.case
                p = mv.misc.person
                if (p != MorphPerson.UNDEFINED and p != mr.misc.person): 
                    mr.misc = mr.misc.clone()
                    mr.misc.person = (mr.misc.person | mv.misc.person)
                return True
        for mr in list0: 
            if ((mv.class0 == mr.class0 and mv.number == mr.number and mv.case == mr.case) and mv.normal_case == mr.normal_case and mv.normal_full == mr.normal_full): 
                mr.gender |= mv.gender
                return True
        for mr in list0: 
            if ((mv.class0 == mr.class0 and mv.gender == mr.gender and mv.case == mr.case) and mv.normal_case == mr.normal_case and mv.normal_full == mr.normal_full): 
                mr.number |= mv.number
                return True
        return False

    
    @staticmethod
    def _new12(_arg1 : str, _arg2 : 'MorphClass', _arg3 : int) -> 'MorphWordForm':
        res = MorphWordForm()
        res.normal_case = _arg1
        res.class0 = _arg2
        res.undef_coef = _arg3
        return res