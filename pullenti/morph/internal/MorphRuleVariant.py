# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphBaseInfo import MorphBaseInfo

class MorphRuleVariant(MorphBaseInfo):
    
    def __init__(self) -> None:
        super().__init__()
        self.tail = None;
        self.misc_info_id = 0
        self.rule_id = 0
        self.id0_ = 0
        self.normal_tail = None;
        self.full_normal_tail = None;
    
    def copy_from_variant(self, src : 'MorphRuleVariant') -> None:
        if (src is None): 
            return
        self.tail = src.tail
        self.copy_from(src)
        self.misc_info_id = src.misc_info_id
        self.normal_tail = src.normal_tail
        self.full_normal_tail = src.full_normal_tail
        self.rule_id = src.rule_id
    
    def __str__(self) -> str:
        return self.to_string_ex(False)
    
    def to_string_ex(self, hide_tails : bool) -> str:
        res = io.StringIO()
        if (not hide_tails): 
            print("-{0}".format(self.tail), end="", file=res, flush=True)
            if (self.normal_tail is not None): 
                print(" [-{0}]".format(self.normal_tail), end="", file=res, flush=True)
            if (self.full_normal_tail is not None and self.full_normal_tail != self.normal_tail): 
                print(" [-{0}]".format(self.full_normal_tail), end="", file=res, flush=True)
        print(" {0}".format(super().__str__()), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    def compare(self, mrv : 'MorphRuleVariant') -> bool:
        if ((mrv.class0_ != self.class0_ or mrv.gender != self.gender or mrv.number != self.number) or mrv.case_ != self.case_): 
            return False
        if (mrv.misc_info_id != self.misc_info_id): 
            return False
        if (mrv.normal_tail != self.normal_tail): 
            return False
        return True
    
    def _deserialize(self, str0_ : 'ByteArrayWrapper', pos : int) -> bool:
        id0__ = str0_.deserialize_short(pos)
        if (id0__ <= 0): 
            return False
        self.misc_info_id = (id0__)
        iii = str0_.deserialize_short(pos)
        mc = MorphClass()
        mc.value = (iii)
        if (mc.is_misc and mc.is_proper): 
            mc.is_misc = False
        self.class0_ = mc
        bbb = str0_.deserialize_byte(pos)
        self.gender = Utils.valToEnum(bbb, MorphGender)
        bbb = str0_.deserialize_byte(pos)
        self.number = Utils.valToEnum(bbb, MorphNumber)
        bbb = str0_.deserialize_byte(pos)
        mca = MorphCase()
        mca.value = (bbb)
        self.case_ = mca
        s = str0_.deserialize_string(pos)
        self.normal_tail = s
        s = str0_.deserialize_string(pos)
        self.full_normal_tail = s
        return True