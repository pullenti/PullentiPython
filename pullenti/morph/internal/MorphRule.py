# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphWordForm import MorphWordForm

class MorphRule:
    
    def __init__(self) -> None:
        self._id0_ = 0
        self.variants = dict()
        self.variants_list = list()
        self.variants_key = list()
        self.lazy_pos = 0
    
    def refresh_variants(self) -> None:
        vars0_ = list()
        for v in self.variants_list: 
            vars0_.extend(v)
        self.variants.clear()
        self.variants_key.clear()
        self.variants_list.clear()
        for v in vars0_: 
            li = [ ]
            wrapli32 = RefOutArgWrapper(None)
            inoutres33 = Utils.tryGetValue(self.variants, Utils.ifNotNull(v.tail, ""), wrapli32)
            li = wrapli32.value
            if (not inoutres33): 
                li = list()
                self.variants[Utils.ifNotNull(v.tail, "")] = li
            li.append(v)
        for kp in self.variants.items(): 
            self.variants_key.append(kp[0])
            self.variants_list.append(kp[1])
    
    def __str__(self) -> str:
        res = io.StringIO()
        i = 0
        while i < len(self.variants_key): 
            if (res.tell() > 0): 
                print(", ", end="", file=res)
            print("-{0}".format(self.variants_key[i]), end="", file=res, flush=True)
            i += 1
        return Utils.toStringStringIO(res)
    
    def add(self, tail : str, var : 'MorphRuleVariant') -> None:
        tail = LanguageHelper.correct_word(tail)
        if (var.class0_.is_undefined): 
            pass
        li = [ ]
        wrapli34 = RefOutArgWrapper(None)
        inoutres35 = Utils.tryGetValue(self.variants, tail, wrapli34)
        li = wrapli34.value
        if (not inoutres35): 
            li = list()
            self.variants[tail] = li
        var.tail = tail
        li.append(var)
        var.rule = self
    
    def process_result(self, res : typing.List['MorphWordForm'], word_begin : str, mvs : typing.List['MorphRuleVariant']) -> None:
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
                r.undef_coef = (0)
                res.append(r)