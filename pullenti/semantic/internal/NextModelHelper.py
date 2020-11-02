# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.semantic.utils.QuestionType import QuestionType
from pullenti.morph.MorphCase import MorphCase
from pullenti.semantic.internal.NextModelItem import NextModelItem

class NextModelHelper:
    
    ITEMS = None
    
    @staticmethod
    def initialize() -> None:
        if (NextModelHelper.ITEMS is not None): 
            return
        NextModelHelper.ITEMS = list()
        NextModelHelper.ITEMS.append(NextModelItem("", MorphCase.NOMINATIVE))
        NextModelHelper.ITEMS.append(NextModelItem("", MorphCase.GENITIVE))
        NextModelHelper.ITEMS.append(NextModelItem("", MorphCase.DATIVE))
        NextModelHelper.ITEMS.append(NextModelItem("", MorphCase.ACCUSATIVE))
        NextModelHelper.ITEMS.append(NextModelItem("", MorphCase.INSTRUMENTAL))
        NextModelHelper.ITEMS.append(NextModelItem("", MorphCase.PREPOSITIONAL))
        for s in ["ИЗ", "ОТ", "С", "ИЗНУТРИ"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.GENITIVE, None, QuestionType.WHEREFROM))
        NextModelHelper.ITEMS.append(NextModelItem("В", MorphCase.ACCUSATIVE, None, QuestionType.WHERETO))
        NextModelHelper.ITEMS.append(NextModelItem("НА", MorphCase.ACCUSATIVE, None, QuestionType.WHERETO))
        NextModelHelper.ITEMS.append(NextModelItem("ПО", MorphCase.ACCUSATIVE, None, QuestionType.WHERETO))
        NextModelHelper.ITEMS.append(NextModelItem("К", MorphCase.DATIVE, None, QuestionType.WHERETO))
        NextModelHelper.ITEMS.append(NextModelItem("НАВСТРЕЧУ", MorphCase.DATIVE, None, QuestionType.WHERETO))
        NextModelHelper.ITEMS.append(NextModelItem("ДО", MorphCase.GENITIVE, None, QuestionType.WHERETO))
        for s in ["У", "ОКОЛО", "ВОКРУГ", "ВОЗЛЕ", "ВБЛИЗИ", "МИМО", "ПОЗАДИ", "ВПЕРЕДИ", "ВГЛУБЬ", "ВДОЛЬ", "ВНЕ", "КРОМЕ", "МЕЖДУ", "НАПРОТИВ", "ПОВЕРХ", "ПОДЛЕ", "ПОПЕРЕК", "ПОСЕРЕДИНЕ", "СВЕРХ", "СРЕДИ", "СНАРУЖИ", "ВНУТРИ"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.GENITIVE, None, QuestionType.WHERE))
        for s in ["ПАРАЛЛЕЛЬНО"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.DATIVE, None, QuestionType.WHERE))
        for s in ["СКВОЗЬ", "ЧЕРЕЗ", "ПОД"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.ACCUSATIVE, None, QuestionType.WHERE))
        for s in ["МЕЖДУ", "НАД", "ПОД", "ПЕРЕД", "ЗА"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.INSTRUMENTAL, None, QuestionType.WHERE))
        for s in ["В", "НА", "ПРИ"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.PREPOSITIONAL, None, QuestionType.WHERE))
        NextModelHelper.ITEMS.append(NextModelItem("ПРЕЖДЕ", MorphCase.GENITIVE, None, QuestionType.WHEN))
        NextModelHelper.ITEMS.append(NextModelItem("ПОСЛЕ", MorphCase.GENITIVE, None, QuestionType.WHEN))
        NextModelHelper.ITEMS.append(NextModelItem("НАКАНУНЕ", MorphCase.GENITIVE, None, QuestionType.WHEN))
        NextModelHelper.ITEMS.append(NextModelItem("СПУСТЯ", MorphCase.ACCUSATIVE, None, QuestionType.WHEN))
        for s in ["БЕЗ", "ДЛЯ", "РАДИ", "ИЗЗА", "ВВИДУ", "ВЗАМЕН", "ВМЕСТО", "ПРОТИВ", "СВЫШЕ", "ВСЛЕДСТВИЕ", "ПОМИМО", "ПОСРЕДСТВОМ"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.GENITIVE))
        for s in ["ПО", "ПОДОБНО", "СОГЛАСНО", "СООТВЕТСТВЕННО", "СОРАЗМЕРНО", "ВОПРЕКИ"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.DATIVE))
        for s in ["ПРО", "О", "ЗА", "ВКЛЮЧАЯ", "С"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.ACCUSATIVE))
        for s in ["С"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.INSTRUMENTAL))
        for s in ["О", "ПО"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.PREPOSITIONAL))
        i = 0
        while i < len(NextModelHelper.ITEMS): 
            j = 0
            while j < (len(NextModelHelper.ITEMS) - 1): 
                if (NextModelHelper.ITEMS[j].compare_to(NextModelHelper.ITEMS[j + 1]) > 0): 
                    it = NextModelHelper.ITEMS[j]
                    NextModelHelper.ITEMS[j] = NextModelHelper.ITEMS[j + 1]
                    NextModelHelper.ITEMS[j + 1] = it
                j += 1
            i += 1
        i = 0
        while i < len(NextModelHelper.ITEMS): 
            NextModelHelper.ITEMS[i].id0_ = (i + 1)
            i += 1