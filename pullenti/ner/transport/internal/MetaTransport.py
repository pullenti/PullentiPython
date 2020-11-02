# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.transport.TransportKind import TransportKind

class MetaTransport(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.transport.TransportReferent import TransportReferent
        MetaTransport._global_meta = MetaTransport()
        MetaTransport._global_meta.add_feature(TransportReferent.ATTR_TYPE, "Тип", 0, 0)
        MetaTransport._global_meta.add_feature(TransportReferent.ATTR_NAME, "Название", 0, 0)
        MetaTransport._global_meta.add_feature(TransportReferent.ATTR_NUMBER, "Номер", 0, 1)
        MetaTransport._global_meta.add_feature(TransportReferent.ATTR_NUMBER_REGION, "Регион номера", 0, 1)
        MetaTransport._global_meta.add_feature(TransportReferent.ATTR_BRAND, "Марка", 0, 0)
        MetaTransport._global_meta.add_feature(TransportReferent.ATTR_MODEL, "Модель", 0, 0)
        MetaTransport._global_meta.add_feature(TransportReferent.ATTR_CLASS, "Класс", 0, 1)
        MetaTransport._global_meta.add_feature(TransportReferent.ATTR_KIND, "Категория", 1, 1)
        MetaTransport._global_meta.add_feature(TransportReferent.ATTR_GEO, "География", 0, 0)
        MetaTransport._global_meta.add_feature(TransportReferent.ATTR_ORG, "Организация", 0, 1)
        MetaTransport._global_meta.add_feature(TransportReferent.ATTR_DATE, "Дата создания", 0, 1)
        MetaTransport._global_meta.add_feature(TransportReferent.ATTR_ROUTEPOINT, "Пункт маршрута", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.transport.TransportReferent import TransportReferent
        return TransportReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Транспорт"
    
    IMAGE_ID = "tansport"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.transport.TransportReferent import TransportReferent
        if (isinstance(obj, TransportReferent)): 
            ok = obj.kind
            if (ok != TransportKind.UNDEFINED): 
                return Utils.enumToString(ok)
        return MetaTransport.IMAGE_ID
    
    _global_meta = None