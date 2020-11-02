# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphMood import MorphMood
from pullenti.morph.MorphVoice import MorphVoice
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphForm import MorphForm
from pullenti.morph.MorphFinite import MorphFinite
from pullenti.morph.MorphAspect import MorphAspect
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.internal.UnicodeInfo import UnicodeInfo
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphPerson import MorphPerson
from pullenti.morph.MorphTense import MorphTense

class LanguageHelper:
    # Служба подержки языков.
    # В качестве универсальных идентификаторов языков выступает 2-х символьный идентификатор ISO 639-1.
    # Также содержит некоторые полезные функции.
    
    @staticmethod
    def get_language_for_text(text : str) -> str:
        """ Определить язык для неструктурированного ткста
        
        Args:
            text(str): текст
        
        Returns:
            str: код языка или null при ненахождении
        """
        if (Utils.isNullOrEmpty(text)): 
            return None
        ru_chars = 0
        en_chars = 0
        i = 0
        first_pass3482 = True
        while True:
            if first_pass3482: first_pass3482 = False
            else: i += 1
            if (not (i < len(text))): break
            ch = text[i]
            if (not str.isalpha(ch)): 
                continue
            j = (ord(ch))
            if (j >= 0x400 and (j < 0x500)): 
                ru_chars += 1
            elif (j < 0x80): 
                en_chars += 1
        if (((ru_chars > (en_chars * 2))) and ru_chars > 10): 
            return "ru"
        if (ru_chars > 0 and en_chars == 0): 
            return "ru"
        if (en_chars > 0): 
            return "en"
        return None
    
    @staticmethod
    def _get_word_lang(word : str) -> 'MorphLang':
        """ Определение языка для одного слова
        
        Args:
            word(str): слово (в верхнем регистре)
        
        """
        cyr = 0
        lat = 0
        undef = 0
        for ch in word: 
            ui = UnicodeInfo.ALL_CHARS[ord(ch)]
            if (ui.is_letter): 
                if (ui.is_cyrillic): 
                    cyr += 1
                elif (ui.is_latin): 
                    lat += 1
                else: 
                    undef += 1
        if (undef > 0): 
            return MorphLang.UNKNOWN
        if (cyr == 0 and lat == 0): 
            return MorphLang.UNKNOWN
        if (cyr == 0): 
            return MorphLang.EN
        if (lat > 0): 
            return MorphLang.UNKNOWN
        lang = ((MorphLang.UA) | MorphLang.RU | MorphLang.BY) | MorphLang.KZ
        for ch in word: 
            ui = UnicodeInfo.ALL_CHARS[ord(ch)]
            if (ui.is_letter): 
                if (ch == 'Ґ' or ch == 'Є' or ch == 'Ї'): 
                    lang.is_ru = False
                    lang.is_by = False
                elif (ch == 'І'): 
                    lang.is_ru = False
                elif (ch == 'Ё' or ch == 'Э'): 
                    lang.is_ua = False
                    lang.is_kz = False
                elif (ch == 'Ы'): 
                    lang.is_ua = False
                elif (ch == 'Ў'): 
                    lang.is_ru = False
                    lang.is_ua = False
                elif (ch == 'Щ'): 
                    lang.is_by = False
                elif (ch == 'Ъ'): 
                    lang.is_by = False
                    lang.is_ua = False
                    lang.is_kz = False
                elif ((((ch == 'Ә' or ch == 'Ғ' or ch == 'Қ') or ch == 'Ң' or ch == 'Ө') or ((ch == 'Ұ' and len(word) > 1)) or ch == 'Ү') or ch == 'Һ'): 
                    lang.is_by = False
                    lang.is_ua = False
                    lang.is_ru = False
                elif ((ch == 'В' or ch == 'Ф' or ch == 'Ц') or ch == 'Ч' or ch == 'Ь'): 
                    lang.is_kz = False
        return lang
    
    @staticmethod
    def is_latin_char(ch : 'char') -> bool:
        ui = UnicodeInfo.ALL_CHARS[ord(ch)]
        return ui.is_latin
    
    @staticmethod
    def is_latin(str0_ : str) -> bool:
        if (str0_ is None): 
            return False
        i = 0
        while i < len(str0_): 
            if (not LanguageHelper.is_latin_char(str0_[i])): 
                if (not Utils.isWhitespace(str0_[i]) and str0_[i] != '-'): 
                    return False
            i += 1
        return True
    
    @staticmethod
    def is_cyrillic_char(ch : 'char') -> bool:
        ui = UnicodeInfo.ALL_CHARS[ord(ch)]
        return ui.is_cyrillic
    
    @staticmethod
    def is_cyrillic(str0_ : str) -> bool:
        if (str0_ is None): 
            return False
        i = 0
        while i < len(str0_): 
            if (not LanguageHelper.is_cyrillic_char(str0_[i])): 
                if (not Utils.isWhitespace(str0_[i]) and str0_[i] != '-'): 
                    return False
            i += 1
        return True
    
    @staticmethod
    def is_hiphen(ch : 'char') -> bool:
        ui = UnicodeInfo.ALL_CHARS[ord(ch)]
        return ui.is_hiphen
    
    @staticmethod
    def is_cyrillic_vowel(ch : 'char') -> bool:
        """ Проверка, что это гласная на кириллице
        
        Args:
            ch('char'): 
        
        """
        ui = UnicodeInfo.ALL_CHARS[ord(ch)]
        return ui.is_cyrillic and ui.is_vowel
    
    @staticmethod
    def is_latin_vowel(ch : 'char') -> bool:
        """ Проверка, что это гласная на латинице
        
        Args:
            ch('char'): 
        
        """
        ui = UnicodeInfo.ALL_CHARS[ord(ch)]
        return ui.is_latin and ui.is_vowel
    
    @staticmethod
    def get_cyr_for_lat(lat : 'char') -> 'char':
        """ Получить для латинской буквы её возможный графический эквивалент на кириллице
        (для тексто-графических замен)
        
        Args:
            lat('char'): 
        
        Returns:
            'char': 0 - нет эквивалента
        """
        i = LanguageHelper._m_lat_chars.find(lat)
        if (i >= 0 and (i < len(LanguageHelper._m_cyr_chars))): 
            return LanguageHelper._m_cyr_chars[i]
        i = LanguageHelper._m_greek_chars.find(lat)
        if (i >= 0 and (i < len(LanguageHelper._m_cyr_greek_chars))): 
            return LanguageHelper._m_cyr_greek_chars[i]
        return chr(0)
    
    @staticmethod
    def get_lat_for_cyr(cyr : 'char') -> 'char':
        """ Получить для кириллической буквы её возможный графический эквивалент на латинице
        (для тексто-графических замен)
        
        Args:
            lat: 
        
        Returns:
            'char': 0 - нет эквивалента
        """
        i = LanguageHelper._m_cyr_chars.find(cyr)
        if ((i < 0) or i >= len(LanguageHelper._m_lat_chars)): 
            return chr(0)
        else: 
            return LanguageHelper._m_lat_chars[i]
    
    @staticmethod
    def transliteral_correction(value : str, prev_value : str, always : bool=False) -> str:
        """ Транслитеральная корректировка
        
        Args:
            value(str): 
            prev_value(str): 
            always(bool): 
        
        """
        pure_cyr = 0
        pure_lat = 0
        ques_cyr = 0
        ques_lat = 0
        udar_cyr = 0
        y = False
        udaren = False
        i = 0
        first_pass3483 = True
        while True:
            if first_pass3483: first_pass3483 = False
            else: i += 1
            if (not (i < len(value))): break
            ch = value[i]
            ui = UnicodeInfo.ALL_CHARS[ord(ch)]
            if (not ui.is_letter): 
                if (ui.is_udaren): 
                    udaren = True
                    continue
                if (ui.is_apos and len(value) > 2): 
                    return LanguageHelper.transliteral_correction(value.replace("{0}".format(ch), ""), prev_value, False)
                return value
            if (ui.is_cyrillic): 
                if (LanguageHelper._m_cyr_chars.find(ch) >= 0): 
                    ques_cyr += 1
                else: 
                    pure_cyr += 1
            elif (ui.is_latin): 
                if (LanguageHelper._m_lat_chars.find(ch) >= 0): 
                    ques_lat += 1
                else: 
                    pure_lat += 1
            elif (LanguageHelper.__m_udar_chars.find(ch) >= 0): 
                udar_cyr += 1
            else: 
                return value
            if (ch == 'Ь' and ((i + 1) < len(value)) and value[i + 1] == 'I'): 
                y = True
        to_rus = False
        to_lat = False
        if (pure_lat > 0 and pure_cyr > 0): 
            return value
        if (((pure_lat > 0 or always)) and ques_cyr > 0): 
            to_lat = True
        elif (((pure_cyr > 0 or always)) and ques_lat > 0): 
            to_rus = True
        elif (pure_cyr == 0 and pure_lat == 0): 
            if (ques_cyr > 0 and ques_lat > 0): 
                if (not Utils.isNullOrEmpty(prev_value)): 
                    if (LanguageHelper.is_cyrillic_char(prev_value[0])): 
                        to_rus = True
                    elif (LanguageHelper.is_latin_char(prev_value[0])): 
                        to_lat = True
                if (not to_lat and not to_rus): 
                    if (ques_cyr > ques_lat): 
                        to_rus = True
                    elif (ques_cyr < ques_lat): 
                        to_lat = True
        if (not to_rus and not to_lat): 
            if (not y and not udaren and udar_cyr == 0): 
                return value
        tmp = Utils.newStringIO(value)
        i = 0
        first_pass3484 = True
        while True:
            if first_pass3484: first_pass3484 = False
            else: i += 1
            if (not (i < tmp.tell())): break
            if (Utils.getCharAtStringIO(tmp, i) == 'Ь' and ((i + 1) < tmp.tell()) and Utils.getCharAtStringIO(tmp, i + 1) == 'I'): 
                Utils.setCharAtStringIO(tmp, i, 'Ы')
                Utils.removeStringIO(tmp, i + 1, 1)
                continue
            cod = ord(Utils.getCharAtStringIO(tmp, i))
            if (cod >= 0x300 and (cod < 0x370)): 
                Utils.removeStringIO(tmp, i, 1)
                continue
            if (to_rus): 
                ii = LanguageHelper._m_lat_chars.find(Utils.getCharAtStringIO(tmp, i))
                if (ii >= 0): 
                    Utils.setCharAtStringIO(tmp, i, LanguageHelper._m_cyr_chars[ii])
                else: 
                    ii = LanguageHelper.__m_udar_chars.find(Utils.getCharAtStringIO(tmp, i))
                    if (((ii)) >= 0): 
                        Utils.setCharAtStringIO(tmp, i, LanguageHelper.__m_udar_cyr_chars[ii])
            elif (to_lat): 
                ii = LanguageHelper._m_cyr_chars.find(Utils.getCharAtStringIO(tmp, i))
                if (ii >= 0): 
                    Utils.setCharAtStringIO(tmp, i, LanguageHelper._m_lat_chars[ii])
            else: 
                ii = LanguageHelper.__m_udar_chars.find(Utils.getCharAtStringIO(tmp, i))
                if (ii >= 0): 
                    Utils.setCharAtStringIO(tmp, i, LanguageHelper.__m_udar_cyr_chars[ii])
        return Utils.toStringStringIO(tmp)
    
    _m_lat_chars = "ABEKMHOPCTYXIaekmopctyxi"
    
    _m_cyr_chars = "АВЕКМНОРСТУХІаекморстухі"
    
    _m_greek_chars = "ΑΒΓΕΗΙΚΛΜΟΠΡΤΥΦΧ"
    
    _m_cyr_greek_chars = "АВГЕНІКЛМОПРТУФХ"
    
    __m_udar_chars = "ÀÁÈÉËÒÓàáèéëýÝòóЀѐЍѝỲỳ"
    
    __m_udar_cyr_chars = "ААЕЕЕООааеееуУооЕеИиУу"
    
    @staticmethod
    def is_quote(ch : 'char') -> bool:
        ui = UnicodeInfo.ALL_CHARS[ord(ch)]
        return ui.is_quot
    
    @staticmethod
    def is_apos(ch : 'char') -> bool:
        ui = UnicodeInfo.ALL_CHARS[ord(ch)]
        return ui.is_apos
    
    __m_preps = None
    
    __m_cases = None
    
    __m_prep_cases = None
    
    @staticmethod
    def get_case_after_preposition(prep : str) -> 'MorphCase':
        """ Получить возможные падежи существительных после предлогов
        
        Args:
            prep(str): предлог
        
        """
        wrapmc25 = RefOutArgWrapper(None)
        inoutres26 = Utils.tryGetValue(LanguageHelper.__m_prep_cases, prep, wrapmc25)
        mc = wrapmc25.value
        if (inoutres26): 
            return mc
        else: 
            return MorphCase.UNDEFINED
    
    __m_prep_norms_src = None
    
    __m_prep_norms = None
    
    @staticmethod
    def normalize_preposition(prep : str) -> str:
        wrapres27 = RefOutArgWrapper(None)
        inoutres28 = Utils.tryGetValue(LanguageHelper.__m_prep_norms, prep, wrapres27)
        res = wrapres27.value
        if (inoutres28): 
            return res
        else: 
            return prep
    
    @staticmethod
    def ends_with(str0_ : str, substr : str) -> bool:
        """ Замена стандартной функции string.EndsWith, которая относительно медленная
        
        Args:
            str0_(str): 
            substr(str): 
        
        """
        if (str0_ is None or substr is None): 
            return False
        i = len(str0_) - 1
        j = len(substr) - 1
        if (j > i or (j < 0)): 
            return False
        while j >= 0: 
            if (str0_[i] != substr[j]): 
                return False
            j -= 1; i -= 1
        return True
    
    @staticmethod
    def ends_with_ex(str0_ : str, substr : str, substr2 : str, substr3 : str=None, substr4 : str=None) -> bool:
        """ Проверка окончания строки на одну из заданных подстрок
        
        Args:
            str0_(str): 
            substr(str): 
            substr2(str): 
            substr3(str): 
            substr4(str): 
        
        """
        if (str0_ is None): 
            return False
        for k in range(4):
            s = substr
            if (k == 1): 
                s = substr2
            elif (k == 2): 
                s = substr3
            elif (k == 3): 
                s = substr4
            if (s is None): 
                continue
            i = len(str0_) - 1
            j = len(s) - 1
            if (j > i or (j < 0)): 
                continue
            while j >= 0: 
                if (str0_[i] != s[j]): 
                    break
                j -= 1; i -= 1
            if (j < 0): 
                return True
        return False
    
    @staticmethod
    def to_string_morph_tense(tense : 'MorphTense') -> str:
        res = io.StringIO()
        if (((tense) & (MorphTense.PAST)) != (MorphTense.UNDEFINED)): 
            print("прошедшее|", end="", file=res)
        if (((tense) & (MorphTense.PRESENT)) != (MorphTense.UNDEFINED)): 
            print("настоящее|", end="", file=res)
        if (((tense) & (MorphTense.FUTURE)) != (MorphTense.UNDEFINED)): 
            print("будущее|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_person(person : 'MorphPerson') -> str:
        res = io.StringIO()
        if (((person) & (MorphPerson.FIRST)) != (MorphPerson.UNDEFINED)): 
            print("1лицо|", end="", file=res)
        if (((person) & (MorphPerson.SECOND)) != (MorphPerson.UNDEFINED)): 
            print("2лицо|", end="", file=res)
        if (((person) & (MorphPerson.THIRD)) != (MorphPerson.UNDEFINED)): 
            print("3лицо|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_gender(gender : 'MorphGender') -> str:
        res = io.StringIO()
        if (((gender) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
            print("муж.|", end="", file=res)
        if (((gender) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
            print("жен.|", end="", file=res)
        if (((gender) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
            print("средн.|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_number(number : 'MorphNumber') -> str:
        res = io.StringIO()
        if (((number) & (MorphNumber.SINGULAR)) != (MorphNumber.UNDEFINED)): 
            print("единств.|", end="", file=res)
        if (((number) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
            print("множеств.|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_voice(voice : 'MorphVoice') -> str:
        res = io.StringIO()
        if (((voice) & (MorphVoice.ACTIVE)) != (MorphVoice.UNDEFINED)): 
            print("действит.|", end="", file=res)
        if (((voice) & (MorphVoice.PASSIVE)) != (MorphVoice.UNDEFINED)): 
            print("страдат.|", end="", file=res)
        if (((voice) & (MorphVoice.MIDDLE)) != (MorphVoice.UNDEFINED)): 
            print("средн.|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_mood(mood : 'MorphMood') -> str:
        res = io.StringIO()
        if (((mood) & (MorphMood.INDICATIVE)) != (MorphMood.UNDEFINED)): 
            print("изъявит.|", end="", file=res)
        if (((mood) & (MorphMood.IMPERATIVE)) != (MorphMood.UNDEFINED)): 
            print("повелит.|", end="", file=res)
        if (((mood) & (MorphMood.SUBJUNCTIVE)) != (MorphMood.UNDEFINED)): 
            print("условн.|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_aspect(aspect : 'MorphAspect') -> str:
        res = io.StringIO()
        if (((aspect) & (MorphAspect.IMPERFECTIVE)) != (MorphAspect.UNDEFINED)): 
            print("несоверш.|", end="", file=res)
        if (((aspect) & (MorphAspect.PERFECTIVE)) != (MorphAspect.UNDEFINED)): 
            print("соверш.|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_finite(finit : 'MorphFinite') -> str:
        res = io.StringIO()
        if (((finit) & (MorphFinite.FINITE)) != (MorphFinite.UNDEFINED)): 
            print("finite|", end="", file=res)
        if (((finit) & (MorphFinite.GERUND)) != (MorphFinite.UNDEFINED)): 
            print("gerund|", end="", file=res)
        if (((finit) & (MorphFinite.INFINITIVE)) != (MorphFinite.UNDEFINED)): 
            print("инфинитив|", end="", file=res)
        if (((finit) & (MorphFinite.PARTICIPLE)) != (MorphFinite.UNDEFINED)): 
            print("participle|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_form(form : 'MorphForm') -> str:
        res = io.StringIO()
        if (((form) & (MorphForm.SHORT)) != (MorphForm.UNDEFINED)): 
            print("кратк.|", end="", file=res)
        if (((form) & (MorphForm.SYNONYM)) != (MorphForm.UNDEFINED)): 
            print("синонимич.|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    __m_rus0 = "–ЁѐЀЍѝЎўӢӣ"
    
    __m_rus1 = "-ЕЕЕИИУУЙЙ"
    
    @staticmethod
    def correct_word(w : str) -> str:
        """ Откорректировать слово (перевод в верхний регистр и замена некоторых букв типа Ё->Е)
        
        Args:
            w(str): исходное слово
        
        Returns:
            str: откорректированное слово
        """
        if (w is None): 
            return None
        res = w.upper()
        for ch in res: 
            if (LanguageHelper.__m_rus0.find(ch) >= 0): 
                tmp = io.StringIO()
                print(res, end="", file=tmp)
                i = 0
                while i < tmp.tell(): 
                    j = LanguageHelper.__m_rus0.find(Utils.getCharAtStringIO(tmp, i))
                    if (j >= 0): 
                        Utils.setCharAtStringIO(tmp, i, LanguageHelper.__m_rus1[j])
                    i += 1
                res = Utils.toStringStringIO(tmp)
                break
        if (res.find(chr(0x00AD)) >= 0): 
            res = res.replace(chr(0x00AD), '-')
        if (res.startswith("АГЕНС")): 
            res = ("АГЕНТС" + res[5:])
        return res
    
    # static constructor for class LanguageHelper
    @staticmethod
    def _static_ctor():
        LanguageHelper.__m_preps = [("БЕЗ;ДО;ИЗ;ИЗЗА;ОТ;У;ДЛЯ;РАДИ;ВОЗЛЕ;ПОЗАДИ;ВПЕРЕДИ;БЛИЗ;ВБЛИЗИ;ВГЛУБЬ;ВВИДУ;ВДОЛЬ;ВЗАМЕН;ВКРУГ;ВМЕСТО;" + "ВНЕ;ВНИЗУ;ВНУТРИ;ВНУТРЬ;ВОКРУГ;ВРОДЕ;ВСЛЕД;ВСЛЕДСТВИЕ;ЗАМЕСТО;ИЗНУТРИ;КАСАТЕЛЬНО;КРОМЕ;" + "МИМО;НАВРОДЕ;НАЗАД;НАКАНУНЕ;НАПОДОБИЕ;НАПРОТИВ;НАСЧЕТ;ОКОЛО;ОТНОСИТЕЛЬНО;") + "ПОВЕРХ;ПОДЛЕ;ПОМИМО;ПОПЕРЕК;ПОРЯДКА;ПОСЕРЕДИНЕ;ПОСРЕДИ;ПОСЛЕ;ПРЕВЫШЕ;ПРЕЖДЕ;ПРОТИВ;СВЕРХ;" + "СВЫШЕ;СНАРУЖИ;СРЕДИ;СУПРОТИВ;ПУТЕМ;ПОСРЕДСТВОМ", "К;БЛАГОДАРЯ;ВОПРЕКИ;НАВСТРЕЧУ;СОГЛАСНО;СООБРАЗНО;ПАРАЛЛЕЛЬНО;ПОДОБНО;СООТВЕТСТВЕННО;СОРАЗМЕРНО", "ПРО;ЧЕРЕЗ;СКВОЗЬ;СПУСТЯ", "НАД;ПЕРЕД;ПРЕД", "ПРИ", "В;НА;О;ВКЛЮЧАЯ", "МЕЖДУ", "ЗА;ПОД", "ПО", "С"]
        LanguageHelper.__m_cases = [MorphCase.GENITIVE, MorphCase.DATIVE, MorphCase.ACCUSATIVE, MorphCase.INSTRUMENTAL, MorphCase.PREPOSITIONAL, (MorphCase.ACCUSATIVE) | MorphCase.PREPOSITIONAL, (MorphCase.GENITIVE) | MorphCase.INSTRUMENTAL, (MorphCase.ACCUSATIVE) | MorphCase.INSTRUMENTAL, (MorphCase.DATIVE) | MorphCase.ACCUSATIVE | MorphCase.PREPOSITIONAL, (MorphCase.GENITIVE) | MorphCase.ACCUSATIVE | MorphCase.INSTRUMENTAL]
        LanguageHelper.__m_prep_norms_src = ["БЕЗ;БЕЗО", "ВБЛИЗИ;БЛИЗ", "В;ВО", "ВОКРУГ;ВКРУГ", "ВНУТРИ;ВНУТРЬ;ВОВНУТРЬ", "ВПЕРЕДИ;ВПЕРЕД", "ВСЛЕД;ВОСЛЕД", "ВМЕСТО;ЗАМЕСТО", "ИЗ;ИЗО", "К;КО", "МЕЖДУ;МЕЖ;ПРОМЕЖДУ;ПРОМЕЖ", "НАД;НАДО", "О;ОБ;ОБО", "ОТ;ОТО", "ПЕРЕД;ПРЕД;ПРЕДО;ПЕРЕДО", "ПОД;ПОДО", "ПОСЕРЕДИНЕ;ПОСРЕДИ;ПОСЕРЕДЬ", "С;СО", "СРЕДИ;СРЕДЬ;СЕРЕДЬ", "ЧЕРЕЗ;ЧРЕЗ"]
        LanguageHelper.__m_prep_cases = dict()
        i = 0
        while i < len(LanguageHelper.__m_preps): 
            for v in Utils.splitString(LanguageHelper.__m_preps[i], ';', False): 
                LanguageHelper.__m_prep_cases[v] = LanguageHelper.__m_cases[i]
            i += 1
        LanguageHelper.__m_prep_norms = dict()
        for s in LanguageHelper.__m_prep_norms_src: 
            vars0_ = Utils.splitString(s, ';', False)
            i = 1
            while i < len(vars0_): 
                LanguageHelper.__m_prep_norms[vars0_[i]] = vars0_[0]
                i += 1

LanguageHelper._static_ctor()