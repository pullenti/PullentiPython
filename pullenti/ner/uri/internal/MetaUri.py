# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass


class MetaUri(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.uri.UriReferent import UriReferent
        super().__init__()
        self.add_feature(UriReferent.ATTR_VALUE, "Значение", 0, 1)
        self.add_feature(UriReferent.ATTR_SCHEME, "Схема", 0, 1)
        self.add_feature(UriReferent.ATTR_DETAIL, "Детализация", 0, 1)
    
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
        web = (obj if isinstance(obj, UriReferent) else None)
        if (web is not None and web.scheme == "mailto"): 
            return MetaUri.MAIL_IMAGE_ID
        else: 
            return MetaUri.URI_IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaUri
    @staticmethod
    def _static_ctor():
        MetaUri._global_meta = MetaUri()

MetaUri._static_ctor()