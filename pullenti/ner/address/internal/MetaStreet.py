# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass


class MetaStreet(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.address.StreetReferent import StreetReferent
        super().__init__()
        self.add_feature(StreetReferent.ATTR_TYP, "Тип", 0, 0)
        self.add_feature(StreetReferent.ATTR_NAME, "Наименование", 1, 0)
        self.add_feature(StreetReferent.ATTR_NUMBER, "Номер", 0, 1)
        self.add_feature(StreetReferent.ATTR_SECNUMBER, "Доп.номер", 0, 1)
        self.add_feature(StreetReferent.ATTR_GEO, "Географический объект", 0, 1)
        self.add_feature(StreetReferent.ATTR_FIAS, "Объект ФИАС", 0, 1)
        self.add_feature(StreetReferent.ATTR_BTI, "Объект БТИ", 0, 1)
        self.add_feature(StreetReferent.ATTR_OKM, "Код ОКМ УМ", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.address.StreetReferent import StreetReferent
        return StreetReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Улица"
    
    IMAGE_ID = "street"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaStreet.IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaStreet
    @staticmethod
    def _static_ctor():
        MetaStreet._global_meta = MetaStreet()

MetaStreet._static_ctor()