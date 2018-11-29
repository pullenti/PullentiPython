# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass


class MetaNamedEntity(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.named.NamedEntityReferent import NamedEntityReferent
        super().__init__()
        self.addFeature(NamedEntityReferent.ATTR_KIND, "Класс", 1, 1)
        self.addFeature(NamedEntityReferent.ATTR_TYPE, "Тип", 0, 0)
        self.addFeature(NamedEntityReferent.ATTR_NAME, "Наименование", 0, 0)
        self.addFeature(NamedEntityReferent.ATTR_REF, "Ссылка", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.named.NamedEntityReferent import NamedEntityReferent
        return NamedEntityReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Именованная сущность"
    
    IMAGE_ID = "monument"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.named.NamedEntityReferent import NamedEntityReferent
        if (isinstance(obj, NamedEntityReferent)): 
            return Utils.enumToString((Utils.asObjectOrNull(obj, NamedEntityReferent)).kind)
        return MetaNamedEntity.IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class MetaNamedEntity
    @staticmethod
    def _static_ctor():
        MetaNamedEntity.GLOBAL_META = MetaNamedEntity()

MetaNamedEntity._static_ctor()