# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.Referent import Referent

class MetaPhone(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.phone.PhoneReferent import PhoneReferent
        MetaPhone._global_meta = MetaPhone()
        MetaPhone._global_meta.add_feature(PhoneReferent.ATTR_NUNBER, "Номер", 1, 1)
        MetaPhone._global_meta.add_feature(PhoneReferent.ATTR_ADDNUMBER, "Добавочный номер", 0, 1)
        MetaPhone._global_meta.add_feature(PhoneReferent.ATTR_COUNTRYCODE, "Код страны", 0, 1)
        MetaPhone._global_meta.add_feature(Referent.ATTR_GENERAL, "Обобщающий номер", 0, 1)
        MetaPhone._global_meta.add_feature(PhoneReferent.ATTR_KIND, "Тип", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.phone.PhoneReferent import PhoneReferent
        return PhoneReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Телефонный номер"
    
    PHONE_IMAGE_ID = "phone"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaPhone.PHONE_IMAGE_ID
    
    _global_meta = None