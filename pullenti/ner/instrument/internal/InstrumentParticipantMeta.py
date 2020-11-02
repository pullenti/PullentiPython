# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass

class InstrumentParticipantMeta(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.instrument.InstrumentParticipantReferent import InstrumentParticipantReferent
        InstrumentParticipantMeta.GLOBAL_META = InstrumentParticipantMeta()
        InstrumentParticipantMeta.GLOBAL_META.add_feature(InstrumentParticipantReferent.ATTR_TYPE, "Тип", 0, 1)
        InstrumentParticipantMeta.GLOBAL_META.add_feature(InstrumentParticipantReferent.ATTR_REF, "Ссылка на объект", 0, 1).show_as_parent = True
        InstrumentParticipantMeta.GLOBAL_META.add_feature(InstrumentParticipantReferent.ATTR_DELEGATE, "Ссылка на представителя", 0, 1).show_as_parent = True
        InstrumentParticipantMeta.GLOBAL_META.add_feature(InstrumentParticipantReferent.ATTR_GROUND, "Основание", 0, 1).show_as_parent = True
    
    @property
    def name(self) -> str:
        from pullenti.ner.instrument.InstrumentParticipantReferent import InstrumentParticipantReferent
        return InstrumentParticipantReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Участник"
    
    IMAGE_ID = "participant"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return InstrumentParticipantMeta.IMAGE_ID
    
    GLOBAL_META = None