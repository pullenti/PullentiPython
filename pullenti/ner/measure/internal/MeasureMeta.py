# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.ner.ReferentClass import ReferentClass


class MeasureMeta(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.measure.MeasureReferent import MeasureReferent
        super().__init__()
        self.addFeature(MeasureReferent.ATTR_TEMPLATE, "Шаблон", 1, 1)
        self.addFeature(MeasureReferent.ATTR_VALUE, "Значение", 1, 0)
        self.addFeature(MeasureReferent.ATTR_UNIT, "Единица измерения", 1, 2)
        self.addFeature(MeasureReferent.ATTR_REF, "Ссылка на уточняющее измерение", 0, 0)
        self.addFeature(MeasureReferent.ATTR_NAME, "Наименование", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.measure.MeasureReferent import MeasureReferent
        return MeasureReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Измеряемые величины"
    
    IMAGE_ID = "measure"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MeasureMeta.IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class MeasureMeta
    @staticmethod
    def _static_ctor():
        MeasureMeta.GLOBAL_META = MeasureMeta()

MeasureMeta._static_ctor()