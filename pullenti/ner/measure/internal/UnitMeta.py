# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass

class UnitMeta(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.measure.UnitReferent import UnitReferent
        UnitMeta.GLOBAL_META = UnitMeta()
        UnitMeta.GLOBAL_META.add_feature(UnitReferent.ATTR_NAME, "Краткое наименование", 1, 0)
        UnitMeta.GLOBAL_META.add_feature(UnitReferent.ATTR_FULLNAME, "Полное наименование", 1, 0)
        UnitMeta.GLOBAL_META.add_feature(UnitReferent.ATTR_POW, "Степень", 0, 1)
        UnitMeta.GLOBAL_META.add_feature(UnitReferent.ATTR_BASEFACTOR, "Мультипликатор для базовой единицы", 0, 1)
        UnitMeta.GLOBAL_META.add_feature(UnitReferent.ATTR_BASEUNIT, "Базовая единица", 0, 1)
        UnitMeta.GLOBAL_META.add_feature(UnitReferent.ATTR_UNKNOWN, "Неизвестная метрика", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.measure.UnitReferent import UnitReferent
        return UnitReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Единицы измерения"
    
    IMAGE_ID = "munit"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return UnitMeta.IMAGE_ID
    
    GLOBAL_META = None