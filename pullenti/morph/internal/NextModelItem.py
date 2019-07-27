# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.morph.internal.NextModelQuestion import NextModelQuestion

class NextModelItem(object):
    
    def __init__(self, prep : str, cas : 'MorphCase', spel : str=None, typ : 'NextModelQuestion'=NextModelQuestion.UNDEFINED) -> None:
        self.preposition = None;
        self.case_ = None;
        self.spelling = None;
        self.question = NextModelQuestion.UNDEFINED
        self.preposition = prep
        self.case_ = cas
        self.spelling = spel
        self.question = typ
        if (spel is not None): 
            return
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
        self.spelling = spel.strip()
    
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