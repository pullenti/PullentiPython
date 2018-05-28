# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.ner.old.DocumentBlockType import DocumentBlockType



class DocumentBlockReferent(Referent):
    """ Блок документа (часть, глава или весь документ целиком) """
    
    def __init__(self) -> None:
        from pullenti.ner.old.internal.MetaDocBlockInfo import MetaDocBlockInfo
        super().__init__(DocumentBlockReferent.OBJ_TYPENAME)
        self.instance_of = MetaDocBlockInfo._global_meta
    
    OBJ_TYPENAME = "DOCBLOCK"
    
    ATTR_NAME = "NAME"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_CONTENT = "CONTENT"
    
    ATTR_PARENT = "PARENT"
    
    ATTR_CHILD = "CHILD"
    
    ATTR_TYPE = "TYPE"
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        res = Utils.newStringIO(None)
        str0 = self.get_string_value(DocumentBlockReferent.ATTR_NUMBER)
        if ((str0) is not None): 
            print("{0}) ".format(str0), end="", file=res, flush=True)
        if (self.typ != DocumentBlockType.UNDEFINED): 
            print("{0}: ".format(Utils.enumToString(self.typ)), end="", file=res, flush=True)
        str0 = self.get_string_value(DocumentBlockReferent.ATTR_NAME)
        if ((str0) is not None): 
            print(MiscHelper.convert_first_char_upper_and_other_lower(str0), end="", file=res)
        else: 
            str0 = self.get_string_value(DocumentBlockReferent.ATTR_CONTENT)
            if ((str0) is not None): 
                sp = True
                for ch in str0: 
                    if (Utils.isWhitespace(ch)): 
                        if (res.tell() > 100): 
                            print("...", end="", file=res)
                            break
                        if (not sp): 
                            print(' ', end="", file=res)
                            sp = True
                    else: 
                        print(ch, end="", file=res)
                        sp = False
        if (res.tell() == 0): 
            print("?", end="", file=res)
        return Utils.toStringStringIO(res)
    
    @property
    def parent_referent(self) -> 'Referent':
        return (self.get_value(DocumentBlockReferent.ATTR_PARENT) if isinstance(self.get_value(DocumentBlockReferent.ATTR_PARENT), Referent) else None)
    
    def _add_parent(self, value : 'Referent') -> None:
        if (value == self.parent_referent): 
            return
        self.add_slot(DocumentBlockReferent.ATTR_PARENT, value, True, 0)
        if (value is not None): 
            value.add_slot(DocumentBlockReferent.ATTR_CHILD, self, False, 0)
    
    @property
    def children(self) -> typing.List['DocumentBlockReferent']:
        res = list()
        for s in self.slots: 
            if (s.type_name == DocumentBlockReferent.ATTR_CHILD): 
                if (isinstance(s.value, DocumentBlockReferent)): 
                    res.append(s.value if isinstance(s.value, DocumentBlockReferent) else None)
        return res
    
    @property
    def typ(self) -> 'DocumentBlockType':
        s = self.get_string_value(DocumentBlockReferent.ATTR_TYPE)
        if (s is None): 
            return DocumentBlockType.UNDEFINED
        try: 
            res = Utils.valToEnum(s, DocumentBlockType)
            if (isinstance(res, DocumentBlockType)): 
                return Utils.valToEnum(res, DocumentBlockType)
        except Exception as ex1477: 
            pass
        return DocumentBlockType.UNDEFINED
    
    @typ.setter
    def typ(self, value) -> 'DocumentBlockType':
        if (value == DocumentBlockType.UNDEFINED): 
            self.add_slot(DocumentBlockReferent.ATTR_TYPE, None, True, 0)
        else: 
            self.add_slot(DocumentBlockReferent.ATTR_TYPE, Utils.enumToString(value), True, 0)
        return value
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        return obj == self

    
    @staticmethod
    def _new1478(_arg1 : 'DocumentBlockType') -> 'DocumentBlockReferent':
        res = DocumentBlockReferent()
        res.typ = _arg1
        return res