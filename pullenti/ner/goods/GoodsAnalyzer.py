# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import math
import threading
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.Token import Token
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.goods.GoodAttrType import GoodAttrType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.internal.PullentiNerCoreInternalResourceHelper import PullentiNerCoreInternalResourceHelper
from pullenti.ner.goods.internal.AttrMeta import AttrMeta
from pullenti.ner.goods.internal.GoodMeta import GoodMeta
from pullenti.ner.core.Termin import Termin
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
from pullenti.ner.goods.GoodAttributeReferent import GoodAttributeReferent
from pullenti.ner.goods.internal.GoodAttrToken import GoodAttrToken
from pullenti.ner.goods.GoodReferent import GoodReferent

class GoodsAnalyzer(Analyzer):
    """ Анализатор названий товаров (номенклатур) и выделение из них характеристик.
    Специфический анализатор, то есть нужно явно создавать процессор через функцию CreateSpecificProcessor,
    указав имя анализатора.
    Выделение происходит из небольшого фрагмента текста, содержащего только один товар и его характеристики.
    Выделять из большого текста такие фрагменты - это не задача анализатора.
    Примеры текстов: "Плед OXFORD Cashnere Touch Herringbone 1.5-сп с эффектом кашемира",
    "Имплантат размером 5 см х 5 см предназначен для реконструкции твердой мозговой оболочки. Изготовлен из биологически совместимого материала на коллагеновой основе.". """
    
    ANALYZER_NAME = "GOODS"
    """ Имя анализатора ("GOODS") """
    
    @property
    def name(self) -> str:
        return GoodsAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Товары и атрибуты"
    
    @property
    def description(self) -> str:
        return "Товары и их атрибуты"
    
    @property
    def is_specific(self) -> bool:
        """ Этот анализатор является специфическим (IsSpecific = true) """
        return True
    
    def clone(self) -> 'Analyzer':
        return GoodsAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [AttrMeta.GLOBAL_META, GoodMeta.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[AttrMeta.ATTR_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("bullet_ball_glass_grey.png")
        res[GoodMeta.IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("shoppingcart.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == GoodAttributeReferent.OBJ_TYPENAME): 
            return GoodAttributeReferent()
        if (type0_ == GoodReferent.OBJ_TYPENAME): 
            return GoodReferent()
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
        goods_ = list()
        t = kit.first_token
        first_pass3673 = True
        while True:
            if first_pass3673: first_pass3673 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not t.is_newline_before): 
                continue
            if (t.begin_char > next_pos): 
                next_pos += delta
                cur += 1
                if (not self._on_progress(cur, parts, kit)): 
                    break
            if (not t.chars.is_letter and t.next0_ is not None): 
                t = t.next0_
            rts = GoodAttrToken.try_parse_list(t)
            if (rts is None or len(rts) == 0): 
                continue
            good = GoodReferent()
            for rt in rts: 
                rt.referent = ad.register_referent(rt.referent)
                if (good.find_slot(GoodReferent.ATTR_ATTR, rt.referent, True) is None): 
                    good.add_slot(GoodReferent.ATTR_ATTR, rt.referent, False, 0)
                kit.embed_token(rt)
            goods_.append(good)
            rt0 = ReferentToken(good, rts[0], rts[len(rts) - 1])
            kit.embed_token(rt0)
            t = (rt0)
        for g in goods_: 
            ad.referents.append(g)
    
    def process_ontology_item(self, begin : 'Token') -> 'ReferentToken':
        if (begin is None): 
            return None
        ga = GoodAttributeReferent()
        if (begin.chars.is_latin_letter): 
            if (begin.is_value("KEYWORD", None)): 
                ga.typ = GoodAttrType.KEYWORD
                begin = begin.next0_
            elif (begin.is_value("CHARACTER", None)): 
                ga.typ = GoodAttrType.CHARACTER
                begin = begin.next0_
            elif (begin.is_value("PROPER", None)): 
                ga.typ = GoodAttrType.PROPER
                begin = begin.next0_
            elif (begin.is_value("MODEL", None)): 
                ga.typ = GoodAttrType.MODEL
                begin = begin.next0_
            if (begin is None): 
                return None
        res = ReferentToken(ga, begin, begin)
        t = begin
        first_pass3674 = True
        while True:
            if first_pass3674: first_pass3674 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_char(';')): 
                ga.add_slot(GoodAttributeReferent.ATTR_VALUE, MiscHelper.get_text_value(begin, t.previous, GetTextAttr.NO), False, 0)
                begin = t.next0_
                continue
            res.end_token = t
        if (res.end_char > begin.begin_char): 
            ga.add_slot(GoodAttributeReferent.ATTR_VALUE, MiscHelper.get_text_value(begin, res.end_token, GetTextAttr.NO), False, 0)
        if (ga.typ == GoodAttrType.UNDEFINED): 
            if (not begin.chars.is_all_lower): 
                ga.typ = GoodAttrType.PROPER
        return res
    
    __m_initialized = False
    
    __m_lock = None
    
    @staticmethod
    def initialize() -> None:
        with GoodsAnalyzer.__m_lock: 
            if (GoodsAnalyzer.__m_initialized): 
                return
            GoodsAnalyzer.__m_initialized = True
            AttrMeta.initialize()
            GoodMeta.initialize()
            try: 
                Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
                GoodAttrToken.initialize()
                Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
            except Exception as ex: 
                raise Utils.newException(ex.__str__(), ex)
            ProcessorService.register_analyzer(GoodsAnalyzer())
    
    # static constructor for class GoodsAnalyzer
    @staticmethod
    def _static_ctor():
        GoodsAnalyzer.__m_lock = threading.Lock()

GoodsAnalyzer._static_ctor()