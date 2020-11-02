# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.core.internal.TextsCompareType import TextsCompareType

class TextAnnotation:
    """ Аннотация слитного фрагмента текста (фрагмент вхождения сущности в текст)
    
    Аннотация
    """
    
    def __init__(self, begin : 'Token'=None, end : 'Token'=None, r : 'Referent'=None) -> None:
        self.sofa = None;
        self.begin_char = 0
        self.end_char = 0
        self.__m_occurence_of = None;
        self.essential_for_occurence = False
        self.tag = None;
        if (begin is not None): 
            self.sofa = begin.kit.sofa
            self.begin_char = begin.begin_char
        if (end is not None): 
            self.end_char = end.end_char
        self.occurence_of = r
    
    @property
    def occurence_of(self) -> 'Referent':
        """ Ссылка на сущность """
        return self.__m_occurence_of
    @occurence_of.setter
    def occurence_of(self, value) -> 'Referent':
        self.__m_occurence_of = value
        return value
    
    def __str__(self) -> str:
        if (self.sofa is None): 
            return "{0}:{1}".format(self.begin_char, self.end_char)
        return self.get_text()
    
    def get_text(self) -> str:
        """ Извлечь фрагмент исходного текста, соответствующий аннотации
        
        Returns:
            str: фрагмент текста
        """
        if (self.sofa is None or self.sofa.text is None): 
            return None
        return self.sofa.text[self.begin_char:self.begin_char+(self.end_char + 1) - self.begin_char]
    
    def _compare_with(self, loc : 'TextAnnotation') -> 'TextsCompareType':
        if (loc.sofa != self.sofa): 
            return TextsCompareType.NONCOMPARABLE
        return self._compare(loc.begin_char, loc.end_char)
    
    def _compare(self, pos : int, pos1 : int) -> 'TextsCompareType':
        if (self.end_char < pos): 
            return TextsCompareType.EARLY
        if (pos1 < self.begin_char): 
            return TextsCompareType.LATER
        if (self.begin_char == pos and self.end_char == pos1): 
            return TextsCompareType.EQUIVALENT
        if (self.begin_char >= pos and self.end_char <= pos1): 
            return TextsCompareType.IN
        if (pos >= self.begin_char and pos1 <= self.end_char): 
            return TextsCompareType.CONTAINS
        return TextsCompareType.INTERSECT
    
    def _merge(self, loc : 'TextAnnotation') -> None:
        if (loc.sofa != self.sofa): 
            return
        if (loc.begin_char < self.begin_char): 
            self.begin_char = loc.begin_char
        if (self.end_char < loc.end_char): 
            self.end_char = loc.end_char
        if (loc.essential_for_occurence): 
            self.essential_for_occurence = True
    
    @staticmethod
    def _new474(_arg1 : 'SourceOfAnalysis', _arg2 : int, _arg3 : int) -> 'TextAnnotation':
        res = TextAnnotation()
        res.sofa = _arg1
        res.begin_char = _arg2
        res.end_char = _arg3
        return res
    
    @staticmethod
    def _new714(_arg1 : 'SourceOfAnalysis', _arg2 : int, _arg3 : int, _arg4 : 'Referent') -> 'TextAnnotation':
        res = TextAnnotation()
        res.sofa = _arg1
        res.begin_char = _arg2
        res.end_char = _arg3
        res.occurence_of = _arg4
        return res
    
    @staticmethod
    def _new1590(_arg1 : int, _arg2 : int, _arg3 : 'Referent', _arg4 : 'SourceOfAnalysis') -> 'TextAnnotation':
        res = TextAnnotation()
        res.begin_char = _arg1
        res.end_char = _arg2
        res.occurence_of = _arg3
        res.sofa = _arg4
        return res
    
    @staticmethod
    def _new2857(_arg1 : int, _arg2 : int, _arg3 : 'SourceOfAnalysis') -> 'TextAnnotation':
        res = TextAnnotation()
        res.begin_char = _arg1
        res.end_char = _arg2
        res.sofa = _arg3
        return res
    
    @staticmethod
    def _new2859(_arg1 : 'SourceOfAnalysis', _arg2 : 'Referent') -> 'TextAnnotation':
        res = TextAnnotation()
        res.sofa = _arg1
        res.occurence_of = _arg2
        return res