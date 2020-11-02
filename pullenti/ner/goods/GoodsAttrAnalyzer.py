# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import math
import threading

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.goods.GoodAttributeReferent import GoodAttributeReferent
from pullenti.ner.Token import Token
from pullenti.ner.Referent import Referent
from pullenti.ner.core.internal.PullentiNerCoreInternalResourceHelper import PullentiNerCoreInternalResourceHelper
from pullenti.ner.goods.internal.AttrMeta import AttrMeta
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
from pullenti.ner.goods.internal.GoodAttrToken import GoodAttrToken
from pullenti.ner.Analyzer import Analyzer

class GoodsAttrAnalyzer(Analyzer):
    """ Анализатор характеристик товаров. Используется, если нужно выделятть только отдельные характеристики, а не товар в целом.
    Если примеряется GoodsAnalyzer, то данный анализатор задействовать не нужно.
    Специфический анализатор, то есть нужно явно создавать процессор через функцию CreateSpecificProcessor,
    указав имя анализатора.
    Выделение происходит из небольшого фрагмента текста, содержащего только характеристики.
    Выделять из большого текста такие фрагменты - это не задача анализатора. """
    
    ANALYZER_NAME = "GOODSATTR"
    """ Имя анализатора ("GOODSATTR") """
    
    @property
    def name(self) -> str:
        return GoodsAttrAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Атрибуты товара"
    
    @property
    def description(self) -> str:
        return "Выделяет только атрибуты (из раздела Характеристик)"
    
    @property
    def is_specific(self) -> bool:
        return True
    
    def clone(self) -> 'Analyzer':
        return GoodsAttrAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [AttrMeta.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[AttrMeta.ATTR_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("bullet_ball_glass_grey.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == GoodAttributeReferent.OBJ_TYPENAME): 
            return GoodAttributeReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 100
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        return AnalyzerDataWithOntology()
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.get_analyzer_data(self)
        delta = 100000
        parts = math.floor((((len(kit.sofa.text) + delta) - 1)) / delta)
        if (parts == 0): 
            parts = 1
        cur = 0
        next_pos = 0
        t = kit.first_token
        first_pass3675 = True
        while True:
            if first_pass3675: first_pass3675 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.begin_char > next_pos): 
                next_pos += delta
                cur += 1
                if (not self._on_progress(cur, parts, kit)): 
                    break
            at = GoodAttrToken.try_parse(t, None, True, True)
            if (at is None): 
                continue
            attr = at._create_attr()
            if (attr is None): 
                t = at.end_token
                continue
            rt = ReferentToken(attr, at.begin_token, at.end_token)
            rt.referent = ad.register_referent(attr)
            kit.embed_token(rt)
            t = (rt)
    
    __m_initialized = False
    
    __m_lock = None
    
    @staticmethod
    def initialize() -> None:
        with GoodsAttrAnalyzer.__m_lock: 
            if (GoodsAttrAnalyzer.__m_initialized): 
                return
            GoodsAttrAnalyzer.__m_initialized = True
            ProcessorService.register_analyzer(GoodsAttrAnalyzer())
    
    # static constructor for class GoodsAttrAnalyzer
    @staticmethod
    def _static_ctor():
        GoodsAttrAnalyzer.__m_lock = threading.Lock()

GoodsAttrAnalyzer._static_ctor()