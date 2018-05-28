# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.date.DatePointerType import DatePointerType


class MetaDate(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.date.DateReferent import DateReferent
        super().__init__()
        self.add_feature(DateReferent.ATTR_CENTURY, "Век", 0, 1)
        self.add_feature(DateReferent.ATTR_YEAR, "Год", 0, 1)
        self.add_feature(DateReferent.ATTR_MONTH, "Месяц", 0, 1)
        self.add_feature(DateReferent.ATTR_DAY, "День", 0, 1)
        self.add_feature(DateReferent.ATTR_HOUR, "Час", 0, 1)
        self.add_feature(DateReferent.ATTR_MINUTE, "Минут", 0, 1)
        self.add_feature(DateReferent.ATTR_SECOND, "Секунд", 0, 1)
        self.add_feature(DateReferent.ATTR_DAYOFWEEK, "День недели", 0, 1)
        MetaDate.POINTER = self.add_feature(DateReferent.ATTR_POINTER, "Указатель", 0, 1)
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.BEGIN), "В начале", "На початку", "In the beginning")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.CENTER), "В середине", "В середині", "In the middle")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.END), "В конце", "В кінці", "In the end")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.TODAY), "Настоящее время", "Теперішній час", "Today")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.WINTER), "Зимой", "Взимку", "Winter")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.SPRING), "Весной", "Навесні", "Spring")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.SUMMER), "Летом", "Влітку", "Summer")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.AUTUMN), "Осенью", "Восени", "Autumn")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.UNDEFINED), "Не определена", None, None)
        self.add_feature(DateReferent.ATTR_HIGHER, "Вышестоящая дата", 0, 1)
    
    POINTER = None
    
    @property
    def name(self) -> str:
        from pullenti.ner.date.DateReferent import DateReferent
        return DateReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Дата"
    
    DATE_FULL_IMAGE_ID = "datefull"
    
    DATE_IMAGE_ID = "date"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.date.DateReferent import DateReferent
        dat = (obj if isinstance(obj, DateReferent) else None)
        if (dat is not None and dat.hour >= 0): 
            return MetaDate.DATE_IMAGE_ID
        else: 
            return MetaDate.DATE_FULL_IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class MetaDate
    @staticmethod
    def _static_ctor():
        MetaDate.GLOBAL_META = MetaDate()

MetaDate._static_ctor()