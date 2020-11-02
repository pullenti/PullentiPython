# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass

class MetaTitleInfo(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.titlepage.TitlePageReferent import TitlePageReferent
        MetaTitleInfo._global_meta = MetaTitleInfo()
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_NAME, "Название", 0, 0)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_TYPE, "Тип", 0, 0)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_AUTHOR, "Автор", 0, 0)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_SUPERVISOR, "Руководитель", 0, 0)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_EDITOR, "Редактор", 0, 0)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_CONSULTANT, "Консультант", 0, 0)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_OPPONENT, "Оппонент", 0, 0)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_AFFIRMANT, "Утверждающий", 0, 0)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_TRANSLATOR, "Переводчик", 0, 0)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_ORG, "Организация", 0, 1)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_STUDENTYEAR, "Номер курса", 0, 1)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_DATE, "Дата", 0, 1)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_CITY, "Город", 0, 1)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_SPECIALITY, "Специальность", 0, 1)
        MetaTitleInfo._global_meta.add_feature(TitlePageReferent.ATTR_ATTR, "Атрибут", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.titlepage.TitlePageReferent import TitlePageReferent
        return TitlePageReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Заголовок"
    
    TITLE_INFO_IMAGE_ID = "titleinfo"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaTitleInfo.TITLE_INFO_IMAGE_ID
    
    _global_meta = None