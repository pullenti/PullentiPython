# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.PrepositionToken import PrepositionToken

class PrepositionHelper:
    """ Поддержка работы с предлогами
    Хелпер предлогов
    """
    
    @staticmethod
    def try_parse(t : 'Token') -> 'PrepositionToken':
        """ Попытаться выделить предлог с указанного токена
        
        Args:
            t(Token): начальный токен
        
        Returns:
            PrepositionToken: результат или null
        """
        if (not (isinstance(t, TextToken))): 
            return None
        tok = PrepositionHelper.__m_ontology.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            return PrepositionToken._new529(t, tok.end_token, tok.termin.canonic_text, tok.termin.tag)
        mc = t.get_morph_class_in_dictionary()
        if (not mc.is_preposition): 
            return None
        res = PrepositionToken(t, t)
        res.normal = t.get_normal_case_text(MorphClass.PREPOSITION, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
        res.next_case = LanguageHelper.get_case_after_preposition(res.normal)
        if ((t.next0_ is not None and t.next0_.is_hiphen and not t.is_whitespace_after) and (isinstance(t.next0_.next0_, TextToken)) and t.next0_.next0_.get_morph_class_in_dictionary().is_preposition): 
            res.end_token = t.next0_.next0_
        return res
    
    __m_ontology = None
    
    @staticmethod
    def _initialize() -> None:
        if (PrepositionHelper.__m_ontology is not None): 
            return
        PrepositionHelper.__m_ontology = TerminCollection()
        for s in ["близко от", "в виде", "в зависимости от", "в интересах", "в качестве", "в лице", "в отличие от", "в отношении", "в пандан", "в пользу", "в преддверии", "в продолжение", "в результате", "в роли", "в силу", "в случае", "в течение", "в целях", "в честь", "во имя", "вплоть до", "впредь до", "за вычетом", "за исключением", "за счет", "исходя из", "на благо", "на виду у", "на глазах у", "начиная с", "невзирая на", "недалеко от", "независимо от", "от имени", "от лица", "по линии", "по мере", "по поводу", "по причине", "по случаю", "поблизости от", "под видом", "под эгидой", "при помощи", "с ведома", "с помощью", "с точки зрения", "с целью"]: 
            PrepositionHelper.__m_ontology.add(Termin._new530(s.upper(), MorphLang.RU, True, MorphCase.GENITIVE))
        for s in ["вдоль по", "по направлению к", "применительно к", "смотря по", "судя по"]: 
            PrepositionHelper.__m_ontology.add(Termin._new530(s.upper(), MorphLang.RU, True, MorphCase.DATIVE))
        for s in ["несмотря на", "с прицелом на"]: 
            PrepositionHelper.__m_ontology.add(Termin._new530(s.upper(), MorphLang.RU, True, MorphCase.ACCUSATIVE))
        for s in ["во славу"]: 
            PrepositionHelper.__m_ontology.add(Termin._new530(s.upper(), MorphLang.RU, True, ((MorphCase.GENITIVE) | MorphCase.DATIVE)))
        for s in ["не считая"]: 
            PrepositionHelper.__m_ontology.add(Termin._new530(s.upper(), MorphLang.RU, True, ((MorphCase.GENITIVE) | MorphCase.ACCUSATIVE)))
        for s in ["в связи с", "в соответствии с", "вслед за", "лицом к лицу с", "наряду с", "по сравнению с", "рядом с", "следом за"]: 
            PrepositionHelper.__m_ontology.add(Termin._new530(s.upper(), MorphLang.RU, True, MorphCase.INSTRUMENTAL))