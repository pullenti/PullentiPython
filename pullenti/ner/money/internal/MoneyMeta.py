# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass


class MoneyMeta(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        super().__init__()
        self.add_feature(MoneyReferent.ATTR_CURRENCY, "Валюта", 1, 1)
        self.add_feature(MoneyReferent.ATTR_VALUE, "Значение", 1, 1)
        self.add_feature(MoneyReferent.ATTR_REST, "Остаток (100)", 0, 1)
        self.add_feature(MoneyReferent.ATTR_ALTVALUE, "Другое значение", 1, 1)
        self.add_feature(MoneyReferent.ATTR_ALTREST, "Другой остаток (100)", 0, 1)
    
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
        m = (obj if isinstance(obj, MoneyReferent) else None)
        if (m is not None): 
            if (m.alt_value is not None or m.alt_rest is not None): 
                return MoneyMeta.IMAGE2ID
        return MoneyMeta.IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class MoneyMeta
    @staticmethod
    def _static_ctor():
        MoneyMeta.GLOBAL_META = MoneyMeta()

MoneyMeta._static_ctor()