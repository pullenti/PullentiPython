# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass

class MeasureMeta(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.measure.MeasureReferent import MeasureReferent
        MeasureMeta.GLOBAL_META = MeasureMeta()
        MeasureMeta.GLOBAL_META.add_feature(MeasureReferent.ATTR_TEMPLATE, "Шаблон", 1, 1)
        MeasureMeta.GLOBAL_META.add_feature(MeasureReferent.ATTR_VALUE, "Значение", 1, 0)
        MeasureMeta.GLOBAL_META.add_feature(MeasureReferent.ATTR_UNIT, "Единица измерения", 1, 2)
        MeasureMeta.GLOBAL_META.add_feature(MeasureReferent.ATTR_REF, "Ссылка на уточняющее измерение", 0, 0)
        MeasureMeta.GLOBAL_META.add_feature(MeasureReferent.ATTR_NAME, "Наименование", 0, 0)
        MeasureMeta.GLOBAL_META.add_feature(MeasureReferent.ATTR_KIND, "Тип", 0, 1)
    
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