# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.date.DatePointerType import DatePointerType

class MetaDate(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.date.DateReferent import DateReferent
        MetaDate.GLOBAL_META = MetaDate()
        MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_ISRELATIVE, "Относительность", 0, 1)
        MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_CENTURY, "Век", 0, 1)
        MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_YEAR, "Год", 0, 1)
        MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_QUARTAL, "Квартал", 0, 1)
        MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_MONTH, "Месяц", 0, 1)
        MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_WEEK, "Неделя", 0, 1)
        MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_DAY, "День", 0, 1)
        MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_HOUR, "Час", 0, 1)
        MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_MINUTE, "Минут", 0, 1)
        MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_SECOND, "Секунд", 0, 1)
        MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_DAYOFWEEK, "День недели", 0, 1)
        MetaDate.POINTER = MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_POINTER, "Указатель", 0, 1)
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.BEGIN), "в начале", "на початку", "in the beginning")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.CENTER), "в середине", "в середині", "in the middle")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.END), "в конце", "в кінці", "in the end")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.TODAY), "настоящее время", "теперішній час", "today")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.WINTER), "зимой", "взимку", "winter")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.SPRING), "весной", "навесні", "spring")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.SUMMER), "летом", "влітку", "summer")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.AUTUMN), "осенью", "восени", "autumn")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.ABOUT), "около", "біля", "about")
        MetaDate.POINTER.add_value(Utils.enumToString(DatePointerType.UNDEFINED), "Не определена", None, None)
        MetaDate.GLOBAL_META.add_feature(DateReferent.ATTR_HIGHER, "Вышестоящая дата", 0, 1)
    
    POINTER = None
    
    @property
    def name(self) -> str:
        from pullenti.ner.date.DateReferent import DateReferent
        return DateReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Дата"
    
    DATE_FULL_IMAGE_ID = "datefull"
    
    DATE_REL_IMAGE_ID = "daterel"
    
    DATE_IMAGE_ID = "date"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.date.DateReferent import DateReferent
        dat = Utils.asObjectOrNull(obj, DateReferent)
        if (dat is not None and dat.is_relative): 
            return MetaDate.DATE_REL_IMAGE_ID
        if (dat is not None and dat.hour >= 0): 
            return MetaDate.DATE_IMAGE_ID
        else: 
            return MetaDate.DATE_FULL_IMAGE_ID
    
    GLOBAL_META = None