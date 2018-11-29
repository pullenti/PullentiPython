# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.ner.ReferentClass import ReferentClass


class InstrumentParticipantMeta(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
        super().__init__()
        self.addFeature(InstrumentParticipant.ATTR_TYPE, "Тип", 0, 1)
        self.addFeature(InstrumentParticipant.ATTR_REF, "Ссылка на объект", 0, 1).show_as_parent = True
        self.addFeature(InstrumentParticipant.ATTR_DELEGATE, "Ссылка на представителя", 0, 1).show_as_parent = True
        self.addFeature(InstrumentParticipant.ATTR_GROUND, "Основание", 0, 1).show_as_parent = True
    
    @property
    def name(self) -> str:
        from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
        return InstrumentParticipant.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Участник"
    
    IMAGE_ID = "participant"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return InstrumentParticipantMeta.IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class InstrumentParticipantMeta
    @staticmethod
    def _static_ctor():
        InstrumentParticipantMeta.GLOBAL_META = InstrumentParticipantMeta()

InstrumentParticipantMeta._static_ctor()