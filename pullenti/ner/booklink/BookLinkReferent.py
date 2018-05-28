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



class BookLinkReferent(Referent):
    """ Ссылка на внешний литературный источник (статью, книгу и пр.) """
    
    OBJ_TYPENAME = "BOOKLINK"
    
    ATTR_AUTHOR = "AUTHOR"
    
    ATTR_NAME = "NAME"
    
    ATTR_YEAR = "YEAR"
    
    ATTR_LANG = "LANG"
    
    ATTR_GEO = "GEO"
    
    ATTR_URL = "URL"
    
    ATTR_MISC = "MISC"
    
    ATTR_TYPE = "TYPE"
    
    def __init__(self) -> None:
        from pullenti.ner.booklink.internal.MetaBookLink import MetaBookLink
        super().__init__(BookLinkReferent.OBJ_TYPENAME)
        self.instance_of = MetaBookLink._global_meta
    
    def to_string(self, short_variant : bool, lang_ : 'MorphLang'=MorphLang(), lev : int=0) -> str:
        from pullenti.ner.uri.UriReferent import UriReferent
        res = Utils.newStringIO(None)
        a = self.get_value(BookLinkReferent.ATTR_AUTHOR)
        if (a is not None): 
            for s in self.slots: 
                if (s.type_name == BookLinkReferent.ATTR_AUTHOR): 
                    if (a != s.value): 
                        print(", ", end="", file=res)
                    if (isinstance(s.value, Referent)): 
                        print((s.value if isinstance(s.value, Referent) else None).to_string(True, lang_, lev + 1), end="", file=res)
                    elif (isinstance(s.value, str)): 
                        print(s.value if isinstance(s.value, str) else None, end="", file=res)
            if (self.authors_and_other): 
                print(" и др.", end="", file=res)
        nam = self.name
        if (nam is not None): 
            if (res.tell() > 0): 
                print(' ', end="", file=res)
            if (len(nam) > 200): 
                nam = (nam[0 : 200] + "...")
            print("\"{0}\"".format(nam), end="", file=res, flush=True)
        uri = (self.get_value(BookLinkReferent.ATTR_URL) if isinstance(self.get_value(BookLinkReferent.ATTR_URL), UriReferent) else None)
        if (uri is not None): 
            print(" [{0}]".format(str(uri)), end="", file=res, flush=True)
        if (self.year > 0): 
            print(", {0}".format(self.year), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def name(self) -> str:
        return self.get_string_value(BookLinkReferent.ATTR_NAME)
    
    @name.setter
    def name(self, value) -> str:
        self.add_slot(BookLinkReferent.ATTR_NAME, value, True, 0)
        return value
    
    @property
    def lang(self) -> str:
        return self.get_string_value(BookLinkReferent.ATTR_LANG)
    
    @lang.setter
    def lang(self, value) -> str:
        self.add_slot(BookLinkReferent.ATTR_LANG, value, True, 0)
        return value
    
    @property
    def typ(self) -> str:
        return self.get_string_value(BookLinkReferent.ATTR_TYPE)
    
    @typ.setter
    def typ(self, value) -> str:
        self.add_slot(BookLinkReferent.ATTR_TYPE, value, True, 0)
        return value
    
    @property
    def url(self) -> 'UriReferent':
        from pullenti.ner.uri.UriReferent import UriReferent
        return (self.get_value(BookLinkReferent.ATTR_URL) if isinstance(self.get_value(BookLinkReferent.ATTR_URL), UriReferent) else None)
    
    @property
    def year(self) -> int:
        inoutarg395 = RefOutArgWrapper(None)
        inoutres396 = Utils.tryParseInt(Utils.ifNotNull(self.get_string_value(BookLinkReferent.ATTR_YEAR), ""), inoutarg395)
        year_ = inoutarg395.value
        if (inoutres396): 
            return year_
        else: 
            return 0
    
    @year.setter
    def year(self, value) -> int:
        self.add_slot(BookLinkReferent.ATTR_YEAR, str(value), True, 0)
        return value
    
    @property
    def authors_and_other(self) -> bool:
        return self.find_slot(BookLinkReferent.ATTR_MISC, "и др.", True) is not None
    
    @authors_and_other.setter
    def authors_and_other(self, value) -> bool:
        self.add_slot(BookLinkReferent.ATTR_MISC, "и др.", False, 0)
        return value
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        from pullenti.ner.core.MiscHelper import MiscHelper
        br = (obj if isinstance(obj, BookLinkReferent) else None)
        if (br is None): 
            return False
        eq = 0
        if (self.year > 0 and br.year > 0): 
            if (self.year == br.year): 
                eq += 1
            else: 
                return False
        if (self.typ is not None and br.typ is not None): 
            if (self.typ != br.typ): 
                return False
        eq_auth = False
        if (self.find_slot(BookLinkReferent.ATTR_AUTHOR, None, True) is not None and br.find_slot(BookLinkReferent.ATTR_AUTHOR, None, True) is not None): 
            ok = False
            for a in self.slots: 
                if (a.type_name == BookLinkReferent.ATTR_AUTHOR): 
                    if (br.find_slot(BookLinkReferent.ATTR_AUTHOR, a.value, True) is not None): 
                        eq += 1
                        ok = True
                        eq_auth = True
            if (not ok): 
                return False
        if (br.name != self.name): 
            if (self.name is None or br.name is None): 
                return False
            if (self.name.startswith(br.name) or br.name.startswith(self.name)): 
                eq += 1
            elif (eq_auth and MiscHelper.can_be_equals(self.name, br.name, False, True, False)): 
                eq += 1
            else: 
                return False
        else: 
            eq += 2
        return eq > 2