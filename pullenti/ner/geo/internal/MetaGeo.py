﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.ner.ReferentClass import ReferentClass

class MetaGeo(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.geo.GeoReferent import GeoReferent
        MetaGeo._global_meta = MetaGeo()
        MetaGeo._global_meta.add_feature(GeoReferent.ATTR_NAME, "Наименование", 1, 0)
        MetaGeo._global_meta.add_feature(GeoReferent.ATTR_TYPE, "Тип", 1, 0)
        MetaGeo._global_meta.add_feature(GeoReferent.ATTR_ALPHA2, "Код страны", 0, 1)
        MetaGeo._global_meta.add_feature(GeoReferent.ATTR_HIGHER, "Вышестоящий объект", 0, 1)
        MetaGeo._global_meta.add_feature(GeoReferent.ATTR_REF, "Ссылка на объект", 0, 1)
        MetaGeo._global_meta.add_feature(GeoReferent.ATTR_FIAS, "Объект ФИАС", 0, 1)
        MetaGeo._global_meta.add_feature(GeoReferent.ATTR_BTI, "Код БТИ", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.geo.GeoReferent import GeoReferent
        return GeoReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Территориальное образование"
    
    COUNTRY_CITY_IMAGE_ID = "countrycity"
    
    COUNTRY_IMAGE_ID = "country"
    
    CITY_IMAGE_ID = "city"
    
    DISTRICT_IMAGE_ID = "district"
    
    REGION_IMAGE_ID = "region"
    
    TERR_IMAGE_ID = "territory"
    
    UNION_IMAGE_ID = "union"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.geo.GeoReferent import GeoReferent
        ter = Utils.asObjectOrNull(obj, GeoReferent)
        if (ter is not None): 
            if (ter.is_union0): 
                return MetaGeo.UNION_IMAGE_ID
            if (ter.is_city0 and ((ter.is_state0 or ter.is_region0))): 
                return MetaGeo.COUNTRY_CITY_IMAGE_ID
            if (ter.is_state0): 
                return MetaGeo.COUNTRY_IMAGE_ID
            if (ter.is_city0): 
                return MetaGeo.CITY_IMAGE_ID
            if (ter.is_region0 and ter.higher is not None and ter.higher.is_city0): 
                return MetaGeo.DISTRICT_IMAGE_ID
            if (ter.is_territory0): 
                return MetaGeo.TERR_IMAGE_ID
        return MetaGeo.REGION_IMAGE_ID
    
    _global_meta = None