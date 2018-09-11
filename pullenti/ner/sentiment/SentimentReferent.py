# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.Referent import Referent
from pullenti.ner.sentiment.SentimentKind import SentimentKind
from pullenti.ner.core.IntOntologyItem import IntOntologyItem


class SentimentReferent(Referent):
    """ Фрагмент, соответсвующий сентиментной оценке """
    
    def __init__(self) -> None:
        from pullenti.ner.sentiment.internal.MetaSentiment import MetaSentiment
        super().__init__(SentimentReferent.OBJ_TYPENAME)
        self.instance_of = MetaSentiment._global_meta
    
    OBJ_TYPENAME = "SENTIMENT"
    
    ATTR_KIND = "KIND"
    
    ATTR_COEF = "COEF"
    
    ATTR_REF = "REF"
    
    ATTR_SPELLING = "SPELLING"
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        from pullenti.ner.sentiment.internal.MetaSentiment import MetaSentiment
        res = io.StringIO()
        print(MetaSentiment.FTYP.convert_inner_value_to_outer_value(self.get_string_value(SentimentReferent.ATTR_KIND), lang), end="", file=res)
        print(" {0}".format(Utils.ifNotNull(self.spelling, "")), end="", file=res, flush=True)
        if (self.coef > 0): 
            print(" (coef={0})".format(self.coef), end="", file=res, flush=True)
        r = self.get_value(SentimentReferent.ATTR_REF)
        if (r is not None and not short_variant): 
            print(" -> {0}".format(r), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def kind(self) -> 'SentimentKind':
        s = self.get_string_value(SentimentReferent.ATTR_KIND)
        if (s is None): 
            return SentimentKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, SentimentKind)
            if (isinstance(res, SentimentKind)): 
                return Utils.valToEnum(res, SentimentKind)
        except Exception as ex2475: 
            pass
        return SentimentKind.UNDEFINED
    
    @kind.setter
    def kind(self, value) -> 'SentimentKind':
        if (value != SentimentKind.UNDEFINED): 
            self.add_slot(SentimentReferent.ATTR_KIND, Utils.enumToString(value), True, 0)
        return value
    
    @property
    def spelling(self) -> str:
        return self.get_string_value(SentimentReferent.ATTR_SPELLING)
    
    @spelling.setter
    def spelling(self, value) -> str:
        self.add_slot(SentimentReferent.ATTR_SPELLING, value, True, 0)
        return value
    
    @property
    def coef(self) -> int:
        val = self.get_string_value(SentimentReferent.ATTR_COEF)
        if (val is None): 
            return 0
        inoutarg2476 = RefOutArgWrapper(0)
        inoutres2477 = Utils.tryParseInt(val, inoutarg2476)
        i = inoutarg2476.value
        if (not inoutres2477): 
            return 0
        return i
    
    @coef.setter
    def coef(self, value) -> int:
        self.add_slot(SentimentReferent.ATTR_COEF, str(value), True, 0)
        return value
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        sr = (obj if isinstance(obj, SentimentReferent) else None)
        if (sr is None): 
            return False
        if (sr.kind != self.kind): 
            return False
        if (sr.spelling != self.spelling): 
            return False
        return True
    
    def can_be_general_for(self, obj : 'Referent') -> bool:
        return False
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        from pullenti.ner.core.Termin import Termin
        oi = IntOntologyItem(self)
        oi.termins.append(Termin(self.spelling))
        return oi