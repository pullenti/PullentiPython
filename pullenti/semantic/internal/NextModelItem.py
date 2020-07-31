# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphCase import MorphCase
from pullenti.semantic.utils.QuestionType import QuestionType

class NextModelItem(object):
    
    def __init__(self, prep : str, cas : 'MorphCase', spel : str=None, typ : 'QuestionType'=QuestionType.UNDEFINED) -> None:
        self.preposition = None;
        self.case_ = None;
        self.spelling = None;
        self.question = QuestionType.UNDEFINED
        self.preposition = prep
        self.case_ = cas
        self.spelling = spel
        self.question = typ
        if (spel is not None): 
            return
        if (not Utils.isNullOrEmpty(prep)): 
            if (cas.is_genitive): 
                spel = "{0} чего".format(prep.lower())
            elif (cas.is_dative): 
                spel = "{0} чему".format(prep.lower())
            elif (cas.is_accusative): 
                spel = "{0} что".format(prep.lower())
            elif (cas.is_instrumental): 
                spel = "{0} чем".format(prep.lower())
            elif (cas.is_prepositional): 
                spel = "{0} чём".format(prep.lower())
        else: 
            self.preposition = ""
            if (cas.is_nominative): 
                spel = "кто"
            elif (cas.is_genitive): 
                spel = "чего"
            elif (cas.is_dative): 
                spel = "чему"
            elif (cas.is_accusative): 
                spel = "что"
            elif (cas.is_instrumental): 
                spel = "чем"
            elif (cas.is_prepositional): 
                spel = "чём"
        self.spelling = spel
    
    def __str__(self) -> str:
        return self.spelling
    
    def compareTo(self, other : 'NextModelItem') -> int:
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
    
    def check(self, prep : str, cas : 'MorphCase') -> bool:
        if (((cas) & self.case_).is_undefined): 
            return False
        if (prep is not None and self.preposition is not None): 
            return prep == self.preposition
        return Utils.isNullOrEmpty(prep) and Utils.isNullOrEmpty(self.preposition)