# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant

class InstrumentArtefactMeta(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.instrument.InstrumentArtefact import InstrumentArtefact
        InstrumentArtefactMeta.GLOBAL_META = InstrumentArtefactMeta()
        InstrumentArtefactMeta.GLOBAL_META.addFeature(InstrumentArtefact.ATTR_TYPE, "Тип", 0, 1)
        InstrumentArtefactMeta.GLOBAL_META.addFeature(InstrumentArtefact.ATTR_VALUE, "Значение", 0, 1)
        InstrumentArtefactMeta.GLOBAL_META.addFeature(InstrumentArtefact.ATTR_REF, "Ссылка на объект", 0, 1).show_as_parent = True
    
    @property
    def name(self) -> str:
        return InstrumentParticipant.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Артефакт"
    
    IMAGE_ID = "artefact"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return InstrumentArtefactMeta.IMAGE_ID
    
    GLOBAL_META = None