# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import EventHandler

from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphMiscInfo import MorphMiscInfo
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.internal.UnicodeInfo import UnicodeInfo
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.morph.internal.InnerMorphology import InnerMorphology

class MorphologyService:
    """ Сервис морфологического анализа текстов (POS-tagger).
    
    Сервис морфологии
    """
    
    @staticmethod
    def initialize(langs : 'MorphLang'=None) -> None:
        """ Инициализация внутренних словарей.
        Можно не вызывать, но тогда будет автоматически вызвано при первом обращении к морфологии,
        и соответственно первый разбор отработает на несколько секунд дольше.
        Если используете Sdk.Initialize() или ProcessorService.Initialize(), то тогда эту функцию вызывать не нужно,
        так как там внутри это делается.
        
        Args:
            langs(MorphLang): по умолчанию, русский и английский
        """
        UnicodeInfo.initialize()
        if (langs is None or langs.is_undefined): 
            langs = ((MorphLang.RU) | MorphLang.EN)
        MorphologyService.__m_morph._load_languages(langs, MorphologyService.LAZY_LOAD)
    
    @staticmethod
    def get_loaded_languages() -> 'MorphLang':
        """ Языки, морфологические словари для которых загружены в память """
        return MorphologyService.__m_morph._loaded_languages
    
    @staticmethod
    def load_languages(langs : 'MorphLang') -> None:
        """ Загрузить язык(и), если они ещё не загружены
        
        Args:
            langs(MorphLang): загружаемые языки
        """
        MorphologyService.__m_morph._load_languages(langs, MorphologyService.LAZY_LOAD)
    
    @staticmethod
    def unload_languages(langs : 'MorphLang') -> None:
        """ Выгрузить язык(и), если они больше не нужны
        
        Args:
            langs(MorphLang): выгружаемые языки
        """
        MorphologyService.__m_morph._unload_languages(langs)
    
    __m_empty_word_forms = None
    
    __m_empty_misc = None
    
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
        res = MorphologyService.__m_morph.run(text, True, MorphLang.UNKNOWN, False, None)
        if (res is not None): 
            for r in res: 
                if (r.word_forms is None): 
                    r.word_forms = MorphologyService.__m_empty_word_forms
                for wf in r.word_forms: 
                    if (wf.misc is None): 
                        wf.misc = MorphologyService.__m_empty_misc
        return res
    
    @staticmethod
    def process(text : str, lang : 'MorphLang'=None, progress : EventHandler=None) -> typing.List['MorphToken']:
        """ Произвести морфологический анализ текста. Если используете морфологию в составе лингвистического процессора из
        ProcessorService, то эту функцию явно вызывать не придётся.
        
        Args:
            text(str): исходный текст
            lang(MorphLang): базовый язык (если null, то будет определён автоматически)
            progress(EventHandler): это для бегунка
        
        Returns:
            typing.List[MorphToken]: последовательность результирующих лексем MorphToken
        
        """
        if (Utils.isNullOrEmpty(text)): 
            return None
        res = MorphologyService.__m_morph.run(text, False, lang, False, progress)
        if (res is not None): 
            for r in res: 
                if (r.word_forms is None): 
                    r.word_forms = MorphologyService.__m_empty_word_forms
                for wf in r.word_forms: 
                    if (wf.misc is None): 
                        wf.misc = MorphologyService.__m_empty_misc
        return res
    
    @staticmethod
    def get_all_wordforms(word : str, lang : 'MorphLang'=None) -> typing.List['MorphWordForm']:
        """ Получить все варианты словоформ для нормальной формы слова
        
        Args:
            word(str): 
            lang(MorphLang): язык (по умолчанию, русский)
        
        Returns:
            typing.List[MorphWordForm]: список словоформ MorphWordForm
        """
        res = MorphologyService.__m_morph.get_all_wordforms(word, lang)
        if (res is not None): 
            for r in res: 
                if (r.misc is None): 
                    r.misc = MorphologyService.__m_empty_misc
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
        if (morph_info is None or Utils.isNullOrEmpty(word)): 
            return word
        cla = morph_info.class0_
        if (cla.is_undefined): 
            mi0 = MorphologyService.get_word_base_info(word, None, False, False)
            if (mi0 is not None): 
                cla = mi0.class0_
        word1 = word
        for ch in word: 
            if (str.islower(ch)): 
                word1 = word.upper()
                break
        wf = Utils.asObjectOrNull(morph_info, MorphWordForm)
        res = MorphologyService.__m_morph.get_wordform(word1, cla, morph_info.gender, morph_info.case_, morph_info.number, morph_info.language, wf)
        if (Utils.isNullOrEmpty(res)): 
            return word
        return res
    
    @staticmethod
    def get_word_base_info(word : str, lang : 'MorphLang'=None, is_case_nominative : bool=False, in_dict_only : bool=False) -> 'MorphWordForm':
        """ Получить для словоформы род\число\падеж
        
        Args:
            word(str): словоформа
            lang(MorphLang): возможный язык
            is_case_nominative(bool): исходное слово в именительном падеже (иначе считается падеж любым)
            in_dict_only(bool): при true не строить гипотезы для несловарных слов
        
        Returns:
            MorphWordForm: базовая морфологическая информация
        """
        mt = MorphologyService.__m_morph.run(word, False, lang, False, None)
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
                        if (not wf.case_.is_nominative and not wf.case_.is_undefined): 
                            continue
                    cla.value |= wf.class0_.value
                    bi.gender = Utils.valToEnum((bi.gender) | (wf.gender), MorphGender)
                    bi.case_ = (bi.case_) | wf.case_
                    bi.number = Utils.valToEnum((bi.number) | (wf.number), MorphNumber)
                    if (wf.misc is not None and bi.misc is None): 
                        bi.misc = wf.misc
                    ok = True
                if (ok or in_dict_only): 
                    break
        bi.class0_ = cla
        return bi
    
    @staticmethod
    def correct_word(word : str, lang : 'MorphLang'=None) -> str:
        """ Попробовать откорретировать одну букву словоформы, чтобы получилось словарное слово
        
        Args:
            word(str): искаженное слово
            lang(MorphLang): возможный язык
        
        Returns:
            str: откорректированное слово или null при невозможности
        """
        return MorphologyService.__m_morph.correct_word_by_morph(word, lang)
    
    @staticmethod
    def convert_adverb_to_adjective(adverb : str, bi : 'MorphBaseInfo') -> str:
        """ Преобразовать наречие в прилагательное (это пока только для русского языка)
        
        Args:
            adverb(str): наречие
            bi(MorphBaseInfo): род число падеж
        
        Returns:
            str: прилагательное
        """
        if (adverb is None or (len(adverb) < 4)): 
            return None
        last = adverb[len(adverb) - 1]
        if (last != 'О' and last != 'Е'): 
            return adverb
        var1 = adverb[0:0+len(adverb) - 1] + "ИЙ"
        var2 = adverb[0:0+len(adverb) - 1] + "ЫЙ"
        bi1 = MorphologyService.get_word_base_info(var1, None, False, False)
        bi2 = MorphologyService.get_word_base_info(var2, None, False, False)
        var = var1
        if (not bi1.class0_.is_adjective and bi2.class0_.is_adjective): 
            var = var2
        if (bi is None): 
            return var
        return Utils.ifNotNull(MorphologyService.__m_morph.get_wordform(var, MorphClass.ADJECTIVE, bi.gender, bi.case_, bi.number, MorphLang.UNKNOWN, None), var)
    
    LAZY_LOAD = True
    # При и нициализации не грузить всю морфологиюю сразу в память, а подгружать по мере необходимости.
    # Сильно экономит время (при инициализации) и память.
    
    __m_morph = None
    
    # static constructor for class MorphologyService
    @staticmethod
    def _static_ctor():
        MorphologyService.__m_empty_word_forms = list()
        MorphologyService.__m_empty_misc = MorphMiscInfo()
        MorphologyService.__m_morph = InnerMorphology()

MorphologyService._static_ctor()