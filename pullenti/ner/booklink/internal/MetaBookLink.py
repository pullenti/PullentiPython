# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.titlepage.internal.MetaTitleInfo import MetaTitleInfo


class MetaBookLink(MetaTitleInfo):
    
    def __init__(self) -> None:
        from pullenti.ner.booklink.BookLinkReferent import BookLinkReferent
        super().__init__()
        self.add_feature(BookLinkReferent.ATTR_AUTHOR, "Автор", 0, 0)
        self.add_feature(BookLinkReferent.ATTR_NAME, "Наименование", 1, 1)
        self.add_feature(BookLinkReferent.ATTR_TYPE, "Тип", 0, 1)
        self.add_feature(BookLinkReferent.ATTR_YEAR, "Год", 0, 1)
        self.add_feature(BookLinkReferent.ATTR_GEO, "География", 0, 1)
        self.add_feature(BookLinkReferent.ATTR_LANG, "Язык", 0, 1)
        self.add_feature(BookLinkReferent.ATTR_URL, "URL", 0, 0)
        self.add_feature(BookLinkReferent.ATTR_MISC, "Разное", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.booklink.BookLinkReferent import BookLinkReferent
        return BookLinkReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Ссылка на внешний источник"
    
    IMAGE_ID = "booklink"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaBookLink.IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaBookLink
    @staticmethod
    def _static_ctor():
        MetaBookLink._global_meta = MetaBookLink()

MetaBookLink._static_ctor()