# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphCase import MorphCase
from pullenti.semantic.utils.QuestionType import QuestionType

class ControlModelQuestion:
    
    def __str__(self) -> str:
        return self.spelling
    
    def check(self, prep : str, cas : 'MorphCase') -> bool:
        if (self.is_abstract): 
            if (self.subquestions is not None): 
                for q in self.subquestions: 
                    if (q.check(prep, cas)): 
                        return True
            return False
        if (((cas) & self.case_).is_undefined): 
            return False
        if (prep is not None and self.preposition is not None): 
            return prep == self.preposition
        return Utils.isNullOrEmpty(prep) and Utils.isNullOrEmpty(self.preposition)
    
    def __init__(self, prep : str, cas : 'MorphCase', typ : 'QuestionType'=QuestionType.UNDEFINED) -> None:
        self.question = QuestionType.UNDEFINED
        self.preposition = None;
        self.case_ = None;
        self.spelling = None;
        self.spelling_ex = None;
        self.is_base = False
        self.is_abstract = False
        self.subquestions = None
        self.preposition = prep
        self.case_ = cas
        self.question = typ
        if (prep is not None): 
            if (cas.is_genitive): 
                self.spelling = "{0} чего".format(prep.lower())
            elif (cas.is_dative): 
                self.spelling = "{0} чему".format(prep.lower())
            elif (cas.is_accusative): 
                self.spelling = "{0} что".format(prep.lower())
            elif (cas.is_instrumental): 
                self.spelling = "{0} чем".format(prep.lower())
            elif (cas.is_prepositional): 
                self.spelling = "{0} чём".format(prep.lower())
            self.spelling_ex = self.spelling
            if (typ == QuestionType.WHEN): 
                self.spelling_ex = "{0}/когда".format(self.spelling)
            elif (typ == QuestionType.WHERE): 
                self.spelling_ex = "{0}/где".format(self.spelling)
            elif (typ == QuestionType.WHEREFROM): 
                self.spelling_ex = "{0}/откуда".format(self.spelling)
            elif (typ == QuestionType.WHERETO): 
                self.spelling_ex = "{0}/куда".format(self.spelling)
        elif (cas is not None): 
            if (cas.is_nominative): 
                self.spelling = "кто"
                self.spelling_ex = "кто/что"
            elif (cas.is_genitive): 
                self.spelling = "чего"
                self.spelling_ex = "кого/чего"
            elif (cas.is_dative): 
                self.spelling = "чему"
                self.spelling_ex = "кому/чему"
            elif (cas.is_accusative): 
                self.spelling = "что"
                self.spelling_ex = "кого/что"
            elif (cas.is_instrumental): 
                self.spelling = "чем"
                self.spelling_ex = "кем/чем"
        elif (typ == QuestionType.WHATTODO): 
            self.spelling_ex = "что делать"
            self.spelling = self.spelling_ex
        elif (typ == QuestionType.WHEN): 
            self.spelling_ex = "когда"
            self.spelling = self.spelling_ex
        elif (typ == QuestionType.WHERE): 
            self.spelling_ex = "где"
            self.spelling = self.spelling_ex
        elif (typ == QuestionType.WHEREFROM): 
            self.spelling_ex = "откуда"
            self.spelling = self.spelling_ex
        elif (typ == QuestionType.WHERETO): 
            self.spelling_ex = "куда"
            self.spelling = self.spelling_ex
    
    BASE_NOMINATIVE = None
    
    BASE_GENETIVE = None
    
    BASE_ACCUSATIVE = None
    
    BASE_INSTRUMENTAL = None
    
    BASE_DATIVE = None
    
    TO_DO = None
    
    ITEMS = None
    
    __m_hash_by_spel = None
    
    __m_hash_by_type = None
    
    @staticmethod
    def initialize() -> None:
        if (ControlModelQuestion.ITEMS is not None): 
            return
        ControlModelQuestion.ITEMS = list()
        for s in ["ИЗ", "ОТ", "С", "ИЗНУТРИ"]: 
            ControlModelQuestion.ITEMS.append(ControlModelQuestion(s, MorphCase.GENITIVE, QuestionType.WHEREFROM))
        ControlModelQuestion.ITEMS.append(ControlModelQuestion("В", MorphCase.ACCUSATIVE, QuestionType.WHERETO))
        ControlModelQuestion.ITEMS.append(ControlModelQuestion("НА", MorphCase.ACCUSATIVE, QuestionType.WHERETO))
        ControlModelQuestion.ITEMS.append(ControlModelQuestion("ПО", MorphCase.ACCUSATIVE, QuestionType.WHERETO))
        ControlModelQuestion.ITEMS.append(ControlModelQuestion("К", MorphCase.DATIVE, QuestionType.WHERETO))
        ControlModelQuestion.ITEMS.append(ControlModelQuestion("НАВСТРЕЧУ", MorphCase.DATIVE, QuestionType.WHERETO))
        ControlModelQuestion.ITEMS.append(ControlModelQuestion("ДО", MorphCase.GENITIVE, QuestionType.WHERETO))
        for s in ["У", "ОКОЛО", "ВОКРУГ", "ВОЗЛЕ", "ВБЛИЗИ", "МИМО", "ПОЗАДИ", "ВПЕРЕДИ", "ВГЛУБЬ", "ВДОЛЬ", "ВНЕ", "КРОМЕ", "МЕЖДУ", "НАПРОТИВ", "ПОВЕРХ", "ПОДЛЕ", "ПОПЕРЕК", "ПОСЕРЕДИНЕ", "СВЕРХ", "СРЕДИ", "СНАРУЖИ", "ВНУТРИ"]: 
            ControlModelQuestion.ITEMS.append(ControlModelQuestion(s, MorphCase.GENITIVE, QuestionType.WHERE))
        for s in ["ПАРАЛЛЕЛЬНО"]: 
            ControlModelQuestion.ITEMS.append(ControlModelQuestion(s, MorphCase.DATIVE, QuestionType.WHERE))
        for s in ["СКВОЗЬ", "ЧЕРЕЗ", "ПОД"]: 
            ControlModelQuestion.ITEMS.append(ControlModelQuestion(s, MorphCase.ACCUSATIVE, QuestionType.WHERE))
        for s in ["МЕЖДУ", "НАД", "ПОД", "ПЕРЕД", "ЗА"]: 
            ControlModelQuestion.ITEMS.append(ControlModelQuestion(s, MorphCase.INSTRUMENTAL, QuestionType.WHERE))
        for s in ["В", "НА", "ПРИ"]: 
            ControlModelQuestion.ITEMS.append(ControlModelQuestion(s, MorphCase.PREPOSITIONAL, QuestionType.WHERE))
        ControlModelQuestion.ITEMS.append(ControlModelQuestion("ПРЕЖДЕ", MorphCase.GENITIVE, QuestionType.WHEN))
        ControlModelQuestion.ITEMS.append(ControlModelQuestion("ПОСЛЕ", MorphCase.GENITIVE, QuestionType.WHEN))
        ControlModelQuestion.ITEMS.append(ControlModelQuestion("НАКАНУНЕ", MorphCase.GENITIVE, QuestionType.WHEN))
        ControlModelQuestion.ITEMS.append(ControlModelQuestion("СПУСТЯ", MorphCase.ACCUSATIVE, QuestionType.WHEN))
        for s in ["БЕЗ", "ДЛЯ", "РАДИ", "ИЗЗА", "ВВИДУ", "ВЗАМЕН", "ВМЕСТО", "ПРОТИВ", "СВЫШЕ", "ВСЛЕДСТВИЕ", "ПОМИМО", "ПОСРЕДСТВОМ", "ПУТЕМ"]: 
            ControlModelQuestion.ITEMS.append(ControlModelQuestion(s, MorphCase.GENITIVE))
        for s in ["ПО", "ПОДОБНО", "СОГЛАСНО", "СООТВЕТСТВЕННО", "СОРАЗМЕРНО", "ВОПРЕКИ"]: 
            ControlModelQuestion.ITEMS.append(ControlModelQuestion(s, MorphCase.DATIVE))
        for s in ["ПРО", "О", "ЗА", "ВКЛЮЧАЯ", "С"]: 
            ControlModelQuestion.ITEMS.append(ControlModelQuestion(s, MorphCase.ACCUSATIVE))
        for s in ["С"]: 
            ControlModelQuestion.ITEMS.append(ControlModelQuestion(s, MorphCase.INSTRUMENTAL))
        for s in ["О", "ПО"]: 
            ControlModelQuestion.ITEMS.append(ControlModelQuestion(s, MorphCase.PREPOSITIONAL))
        i = 0
        while i < len(ControlModelQuestion.ITEMS): 
            j = 0
            while j < (len(ControlModelQuestion.ITEMS) - 1): 
                if (ControlModelQuestion.ITEMS[j].__compare_to(ControlModelQuestion.ITEMS[j + 1]) > 0): 
                    it = ControlModelQuestion.ITEMS[j]
                    ControlModelQuestion.ITEMS[j] = ControlModelQuestion.ITEMS[j + 1]
                    ControlModelQuestion.ITEMS[j + 1] = it
                j += 1
            i += 1
        ControlModelQuestion.BASE_NOMINATIVE = ControlModelQuestion._new3032(None, MorphCase.NOMINATIVE, True)
        ControlModelQuestion.ITEMS.insert(0, ControlModelQuestion.BASE_NOMINATIVE)
        ControlModelQuestion.BASE_GENETIVE = ControlModelQuestion._new3032(None, MorphCase.GENITIVE, True)
        ControlModelQuestion.ITEMS.insert(1, ControlModelQuestion.BASE_GENETIVE)
        ControlModelQuestion.BASE_ACCUSATIVE = ControlModelQuestion._new3032(None, MorphCase.ACCUSATIVE, True)
        ControlModelQuestion.ITEMS.insert(2, ControlModelQuestion.BASE_ACCUSATIVE)
        ControlModelQuestion.BASE_INSTRUMENTAL = ControlModelQuestion._new3032(None, MorphCase.INSTRUMENTAL, True)
        ControlModelQuestion.ITEMS.insert(3, ControlModelQuestion.BASE_INSTRUMENTAL)
        ControlModelQuestion.BASE_DATIVE = ControlModelQuestion._new3032(None, MorphCase.DATIVE, True)
        ControlModelQuestion.ITEMS.insert(4, ControlModelQuestion.BASE_DATIVE)
        ControlModelQuestion.TO_DO = ControlModelQuestion(None, None, QuestionType.WHATTODO)
        ControlModelQuestion.ITEMS.insert(5, ControlModelQuestion.TO_DO)
        ControlModelQuestion.ITEMS.insert(6, ControlModelQuestion._new3037(None, None, QuestionType.WHERE, True))
        ControlModelQuestion.ITEMS.insert(7, ControlModelQuestion._new3037(None, None, QuestionType.WHERETO, True))
        ControlModelQuestion.ITEMS.insert(8, ControlModelQuestion._new3037(None, None, QuestionType.WHEREFROM, True))
        ControlModelQuestion.ITEMS.insert(9, ControlModelQuestion._new3037(None, None, QuestionType.WHEN, True))
        ControlModelQuestion.__m_hash_by_spel = dict()
        ControlModelQuestion.__m_hash_by_type = dict()
        for it in ControlModelQuestion.ITEMS: 
            ControlModelQuestion.__m_hash_by_spel[it.spelling] = it
            if (it.question != QuestionType.UNDEFINED): 
                li = [ ]
                wrapli3041 = RefOutArgWrapper(None)
                inoutres3042 = Utils.tryGetValue(ControlModelQuestion.__m_hash_by_type, it.question, wrapli3041)
                li = wrapli3041.value
                if (not inoutres3042): 
                    li = list()
                    ControlModelQuestion.__m_hash_by_type[it.question] = li
                li.append(it)
        for a in ControlModelQuestion.ITEMS: 
            if (a.is_abstract): 
                for q in ControlModelQuestion.ITEMS: 
                    if (not q.is_abstract and q.question == a.question): 
                        if (a.subquestions is None): 
                            a.subquestions = list()
                        a.subquestions.append(q)
    
    def __compare_to(self, other : 'ControlModelQuestion') -> int:
        i = Utils.compareStrings(self.preposition, other.preposition, False)
        if (i != 0): 
            return i
        if (self.__cas_rank() < other.__cas_rank()): 
            return -1
        if (self.__cas_rank() > other.__cas_rank()): 
            return 1
        return 0
    
    def __cas_rank(self) -> int:
        if (self.case_.is_genitive): 
            return 1
        if (self.case_.is_dative): 
            return 2
        if (self.case_.is_accusative): 
            return 3
        if (self.case_.is_instrumental): 
            return 4
        if (self.case_.is_prepositional): 
            return 5
        return 0
    
    @staticmethod
    def find_by_spel(spel : str) -> 'ControlModelQuestion':
        wrapres3043 = RefOutArgWrapper(None)
        inoutres3044 = Utils.tryGetValue(ControlModelQuestion.__m_hash_by_spel, spel, wrapres3043)
        res = wrapres3043.value
        if (not inoutres3044): 
            return None
        return res
    
    @staticmethod
    def find_by_prep_case(prep : str, cas : 'MorphCase') -> 'ControlModelQuestion':
        if (Utils.isNullOrEmpty(prep)): 
            prep = (None)
        for it in ControlModelQuestion.ITEMS: 
            if (it.preposition == prep and it.case_ == cas): 
                return it
        return None
    
    @staticmethod
    def find_by_type(ty : 'QuestionType') -> 'ControlModelQuestion':
        for it in ControlModelQuestion.ITEMS: 
            if (it.question == ty): 
                return it
        return None
    
    @staticmethod
    def find_list_by_type(ty : 'QuestionType') -> typing.List['ControlModelQuestion']:
        if (ty in ControlModelQuestion.__m_hash_by_type): 
            return ControlModelQuestion.__m_hash_by_type[ty]
        return None
    
    @staticmethod
    def _new3032(_arg1 : str, _arg2 : 'MorphCase', _arg3 : bool) -> 'ControlModelQuestion':
        res = ControlModelQuestion(_arg1, _arg2)
        res.is_base = _arg3
        return res
    
    @staticmethod
    def _new3037(_arg1 : str, _arg2 : 'MorphCase', _arg3 : 'QuestionType', _arg4 : bool) -> 'ControlModelQuestion':
        res = ControlModelQuestion(_arg1, _arg2, _arg3)
        res.is_abstract = _arg4
        return res