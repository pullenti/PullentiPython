# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import EventHandler
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.internal.UnicodeInfo import UnicodeInfo
from pullenti.morph.internal.InnerMorphology import InnerMorphology
from pullenti.morph.MorphMiscInfo import MorphMiscInfo


class Morphology:
    """ Морфологический анализ текстов """
    
    @staticmethod
    def initialize(langs : 'MorphLang'=MorphLang()) -> None:
        """ Инициализация внутренних словарей.
         Можно не вызывать, но тогда будет автоматически вызвано при первом обращении к морфологии,
         и соответственно первый разбор отработает на несколько секунд дольше.
        
        Args:
            langs(MorphLang): по умолчанию, русский и английский
        """
        UnicodeInfo.initialize()
        if (langs is None or langs.is_undefined): 
            langs = (MorphLang.RU | MorphLang.EN)
        InnerMorphology._load_languages(langs)
    
    @staticmethod
    def _get_loaded_languages() -> 'MorphLang':
        """ Языки, морфологические словари для которых загружены в память """
        return InnerMorphology._get_loaded_languages()
    
    @staticmethod
    def load_languages(langs : 'MorphLang') -> None:
        """ Загрузить язык(и), если они ещё не загружены
        
        Args:
            langs(MorphLang): загружаемые языки
        """
        InnerMorphology._load_languages(langs)
    
    @staticmethod
    def unload_languages(langs : 'MorphLang') -> None:
        """ Выгрузить язык(и), если они больше не нужны
        
        Args:
            langs(MorphLang): выгружаемые языки
        """
        InnerMorphology._unload_languages(langs)
    
    __m_inner = None
    
    @staticmethod
    def tokenize(text : str) -> typing.List['MorphToken']:
        """ Произвести чистую токенизацию без формирования морф-вариантов
        
        Args:
            text(str): исходный текст
        
        Returns:
            typing.List[MorphToken]: последовательность результирующих лексем
        """
        if (Utils.isNullOrEmpty(text)): 
            return None
        res = Morphology.__m_inner.run(text, True, MorphLang.UNKNOWN, None, False)
        if (res is not None): 
            for r in res: 
                if (r.word_forms is None): 
                    r.word_forms = Morphology.__m_empty_word_forms
                for wf in r.word_forms: 
                    if (wf.misc is None): 
                        wf.misc = Morphology.__m_empty_misc
        return res
    
    @staticmethod
    def process(text : str, lang : 'MorphLang'=None, progress : EventHandler=None) -> typing.List['MorphToken']:
        """ Произвести морфологический анализ текста
        
        Args:
            text(str): исходный текст
            lang(MorphLang): базовый язык (если null, то будет определён автоматически)
            progress(EventHandler): это для бегунка
        
        Returns:
            typing.List[MorphToken]: последовательность результирующих лексем
        """
        if (Utils.isNullOrEmpty(text)): 
            return None
        res = Morphology.__m_inner.run(text, False, lang, progress, False)
        if (res is not None): 
            for r in res: 
                if (r.word_forms is None): 
                    r.word_forms = Morphology.__m_empty_word_forms
                for wf in r.word_forms: 
                    if (wf.misc is None): 
                        wf.misc = Morphology.__m_empty_misc
        return res
    
    __m_empty_word_forms = None
    
    __m_empty_misc = None
    
    @staticmethod
    def get_all_wordforms(word : str, lang : 'MorphLang'=MorphLang()) -> typing.List['MorphWordForm']:
        """ Получить все варианты словоформ для нормальной формы слова
        
        Args:
            word(str): 
            lang(MorphLang): язык (по умолчанию, русский)
        
        Returns:
            typing.List[MorphWordForm]: список словоформ
        """
        res = Morphology.__m_inner.get_all_wordforms(word, lang)
        if (res is not None): 
            for r in res: 
                if (r.misc is None): 
                    r.misc = Morphology.__m_empty_misc
        return res
    
    @staticmethod
    def get_wordform(word : str, morph_info : 'MorphBaseInfo') -> str:
        """ Получить вариант написания словоформы
        
        Args:
            word(str): слово
            morph_info(MorphBaseInfo): морфологическая информация
        
        Returns:
            str: вариант написания
        """
        from pullenti.morph.MorphWordForm import MorphWordForm
        if (morph_info is None or Utils.isNullOrEmpty(word)): 
            return word
        cla = morph_info.class0_
        if (cla.is_undefined): 
            mi0 = Morphology.get_word_base_info(word, MorphLang(), False, False)
            if (mi0 is not None): 
                cla = mi0.class0_
        for ch in word: 
            if (ch.islower()): 
                word = word.upper()
                break
        return Utils.ifNotNull(Morphology.__m_inner.get_wordform(word, cla, morph_info.gender, morph_info.case, morph_info.number, morph_info.language, (morph_info if isinstance(morph_info, MorphWordForm) else None)), word)
    
    @staticmethod
    def get_word_base_info(word : str, lang : 'MorphLang'=MorphLang(), is_case_nominative : bool=False, in_dict_only : bool=False) -> 'MorphBaseInfo':
        """ Получить для словоформы род\число\падеж
        
        Args:
            word(str): словоформа
            lang(MorphLang): возможный язык
            is_case_nominative(bool): исходное слово в именительном падеже (иначе считается падеж любым)
            in_dict_only(bool): при true не строить гипотезы для несловарных слов
        
        Returns:
            MorphBaseInfo: базовая морфологическая информация
        """
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.morph.MorphClass import MorphClass
        mt = Morphology.__m_inner.run(word, False, lang, None, False)
        bi = MorphWordForm()
        cla = MorphClass()
        if (mt is not None and len(mt) > 0): 
            for k in range(2):
                ok = False
                for wf in mt[0].word_forms: 
                    if (k == 0): 
                        if (not wf.is_in_dictionary): 
                            continue
                    elif (wf.is_in_dictionary): 
                        continue
                    if (is_case_nominative): 
                        if (not wf.case.is_nominative and not wf.case.is_undefined): 
                            continue
                    cla.value |= wf.class0_.value
                    bi.gender |= wf.gender
                    bi.case |= wf.case
                    bi.number |= wf.number
                    if (wf.misc is not None and bi.misc is None): 
                        bi.misc = wf.misc
                    ok = True
                if (ok or in_dict_only): 
                    break
        bi.class0_ = cla
        return bi
    
    @staticmethod
    def correct_word(word : str, lang : 'MorphLang'=MorphLang()) -> str:
        """ Попробовать откорретировать одну букву словоформы, чтобы получилось словарное слово
        
        Args:
            word(str): искаженное слово
            lang(MorphLang): возможный язык
        
        Returns:
            str: откорректированное слово или null при невозможности
        """
        return Morphology.__m_inner.correct_word_by_morph(word, lang)
    
    @staticmethod
    def convert_adverb_to_adjective(adverb : str, bi : 'MorphBaseInfo') -> str:
        """ Преобразовать наречие в прилагательное (это пока только для русского языка)
        
        Args:
            adverb(str): наречие
            bi(MorphBaseInfo): род число падеж
        
        Returns:
            str: прилагательное
        """
        from pullenti.morph.MorphClass import MorphClass
        if (adverb is None or (len(adverb) < 4)): 
            return None
        last = adverb[len(adverb) - 1]
        if (last != 'О' and last != 'Е'): 
            return adverb
        var1 = adverb[0 : (len(adverb) - 1)] + "ИЙ"
        var2 = adverb[0 : (len(adverb) - 1)] + "ЫЙ"
        bi1 = Morphology.get_word_base_info(var1, MorphLang(), False, False)
        bi2 = Morphology.get_word_base_info(var2, MorphLang(), False, False)
        var = var1
        if (not bi1.class0_.is_adjective and bi2.class0_.is_adjective): 
            var = var2
        if (bi is None): 
            return var
        return Utils.ifNotNull(Morphology.__m_inner.get_wordform(var, MorphClass.ADJECTIVE, bi.gender, bi.case, bi.number, MorphLang.UNKNOWN, None), var)
    
    # static constructor for class Morphology
    @staticmethod
    def _static_ctor():
        Morphology.__m_inner = InnerMorphology()
        Morphology.__m_empty_word_forms = list()
        Morphology.__m_empty_misc = MorphMiscInfo()

Morphology._static_ctor()