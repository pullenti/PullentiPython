# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.Referent import Referent
from pullenti.ner.decree.DecreeKind import DecreeKind


class MetaDecree(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        super().__init__()
        self.addFeature(DecreeReferent.ATTR_TYPE, "Тип", 1, 1)
        self.addFeature(DecreeReferent.ATTR_NUMBER, "Номер", 0, 0)
        self.addFeature(DecreeReferent.ATTR_CASENUMBER, "Номер дела", 0, 0)
        self.addFeature(DecreeReferent.ATTR_DATE, "Дата", 0, 0)
        self.addFeature(DecreeReferent.ATTR_SOURCE, "Источник", 0, 1)
        self.addFeature(DecreeReferent.ATTR_GEO, "Географический объект", 0, 1)
        self.addFeature(DecreeReferent.ATTR_NAME, "Наименование", 0, 0)
        self.addFeature(DecreeReferent.ATTR_READING, "Чтение", 0, 1)
        self.addFeature(DecreeReferent.ATTR_EDITION, "В редакции", 0, 0)
        self.addFeature(Referent.ATTR_GENERAL, "Обобщающий объект", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        return DecreeReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Декрет"
    
    DECREE_IMAGE_ID = "decree"
    
    PUBLISH_IMAGE_ID = "publish"
    
    STANDADR_IMAGE_ID = "decreestd"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        if (isinstance(obj, DecreeReferent)): 
            ki = (Utils.asObjectOrNull(obj, DecreeReferent)).kind
            if (ki == DecreeKind.PUBLISHER): 
                return MetaDecree.PUBLISH_IMAGE_ID
            if (ki == DecreeKind.STANDARD): 
                return MetaDecree.STANDADR_IMAGE_ID
        return MetaDecree.DECREE_IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class MetaDecree
    @staticmethod
    def _static_ctor():
        MetaDecree.GLOBAL_META = MetaDecree()

MetaDecree._static_ctor()