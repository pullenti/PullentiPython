# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass

class MetaUri(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.uri.UriReferent import UriReferent
        MetaUri._global_meta = MetaUri()
        MetaUri._global_meta.add_feature(UriReferent.ATTR_VALUE, "Значение", 0, 1)
        MetaUri._global_meta.add_feature(UriReferent.ATTR_SCHEME, "Схема", 0, 1)
        MetaUri._global_meta.add_feature(UriReferent.ATTR_DETAIL, "Детализация", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.uri.UriReferent import UriReferent
        return UriReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "URI"
    
    MAIL_IMAGE_ID = "mail"
    
    URI_IMAGE_ID = "uri"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.uri.UriReferent import UriReferent
        web = Utils.asObjectOrNull(obj, UriReferent)
        if (web is not None and web.scheme == "mailto"): 
            return MetaUri.MAIL_IMAGE_ID
        else: 
            return MetaUri.URI_IMAGE_ID
    
    _global_meta = None