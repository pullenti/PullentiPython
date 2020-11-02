# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass

class MetaDateRange(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        MetaDateRange.GLOBAL_META = MetaDateRange()
        MetaDateRange.GLOBAL_META.add_feature(DateRangeReferent.ATTR_FROM, "Начало периода", 0, 1)
        MetaDateRange.GLOBAL_META.add_feature(DateRangeReferent.ATTR_TO, "Конец периода", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        return DateRangeReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Период"
    
    DATE_RANGE_IMAGE_ID = "daterange"
    
    DATE_RANGE_REL_IMAGE_ID = "daterangerel"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        if (isinstance(obj, DateRangeReferent)): 
            if (obj.is_relative): 
                return MetaDateRange.DATE_RANGE_REL_IMAGE_ID
        return MetaDateRange.DATE_RANGE_IMAGE_ID
    
    GLOBAL_META = None