# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.ntopy.Utils import Utils
from pullenti.morph.MorphBaseInfo import MorphBaseInfo


class MorphRuleVariant(MorphBaseInfo):
    
    def __init__(self, src : 'MorphRuleVariant'=None) -> None:
        self.coef = 0
        self.tail = None
        self.misc_info = None
        self.rule = None
        self.normal_tail = None
        self.full_normal_tail = None
        self.tag = None
        super().__init__(None)
        if (src is None): 
            return
        self.tail = src.tail
        src.copy_to(self)
        self.misc_info = src.misc_info
        self.normal_tail = src.normal_tail
        self.full_normal_tail = src.full_normal_tail
        self.rule = src.rule
        self.tag = src.tag
    
    def __str__(self) -> str:
        return self.to_string_ex(False)
    
    def to_string_ex(self, hide_tails : bool) -> str:
        res = Utils.newStringIO(None)
        if (not hide_tails): 
            print("-{0}".format(self.tail), end="", file=res, flush=True)
            if (self.normal_tail is not None): 
                print(" [-{0}]".format(self.normal_tail), end="", file=res, flush=True)
            if (self.full_normal_tail is not None and self.full_normal_tail != self.normal_tail): 
                print(" [-{0}]".format(self.full_normal_tail), end="", file=res, flush=True)
        print(" {0} {1}".format(super().__str__(), ("" if self.misc_info is None else str(self.misc_info))), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    def compare(self, mrv : 'MorphRuleVariant') -> bool:
        if ((mrv.class0 != self.class0 or mrv.gender != self.gender or mrv.number != self.number) or mrv.case != self.case): 
            return False
        if (mrv.misc_info != self.misc_info): 
            return False
        if (mrv.normal_tail != self.normal_tail): 
            return False
        return True
    
    def calc_eq_coef(self, wf : 'MorphWordForm') -> int:
        if (self.class0 != wf.class0): 
            return -1
        if (self.misc_info != wf.misc): 
            return -1
        if (not self.check_accord(wf, False)): 
            return -1
        return 1

    
    @staticmethod
    def _new35(_arg1 : 'MorphMiscInfo') -> 'MorphRuleVariant':
        res = MorphRuleVariant()
        res.misc_info = _arg1
        return res