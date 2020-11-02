# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.NounPhraseToken import NounPhraseToken

class SemanticAbstractSlave(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.preposition = None;
        self.source = None;
    
    @staticmethod
    def create_from_noun(npt : 'NounPhraseToken') -> 'SemanticAbstractSlave':
        res = SemanticAbstractSlave(npt.begin_token, npt.end_token)
        if (npt.preposition is not None): 
            res.preposition = npt.preposition.normal
        res.morph = npt.morph
        res.source = (npt)
        return res
    
    def __str__(self) -> str:
        if (self.preposition is not None): 
            return "{0}: {1}".format(self.preposition, self.get_source_text())
        return self.get_source_text()
    
    @property
    def has_pronoun(self) -> bool:
        npt = Utils.asObjectOrNull(self.source, NounPhraseToken)
        if (npt is None): 
            return False
        for a in npt.adjectives: 
            if (a.begin_token.morph.class0_.is_pronoun): 
                return True
        return False