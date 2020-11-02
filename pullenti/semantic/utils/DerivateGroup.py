# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphAspect import MorphAspect
from pullenti.morph.MorphTense import MorphTense
from pullenti.morph.MorphVoice import MorphVoice
from pullenti.semantic.utils.ControlModel import ControlModel
from pullenti.semantic.utils.DerivateWord import DerivateWord
from pullenti.morph.MorphLang import MorphLang
from pullenti.semantic.internal.ControlModelOld import ControlModelOld

class DerivateGroup:
    """ Дериватная группа - группа, содержащая однокоренные слова разных частей речи и языков,
    а также модель управления (что может идти за словом).
    
    Дериватная группа
    """
    
    def __init__(self) -> None:
        self.words = list()
        self.prefix = None;
        self.is_dummy = False
        self.not_generate = False
        self.is_generated = False
        self.model = ControlModel()
        self.cm = ControlModelOld()
        self.cm_rev = ControlModelOld()
        self._lazy_pos = 0
        self.id0_ = 0
    
    def contains_word(self, word : str, lang : 'MorphLang') -> bool:
        """ Содержит ли группа слово
        
        Args:
            word(str): слово в верхнем регистре и нормальной форме
            lang(MorphLang): возможный язык
        
        Returns:
            bool: да-нет
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
        if (len(self.words) > 0): 
            res = "<{0}>".format(self.words[0].spelling)
        if (self.is_dummy): 
            res = "DUMMY: {0}".format(res)
        elif (self.is_generated): 
            res = "GEN: {0}".format(res)
        return res
    
    def create_by_prefix(self, pref : str, lang : 'MorphLang') -> 'DerivateGroup':
        res = DerivateGroup._new2964(True, pref)
        for w in self.words: 
            if (lang is not None and not lang.is_undefined and ((w.lang) & lang).is_undefined): 
                continue
            rw = DerivateWord._new2965(pref + w.spelling, w.lang, w.class0_, w.aspect, w.reflexive, w.tense, w.voice, w.attrs)
            res.words.append(rw)
        return res
    
    def _deserialize(self, str0_ : 'ByteArrayWrapper', pos : int) -> None:
        attr = str0_.deserialize_short(pos)
        if (((attr & 1)) != 0): 
            self.is_dummy = True
        if (((attr & 2)) != 0): 
            self.not_generate = True
        self.prefix = str0_.deserialize_string(pos)
        self.model._deserialize(str0_, pos)
        self.cm._deserialize(str0_, pos)
        self.cm_rev._deserialize(str0_, pos)
        cou = str0_.deserialize_short(pos)
        while cou > 0: 
            w = DerivateWord()
            w.spelling = str0_.deserialize_string(pos)
            sh = str0_.deserialize_short(pos)
            w.class0_ = MorphClass()
            w.class0_.value = (sh)
            sh = str0_.deserialize_short(pos)
            w.lang = MorphLang()
            w.lang.value = (sh)
            sh = str0_.deserialize_short(pos)
            w.attrs.value = (sh)
            b = str0_.deserialize_byte(pos)
            w.aspect = (Utils.valToEnum(b, MorphAspect))
            b = str0_.deserialize_byte(pos)
            w.tense = (Utils.valToEnum(b, MorphTense))
            b = str0_.deserialize_byte(pos)
            w.voice = (Utils.valToEnum(b, MorphVoice))
            b = str0_.deserialize_byte(pos)
            cou1 = b
            while cou1 > 0: 
                n = str0_.deserialize_string(pos)
                if (w.next_words is None): 
                    w.next_words = list()
                if (n is not None): 
                    w.next_words.append(n)
                cou1 -= 1
            self.words.append(w)
            cou -= 1
    
    @staticmethod
    def _new2964(_arg1 : bool, _arg2 : str) -> 'DerivateGroup':
        res = DerivateGroup()
        res.is_generated = _arg1
        res.prefix = _arg2
        return res