# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass


class UnitMeta(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.measure.UnitReferent import UnitReferent
        super().__init__()
        self.add_feature(UnitReferent.ATTR_NAME, "Краткое наименование", 1, 0)
        self.add_feature(UnitReferent.ATTR_FULLNAME, "Полное наименование", 1, 0)
        self.add_feature(UnitReferent.ATTR_POW, "Степень", 0, 1)
        self.add_feature(UnitReferent.ATTR_BASEFACTOR, "Мультипликатор для базовой единицы", 0, 1)
        self.add_feature(UnitReferent.ATTR_BASEUNIT, "Базовая единица", 0, 1)
    
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
    
    # static constructor for class UnitMeta
    @staticmethod
    def _static_ctor():
        UnitMeta.GLOBAL_META = UnitMeta()

UnitMeta._static_ctor()