# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.Referent import Referent

class MetaOrganization(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        MetaOrganization._global_meta = MetaOrganization()
        MetaOrganization._global_meta.add_feature(OrganizationReferent.ATTR_NAME, "Название", 0, 0)
        MetaOrganization._global_meta.add_feature(OrganizationReferent.ATTR_TYPE, "Тип", 0, 0)
        MetaOrganization._global_meta.add_feature(OrganizationReferent.ATTR_EPONYM, "Эпоним (имени)", 0, 0)
        MetaOrganization._global_meta.add_feature(OrganizationReferent.ATTR_NUMBER, "Номер", 0, 1)
        MetaOrganization._global_meta.add_feature(OrganizationReferent.ATTR_HIGHER, "Вышестоящая организация", 0, 1)
        MetaOrganization._global_meta.add_feature(OrganizationReferent.ATTR_OWNER, "Объект-владелец", 0, 1)
        MetaOrganization._global_meta.add_feature(OrganizationReferent.ATTR_GEO, "Географический объект", 0, 1)
        MetaOrganization._global_meta.add_feature(Referent.ATTR_GENERAL, "Обобщающая организация", 0, 1)
        MetaOrganization._global_meta.add_feature(OrganizationReferent.ATTR_MISC, "Разное", 0, 0)
        MetaOrganization._global_meta.add_feature(OrganizationReferent.ATTR_PROFILE, "Профиль", 0, 0)
        MetaOrganization._global_meta.add_feature(OrganizationReferent.ATTR_MARKER, "Маркер", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        return OrganizationReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Организация"
    
    ORG_IMAGE_ID = "org"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        if (isinstance(obj, OrganizationReferent)): 
            prs = obj.profiles
            if (prs is not None and len(prs) > 0): 
                pr = prs[len(prs) - 1]
                return Utils.enumToString(pr)
        return MetaOrganization.ORG_IMAGE_ID
    
    _global_meta = None