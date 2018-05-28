# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass


class MetaDateRange(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        super().__init__()
        self.add_feature(DateRangeReferent.ATTR_FROM, "Начало периода", 0, 1)
        self.add_feature(DateRangeReferent.ATTR_TO, "Конец периода", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        return DateRangeReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Период"
    
    DATE_RANGE_IMAGE_ID = "daterange"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaDateRange.DATE_RANGE_IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class MetaDateRange
    @staticmethod
    def _static_ctor():
        MetaDateRange.GLOBAL_META = MetaDateRange()

MetaDateRange._static_ctor()