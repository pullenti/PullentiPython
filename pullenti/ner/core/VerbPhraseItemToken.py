# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphPerson import MorphPerson
from pullenti.morph.Morphology import Morphology
from pullenti.ner.TextToken import TextToken

class VerbPhraseItemToken(MetaToken):
    """ Элемент глагольной группы """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.not0_ = False
        self.is_adverb = False
        self.__m_is_verb_adjective = -1
        self.normal = None;
    
    @property
    def is_verb_adjective(self) -> bool:
        """ Причастие """
        if (self.__m_is_verb_adjective >= 0): 
            return self.__m_is_verb_adjective > 0
        for f in self.morph.items: 
            if (f.class0_.is_adjective and (isinstance(f, MorphWordForm)) and not "к.ф." in (f).misc.attrs): 
                return True
        self.__m_is_verb_adjective = 0
        tt = Utils.asObjectOrNull(self.end_token, TextToken)
        if (tt is not None and tt.term.endswith("СЯ")): 
            mb = Morphology.getWordBaseInfo(tt.term[0:0+len(tt.term) - 2], None, False, False)
            if (mb is not None): 
                if (mb.class0_.is_adjective): 
                    self.__m_is_verb_adjective = 1
        return self.__m_is_verb_adjective > 0
    @is_verb_adjective.setter
    def is_verb_adjective(self, value) -> bool:
        self.__m_is_verb_adjective = (1 if value else 0)
        return value
    
    @property
    def is_verb_infinitive(self) -> bool:
        """ Глагол-инфиниитив """
        for f in self.morph.items: 
            if (f.class0_.is_verb and (isinstance(f, MorphWordForm)) and "инф." in (f).misc.attrs): 
                return True
        return False
    
    @property
    def verb_morph(self) -> 'MorphWordForm':
        """ Полное морф.информация о глаголе глагола """
        for f in self.morph.items: 
            if (f.class0_.is_verb and (isinstance(f, MorphWordForm)) and ((((f).misc.person) & (MorphPerson.THIRD))) != (MorphPerson.UNDEFINED)): 
                return (Utils.asObjectOrNull(f, MorphWordForm))
        for f in self.morph.items: 
            if (f.class0_.is_verb and (isinstance(f, MorphWordForm))): 
                return (Utils.asObjectOrNull(f, MorphWordForm))
        return None
    
    def __str__(self) -> str:
        return ((("НЕ " if self.not0_ else ""))) + self.normal
    
    @staticmethod
    def _new665(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection') -> 'VerbPhraseItemToken':
        res = VerbPhraseItemToken(_arg1, _arg2)
        res.morph = _arg3
        return res