# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass


class MeasureMeta(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.measure.MeasureReferent import MeasureReferent
        super().__init__()
        self.add_feature(MeasureReferent.ATTR_TEMPLATE, "Шаблон", 1, 1)
        self.add_feature(MeasureReferent.ATTR_VALUE, "Значение", 1, 0)
        self.add_feature(MeasureReferent.ATTR_UNIT, "Единица измерения", 1, 2)
        self.add_feature(MeasureReferent.ATTR_REF, "Ссылка на уточняющее измерение", 0, 0)
        self.add_feature(MeasureReferent.ATTR_NAME, "Наименование", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.measure.MeasureReferent import MeasureReferent
        return MeasureReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Измеряемые величины"
    
    IMAGE_ID = "measure"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MeasureMeta.IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class MeasureMeta
    @staticmethod
    def _static_ctor():
        MeasureMeta.GLOBAL_META = MeasureMeta()

MeasureMeta._static_ctor()