# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass


class MetaWeapon(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.weapon.WeaponReferent import WeaponReferent
        super().__init__()
        self.add_feature(WeaponReferent.ATTR_TYPE, "Тип", 0, 0)
        self.add_feature(WeaponReferent.ATTR_NAME, "Название", 0, 0)
        self.add_feature(WeaponReferent.ATTR_NUMBER, "Номер", 0, 1)
        self.add_feature(WeaponReferent.ATTR_BRAND, "Марка", 0, 0)
        self.add_feature(WeaponReferent.ATTR_MODEL, "Модель", 0, 0)
        self.add_feature(WeaponReferent.ATTR_DATE, "Дата создания", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.weapon.WeaponReferent import WeaponReferent
        return WeaponReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Оружие"
    
    IMAGE_ID = "weapon"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaWeapon.IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaWeapon
    @staticmethod
    def _static_ctor():
        MetaWeapon._global_meta = MetaWeapon()

MetaWeapon._static_ctor()