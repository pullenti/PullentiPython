# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import threading
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.bank.internal.EpNerBankInternalResourceHelper import EpNerBankInternalResourceHelper
from pullenti.ner.measure.internal.UnitsHelper import UnitsHelper


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
        from pullenti.ner.measure.internal.MeasureMeta import MeasureMeta
        from pullenti.ner.measure.internal.UnitMeta import UnitMeta
        return [MeasureMeta.GLOBAL_META, UnitMeta.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        from pullenti.ner.measure.internal.MeasureMeta import MeasureMeta
        from pullenti.ner.measure.internal.UnitMeta import UnitMeta
        res = dict()
        res[MeasureMeta.IMAGE_ID] = EpNerBankInternalResourceHelper.getBytes("measure.png")
        res[UnitMeta.IMAGE_ID] = EpNerBankInternalResourceHelper.getBytes("munit.png")
        return res
    
    def createReferent(self, type0_ : str) -> 'Referent':
        from pullenti.ner.measure.MeasureReferent import MeasureReferent
        from pullenti.ner.measure.UnitReferent import UnitReferent
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
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.measure.UnitReferent import UnitReferent
        from pullenti.ner.core.Termin import Termin
        from pullenti.ner.measure.internal.MeasureToken import MeasureToken
        ad = kit.getAnalyzerData(self)
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
                        addunits.add(Termin._new118(Utils.asObjectOrNull(s.value, str), uu))
        t = kit.first_token
        first_pass3052 = True
        while True:
            if first_pass3052: first_pass3052 = False
            else: t = t.next0_
            if (not (t is not None)): break
            mt = MeasureToken.tryParseMinimal(t, addunits, False)
            if (mt is None): 
                mt = MeasureToken.tryParse(t, addunits, True)
            if (mt is None): 
                continue
            rts = mt.createRefenetsTokensWithRegister(ad, True)
            if (rts is None): 
                continue
            i = 0
            while i < len(rts): 
                rt = rts[i]
                t.kit.embedToken(rt)
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
                            if (u.findSlot(None, s.value, True) is not None): 
                                ok = True
                                break
                    if (ok): 
                        u.ontology_items = list()
                        u.ontology_items.append(r)
                        break
    
    def _processReferent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        from pullenti.ner.measure.internal.MeasureToken import MeasureToken
        mt = MeasureToken.tryParseMinimal(begin, None, True)
        if (mt is not None): 
            rts = mt.createRefenetsTokensWithRegister(None, True)
            if (rts is not None): 
                return rts[len(rts) - 1]
        return None
    
    def processOntologyItem(self, begin : 'Token') -> 'ReferentToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.measure.internal.UnitToken import UnitToken
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.measure.UnitReferent import UnitReferent
        if (not ((isinstance(begin, TextToken)))): 
            return None
        ut = UnitToken.tryParse(begin, None, None)
        if (ut is not None): 
            return ReferentToken(ut.createReferentWithRegister(None), ut.begin_token, ut.end_token)
        u = UnitReferent()
        u.addSlot(UnitReferent.ATTR_NAME, begin.getSourceText(), False, 0)
        return ReferentToken(u, begin, begin)
    
    __m_initialized = False
    
    __m_lock = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.Termin import Termin
        from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
        from pullenti.ner.ProcessorService import ProcessorService
        with MeasureAnalyzer.__m_lock: 
            if (MeasureAnalyzer.__m_initialized): 
                return
            MeasureAnalyzer.__m_initialized = True
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            UnitsHelper.initialize()
            NumbersWithUnitToken._initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
            ProcessorService.registerAnalyzer(MeasureAnalyzer())
    
    # static constructor for class MeasureAnalyzer
    @staticmethod
    def _static_ctor():
        MeasureAnalyzer.__m_lock = threading.Lock()

MeasureAnalyzer._static_ctor()