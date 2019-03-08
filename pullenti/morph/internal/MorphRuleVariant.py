# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphVoice import MorphVoice
from pullenti.morph.MorphPerson import MorphPerson
from pullenti.morph.MorphTense import MorphTense
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphMood import MorphMood

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
        src.copy_to(self)
        self.misc_info = src.misc_info
        self.normal_tail = src.normal_tail
        self.full_normal_tail = src.full_normal_tail
        self.rule = src.rule
        self.tag = src.tag
    
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
    
    def calc_eq_coef(self, wf : 'MorphWordForm') -> int:
        if (wf.class0_.value != (0)): 
            if ((((self.class0_.value) & (wf.class0_.value))) == 0): 
                return -1
        if (self.misc_info != wf.misc): 
            if (self.misc_info.mood != MorphMood.UNDEFINED and wf.misc.mood != MorphMood.UNDEFINED): 
                if (self.misc_info.mood != wf.misc.mood): 
                    return -1
            if (self.misc_info.tense != MorphTense.UNDEFINED and wf.misc.tense != MorphTense.UNDEFINED): 
                if ((((self.misc_info.tense) & (wf.misc.tense))) == (MorphTense.UNDEFINED)): 
                    return -1
            if (self.misc_info.voice != MorphVoice.UNDEFINED and wf.misc.voice != MorphVoice.UNDEFINED): 
                if (self.misc_info.voice != wf.misc.voice): 
                    return -1
            if (self.misc_info.person != MorphPerson.UNDEFINED and wf.misc.person != MorphPerson.UNDEFINED): 
                if ((((self.misc_info.person) & (wf.misc.person))) == (MorphPerson.UNDEFINED)): 
                    return -1
            return 0
        if (not self.check_accord(wf, False, False)): 
            return -1
        return 1
    
    @staticmethod
    def _new36(_arg1 : 'MorphMiscInfo') -> 'MorphRuleVariant':
        res = MorphRuleVariant()
        res.misc_info = _arg1
        return res