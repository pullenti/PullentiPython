# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass

class MetaDenom(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.denomination.DenominationReferent import DenominationReferent
        MetaDenom._global_meta = MetaDenom()
        MetaDenom._global_meta.add_feature(DenominationReferent.ATTR_VALUE, "Значение", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.denomination.DenominationReferent import DenominationReferent
        return DenominationReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Обозначение"
    
    DENOM_IMAGE_ID = "denom"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaDenom.DENOM_IMAGE_ID
    
    _global_meta = None