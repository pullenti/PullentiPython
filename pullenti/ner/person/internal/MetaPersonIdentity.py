# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.ner.ReferentClass import ReferentClass

class MetaPersonIdentity(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent
        MetaPersonIdentity._global_meta = MetaPersonIdentity()
        MetaPersonIdentity._global_meta.addFeature(PersonIdentityReferent.ATTR_TYPE, "Тип", 1, 1)
        MetaPersonIdentity._global_meta.addFeature(PersonIdentityReferent.ATTR_NUMBER, "Номер", 1, 1)
        MetaPersonIdentity._global_meta.addFeature(PersonIdentityReferent.ATTR_DATE, "Дата выдачи", 0, 1)
        MetaPersonIdentity._global_meta.addFeature(PersonIdentityReferent.ATTR_ORG, "Кто выдал", 0, 1)
        MetaPersonIdentity._global_meta.addFeature(PersonIdentityReferent.ATTR_ADDRESS, "Адрес регистрации", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent
        return PersonIdentityReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Удостоверение личности"
    
    IMAGE_ID = "identity"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MetaPersonIdentity.IMAGE_ID
    
    _global_meta = None