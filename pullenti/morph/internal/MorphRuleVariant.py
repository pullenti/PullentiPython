# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.morph.MorphBaseInfo import MorphBaseInfo


class MorphRuleVariant(MorphBaseInfo):
    
    def __init__(self, src : 'MorphRuleVariant'=None) -> None:
        super().__init__(None)
        self.coef = 0
        self.tail = None;
        self.misc_info = None;
        self.rule = None;
        self.normal_tail = None;
        self.full_normal_tail = None;
        self.tag = None;
        if (src is None): 
            return
        self.tail = src.tail
        src.copyTo(self)
        self.misc_info = src.misc_info
        self.normal_tail = src.normal_tail
        self.full_normal_tail = src.full_normal_tail
        self.rule = src.rule
        self.tag = src.tag
    
    def __str__(self) -> str:
        return self.toStringEx(False)
    
    def toStringEx(self, hide_tails : bool) -> str:
        res = io.StringIO()
        if (not hide_tails): 
            print("-{0}".format(self.tail), end="", file=res, flush=True)
            if (self.normal_tail is not None): 
                print(" [-{0}]".format(self.normal_tail), end="", file=res, flush=True)
            if (self.full_normal_tail is not None and self.full_normal_tail != self.normal_tail): 
                print(" [-{0}]".format(self.full_normal_tail), end="", file=res, flush=True)
        print(" {0} {1}".format(super().__str__(), ("" if self.misc_info is None else str(self.misc_info))), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    def compare(self, mrv : 'MorphRuleVariant') -> bool:
        if ((mrv.class0_ != self.class0_ or mrv.gender != self.gender or mrv.number != self.number) or mrv.case_ != self.case_): 
            return False
        if (mrv.misc_info != self.misc_info): 
            return False
        if (mrv.normal_tail != self.normal_tail): 
            return False
        return True
    
    def calcEqCoef(self, wf : 'MorphWordForm') -> int:
        if (self.class0_ != wf.class0_): 
            return -1
        if (self.misc_info != wf.misc): 
            return -1
        if (not self.checkAccord(wf, False)): 
            return -1
        return 1
    
    @staticmethod
    def _new37(_arg1 : 'MorphMiscInfo') -> 'MorphRuleVariant':
        res = MorphRuleVariant()
        res.misc_info = _arg1
        return res