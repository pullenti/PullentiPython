# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.booklink.BookLinkRefType import BookLinkRefType


class MetaBookLinkRef(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.booklink.BookLinkRefReferent import BookLinkRefReferent
        super().__init__()
        self.add_feature(BookLinkRefReferent.ATTR_BOOK, "Источник", 1, 1)
        self.add_feature(BookLinkRefReferent.ATTR_TYPE, "Тип", 0, 1)
        self.add_feature(BookLinkRefReferent.ATTR_PAGES, "Страницы", 0, 1)
        self.add_feature(BookLinkRefReferent.ATTR_NUMBER, "Номер", 0, 1)
        self.add_feature(BookLinkRefReferent.ATTR_MISC, "Разное", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.booklink.BookLinkRefReferent import BookLinkRefReferent
        return BookLinkRefReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Ссылка на внешний источник в тексте"
    
    IMAGE_ID = "booklinkref"
    
    IMAGE_ID_INLINE = "booklinkrefinline"
    
    IMAGE_ID_LAST = "booklinkreflast"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.booklink.BookLinkRefReferent import BookLinkRefReferent
        rr = (obj if isinstance(obj, BookLinkRefReferent) else None)
        if (rr is not None): 
            if (rr.typ == BookLinkRefType.INLINE): 
                return MetaBookLinkRef.IMAGE_ID_INLINE
        return MetaBookLinkRef.IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaBookLinkRef
    @staticmethod
    def _static_ctor():
        MetaBookLinkRef._global_meta = MetaBookLinkRef()

MetaBookLinkRef._static_ctor()