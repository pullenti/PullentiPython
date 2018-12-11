# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

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
    def initialize(langs : 'MorphLang'=None) -> None:
        """ Инициализация внутренних словарей.
         Можно не вызывать, но тогда будет автоматически вызвано при первом обращении,
         и соответственно первое обращение отработает на несколько секунд дольше.
        
        Args:
            langs(MorphLang): по умолчанию, русский с украинским
        """
        if (langs is None or langs.is_undefined): 
            langs = MorphLang.RU
        Explanatory.loadLanguages(langs)
    
    __m_der_ru = None
    
    @staticmethod
    def getLoadedLanguages() -> 'MorphLang':
        """ Языки, морфологические словари для которых загружены в память """
        if (len(Explanatory.__m_der_ru._m_all_groups) > 0): 
            return (MorphLang.RU) | MorphLang.UA
        return MorphLang.UNKNOWN
    
    @staticmethod
    def loadLanguages(langs : 'MorphLang') -> None:
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
    def unloadLanguages(langs : 'MorphLang') -> None:
        """ Выгрузить язык(и), если они больше не нужны
        
        Args:
            langs(MorphLang): 
        """
        if (langs.is_ru or langs.is_ua): 
            if (langs.is_ru and langs.is_ua): 
                Explanatory.__m_der_ru.unload()
        gc.collect()
    
    @staticmethod
    def findDerivates(word : str, try_variants : bool=True, lang : 'MorphLang'=None) -> typing.List['DerivateGroup']:
        """ Найти для слова дериативные группы, в которые входит это слово
         (групп может быть несколько, но в большинстве случаев - одна)
        
        Args:
            word(str): 
            try_variants(bool): 
            lang(MorphLang): 
        
        """
        return Explanatory.__m_der_ru.find(word, try_variants, lang)
    
    @staticmethod
    def findWords(word : str, lang : 'MorphLang'=None) -> typing.List['DerivateWord']:
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
    def getWordClassVar(word : str, cla : 'MorphClass', lang : 'MorphLang'=None) -> str:
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
                if (w.class0_ == cla): 
                    return w.spelling
        return None
    
    @staticmethod
    def isAnimated(word : str, lang : 'MorphLang'=None) -> bool:
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
    def isNamed(word : str, lang : 'MorphLang'=None) -> bool:
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