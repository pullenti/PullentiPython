# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.business.FundsKind import FundsKind


class FundsMeta(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.business.FundsReferent import FundsReferent
        super().__init__()
        self.kind_feature = None;
        f = self.addFeature(FundsReferent.ATTR_KIND, "Класс", 0, 1)
        self.kind_feature = f
        f.addValue(Utils.enumToString(FundsKind.STOCK), "Акция", None, None)
        f.addValue(Utils.enumToString(FundsKind.CAPITAL), "Уставной капитал", None, None)
        self.addFeature(FundsReferent.ATTR_TYPE, "Тип", 0, 1)
        self.addFeature(FundsReferent.ATTR_SOURCE, "Эмитент", 0, 1)
        self.addFeature(FundsReferent.ATTR_PERCENT, "Процент", 0, 1)
        self.addFeature(FundsReferent.ATTR_COUNT, "Количество", 0, 1)
        self.addFeature(FundsReferent.ATTR_PRICE, "Номинал", 0, 1)
        self.addFeature(FundsReferent.ATTR_SUM, "Денежная сумма", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.business.FundsReferent import FundsReferent
        return FundsReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Ценная бумага"
    
    IMAGE_ID = "funds"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return FundsMeta.IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class FundsMeta
    @staticmethod
    def _static_ctor():
        FundsMeta.GLOBAL_META = FundsMeta()

FundsMeta._static_ctor()