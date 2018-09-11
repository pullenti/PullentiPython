# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.unisharp.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass


class MetaNamedEntity(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.named.NamedEntityReferent import NamedEntityReferent
        super().__init__()
        self.add_feature(NamedEntityReferent.ATTR_KIND, "Класс", 1, 1)
        self.add_feature(NamedEntityReferent.ATTR_TYPE, "Тип", 0, 0)
        self.add_feature(NamedEntityReferent.ATTR_NAME, "Наименование", 0, 0)
        self.add_feature(NamedEntityReferent.ATTR_REF, "Ссылка", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.named.NamedEntityReferent import NamedEntityReferent
        return NamedEntityReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Именованная сущность"
    
    IMAGE_ID = "monument"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.named.NamedEntityReferent import NamedEntityReferent
        if (isinstance(obj, NamedEntityReferent)): 
            return Utils.enumToString((obj if isinstance(obj, NamedEntityReferent) else None).kind)
        return MetaNamedEntity.IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class MetaNamedEntity
    @staticmethod
    def _static_ctor():
        MetaNamedEntity.GLOBAL_META = MetaNamedEntity()

MetaNamedEntity._static_ctor()