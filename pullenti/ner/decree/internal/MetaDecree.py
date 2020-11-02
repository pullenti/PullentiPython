# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.decree.DecreeKind import DecreeKind
from pullenti.ner.Referent import Referent

class MetaDecree(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        MetaDecree.GLOBAL_META = MetaDecree()
        MetaDecree.GLOBAL_META.add_feature(DecreeReferent.ATTR_TYPE, "Тип", 1, 1)
        MetaDecree.GLOBAL_META.add_feature(DecreeReferent.ATTR_NUMBER, "Номер", 0, 0)
        MetaDecree.GLOBAL_META.add_feature(DecreeReferent.ATTR_CASENUMBER, "Номер дела", 0, 0)
        MetaDecree.GLOBAL_META.add_feature(DecreeReferent.ATTR_DATE, "Дата", 0, 0)
        MetaDecree.GLOBAL_META.add_feature(DecreeReferent.ATTR_SOURCE, "Источник", 0, 1)
        MetaDecree.GLOBAL_META.add_feature(DecreeReferent.ATTR_GEO, "Географический объект", 0, 1)
        MetaDecree.GLOBAL_META.add_feature(DecreeReferent.ATTR_NAME, "Наименование", 0, 0)
        MetaDecree.GLOBAL_META.add_feature(DecreeReferent.ATTR_READING, "Чтение", 0, 1)
        MetaDecree.GLOBAL_META.add_feature(DecreeReferent.ATTR_EDITION, "В редакции", 0, 0)
        MetaDecree.GLOBAL_META.add_feature(Referent.ATTR_GENERAL, "Обобщающий объект", 0, 1)
    
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
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        if (isinstance(obj, DecreeReferent)): 
            ki = obj.kind
            if (ki == DecreeKind.PUBLISHER): 
                return MetaDecree.PUBLISH_IMAGE_ID
            if (ki == DecreeKind.STANDARD): 
                return MetaDecree.STANDADR_IMAGE_ID
        return MetaDecree.DECREE_IMAGE_ID
    
    GLOBAL_META = None