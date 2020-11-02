# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphCase import MorphCase
from pullenti.semantic.utils.QuestionType import QuestionType

class ControlModelQuestion:
    """ Вопрос модели управления """
    
    def __str__(self) -> str:
        return self.spelling
    
    def check(self, prep : str, cas : 'MorphCase') -> bool:
        """ Проверить на соответствие вопросу предлога с падежом
        
        Args:
            prep(str): предлог
            cas(MorphCase): падеж
        
        Returns:
            bool: да-нет
        """
        if (self.is_abstract): 
            for it in ControlModelQuestion.ITEMS: 
                if (not it.is_abstract and it.question == self.question): 
                    if (it.check(prep, cas)): 
                        return True
            return False
        if (((cas) & self.case_).is_undefined): 
            if (self.preposition == "В" and prep == self.preposition): 
                if (self.case_.is_accusative): 
                    if (cas.is_undefined or cas.is_nominative): 
                        return True
            return False
        if (prep is not None and self.preposition is not None): 
            if (prep == self.preposition): 
                return True
            if (self.preposition == "ОТ" and prep == "ОТ ИМЕНИ"): 
                return True
        return Utils.isNullOrEmpty(prep) and Utils.isNullOrEmpty(self.preposition)
    
    def check_abstract(self, prep : str, cas : 'MorphCase') -> 'ControlModelQuestion':
        for it in ControlModelQuestion.ITEMS: 
            if (not it.is_abstract and it.question == self.question): 
                if (it.check(prep, cas)): 
                    return it
        return None
    
    def __init__(self, prep : str, cas : 'MorphCase', typ : 'QuestionType'=QuestionType.UNDEFINED) -> None:
        self.question = QuestionType.UNDEFINED
        self.preposition = None;
        self.case_ = None;
        self.spelling = None;
        self.spelling_ex = None;
        self.id0_ = 0
        self.is_base = False
        self.is_abstract = False
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
            self.spelling = "что делать"
            self.spelling_ex = "что делать"
        elif (typ == QuestionType.WHEN): 
            self.spelling = "когда"
            self.spelling_ex = "когда"
        elif (typ == QuestionType.WHERE): 
            self.spelling = "где"
            self.spelling_ex = "где"
        elif (typ == QuestionType.WHEREFROM): 
            self.spelling = "откуда"
            self.spelling_ex = "откуда"
        elif (typ == QuestionType.WHERETO): 
            self.spelling = "куда"
            self.spelling_ex = "куда"
    
    @staticmethod
    def get_base_nominative() -> 'ControlModelQuestion':
        """ Вопрос "кто-что" """
        return ControlModelQuestion.ITEMS[ControlModelQuestion.__m_base_nominative_ind]
    
    __m_base_nominative_ind = None
    
    @staticmethod
    def get_base_genetive() -> 'ControlModelQuestion':
        """ Вопрос "кого-чего" """
        return ControlModelQuestion.ITEMS[ControlModelQuestion.__m_base_genetive_ind]
    
    __m_base_genetive_ind = None
    
    @staticmethod
    def get_base_accusative() -> 'ControlModelQuestion':
        """ Вопрос "кого-что" """
        return ControlModelQuestion.ITEMS[ControlModelQuestion.__m_base_accusative_ind]
    
    __m_base_accusative_ind = None
    
    @staticmethod
    def get_base_instrumental() -> 'ControlModelQuestion':
        """ Вопрос "кем-чем" """
        return ControlModelQuestion.ITEMS[ControlModelQuestion.__m_base_instrumental_ind]
    
    __m_base_instrumental_ind = None
    
    @staticmethod
    def get_base_dative() -> 'ControlModelQuestion':
        """ Вопрос "кому-чему" """
        return ControlModelQuestion.ITEMS[ControlModelQuestion.__m_base_dative_ind]
    
    __m_base_dative_ind = None
    
    @staticmethod
    def get_to_do() -> 'ControlModelQuestion':
        """ Вопрос "что делать" """
        return ControlModelQuestion.ITEMS[ControlModelQuestion.__m_base_to_do_ind]
    
    __m_base_to_do_ind = None
    
    ITEMS = None
    """ Список всех вопросов ControlModelQuestion """
    
    __m_hash_by_spel = None
    
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
        ControlModelQuestion.__m_base_nominative_ind = 0
        ControlModelQuestion.ITEMS.insert(ControlModelQuestion.__m_base_nominative_ind, ControlModelQuestion._new2953(None, MorphCase.NOMINATIVE, True))
        ControlModelQuestion.__m_base_genetive_ind = 1
        ControlModelQuestion.ITEMS.insert(ControlModelQuestion.__m_base_genetive_ind, ControlModelQuestion._new2953(None, MorphCase.GENITIVE, True))
        ControlModelQuestion.__m_base_accusative_ind = 2
        ControlModelQuestion.ITEMS.insert(ControlModelQuestion.__m_base_accusative_ind, ControlModelQuestion._new2953(None, MorphCase.ACCUSATIVE, True))
        ControlModelQuestion.__m_base_instrumental_ind = 3
        ControlModelQuestion.ITEMS.insert(ControlModelQuestion.__m_base_instrumental_ind, ControlModelQuestion._new2953(None, MorphCase.INSTRUMENTAL, True))
        ControlModelQuestion.__m_base_dative_ind = 4
        ControlModelQuestion.ITEMS.insert(ControlModelQuestion.__m_base_dative_ind, ControlModelQuestion._new2953(None, MorphCase.DATIVE, True))
        ControlModelQuestion.__m_base_to_do_ind = 5
        ControlModelQuestion.ITEMS.insert(ControlModelQuestion.__m_base_to_do_ind, ControlModelQuestion(None, None, QuestionType.WHATTODO))
        ControlModelQuestion.ITEMS.insert(6, ControlModelQuestion._new2958(None, None, QuestionType.WHERE, True))
        ControlModelQuestion.ITEMS.insert(7, ControlModelQuestion._new2958(None, None, QuestionType.WHERETO, True))
        ControlModelQuestion.ITEMS.insert(8, ControlModelQuestion._new2958(None, None, QuestionType.WHEREFROM, True))
        ControlModelQuestion.ITEMS.insert(9, ControlModelQuestion._new2958(None, None, QuestionType.WHEN, True))
        ControlModelQuestion.__m_hash_by_spel = dict()
        i = 0
        while i < len(ControlModelQuestion.ITEMS): 
            it = ControlModelQuestion.ITEMS[i]
            it.id0_ = (i + 1)
            ControlModelQuestion.__m_hash_by_spel[it.spelling] = i
            i += 1
    
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
    def get_by_id(id0__ : int) -> 'ControlModelQuestion':
        if (id0__ >= 1 and id0__ <= len(ControlModelQuestion.ITEMS)): 
            return ControlModelQuestion.ITEMS[id0__ - 1]
        return None
    
    @staticmethod
    def find_by_spel(spel : str) -> 'ControlModelQuestion':
        wrapind2962 = RefOutArgWrapper(0)
        inoutres2963 = Utils.tryGetValue(ControlModelQuestion.__m_hash_by_spel, spel, wrapind2962)
        ind = wrapind2962.value
        if (not inoutres2963): 
            return None
        return ControlModelQuestion.ITEMS[ind]
    
    @staticmethod
    def _new2953(_arg1 : str, _arg2 : 'MorphCase', _arg3 : bool) -> 'ControlModelQuestion':
        res = ControlModelQuestion(_arg1, _arg2)
        res.is_base = _arg3
        return res
    
    @staticmethod
    def _new2958(_arg1 : str, _arg2 : 'MorphCase', _arg3 : 'QuestionType', _arg4 : bool) -> 'ControlModelQuestion':
        res = ControlModelQuestion(_arg1, _arg2, _arg3)
        res.is_abstract = _arg4
        return res