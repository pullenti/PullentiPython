# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.Referent import Referent


class MetaOrganization(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        super().__init__()
        self.add_feature(OrganizationReferent.ATTR_NAME, "Название", 0, 0)
        self.add_feature(OrganizationReferent.ATTR_TYPE, "Тип", 0, 0)
        self.add_feature(OrganizationReferent.ATTR_EPONYM, "Эпоним (имени)", 0, 0)
        self.add_feature(OrganizationReferent.ATTR_NUMBER, "Номер", 0, 1)
        self.add_feature(OrganizationReferent.ATTR_HIGHER, "Вышестоящая организация", 0, 1)
        self.add_feature(OrganizationReferent.ATTR_OWNER, "Объект-владелец", 0, 1)
        self.add_feature(OrganizationReferent.ATTR_GEO, "Географический объект", 0, 1)
        self.add_feature(Referent.ATTR_GENERAL, "Обобщающая организация", 0, 1)
        self.add_feature(OrganizationReferent.ATTR_KLADR, "Код КЛАДР", 0, 1)
        self.add_feature(OrganizationReferent.ATTR_MISC, "Разное", 0, 0)
        self.add_feature(OrganizationReferent.ATTR_PROFILE, "Профиль", 0, 0)
    
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
            prs = (obj if isinstance(obj, OrganizationReferent) else None).profiles
            if (prs is not None and len(prs) > 0): 
                pr = prs[len(prs) - 1]
                return Utils.enumToString(pr)
        return MetaOrganization.ORG_IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaOrganization
    @staticmethod
    def _static_ctor():
        MetaOrganization._global_meta = MetaOrganization()

MetaOrganization._static_ctor()