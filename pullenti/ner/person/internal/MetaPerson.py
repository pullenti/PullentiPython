# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.Referent import Referent


class MetaPerson(ReferentClass):
    
    ATTR_SEXMALE = "MALE"
    
    ATTR_SEXFEMALE = "FEMALE"
    
    def __init__(self) -> None:
        from pullenti.ner.person.PersonReferent import PersonReferent
        super().__init__()
        self.add_feature(PersonReferent.ATTR_IDENTITY, "Идентификация", 0, 0)
        sex = self.add_feature(PersonReferent.ATTR_SEX, "Пол", 0, 0)
        sex.add_value(MetaPerson.ATTR_SEXMALE, "мужской", None, None)
        sex.add_value(MetaPerson.ATTR_SEXFEMALE, "женский", None, None)
        self.add_feature(PersonReferent.ATTR_LASTNAME, "Фамилия", 0, 0)
        self.add_feature(PersonReferent.ATTR_FIRSTNAME, "Имя", 0, 0)
        self.add_feature(PersonReferent.ATTR_MIDDLENAME, "Отчество", 0, 0)
        self.add_feature(PersonReferent.ATTR_NICKNAME, "Псевдоним", 0, 0)
        self.add_feature(PersonReferent.ATTR_ATTR, "Свойство", 0, 0)
        self.add_feature(PersonReferent.ATTR_AGE, "Возраст", 0, 1)
        self.add_feature(PersonReferent.ATTR_BORN, "Родился", 0, 1)
        self.add_feature(PersonReferent.ATTR_DIE, "Умер", 0, 1)
        self.add_feature(PersonReferent.ATTR_CONTACT, "Контактные данные", 0, 0)
        self.add_feature(PersonReferent.ATTR_IDDOC, "Удостоверение личности", 0, 0).show_as_parent = True
        self.add_feature(Referent.ATTR_GENERAL, "Обобщающая персона", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.person.PersonReferent import PersonReferent
        return PersonReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Персона"
    
    MAN_IMAGE_ID = "man"
    
    WOMEN_IMAGE_ID = "women"
    
    PERSON_IMAGE_ID = "person"
    
    GENERAL_IMAGE_ID = "general"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.person.PersonReferent import PersonReferent
        pers = (obj if isinstance(obj, PersonReferent) else None)
        if (pers is not None): 
            if (pers.find_slot("@GENERAL", None, True) is not None): 
                return MetaPerson.GENERAL_IMAGE_ID
            if (pers.is_male): 
                return MetaPerson.MAN_IMAGE_ID
            if (pers.is_female): 
                return MetaPerson.WOMEN_IMAGE_ID
        return MetaPerson.PERSON_IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaPerson
    @staticmethod
    def _static_ctor():
        MetaPerson._global_meta = MetaPerson()

MetaPerson._static_ctor()