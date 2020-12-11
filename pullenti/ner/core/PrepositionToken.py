﻿# Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.MiscHelper import MiscHelper

class PrepositionToken(MetaToken):
    """ Метатокен - предлог (они могут быть из нескольких токенов, например,
    "несмотря на", "в соответствии с").
    Создаётся методом PrepositionHelper.TryParse(t).
    Предложная группа
    """
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.normal = None;
        self.next_case = None;
    
    def __str__(self) -> str:
        return self.normal
    
    def get_normal_case_text(self, mc : 'MorphClass'=None, num : 'MorphNumber'=MorphNumber.UNDEFINED, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        res = self.normal
        if (keep_chars): 
            if (self.chars.is_all_lower): 
                res = res.lower()
            elif (self.chars.is_all_upper): 
                pass
            elif (self.chars.is_capital_upper): 
                res = MiscHelper.convert_first_char_upper_and_other_lower(res)
        return res
    
    @staticmethod
    def _new529(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'MorphCase') -> 'PrepositionToken':
        res = PrepositionToken(_arg1, _arg2)
        res.normal = _arg3
        res.next_case = _arg4
        return res