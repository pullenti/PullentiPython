# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import gc
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.semantic.utils.ControlModelQuestion import ControlModelQuestion
from pullenti.semantic.internal.DerivateDictionary import DerivateDictionary
from pullenti.morph.MorphLang import MorphLang
from pullenti.semantic.internal.NextModelHelper import NextModelHelper

class DerivateService:
    """ Сервис для получение информации о словах. Однокоренные слова объединены в так называемые дериватные группы.
    В настоящий момент поддержаны русский и украинский языки.
    
    Сервис дериватных групп
    """
    
    @staticmethod
    def initialize(langs : 'MorphLang'=None) -> None:
        """ Инициализация внутренних словарей.
        Можно не вызывать, но тогда будет автоматически вызвано при первом обращении,
        и соответственно первое обращение отработает на несколько секунд дольше.
        Если инициализация идёт через Sdk.Initialize или ProcessorService.Initialize, то эту функцию вызывать не надо.
        
        Args:
            langs(MorphLang): по умолчанию, русский с украинским
        """
        if (langs is None or langs.is_undefined): 
            langs = MorphLang.RU
        NextModelHelper.initialize()
        ControlModelQuestion.initialize()
        DerivateService.load_languages(langs)
    
    __m_der_ru = None
    
    @staticmethod
    def get_loaded_languages() -> 'MorphLang':
        if (len(DerivateService.__m_der_ru._m_all_groups) > 0): 
            return (MorphLang.RU) | MorphLang.UA
        return MorphLang.UNKNOWN
    
    @staticmethod
    def load_languages(langs : 'MorphLang') -> None:
        if (langs.is_ru or langs.is_ua): 
            if (not DerivateService.__m_der_ru.init(MorphLang.RU, True)): 
                raise Utils.newException("Not found resource file e_ru.dat in Enplanatory", None)
        if (langs.is_ua): 
            pass
    
    @staticmethod
    def load_dictionary_ru(dat : bytearray) -> None:
        DerivateService.__m_der_ru.load(dat)
    
    @staticmethod
    def unload_languages(langs : 'MorphLang') -> None:
        if (langs.is_ru or langs.is_ua): 
            if (langs.is_ru and langs.is_ua): 
                DerivateService.__m_der_ru.unload()
        gc.collect()
    
    @staticmethod
    def find_derivates(word : str, try_variants : bool=True, lang : 'MorphLang'=None) -> typing.List['DerivateGroup']:
        """ Найти для слова дериватные группы DerivateGroup, в которые входит это слово
        (групп может быть несколько, но в большинстве случаев - одна)
        
        Args:
            word(str): слово в верхнем регистре и нормальной форме
            try_variants(bool): пытаться ли для неизвестных слов делать варианты
            lang(MorphLang): язык (по умолчанию, русский)
        
        Returns:
            typing.List[DerivateGroup]: список дериватных групп DerivateGroup
        """
        return DerivateService.__m_der_ru.find(word, try_variants, lang)
    
    @staticmethod
    def find_words(word : str, lang : 'MorphLang'=None) -> typing.List['DerivateWord']:
        """ Найти для слова его толковую информацию (среди дериватных групп)
        
        Args:
            word(str): слово в верхнем регистре и нормальной форме
            lang(MorphLang): возможный язык
        
        Returns:
            typing.List[DerivateWord]: список слов DerivateWord
        """
        grs = DerivateService.__m_der_ru.find(word, False, lang)
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
    def get_word_class_var(word : str, cla : 'MorphClass', lang : 'MorphLang'=None) -> str:
        """ Получить слова однокоренное слово заданной части речи.
        Например, для существительного "ГЛАГОЛ" вариант прилагательного: "ГЛАГОЛЬНЫЙ"
        
        Args:
            word(str): слово в верхнем регистре и нормальной форме
            cla(MorphClass): нужная часть речи
            lang(MorphLang): возможный язык
        
        Returns:
            str: вариант или null при ненахождении
        
        """
        grs = DerivateService.__m_der_ru.find(word, False, lang)
        if (grs is None): 
            return None
        for g in grs: 
            for w in g.words: 
                if (w.class0_ == cla): 
                    return w.spelling
        return None
    
    @staticmethod
    def is_animated(word : str, lang : 'MorphLang'=None) -> bool:
        """ Может ли быть одушевлённым
        
        Args:
            word(str): слово в верхнем регистре и нормальной форме
            lang(MorphLang): язык (по умолчанию, русский)
        
        Returns:
            bool: да-нет
        """
        grs = DerivateService.__m_der_ru.find(word, False, lang)
        if (grs is None): 
            return False
        for g in grs: 
            for w in g.words: 
                if (w.spelling == word): 
                    if (w.attrs.is_animated): 
                        return True
        return False
    
    @staticmethod
    def is_named(word : str, lang : 'MorphLang'=None) -> bool:
        """ Может ли иметь собственное имя
        
        Args:
            word(str): слово в верхнем регистре и нормальной форме
            lang(MorphLang): язык (по умолчанию, русский)
        
        Returns:
            bool: да-нет
        """
        grs = DerivateService.__m_der_ru.find(word, False, lang)
        if (grs is None): 
            return False
        for g in grs: 
            for w in g.words: 
                if (w.spelling == word): 
                    if (w.attrs.is_named): 
                        return True
        return False
    
    _m_lock = None
    
    @staticmethod
    def set_dictionary(dic : 'DerivateDictionary') -> None:
        DerivateService.__m_der_ru = dic
    
    # static constructor for class DerivateService
    @staticmethod
    def _static_ctor():
        DerivateService.__m_der_ru = DerivateDictionary()
        DerivateService._m_lock = object()

DerivateService._static_ctor()