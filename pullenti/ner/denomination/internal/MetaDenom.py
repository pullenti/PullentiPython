# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass


class MetaDenom(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.denomination.DenominationReferent import DenominationReferent
        super().__init__()
        self.add_feature(DenominationReferent.ATTR_VALUE, "Значение", 0, 1)
    
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
    
    # static constructor for class MetaDenom
    @staticmethod
    def _static_ctor():
        MetaDenom._global_meta = MetaDenom()

MetaDenom._static_ctor()