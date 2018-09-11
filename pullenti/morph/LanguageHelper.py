# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.morph.internal.UnicodeInfo import UnicodeInfo
from pullenti.morph.MorphTense import MorphTense
from pullenti.morph.MorphPerson import MorphPerson
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphVoice import MorphVoice
from pullenti.morph.MorphMood import MorphMood
from pullenti.morph.MorphAspect import MorphAspect
from pullenti.morph.MorphFinite import MorphFinite
from pullenti.morph.MorphForm import MorphForm


class LanguageHelper:
    """ Служба подержки языков. 
     В качестве универсальных идентификаторов языков выступает 2-х символьный идентификатор ISO 639-1.
     Также содержит некоторые полезные функции. """
    
    @staticmethod
    def get_language_for_text(text : str) -> str:
        if (Utils.isNullOrEmpty(text)): 
            return None
        ru_chars = 0
        en_chars = 0
        i = 0
        first_pass3621 = True
        while True:
            if first_pass3621: first_pass3621 = False
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
        ui = UnicodeInfo.ALL_CHARS[ord(ch)]
        return ui.is_cyrillic and ui.is_vowel
    
    @staticmethod
    def is_latin_vowel(ch : 'char') -> bool:
        ui = UnicodeInfo.ALL_CHARS[ord(ch)]
        return ui.is_latin and ui.is_vowel
    
    @staticmethod
    def get_cyr_for_lat(lat : 'char') -> 'char':
        i = LanguageHelper._m_lat_chars.find(lat)
        if (i >= 0 and (i < len(LanguageHelper._m_cyr_chars))): 
            return LanguageHelper._m_cyr_chars[i]
        i = LanguageHelper._m_greek_chars.find(lat)
        if (i >= 0 and (i < len(LanguageHelper._m_cyr_greek_chars))): 
            return LanguageHelper._m_cyr_greek_chars[i]
        return chr(0)
    
    @staticmethod
    def get_lat_for_cyr(cyr : 'char') -> 'char':
        i = LanguageHelper._m_cyr_chars.find(cyr)
        if ((i < 0) or i >= len(LanguageHelper._m_lat_chars)): 
            return chr(0)
        else: 
            return LanguageHelper._m_lat_chars[i]
    
    @staticmethod
    def transliteral_correction(value : str, prev_value : str, always : bool=False) -> str:
        pure_cyr = 0
        pure_lat = 0
        ques_cyr = 0
        ques_lat = 0
        udar_cyr = 0
        y = False
        udaren = False
        i = 0
        first_pass3622 = True
        while True:
            if first_pass3622: first_pass3622 = False
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
        first_pass3623 = True
        while True:
            if first_pass3623: first_pass3623 = False
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
        from pullenti.morph.MorphCase import MorphCase
        inoutarg44 = RefOutArgWrapper(None)
        inoutres45 = Utils.tryGetValue(LanguageHelper.__m_prep_cases, prep, inoutarg44)
        mc = inoutarg44.value
        if (inoutres45): 
            return mc
        else: 
            return MorphCase.UNDEFINED
    
    __m_prep_norms_src = None
    
    __m_prep_norms = None
    
    @staticmethod
    def normalize_preposition(prep : str) -> str:
        inoutarg46 = RefOutArgWrapper(None)
        inoutres47 = Utils.tryGetValue(LanguageHelper.__m_prep_norms, prep, inoutarg46)
        res = inoutarg46.value
        if (inoutres47): 
            return res
        else: 
            return prep
    
    @staticmethod
    def ends_with(str0_ : str, substr : str) -> bool:
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
        if (str0_ is None): 
            return False
        for k in range(4):
            if (k == 1): 
                substr = substr2
            elif (k == 2): 
                substr = substr3
            elif (k == 3): 
                substr = substr4
            if (substr is None): 
                continue
            i = len(str0_) - 1
            j = len(substr) - 1
            if (j > i or (j < 0)): 
                continue
            while j >= 0: 
                if (str0_[i] != substr[j]): 
                    break
                j -= 1; i -= 1
            if (j < 0): 
                return True
        return False
    
    @staticmethod
    def to_string_morph_tense(tense : 'MorphTense') -> str:
        res = io.StringIO()
        if ((((tense) & (MorphTense.PAST))) != (MorphTense.UNDEFINED)): 
            print("прошедшее|", end="", file=res)
        if ((((tense) & (MorphTense.PRESENT))) != (MorphTense.UNDEFINED)): 
            print("настоящее|", end="", file=res)
        if ((((tense) & (MorphTense.FUTURE))) != (MorphTense.UNDEFINED)): 
            print("будущее|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_person(person : 'MorphPerson') -> str:
        res = io.StringIO()
        if ((((person) & (MorphPerson.FIRST))) != (MorphPerson.UNDEFINED)): 
            print("1лицо|", end="", file=res)
        if ((((person) & (MorphPerson.SECOND))) != (MorphPerson.UNDEFINED)): 
            print("2лицо|", end="", file=res)
        if ((((person) & (MorphPerson.THIRD))) != (MorphPerson.UNDEFINED)): 
            print("3лицо|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_gender(gender : 'MorphGender') -> str:
        res = io.StringIO()
        if ((((gender) & (MorphGender.MASCULINE))) != (MorphGender.UNDEFINED)): 
            print("муж.|", end="", file=res)
        if ((((gender) & (MorphGender.FEMINIE))) != (MorphGender.UNDEFINED)): 
            print("жен.|", end="", file=res)
        if ((((gender) & (MorphGender.NEUTER))) != (MorphGender.UNDEFINED)): 
            print("средн.|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_number(number : 'MorphNumber') -> str:
        res = io.StringIO()
        if ((((number) & (MorphNumber.SINGULAR))) != (MorphNumber.UNDEFINED)): 
            print("единств.|", end="", file=res)
        if ((((number) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
            print("множеств.|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_voice(voice : 'MorphVoice') -> str:
        res = io.StringIO()
        if ((((voice) & (MorphVoice.ACTIVE))) != (MorphVoice.UNDEFINED)): 
            print("действит.|", end="", file=res)
        if ((((voice) & (MorphVoice.PASSIVE))) != (MorphVoice.UNDEFINED)): 
            print("страдат.|", end="", file=res)
        if ((((voice) & (MorphVoice.MIDDLE))) != (MorphVoice.UNDEFINED)): 
            print("средн.|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_mood(mood : 'MorphMood') -> str:
        res = io.StringIO()
        if ((((mood) & (MorphMood.INDICATIVE))) != (MorphMood.UNDEFINED)): 
            print("изъявит.|", end="", file=res)
        if ((((mood) & (MorphMood.IMPERATIVE))) != (MorphMood.UNDEFINED)): 
            print("повелит.|", end="", file=res)
        if ((((mood) & (MorphMood.SUBJUNCTIVE))) != (MorphMood.UNDEFINED)): 
            print("условн.|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_aspect(aspect : 'MorphAspect') -> str:
        res = io.StringIO()
        if ((((aspect) & (MorphAspect.IMPERFECTIVE))) != (MorphAspect.UNDEFINED)): 
            print("несоверш.|", end="", file=res)
        if ((((aspect) & (MorphAspect.PERFECTIVE))) != (MorphAspect.UNDEFINED)): 
            print("соверш.|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_finite(finit : 'MorphFinite') -> str:
        res = io.StringIO()
        if ((((finit) & (MorphFinite.FINITE))) != (MorphFinite.UNDEFINED)): 
            print("finite|", end="", file=res)
        if ((((finit) & (MorphFinite.GERUND))) != (MorphFinite.UNDEFINED)): 
            print("gerund|", end="", file=res)
        if ((((finit) & (MorphFinite.INFINITIVE))) != (MorphFinite.UNDEFINED)): 
            print("инфинитив|", end="", file=res)
        if ((((finit) & (MorphFinite.PARTICIPLE))) != (MorphFinite.UNDEFINED)): 
            print("participle|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def to_string_morph_form(form : 'MorphForm') -> str:
        res = io.StringIO()
        if ((((form) & (MorphForm.SHORT))) != (MorphForm.UNDEFINED)): 
            print("кратк.|", end="", file=res)
        if ((((form) & (MorphForm.SYNONYM))) != (MorphForm.UNDEFINED)): 
            print("синонимич.|", end="", file=res)
        if (res.tell() > 0): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    __m_rus0 = "–ЁѐЀЍѝЎўӢӣ"
    
    __m_rus1 = "-ЕЕЕИИУУЙЙ"
    
    @staticmethod
    def correct_word(w : str) -> str:
        if (w is None): 
            return None
        w = w.upper()
        for ch in w: 
            if (LanguageHelper.__m_rus0.find(ch) >= 0): 
                tmp = io.StringIO()
                print(w, end="", file=tmp)
                i = 0
                while i < tmp.tell(): 
                    j = LanguageHelper.__m_rus0.find(Utils.getCharAtStringIO(tmp, i))
                    if (j >= 0): 
                        Utils.setCharAtStringIO(tmp, i, LanguageHelper.__m_rus1[j])
                    i += 1
                w = Utils.toStringStringIO(tmp)
                break
        if (w.find(chr(0x00AD)) >= 0): 
            w = w.replace(chr(0x00AD), '-')
        if (w.startswith("АГЕНС")): 
            w = ("АГЕНТС" + w[5:])
        return w
    
    # static constructor for class LanguageHelper
    @staticmethod
    def _static_ctor():
        from pullenti.morph.MorphCase import MorphCase
        LanguageHelper.__m_preps = [("БЕЗ;ДО;ИЗ;ИЗЗА;ОТ;У;ДЛЯ;РАДИ;ВОЗЛЕ;ПОЗАДИ;ВПЕРЕДИ;БЛИЗ;ВБЛИЗИ;ВГЛУБЬ;ВВИДУ;ВДОЛЬ;ВЗАМЕН;ВКРУГ;ВМЕСТО;" + "ВНЕ;ВНИЗУ;ВНУТРИ;ВНУТРЬ;ВОКРУГ;ВРОДЕ;ВСЛЕД;ВСЛЕДСТВИЕ;ЗАМЕСТО;ИЗНУТРИ;КАСАТЕЛЬНО;КРОМЕ;" + "МИМО;НАВРОДЕ;НАЗАД;НАКАНУНЕ;НАПОДОБИЕ;НАПРОТИВ;НАСЧЕТ;ОКОЛО;ОТНОСИТЕЛЬНО;") + "ПОВЕРХ;ПОДЛЕ;ПОМИМО;ПОПЕРЕК;ПОРЯДКА;ПОСЕРЕДИНЕ;ПОСРЕДИ;ПОСЛЕ;ПРЕВЫШЕ;ПРЕЖДЕ;ПРОТИВ;СВЕРХ;" + "СВЫШЕ;СНАРУЖИ;СРЕДИ;СУПРОТИВ", "К;БЛАГОДАРЯ;ВОПРЕКИ;НАВСТРЕЧУ;СОГЛАСНО;СООБРАЗНО;ПАРАЛЛЕЛЬНО;ПОДОБНО;СООТВЕТСТВЕННО;СОРАЗМЕРНО", "ПРО;ЧЕРЕЗ;СКВОЗЬ;СПУСТЯ", "НАД;ПЕРЕД;ПРЕД", "ПРИ", "В;НА;О;ВКЛЮЧАЯ", "МЕЖДУ", "ЗА;ПОД", "ПО", "С"]
        LanguageHelper.__m_cases = [MorphCase.GENITIVE, MorphCase.DATIVE, MorphCase.ACCUSATIVE, MorphCase.INSTRUMENTAL, MorphCase.PREPOSITIONAL, (MorphCase.ACCUSATIVE) | MorphCase.PREPOSITIONAL, (MorphCase.GENITIVE) | MorphCase.ACCUSATIVE, (MorphCase.ACCUSATIVE) | MorphCase.INSTRUMENTAL, (MorphCase.DATIVE) | MorphCase.ACCUSATIVE | MorphCase.PREPOSITIONAL, (MorphCase.GENITIVE) | MorphCase.ACCUSATIVE | MorphCase.INSTRUMENTAL]
        LanguageHelper.__m_prep_norms_src = ["БЕЗ;БЕЗО", "В;ВО", "ВОКРУГ;ВКРУГ", "ВПЕРЕДИ;ВПЕРЕД", "ВСЛЕД;ВОСЛЕД", "ИЗ;ИЗО", "К;КО", "МЕЖДУ;МЕЖ", "НАД;НАДО", "О;ОБ;ОБО", "ОТ;ОТО", "ПЕРЕД;ПРЕД;ПРЕДО;ПЕРЕДО", "ПОД;ПОДО", "ПОСЕРЕДИНЕ;ПОСРЕДИ", "ПРОМЕЖДУ;ПРОМЕЖ", "С;СО", "СРЕДИ;СРЕДЬ", "ЧЕРЕЗ;ЧРЕЗ"]
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