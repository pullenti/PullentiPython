# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass

class MoneyMeta(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        MoneyMeta.GLOBAL_META = MoneyMeta()
        MoneyMeta.GLOBAL_META.add_feature(MoneyReferent.ATTR_CURRENCY, "Валюта", 1, 1)
        MoneyMeta.GLOBAL_META.add_feature(MoneyReferent.ATTR_VALUE, "Значение", 1, 1)
        MoneyMeta.GLOBAL_META.add_feature(MoneyReferent.ATTR_REST, "Остаток (100)", 0, 1)
        MoneyMeta.GLOBAL_META.add_feature(MoneyReferent.ATTR_ALTVALUE, "Другое значение", 1, 1)
        MoneyMeta.GLOBAL_META.add_feature(MoneyReferent.ATTR_ALTREST, "Другой остаток (100)", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        return MoneyReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Денежная сумма"
    
    IMAGE_ID = "sum"
    
    IMAGE2ID = "sumerr"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        m = Utils.asObjectOrNull(obj, MoneyReferent)
        if (m is not None): 
            if (m.alt_value is not None or m.alt_rest is not None): 
                return MoneyMeta.IMAGE2ID
        return MoneyMeta.IMAGE_ID
    
    GLOBAL_META = None