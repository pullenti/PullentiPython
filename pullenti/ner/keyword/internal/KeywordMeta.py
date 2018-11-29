﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.keyword.KeywordType import KeywordType


class KeywordMeta(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.keyword.KeywordReferent import KeywordReferent
        super().__init__()
        self.addFeature(KeywordReferent.ATTR_TYPE, "Тип", 1, 1)
        self.addFeature(KeywordReferent.ATTR_VALUE, "Значение", 1, 0)
        self.addFeature(KeywordReferent.ATTR_NORMAL, "Нормализация", 1, 0)
        self.addFeature(KeywordReferent.ATTR_REF, "Ссылка", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.keyword.KeywordReferent import KeywordReferent
        return KeywordReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Ключевое слово"
    
    IMAGE_OBJ = "kwobject"
    
    IMAGE_PRED = "kwpredicate"
    
    IMAGE_REF = "kwreferent"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.keyword.KeywordReferent import KeywordReferent
        m = Utils.asObjectOrNull(obj, KeywordReferent)
        if (m is not None): 
            if (m.typ == KeywordType.PREDICATE): 
                return KeywordMeta.IMAGE_PRED
            if (m.typ == KeywordType.REFERENT): 
                return KeywordMeta.IMAGE_REF
        return KeywordMeta.IMAGE_OBJ
    
    GLOBAL_META = None
    
    # static constructor for class KeywordMeta
    @staticmethod
    def _static_ctor():
        KeywordMeta.GLOBAL_META = KeywordMeta()

KeywordMeta._static_ctor()