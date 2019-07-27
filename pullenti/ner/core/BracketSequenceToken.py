# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.MiscHelper import MiscHelper

class BracketSequenceToken(MetaToken):
    """ Представление последовательности, обрамлённой кавычками (скобками) """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.internal = list()
    
    @property
    def is_quote_type(self) -> bool:
        """ Признак обрамления кавычками (если false, то м.б. [...], (...), {...}) """
        return "{([".find(self.open_char) < 0
    
    @property
    def open_char(self) -> 'char':
        """ Открывающий символ """
        return self.begin_token.kit.get_text_character(self.begin_token.begin_char)
    
    @property
    def close_char(self) -> 'char':
        """ Закрывающий символ """
        return self.end_token.kit.get_text_character(self.end_token.begin_char)
    
    def __str__(self) -> str:
        return super().__str__()
    
    def get_normal_case_text(self, mc : 'MorphClass'=None, single_number : bool=False, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        attr = GetTextAttr.NO
        if (single_number): 
            attr = (Utils.valToEnum((attr) | (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE), GetTextAttr))
        else: 
            attr = (Utils.valToEnum((attr) | (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE), GetTextAttr))
        if (keep_chars): 
            attr = (Utils.valToEnum((attr) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
        return MiscHelper.get_text_value(self.begin_token, self.end_token, attr)