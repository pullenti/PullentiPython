# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass

class MetaNamedEntity(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.named.NamedEntityReferent import NamedEntityReferent
        MetaNamedEntity.GLOBAL_META = MetaNamedEntity()
        MetaNamedEntity.GLOBAL_META.add_feature(NamedEntityReferent.ATTR_KIND, "Класс", 1, 1)
        MetaNamedEntity.GLOBAL_META.add_feature(NamedEntityReferent.ATTR_TYPE, "Тип", 0, 0)
        MetaNamedEntity.GLOBAL_META.add_feature(NamedEntityReferent.ATTR_NAME, "Наименование", 0, 0)
        MetaNamedEntity.GLOBAL_META.add_feature(NamedEntityReferent.ATTR_REF, "Ссылка", 0, 1)
    
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
            return Utils.enumToString(obj.kind)
        return MetaNamedEntity.IMAGE_ID
    
    GLOBAL_META = None