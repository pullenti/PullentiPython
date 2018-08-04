# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.morph.LanguageHelper import LanguageHelper


class MorphRule:
    
    def __init__(self) -> None:
        self._id0_ = 0
        self.variants = dict()
        self.variants_list = list()
        self.variants_key = list()
        self._lazy = None
    
    def __str__(self) -> str:
        res = Utils.newStringIO(None)
        for k in self.variants_key: 
            if (res.tell() > 0): 
                print(", ", end="", file=res)
            print("-{0}".format(k), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def add(self, tail : str, var : 'MorphRuleVariant') -> None:
        tail = LanguageHelper.correct_word(tail)
        if (var.class0_.is_undefined): 
            pass
        li = [ ]
        inoutarg33 = RefOutArgWrapper(None)
        inoutres34 = Utils.tryGetValue(self.variants, tail, inoutarg33)
        li = inoutarg33.value
        if (not inoutres34): 
            li = list()
            self.variants[tail] = li
        var.tail = tail
        li.append(var)
        var.rule = self
    
    def process_result(self, res : typing.List['MorphWordForm'], word_begin : str, mvs : typing.List['MorphRuleVariant']) -> None:
        from pullenti.morph.MorphWordForm import MorphWordForm
        for mv in mvs: 
            r = MorphWordForm(mv, None)
            if (mv.normal_tail is not None and len(mv.normal_tail) > 0 and mv.normal_tail[0] != '-'): 
                r.normal_case = (word_begin + mv.normal_tail)
            else: 
                r.normal_case = word_begin
            if (mv.full_normal_tail is not None): 
                if (len(mv.full_normal_tail) > 0 and mv.full_normal_tail[0] != '-'): 
                    r.normal_full = (word_begin + mv.full_normal_tail)
                else: 
                    r.normal_full = word_begin
            if (not MorphWordForm._has_morph_equals(res, r)): 
                r.undef_coef = 0
                res.append(r)