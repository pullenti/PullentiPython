# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.keyword.KeywordType import KeywordType

class KeywordMeta(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.keyword.KeywordReferent import KeywordReferent
        KeywordMeta.GLOBAL_META = KeywordMeta()
        KeywordMeta.GLOBAL_META.add_feature(KeywordReferent.ATTR_TYPE, "Тип", 1, 1)
        KeywordMeta.GLOBAL_META.add_feature(KeywordReferent.ATTR_VALUE, "Значение", 1, 0)
        KeywordMeta.GLOBAL_META.add_feature(KeywordReferent.ATTR_NORMAL, "Нормализация", 1, 0)
        KeywordMeta.GLOBAL_META.add_feature(KeywordReferent.ATTR_REF, "Ссылка", 0, 0)
    
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
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.keyword.KeywordReferent import KeywordReferent
        m = Utils.asObjectOrNull(obj, KeywordReferent)
        if (m is not None): 
            if (m.typ == KeywordType.PREDICATE): 
                return KeywordMeta.IMAGE_PRED
            if (m.typ == KeywordType.REFERENT): 
                return KeywordMeta.IMAGE_REF
        return KeywordMeta.IMAGE_OBJ
    
    GLOBAL_META = None