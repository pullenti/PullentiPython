# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.MiscHelper import MiscHelper

class NounPhraseMultivarToken(MetaToken):
    """ Вариант расщепления именной группы, у которой слиплись существительные.
    Получается методом GetMultivars() у NounPhraseToken, у которой MultiNouns = true.
    Расщепление именной группы
    """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.source = None;
        self.adj_index1 = 0
        self.adj_index2 = 0
    
    def __str__(self) -> str:
        return "{0} {1}".format(self.source.adjectives[self.adj_index1], self.source.noun)
    
    def get_normal_case_text(self, mc : 'MorphClass'=None, num : 'MorphNumber'=MorphNumber.UNDEFINED, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        if (gender == MorphGender.UNDEFINED): 
            gender = self.source.morph.gender
        res = io.StringIO()
        k = self.adj_index1
        while k <= self.adj_index2: 
            adj = self.source.adjectives[k].get_normal_case_text((MorphClass.ADJECTIVE) | MorphClass.PRONOUN, num, gender, keep_chars)
            if (adj is None or adj == "?"): 
                adj = MiscHelper.get_text_value_of_meta_token(self.source.adjectives[k], (GetTextAttr.KEEPREGISTER if keep_chars else GetTextAttr.NO))
            print("{0} ".format(Utils.ifNotNull(adj, "?")), end="", file=res, flush=True)
            k += 1
        noun = None
        if ((isinstance(self.source.noun.begin_token, ReferentToken)) and self.source.begin_token == self.source.noun.end_token): 
            noun = self.source.noun.begin_token.get_normal_case_text(None, num, gender, keep_chars)
        else: 
            cas = (MorphClass.NOUN) | MorphClass.PRONOUN
            if (mc is not None and not mc.is_undefined): 
                cas = mc
            noun = self.source.noun.get_normal_case_text(cas, num, gender, keep_chars)
        if (noun is None or noun == "?"): 
            noun = self.source.noun.get_normal_case_text(None, num, MorphGender.UNDEFINED, False)
        print(Utils.ifNotNull(noun, "?"), end="", file=res)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def _new498(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'NounPhraseToken', _arg4 : int, _arg5 : int) -> 'NounPhraseMultivarToken':
        res = NounPhraseMultivarToken(_arg1, _arg2)
        res.source = _arg3
        res.adj_index1 = _arg4
        res.adj_index2 = _arg5
        return res