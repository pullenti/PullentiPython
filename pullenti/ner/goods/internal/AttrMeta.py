# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.goods.GoodAttrType import GoodAttrType

class AttrMeta(ReferentClass):
    
    def __init__(self) -> None:
        super().__init__()
        self.typ_attr = None;
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.goods.GoodAttributeReferent import GoodAttributeReferent
        AttrMeta.GLOBAL_META = AttrMeta()
        AttrMeta.GLOBAL_META.typ_attr = AttrMeta.GLOBAL_META.add_feature(GoodAttributeReferent.ATTR_TYPE, "Тип", 0, 1)
        AttrMeta.GLOBAL_META.typ_attr.add_value(Utils.enumToString(GoodAttrType.KEYWORD), "Ключевое слово", None, None)
        AttrMeta.GLOBAL_META.typ_attr.add_value(Utils.enumToString(GoodAttrType.CHARACTER), "Качеств.свойство", None, None)
        AttrMeta.GLOBAL_META.typ_attr.add_value(Utils.enumToString(GoodAttrType.MODEL), "Модель", None, None)
        AttrMeta.GLOBAL_META.typ_attr.add_value(Utils.enumToString(GoodAttrType.NUMERIC), "Колич.свойство", None, None)
        AttrMeta.GLOBAL_META.typ_attr.add_value(Utils.enumToString(GoodAttrType.PROPER), "Имя собственное", None, None)
        AttrMeta.GLOBAL_META.typ_attr.add_value(Utils.enumToString(GoodAttrType.REFERENT), "Ссылка", None, None)
        AttrMeta.GLOBAL_META.add_feature(GoodAttributeReferent.ATTR_VALUE, "Значение", 1, 0)
        AttrMeta.GLOBAL_META.add_feature(GoodAttributeReferent.ATTR_ALTVALUE, "Значание (альт.)", 0, 0)
        AttrMeta.GLOBAL_META.add_feature(GoodAttributeReferent.ATTR_UNIT, "Единица измерения", 0, 1)
        AttrMeta.GLOBAL_META.add_feature(GoodAttributeReferent.ATTR_NAME, "Название", 0, 1)
        AttrMeta.GLOBAL_META.add_feature(GoodAttributeReferent.ATTR_REF, "Ссылка", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.goods.GoodAttributeReferent import GoodAttributeReferent
        return GoodAttributeReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Атрибут товара"
    
    ATTR_IMAGE_ID = "attr"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return AttrMeta.ATTR_IMAGE_ID
    
    GLOBAL_META = None