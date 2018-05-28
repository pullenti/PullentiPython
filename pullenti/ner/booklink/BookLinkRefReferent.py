# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.Referent import Referent
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.booklink.BookLinkRefType import BookLinkRefType



class BookLinkRefReferent(Referent):
    """ Ссылка на внешний литературный источник (статью, книгу и пр.) """
    
    OBJ_TYPENAME = "BOOKLINKREF"
    
    ATTR_BOOK = "BOOK"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_PAGES = "PAGES"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_MISC = "MISC"
    
    def __init__(self) -> None:
        from pullenti.ner.booklink.internal.MetaBookLinkRef import MetaBookLinkRef
        super().__init__(BookLinkRefReferent.OBJ_TYPENAME)
        self.instance_of = MetaBookLinkRef._global_meta
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=MorphLang(), lev : int=0) -> str:
        res = Utils.newStringIO(None)
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
        return (self.get_value(BookLinkRefReferent.ATTR_BOOK) if isinstance(self.get_value(BookLinkRefReferent.ATTR_BOOK), Referent) else None)
    
    @property
    def typ(self) -> 'BookLinkRefType':
        """ Тип ссылки """
        val = self.get_string_value(BookLinkRefReferent.ATTR_TYPE)
        if (val is None): 
            return BookLinkRefType.UNDEFINED
        try: 
            return Utils.valToEnum(val, BookLinkRefType)
        except Exception as ex397: 
            pass
        return BookLinkRefType.UNDEFINED
    
    @typ.setter
    def typ(self, value) -> 'BookLinkRefType':
        self.add_slot(BookLinkRefReferent.ATTR_TYPE, Utils.enumToString(value), True, 0)
        return value
    
    @property
    def book(self) -> 'Referent':
        """ Собственно ссылка вовне на источник - BookLinkReferent или DecreeReferent """
        return (self.get_value(BookLinkRefReferent.ATTR_BOOK) if isinstance(self.get_value(BookLinkRefReferent.ATTR_BOOK), Referent) else None)
    
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
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        r = (obj if isinstance(obj, BookLinkRefReferent) else None)
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
            r1(Referent): 
            r2(Referent): 
        
        """
        num1 = r1.get_string_value(BookLinkRefReferent.ATTR_NUMBER)
        num2 = r2.get_string_value(BookLinkRefReferent.ATTR_NUMBER)
        if (num1 is None or num2 is None): 
            return None
        inoutarg398 = RefOutArgWrapper(None)
        inoutres399 = Utils.tryParseInt(num1, inoutarg398)
        inoutarg400 = RefOutArgWrapper(None)
        inoutres401 = Utils.tryParseInt(num2, inoutarg400)
        n1 = inoutarg398.value
        n2 = inoutarg400.value
        if (not inoutres399 or not inoutres401): 
            return None
        return n2 - n1

    
    @staticmethod
    def _new389(_arg1 : 'Referent') -> 'BookLinkRefReferent':
        res = BookLinkRefReferent()
        res.book = _arg1
        return res