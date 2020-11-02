# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.ConjunctionToken import ConjunctionToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.ConjunctionType import ConjunctionType

class ConjunctionHelper:
    """ Поддержка работы с союзами (запятая тоже считается союзом). Союзы могут быть из нескольких слов,
    например, "а также и".
    Хелпер союзов
    """
    
    @staticmethod
    def try_parse(t : 'Token') -> 'ConjunctionToken':
        """ Попытаться выделить союз с указанного токена.
        
        Args:
            t(Token): начальный токен
        
        Returns:
            ConjunctionToken: результат или null
        """
        if (not (isinstance(t, TextToken))): 
            return None
        if (t.is_comma): 
            ne = ConjunctionHelper.try_parse(t.next0_)
            if (ne is not None): 
                ne.begin_token = t
                ne.is_simple = False
                return ne
            return ConjunctionToken._new478(t, t, ConjunctionType.COMMA, True, ",")
        tok = ConjunctionHelper.__m_ontology.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            if (t.is_value("ТО", None)): 
                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSEADVERBS, 0, None)
                if (npt is not None and npt.end_char > tok.end_token.end_char): 
                    return None
            if (tok.termin.tag2 is not None): 
                if (not (isinstance(tok.end_token, TextToken))): 
                    return None
                if (tok.end_token.get_morph_class_in_dictionary().is_verb): 
                    if (not tok.end_token.term.endswith("АЯ")): 
                        return None
            return ConjunctionToken._new479(t, tok.end_token, tok.termin.canonic_text, Utils.valToEnum(tok.termin.tag, ConjunctionType))
        if (not t.get_morph_class_in_dictionary().is_conjunction): 
            return None
        if (t.is_and or t.is_or): 
            res = ConjunctionToken._new480(t, t, t.term, True, (ConjunctionType.OR if t.is_or else ConjunctionType.AND))
            if (((t.next0_ is not None and t.next0_.is_char('(') and (isinstance(t.next0_.next0_, TextToken))) and t.next0_.next0_.is_or and t.next0_.next0_.next0_ is not None) and t.next0_.next0_.next0_.is_char(')')): 
                res.end_token = t.next0_.next0_.next0_
            elif ((t.next0_ is not None and t.next0_.is_char_of("\\/") and (isinstance(t.next0_.next0_, TextToken))) and t.next0_.next0_.is_or): 
                res.end_token = t.next0_.next0_
            return res
        term = t.term
        if (term == "НИ"): 
            return ConjunctionToken._new479(t, t, term, ConjunctionType.NOT)
        if ((term == "А" or term == "НО" or term == "ЗАТО") or term == "ОДНАКО"): 
            return ConjunctionToken._new479(t, t, term, ConjunctionType.BUT)
        return None
    
    __m_ontology = None
    
    @staticmethod
    def _initialize() -> None:
        if (ConjunctionHelper.__m_ontology is not None): 
            return
        ConjunctionHelper.__m_ontology = TerminCollection()
        te = Termin._new100("ТАКЖЕ", ConjunctionType.AND)
        te.add_variant("А ТАКЖЕ", False)
        te.add_variant("КАК И", False)
        te.add_variant("ТАК И", False)
        te.add_variant("А РАВНО", False)
        te.add_variant("А РАВНО И", False)
        ConjunctionHelper.__m_ontology.add(te)
        te = Termin._new100("ЕСЛИ", ConjunctionType.IF)
        ConjunctionHelper.__m_ontology.add(te)
        te = Termin._new100("ТО", ConjunctionType.THEN)
        ConjunctionHelper.__m_ontology.add(te)
        te = Termin._new100("ИНАЧЕ", ConjunctionType.ELSE)
        ConjunctionHelper.__m_ontology.add(te)
        te = Termin._new102("ИНАЧЕ КАК", ConjunctionType.EXCEPT, True)
        te.add_variant("ИНАЧЕ, КАК", False)
        te.add_variant("ЗА ИСКЛЮЧЕНИЕМ", False)
        te.add_variant("ИСКЛЮЧАЯ", False)
        te.add_abridge("КРОМЕ")
        te.add_abridge("КРОМЕ КАК")
        te.add_abridge("КРОМЕ, КАК")
        ConjunctionHelper.__m_ontology.add(te)
        te = Termin._new102("ВКЛЮЧАЯ", ConjunctionType.INCLUDE, True)
        te.add_variant("В ТОМ ЧИСЛЕ", False)
        ConjunctionHelper.__m_ontology.add(te)