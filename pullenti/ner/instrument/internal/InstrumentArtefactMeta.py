# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass


class InstrumentArtefactMeta(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.instrument.InstrumentArtefact import InstrumentArtefact
        super().__init__()
        self.add_feature(InstrumentArtefact.ATTR_TYPE, "Тип", 0, 1)
        self.add_feature(InstrumentArtefact.ATTR_VALUE, "Значение", 0, 1)
        self.add_feature(InstrumentArtefact.ATTR_REF, "Ссылка на объект", 0, 1).show_as_parent = True
    
    @property
    def name(self) -> str:
        from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
        return InstrumentParticipant.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Артефакт"
    
    IMAGE_ID = "artefact"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return InstrumentArtefactMeta.IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class InstrumentArtefactMeta
    @staticmethod
    def _static_ctor():
        InstrumentArtefactMeta.GLOBAL_META = InstrumentArtefactMeta()

InstrumentArtefactMeta._static_ctor()