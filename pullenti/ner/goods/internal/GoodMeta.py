# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass

class GoodMeta(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.goods.GoodReferent import GoodReferent
        GoodMeta.GLOBAL_META = GoodMeta()
        GoodMeta.GLOBAL_META.add_feature(GoodReferent.ATTR_ATTR, "Атрибут", 1, 0).show_as_parent = True
    
    @property
    def name(self) -> str:
        from pullenti.ner.goods.GoodReferent import GoodReferent
        return GoodReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Товар"
    
    IMAGE_ID = "good"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return GoodMeta.IMAGE_ID
    
    GLOBAL_META = None