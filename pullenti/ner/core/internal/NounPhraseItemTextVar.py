# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphWordForm import MorphWordForm

class NounPhraseItemTextVar(MorphBaseInfo):
    """ Морфологический вариант для элемента именной группы """
    
    def __init__(self, src : 'MorphBaseInfo'=None, t : 'Token'=None) -> None:
        super().__init__()
        self.normal_value = None;
        self.single_number_value = None;
        self.undef_coef = 0
        if (src is not None): 
            self.copy_from(src)
        wf = Utils.asObjectOrNull(src, MorphWordForm)
        if (wf is not None): 
            self.normal_value = wf.normal_case
            if (wf.number == MorphNumber.PLURAL and wf.normal_full is not None): 
                self.single_number_value = wf.normal_full
            self.undef_coef = (wf.undef_coef)
        elif (t is not None): 
            self.normal_value = t.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
        if (self.case_.is_undefined and src is not None): 
            if (src.contains_attr("неизм.", None)): 
                self.case_ = MorphCase.ALL_CASES
    
    def __str__(self) -> str:
        return "{0} {1}".format(self.normal_value, super().__str__())
    
    def copy_from_item(self, src : 'NounPhraseItemTextVar') -> None:
        self.copy_from(src)
        self.normal_value = src.normal_value
        self.single_number_value = src.single_number_value
        self.undef_coef = src.undef_coef
    
    def correct_prefix(self, t : 'TextToken', ignore_gender : bool) -> None:
        if (t is None): 
            return
        for v in t.morph.items: 
            if (v.class0_ == self.class0_ and self.check_accord(v, ignore_gender, False)): 
                self.normal_value = "{0}-{1}".format(v.normal_case, self.normal_value)
                if (self.single_number_value is not None): 
                    self.single_number_value = "{0}-{1}".format(Utils.ifNotNull(v.normal_full, v.normal_case), self.single_number_value)
                return
        self.normal_value = "{0}-{1}".format(t.term, self.normal_value)
        if (self.single_number_value is not None): 
            self.single_number_value = "{0}-{1}".format(t.term, self.single_number_value)