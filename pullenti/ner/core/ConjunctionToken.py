# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.MiscHelper import MiscHelper

class ConjunctionToken(MetaToken):
    """ Представление союзов (они могут быть из нескольких токенов, например, "из-за того что"
     Получить можно с помощью ConjunctionHelper.TryParse(t) """
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.normal = None;
        self.typ = ConjunctionType.UNDEFINED
    
    def __str__(self) -> str:
        return self.normal
    
    def get_normal_case_text(self, mc : 'MorphClass'=None, single_number : bool=False, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
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
    def _new565(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ConjunctionType', _arg4 : str) -> 'ConjunctionToken':
        res = ConjunctionToken(_arg1, _arg2)
        res.typ = _arg3
        res.normal = _arg4
        return res
    
    @staticmethod
    def _new566(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'ConjunctionType') -> 'ConjunctionToken':
        res = ConjunctionToken(_arg1, _arg2)
        res.normal = _arg3
        res.typ = _arg4
        return res