# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.decree.DecreeChangeValueKind import DecreeChangeValueKind


class MetaDecreeChangeValue(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.decree.DecreeChangeValueReferent import DecreeChangeValueReferent
        super().__init__()
        fi = self.add_feature(DecreeChangeValueReferent.ATTR_KIND, "Тип", 1, 1)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.TEXT), "Текст", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.WORDS), "Слова", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.ROBUSTWORDS), "Слова (неточно)", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.NUMBERS), "Цифры", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.SEQUENCE), "Предложение", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.FOOTNOTE), "Сноска", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.BLOCK), "Блок", None, None)
        MetaDecreeChangeValue.KIND_FEATURE = fi
        self.add_feature(DecreeChangeValueReferent.ATTR_VALUE, "Значение", 1, 1)
        self.add_feature(DecreeChangeValueReferent.ATTR_NUMBER, "Номер", 0, 1)
        self.add_feature(DecreeChangeValueReferent.ATTR_NEWITEM, "Новый структурный элемент", 0, 0)
    
    KIND_FEATURE = None
    
    @property
    def name(self) -> str:
        from pullenti.ner.decree.DecreeChangeValueReferent import DecreeChangeValueReferent
        return DecreeChangeValueReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Значение изменения СЭ НПА"
    
    IMAGE_ID = "decreechangevalue"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaDecreeChangeValue.IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class MetaDecreeChangeValue
    @staticmethod
    def _static_ctor():
        MetaDecreeChangeValue.GLOBAL_META = MetaDecreeChangeValue()

MetaDecreeChangeValue._static_ctor()