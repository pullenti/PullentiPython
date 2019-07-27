# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphPerson import MorphPerson
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.morph.Morphology import Morphology
from pullenti.ner.TextToken import TextToken

class VerbPhraseItemToken(MetaToken):
    """ Элемент глагольной группы """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.not0_ = False
        self.is_adverb = False
        self.__m_is_participle = -1
        self.__m_normal = None;
        self.__m_verb_morph = None;
    
    @property
    def is_participle(self) -> bool:
        """ Причастие """
        if (self.__m_is_participle >= 0): 
            return self.__m_is_participle > 0
        for f in self.morph.items: 
            if (f.class0_.is_adjective and (isinstance(f, MorphWordForm)) and not "к.ф." in (f).misc.attrs): 
                return True
            elif (f.class0_.is_verb and not f.case_.is_undefined): 
                return True
        self.__m_is_participle = 0
        tt = Utils.asObjectOrNull(self.end_token, TextToken)
        if (tt is not None and tt.term.endswith("СЯ")): 
            mb = Morphology.get_word_base_info(tt.term[0:0+len(tt.term) - 2], None, False, False)
            if (mb is not None): 
                if (mb.class0_.is_adjective): 
                    self.__m_is_participle = 1
        return self.__m_is_participle > 0
    @is_participle.setter
    def is_participle(self, value) -> bool:
        self.__m_is_participle = (1 if value else 0)
        return value
    
    @property
    def is_dee_participle(self) -> bool:
        """ Признак деепричастия """
        tt = Utils.asObjectOrNull(self.end_token, TextToken)
        if (tt is None): 
            return False
        if (not tt.term.endswith("Я") and not tt.term.endswith("В")): 
            return False
        if (tt.morph.class0_.is_verb and not tt.morph.class0_.is_adjective): 
            if (tt.morph.gender == MorphGender.UNDEFINED and tt.morph.case_.is_undefined and tt.morph.number == MorphNumber.UNDEFINED): 
                return True
        return False
    
    @property
    def is_verb_infinitive(self) -> bool:
        """ Глагол-инфиниитив """
        for f in self.morph.items: 
            if (f.class0_.is_verb and (isinstance(f, MorphWordForm)) and "инф." in (f).misc.attrs): 
                return True
        return False
    
    @property
    def normal(self) -> str:
        """ Нормализованное значение """
        wf = self.verb_morph
        if (wf is not None): 
            if (not wf.class0_.is_adjective and not wf.case_.is_undefined and self.__m_normal is not None): 
                return self.__m_normal
            if (wf.class0_.is_adjective and not wf.class0_.is_verb): 
                return Utils.ifNotNull(wf.normal_full, wf.normal_case)
            return wf.normal_case
        return self.__m_normal
    @normal.setter
    def normal(self, value) -> str:
        self.__m_normal = value
        return value
    
    @property
    def verb_morph(self) -> 'MorphWordForm':
        """ Полное морф.информация о глаголе глагола """
        if (self.__m_verb_morph is not None): 
            return self.__m_verb_morph
        for f in self.morph.items: 
            if (f.class0_.is_verb and (isinstance(f, MorphWordForm)) and ((((f).misc.person) & (MorphPerson.THIRD))) != (MorphPerson.UNDEFINED)): 
                return (Utils.asObjectOrNull(f, MorphWordForm))
        for f in self.morph.items: 
            if (f.class0_.is_verb and (isinstance(f, MorphWordForm))): 
                return (Utils.asObjectOrNull(f, MorphWordForm))
        for f in self.morph.items: 
            if (f.class0_.is_adjective and (isinstance(f, MorphWordForm))): 
                return (Utils.asObjectOrNull(f, MorphWordForm))
        return None
    @verb_morph.setter
    def verb_morph(self, value) -> 'MorphWordForm':
        self.__m_verb_morph = value
        return value
    
    def __str__(self) -> str:
        return ((("НЕ " if self.not0_ else ""))) + self.normal
    
    @staticmethod
    def _new663(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection') -> 'VerbPhraseItemToken':
        res = VerbPhraseItemToken(_arg1, _arg2)
        res.morph = _arg3
        return res