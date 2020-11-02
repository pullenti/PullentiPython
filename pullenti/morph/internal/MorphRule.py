# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.internal.MorphRuleVariant import MorphRuleVariant

class MorphRule:
    
    def __init__(self) -> None:
        self.id0_ = 0
        self.tails = list()
        self.morph_vars = list()
        self.lazy_pos = 0
    
    def contains_var(self, tail : str) -> bool:
        return Utils.indexOfList(self.tails, tail, 0) >= 0
    
    def get_vars(self, key : str) -> typing.List['MorphRuleVariant']:
        i = Utils.indexOfList(self.tails, key, 0)
        if (i >= 0): 
            return self.morph_vars[i]
        return None
    
    def find_var(self, id0__ : int) -> 'MorphRuleVariant':
        for li in self.morph_vars: 
            for v in li: 
                if (v.id0_ == id0__): 
                    return v
        return None
    
    def add(self, tail : str, vars0_ : typing.List['MorphRuleVariant']) -> None:
        self.tails.append(tail)
        self.morph_vars.append(vars0_)
    
    def __str__(self) -> str:
        res = io.StringIO()
        i = 0
        while i < len(self.tails): 
            if (res.tell() > 0): 
                print(", ", end="", file=res)
            print("-{0}".format(self.tails[i]), end="", file=res, flush=True)
            i += 1
        return Utils.toStringStringIO(res)
    
    def _deserialize(self, str0_ : 'ByteArrayWrapper', pos : int) -> None:
        ii = str0_.deserialize_short(pos)
        self.id0_ = ii
        id0__ = 1
        while not str0_.iseof(pos.value):
            b = str0_.deserialize_byte(pos)
            if (b == (0xFF)): 
                break
            pos.value -= 1
            key = str0_.deserialize_string(pos)
            if (key is None): 
                key = ""
            li = list()
            while not str0_.iseof(pos.value):
                mrv = MorphRuleVariant()
                inoutres24 = mrv._deserialize(str0_, pos)
                if (not inoutres24): 
                    break
                mrv.tail = key
                mrv.rule_id = (ii)
                mrv.id0_ = id0__
                id0__ += 1
                li.append(mrv)
            self.add(key, li)