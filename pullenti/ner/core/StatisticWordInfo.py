# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


class StatisticWordInfo:
    """ Статистическая информация о токене - возвращается StatisticCollection.GetWordInfo
    Статистика токена
    """
    
    def __init__(self) -> None:
        self.normal = None;
        self.total_count = 0
        self.lower_count = 0
        self.upper_count = 0
        self.capital_count = 0
        self.male_verbs_after_count = 0
        self.female_verbs_after_count = 0
        self.has_before_person_attr = False
        self.not_capital_before_count = 0
        self.like_chars_before_words = None;
        self.like_chars_after_words = None;
    
    def __str__(self) -> str:
        return self.normal
    
    def add_before(self, w : 'StatisticWordInfo') -> None:
        if (self.like_chars_before_words is None): 
            self.like_chars_before_words = dict()
        if (not w in self.like_chars_before_words): 
            self.like_chars_before_words[w] = 1
        else: 
            self.like_chars_before_words[w] += 1
    
    def add_after(self, w : 'StatisticWordInfo') -> None:
        if (self.like_chars_after_words is None): 
            self.like_chars_after_words = dict()
        if (not w in self.like_chars_after_words): 
            self.like_chars_after_words[w] = 1
        else: 
            self.like_chars_after_words[w] += 1
    
    @staticmethod
    def _new539(_arg1 : str) -> 'StatisticWordInfo':
        res = StatisticWordInfo()
        res.normal = _arg1
        return res