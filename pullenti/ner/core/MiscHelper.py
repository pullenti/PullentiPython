# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
import unicodedata
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.core.internal.RusLatAccord import RusLatAccord
from pullenti.morph.Morphology import Morphology
from pullenti.ner.Token import Token
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.CanBeEqualsAttrs import CanBeEqualsAttrs
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.TextToken import TextToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.core.AnalysisKit import AnalysisKit

class MiscHelper:
    """ Разные полезные процедурки """
    
    class CyrLatWord:
        
        def __init__(self) -> None:
            self.cyr_word = None;
            self.lat_word = None;
        
        def __str__(self) -> str:
            if (self.cyr_word is not None and self.lat_word is not None): 
                return "{0}\\{1}".format(self.cyr_word, self.lat_word)
            elif (self.cyr_word is not None): 
                return self.cyr_word
            else: 
                return Utils.ifNotNull(self.lat_word, "?")
        
        @property
        def length(self) -> int:
            return (len(self.cyr_word) if self.cyr_word is not None else ((len(self.lat_word) if self.lat_word is not None else 0)))
    
    @staticmethod
    def is_not_more_than_one_error(value : str, t : 'Token') -> bool:
        """ Сравнение, чтобы не было больше одной ошибки в написании.
         Ошибка - это замена буквы или пропуск буквы.
        
        Args:
            value(str): правильное написание
            t(Token): проверяемый токен
        
        """
        if (t is None): 
            return False
        if (isinstance(t, TextToken)): 
            tt = Utils.asObjectOrNull(t, TextToken)
            if (t.is_value(value, None)): 
                return True
            if (MiscHelper.__is_not_more_than_one_error(value, tt.term, True)): 
                return True
            for wf in tt.morph.items: 
                if (isinstance(wf, MorphWordForm)): 
                    if (MiscHelper.__is_not_more_than_one_error(value, (wf).normal_case, True)): 
                        return True
        elif ((isinstance(t, MetaToken)) and (t).begin_token == (t).end_token): 
            return MiscHelper.is_not_more_than_one_error(value, (t).begin_token)
        elif (MiscHelper.__is_not_more_than_one_error(value, t.get_normal_case_text(None, False, MorphGender.UNDEFINED, False), True)): 
            return True
        return False
    
    @staticmethod
    def __is_not_more_than_one_error(pattern : str, test : str, tmp : bool=False) -> bool:
        if (test is None or pattern is None): 
            return False
        if (len(test) == len(pattern)): 
            cou = 0
            i = 0
            while i < len(pattern): 
                if (pattern[i] != test[i]): 
                    cou += 1
                    if ((cou) > 1): 
                        return False
                i += 1
            return True
        if (len(test) == (len(pattern) - 1)): 
            i = 0
            while i < len(test): 
                if (pattern[i] != test[i]): 
                    break
                i += 1
            if (i < 2): 
                return False
            if (i == len(test)): 
                return True
            while i < len(test): 
                if (pattern[i + 1] != test[i]): 
                    return False
                i += 1
            return True
        if (not tmp and (len(test) - 1) == len(pattern)): 
            i = 0
            while i < len(pattern): 
                if (pattern[i] != test[i]): 
                    break
                i += 1
            if (i < 2): 
                return False
            if (i == len(pattern)): 
                return True
            while i < len(pattern): 
                if (pattern[i] != test[i + 1]): 
                    return False
                i += 1
            return True
        return False
    
    @staticmethod
    def try_attach_word_by_letters(word : str, t : 'Token', use_morph_variants : bool=False) -> 'Token':
        """ Проверить написание слова вразбивку по буквам (например:   П Р И К А З)
        
        Args:
            word(str): проверяемое слово
            t(Token): начальный токен
            use_morph_variants(bool): перебирать ли падежи у слова
        
        Returns:
            Token: токен последней буквы или null
        """
        t1 = Utils.asObjectOrNull(t, TextToken)
        if (t1 is None): 
            return None
        i = 0
        while t1 is not None: 
            s = t1.term
            j = 0
            while (j < len(s)) and ((i + j) < len(word)): 
                if (word[i + j] != s[j]): 
                    break
                j += 1
            if (j < len(s)): 
                if (not use_morph_variants): 
                    return None
                if (i < 7): 
                    return None
                tmp = io.StringIO()
                print(word[0:0+i], end="", file=tmp)
                tt = t1
                while tt is not None: 
                    if (not ((isinstance(tt, TextToken))) or not tt.chars.is_letter or tt.is_newline_before): 
                        break
                    t1 = (Utils.asObjectOrNull(tt, TextToken))
                    print(t1.term, end="", file=tmp)
                    tt = tt.next0_
                li = Morphology.process(Utils.toStringStringIO(tmp), t.morph.language, None)
                if (li is not None): 
                    for l_ in li: 
                        if (l_.word_forms is not None): 
                            for wf in l_.word_forms: 
                                if (wf.normal_case == word or wf.normal_full == word): 
                                    return t1
                return None
            i += j
            if (i == len(word)): 
                return t1
            t1 = (Utils.asObjectOrNull(t1.next0_, TextToken))
        return None
    
    @staticmethod
    def can_be_equals(s1 : str, s2 : str, ignore_nonletters : bool=True, ignore_case : bool=True, check_morph_equ_after_first_noun : bool=False) -> bool:
        """ Сравнение 2-х строк на предмет равенства с учётом морфологии и пунктуации (то есть инвариантно относительно них).
         Функция довольно трудоёмка, не использовать без крайней необходимости.
         ВНИМАНИЕ! Вместо этой функции теперь используйте CanBeEqualsEx.
        
        Args:
            s1(str): первая строка
            s2(str): вторая строка
            ignore_nonletters(bool): игнорировать небуквенные символы
            ignore_case(bool): игнорировать регистр символов
            check_morph_equ_after_first_noun(bool): после первого существительного слова должны полностью совпадать
        
        """
        attrs = CanBeEqualsAttrs.NO
        if (ignore_nonletters): 
            attrs = (Utils.valToEnum((attrs) | (CanBeEqualsAttrs.IGNORENONLETTERS), CanBeEqualsAttrs))
        if (ignore_case): 
            attrs = (Utils.valToEnum((attrs) | (CanBeEqualsAttrs.IGNOREUPPERCASE), CanBeEqualsAttrs))
        if (check_morph_equ_after_first_noun): 
            attrs = (Utils.valToEnum((attrs) | (CanBeEqualsAttrs.CHECKMORPHEQUAFTERFIRSTNOUN), CanBeEqualsAttrs))
        return MiscHelper.can_be_equals_ex(s1, s2, attrs)
    
    @staticmethod
    def can_be_equals_ex(s1 : str, s2 : str, attrs : 'CanBeEqualsAttrs') -> bool:
        """ Сравнение 2-х строк на предмет равенства с учётом морфологии и пунктуации (то есть инвариантно относительно них).
         Функция довольно трудоёмка, не использовать без крайней необходимости.
        
        Args:
            s1(str): первая строка
            s2(str): вторая строка
            attrs(CanBeEqualsAttrs): дополнительные атрибуты
        
        """
        from pullenti.ner.core.BracketHelper import BracketHelper
        if (Utils.isNullOrEmpty(s1) or Utils.isNullOrEmpty(s2)): 
            return False
        if (s1 == s2): 
            return True
        ak1 = AnalysisKit(SourceOfAnalysis(s1))
        ak2 = AnalysisKit(SourceOfAnalysis(s2))
        t1 = ak1.first_token
        t2 = ak2.first_token
        was_noun = False
        while t1 is not None or t2 is not None:
            if (t1 is not None): 
                if (isinstance(t1, TextToken)): 
                    if (not t1.chars.is_letter and not t1.is_char('№')): 
                        if (BracketHelper.is_bracket(t1, False) and (((attrs) & (CanBeEqualsAttrs.USEBRACKETS))) != (CanBeEqualsAttrs.NO)): 
                            pass
                        else: 
                            if (t1.is_hiphen): 
                                was_noun = False
                            if (((not t1.is_char_of("()") and not t1.is_hiphen)) or (((attrs) & (CanBeEqualsAttrs.IGNORENONLETTERS))) != (CanBeEqualsAttrs.NO)): 
                                t1 = t1.next0_
                                continue
            if (t2 is not None): 
                if (isinstance(t2, TextToken)): 
                    if (not t2.chars.is_letter and not t2.is_char('№')): 
                        if (BracketHelper.is_bracket(t2, False) and (((attrs) & (CanBeEqualsAttrs.USEBRACKETS))) != (CanBeEqualsAttrs.NO)): 
                            pass
                        else: 
                            if (t2.is_hiphen): 
                                was_noun = False
                            if (((not t2.is_char_of("()") and not t2.is_hiphen)) or (((attrs) & (CanBeEqualsAttrs.IGNORENONLETTERS))) != (CanBeEqualsAttrs.NO)): 
                                t2 = t2.next0_
                                continue
            if (isinstance(t1, NumberToken)): 
                if (not ((isinstance(t2, NumberToken)))): 
                    break
                if ((t1).value != (t2).value): 
                    break
                t1 = t1.next0_
                t2 = t2.next0_
                continue
            if (not ((isinstance(t1, TextToken))) or not ((isinstance(t2, TextToken)))): 
                break
            if ((((attrs) & (CanBeEqualsAttrs.IGNOREUPPERCASE))) == (CanBeEqualsAttrs.NO)): 
                if (t1.previous is None and (((attrs) & (CanBeEqualsAttrs.IGNOREUPPERCASEFIRSTWORD))) != (CanBeEqualsAttrs.NO)): 
                    pass
                elif (t1.chars != t2.chars): 
                    return False
            if (not t1.chars.is_letter): 
                bs1 = BracketHelper.can_be_start_of_sequence(t1, False, False)
                bs2 = BracketHelper.can_be_start_of_sequence(t2, False, False)
                if (bs1 != bs2): 
                    return False
                if (bs1): 
                    t1 = t1.next0_
                    t2 = t2.next0_
                    continue
                bs1 = BracketHelper.can_be_end_of_sequence(t1, False, None, False)
                bs2 = BracketHelper.can_be_end_of_sequence(t2, False, None, False)
                if (bs1 != bs2): 
                    return False
                if (bs1): 
                    t1 = t1.next0_
                    t2 = t2.next0_
                    continue
                if (t1.is_hiphen and t2.is_hiphen): 
                    pass
                elif ((t1).term != (t2).term): 
                    return False
                t1 = t1.next0_
                t2 = t2.next0_
                continue
            ok = False
            if (was_noun and (((attrs) & (CanBeEqualsAttrs.CHECKMORPHEQUAFTERFIRSTNOUN))) != (CanBeEqualsAttrs.NO)): 
                if ((t1).term == (t2).term): 
                    ok = True
            else: 
                tt = Utils.asObjectOrNull(t1, TextToken)
                for it in tt.morph.items: 
                    if (isinstance(it, MorphWordForm)): 
                        wf = Utils.asObjectOrNull(it, MorphWordForm)
                        if (t2.is_value(wf.normal_case, None) or t2.is_value(wf.normal_full, None)): 
                            ok = True
                            break
                if (tt.get_morph_class_in_dictionary().is_noun): 
                    was_noun = True
                if (not ok and t1.is_hiphen and t2.is_hiphen): 
                    ok = True
                if (not ok): 
                    if (t2.is_value(tt.term, None) or t2.is_value(tt.lemma, None)): 
                        ok = True
            if (ok): 
                t1 = t1.next0_
                t2 = t2.next0_
                continue
            break
        if ((((attrs) & (CanBeEqualsAttrs.FIRSTCANBESHORTER))) != (CanBeEqualsAttrs.NO)): 
            if (t1 is None): 
                return True
        return t1 is None and t2 is None
    
    @staticmethod
    def can_be_start_of_sentence(t : 'Token') -> bool:
        """ Проверка того, может ли здесь начинаться новое предложение
        
        Args:
            t(Token): токен начала предложения
        
        """
        if (t is None): 
            return False
        if (t.previous is None): 
            return True
        if (not t.is_whitespace_before): 
            if (t.previous is not None and t.previous.is_table_control_char): 
                pass
            else: 
                return False
        if (t.chars.is_letter and t.chars.is_all_lower): 
            if (t.previous.chars.is_letter and t.previous.chars.is_all_lower): 
                return False
            if (((t.previous.is_hiphen or t.previous.is_comma)) and not t.previous.is_whitespace_before and t.previous.previous is not None): 
                if (t.previous.previous.chars.is_letter and t.previous.previous.chars.is_all_lower): 
                    return False
        if (t.whitespaces_before_count > 25 or t.newlines_before_count > 2): 
            return True
        if (t.previous.is_comma_and or t.previous.morph.class0_.is_conjunction): 
            return False
        if (MiscHelper.is_eng_article(t.previous)): 
            return False
        if (t.previous.is_char(':')): 
            return False
        if (t.previous.is_char(';') and t.is_newline_before): 
            return True
        if (t.previous.is_hiphen): 
            if (t.previous.is_newline_before): 
                return True
            pp = t.previous.previous
            if (pp is not None and pp.is_char('.')): 
                return True
        if (t.chars.is_letter and t.chars.is_all_lower): 
            return False
        if (t.is_newline_before): 
            return True
        if (t.previous.is_char_of("!?") or t.previous.is_table_control_char): 
            return True
        if (t.previous.is_char('.') or (((isinstance(t.previous, ReferentToken)) and (t.previous).end_token.is_char('.')))): 
            if (t.whitespaces_before_count > 1): 
                return True
            if (t.next0_ is not None and t.next0_.is_char('.')): 
                if ((isinstance(t.previous.previous, TextToken)) and t.previous.previous.chars.is_all_lower): 
                    pass
                elif (isinstance(t.previous.previous, ReferentToken)): 
                    pass
                else: 
                    return False
            if ((isinstance(t.previous.previous, NumberToken)) and t.previous.is_whitespace_before): 
                if ((t.previous.previous).typ != NumberSpellingType.WORDS): 
                    return False
            return True
        if (MiscHelper.is_eng_article(t)): 
            return True
        return False
    
    @staticmethod
    def find_end_of_sentence(t : 'Token') -> 'Token':
        """ Переместиться на конец предложения
        
        Args:
            t(Token): токен, с которого идёт поиск
        
        Returns:
            Token: последний токен предложения (не обязательно точка!)
        """
        tt = t
        while tt is not None: 
            if (tt.next0_ is None): 
                return tt
            elif (MiscHelper.can_be_start_of_sentence(tt)): 
                return (t if tt == t else tt.previous)
            tt = tt.next0_
        return None
    
    @staticmethod
    def check_number_prefix(t : 'Token') -> 'Token':
        """ Привязка различных способов написания ключевых слов для номеров (ном., №, рег.номер и пр.)
        
        Args:
            t(Token): начало префикса
        
        Returns:
            Token: null, если не префикс, или токен, следующий сразу за префиксом номера
        """
        if (not ((isinstance(t, TextToken)))): 
            return None
        s = (t).term
        t1 = None
        if (t.is_value("ПО", None) and t.next0_ is not None): 
            t = t.next0_
        if ((((t.is_value("РЕГИСТРАЦИОННЫЙ", "РЕЄСТРАЦІЙНИЙ") or t.is_value("ГОСУДАРСТВЕННЫЙ", "ДЕРЖАВНИЙ") or t.is_value("ТРАНЗИТНЫЙ", "ТРАНЗИТНИЙ")) or t.is_value("ДЕЛО", None) or t.is_value("СПРАВА", None))) and (isinstance(t.next0_, TextToken))): 
            t = t.next0_
            s = (t).term
        elif (s == "РЕГ" or s == "ГОС" or s == "ТРАНЗ"): 
            if (t.next0_ is not None and t.next0_.is_char('.')): 
                t = t.next0_
            if (isinstance(t.next0_, TextToken)): 
                t = t.next0_
                s = (t).term
            else: 
                return None
        if (((s == "НОМЕР" or s == "№" or s == "N") or s == "NO" or s == "NN") or s == "НР"): 
            t1 = t.next0_
            if (t1 is not None and ((t1.is_char_of("°№") or t1.is_value("О", None)))): 
                t1 = t1.next0_
            if (t1 is not None and t1.is_char('.')): 
                t1 = t1.next0_
            if (t1 is not None and t1.is_char(':')): 
                t1 = t1.next0_
        elif (s == "НОМ"): 
            t1 = t.next0_
            if (t1 is not None and t1.is_char('.')): 
                t1 = t1.next0_
        while t1 is not None:
            if (t1.is_value("ЗАПИСЬ", None)): 
                t1 = t1.next0_
            elif (t1.is_value("В", None) and t1.next0_ is not None and t1.next0_.is_value("РЕЕСТР", None)): 
                t1 = t1.next0_.next0_
            else: 
                break
        return t1
    
    @staticmethod
    def _corr_xml_text(txt : str) -> str:
        if (txt is None): 
            return ""
        for c in txt: 
            if ((((ord(c)) < 0x20) and c != '\r' and c != '\n') and c != '\t'): 
                tmp = Utils.newStringIO(txt)
                i = 0
                while i < tmp.tell(): 
                    ch = Utils.getCharAtStringIO(tmp, i)
                    if ((((ord(ch)) < 0x20) and ch != '\r' and ch != '\n') and ch != '\t'): 
                        Utils.setCharAtStringIO(tmp, i, ' ')
                    i += 1
                return Utils.toStringStringIO(tmp)
        return txt
    
    @staticmethod
    def convert_first_char_upper_and_other_lower(str0_ : str) -> str:
        """ Преобразовать строку чтобы первая буква стала большой, остальные маленькие
        
        Args:
            str0_(str): 
        
        """
        if (Utils.isNullOrEmpty(str0_)): 
            return str0_
        fstr_tmp = io.StringIO()
        print(str0_.lower(), end="", file=fstr_tmp)
        up = True
        Utils.replaceStringIO(fstr_tmp, " .", ".")
        i = 0
        while i < fstr_tmp.tell(): 
            if (str.isalpha(Utils.getCharAtStringIO(fstr_tmp, i))): 
                if (up): 
                    if (((i + 1) >= fstr_tmp.tell() or str.isalpha(Utils.getCharAtStringIO(fstr_tmp, i + 1)) or ((Utils.getCharAtStringIO(fstr_tmp, i + 1) == '.' or Utils.getCharAtStringIO(fstr_tmp, i + 1) == '-'))) or i == 0): 
                        Utils.setCharAtStringIO(fstr_tmp, i, str.upper(Utils.getCharAtStringIO(fstr_tmp, i)))
                up = False
            elif (not str.isdigit(Utils.getCharAtStringIO(fstr_tmp, i))): 
                up = True
            i += 1
        Utils.replaceStringIO(fstr_tmp, " - ", "-")
        return Utils.toStringStringIO(fstr_tmp)
    
    @staticmethod
    def get_abbreviation(name : str) -> str:
        """ Сделать аббревиатуру для строки из нескольких слов
        
        Args:
            name(str): 
        
        """
        abbr = io.StringIO()
        i = 0
        while i < len(name): 
            if (str.isdigit(name[i])): 
                break
            elif (str.isalpha(name[i])): 
                j = (i + 1)
                while j < len(name): 
                    if (not str.isalpha(name[j])): 
                        break
                    j += 1
                if ((j - i) > 2): 
                    w = name[i:i+j - i]
                    if (w != "ПРИ"): 
                        print(name[i], end="", file=abbr)
                i = j
            i += 1
        if (abbr.tell() < 2): 
            return None
        return Utils.toStringStringIO(abbr).upper()
    
    @staticmethod
    def get_tail_abbreviation(name : str) -> str:
        """ Получить аббревиатуру (уже не помню, какую именно...)
        
        Args:
            name(str): 
        
        """
        j = 0
        i = 0
        while i < len(name): 
            if (name[i] == ' '): 
                j += 1
            i += 1
        if (j < 2): 
            return None
        a0 = chr(0)
        a1 = chr(0)
        j = 0
        for i in range(len(name) - 2, 0, -1):
            if (name[i] == ' '): 
                le = 0
                jj = i + 1
                while jj < len(name): 
                    if (name[jj] == ' '): 
                        break
                    else: 
                        le += 1
                    jj += 1
                if (le < 4): 
                    break
                if (j == 0): 
                    a1 = name[i + 1]
                elif (j == 1): 
                    a0 = name[i + 1]
                    if (str.isalpha(a0) and str.isalpha(a1)): 
                        return "{0} {1}{2}".format(name[0:0+i], a0, a1)
                    break
                j += 1
        else: i = 0
        return None
    
    @staticmethod
    def create_cyr_lat_alternative(str0_ : str) -> str:
        """ Попытка через транслитеральную замену сделать альтернативное написание строки
         Например, А-10 => A-10  (здесь латиница и кириллица)
        
        Args:
            str0_(str): 
        
        Returns:
            str: если null, то не получается
        """
        if (str0_ is None): 
            return None
        cyr = 0
        cyr_to_lat = 0
        lat = 0
        lat_to_cyr = 0
        i = 0
        while i < len(str0_): 
            ch = str0_[i]
            if (LanguageHelper.is_latin_char(ch)): 
                lat += 1
                if (LanguageHelper.get_cyr_for_lat(ch) != (chr(0))): 
                    lat_to_cyr += 1
            elif (LanguageHelper.is_cyrillic_char(ch)): 
                cyr += 1
                if (LanguageHelper.get_lat_for_cyr(ch) != (chr(0))): 
                    cyr_to_lat += 1
            i += 1
        if (cyr > 0 and cyr_to_lat == cyr): 
            if (lat > 0): 
                return None
            tmp = Utils.newStringIO(str0_)
            i = 0
            while i < tmp.tell(): 
                if (LanguageHelper.is_cyrillic_char(Utils.getCharAtStringIO(tmp, i))): 
                    Utils.setCharAtStringIO(tmp, i, LanguageHelper.get_lat_for_cyr(Utils.getCharAtStringIO(tmp, i)))
                i += 1
            return Utils.toStringStringIO(tmp)
        if (lat > 0 and lat_to_cyr == lat): 
            if (cyr > 0): 
                return None
            tmp = Utils.newStringIO(str0_)
            i = 0
            while i < tmp.tell(): 
                if (LanguageHelper.is_latin_char(Utils.getCharAtStringIO(tmp, i))): 
                    Utils.setCharAtStringIO(tmp, i, LanguageHelper.get_cyr_for_lat(Utils.getCharAtStringIO(tmp, i)))
                i += 1
            return Utils.toStringStringIO(tmp)
        return None
    
    @staticmethod
    def convert_latin_word_to_russian_variants(str0_ : str) -> typing.List[str]:
        """ Преобразовать слово, написанное по латыни, в варианты на русском языке.
         Например, "Mikhail" -> "Михаил"
        
        Args:
            str0_(str): Строка на латыни
        
        Returns:
            typing.List[str]: Варианты на русском языке
        """
        return MiscHelper.__convert_word(str0_, True)
    
    @staticmethod
    def convert_russian_word_to_latin_variants(str0_ : str) -> typing.List[str]:
        """ Преобразовать слово, написанное в кириллице, в варианты на латинице.
        
        Args:
            str0_(str): Строка на кириллице
        
        Returns:
            typing.List[str]: Варианты на латинице
        """
        return MiscHelper.__convert_word(str0_, False)
    
    @staticmethod
    def __convert_word(str0_ : str, latin_to_rus : bool) -> typing.List[str]:
        if (str0_ is None): 
            return None
        if (len(str0_) == 0): 
            return None
        str0_ = str0_.upper()
        res = list()
        vars0_ = list()
        i = 0
        while i < len(str0_): 
            v = list()
            if (latin_to_rus): 
                j = RusLatAccord.find_accords_lat_to_rus(str0_, i, v)
            else: 
                j = RusLatAccord.find_accords_rus_to_lat(str0_, i, v)
            if (j < 1): 
                j = 1
                v.append(str0_[i:i+1])
            vars0_.append(v)
            i += (j - 1)
            i += 1
        if (latin_to_rus and ("AEIJOUY".find(str0_[len(str0_) - 1]) < 0)): 
            v = list()
            v.append("")
            v.append("Ь")
            vars0_.append(v)
        fstr_tmp = io.StringIO()
        inds = list()
        i = 0
        while i < len(vars0_): 
            inds.append(0)
            i += 1
        while True:
            Utils.setLengthStringIO(fstr_tmp, 0)
            i = 0
            while i < len(vars0_): 
                if (len(vars0_[i]) > 0): 
                    print(vars0_[i][inds[i]], end="", file=fstr_tmp)
                i += 1
            res.append(Utils.toStringStringIO(fstr_tmp))
            for i in range(len(inds) - 1, -1, -1):
                inds[i] += 1
                if (inds[i] < len(vars0_[i])): 
                    break
                inds[i] = 0
            else: i = -1
            if (i < 0): 
                break
        return res
    
    @staticmethod
    def get_absolute_normal_value(str0_ : str, get_always : bool=False) -> str:
        """ Получение абсолютного нормализованного значения (с учётом гласных, удалением невидимых знаков и т.п.).
         Используется для сравнений различных вариантов написаний.
         Преобразования:  гласные заменяются на *, Щ на Ш, Х на Г, одинаковые соседние буквы сливаются,
         Ъ и Ь выбрасываются.
         Например, ХАБИБУЛЛИН -  Г*Б*Б*Л*Н
        
        Args:
            str0_(str): страка
        
        Returns:
            str: если null, то не удалось нормализовать (слишком короткий)
        """
        res = io.StringIO()
        k = 0
        i = 0
        while i < len(str0_): 
            if (LanguageHelper.is_cyrillic_vowel(str0_[i]) or str0_[i] == 'Й' or LanguageHelper.is_latin_vowel(str0_[i])): 
                if (res.tell() > 0 and Utils.getCharAtStringIO(res, res.tell() - 1) == '*'): 
                    pass
                else: 
                    print('*', end="", file=res)
            elif (str0_[i] != 'Ь' and str0_[i] != 'Ъ'): 
                ch = str0_[i]
                if (ch == 'Щ'): 
                    ch = 'Ш'
                if (ch == 'Х'): 
                    ch = 'Г'
                if (ch == ' '): 
                    ch = '-'
                print(ch, end="", file=res)
                k += 1
            i += 1
        if (res.tell() > 0 and Utils.getCharAtStringIO(res, res.tell() - 1) == '*'): 
            Utils.setLengthStringIO(res, res.tell() - 1)
        for i in range(res.tell() - 1, 0, -1):
            if (Utils.getCharAtStringIO(res, i) == Utils.getCharAtStringIO(res, i - 1) and Utils.getCharAtStringIO(res, i) != '*'): 
                Utils.removeStringIO(res, i, 1)
        for i in range(res.tell() - 1, 0, -1):
            if (Utils.getCharAtStringIO(res, i - 1) == '*' and Utils.getCharAtStringIO(res, i) == '-'): 
                Utils.removeStringIO(res, i - 1, 1)
        if (not get_always): 
            if ((res.tell() < 3) or (k < 2)): 
                return None
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def is_exists_in_dictionary(begin : 'Token', end : 'Token', cla : 'MorphClass') -> bool:
        """ Проверка, что хотя бы одно из слов внутри заданного диапазона находится в морфологическом словаре
        
        Args:
            begin(Token): 
            end(Token): 
            cla(MorphClass): 
        
        """
        ret = False
        t = begin
        while t is not None: 
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is not None): 
                if (tt.is_hiphen): 
                    ret = False
                for wf in tt.morph.items: 
                    if (cla.value == (0) or (((cla.value) & (wf.class0_.value))) != 0): 
                        if ((isinstance(wf, MorphWordForm)) and (wf).is_in_dictionary): 
                            ret = True
                            break
            if (t == end): 
                break
            t = t.next0_
        return ret
    
    @staticmethod
    def is_all_characters_lower(begin : 'Token', end : 'Token', error_if_not_text : bool=False) -> bool:
        """ Проверка, что все в заданном диапазоне в нижнем регистре
        
        Args:
            begin(Token): 
            end(Token): 
            error_if_not_text(bool): 
        
        """
        t = begin
        while t is not None: 
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is None): 
                if (error_if_not_text): 
                    return False
            elif (not tt.chars.is_all_lower): 
                return False
            if (t == end): 
                break
            t = t.next0_
        return True
    
    @staticmethod
    def has_vowel(t : 'TextToken') -> bool:
        """ Текстовой токен должен иметь гласную
        
        Args:
            t(TextToken): токен
        
        """
        if (t is None): 
            return False
        tmp = unicodedata.normalize('NFD', t.term)
        for ch in tmp: 
            if (LanguageHelper.is_cyrillic_vowel(ch) or LanguageHelper.is_latin_vowel(ch)): 
                return True
        return False
    
    @staticmethod
    def test_acronym(acr : 'Token', begin : 'Token', end : 'Token') -> bool:
        """ Проверка акронима, что из первых букв слов диапазона может получиться проверяемый акроним.
         Например,  РФ = Российская Федерация, ГосПлан = государственный план
        
        Args:
            acr(Token): акроним
            begin(Token): начало диапазона
            end(Token): конец диапазона
        
        """
        if (not ((isinstance(acr, TextToken)))): 
            return False
        if (begin is None or end is None or begin.end_char >= end.begin_char): 
            return False
        str0_ = (acr).term
        i = 0
        t = begin
        while t is not None and t.previous != end: 
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is None): 
                break
            if (i >= len(str0_)): 
                return False
            s = tt.term
            if (s[0] != str0_[i]): 
                return False
            i += 1
            t = t.next0_
        if (i >= len(str0_)): 
            return True
        return False
    
    @staticmethod
    def get_cyr_lat_word(t : 'Token', max_len : int=0) -> 'CyrLatWord':
        """ Получить вариант на кириллице и\или латинице
        
        Args:
            t(Token): 
            max_len(int): 
        
        """
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            rt = Utils.asObjectOrNull(t, ReferentToken)
            if ((rt is not None and (rt.length_char < 3) and rt.begin_token == rt.end_token) and (isinstance(rt.begin_token, TextToken))): 
                tt = (Utils.asObjectOrNull(rt.begin_token, TextToken))
            else: 
                return None
        if (not tt.chars.is_letter): 
            return None
        str0_ = tt.get_source_text()
        if (max_len > 0 and len(str0_) > max_len): 
            return None
        cyr = io.StringIO()
        lat = io.StringIO()
        for s in str0_: 
            if (LanguageHelper.is_latin_char(s)): 
                if (lat is not None): 
                    print(s, end="", file=lat)
                i = MiscHelper.M_LAT.find(s)
                if (i < 0): 
                    cyr = (None)
                elif (cyr is not None): 
                    print(MiscHelper.M_CYR[i], end="", file=cyr)
            elif (LanguageHelper.is_cyrillic_char(s)): 
                if (cyr is not None): 
                    print(s, end="", file=cyr)
                i = MiscHelper.M_CYR.find(s)
                if (i < 0): 
                    lat = (None)
                elif (lat is not None): 
                    print(MiscHelper.M_LAT[i], end="", file=lat)
            else: 
                return None
        if (cyr is None and lat is None): 
            return None
        res = MiscHelper.CyrLatWord()
        if (cyr is not None): 
            res.cyr_word = Utils.toStringStringIO(cyr).upper()
        if (lat is not None): 
            res.lat_word = Utils.toStringStringIO(lat).upper()
        return res
    
    M_CYR = "АВДЕКМНОРСТХаекорсух"
    
    M_LAT = "ABDEKMHOPCTXaekopcyx"
    
    @staticmethod
    def can_be_equal_cyr_and_latts(t : 'Token', str0_ : str) -> bool:
        """ Проверка на возможную эквивалентность русского и латинского написания одного и того же слова
        
        Args:
            t(Token): 
            str0_(str): 
        
        """
        if (t is None or Utils.isNullOrEmpty(str0_)): 
            return False
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return False
        if (MiscHelper.can_be_equal_cyr_and_latss(tt.term, str0_)): 
            return True
        for wf in tt.morph.items: 
            if ((isinstance(wf, MorphWordForm)) and MiscHelper.can_be_equal_cyr_and_latss((wf).normal_case, str0_)): 
                return True
        return False
    
    @staticmethod
    def can_be_equal_cyr_and_lattt(t1 : 'Token', t2 : 'Token') -> bool:
        """ Проверка на возможную эквивалентность русского и латинского написания одного и того же слова.
         Например,  ИКЕЯ ? IKEA
        
        Args:
            t1(Token): токен на одном языке
            t2(Token): токен на другом языке
        
        """
        tt1 = Utils.asObjectOrNull(t1, TextToken)
        tt2 = Utils.asObjectOrNull(t2, TextToken)
        if (tt1 is None or tt2 is None): 
            return False
        if (MiscHelper.can_be_equal_cyr_and_latts(t2, tt1.term)): 
            return True
        for wf in tt1.morph.items: 
            if ((isinstance(wf, MorphWordForm)) and MiscHelper.can_be_equal_cyr_and_latts(t2, (wf).normal_case)): 
                return True
        return False
    
    @staticmethod
    def can_be_equal_cyr_and_latss(str1 : str, str2 : str) -> bool:
        """ Проверка на возможную эквивалентность русского и латинского написания одного и того же слова.
         Например,  ИКЕЯ ? IKEA
        
        Args:
            str1(str): слово на одном языке
            str2(str): слово на другом языке
        
        """
        if (Utils.isNullOrEmpty(str1) or Utils.isNullOrEmpty(str2)): 
            return False
        if (LanguageHelper.is_cyrillic_char(str1[0]) and LanguageHelper.is_latin_char(str2[0])): 
            return RusLatAccord.can_be_equals(str1, str2)
        if (LanguageHelper.is_cyrillic_char(str2[0]) and LanguageHelper.is_latin_char(str1[0])): 
            return RusLatAccord.can_be_equals(str2, str1)
        return False
    
    @staticmethod
    def get_text_value_of_meta_token(mt : 'MetaToken', attrs : 'GetTextAttr'=GetTextAttr.NO) -> str:
        """ Получить текст, покрываемый метатокеном
        
        Args:
            mt(MetaToken): метатокен
            attrs(GetTextAttr): атрибуты преобразования текста
        
        Returns:
            str: результат
        """
        if (mt is None): 
            return None
        return MiscHelper.__get_text_value_(mt.begin_token, mt.end_token, attrs, mt.get_referent())
    
    @staticmethod
    def get_text_value(begin : 'Token', end : 'Token', attrs : 'GetTextAttr'=GetTextAttr.NO) -> str:
        """ Получить текст, задаваемый диапазоном токенов
        
        Args:
            begin(Token): начальный токен
            end(Token): конечный токен
            attrs(GetTextAttr): атрибуты преобразования текста
        
        Returns:
            str: результат
        """
        return MiscHelper.__get_text_value_(begin, end, attrs, None)
    
    @staticmethod
    def __get_text_value_(begin : 'Token', end : 'Token', attrs : 'GetTextAttr', r : 'Referent') -> str:
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.core.BracketHelper import BracketHelper
        if (begin is None or end is None or begin.end_char > end.end_char): 
            return None
        if ((((attrs) & (GetTextAttr.KEEPQUOTES))) == (GetTextAttr.NO)): 
            while begin is not None and begin.end_char <= end.end_char: 
                if (BracketHelper.is_bracket(begin, True)): 
                    pass
                else: 
                    break
                begin = begin.next0_
        res = io.StringIO()
        if ((isinstance(begin, MetaToken)) and not ((isinstance(begin, NumberToken)))): 
            str0_ = MiscHelper.__get_text_value_((begin).begin_token, (begin).end_token, attrs, begin.get_referent())
            if (str0_ is not None): 
                if (end == begin): 
                    return str0_
                if ((isinstance(end, MetaToken)) and not ((isinstance(end, NumberToken))) and begin.next0_ == end): 
                    if ((((attrs) & (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE))) == (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE) or (((attrs) & (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE))) == (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE)): 
                        attrs1 = attrs
                        if ((((attrs1) & (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE))) == (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)): 
                            attrs1 = (Utils.valToEnum((attrs1) ^ (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE), GetTextAttr))
                        if ((((attrs1) & (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE))) == (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE)): 
                            attrs1 = (Utils.valToEnum((attrs1) ^ (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE), GetTextAttr))
                        str0 = MiscHelper.__get_text_value_((begin).begin_token, (begin).end_token, attrs1, begin.get_referent())
                        str1 = MiscHelper.__get_text_value_((end).begin_token, (end).end_token, attrs1, begin.get_referent())
                        ar0 = ProcessorService.get_empty_processor().process(SourceOfAnalysis("{0} {1}".format(str0, str1)), None, None)
                        npt1 = NounPhraseHelper.try_parse(ar0.first_token, NounPhraseParseAttr.NO, 0)
                        if (npt1 is not None and npt1.end_token.next0_ is None): 
                            return MiscHelper.__get_text_value_(npt1.begin_token, npt1.end_token, attrs, r)
                print(str0_, end="", file=res)
                begin = begin.next0_
                if ((((attrs) & (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE))) == (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)): 
                    attrs = (Utils.valToEnum((attrs) ^ (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE), GetTextAttr))
                if ((((attrs) & (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE))) == (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE)): 
                    attrs = (Utils.valToEnum((attrs) ^ (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE), GetTextAttr))
        keep_chars = (((attrs) & (GetTextAttr.KEEPREGISTER))) != (GetTextAttr.NO)
        if (keep_chars): 
            pass
        restore_chars_end_pos = -1
        if ((((attrs) & (GetTextAttr.RESTOREREGISTER))) != (GetTextAttr.NO)): 
            if (not MiscHelper.__has_not_all_upper(begin, end)): 
                restore_chars_end_pos = end.end_char
            else: 
                tt1 = begin
                while tt1 is not None and (tt1.end_char < end.end_char): 
                    if (tt1.is_newline_after and not tt1.is_hiphen): 
                        if (not MiscHelper.__has_not_all_upper(begin, tt1)): 
                            restore_chars_end_pos = tt1.end_char
                        break
                    tt1 = tt1.next0_
        if ((((attrs) & (((GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE) | (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE))))) != (GetTextAttr.NO)): 
            npt = NounPhraseHelper.try_parse(begin, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.end_char <= end.end_char): 
                str0_ = npt.get_normal_case_text(None, (((attrs) & (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE))) != (GetTextAttr.NO), npt.morph.gender, keep_chars)
                if (str0_ is not None): 
                    begin = npt.end_token.next0_
                    print(str0_, end="", file=res)
                    te = npt.end_token.next0_
                    if (((te is not None and te.next0_ is not None and te.is_comma) and (isinstance(te.next0_, TextToken)) and te.next0_.end_char <= end.end_char) and te.next0_.morph.class0_.is_verb and te.next0_.morph.class0_.is_adjective): 
                        for it in te.next0_.morph.items: 
                            if (it.gender == npt.morph.gender or (((it.gender) & (npt.morph.gender))) != (MorphGender.UNDEFINED)): 
                                if (not ((it.case_) & npt.morph.case_).is_undefined): 
                                    if (it.number == npt.morph.number or (((it.number) & (npt.morph.number))) != (MorphNumber.UNDEFINED)): 
                                        var = (te.next0_).term
                                        if (isinstance(it, MorphWordForm)): 
                                            var = (it).normal_case
                                        bi = MorphBaseInfo._new562(MorphClass.ADJECTIVE, npt.morph.gender, npt.morph.number, npt.morph.language)
                                        var = Morphology.get_wordform(var, bi)
                                        if (var is not None): 
                                            var = MiscHelper.__corr_chars(var, te.next0_.chars, keep_chars, Utils.asObjectOrNull(te.next0_, TextToken))
                                            print(", {1}".format(res, var), end="", file=res, flush=True)
                                            te = te.next0_.next0_
                                        break
                    begin = te
            if ((((attrs) & (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE))) == (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)): 
                attrs = (Utils.valToEnum((attrs) ^ (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE), GetTextAttr))
            if ((((attrs) & (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE))) == (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE)): 
                attrs = (Utils.valToEnum((attrs) ^ (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE), GetTextAttr))
        if (begin is None or begin.end_char > end.end_char): 
            return Utils.toStringStringIO(res)
        t = begin
        first_pass2950 = True
        while True:
            if first_pass2950: first_pass2950 = False
            else: t = t.next0_
            if (not (t is not None and t.end_char <= end.end_char)): break
            last = (Utils.getCharAtStringIO(res, res.tell() - 1) if res.tell() > 0 else ' ')
            if (t.is_whitespace_before and res.tell() > 0): 
                if (t.is_hiphen and t.is_whitespace_after and last != ' '): 
                    print(" - ", end="", file=res)
                    continue
                if ((last != ' ' and not t.is_hiphen and last != '-') and not BracketHelper.can_be_start_of_sequence(t.previous, False, False)): 
                    print(' ', end="", file=res)
            if (t.is_table_control_char): 
                if (res.tell() > 0 and Utils.getCharAtStringIO(res, res.tell() - 1) == ' '): 
                    pass
                else: 
                    print(' ', end="", file=res)
                continue
            if ((((attrs) & (GetTextAttr.IGNOREARTICLES))) != (GetTextAttr.NO)): 
                if (MiscHelper.is_eng_adj_suffix(t)): 
                    t = t.next0_
                    continue
                if (MiscHelper.is_eng_article(t)): 
                    if (t.is_whitespace_after): 
                        continue
            if ((((attrs) & (GetTextAttr.KEEPQUOTES))) == (GetTextAttr.NO)): 
                if (BracketHelper.is_bracket(t, True)): 
                    if (res.tell() > 0 and Utils.getCharAtStringIO(res, res.tell() - 1) != ' '): 
                        print(' ', end="", file=res)
                    continue
            if ((((attrs) & (GetTextAttr.IGNOREGEOREFERENT))) != (GetTextAttr.NO)): 
                if ((isinstance(t, ReferentToken)) and t.get_referent() is not None): 
                    if (t.get_referent().type_name == "GEO"): 
                        continue
            if (isinstance(t, NumberToken)): 
                if ((((attrs) & (GetTextAttr.NORMALIZENUMBERS))) != (GetTextAttr.NO)): 
                    if (res.tell() > 0 and str.isdigit(Utils.getCharAtStringIO(res, res.tell() - 1))): 
                        print(' ', end="", file=res)
                    print((t).value, end="", file=res)
                    continue
            if (isinstance(t, MetaToken)): 
                str0_ = MiscHelper.__get_text_value_((t).begin_token, (t).end_token, attrs, t.get_referent())
                if (not Utils.isNullOrEmpty(str0_)): 
                    if (str.isdigit(str0_[0]) and res.tell() > 0 and str.isdigit(Utils.getCharAtStringIO(res, res.tell() - 1))): 
                        print(' ', end="", file=res)
                    print(str0_, end="", file=res)
                else: 
                    print(t.get_source_text(), end="", file=res)
                continue
            if (not ((isinstance(t, TextToken)))): 
                print(t.get_source_text(), end="", file=res)
                continue
            if (t.chars.is_letter): 
                str0_ = (MiscHelper.__rest_chars(Utils.asObjectOrNull(t, TextToken), r) if t.end_char <= restore_chars_end_pos else MiscHelper.__corr_chars((t).term, t.chars, keep_chars, Utils.asObjectOrNull(t, TextToken)))
                print(str0_, end="", file=res)
                continue
            if (last == ' ' and res.tell() > 0): 
                if (((t.is_hiphen and not t.is_whitespace_after)) or t.is_char_of(",.;!?") or BracketHelper.can_be_end_of_sequence(t, False, None, False)): 
                    Utils.setLengthStringIO(res, res.tell() - 1)
            if (t.is_hiphen): 
                print('-', end="", file=res)
                if (t.is_whitespace_before and t.is_whitespace_after): 
                    print(' ', end="", file=res)
            else: 
                print((t).term, end="", file=res)
        i = res.tell() - 1
        while i >= 0: 
            if (Utils.getCharAtStringIO(res, i) == '*' or Utils.isWhitespace(Utils.getCharAtStringIO(res, i))): 
                Utils.setLengthStringIO(res, res.tell() - 1)
            elif (Utils.getCharAtStringIO(res, i) == '>' and (((attrs) & (GetTextAttr.KEEPQUOTES))) == (GetTextAttr.NO)): 
                if (Utils.getCharAtStringIO(res, 0) == '<'): 
                    Utils.setLengthStringIO(res, res.tell() - 1)
                    Utils.removeStringIO(res, 0, 1)
                    i -= 1
                elif (begin.previous is not None and begin.previous.is_char('<')): 
                    Utils.setLengthStringIO(res, res.tell() - 1)
                else: 
                    break
            elif (Utils.getCharAtStringIO(res, i) == ')' and (((attrs) & (GetTextAttr.KEEPQUOTES))) == (GetTextAttr.NO)): 
                if (Utils.getCharAtStringIO(res, 0) == '('): 
                    Utils.setLengthStringIO(res, res.tell() - 1)
                    Utils.removeStringIO(res, 0, 1)
                    i -= 1
                elif (begin.previous is not None and begin.previous.is_char('(')): 
                    Utils.setLengthStringIO(res, res.tell() - 1)
                else: 
                    break
            else: 
                break
            i -= 1
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def is_eng_adj_suffix(t : 'Token') -> bool:
        """ Проверка, что это суффикс прилагательного (street's)
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.core.BracketHelper import BracketHelper
        if (t is None): 
            return False
        if (not BracketHelper.is_bracket(t, True)): 
            return False
        if ((isinstance(t.next0_, TextToken)) and (t.next0_).term == "S"): 
            return True
        return False
    
    @staticmethod
    def is_eng_article(t : 'Token') -> bool:
        if (not ((isinstance(t, TextToken))) or not t.chars.is_latin_letter): 
            return False
        str0_ = (t).term
        return ((str0_ == "THE" or str0_ == "A" or str0_ == "AN") or str0_ == "DER" or str0_ == "DIE") or str0_ == "DAS"
    
    @staticmethod
    def __has_not_all_upper(b : 'Token', e0_ : 'Token') -> bool:
        t = b
        while t is not None and t.end_char <= e0_.end_char: 
            if (isinstance(t, TextToken)): 
                if (t.chars.is_letter and not t.chars.is_all_upper): 
                    return True
            elif (isinstance(t, MetaToken)): 
                if (MiscHelper.__has_not_all_upper((t).begin_token, (t).end_token)): 
                    return True
            t = t.next0_
        return False
    
    @staticmethod
    def __corr_chars(str0_ : str, ci : 'CharsInfo', keep_chars : bool, t : 'TextToken') -> str:
        if (not keep_chars): 
            return str0_
        if (ci.is_all_lower): 
            return str0_.lower()
        if (ci.is_capital_upper): 
            return MiscHelper.convert_first_char_upper_and_other_lower(str0_)
        if (ci.is_all_upper or t is None): 
            return str0_
        src = t.get_source_text()
        if (len(src) == len(str0_)): 
            tmp = Utils.newStringIO(str0_)
            i = 0
            while i < tmp.tell(): 
                if (str.isalpha(src[i]) and str.islower(src[i])): 
                    Utils.setCharAtStringIO(tmp, i, str.lower(Utils.getCharAtStringIO(tmp, i)))
                i += 1
            str0_ = Utils.toStringStringIO(tmp)
        return str0_
    
    @staticmethod
    def __rest_chars(t : 'TextToken', r : 'Referent') -> str:
        from pullenti.ner.core.BracketHelper import BracketHelper
        if (not t.chars.is_all_upper or not t.chars.is_letter): 
            return MiscHelper.__corr_chars(t.term, t.chars, True, t)
        if (t.term == "Г" or t.term == "ГГ"): 
            if (isinstance(t.previous, NumberToken)): 
                return t.term.lower()
        elif (t.term == "X"): 
            if ((isinstance(t.previous, NumberToken)) or ((t.previous is not None and t.previous.is_hiphen))): 
                return t.term.lower()
        elif (t.term == "N" or t.term == "№"): 
            return t.term
        can_cap_up = False
        if (BracketHelper.can_be_start_of_sequence(t.previous, True, False)): 
            can_cap_up = True
        elif (t.previous is not None and t.previous.is_char('.') and t.is_whitespace_before): 
            can_cap_up = True
        stat = t.kit.statistics.get_word_info(t)
        if (stat is None or ((r is not None and ((r.type_name == "DATE" or r.type_name == "DATERANGE"))))): 
            return (MiscHelper.convert_first_char_upper_and_other_lower(t.term) if can_cap_up else t.term.lower())
        if (stat.lower_count > 0): 
            return (MiscHelper.convert_first_char_upper_and_other_lower(t.term) if can_cap_up else t.term.lower())
        mc = t.get_morph_class_in_dictionary()
        if (mc.is_noun): 
            if (((t.is_value("СОЗДАНИЕ", None) or t.is_value("РАЗВИТИЕ", None) or t.is_value("ВНЕСЕНИЕ", None)) or t.is_value("ИЗМЕНЕНИЕ", None) or t.is_value("УТВЕРЖДЕНИЕ", None)) or t.is_value("ПРИНЯТИЕ", None)): 
                return (MiscHelper.convert_first_char_upper_and_other_lower(t.term) if can_cap_up else t.term.lower())
        if (((mc.is_verb or mc.is_adverb or mc.is_conjunction) or mc.is_preposition or mc.is_pronoun) or mc.is_personal_pronoun): 
            return (MiscHelper.convert_first_char_upper_and_other_lower(t.term) if can_cap_up else t.term.lower())
        if (stat.capital_count > 0): 
            return MiscHelper.convert_first_char_upper_and_other_lower(t.term)
        if (mc.is_proper): 
            return MiscHelper.convert_first_char_upper_and_other_lower(t.term)
        if (mc.is_adjective): 
            return (MiscHelper.convert_first_char_upper_and_other_lower(t.term) if can_cap_up else t.term.lower())
        if (mc == MorphClass.NOUN): 
            return (MiscHelper.convert_first_char_upper_and_other_lower(t.term) if can_cap_up else t.term.lower())
        return t.term
    
    @staticmethod
    def get_text_morph_var_by_sample(txt : str, begin_sample : 'Token', use_morph_sample : bool, use_register_sample : bool) -> str:
        """ Преобразовать строку в нужный род, число и падеж (точнее, преобразуется
         первая именная группа), регистр определяется соответствующими символами примера.
         Морфология определяется по первой именной группе примера.
         Фукнция полезна при замене по тексту одной комбинации на другую с учётом
         морфологии и регистра.
        
        Args:
            txt(str): преобразуемая строка
            begin_sample(Token): начало фрагмента примера
            useMopthSample: использовать именную группу примера для морфологии
            use_register_sample(bool): регистр определять по фрагменту пример, при false регистр исходной строки
        
        Returns:
            str: результат, в худшем случае вернёт исходную строку
        """
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        if (Utils.isNullOrEmpty(txt)): 
            return txt
        npt = NounPhraseHelper.try_parse(begin_sample, NounPhraseParseAttr.NO, 0)
        if (npt is not None and begin_sample.previous is not None): 
            tt = begin_sample.previous
            while tt is not None: 
                if (tt.whitespaces_after_count > 2): 
                    break
                npt0 = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0)
                if (npt0 is not None): 
                    if (npt0.end_token == npt.end_token): 
                        npt.morph = npt0.morph
                    else: 
                        if (tt == begin_sample.previous and npt.begin_token == npt.end_token and npt.morph.case_.is_genitive): 
                            npt.morph.remove_items(MorphCase.GENITIVE, False)
                        break
                tt = tt.previous
        ar = ProcessorService.get_empty_processor().process(SourceOfAnalysis(txt), None, None)
        if (ar is None or ar.first_token is None): 
            return txt
        npt1 = NounPhraseHelper.try_parse(ar.first_token, NounPhraseParseAttr.NO, 0)
        t0 = begin_sample
        res = io.StringIO()
        t = ar.first_token
        while t is not None: 
            if (t.is_whitespace_before and t != ar.first_token): 
                print(' ', end="", file=res)
            word = None
            if ((isinstance(t, TextToken)) and t.chars.is_letter): 
                word = (t).term
                if ((npt1 is not None and t.end_char <= npt1.end_char and npt is not None) and use_morph_sample): 
                    bi = MorphBaseInfo()
                    bi.number = npt.morph.number
                    bi.case_ = npt.morph.case_
                    bi.gender = npt1.morph.gender
                    ww = Morphology.get_wordform(word, bi)
                    if (ww is not None): 
                        word = ww
                if (use_register_sample and t0 is not None): 
                    ci = t0.chars
                else: 
                    ci = t.chars
                if (ci.is_all_lower): 
                    word = word.lower()
                elif (ci.is_capital_upper): 
                    word = MiscHelper.convert_first_char_upper_and_other_lower(word)
            else: 
                word = t.get_source_text()
            print(word, end="", file=res)
            t = t.next0_; t0 = (None if t0 is None else t0.next0_)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def get_text_morph_var_by_case(txt : str, cas : 'MorphCase', plural_number : bool=False) -> str:
        """ Преобразовать строку к нужному падежу (и числу).
         Преобразуется только начало строки, содержащей в начале именную группу или персону
        
        Args:
            txt(str): исходная строка
            cas(MorphCase): падеж
            plural_number(bool): множественное число
        
        Returns:
            str: результат (в крайнем случае, вернёт исходную строку, если ничего не получилось)
        """
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        ar = ProcessorService.get_empty_processor().process(SourceOfAnalysis(txt), None, None)
        if (ar is None or ar.first_token is None): 
            return txt
        res = io.StringIO()
        t0 = ar.first_token
        npt = NounPhraseHelper.try_parse(ar.first_token, NounPhraseParseAttr.NO, 0)
        if (npt is not None): 
            t = npt.begin_token
            while t is not None and t.end_char <= npt.end_char: 
                is_noun = t.begin_char >= npt.noun.begin_char
                word = None
                if (isinstance(t, NumberToken)): 
                    word = t.get_source_text()
                elif (isinstance(t, TextToken)): 
                    for it in t.morph.items: 
                        wf = Utils.asObjectOrNull(it, MorphWordForm)
                        if (wf is None): 
                            continue
                        if (not npt.morph.case_.is_undefined): 
                            if (((npt.morph.case_) & wf.case_).is_undefined): 
                                continue
                        if (is_noun): 
                            if ((wf.class0_.is_noun or wf.class0_.is_personal_pronoun or wf.class0_.is_pronoun) or wf.class0_.is_proper): 
                                word = wf.normal_case
                                break
                        elif (wf.class0_.is_adjective or wf.class0_.is_pronoun or wf.class0_.is_personal_pronoun): 
                            word = wf.normal_case
                            break
                    if (word is None): 
                        word = (t).lemma
                    if (not t.chars.is_letter): 
                        pass
                    elif ((t.next0_ is not None and t.next0_.is_hiphen and t.is_value("ГЕНЕРАЛ", None)) or t.is_value("КАПИТАН", None)): 
                        pass
                    else: 
                        mbi = MorphBaseInfo._new563(npt.morph.gender, cas, MorphNumber.SINGULAR)
                        if (plural_number): 
                            mbi.number = MorphNumber.PLURAL
                        wcas = Morphology.get_wordform(word, mbi)
                        if (wcas is not None): 
                            word = wcas
                if (t.chars.is_all_lower): 
                    word = word.lower()
                elif (t.chars.is_capital_upper): 
                    word = MiscHelper.convert_first_char_upper_and_other_lower(word)
                if (t != ar.first_token and t.is_whitespace_before): 
                    print(' ', end="", file=res)
                print(word, end="", file=res)
                t0 = t.next0_
                t = t.next0_
        if (t0 == ar.first_token): 
            return txt
        if (t0 is not None): 
            if (t0.is_whitespace_before): 
                print(' ', end="", file=res)
            print(txt[t0.begin_char:], end="", file=res)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def get_text_morph_var_by_case_and_number_ex(str0_ : str, cas : 'MorphCase'=None, num : 'MorphNumber'=MorphNumber.SINGULAR, num_val : str=None) -> str:
        """ Корректировка числа и падежа строки
        
        Args:
            str0_(str): исходная строка, изменяется только первая именная группа
            cas(MorphCase): 
            num(MorphNumber): 
            num_val(str): 
        
        """
        from pullenti.ner.core.NounPhraseToken import NounPhraseToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        ar = ProcessorService.get_empty_processor().process(SourceOfAnalysis(str0_), None, None)
        if (ar is None or ar.first_token is None): 
            return str0_
        npt = NounPhraseHelper.try_parse(ar.first_token, NounPhraseParseAttr.PARSENUMERICASADJECTIVE, 0)
        if (npt is None and ((str0_ == "раз" or ar.first_token.get_morph_class_in_dictionary().is_proper_name))): 
            npt = NounPhraseToken(ar.first_token, ar.first_token)
            npt.noun = MetaToken(ar.first_token, ar.first_token)
        if (npt is None): 
            return str0_
        if (num_val is None and num == MorphNumber.UNDEFINED): 
            num = npt.morph.number
        if (cas is None or cas.is_undefined): 
            cas = MorphCase.NOMINATIVE
        if (not Utils.isNullOrEmpty(num_val) and num == MorphNumber.UNDEFINED): 
            if (cas is not None and not cas.is_nominative): 
                if (num_val == "1"): 
                    num = MorphNumber.SINGULAR
                else: 
                    num = MorphNumber.PLURAL
        adj_bi = MorphBaseInfo._new564((MorphClass.ADJECTIVE) | MorphClass.NOUN, cas, num, npt.morph.gender)
        noun_bi = MorphBaseInfo._new565(npt.noun.morph.class0_, cas, num)
        if (npt.noun.morph.class0_.is_noun): 
            noun_bi.class0_ = MorphClass.NOUN
        year = None
        pair = None
        if (not Utils.isNullOrEmpty(num_val) and num == MorphNumber.UNDEFINED): 
            ch = num_val[len(num_val) - 1]
            n = 0
            wrapn566 = RefOutArgWrapper(0)
            Utils.tryParseInt(num_val, wrapn566)
            n = wrapn566.value
            if (num_val == "1" or ((ch == '1' and n > 20 and ((n % 100)) != 11))): 
                adj_bi.number = noun_bi.number = MorphNumber.SINGULAR
                if (str0_ == "год" or str0_ == "раз"): 
                    year = str0_
                elif (str0_ == "пар" or str0_ == "пара"): 
                    pair = "пара"
            elif (((ch == '2' or ch == '3' or ch == '4')) and (((n < 10) or n > 20))): 
                noun_bi.number = MorphNumber.SINGULAR
                noun_bi.case_ = MorphCase.GENITIVE
                adj_bi.number = MorphNumber.PLURAL
                adj_bi.case_ = MorphCase.NOMINATIVE
                if (str0_ == "год"): 
                    year = ("года" if ((n < 10) or n > 20) else "лет")
                elif (str0_ == "раз"): 
                    year = ("раза" if ((n < 10) or n > 20) else "раз")
                elif (str0_ == "пар" or str0_ == "пара"): 
                    pair = "пары"
                elif (str0_ == "стул"): 
                    pair = "стула"
            else: 
                noun_bi.number = MorphNumber.PLURAL
                noun_bi.case_ = MorphCase.GENITIVE
                adj_bi.number = MorphNumber.PLURAL
                adj_bi.case_ = MorphCase.GENITIVE
                if (str0_ == "год"): 
                    year = ("год" if ch == '1' and n > 20 else "лет")
                elif (str0_ == "раз"): 
                    year = "раз"
                elif (str0_ == "пар" or str0_ == "пара"): 
                    pair = "пар"
                elif (str0_ == "стул"): 
                    year = "стульев"
        res = io.StringIO()
        for a in npt.adjectives: 
            norm = a.get_normal_case_text(MorphClass.ADJECTIVE, False, MorphGender.UNDEFINED, False)
            val = Morphology.get_wordform(norm, adj_bi)
            if (val is None): 
                val = a.get_source_text()
            elif (a.chars.is_all_lower): 
                val = val.lower()
            elif (a.chars.is_capital_upper): 
                val = MiscHelper.convert_first_char_upper_and_other_lower(val)
            if (res.tell() > 0): 
                print(' ', end="", file=res)
            print(val, end="", file=res)
        norm = npt.noun.get_normal_case_text(noun_bi.class0_, True, MorphGender.UNDEFINED, False)
        if (year is not None): 
            val = year
        elif (pair is not None): 
            val = pair
        elif (str0_ == "мин" or str0_ == "мес"): 
            val = str0_
        else: 
            val = Morphology.get_wordform(norm, noun_bi)
            if (val == "РЕБЕНОК" and noun_bi.number == MorphNumber.PLURAL): 
                val = Morphology.get_wordform("ДЕТИ", noun_bi)
            if (val == "ЧЕЛОВЕКОВ"): 
                val = "ЧЕЛОВЕК"
            elif (val == "МОРОВ"): 
                val = "МОРЕЙ"
            elif (val == "ПАРОВ"): 
                val = "ПАР"
            if (val is None): 
                val = npt.noun.get_source_text()
            elif (npt.noun.chars.is_all_lower): 
                val = val.lower()
            elif (npt.noun.chars.is_capital_upper): 
                val = MiscHelper.convert_first_char_upper_and_other_lower(val)
        if (res.tell() > 0): 
            print(' ', end="", file=res)
        print(val, end="", file=res)
        if (npt.end_token.next0_ is not None): 
            print(" ", end="", file=res)
            print(str0_[npt.end_token.next0_.begin_char:], end="", file=res)
        return Utils.toStringStringIO(res)