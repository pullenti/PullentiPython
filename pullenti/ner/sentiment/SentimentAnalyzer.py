# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.sentiment.SentimentKind import SentimentKind
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.Token import Token
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.Referent import Referent
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.business.internal.EpNerBusinessInternalResourceHelper import EpNerBusinessInternalResourceHelper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.sentiment.internal.MetaSentiment import MetaSentiment
from pullenti.ner.TextToken import TextToken
from pullenti.ner.sentiment.SentimentReferent import SentimentReferent
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
from pullenti.ner.core.MiscHelper import MiscHelper

class SentimentAnalyzer(Analyzer):
    """ Анализатор для сентиментов (эмоциональная оценка) """
    
    ANALYZER_NAME = "SENTIMENT"
    
    @property
    def name(self) -> str:
        return SentimentAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Сентиментный анализ"
    
    @property
    def description(self) -> str:
        return "Выделение тональных объектов"
    
    def clone(self) -> 'Analyzer':
        return SentimentAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaSentiment._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaSentiment.IMAGE_ID] = EpNerBusinessInternalResourceHelper.get_bytes("neutral.png")
        res[MetaSentiment.IMAGE_ID_GOOD] = EpNerBusinessInternalResourceHelper.get_bytes("good.png")
        res[MetaSentiment.IMAGE_ID_BAD] = EpNerBusinessInternalResourceHelper.get_bytes("bad.png")
        return res
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["ALL"]
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == SentimentReferent.OBJ_TYPENAME): 
            return SentimentReferent()
        return None
    
    @property
    def is_specific(self) -> bool:
        return True
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        return AnalyzerDataWithOntology()
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.get_analyzer_data(self)
        t = kit.first_token
        first_pass4004 = True
        while True:
            if first_pass4004: first_pass4004 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not ((isinstance(t, TextToken)))): 
                continue
            if (not t.chars.is_letter): 
                continue
            tok = SentimentAnalyzer.__m_termins.try_parse(t, TerminParseAttr.NO)
            if (tok is None): 
                continue
            coef = tok.termin.tag
            if (coef == 0): 
                continue
            t0 = t
            t1 = tok.end_token
            tt = t.previous
            first_pass4005 = True
            while True:
                if first_pass4005: first_pass4005 = False
                else: tt = tt.previous
                if (not (tt is not None)): break
                tok0 = SentimentAnalyzer.__m_termins.try_parse(tt, TerminParseAttr.NO)
                if (tok0 is not None): 
                    if ((tok0.termin.tag) == 0): 
                        coef *= 2
                        t0 = tt
                        continue
                    break
                if ((isinstance(tt, TextToken)) and (tt).term == "НЕ"): 
                    coef = (- coef)
                    t0 = tt
                    continue
                break
            tt = t1.next0_
            first_pass4006 = True
            while True:
                if first_pass4006: first_pass4006 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (not ((isinstance(tt, TextToken)))): 
                    break
                if (not tt.chars.is_letter): 
                    continue
                tok0 = SentimentAnalyzer.__m_termins.try_parse(tt, TerminParseAttr.NO)
                if (tok0 is None): 
                    break
                coef += (tok0.termin.tag)
                t1 = tok0.end_token
                tt = t1
            if (coef == 0): 
                continue
            sr = SentimentReferent()
            sr.kind = (SentimentKind.POSITIVE if coef > 0 else SentimentKind.NEGATIVE)
            sr.coef = (coef if coef > 0 else - coef)
            sr.spelling = MiscHelper.get_text_value(t0, t1, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
            sr = (Utils.asObjectOrNull(ad.register_referent(sr), SentimentReferent))
            rt = ReferentToken(sr, t0, t1)
            kit.embed_token(rt)
            t = (rt)
    
    __m_termins = None
    
    __m_inited = None
    
    @staticmethod
    def initialize() -> None:
        if (SentimentAnalyzer.__m_inited): 
            return
        SentimentAnalyzer.__m_inited = True
        MetaSentiment.initialize()
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        try: 
            for i in range(2):
                str0_ = EpNerBusinessInternalResourceHelper.get_string(("Positives.txt" if i == 0 else "Negatives.txt"))
                if (str0_ is None): 
                    continue
                for line0 in Utils.splitString(str0_, '\n', False): 
                    line = line0.strip()
                    if (Utils.isNullOrEmpty(line)): 
                        continue
                    coef = (1 if i == 0 else -1)
                    SentimentAnalyzer.__m_termins.add(Termin._new119(line, coef))
        except Exception as ex: 
            pass
        for s in ["ОЧЕНЬ", "СИЛЬНО"]: 
            SentimentAnalyzer.__m_termins.add(Termin._new119(s, 0))
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        ProcessorService.register_analyzer(SentimentAnalyzer())
    
    # static constructor for class SentimentAnalyzer
    @staticmethod
    def _static_ctor():
        SentimentAnalyzer.__m_termins = TerminCollection()

SentimentAnalyzer._static_ctor()