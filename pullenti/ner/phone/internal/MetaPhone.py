# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.Referent import Referent


class MetaPhone(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.phone.PhoneReferent import PhoneReferent
        super().__init__()
        self.addFeature(PhoneReferent.ATTR_NUNBER, "Номер", 1, 1)
        self.addFeature(PhoneReferent.ATTR_ADDNUMBER, "Добавочный номер", 0, 1)
        self.addFeature(PhoneReferent.ATTR_COUNTRYCODE, "Код страны", 0, 1)
        self.addFeature(Referent.ATTR_GENERAL, "Обобщающий номер", 0, 1)
        self.addFeature(PhoneReferent.ATTR_KIND, "Тип", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.phone.PhoneReferent import PhoneReferent
        return PhoneReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Телефонный номер"
    
    PHONE_IMAGE_ID = "phone"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MetaPhone.PHONE_IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaPhone
    @staticmethod
    def _static_ctor():
        MetaPhone._global_meta = MetaPhone()

MetaPhone._static_ctor()