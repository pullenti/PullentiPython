# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.LanguageHelper import LanguageHelper

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
            wrapli28 = RefOutArgWrapper(None)
            inoutres29 = Utils.tryGetValue(self.variants, Utils.ifNotNull(v.tail, ""), wrapli28)
            li = wrapli28.value
            if (not inoutres29): 
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
        wrapli30 = RefOutArgWrapper(None)
        inoutres31 = Utils.tryGetValue(self.variants, tail, wrapli30)
        li = wrapli30.value
        if (not inoutres31): 
            li = list()
            self.variants[tail] = li
        var.tail = tail
        li.append(var)
        var.rule = (self)