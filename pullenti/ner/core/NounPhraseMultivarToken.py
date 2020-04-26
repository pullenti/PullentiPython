# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.core.MiscHelper import MiscHelper

class NounPhraseMultivarToken(MetaToken):
    """ Вариант расщепления именной группы, у которой слиплись существительные """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.source = None;
        self.adj_index = 0
    
    def __str__(self) -> str:
        return "{0} {1}".format(self.source.adjectives[self.adj_index], self.source.noun)
    
    def get_normal_case_text(self, mc : 'MorphClass'=None, single_number : bool=False, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        if (gender == MorphGender.UNDEFINED): 
            gender = self.source.morph.gender
        adj = self.source.adjectives[self.adj_index].get_normal_case_text((MorphClass.ADJECTIVE) | MorphClass.PRONOUN, single_number, gender, keep_chars)
        if (adj is None or adj == "?"): 
            adj = MiscHelper.get_text_value_of_meta_token(self.source.adjectives[self.adj_index], (GetTextAttr.KEEPREGISTER if keep_chars else GetTextAttr.NO))
        noun = None
        if ((isinstance(self.source.noun.begin_token, ReferentToken)) and self.source.begin_token == self.source.noun.end_token): 
            noun = self.source.noun.begin_token.get_normal_case_text(None, single_number, gender, keep_chars)
        else: 
            cas = (MorphClass.NOUN) | MorphClass.PRONOUN
            if (mc is not None and not mc.is_undefined): 
                cas = mc
            noun = self.source.noun.get_normal_case_text(cas, single_number, gender, keep_chars)
        if (noun is None or noun == "?"): 
            noun = self.source.noun.get_normal_case_text(None, single_number, MorphGender.UNDEFINED, False)
        return "{0} {1}".format(Utils.ifNotNull(adj, "?"), Utils.ifNotNull(noun, "?"))
    
    @staticmethod
    def _new583(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'NounPhraseToken', _arg4 : int) -> 'NounPhraseMultivarToken':
        res = NounPhraseMultivarToken(_arg1, _arg2)
        res.source = _arg3
        res.adj_index = _arg4
        return res