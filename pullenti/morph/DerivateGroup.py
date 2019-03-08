# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.morph.DerivateWord import DerivateWord
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.internal.NextModelQuestion import NextModelQuestion

class DerivateGroup:
    """ Дериватная группа """
    
    def __init__(self) -> None:
        self.words = list()
        self.prefix = None;
        self.is_dummy = False
        self.not_generate = False
        self.is_generated = False
        self.m_transitive = -1
        self.m_rev_agent_case = -1
        self.nexts = None;
        self.nexts_ref = None;
        self.questions = NextModelQuestion.UNDEFINED
        self.questions_ref = NextModelQuestion.UNDEFINED
        self._lazy_pos = 0
        self.tag = None;
    
    @property
    def transitive(self) -> int:
        """ Признак транзитивности группы (не только глаголов!) """
        if (self.m_transitive >= 0): 
            return self.m_transitive
        return -1
    
    @property
    def rev_agent_case(self) -> int:
        """ Падеж агенса для возвратного глагола (0 - именит, 1 - дател, 2 - творит) """
        if (self.m_rev_agent_case >= 0): 
            return self.m_rev_agent_case
        return -1
    
    def contains_word(self, word : str, lang : 'MorphLang') -> bool:
        """ Содержит ли группа слово
        
        Args:
            word(str): слово
            lang(MorphLang): возможный язык
        
        """
        for w in self.words: 
            if (w.spelling == word): 
                if (lang is None or lang.is_undefined0 or w.lang is None): 
                    return True
                if (not ((lang) & w.lang).is_undefined0): 
                    return True
        return False
    
    def __str__(self) -> str:
        res = "?"
        if (len(self.words) > 0): 
            res = "<{0}>".format(self.words[0].spelling)
        if (self.is_dummy): 
            res = "DUMMY: {0}".format(res)
        elif (self.is_generated): 
            res = "GEN: {0}".format(res)
        return res
    
    def create_by_prefix(self, pref : str, lang : 'MorphLang') -> 'DerivateGroup':
        res = DerivateGroup._new41(True, pref)
        for w in self.words: 
            if (lang is not None and not lang.is_undefined0 and ((w.lang) & lang).is_undefined0): 
                continue
            rw = DerivateWord._new42(res, pref + w.spelling, w.lang, w.class0_, w.aspect, w.reflexive, w.tense, w.voice, w.attrs)
            res.words.append(rw)
        return res
    
    @staticmethod
    def _new41(_arg1 : bool, _arg2 : str) -> 'DerivateGroup':
        res = DerivateGroup()
        res.is_generated = _arg1
        res.prefix = _arg2
        return res