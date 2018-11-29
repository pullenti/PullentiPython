# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.ner.address.AddressDetailType import AddressDetailType


class MetaAddress(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.address.AddressReferent import AddressReferent
        super().__init__()
        self.detail_feature = None;
        self.house_type_feature = None;
        self.building_type_feature = None;
        self.addFeature(AddressReferent.ATTR_STREET, "Улица", 0, 2)
        self.addFeature(AddressReferent.ATTR_HOUSE, "Дом", 0, 1)
        self.house_type_feature = self.addFeature(AddressReferent.ATTR_HOUSETYPE, "Тип дома", 0, 1)
        self.house_type_feature.addValue(Utils.enumToString(AddressHouseType.ESTATE), "Владение", None, None)
        self.house_type_feature.addValue(Utils.enumToString(AddressHouseType.HOUSE), "Дом", None, None)
        self.house_type_feature.addValue(Utils.enumToString(AddressHouseType.HOUSEESTATE), "Домовладение", None, None)
        self.addFeature(AddressReferent.ATTR_BUILDING, "Строение", 0, 1)
        self.building_type_feature = self.addFeature(AddressReferent.ATTR_BUILDINGTYPE, "Тип строения", 0, 1)
        self.building_type_feature.addValue(Utils.enumToString(AddressBuildingType.BUILDING), "Строение", None, None)
        self.building_type_feature.addValue(Utils.enumToString(AddressBuildingType.CONSTRUCTION), "Сооружение", None, None)
        self.building_type_feature.addValue(Utils.enumToString(AddressBuildingType.LITER), "Литера", None, None)
        self.addFeature(AddressReferent.ATTR_CORPUS, "Корпус", 0, 1)
        self.addFeature(AddressReferent.ATTR_PORCH, "Подъезд", 0, 1)
        self.addFeature(AddressReferent.ATTR_FLOOR, "Этаж", 0, 1)
        self.addFeature(AddressReferent.ATTR_FLAT, "Квартира", 0, 1)
        self.addFeature(AddressReferent.ATTR_CORPUSORFLAT, "Корпус или квартира", 0, 1)
        self.addFeature(AddressReferent.ATTR_OFFICE, "Офис", 0, 1)
        self.addFeature(AddressReferent.ATTR_PLOT, "Участок", 0, 1)
        self.addFeature(AddressReferent.ATTR_BLOCK, "Блок", 0, 1)
        self.addFeature(AddressReferent.ATTR_BOX, "Бокс", 0, 1)
        self.addFeature(AddressReferent.ATTR_KILOMETER, "Километр", 0, 1)
        self.addFeature(AddressReferent.ATTR_GEO, "Город\\Регион\\Страна", 0, 1)
        self.addFeature(AddressReferent.ATTR_ZIP, "Индекс", 0, 1)
        self.addFeature(AddressReferent.ATTR_POSTOFFICEBOX, "Абоненский ящик", 0, 1)
        self.addFeature(AddressReferent.ATTR_CSP, "ГСП", 0, 1)
        self.addFeature(AddressReferent.ATTR_METRO, "Метро", 0, 1)
        detail = self.addFeature(AddressReferent.ATTR_DETAIL, "Дополнительный указатель", 0, 1)
        self.detail_feature = detail
        detail.addValue(Utils.enumToString(AddressDetailType.CROSS), "На пересечении", None, None)
        detail.addValue(Utils.enumToString(AddressDetailType.NEAR), "Вблизи", None, None)
        detail.addValue(Utils.enumToString(AddressDetailType.HOSTEL), "Общежитие", None, None)
        detail.addValue(Utils.enumToString(AddressDetailType.NORTH), "Севернее", None, None)
        detail.addValue(Utils.enumToString(AddressDetailType.SOUTH), "Южнее", None, None)
        detail.addValue(Utils.enumToString(AddressDetailType.EAST), "Восточнее", None, None)
        detail.addValue(Utils.enumToString(AddressDetailType.WEST), "Западнее", None, None)
        detail.addValue(Utils.enumToString(AddressDetailType.NORTHEAST), "Северо-восточнее", None, None)
        detail.addValue(Utils.enumToString(AddressDetailType.NORTHWEST), "Северо-западнее", None, None)
        detail.addValue(Utils.enumToString(AddressDetailType.SOUTHEAST), "Юго-восточнее", None, None)
        detail.addValue(Utils.enumToString(AddressDetailType.SOUTHWEST), "Юго-западнее", None, None)
        self.addFeature(AddressReferent.ATTR_MISC, "Разное", 0, 0)
        self.addFeature(AddressReferent.ATTR_DETAILPARAM, "Параметр детализации", 0, 1)
        self.addFeature(AddressReferent.ATTR_FIAS, "Объект ФИАС", 0, 1)
        self.addFeature(AddressReferent.ATTR_BTI, "Объект БТИ", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.address.AddressReferent import AddressReferent
        return AddressReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Адрес"
    
    ADDRESS_IMAGE_ID = "address"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MetaAddress.ADDRESS_IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaAddress
    @staticmethod
    def _static_ctor():
        MetaAddress._global_meta = MetaAddress()

MetaAddress._static_ctor()