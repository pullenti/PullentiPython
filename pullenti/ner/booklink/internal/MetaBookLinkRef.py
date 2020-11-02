# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.booklink.BookLinkRefType import BookLinkRefType

class MetaBookLinkRef(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.booklink.BookLinkRefReferent import BookLinkRefReferent
        MetaBookLinkRef._global_meta = MetaBookLinkRef()
        MetaBookLinkRef._global_meta.add_feature(BookLinkRefReferent.ATTR_BOOK, "Источник", 1, 1)
        MetaBookLinkRef._global_meta.add_feature(BookLinkRefReferent.ATTR_TYPE, "Тип", 0, 1)
        MetaBookLinkRef._global_meta.add_feature(BookLinkRefReferent.ATTR_PAGES, "Страницы", 0, 1)
        MetaBookLinkRef._global_meta.add_feature(BookLinkRefReferent.ATTR_NUMBER, "Номер", 0, 1)
        MetaBookLinkRef._global_meta.add_feature(BookLinkRefReferent.ATTR_MISC, "Разное", 0, 0)
    
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
        rr = Utils.asObjectOrNull(obj, BookLinkRefReferent)
        if (rr is not None): 
            if (rr.typ == BookLinkRefType.INLINE): 
                return MetaBookLinkRef.IMAGE_ID_INLINE
        return MetaBookLinkRef.IMAGE_ID
    
    _global_meta = None