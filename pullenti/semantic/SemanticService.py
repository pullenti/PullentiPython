# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.money.MoneyAnalyzer import MoneyAnalyzer
from pullenti.semantic.SemProcessParams import SemProcessParams
from pullenti.semantic.internal.AlgoParams import AlgoParams
from pullenti.semantic.internal.DelimToken import DelimToken
from pullenti.semantic.internal.AdverbToken import AdverbToken
from pullenti.ner.measure.MeasureAnalyzer import MeasureAnalyzer

class SemanticService:
    """ Сервис семантического анализа. Основная концепция изложена в документе Pullenti.Semantic.
    В реальных проектах не использовался, слабо отлажен, но ведется доработка данной функциональности.
    
    Сервис семантики
    """
    
    VERSION = "0.2"
    """ Версия семантики """
    
    @staticmethod
    def initialize() -> None:
        """ Если собираетесь использовать семантику, то необходимо вызывать в самом начале и только один раз
        (после инициализации ProcessorService.Initialize). Если вызвали Sdk.Initialize(), то там семантика инициализуется,
        и эту функцию вызывать уже не надо.
        Отметим, что для NER семантический анализ не используется. """
        if (SemanticService.__m_inited): 
            return
        SemanticService.__m_inited = True
        DelimToken.initialize()
        AdverbToken.initialize()
        MeasureAnalyzer.initialize()
        MoneyAnalyzer.initialize()
    
    __m_inited = None
    
    @staticmethod
    def process(ar : 'AnalysisResult', pars : 'SemProcessParams'=None) -> 'SemDocument':
        """ Сделать семантический анализ поверх результатов морфологического анализа и NER
        
        Args:
            ar(AnalysisResult): результат обработки Processor
            pars(SemProcessParams): дополнительные параметры
        
        Returns:
            SemDocument: результат анализа текста
        
        """
        from pullenti.semantic.internal.AnalyzeHelper import AnalyzeHelper
        return AnalyzeHelper.process(ar, Utils.ifNotNull(pars, SemProcessParams()))
    
    PARAMS = None
    
    # static constructor for class SemanticService
    @staticmethod
    def _static_ctor():
        SemanticService.PARAMS = AlgoParams()

SemanticService._static_ctor()