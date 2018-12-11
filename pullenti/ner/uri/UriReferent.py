# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.uri.internal.MetaUri import MetaUri

class UriReferent(Referent):
    """ URI, а также ISBN, УДК, ББК, ICQ и пр. """
    
    def __init__(self) -> None:
        super().__init__(UriReferent.OBJ_TYPENAME)
        self.instance_of = MetaUri._global_meta
    
    OBJ_TYPENAME = "URI"
    
    ATTR_VALUE = "VALUE"
    
    ATTR_DETAIL = "DETAIL"
    
    ATTR_SCHEME = "SCHEME"
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        if (self.scheme is not None): 
            split = ":"
            if (self.scheme == "ISBN" or self.scheme == "ББК" or self.scheme == "УДК"): 
                split = " "
            elif (self.scheme == "http" or self.scheme == "ftp" or self.scheme == "https"): 
                split = "://"
            return "{0}{1}{2}".format(self.scheme, split, Utils.ifNotNull(self.value, "?"))
        else: 
            return self.value
    
    @property
    def value(self) -> str:
        """ Значение """
        return self.getStringValue(UriReferent.ATTR_VALUE)
    @value.setter
    def value(self, value_) -> str:
        val = value_
        self.addSlot(UriReferent.ATTR_VALUE, val, True, 0)
        return value_
    
    @property
    def scheme(self) -> str:
        """ Схема """
        return self.getStringValue(UriReferent.ATTR_SCHEME)
    @scheme.setter
    def scheme(self, value_) -> str:
        self.addSlot(UriReferent.ATTR_SCHEME, value_, True, 0)
        return value_
    
    @property
    def detail(self) -> str:
        """ Детализация кода (если есть) """
        return self.getStringValue(UriReferent.ATTR_DETAIL)
    @detail.setter
    def detail(self, value_) -> str:
        self.addSlot(UriReferent.ATTR_DETAIL, value_, True, 0)
        return value_
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType') -> bool:
        uri_ = Utils.asObjectOrNull(obj, UriReferent)
        if (uri_ is None): 
            return False
        return Utils.compareStrings(self.value, uri_.value, True) == 0
    
    @staticmethod
    def _new2569(_arg1 : str, _arg2 : str) -> 'UriReferent':
        res = UriReferent()
        res.scheme = _arg1
        res.value = _arg2
        return res
    
    @staticmethod
    def _new2572(_arg1 : str, _arg2 : str) -> 'UriReferent':
        res = UriReferent()
        res.value = _arg1
        res.scheme = _arg2
        return res