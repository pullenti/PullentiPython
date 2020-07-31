﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import threading
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.measure.UnitReferent import UnitReferent
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.measure.MeasureReferent import MeasureReferent
from pullenti.ner.measure.internal.UnitsHelper import UnitsHelper
from pullenti.ner.measure.internal.UnitToken import UnitToken
from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
from pullenti.ner.Token import Token
from pullenti.ner.bank.internal.EpNerBankInternalResourceHelper import EpNerBankInternalResourceHelper
from pullenti.ner.measure.internal.UnitMeta import UnitMeta
from pullenti.ner.measure.internal.MeasureMeta import MeasureMeta
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.measure.internal.MeasureToken import MeasureToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection

class MeasureAnalyzer(Analyzer):
    """ Аналозатор для измеряемых величин """
    
    ANALYZER_NAME = "MEASURE"
    
    @property
    def name(self) -> str:
        return MeasureAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Измеряемые величины"
    
    @property
    def description(self) -> str:
        return "Диапазоны и просто значения в некоторых единицах измерения"
    
    def clone(self) -> 'Analyzer':
        return MeasureAnalyzer()
    
    @property
    def is_specific(self) -> bool:
        return True
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MeasureMeta.GLOBAL_META, UnitMeta.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MeasureMeta.IMAGE_ID] = EpNerBankInternalResourceHelper.get_bytes("measure.png")
        res[UnitMeta.IMAGE_ID] = EpNerBankInternalResourceHelper.get_bytes("munit.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == MeasureReferent.OBJ_TYPENAME): 
            return MeasureReferent()
        if (type0_ == UnitReferent.OBJ_TYPENAME): 
            return UnitReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    def process(self, kit : 'AnalysisKit') -> None:
        """ Основная функция выделения телефонов
        
        Args:
            cnt: 
            stage: 
        
        """
        ad = kit.get_analyzer_data(self)
        addunits = None
        if (kit.ontology is not None): 
            addunits = TerminCollection()
            for r in kit.ontology.items: 
                uu = Utils.asObjectOrNull(r.referent, UnitReferent)
                if (uu is None): 
                    continue
                if (uu._m_unit is not None): 
                    continue
                for s in uu.slots: 
                    if (s.type_name == UnitReferent.ATTR_NAME or s.type_name == UnitReferent.ATTR_FULLNAME): 
                        addunits.add(Termin._new119(Utils.asObjectOrNull(s.value, str), uu))
        t = kit.first_token
        first_pass3921 = True
        while True:
            if first_pass3921: first_pass3921 = False
            else: t = t.next0_
            if (not (t is not None)): break
            mt = MeasureToken.try_parse_minimal(t, addunits, False)
            if (mt is None): 
                mt = MeasureToken.try_parse(t, addunits, True, False, False, False)
            if (mt is None): 
                continue
            rts = mt.create_refenets_tokens_with_register(ad, True)
            if (rts is None): 
                continue
            i = 0
            while i < len(rts): 
                rt = rts[i]
                t.kit.embed_token(rt)
                t = (rt)
                j = i + 1
                while j < len(rts): 
                    if (rts[j].begin_token == rt.begin_token): 
                        rts[j].begin_token = t
                    if (rts[j].end_token == rt.end_token): 
                        rts[j].end_token = t
                    j += 1
                i += 1
        if (kit.ontology is not None): 
            for e0_ in ad.referents: 
                u = Utils.asObjectOrNull(e0_, UnitReferent)
                if (u is None): 
                    continue
                for r in kit.ontology.items: 
                    uu = Utils.asObjectOrNull(r.referent, UnitReferent)
                    if (uu is None): 
                        continue
                    ok = False
                    for s in uu.slots: 
                        if (s.type_name == UnitReferent.ATTR_NAME or s.type_name == UnitReferent.ATTR_FULLNAME): 
                            if (u.find_slot(None, s.value, True) is not None): 
                                ok = True
                                break
                    if (ok): 
                        u.ontology_items = list()
                        u.ontology_items.append(r)
                        break
    
    def _process_referent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        mt = MeasureToken.try_parse_minimal(begin, None, True)
        if (mt is not None): 
            rts = mt.create_refenets_tokens_with_register(None, True)
            if (rts is not None): 
                return rts[len(rts) - 1]
        return None
    
    def process_ontology_item(self, begin : 'Token') -> 'ReferentToken':
        if (not ((isinstance(begin, TextToken)))): 
            return None
        ut = UnitToken.try_parse(begin, None, None, False)
        if (ut is not None): 
            return ReferentToken(ut.create_referent_with_register(None), ut.begin_token, ut.end_token)
        u = UnitReferent()
        u.add_slot(UnitReferent.ATTR_NAME, begin.get_source_text(), False, 0)
        return ReferentToken(u, begin, begin)
    
    __m_initialized = False
    
    __m_lock = None
    
    @staticmethod
    def initialize() -> None:
        with MeasureAnalyzer.__m_lock: 
            if (MeasureAnalyzer.__m_initialized): 
                return
            MeasureAnalyzer.__m_initialized = True
            MeasureMeta.initialize()
            UnitMeta.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            UnitsHelper.initialize()
            NumbersWithUnitToken._initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
            ProcessorService.register_analyzer(MeasureAnalyzer())
    
    # static constructor for class MeasureAnalyzer
    @staticmethod
    def _static_ctor():
        MeasureAnalyzer.__m_lock = threading.Lock()

MeasureAnalyzer._static_ctor()