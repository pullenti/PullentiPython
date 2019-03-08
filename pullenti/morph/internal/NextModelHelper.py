# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.internal.NextModelQuestion import NextModelQuestion
from pullenti.morph.internal.NextModelItem import NextModelItem
from pullenti.morph.MorphCase import MorphCase

class NextModelHelper:
    
    ITEMS = None
    
    __m_hash_by_spel = None
    
    @staticmethod
    def initialize() -> None:
        if (NextModelHelper.ITEMS is not None): 
            return
        NextModelHelper.ITEMS = list()
        NextModelHelper.ITEMS.append(NextModelItem("", MorphCase.GENITIVE))
        NextModelHelper.ITEMS.append(NextModelItem("", MorphCase.DATIVE))
        NextModelHelper.ITEMS.append(NextModelItem("", MorphCase.ACCUSATIVE))
        NextModelHelper.ITEMS.append(NextModelItem("", MorphCase.INSTRUMENTAL))
        NextModelHelper.ITEMS.append(NextModelItem("", MorphCase.PREPOSITIONAL))
        for s in ["ИЗ", "ОТ", "С", "ИЗНУТРИ"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.GENITIVE, None, NextModelQuestion.WHEREFROM))
        NextModelHelper.ITEMS.append(NextModelItem("В", MorphCase.ACCUSATIVE, None, NextModelQuestion.WHERETO))
        NextModelHelper.ITEMS.append(NextModelItem("НА", MorphCase.ACCUSATIVE, None, NextModelQuestion.WHERETO))
        NextModelHelper.ITEMS.append(NextModelItem("ПО", MorphCase.ACCUSATIVE, None, NextModelQuestion.WHERETO))
        NextModelHelper.ITEMS.append(NextModelItem("К", MorphCase.DATIVE, None, NextModelQuestion.WHERETO))
        NextModelHelper.ITEMS.append(NextModelItem("НАВСТРЕЧУ", MorphCase.DATIVE, None, NextModelQuestion.WHERETO))
        NextModelHelper.ITEMS.append(NextModelItem("ДО", MorphCase.GENITIVE, None, NextModelQuestion.WHERETO))
        for s in ["У", "ОКОЛО", "ВОКРУГ", "ВОЗЛЕ", "ВБЛИЗИ", "МИМО", "ПОЗАДИ", "ВПЕРЕДИ", "ВГЛУБЬ", "ВДОЛЬ", "ВНЕ", "КРОМЕ", "МЕЖДУ", "НАПРОТИВ", "ПОВЕРХ", "ПОДЛЕ", "ПОПЕРЕК", "ПОСЕРЕДИНЕ", "СВЕРХ", "СРЕДИ", "СНАРУЖИ", "ВНУТРИ"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.GENITIVE, None, NextModelQuestion.WHERE))
        for s in ["ПАРАЛЛЕЛЬНО"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.DATIVE, None, NextModelQuestion.WHERE))
        for s in ["СКВОЗЬ", "ЧЕРЕЗ", "ПОД"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.ACCUSATIVE, None, NextModelQuestion.WHERE))
        for s in ["МЕЖДУ", "НАД", "ПОД", "ПЕРЕД", "ЗА"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.INSTRUMENTAL, None, NextModelQuestion.WHERE))
        for s in ["В", "НА", "ПРИ"]: 
            NextModelHelper.ITEMS.append(NextModelItem(s, MorphCase.PREPOSITIONAL, None, NextModelQuestion.WHERE))
        NextModelHelper.ITEMS.append(NextModelItem("ПРЕЖДЕ", MorphCase.GENITIVE, None, NextModelQuestion.WHEN))
        NextModelHelper.ITEMS.append(NextModelItem("ПОСЛЕ", MorphCase.GENITIVE, None, NextModelQuestion.WHEN))
        NextModelHelper.ITEMS.append(NextModelItem("НАКАНУНЕ", MorphCase.GENITIVE, None, NextModelQuestion.WHEN))
        NextModelHelper.ITEMS.append(NextModelItem("СПУСТЯ", MorphCase.ACCUSATIVE, None, NextModelQuestion.WHEN))
        for s in ["БЕЗ", "ДЛЯ", "РАДИ", "ИЗЗА", "ВВИДУ", "ВЗАМЕН", "ВМЕСТО", "ПРОТИВ", "СВЫШЕ", "ВСЛЕДСТВИЕ", "ПОМИМО"]: 
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
                if (NextModelHelper.ITEMS[j].compareTo(NextModelHelper.ITEMS[j + 1]) > 0): 
                    it = NextModelHelper.ITEMS[j]
                    NextModelHelper.ITEMS[j] = NextModelHelper.ITEMS[j + 1]
                    NextModelHelper.ITEMS[j + 1] = it
                j += 1
            i += 1
        NextModelHelper.__m_hash_by_spel = dict()
        for it in NextModelHelper.ITEMS: 
            NextModelHelper.__m_hash_by_spel[it.spelling] = it
    
    @staticmethod
    def find_by_spel(spel : str) -> 'NextModelItem':
        wrapres39 = RefOutArgWrapper(None)
        inoutres40 = Utils.tryGetValue(NextModelHelper.__m_hash_by_spel, spel, wrapres39)
        res = wrapres39.value
        if (not inoutres40): 
            return None
        return res