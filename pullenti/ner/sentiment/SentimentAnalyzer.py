# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
import io
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.business.internal.ResourceHelper import ResourceHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.sentiment.SentimentKind import SentimentKind
from pullenti.ner.core.GetTextAttr import GetTextAttr


class SentimentAnalyzer(Analyzer):
    """ Семантический анализатор выделения персон """
    
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
        from pullenti.ner.sentiment.internal.MetaSentiment import MetaSentiment
        return [MetaSentiment._global_meta]
    
    @property
    def images(self) -> typing.List['java.util.Map.Entry']:
        from pullenti.ner.sentiment.internal.MetaSentiment import MetaSentiment
        res = dict()
        res[MetaSentiment.IMAGE_ID] = ResourceHelper.get_bytes("neutral.png")
        res[MetaSentiment.IMAGE_ID_GOOD] = ResourceHelper.get_bytes("good.png")
        res[MetaSentiment.IMAGE_ID_BAD] = ResourceHelper.get_bytes("bad.png")
        return res
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["ALL"]
    
    def create_referent(self, type0 : str) -> 'Referent':
        from pullenti.ner.sentiment.SentimentReferent import SentimentReferent
        if (type0 == SentimentReferent.OBJ_TYPENAME): 
            return SentimentReferent()
        return None
    
    @property
    def is_specific(self) -> bool:
        return True
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
        return AnalyzerDataWithOntology()
    
    def process(self, kit : 'AnalysisKit') -> None:
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.sentiment.SentimentReferent import SentimentReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.ReferentToken import ReferentToken
        ad = kit.get_analyzer_data(self)
        t = kit.first_token
        first_pass2881 = True
        while True:
            if first_pass2881: first_pass2881 = False
            else: t = t.next0
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
            first_pass2882 = True
            while True:
                if first_pass2882: first_pass2882 = False
                else: tt = tt.previous
                if (not (tt is not None)): break
                tok0 = SentimentAnalyzer.__m_termins.try_parse(tt, TerminParseAttr.NO)
                if (tok0 is not None): 
                    if (tok0.termin.tag == 0): 
                        coef *= 2
                        t0 = tt
                        continue
                    break
                if (isinstance(tt, TextToken) and (tt if isinstance(tt, TextToken) else None).term == "НЕ"): 
                    coef = (- coef)
                    t0 = tt
                    continue
                break
            tt = t1.next0
            first_pass2883 = True
            while True:
                if first_pass2883: first_pass2883 = False
                else: tt = tt.next0
                if (not (tt is not None)): break
                if (not ((isinstance(tt, TextToken)))): 
                    break
                if (not tt.chars.is_letter): 
                    continue
                tok0 = SentimentAnalyzer.__m_termins.try_parse(tt, TerminParseAttr.NO)
                if (tok0 is None): 
                    break
                coef += tok0.termin.tag
                t1 = tok0.end_token
                tt = t1
            if (coef == 0): 
                continue
            sr = SentimentReferent()
            sr.kind = (SentimentKind.POSITIVE if coef > 0 else SentimentKind.NEGATIVE)
            sr.coef = (coef if coef > 0 else - coef)
            sr.spelling = MiscHelper.get_text_value(t0, t1, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
            sr = (ad.register_referent(sr) if isinstance(ad.register_referent(sr), SentimentReferent) else None)
            rt = ReferentToken(sr, t0, t1)
            kit.embed_token(rt)
            t = rt
    
    __m_termins = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.ProcessorService import ProcessorService
        from pullenti.ner.core.Termin import Termin
        ProcessorService.register_analyzer(SentimentAnalyzer())
        try: 
            for i in range(2):
                with io.StringIO(ResourceHelper.get_string(("Positives.txt" if i == 0 else "Negatives.txt"))) as tr: 
                    while True:
                        line = Utils.readLineIO(tr)
                        if (line is None): 
                            break
                        line = line.strip()
                        if (Utils.isNullOrEmpty(line)): 
                            continue
                        coef = (1 if i == 0 else -1)
                        SentimentAnalyzer.__m_termins.add(Termin._new118(line, coef))
        except Exception as ex: 
            pass
        for s in ["ОЧЕНЬ", "СИЛЬНО"]: 
            SentimentAnalyzer.__m_termins.add(Termin._new118(s, 0))
    
    # static constructor for class SentimentAnalyzer
    @staticmethod
    def _static_ctor():
        from pullenti.ner.core.TerminCollection import TerminCollection
        SentimentAnalyzer.__m_termins = TerminCollection()

SentimentAnalyzer._static_ctor()