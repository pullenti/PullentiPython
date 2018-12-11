# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.ner.ReferentClass import ReferentClass

class MetaDenom(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.denomination.DenominationReferent import DenominationReferent
        MetaDenom._global_meta = MetaDenom()
        MetaDenom._global_meta.addFeature(DenominationReferent.ATTR_VALUE, "Значение", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.denomination.DenominationReferent import DenominationReferent
        return DenominationReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Обозначение"
    
    DENOM_IMAGE_ID = "denom"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MetaDenom.DENOM_IMAGE_ID
    
    _global_meta = None