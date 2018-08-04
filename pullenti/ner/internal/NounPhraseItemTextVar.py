# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender


class NounPhraseItemTextVar(MorphBaseInfo):
    """ Морфологический вариант для элемента именной группы """
    
    def __init__(self, src : 'MorphBaseInfo'=None, t : 'Token'=None) -> None:
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.morph.MorphCase import MorphCase
        self.normal_value = None
        self.single_number_value = None
        self.undef_coef = 0
        super().__init__(src)
        wf = (src if isinstance(src, MorphWordForm) else None)
        if (wf is not None): 
            self.normal_value = wf.normal_case
            if (wf.number == MorphNumber.PLURAL and wf.normal_full is not None): 
                self.single_number_value = wf.normal_full
            self.undef_coef = wf.undef_coef
        elif (t is not None): 
            self.normal_value = t.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False)
        if (self.case.is_undefined and src is not None): 
            if (src.contains_attr("неизм.", MorphClass())): 
                self.case = MorphCase.ALL_CASES
    
    def __str__(self) -> str:
        return "{0} {1}".format(self.normal_value, super().__str__())
    
    def clone(self) -> object:
        res = NounPhraseItemTextVar()
        self.copy_to(res)
        res.normal_value = self.normal_value
        res.single_number_value = self.single_number_value
        res.undef_coef = self.undef_coef
        return res
    
    def correct_prefix(self, t : 'TextToken', ignore_gender : bool) -> None:
        from pullenti.morph.MorphWordForm import MorphWordForm
        if (t is None): 
            return
        for v in t.morph.items: 
            if (v.class0_ == self.class0_ and self.check_accord(v, ignore_gender)): 
                self.normal_value = "{0}-{1}".format((v if isinstance(v, MorphWordForm) else None).normal_case, self.normal_value)
                if (self.single_number_value is not None): 
                    self.single_number_value = "{0}-{1}".format(Utils.ifNotNull((v if isinstance(v, MorphWordForm) else None).normal_full, (v if isinstance(v, MorphWordForm) else None).normal_case), self.single_number_value)
                return
        self.normal_value = "{0}-{1}".format(t.term, self.normal_value)
        if (self.single_number_value is not None): 
            self.single_number_value = "{0}-{1}".format(t.term, self.single_number_value)