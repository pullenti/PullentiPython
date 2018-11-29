# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.business.BusinessFactKind import BusinessFactKind


class MetaBusinessFact(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        super().__init__()
        self.kind_feature = None;
        f = self.addFeature(BusinessFactReferent.ATTR_KIND, "Класс", 0, 1)
        self.kind_feature = f
        f.addValue(Utils.enumToString(BusinessFactKind.CREATE), "Создавать", None, None)
        f.addValue(Utils.enumToString(BusinessFactKind.DELETE), "Удалять", None, None)
        f.addValue(Utils.enumToString(BusinessFactKind.HAVE), "Иметь", None, None)
        f.addValue(Utils.enumToString(BusinessFactKind.GET), "Приобретать", None, None)
        f.addValue(Utils.enumToString(BusinessFactKind.SELL), "Продавать", None, None)
        f.addValue(Utils.enumToString(BusinessFactKind.PROFIT), "Доход", None, None)
        f.addValue(Utils.enumToString(BusinessFactKind.DAMAGES), "Убытки", None, None)
        f.addValue(Utils.enumToString(BusinessFactKind.AGREEMENT), "Соглашение", None, None)
        f.addValue(Utils.enumToString(BusinessFactKind.SUBSIDIARY), "Дочернее предприятие", None, None)
        f.addValue(Utils.enumToString(BusinessFactKind.FINANCE), "Финансировать", None, None)
        f.addValue(Utils.enumToString(BusinessFactKind.LAWSUIT), "Судебный иск", None, None)
        self.addFeature(BusinessFactReferent.ATTR_TYPE, "Тип", 0, 1)
        self.addFeature(BusinessFactReferent.ATTR_WHO, "Кто", 0, 1).show_as_parent = True
        self.addFeature(BusinessFactReferent.ATTR_WHOM, "Кого\\Кому", 0, 1).show_as_parent = True
        self.addFeature(BusinessFactReferent.ATTR_WHEN, "Когда", 0, 1).show_as_parent = True
        self.addFeature(BusinessFactReferent.ATTR_WHAT, "Что", 0, 0).show_as_parent = True
        self.addFeature(BusinessFactReferent.ATTR_MISC, "Дополнительная информация", 0, 0).show_as_parent = True
    
    @property
    def name(self) -> str:
        from pullenti.ner.business.BusinessFactReferent import BusinessFactReferent
        return BusinessFactReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Бизнес-факт"
    
    IMAGE_ID = "businessfact"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MetaBusinessFact.IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class MetaBusinessFact
    @staticmethod
    def _static_ctor():
        MetaBusinessFact.GLOBAL_META = MetaBusinessFact()

MetaBusinessFact._static_ctor()