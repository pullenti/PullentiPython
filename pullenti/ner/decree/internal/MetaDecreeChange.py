# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.decree.DecreeChangeKind import DecreeChangeKind

class MetaDecreeChange(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
        MetaDecreeChange.GLOBAL_META = MetaDecreeChange()
        MetaDecreeChange.GLOBAL_META.add_feature(DecreeChangeReferent.ATTR_OWNER, "Структурный элемент", 1, 0)
        fi = MetaDecreeChange.GLOBAL_META.add_feature(DecreeChangeReferent.ATTR_KIND, "Тип", 1, 1)
        fi.add_value(Utils.enumToString(DecreeChangeKind.APPEND), "Дополнить", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeKind.EXPIRE), "Утратить силу", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeKind.NEW), "В редакции", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeKind.EXCHANGE), "Заменить", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeKind.REMOVE), "Исключить", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeKind.CONSIDER), "Считать", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeKind.CONTAINER), "Внести изменение", None, None)
        MetaDecreeChange.KIND_FEATURE = fi
        MetaDecreeChange.GLOBAL_META.add_feature(DecreeChangeReferent.ATTR_CHILD, "Дочернее изменение", 0, 0)
        MetaDecreeChange.GLOBAL_META.add_feature(DecreeChangeReferent.ATTR_VALUE, "Значение", 0, 1).show_as_parent = True
        MetaDecreeChange.GLOBAL_META.add_feature(DecreeChangeReferent.ATTR_PARAM, "Параметр", 0, 1).show_as_parent = True
        MetaDecreeChange.GLOBAL_META.add_feature(DecreeChangeReferent.ATTR_MISC, "Разное", 0, 0)
    
    KIND_FEATURE = None
    
    @property
    def name(self) -> str:
        from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
        return DecreeChangeReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Изменение СЭ НПА"
    
    IMAGE_ID = "decreechange"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaDecreeChange.IMAGE_ID
    
    GLOBAL_META = None