# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import threading
import gc
import math
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Misc import EventHandler
from pullenti.unisharp.Misc import ProgressEventArgs

from pullenti.morph.CharsInfo import CharsInfo
from pullenti.morph.MorphToken import MorphToken
from pullenti.morph.internal.UnicodeInfo import UnicodeInfo
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.internal.MorphEngine import MorphEngine
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.morph.internal.TextWrapper import TextWrapper
from pullenti.morph.internal.UniLexWrap import UniLexWrap
from pullenti.morph.LanguageHelper import LanguageHelper

class InnerMorphology:
    
    def __init__(self) -> None:
        self.__m_engine_ru = MorphEngine()
        self.__m_engine_en = MorphEngine()
        self.__m_engine_ua = MorphEngine()
        self.__m_engine_by = MorphEngine()
        self.__m_engine_kz = MorphEngine()
        self.__m_lock = threading.Lock()
        self.__last_percent = 0
    
    @property
    def _loaded_languages(self) -> 'MorphLang':
        return ((self.__m_engine_ru.language) | self.__m_engine_en.language | self.__m_engine_ua.language) | self.__m_engine_by.language | self.__m_engine_kz.language
    
    def _load_languages(self, langs : 'MorphLang', lazy_load : bool) -> None:
        if (langs.is_ru and not self.__m_engine_ru.language.is_ru): 
            with self.__m_lock: 
                if (not self.__m_engine_ru.language.is_ru): 
                    if (not self.__m_engine_ru.initialize(MorphLang.RU, lazy_load)): 
                        raise Utils.newException("Not found resource file m_ru.dat in Morphology", None)
        if (langs.is_en and not self.__m_engine_en.language.is_en): 
            with self.__m_lock: 
                if (not self.__m_engine_en.language.is_en): 
                    if (not self.__m_engine_en.initialize(MorphLang.EN, lazy_load)): 
                        raise Utils.newException("Not found resource file m_en.dat in Morphology", None)
        if (langs.is_ua and not self.__m_engine_ua.language.is_ua): 
            with self.__m_lock: 
                if (not self.__m_engine_ua.language.is_ua): 
                    self.__m_engine_ua.initialize(MorphLang.UA, lazy_load)
        if (langs.is_by and not self.__m_engine_by.language.is_by): 
            with self.__m_lock: 
                if (not self.__m_engine_by.language.is_by): 
                    self.__m_engine_by.initialize(MorphLang.BY, lazy_load)
        if (langs.is_kz and not self.__m_engine_kz.language.is_kz): 
            with self.__m_lock: 
                if (not self.__m_engine_kz.language.is_kz): 
                    self.__m_engine_kz.initialize(MorphLang.KZ, lazy_load)
    
    def _unload_languages(self, langs : 'MorphLang') -> None:
        """ Выгрузить язык(и), если они больше не нужны
        
        Args:
            langs(MorphLang): 
        """
        if (langs.is_ru and self.__m_engine_ru.language.is_ru): 
            self.__m_engine_ru = MorphEngine()
        if (langs.is_en and self.__m_engine_en.language.is_en): 
            self.__m_engine_en = MorphEngine()
        if (langs.is_ua and self.__m_engine_ua.language.is_ua): 
            self.__m_engine_ua = MorphEngine()
        if (langs.is_by and self.__m_engine_by.language.is_by): 
            self.__m_engine_by = MorphEngine()
        if (langs.is_kz and self.__m_engine_kz.language.is_kz): 
            self.__m_engine_kz = MorphEngine()
        gc.collect()
    
    def set_engines(self, engine : 'MorphEngine') -> None:
        if (engine is not None): 
            self.__m_engine_ru = engine
            self.__m_engine_en = engine
            self.__m_engine_ua = engine
            self.__m_engine_by = engine
    
    def __on_progress(self, val : int, max0_ : int, progress : EventHandler) -> None:
        p = val
        if (max0_ > 0xFFFF): 
            p = (math.floor(p / ((math.floor(max0_ / 100)))))
        else: 
            p = (math.floor((p * 100) / max0_))
        if (p != self.__last_percent and progress is not None): 
            progress.call(None, ProgressEventArgs(p, None))
        self.__last_percent = p
    
    def run(self, text : str, only_tokenizing : bool, dlang : 'MorphLang', good_text : bool, progress : EventHandler) -> typing.List['MorphToken']:
        """ Произвести морфологический анализ текста
        
        Args:
            text(str): исходный текст
            lang: язык (если null, то попробует определить)
        
        Returns:
            typing.List[MorphToken]: последовательность результирующих морфем
        """
        if (Utils.isNullOrEmpty(text)): 
            return None
        twr = TextWrapper(text, good_text)
        twrch = twr.chars
        res = list()
        uni_lex = dict()
        term0 = None
        pure_rus_words = 0
        pure_ukr_words = 0
        pure_by_words = 0
        pure_kz_words = 0
        tot_rus_words = 0
        tot_ukr_words = 0
        tot_by_words = 0
        tot_kz_words = 0
        i = 0
        first_pass3471 = True
        while True:
            if first_pass3471: first_pass3471 = False
            else: i += 1
            if (not (i < twr.length)): break
            ty = self._get_char_typ(twrch[i])
            if (ty == 0): 
                continue
            if (ty > 2): 
                j = (i + 1)
            else: 
                j = (i + 1)
                while j < twr.length: 
                    if (self._get_char_typ(twrch[j]) != ty): 
                        break
                    j += 1
            wstr = text[i:i+j - i]
            term = None
            if (good_text): 
                term = wstr
            else: 
                trstr = LanguageHelper.transliteral_correction(wstr, term0, False)
                term = LanguageHelper.correct_word(trstr)
            if (Utils.isNullOrEmpty(term)): 
                i = (j - 1)
                continue
            lang = LanguageHelper._get_word_lang(term)
            if (lang == MorphLang.UA): 
                pure_ukr_words += 1
            elif (lang == MorphLang.RU): 
                pure_rus_words += 1
            elif (lang == MorphLang.BY): 
                pure_by_words += 1
            elif (lang == MorphLang.KZ): 
                pure_kz_words += 1
            if ((((lang) & MorphLang.RU)) != MorphLang.UNKNOWN): 
                tot_rus_words += 1
            if ((((lang) & MorphLang.UA)) != MorphLang.UNKNOWN): 
                tot_ukr_words += 1
            if ((((lang) & MorphLang.BY)) != MorphLang.UNKNOWN): 
                tot_by_words += 1
            if ((((lang) & MorphLang.KZ)) != MorphLang.UNKNOWN): 
                tot_kz_words += 1
            if (ty == 1): 
                term0 = term
            lemmas = None
            if (ty == 1 and not only_tokenizing): 
                wraplemmas1 = RefOutArgWrapper(None)
                inoutres2 = Utils.tryGetValue(uni_lex, term, wraplemmas1)
                lemmas = wraplemmas1.value
                if (not inoutres2): 
                    nuni = UniLexWrap(lang)
                    uni_lex[term] = nuni
                    lemmas = nuni
            tok = MorphToken()
            tok.term = term
            tok.begin_char = i
            if (i == 733860): 
                pass
            tok.end_char = (j - 1)
            tok.tag = (lemmas)
            res.append(tok)
            i = (j - 1)
        def_lang = MorphLang()
        if (dlang is not None): 
            def_lang.value = dlang.value
        if (pure_rus_words > pure_ukr_words and pure_rus_words > pure_by_words and pure_rus_words > pure_kz_words): 
            def_lang = MorphLang.RU
        elif (tot_rus_words > tot_ukr_words and tot_rus_words > tot_by_words and tot_rus_words > tot_kz_words): 
            def_lang = MorphLang.RU
        elif (pure_ukr_words > pure_rus_words and pure_ukr_words > pure_by_words and pure_ukr_words > pure_kz_words): 
            def_lang = MorphLang.UA
        elif (tot_ukr_words > tot_rus_words and tot_ukr_words > tot_by_words and tot_ukr_words > tot_kz_words): 
            def_lang = MorphLang.UA
        elif (pure_kz_words > pure_rus_words and pure_kz_words > pure_ukr_words and pure_kz_words > pure_by_words): 
            def_lang = MorphLang.KZ
        elif (tot_kz_words > tot_rus_words and tot_kz_words > tot_ukr_words and tot_kz_words > tot_by_words): 
            def_lang = MorphLang.KZ
        elif (pure_by_words > pure_rus_words and pure_by_words > pure_ukr_words and pure_by_words > pure_kz_words): 
            def_lang = MorphLang.BY
        elif (tot_by_words > tot_rus_words and tot_by_words > tot_ukr_words and tot_by_words > tot_kz_words): 
            if (tot_rus_words > 10 and tot_by_words > (tot_rus_words + 20)): 
                def_lang = MorphLang.BY
            elif (tot_rus_words == 0 or tot_by_words >= (tot_rus_words * 2)): 
                def_lang = MorphLang.BY
        if (((def_lang.is_undefined or def_lang.is_ua)) and tot_rus_words > 0): 
            if (((tot_ukr_words > tot_rus_words and self.__m_engine_ua.language.is_ua)) or ((tot_by_words > tot_rus_words and self.__m_engine_by.language.is_by)) or ((tot_kz_words > tot_rus_words and self.__m_engine_kz.language.is_kz))): 
                cou0 = 0
                tot_kz_words = 0
                tot_ukr_words = tot_kz_words
                tot_by_words = tot_ukr_words
                tot_rus_words = tot_by_words
                for kp in uni_lex.items(): 
                    lang = MorphLang()
                    wraplang3 = RefOutArgWrapper(lang)
                    kp[1].word_forms = self.__process_one_word(kp[0], wraplang3)
                    lang = wraplang3.value
                    if (kp[1].word_forms is not None): 
                        for wf in kp[1].word_forms: 
                            lang |= wf.language
                    kp[1].lang = lang
                    if (lang.is_ru): 
                        tot_rus_words += 1
                    if (lang.is_ua): 
                        tot_ukr_words += 1
                    if (lang.is_by): 
                        tot_by_words += 1
                    if (lang.is_kz): 
                        tot_kz_words += 1
                    if (lang.is_cyrillic): 
                        cou0 += 1
                    if (cou0 >= 100): 
                        break
                if (tot_rus_words > ((math.floor(tot_by_words / 2))) and tot_rus_words > ((math.floor(tot_ukr_words / 2)))): 
                    def_lang = MorphLang.RU
                elif (tot_ukr_words > ((math.floor(tot_rus_words / 2))) and tot_ukr_words > ((math.floor(tot_by_words / 2)))): 
                    def_lang = MorphLang.UA
                elif (tot_by_words > ((math.floor(tot_rus_words / 2))) and tot_by_words > ((math.floor(tot_ukr_words / 2)))): 
                    def_lang = MorphLang.BY
            elif (def_lang.is_undefined): 
                def_lang = MorphLang.RU
        cou = 0
        tot_kz_words = 0
        tot_ukr_words = tot_kz_words
        tot_by_words = tot_ukr_words
        tot_rus_words = tot_by_words
        for kp in uni_lex.items(): 
            lang = def_lang
            if (lang.is_undefined): 
                if (tot_rus_words > tot_by_words and tot_rus_words > tot_ukr_words and tot_rus_words > tot_kz_words): 
                    lang = MorphLang.RU
                elif (tot_ukr_words > tot_rus_words and tot_ukr_words > tot_by_words and tot_ukr_words > tot_kz_words): 
                    lang = MorphLang.UA
                elif (tot_by_words > tot_rus_words and tot_by_words > tot_ukr_words and tot_by_words > tot_kz_words): 
                    lang = MorphLang.BY
                elif (tot_kz_words > tot_rus_words and tot_kz_words > tot_ukr_words and tot_kz_words > tot_by_words): 
                    lang = MorphLang.KZ
            wraplang4 = RefOutArgWrapper(lang)
            kp[1].word_forms = self.__process_one_word(kp[0], wraplang4)
            lang = wraplang4.value
            kp[1].lang = lang
            if ((((lang) & MorphLang.RU)) != MorphLang.UNKNOWN): 
                tot_rus_words += 1
            if ((((lang) & MorphLang.UA)) != MorphLang.UNKNOWN): 
                tot_ukr_words += 1
            if ((((lang) & MorphLang.BY)) != MorphLang.UNKNOWN): 
                tot_by_words += 1
            if ((((lang) & MorphLang.KZ)) != MorphLang.UNKNOWN): 
                tot_kz_words += 1
            if (progress is not None): 
                self.__on_progress(cou, len(uni_lex), progress)
            cou += 1
        empty_list = None
        for r in res: 
            uni = Utils.asObjectOrNull(r.tag, UniLexWrap)
            r.tag = None
            if (uni is None or uni.word_forms is None or len(uni.word_forms) == 0): 
                if (empty_list is None): 
                    empty_list = list()
                r.word_forms = empty_list
                if (uni is not None): 
                    r.language = uni.lang
            else: 
                r.word_forms = uni.word_forms
        if (not good_text): 
            i = 0
            first_pass3472 = True
            while True:
                if first_pass3472: first_pass3472 = False
                else: i += 1
                if (not (i < (len(res) - 2))): break
                ui0 = twrch[res[i].begin_char]
                ui1 = twrch[res[i + 1].begin_char]
                ui2 = twrch[res[i + 2].begin_char]
                if (ui1.is_quot): 
                    p = res[i + 1].begin_char
                    if ((p >= 2 and "БбТт".find(text[p - 1]) >= 0 and ((p + 3) < len(text))) and "ЕеЯяЁё".find(text[p + 1]) >= 0): 
                        wstr = LanguageHelper.transliteral_correction(LanguageHelper.correct_word("{0}Ъ{1}".format(res[i].get_source_text(text), res[i + 2].get_source_text(text))), None, False)
                        li = self.__process_one_word0(wstr)
                        if (li is not None and len(li) > 0 and li[0].is_in_dictionary): 
                            res[i].end_char = res[i + 2].end_char
                            res[i].term = wstr
                            res[i].word_forms = li
                            del res[i + 1:i + 1+2]
                    elif ((ui1.is_apos and p > 0 and str.isalpha(text[p - 1])) and ((p + 1) < len(text)) and str.isalpha(text[p + 1])): 
                        if (def_lang == MorphLang.UA or (((res[i].language) & MorphLang.UA)) != MorphLang.UNKNOWN or (((res[i + 2].language) & MorphLang.UA)) != MorphLang.UNKNOWN): 
                            wstr = LanguageHelper.transliteral_correction(LanguageHelper.correct_word("{0}{1}".format(res[i].get_source_text(text), res[i + 2].get_source_text(text))), None, False)
                            li = self.__process_one_word0(wstr)
                            okk = True
                            if (okk): 
                                res[i].end_char = res[i + 2].end_char
                                res[i].term = wstr
                                if (li is None): 
                                    li = list()
                                if (li is not None and len(li) > 0): 
                                    res[i].language = li[0].language
                                res[i].word_forms = li
                                del res[i + 1:i + 1+2]
                elif (((ui1.uni_char == '3' or ui1.uni_char == '4')) and res[i + 1].length == 1): 
                    src = ("З" if ui1.uni_char == '3' else "Ч")
                    i0 = i + 1
                    if ((res[i].end_char + 1) == res[i + 1].begin_char and ui0.is_cyrillic): 
                        i0 -= 1
                        src = (res[i0].get_source_text(text) + src)
                    i1 = i + 1
                    if ((res[i + 1].end_char + 1) == res[i + 2].begin_char and ui2.is_cyrillic): 
                        i1 += 1
                        src += res[i1].get_source_text(text)
                    if (len(src) > 2): 
                        wstr = LanguageHelper.transliteral_correction(LanguageHelper.correct_word(src), None, False)
                        li = self.__process_one_word0(wstr)
                        if (li is not None and len(li) > 0 and li[0].is_in_dictionary): 
                            res[i0].end_char = res[i1].end_char
                            res[i0].term = wstr
                            res[i0].word_forms = li
                            del res[i0 + 1:i0 + 1+i1 - i0]
                elif ((ui1.is_hiphen and ui0.is_letter and ui2.is_letter) and res[i].end_char > res[i].begin_char and res[i + 2].end_char > res[i + 2].begin_char): 
                    newline = False
                    sps = 0
                    j = (res[i + 1].end_char + 1)
                    while j < res[i + 2].begin_char: 
                        if (text[j] == '\r' or text[j] == '\n'): 
                            newline = True
                            sps += 1
                        elif (not Utils.isWhitespace(text[j])): 
                            break
                        else: 
                            sps += 1
                        j += 1
                    full_word = LanguageHelper.correct_word(res[i].get_source_text(text) + res[i + 2].get_source_text(text))
                    if (not newline): 
                        if (full_word in uni_lex or full_word == "ИЗЗА"): 
                            newline = True
                        elif (text[res[i + 1].begin_char] == (chr(0x00AD))): 
                            newline = True
                        elif (LanguageHelper.ends_with_ex(res[i].get_source_text(text), "О", "о", None, None) and len(res[i + 2].word_forms) > 0 and res[i + 2].word_forms[0].is_in_dictionary): 
                            if (text[res[i + 1].begin_char] == '¬'): 
                                li = self.__process_one_word0(full_word)
                                if (li is not None and len(li) > 0 and li[0].is_in_dictionary): 
                                    newline = True
                        elif ((res[i].end_char + 2) == res[i + 2].begin_char): 
                            if (not str.isupper(text[res[i + 2].begin_char]) and (sps < 2) and len(full_word) > 4): 
                                newline = True
                                if ((i + 3) < len(res)): 
                                    ui3 = twrch[res[i + 3].begin_char]
                                    if (ui3.is_hiphen): 
                                        newline = False
                        elif (((res[i].end_char + 1) == res[i + 1].begin_char and sps > 0 and (sps < 3)) and len(full_word) > 4): 
                            newline = True
                    if (newline): 
                        li = self.__process_one_word0(full_word)
                        if (li is not None and len(li) > 0 and ((li[0].is_in_dictionary or full_word in uni_lex))): 
                            res[i].end_char = res[i + 2].end_char
                            res[i].term = full_word
                            res[i].word_forms = li
                            del res[i + 1:i + 1+2]
                    else: 
                        pass
                elif ((ui1.is_letter and ui0.is_letter and res[i].length > 2) and res[i + 1].length > 1): 
                    if (ui0.is_upper != ui1.is_upper): 
                        continue
                    if (not ui0.is_cyrillic or not ui1.is_cyrillic): 
                        continue
                    newline = False
                    j = (res[i].end_char + 1)
                    while j < res[i + 1].begin_char: 
                        if (twrch[j].code == 0xD or twrch[j].code == 0xA): 
                            newline = True
                            break
                        j += 1
                    if (not newline): 
                        continue
                    full_word = LanguageHelper.correct_word(res[i].get_source_text(text) + res[i + 1].get_source_text(text))
                    if (not full_word in uni_lex): 
                        continue
                    li = self.__process_one_word0(full_word)
                    if (li is not None and len(li) > 0 and li[0].is_in_dictionary): 
                        res[i].end_char = res[i + 1].end_char
                        res[i].term = full_word
                        res[i].word_forms = li
                        del res[i + 1]
        i = 0
        first_pass3473 = True
        while True:
            if first_pass3473: first_pass3473 = False
            else: i += 1
            if (not (i < len(res))): break
            mt = res[i]
            mt.char_info = CharsInfo()
            ui0 = twrch[mt.begin_char]
            ui00 = UnicodeInfo.ALL_CHARS[ord((mt.term[0]))]
            j = (mt.begin_char + 1)
            while j <= mt.end_char: 
                if (ui0.is_letter): 
                    break
                ui0 = twrch[j]
                j += 1
            if (ui0.is_letter): 
                mt.char_info.is_letter = True
                if (ui00.is_latin): 
                    mt.char_info.is_latin_letter = True
                elif (ui00.is_cyrillic): 
                    mt.char_info.is_cyrillic_letter = True
                if (mt.language == MorphLang.UNKNOWN): 
                    if (LanguageHelper.is_cyrillic(mt.term)): 
                        mt.language = (MorphLang.RU if def_lang.is_undefined else def_lang)
                if (good_text): 
                    continue
                all_up = True
                all_lo = True
                j = mt.begin_char
                while j <= mt.end_char: 
                    if (twrch[j].is_upper or twrch[j].is_digit): 
                        all_lo = False
                    else: 
                        all_up = False
                    j += 1
                if (all_up): 
                    mt.char_info.is_all_upper = True
                elif (all_lo): 
                    mt.char_info.is_all_lower = True
                elif (((ui0.is_upper or twrch[mt.begin_char].is_digit)) and mt.end_char > mt.begin_char): 
                    all_lo = True
                    j = (mt.begin_char + 1)
                    while j <= mt.end_char: 
                        if (twrch[j].is_upper or twrch[j].is_digit): 
                            all_lo = False
                            break
                        j += 1
                    if (all_lo): 
                        mt.char_info.is_capital_upper = True
                    elif (twrch[mt.end_char].is_lower and (mt.end_char - mt.begin_char) > 1): 
                        all_up = True
                        j = mt.begin_char
                        while j < mt.end_char: 
                            if (twrch[j].is_lower): 
                                all_up = False
                                break
                            j += 1
                        if (all_up): 
                            mt.char_info.is_last_lower = True
            if (mt.char_info.is_last_lower and mt.length > 2 and mt.char_info.is_cyrillic_letter): 
                pref = text[mt.begin_char:mt.begin_char+mt.end_char - mt.begin_char]
                ok = False
                for wf in mt.word_forms: 
                    if (wf.normal_case == pref or wf.normal_full == pref): 
                        ok = True
                        break
                if (not ok): 
                    wf0 = MorphWordForm._new5(pref, MorphClass.NOUN, 1)
                    mt.word_forms = list(mt.word_forms)
                    mt.word_forms.insert(0, wf0)
        if (good_text or only_tokenizing): 
            return res
        i = 0
        first_pass3474 = True
        while True:
            if first_pass3474: first_pass3474 = False
            else: i += 1
            if (not (i < len(res))): break
            if (res[i].length == 1 and res[i].char_info.is_latin_letter): 
                ch = res[i].term[0]
                if (ch == 'C' or ch == 'A' or ch == 'P'): 
                    pass
                else: 
                    continue
                is_rus = False
                for ii in range(i - 1, -1, -1):
                    if ((res[ii].end_char + 1) != res[ii + 1].begin_char): 
                        break
                    elif (res[ii].char_info.is_letter): 
                        is_rus = res[ii].char_info.is_cyrillic_letter
                        break
                if (not is_rus): 
                    ii = i + 1
                    while ii < len(res): 
                        if ((res[ii - 1].end_char + 1) != res[ii].begin_char): 
                            break
                        elif (res[ii].char_info.is_letter): 
                            is_rus = res[ii].char_info.is_cyrillic_letter
                            break
                        ii += 1
                if (is_rus): 
                    res[i].term = LanguageHelper.transliteral_correction(res[i].term, None, True)
                    res[i].char_info.is_cyrillic_letter = True
                    res[i].char_info.is_latin_letter = True
        for r in res: 
            if (r.char_info.is_all_upper or r.char_info.is_capital_upper): 
                if (r.language.is_cyrillic): 
                    ok = False
                    for wf in r.word_forms: 
                        if (wf.class0_.is_proper_surname): 
                            ok = True
                            break
                    if (not ok): 
                        r.word_forms = list(r.word_forms)
                        self.__m_engine_ru.process_surname_variants(r.term, r.word_forms)
        for r in res: 
            for mv in r.word_forms: 
                if (mv.normal_case is None): 
                    mv.normal_case = r.term
        i = 0
        while i < (len(res) - 2): 
            if (res[i].char_info.is_latin_letter and res[i].char_info.is_all_upper and res[i].length == 1): 
                if (twrch[res[i + 1].begin_char].is_quot and res[i + 2].char_info.is_latin_letter and res[i + 2].length > 2): 
                    if ((res[i].end_char + 1) == res[i + 1].begin_char and (res[i + 1].end_char + 1) == res[i + 2].begin_char): 
                        wstr = "{0}{1}".format(res[i].term, res[i + 2].term)
                        li = self.__process_one_word0(wstr)
                        if (li is not None): 
                            res[i].word_forms = li
                        res[i].end_char = res[i + 2].end_char
                        res[i].term = wstr
                        if (res[i + 2].char_info.is_all_lower): 
                            res[i].char_info.is_all_upper = False
                            res[i].char_info.is_capital_upper = True
                        elif (not res[i + 2].char_info.is_all_upper): 
                            res[i].char_info.is_all_upper = False
                        del res[i + 1:i + 1+2]
            i += 1
        i = 0
        first_pass3475 = True
        while True:
            if first_pass3475: first_pass3475 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (not res[i].char_info.is_letter and not res[i + 1].char_info.is_letter and (res[i].end_char + 1) == res[i + 1].begin_char): 
                if (twrch[res[i].begin_char].is_hiphen and twrch[res[i + 1].begin_char].is_hiphen): 
                    if (i == 0 or not twrch[res[i - 1].begin_char].is_hiphen): 
                        pass
                    else: 
                        continue
                    if ((i + 2) == len(res) or not twrch[res[i + 2].begin_char].is_hiphen): 
                        pass
                    else: 
                        continue
                    res[i].end_char = res[i + 1].end_char
                    del res[i + 1]
        return res
    
    def _get_char_typ(self, ui : 'UnicodeInfo') -> int:
        if (ui.is_letter): 
            return 1
        if (ui.is_digit): 
            return 2
        if (ui.is_whitespace): 
            return 0
        if (ui.is_udaren): 
            return 1
        return ui.code
    
    def get_all_wordforms(self, word : str, lang : 'MorphLang') -> typing.List['MorphWordForm']:
        if (LanguageHelper.is_cyrillic_char(word[0])): 
            if (lang is not None): 
                if (self.__m_engine_ru.language.is_ru and lang.is_ru): 
                    return self.__m_engine_ru.get_all_wordforms(word)
                if (self.__m_engine_ua.language.is_ua and lang.is_ua): 
                    return self.__m_engine_ua.get_all_wordforms(word)
                if (self.__m_engine_by.language.is_by and lang.is_by): 
                    return self.__m_engine_by.get_all_wordforms(word)
                if (self.__m_engine_kz.language.is_kz and lang.is_kz): 
                    return self.__m_engine_kz.get_all_wordforms(word)
            return self.__m_engine_ru.get_all_wordforms(word)
        else: 
            return self.__m_engine_en.get_all_wordforms(word)
    
    def get_wordform(self, word : str, cla : 'MorphClass', gender : 'MorphGender', cas : 'MorphCase', num : 'MorphNumber', lang : 'MorphLang', add_info : 'MorphWordForm') -> str:
        if (LanguageHelper.is_cyrillic_char(word[0])): 
            if (self.__m_engine_ru.language.is_ru and lang.is_ru): 
                return self.__m_engine_ru.get_wordform(word, cla, gender, cas, num, add_info)
            if (self.__m_engine_ua.language.is_ua and lang.is_ua): 
                return self.__m_engine_ua.get_wordform(word, cla, gender, cas, num, add_info)
            if (self.__m_engine_by.language.is_by and lang.is_by): 
                return self.__m_engine_by.get_wordform(word, cla, gender, cas, num, add_info)
            if (self.__m_engine_kz.language.is_kz and lang.is_kz): 
                return self.__m_engine_kz.get_wordform(word, cla, gender, cas, num, add_info)
            return self.__m_engine_ru.get_wordform(word, cla, gender, cas, num, add_info)
        else: 
            return self.__m_engine_en.get_wordform(word, cla, gender, cas, num, add_info)
    
    def correct_word_by_morph(self, word : str, lang : 'MorphLang') -> str:
        if (LanguageHelper.is_cyrillic_char(word[0])): 
            if (lang is not None): 
                if (self.__m_engine_ru.language.is_ru and lang.is_ru): 
                    return self.__m_engine_ru.correct_word_by_morph(word)
                if (self.__m_engine_ua.language.is_ua and lang.is_ua): 
                    return self.__m_engine_ua.correct_word_by_morph(word)
                if (self.__m_engine_by.language.is_by and lang.is_by): 
                    return self.__m_engine_by.correct_word_by_morph(word)
                if (self.__m_engine_kz.language.is_kz and lang.is_kz): 
                    return self.__m_engine_kz.correct_word_by_morph(word)
            return self.__m_engine_ru.correct_word_by_morph(word)
        else: 
            return self.__m_engine_en.correct_word_by_morph(word)
    
    def __process_one_word0(self, wstr : str) -> typing.List['MorphWordForm']:
        dl = MorphLang()
        wrapdl6 = RefOutArgWrapper(dl)
        inoutres7 = self.__process_one_word(wstr, wrapdl6)
        dl = wrapdl6.value
        return inoutres7
    
    def __process_one_word(self, wstr : str, def_lang : 'MorphLang') -> typing.List['MorphWordForm']:
        lang = LanguageHelper._get_word_lang(wstr)
        if (lang == MorphLang.UNKNOWN): 
            def_lang.value = MorphLang()
            return None
        if (lang == MorphLang.EN): 
            return self.__m_engine_en.process(wstr)
        if (def_lang.value == MorphLang.RU): 
            if (lang.is_ru): 
                return self.__m_engine_ru.process(wstr)
        if (lang == MorphLang.RU): 
            def_lang.value = lang
            return self.__m_engine_ru.process(wstr)
        if (def_lang.value == MorphLang.UA): 
            if (lang.is_ua): 
                return self.__m_engine_ua.process(wstr)
        if (lang == MorphLang.UA): 
            def_lang.value = lang
            return self.__m_engine_ua.process(wstr)
        if (def_lang.value == MorphLang.BY): 
            if (lang.is_by): 
                return self.__m_engine_by.process(wstr)
        if (lang == MorphLang.BY): 
            def_lang.value = lang
            return self.__m_engine_by.process(wstr)
        if (def_lang.value == MorphLang.KZ): 
            if (lang.is_kz): 
                return self.__m_engine_kz.process(wstr)
        if (lang == MorphLang.KZ): 
            def_lang.value = lang
            return self.__m_engine_kz.process(wstr)
        ru = None
        if (lang.is_ru): 
            ru = self.__m_engine_ru.process(wstr)
        ua = None
        if (lang.is_ua): 
            ua = self.__m_engine_ua.process(wstr)
        by = None
        if (lang.is_by): 
            by = self.__m_engine_by.process(wstr)
        kz = None
        if (lang.is_kz): 
            kz = self.__m_engine_kz.process(wstr)
        has_ru = False
        has_ua = False
        has_by = False
        has_kz = False
        if (ru is not None): 
            for wf in ru: 
                if (wf.is_in_dictionary): 
                    has_ru = True
        if (ua is not None): 
            for wf in ua: 
                if (wf.is_in_dictionary): 
                    has_ua = True
        if (by is not None): 
            for wf in by: 
                if (wf.is_in_dictionary): 
                    has_by = True
        if (kz is not None): 
            for wf in kz: 
                if (wf.is_in_dictionary): 
                    has_kz = True
        if ((has_ru and not has_ua and not has_by) and not has_kz): 
            def_lang.value = MorphLang.RU
            return ru
        if ((has_ua and not has_ru and not has_by) and not has_kz): 
            def_lang.value = MorphLang.UA
            return ua
        if ((has_by and not has_ru and not has_ua) and not has_kz): 
            def_lang.value = MorphLang.BY
            return by
        if ((has_kz and not has_ru and not has_ua) and not has_by): 
            def_lang.value = MorphLang.KZ
            return kz
        if ((ru is None and ua is None and by is None) and kz is None): 
            return None
        if ((ru is not None and ua is None and by is None) and kz is None): 
            return ru
        if ((ua is not None and ru is None and by is None) and kz is None): 
            return ua
        if ((by is not None and ru is None and ua is None) and kz is None): 
            return by
        if ((kz is not None and ru is None and ua is None) and by is None): 
            return kz
        res = list()
        if (ru is not None): 
            lang |= MorphLang.RU
            res.extend(ru)
        if (ua is not None): 
            lang |= MorphLang.UA
            res.extend(ua)
        if (by is not None): 
            lang |= MorphLang.BY
            res.extend(by)
        if (kz is not None): 
            lang |= MorphLang.KZ
            res.extend(kz)
        return res