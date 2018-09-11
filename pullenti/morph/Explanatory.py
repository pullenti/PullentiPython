# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import gc
import typing
import threading
from pullenti.unisharp.Utils import Utils
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.internal.DerivateDictionary import DerivateDictionary


class Explanatory:
    """ Сервис для получение толковой информации о словах.
     В настоящий момент поддержаны русский и украинский языки. """
    
    @staticmethod
    def initialize(langs : 'MorphLang'=MorphLang()) -> None:
        if (langs is None or langs.is_undefined): 
            langs = MorphLang.RU
        Explanatory.load_languages(langs)
    
    __m_der_ru = None
    
    @staticmethod
    def get_loaded_languages() -> 'MorphLang':
        """ Языки, морфологические словари для которых загружены в память """
        if (len(Explanatory.__m_der_ru._m_all_groups) > 0): 
            return (MorphLang.RU) | MorphLang.UA
        return MorphLang.UNKNOWN
    
    @staticmethod
    def load_languages(langs : 'MorphLang') -> None:
        if (langs.is_ru or langs.is_ua): 
            if (not Explanatory.__m_der_ru.init(MorphLang.RU)): 
                raise Utils.newException("Not found resource file e_ru.dat in Enplanatory", None)
        if (langs.is_ua): 
            pass
    
    @staticmethod
    def unload_languages(langs : 'MorphLang') -> None:
        if (langs.is_ru or langs.is_ua): 
            if (langs.is_ru and langs.is_ua): 
                Explanatory.__m_der_ru.unload()
        gc.collect()
    
    @staticmethod
    def find_derivates(word : str, try_variants : bool=True, lang : 'MorphLang'=MorphLang()) -> typing.List['DerivateGroup']:
        return Explanatory.__m_der_ru.find(word, try_variants, lang)
    
    @staticmethod
    def find_words(word : str, lang : 'MorphLang'=MorphLang()) -> typing.List['DerivateWord']:
        grs = Explanatory.__m_der_ru.find(word, False, lang)
        if (grs is None): 
            return None
        res = None
        for g in grs: 
            for w in g.words: 
                if (w.spelling == word): 
                    if (res is None): 
                        res = list()
                    res.append(w)
        return res
    
    @staticmethod
    def get_word_class_var(word : str, cla : 'MorphClass', lang : 'MorphLang'=MorphLang()) -> str:
        grs = Explanatory.__m_der_ru.find(word, False, lang)
        if (grs is None): 
            return None
        for g in grs: 
            for w in g.words: 
                if (w.class0_ == cla): 
                    return w.spelling
        return None
    
    @staticmethod
    def is_animated(word : str, lang : 'MorphLang'=MorphLang()) -> bool:
        grs = Explanatory.__m_der_ru.find(word, False, lang)
        if (grs is None): 
            return False
        for g in grs: 
            for w in g.words: 
                if (w.spelling == word): 
                    if (w.attrs.is_animated): 
                        return True
        return False
    
    @staticmethod
    def is_named(word : str, lang : 'MorphLang'=MorphLang()) -> bool:
        grs = Explanatory.__m_der_ru.find(word, False, lang)
        if (grs is None): 
            return False
        for g in grs: 
            for w in g.words: 
                if (w.spelling == word): 
                    if (w.attrs.is_named): 
                        return True
        return False
    
    _m_lock = None
    
    # static constructor for class Explanatory
    @staticmethod
    def _static_ctor():
        Explanatory.__m_der_ru = DerivateDictionary()
        Explanatory._m_lock = threading.Lock()

Explanatory._static_ctor()