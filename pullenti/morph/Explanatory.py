# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import gc
import typing
import threading
from pullenti.ntopy.Utils import Utils
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.internal.DerivateDictionary import DerivateDictionary


class Explanatory:
    """ Сервис для получение толковой информации о словах.
     В настоящий момент поддержаны русский и украинский языки. """
    
    @staticmethod
    def initialize(langs : 'MorphLang'=MorphLang()) -> None:
        """ Инициализация внутренних словарей.
         Можно не вызывать, но тогда будет автоматически вызвано при первом обращении,
         и соответственно первое обращение отработает на несколько секунд дольше.
        
        Args:
            langs(MorphLang): по умолчанию, русский с украинским
        """
        if (langs is None or langs.is_undefined): 
            langs = MorphLang.RU
        Explanatory.load_languages(langs)
    
    __m_der_ru = None
    
    @staticmethod
    def _get_loaded_languages() -> 'MorphLang':
        """ Языки, морфологические словари для которых загружены в память """
        if (len(Explanatory.__m_der_ru._m_all_groups) > 0): 
            return MorphLang.RU | MorphLang.UA
        return MorphLang.UNKNOWN
    
    @staticmethod
    def load_languages(langs : 'MorphLang') -> None:
        """ Загрузить язык(и), если они ещё не загружены
        
        Args:
            langs(MorphLang): 
        """
        if (langs.is_ru or langs.is_ua): 
            if (not Explanatory.__m_der_ru.init(MorphLang.RU)): 
                raise Utils.newException("Not found resource file e_ru.dat in Enplanatory", None)
        if (langs.is_ua): 
            pass
    
    @staticmethod
    def unload_languages(langs : 'MorphLang') -> None:
        """ Выгрузить язык(и), если они больше не нужны
        
        Args:
            langs(MorphLang): 
        """
        if (langs.is_ru or langs.is_ua): 
            if (langs.is_ru and langs.is_ua): 
                Explanatory.__m_der_ru.unload()
        gc.collect()
    
    @staticmethod
    def find_derivates(word : str, try_variants : bool=True, lang : 'MorphLang'=MorphLang()) -> typing.List['DerivateGroup']:
        """ Найти для слова дериативные группы, в которые входит это слово
         (групп может быть несколько, но в большинстве случаев - одна)
        
        Args:
            word(str): 
            try_variants(bool): 
            lang(MorphLang): 
        
        """
        return Explanatory.__m_der_ru.find(word, try_variants, lang)
    
    @staticmethod
    def find_words(word : str, lang : 'MorphLang'=MorphLang()) -> typing.List['DerivateWord']:
        """ Найти для слова его толковую информацию (среди деривативных групп)
        
        Args:
            word(str): нормальная форма слова
            lang(MorphLang): возможный язык
        
        """
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
        """ Получить вариант для слова аналог нужного типа.
         Например, для "ГЛАГОЛ" вариант прилагательного: "ГЛАГОЛЬНЫЙ"
        
        Args:
            word(str): исходное слово
            cla(MorphClass): нужный тип
            lang(MorphLang): возможный язык
        
        Returns:
            str: вариант или null при ненахождении
        """
        grs = Explanatory.__m_der_ru.find(word, False, lang)
        if (grs is None): 
            return None
        for g in grs: 
            for w in g.words: 
                if (w.class0 == cla): 
                    return w.spelling
        return None
    
    @staticmethod
    def is_animated(word : str, lang : 'MorphLang'=MorphLang()) -> bool:
        """ Может ли быть одушевлённым
        
        Args:
            word(str): 
            lang(MorphLang): язык (по умолчанию, русский)
        
        """
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
        """ Может ли иметь собственное имя
        
        Args:
            word(str): 
            lang(MorphLang): язык (по умолчанию, русский)
        
        """
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