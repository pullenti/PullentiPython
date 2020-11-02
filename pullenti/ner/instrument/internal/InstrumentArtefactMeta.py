# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.instrument.InstrumentParticipantReferent import InstrumentParticipantReferent

class InstrumentArtefactMeta(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.instrument.InstrumentArtefactReferent import InstrumentArtefactReferent
        InstrumentArtefactMeta.GLOBAL_META = InstrumentArtefactMeta()
        InstrumentArtefactMeta.GLOBAL_META.add_feature(InstrumentArtefactReferent.ATTR_TYPE, "Тип", 0, 1)
        InstrumentArtefactMeta.GLOBAL_META.add_feature(InstrumentArtefactReferent.ATTR_VALUE, "Значение", 0, 1)
        InstrumentArtefactMeta.GLOBAL_META.add_feature(InstrumentArtefactReferent.ATTR_REF, "Ссылка на объект", 0, 1).show_as_parent = True
    
    @property
    def name(self) -> str:
        return InstrumentParticipantReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Артефакт"
    
    IMAGE_ID = "artefact"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return InstrumentArtefactMeta.IMAGE_ID
    
    GLOBAL_META = None