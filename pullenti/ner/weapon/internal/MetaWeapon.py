# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass

class MetaWeapon(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.weapon.WeaponReferent import WeaponReferent
        MetaWeapon._global_meta = MetaWeapon()
        MetaWeapon._global_meta.add_feature(WeaponReferent.ATTR_TYPE, "Тип", 0, 0)
        MetaWeapon._global_meta.add_feature(WeaponReferent.ATTR_NAME, "Название", 0, 0)
        MetaWeapon._global_meta.add_feature(WeaponReferent.ATTR_NUMBER, "Номер", 0, 1)
        MetaWeapon._global_meta.add_feature(WeaponReferent.ATTR_BRAND, "Марка", 0, 0)
        MetaWeapon._global_meta.add_feature(WeaponReferent.ATTR_MODEL, "Модель", 0, 0)
        MetaWeapon._global_meta.add_feature(WeaponReferent.ATTR_DATE, "Дата создания", 0, 1)
        MetaWeapon._global_meta.add_feature(WeaponReferent.ATTR_CALIBER, "Калибр", 0, 1)
        MetaWeapon._global_meta.add_feature(WeaponReferent.ATTR_REF, "Ссылка", 0, 0)
    
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