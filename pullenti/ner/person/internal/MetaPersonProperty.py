# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.Referent import Referent
from pullenti.ner.person.PersonPropertyKind import PersonPropertyKind


class MetaPersonProperty(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        super().__init__()
        self.add_feature(PersonPropertyReferent.ATTR_NAME, "Наименование", 1, 1)
        self.add_feature(PersonPropertyReferent.ATTR_HIGHER, "Вышестоящее свойство", 0, 0)
        self.add_feature(PersonPropertyReferent.ATTR_ATTR, "Атрибут", 0, 0)
        self.add_feature(PersonPropertyReferent.ATTR_REF, "Ссылка на объект", 0, 1)
        self.add_feature(Referent.ATTR_GENERAL, "Обобщающее свойство", 1, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        return PersonPropertyReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Свойство персоны"
    
    PERSON_PROP_IMAGE_ID = "personprop"
    
    PERSON_PROP_KING_IMAGE_ID = "king"
    
    PERSON_PROP_BOSS_IMAGE_ID = "boss"
    
    PERSON_PROP_KIN_IMAGE_ID = "kin"
    
    PERSON_PROP_MILITARY_ID = "militaryrank"
    
    PERSON_PROP_NATION_ID = "nationality"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        ki = PersonPropertyKind.UNDEFINED
        if (isinstance(obj, PersonPropertyReferent)): 
            ki = (obj if isinstance(obj, PersonPropertyReferent) else None).kind
        if (ki == PersonPropertyKind.BOSS): 
            return MetaPersonProperty.PERSON_PROP_BOSS_IMAGE_ID
        if (ki == PersonPropertyKind.KING): 
            return MetaPersonProperty.PERSON_PROP_KING_IMAGE_ID
        if (ki == PersonPropertyKind.KIN): 
            return MetaPersonProperty.PERSON_PROP_KIN_IMAGE_ID
        if (ki == PersonPropertyKind.MILITARYRANK): 
            return MetaPersonProperty.PERSON_PROP_MILITARY_ID
        if (ki == PersonPropertyKind.NATIONALITY): 
            return MetaPersonProperty.PERSON_PROP_NATION_ID
        return MetaPersonProperty.PERSON_PROP_IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaPersonProperty
    @staticmethod
    def _static_ctor():
        MetaPersonProperty._global_meta = MetaPersonProperty()

MetaPersonProperty._static_ctor()