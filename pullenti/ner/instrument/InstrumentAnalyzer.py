# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.decree.internal.ResourceHelper import ResourceHelper
from pullenti.ner.instrument.InstrumentKind import InstrumentKind


class InstrumentAnalyzer(Analyzer):
    
    @property
    def name(self) -> str:
        return InstrumentAnalyzer.ANALYZER_NAME
    
    ANALYZER_NAME = "INSTRUMENT"
    
    @property
    def caption(self) -> str:
        return "Структура нормативно-правовых документов (НПА)"
    
    @property
    def description(self) -> str:
        return "Разбор структуры НПА на разделы и подразделы"
    
    def clone(self) -> 'Analyzer':
        return InstrumentAnalyzer()
    
    @property
    def is_specific(self) -> bool:
        """ Этот анализатор является специфическим """
        return True
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        from pullenti.ner.instrument.internal.MetaInstrument import MetaInstrument
        from pullenti.ner.instrument.internal.MetaInstrumentBlock import MetaInstrumentBlock
        from pullenti.ner.instrument.internal.InstrumentParticipantMeta import InstrumentParticipantMeta
        from pullenti.ner.instrument.internal.InstrumentArtefactMeta import InstrumentArtefactMeta
        return [MetaInstrument.GLOBAL_META, MetaInstrumentBlock.GLOBAL_META, InstrumentParticipantMeta.GLOBAL_META, InstrumentArtefactMeta.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        from pullenti.ner.instrument.internal.MetaInstrument import MetaInstrument
        from pullenti.ner.instrument.internal.MetaInstrumentBlock import MetaInstrumentBlock
        from pullenti.ner.instrument.internal.InstrumentParticipantMeta import InstrumentParticipantMeta
        from pullenti.ner.instrument.internal.InstrumentArtefactMeta import InstrumentArtefactMeta
        res = dict()
        res[MetaInstrument.DOC_IMAGE_ID] = ResourceHelper.get_bytes("decree.png")
        res[MetaInstrumentBlock.PART_IMAGE_ID] = ResourceHelper.get_bytes("part.png")
        res[InstrumentParticipantMeta.IMAGE_ID] = ResourceHelper.get_bytes("participant.png")
        res[InstrumentArtefactMeta.IMAGE_ID] = ResourceHelper.get_bytes("artefact.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        from pullenti.ner.instrument.InstrumentBlockReferent import InstrumentBlockReferent
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
        from pullenti.ner.instrument.InstrumentArtefact import InstrumentArtefact
        if (type0_ == InstrumentReferent.OBJ_TYPENAME): 
            return InstrumentReferent()
        if (type0_ == InstrumentBlockReferent.OBJ_TYPENAME): 
            return InstrumentBlockReferent()
        if (type0_ == InstrumentParticipant.OBJ_TYPENAME): 
            return InstrumentParticipant()
        if (type0_ == InstrumentArtefact.OBJ_TYPENAME): 
            return InstrumentArtefact()
        return None
    
    def process(self, kit : 'AnalysisKit') -> None:
        from pullenti.ner.instrument.internal.FragToken import FragToken
        t = kit.first_token
        t1 = t
        if (t is None): 
            return
        dfr = FragToken.create_document(t, 0, InstrumentKind.UNDEFINED)
        if (dfr is None): 
            return
        ad = kit.get_analyzer_data(self)
        res = dfr.create_referent(ad)
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.Termin import Termin
        from pullenti.ner.instrument.internal.InstrToken import InstrToken
        from pullenti.ner.instrument.internal.ParticipantToken import ParticipantToken
        from pullenti.ner.ProcessorService import ProcessorService
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            InstrToken.initialize()
            ParticipantToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.register_analyzer(InstrumentAnalyzer())