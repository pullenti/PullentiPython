# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.business.FundsKind import FundsKind


class FundsMeta(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.business.FundsReferent import FundsReferent
        self.kind_feature = None
        super().__init__()
        f = self.add_feature(FundsReferent.ATTR_KIND, "Класс", 0, 1)
        self.kind_feature = f
        f.add_value(Utils.enumToString(FundsKind.STOCK), "Акция", None, None)
        f.add_value(Utils.enumToString(FundsKind.CAPITAL), "Уставной капитал", None, None)
        self.add_feature(FundsReferent.ATTR_TYPE, "Тип", 0, 1)
        self.add_feature(FundsReferent.ATTR_SOURCE, "Эмитент", 0, 1)
        self.add_feature(FundsReferent.ATTR_PERCENT, "Процент", 0, 1)
        self.add_feature(FundsReferent.ATTR_COUNT, "Количество", 0, 1)
        self.add_feature(FundsReferent.ATTR_PRICE, "Номинал", 0, 1)
        self.add_feature(FundsReferent.ATTR_SUM, "Денежная сумма", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.business.FundsReferent import FundsReferent
        return FundsReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Ценная бумага"
    
    IMAGE_ID = "funds"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return FundsMeta.IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class FundsMeta
    @staticmethod
    def _static_ctor():
        FundsMeta.GLOBAL_META = FundsMeta()

FundsMeta._static_ctor()