# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.ntopy.Utils import Utils
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphNumber import MorphNumber


class MorphToken:
    """ Элементы, на которые разбивается исходный текст (токены) """
    
    @property
    def length(self) -> int:
        """ Число символов (нормализованного фрагмента = Term.Length) """
        return (0 if self.term is None else len(self.term))
    
    def get_source_text(self, text : str) -> str:
        """ Извлечь фрагмент из исходного текста, соответствующий токену
        
        Args:
            text(str): полный исходный текст
        
        Returns:
            str: фрагмент
        """
        return text[self.begin_char : self.end_char + 1]
    
    @property
    def lemma(self) -> str:
        """ Лемма (вариант морфологической нормализации) """
        if (self.__m_lemma is not None): 
            return self.__m_lemma
        res = None
        if (self.word_forms is not None and len(self.word_forms) > 0): 
            if (len(self.word_forms) == 1): 
                res = (Utils.ifNotNull(self.word_forms[0].normal_full, self.word_forms[0].normal_case))
            if (res is None and not self.char_info.is_all_lower): 
                for m in self.word_forms: 
                    if (m.class0.is_proper_surname): 
                        s = Utils.ifNotNull(m.normal_full, Utils.ifNotNull(m.normal_case, ""))
                        if (LanguageHelper.ends_with_ex(s, "ОВ", "ЕВ", None, None)): 
                            res = s
                            break
                    elif (m.class0.is_proper_name and m.is_in_dictionary): 
                        return m.normal_case
            if (res is None): 
                best = None
                for m in self.word_forms: 
                    if (best is None): 
                        best = m
                    elif (self.__compare_forms(best, m) > 0): 
                        best = m
                res = (Utils.ifNotNull(best.normal_full, best.normal_case))
        if (res is not None): 
            if (LanguageHelper.ends_with_ex(res, "АНЫЙ", "ЕНЫЙ", None, None)): 
                res = (res[0 : (len(res) - 3)] + "ННЫЙ")
            elif (LanguageHelper.ends_with(res, "ЙСЯ")): 
                res = res[0 : (len(res) - 2)]
            elif (LanguageHelper.ends_with(res, "АНИЙ") and res == self.term): 
                for wf in self.word_forms: 
                    if (wf.is_in_dictionary): 
                        return res
                return res[0 : (len(res) - 1)] + "Е"
            return res
        return Utils.ifNotNull(self.term, "?")
    
    @lemma.setter
    def lemma(self, value) -> str:
        self.__m_lemma = value
        return value
    
    def __compare_forms(self, x : 'MorphWordForm', y : 'MorphWordForm') -> int:
        vx = Utils.ifNotNull(x.normal_full, x.normal_case)
        vy = Utils.ifNotNull(y.normal_full, y.normal_case)
        if (vx == vy): 
            return 0
        if (Utils.isNullOrEmpty(vx)): 
            return 1
        if (Utils.isNullOrEmpty(vy)): 
            return -1
        lastx = vx[len(vx) - 1]
        lasty = vy[len(vy) - 1]
        if (x.class0.is_proper_surname and not self.char_info.is_all_lower): 
            if (LanguageHelper.ends_with_ex(vx, "ОВ", "ЕВ", "ИН", None)): 
                if (not y.class0.is_proper_surname): 
                    return -1
        if (y.class0.is_proper_surname and not self.char_info.is_all_lower): 
            if (LanguageHelper.ends_with_ex(vy, "ОВ", "ЕВ", "ИН", None)): 
                if (not x.class0.is_proper_surname): 
                    return 1
                if (len(vx) > len(vy)): 
                    return -1
                if (len(vx) < len(vy)): 
                    return 1
                return 0
        if (x.class0 == y.class0): 
            if (x.class0.is_adjective): 
                if (lastx == 'Й' and lasty != 'Й'): 
                    return -1
                if (lastx != 'Й' and lasty == 'Й'): 
                    return 1
                if (not LanguageHelper.ends_with(vx, "ОЙ") and LanguageHelper.ends_with(vy, "ОЙ")): 
                    return -1
                if (LanguageHelper.ends_with(vx, "ОЙ") and not LanguageHelper.ends_with(vy, "ОЙ")): 
                    return 1
            if (x.class0.is_noun): 
                if (x.number == MorphNumber.SINGULAR and y.number == MorphNumber.PLURAL and len(vx) <= (len(vy) + 1)): 
                    return -1
                if (x.number == MorphNumber.PLURAL and y.number == MorphNumber.SINGULAR and len(vx) >= (len(vy) - 1)): 
                    return 1
            if (len(vx) < len(vy)): 
                return -1
            if (len(vx) > len(vy)): 
                return 1
            return 0
        if (x.class0.is_adverb): 
            return 1
        if (x.class0.is_noun and x.is_in_dictionary): 
            if (y.class0.is_adjective and y.is_in_dictionary): 
                if (not "к.ф." in y.misc.attrs): 
                    return 1
            return -1
        if (x.class0.is_adjective): 
            if (not x.is_in_dictionary and y.class0.is_noun and y.is_in_dictionary): 
                return 1
            return -1
        if (x.class0.is_verb): 
            if (y.class0.is_noun or y.class0.is_adjective or y.class0.is_preposition): 
                return 1
            return -1
        if (y.class0.is_adverb): 
            return -1
        if (y.class0.is_noun and y.is_in_dictionary): 
            return 1
        if (y.class0.is_adjective): 
            if (((x.class0.is_noun or x.class0.is_proper_secname)) and x.is_in_dictionary): 
                return -1
            if (x.class0.is_noun and not y.is_in_dictionary): 
                if (len(vx) < len(vy)): 
                    return -1
            return 1
        if (y.class0.is_verb): 
            if (x.class0.is_noun or x.class0.is_adjective or x.class0.is_preposition): 
                return -1
            if (x.class0.is_proper): 
                return -1
            return 1
        if (len(vx) < len(vy)): 
            return -1
        if (len(vx) > len(vy)): 
            return 1
        return 0
    
    @property
    def language(self) -> 'MorphLang':
        """ Язык(и) """
        from pullenti.morph.MorphLang import MorphLang
        if (self.__m_language is not None and self.__m_language != MorphLang.UNKNOWN): 
            return self.__m_language
        lang = MorphLang()
        if (self.word_forms is not None): 
            for wf in self.word_forms: 
                if (wf.language != MorphLang.UNKNOWN): 
                    lang |= wf.language
        return lang
    
    @language.setter
    def language(self, value) -> 'MorphLang':
        self.__m_language = value
        return value
    
    def __init__(self) -> None:
        self.begin_char = 0
        self.end_char = 0
        self.term = None
        self.__m_lemma = None
        self.tag = None
        self.__m_language = None
        self.word_forms = None
        self.char_info = None
        pass
    
    def __str__(self) -> str:
        if (Utils.isNullOrEmpty(self.term)): 
            return "Null"
        str0 = self.term
        if (self.char_info.is_all_lower): 
            str0 = str0.lower()
        elif (self.char_info.is_capital_upper and len(str0) > 0): 
            str0 = "{0}{1}".format(self.term[0], self.term[1 : ].lower())
        elif (self.char_info.is_last_lower): 
            str0 = "{0}{1}".format(self.term[0 : (len(self.term) - 1)], self.term[len(self.term) - 1 : ].lower())
        if (self.word_forms is None): 
            return str0
        res = Utils.newStringIO(str0)
        for l_ in self.word_forms: 
            print(", {0}".format(str(l_)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)