# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.booklink.BookLinkRefType import BookLinkRefType
from pullenti.ner.Referent import Referent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.booklink.internal.MetaBookLinkRef import MetaBookLinkRef

class BookLinkRefReferent(Referent):
    """ Ссылка на ССЫЛКУ (BookLinkReferent или DecreeReferent)
    
    """
    
    OBJ_TYPENAME = "BOOKLINKREF"
    """ Имя типа сущности TypeName ("BOOKLINKREF") """
    
    ATTR_BOOK = "BOOK"
    """ Имя атрибута - источник (BookLinkReferent или DecreeReferent) """
    
    ATTR_TYPE = "TYPE"
    """ Имя атрибута - тип (BookLinkRefType) """
    
    ATTR_PAGES = "PAGES"
    """ Имя атрибута - ссылка на страницу или диапазон страниц """
    
    ATTR_NUMBER = "NUMBER"
    """ Имя атрибута - порядковый номер в списке """
    
    ATTR_MISC = "MISC"
    """ Имя атрибута - разное """
    
    def __init__(self) -> None:
        super().__init__(BookLinkRefReferent.OBJ_TYPENAME)
        self.instance_of = MetaBookLinkRef._global_meta
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        if (self.number is not None): 
            print("[{0}] ".format(self.number), end="", file=res, flush=True)
        if (self.pages is not None): 
            print("{0} {1}; ".format(("pages" if lang is not None and lang.is_en else "стр."), self.pages), end="", file=res, flush=True)
        book_ = self.book
        if (book_ is None): 
            print("?", end="", file=res)
        else: 
            print(book_.to_string(short_variant, lang, lev), end="", file=res)
        return Utils.toStringStringIO(res)
    
    @property
    def parent_referent(self) -> 'Referent':
        return Utils.asObjectOrNull(self.get_slot_value(BookLinkRefReferent.ATTR_BOOK), Referent)
    
    @property
    def typ(self) -> 'BookLinkRefType':
        """ Тип ссылки """
        val = self.get_string_value(BookLinkRefReferent.ATTR_TYPE)
        if (val is None): 
            return BookLinkRefType.UNDEFINED
        try: 
            return Utils.valToEnum(val, BookLinkRefType)
        except Exception as ex380: 
            pass
        return BookLinkRefType.UNDEFINED
    @typ.setter
    def typ(self, value) -> 'BookLinkRefType':
        self.add_slot(BookLinkRefReferent.ATTR_TYPE, Utils.enumToString(value), True, 0)
        return value
    
    @property
    def book(self) -> 'Referent':
        """ Собственно ссылка вовне на источник - BookLinkReferent или DecreeReferent """
        return Utils.asObjectOrNull(self.get_slot_value(BookLinkRefReferent.ATTR_BOOK), Referent)
    @book.setter
    def book(self, value) -> 'Referent':
        self.add_slot(BookLinkRefReferent.ATTR_BOOK, value, True, 0)
        return value
    
    @property
    def number(self) -> str:
        """ Порядковый номер в списке """
        return self.get_string_value(BookLinkRefReferent.ATTR_NUMBER)
    @number.setter
    def number(self, value) -> str:
        num = value
        if (num is not None and num.find('-') > 0): 
            num = num.replace(" - ", "-")
        self.add_slot(BookLinkRefReferent.ATTR_NUMBER, num, True, 0)
        return value
    
    @property
    def pages(self) -> str:
        """ Ссылка на страницу или диапазон страниц """
        return self.get_string_value(BookLinkRefReferent.ATTR_PAGES)
    @pages.setter
    def pages(self, value) -> str:
        self.add_slot(BookLinkRefReferent.ATTR_PAGES, value, True, 0)
        return value
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        r = Utils.asObjectOrNull(obj, BookLinkRefReferent)
        if (r is None): 
            return False
        if (self.book != r.book): 
            return False
        if (self.number != r.number): 
            return False
        if (self.pages != r.pages): 
            return False
        if (((self.typ == BookLinkRefType.INLINE)) != ((r.typ == BookLinkRefType.INLINE))): 
            return False
        return True
    
    @staticmethod
    def get_number_diff(r1 : 'Referent', r2 : 'Referent') -> int:
        """ Возвращает разницу номеров r2 - r1, иначе null, если номеров нет
        
        Args:
            r1(Referent): первая ссылка
            r2(Referent): вторая ссылка
        
        """
        num1 = r1.get_string_value(BookLinkRefReferent.ATTR_NUMBER)
        num2 = r2.get_string_value(BookLinkRefReferent.ATTR_NUMBER)
        if (num1 is None or num2 is None): 
            return None
        wrapn1381 = RefOutArgWrapper(0)
        inoutres382 = Utils.tryParseInt(num1, wrapn1381)
        wrapn2383 = RefOutArgWrapper(0)
        inoutres384 = Utils.tryParseInt(num2, wrapn2383)
        n1 = wrapn1381.value
        n2 = wrapn2383.value
        if (not inoutres382 or not inoutres384): 
            return None
        return n2 - n1
    
    @staticmethod
    def _new372(_arg1 : 'Referent') -> 'BookLinkRefReferent':
        res = BookLinkRefReferent()
        res.book = _arg1
        return res