# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.transport.TransportKind import TransportKind


class MetaTransport(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.transport.TransportReferent import TransportReferent
        super().__init__()
        self.addFeature(TransportReferent.ATTR_TYPE, "Тип", 0, 0)
        self.addFeature(TransportReferent.ATTR_NAME, "Название", 0, 0)
        self.addFeature(TransportReferent.ATTR_NUMBER, "Номер", 0, 1)
        self.addFeature(TransportReferent.ATTR_NUMBER_REGION, "Регион номера", 0, 1)
        self.addFeature(TransportReferent.ATTR_BRAND, "Марка", 0, 0)
        self.addFeature(TransportReferent.ATTR_MODEL, "Модель", 0, 0)
        self.addFeature(TransportReferent.ATTR_CLASS, "Класс", 0, 1)
        self.addFeature(TransportReferent.ATTR_KIND, "Категория", 1, 1)
        self.addFeature(TransportReferent.ATTR_STATE, "Государство", 0, 1)
        self.addFeature(TransportReferent.ATTR_ORG, "Организация", 0, 1)
        self.addFeature(TransportReferent.ATTR_DATE, "Дата создания", 0, 1)
        self.addFeature(TransportReferent.ATTR_ROUTEPOINT, "Пункт маршрута", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.transport.TransportReferent import TransportReferent
        return TransportReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Транспорт"
    
    IMAGE_ID = "tansport"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.transport.TransportReferent import TransportReferent
        if (isinstance(obj, TransportReferent)): 
            ok = (Utils.asObjectOrNull(obj, TransportReferent)).kind
            if (ok != TransportKind.UNDEFINED): 
                return Utils.enumToString(ok)
        return MetaTransport.IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaTransport
    @staticmethod
    def _static_ctor():
        MetaTransport._global_meta = MetaTransport()

MetaTransport._static_ctor()