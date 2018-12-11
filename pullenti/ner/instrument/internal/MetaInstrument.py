# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.instrument.InstrumentBlockReferent import InstrumentBlockReferent

class MetaInstrument(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        MetaInstrument.GLOBAL_META = MetaInstrument()
        MetaInstrument.GLOBAL_META.addFeature(InstrumentReferent.ATTR_TYPE, "Тип", 0, 1)
        MetaInstrument.GLOBAL_META.addFeature(InstrumentBlockReferent.ATTR_NUMBER, "Номер", 0, 1)
        MetaInstrument.GLOBAL_META.addFeature(InstrumentReferent.ATTR_CASENUMBER, "Номер дела", 0, 1)
        MetaInstrument.GLOBAL_META.addFeature(InstrumentReferent.ATTR_DATE, "Дата", 0, 1)
        MetaInstrument.GLOBAL_META.addFeature(InstrumentReferent.ATTR_SOURCE, "Публикующий орган", 0, 1)
        MetaInstrument.GLOBAL_META.addFeature(InstrumentReferent.ATTR_GEO, "Географический объект", 0, 1)
        MetaInstrument.GLOBAL_META.addFeature(InstrumentBlockReferent.ATTR_NAME, "Наименование", 0, 0)
        MetaInstrument.GLOBAL_META.addFeature(InstrumentBlockReferent.ATTR_CHILD, "Внутренний элемент", 0, 0).show_as_parent = True
        MetaInstrument.GLOBAL_META.addFeature(InstrumentReferent.ATTR_SIGNER, "Подписант", 0, 1)
        MetaInstrument.GLOBAL_META.addFeature(InstrumentReferent.ATTR_PART, "Часть", 0, 1)
        MetaInstrument.GLOBAL_META.addFeature(InstrumentReferent.ATTR_APPENDIX, "Приложение", 0, 0)
        MetaInstrument.GLOBAL_META.addFeature(InstrumentReferent.ATTR_PARTICIPANT, "Участник", 0, 0).show_as_parent = True
        MetaInstrument.GLOBAL_META.addFeature(InstrumentReferent.ATTR_ARTEFACT, "Артефакт", 0, 0).show_as_parent = True
    
    @property
    def name(self) -> str:
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        return InstrumentReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Нормативно-правовой акт"
    
    DOC_IMAGE_ID = "decree"
    
    PART_IMAGE_ID = "part"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MetaInstrument.DOC_IMAGE_ID
    
    GLOBAL_META = None