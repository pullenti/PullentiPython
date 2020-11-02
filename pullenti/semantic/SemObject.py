# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.semantic.utils.DerivateGroup import DerivateGroup
from pullenti.semantic.SemLinkType import SemLinkType
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.semantic.SemObjectType import SemObjectType
from pullenti.ner.measure.MeasureKind import MeasureKind

class SemObject(object):
    """ Семантический объект """
    
    def __init__(self, graph_ : 'SemGraph') -> None:
        self.graph = None;
        self.morph = MorphWordForm()
        self.typ = SemObjectType.UNDEFINED
        self.quantity = None;
        self.concept = None;
        self.attrs = list()
        self.measure = MeasureKind.UNDEFINED
        self.not0_ = False
        self.tokens = list()
        self.links_from = list()
        self.links_to = list()
        self.tag = None;
        self.graph = graph_
    
    @property
    def begin_char(self) -> int:
        """ Начальная позиция первого токена """
        return (self.tokens[0].begin_char if len(self.tokens) > 0 else 0)
    
    @property
    def end_char(self) -> int:
        """ Последняя позиция последнего токена """
        return (self.tokens[len(self.tokens) - 1].end_char if len(self.tokens) > 0 else 0)
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.not0_): 
            print("НЕ ", end="", file=res)
        for a in self.attrs: 
            print("{0} ".format(str(a).lower()), end="", file=res, flush=True)
        if (self.quantity is not None): 
            print("{0} ".format(self.quantity), end="", file=res, flush=True)
        elif (self.morph.number == MorphNumber.PLURAL and self.typ == SemObjectType.NOUN): 
            print("* ".format(), end="", file=res, flush=True)
        print(Utils.ifNotNull(self.morph.normal_case, "?"), end="", file=res)
        return Utils.toStringStringIO(res)
    
    def compareTo(self, other : 'SemObject') -> int:
        if (len(self.tokens) == 0 or len(other.tokens) == 0): 
            return 0
        if (self.tokens[0].begin_char < other.tokens[0].begin_char): 
            return -1
        if (self.tokens[0].begin_char > other.tokens[0].begin_char): 
            return 1
        if (self.tokens[len(self.tokens) - 1].end_char < other.tokens[len(other.tokens) - 1].end_char): 
            return -1
        if (self.tokens[len(self.tokens) - 1].end_char > other.tokens[len(other.tokens) - 1].end_char): 
            return 1
        return 0
    
    def is_value(self, word : str, typ_ : 'SemObjectType'=SemObjectType.UNDEFINED) -> bool:
        """ Проверка значения
        
        Args:
            word(str): 
            typ_(SemObjectType): 
        
        """
        if (typ_ != SemObjectType.UNDEFINED): 
            if (typ_ != self.typ): 
                return False
        if (self.morph.normal_full == word or self.morph.normal_case == word): 
            return True
        gr = Utils.asObjectOrNull(self.concept, DerivateGroup)
        if (gr is not None): 
            if (gr.words[0].spelling == word): 
                return True
        return False
    
    def find_from_object(self, word : str, typ_ : 'SemLinkType'=SemLinkType.UNDEFINED, otyp : 'SemObjectType'=SemObjectType.UNDEFINED) -> 'SemObject':
        """ Найти объект, кторый связан с текущим исходящий связью (Source = this)
        
        Args:
            word(str): 
            typ_(SemLinkType): 
            otyp(SemObjectType): 
        
        """
        for li in self.links_from: 
            if (typ_ != SemLinkType.UNDEFINED and typ_ != li.typ): 
                continue
            if (li.target.is_value(word, otyp)): 
                return li.target
        return None
    
    def find_attr(self, typ_ : 'SemAttributeType') -> 'SemAttribute':
        """ Найти атрибут указанного типа
        
        Args:
            typ_(SemAttributeType): 
        
        """
        for a in self.attrs: 
            if (a.typ == typ_): 
                return a
        return None
    
    @staticmethod
    def _new2929(_arg1 : 'SemGraph', _arg2 : 'SemObjectType') -> 'SemObject':
        res = SemObject(_arg1)
        res.typ = _arg2
        return res