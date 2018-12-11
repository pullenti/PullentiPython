# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.decree.DecreeChangeKind import DecreeChangeKind

class MetaDecreeChange(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
        MetaDecreeChange.GLOBAL_META = MetaDecreeChange()
        MetaDecreeChange.GLOBAL_META.addFeature(DecreeChangeReferent.ATTR_OWNER, "Структурный элемент", 1, 0)
        fi = MetaDecreeChange.GLOBAL_META.addFeature(DecreeChangeReferent.ATTR_KIND, "Тип", 1, 1)
        fi.addValue(Utils.enumToString(DecreeChangeKind.APPEND), "Дополнить", None, None)
        fi.addValue(Utils.enumToString(DecreeChangeKind.EXPIRE), "Утратить силу", None, None)
        fi.addValue(Utils.enumToString(DecreeChangeKind.NEW), "В редакции", None, None)
        fi.addValue(Utils.enumToString(DecreeChangeKind.EXCHANGE), "Заменить", None, None)
        fi.addValue(Utils.enumToString(DecreeChangeKind.REMOVE), "Исключить", None, None)
        fi.addValue(Utils.enumToString(DecreeChangeKind.CONSIDER), "Считать", None, None)
        fi.addValue(Utils.enumToString(DecreeChangeKind.CONTAINER), "Внести изменение", None, None)
        MetaDecreeChange.KIND_FEATURE = fi
        MetaDecreeChange.GLOBAL_META.addFeature(DecreeChangeReferent.ATTR_CHILD, "Дочернее изменение", 0, 0)
        MetaDecreeChange.GLOBAL_META.addFeature(DecreeChangeReferent.ATTR_VALUE, "Значение", 0, 1).show_as_parent = True
        MetaDecreeChange.GLOBAL_META.addFeature(DecreeChangeReferent.ATTR_PARAM, "Параметр", 0, 1).show_as_parent = True
        MetaDecreeChange.GLOBAL_META.addFeature(DecreeChangeReferent.ATTR_MISC, "Разное", 0, 0)
    
    KIND_FEATURE = None
    
    @property
    def name(self) -> str:
        from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
        return DecreeChangeReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Изменение СЭ НПА"
    
    IMAGE_ID = "decreechange"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MetaDecreeChange.IMAGE_ID
    
    GLOBAL_META = None