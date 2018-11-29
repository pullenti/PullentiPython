# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import datetime
from pullenti.unisharp.Utils import Utils
from pullenti.morph.DerivateWord import DerivateWord


class DerivateGroup:
    """ Дериватная группа """
    
    def __init__(self) -> None:
        self.root = None;
        self.prefix = None;
        self.words = list()
        self.ok = False
        self.is_dummy = False
        self.not_generate = False
        self.is_generated = False
        self.m_transitive = -1
        self.deleted = False
        self.id0_ = None;
        self.modified = datetime.datetime(1, 1, 1, 0, 0, 0)
        self.changed = False
        self._lazy = None
        self.tag = None;
    
    @property
    def transitive(self) -> int:
        """ Признак транзитивности глаголов """
        if (self.m_transitive >= 0): 
            return self.m_transitive
        if (self.root is not None): 
            return self.root.transitive
        return -1
    
    def containsWord(self, word : str, lang : 'MorphLang') -> bool:
        """ Содержит ли группа слово
        
        Args:
            word(str): слово
            lang(MorphLang): возможный язык
        
        """
        for w in self.words: 
            if (w.spelling == word): 
                if (lang is None or lang.is_undefined or w.lang is None): 
                    return True
                if (not ((lang) & w.lang).is_undefined): 
                    return True
        return False
    
    def __str__(self) -> str:
        res = "?"
        if (self.prefix is not None and self.root is not None): 
            res = "[{0}] + <{1}>".format(self.prefix, (self.root.words[0].spelling if len(self.root.words) > 0 else "?"))
        elif (len(self.words) > 0): 
            res = "<{0}>".format(self.words[0].spelling)
        if (self.is_dummy): 
            res = "DUMMY: {0}".format(res)
        elif (self.is_generated): 
            res = "GEN: {0}".format(res)
        return res
    
    def compareTo(self, other : 'DerivateGroup') -> int:
        if (len(self.words) == 0): 
            return (-1 if len(other.words) > 0 else 0)
        if (len(other.words) == 0): 
            return 1
        return Utils.compareStrings(self.words[0].spelling, other.words[0].spelling, False)
    
    def createByPrefix(self, pref : str, lang : 'MorphLang') -> 'DerivateGroup':
        res = DerivateGroup._new40(True, self, pref)
        for w in self.words: 
            if (lang is not None and not lang.is_undefined and ((w.lang) & lang).is_undefined): 
                continue
            rw = DerivateWord._new41(res, pref + w.spelling, w.lang, w.class0_, w.aspect, w.reflexive, w.tense, w.voice, w.attrs)
            res.words.append(rw)
        return res
    
    @staticmethod
    def _new40(_arg1 : bool, _arg2 : 'DerivateGroup', _arg3 : str) -> 'DerivateGroup':
        res = DerivateGroup()
        res.is_generated = _arg1
        res.root = _arg2
        res.prefix = _arg3
        return res