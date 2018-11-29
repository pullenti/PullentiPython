# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.ner.ReferentClass import ReferentClass


class MetaTitleInfo(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.titlepage.TitlePageReferent import TitlePageReferent
        super().__init__()
        self.addFeature(TitlePageReferent.ATTR_NAME, "Название", 0, 0)
        self.addFeature(TitlePageReferent.ATTR_TYPE, "Тип", 0, 0)
        self.addFeature(TitlePageReferent.ATTR_AUTHOR, "Автор", 0, 0)
        self.addFeature(TitlePageReferent.ATTR_SUPERVISOR, "Руководитель", 0, 0)
        self.addFeature(TitlePageReferent.ATTR_EDITOR, "Редактор", 0, 0)
        self.addFeature(TitlePageReferent.ATTR_CONSULTANT, "Консультант", 0, 0)
        self.addFeature(TitlePageReferent.ATTR_OPPONENT, "Оппонент", 0, 0)
        self.addFeature(TitlePageReferent.ATTR_AFFIRMANT, "Утверждающий", 0, 0)
        self.addFeature(TitlePageReferent.ATTR_TRANSLATOR, "Переводчик", 0, 0)
        self.addFeature(TitlePageReferent.ATTR_ORG, "Организация", 0, 1)
        self.addFeature(TitlePageReferent.ATTR_DEP, "Подразделение", 0, 1)
        self.addFeature(TitlePageReferent.ATTR_STUDENTYEAR, "Номер курса", 0, 1)
        self.addFeature(TitlePageReferent.ATTR_DATE, "Дата", 0, 1)
        self.addFeature(TitlePageReferent.ATTR_CITY, "Город", 0, 1)
        self.addFeature(TitlePageReferent.ATTR_SPECIALITY, "Специальность", 0, 1)
        self.addFeature(TitlePageReferent.ATTR_ATTR, "Атрибут", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.titlepage.TitlePageReferent import TitlePageReferent
        return TitlePageReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Заголовок"
    
    TITLE_INFO_IMAGE_ID = "titleinfo"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MetaTitleInfo.TITLE_INFO_IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaTitleInfo
    @staticmethod
    def _static_ctor():
        MetaTitleInfo._global_meta = MetaTitleInfo()

MetaTitleInfo._static_ctor()