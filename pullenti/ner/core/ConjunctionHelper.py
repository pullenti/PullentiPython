# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.ConjunctionType import ConjunctionType
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.ConjunctionToken import ConjunctionToken

class ConjunctionHelper:
    """ Поддержка работы с союзами (запятая тоже считается союзом) """
    
    @staticmethod
    def try_parse(t : 'Token') -> 'ConjunctionToken':
        """ Попытаться выделить союз с указанного токена
        
        Args:
            t(Token): начальный токен
        
        Returns:
            ConjunctionToken: результат или null
        """
        if (not ((isinstance(t, TextToken)))): 
            return None
        if (t.is_comma): 
            ne = ConjunctionHelper.try_parse(t.next0_)
            if (ne is not None): 
                ne.begin_token = t
                return ne
            return ConjunctionToken._new565(t, t, ConjunctionType.COMMA, ",")
        tok = ConjunctionHelper.__m_ontology.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            if (t.is_value("ТО", None)): 
                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSEADVERBS, 0)
                if (npt is not None and npt.end_char > tok.end_token.end_char): 
                    return None
            return ConjunctionToken._new566(t, tok.end_token, tok.termin.canonic_text, Utils.valToEnum(tok.termin.tag, ConjunctionType))
        if (not t.get_morph_class_in_dictionary().is_conjunction): 
            return None
        if (t.is_and or t.is_or): 
            return ConjunctionToken._new566(t, t, (t).term, (ConjunctionType.OR if t.is_or else ConjunctionType.AND))
        term = (t).term
        if (term == "НИ"): 
            return ConjunctionToken._new566(t, t, term, ConjunctionType.NOT)
        if ((term == "А" or term == "НО" or term == "ЗАТО") or term == "ОДНАКО"): 
            return ConjunctionToken._new566(t, t, term, ConjunctionType.BUT)
        return None
    
    __m_ontology = None
    
    @staticmethod
    def _initialize() -> None:
        if (ConjunctionHelper.__m_ontology is not None): 
            return
        ConjunctionHelper.__m_ontology = TerminCollection()
        te = Termin._new135("ТАКЖЕ", ConjunctionType.AND)
        te.add_variant("А ТАКЖЕ", False)
        te.add_variant("КАК И", False)
        te.add_variant("ТАК И", False)
        ConjunctionHelper.__m_ontology.add(te)
        te = Termin._new135("ЕСЛИ", ConjunctionType.IF)
        ConjunctionHelper.__m_ontology.add(te)
        te = Termin._new135("ТО", ConjunctionType.THEN)
        ConjunctionHelper.__m_ontology.add(te)
        te = Termin._new135("ИНАЧЕ", ConjunctionType.ELSE)
        ConjunctionHelper.__m_ontology.add(te)