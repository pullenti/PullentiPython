# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.definition.DefinitionKind import DefinitionKind


class MetaDefin(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.definition.DefinitionReferent import DefinitionReferent
        super().__init__()
        self.addFeature(DefinitionReferent.ATTR_TERMIN, "Термин", 1, 0)
        self.addFeature(DefinitionReferent.ATTR_TERMIN_ADD, "Дополнение термина", 0, 0)
        self.addFeature(DefinitionReferent.ATTR_VALUE, "Значение", 1, 0)
        self.addFeature(DefinitionReferent.ATTR_MISC, "Мелочь", 0, 0)
        self.addFeature(DefinitionReferent.ATTR_DECREE, "Ссылка на НПА", 0, 0)
        fi = self.addFeature(DefinitionReferent.ATTR_KIND, "Тип", 1, 1)
        fi.addValue(Utils.enumToString(DefinitionKind.ASSERTATION), "Утверждение", None, None)
        fi.addValue(Utils.enumToString(DefinitionKind.DEFINITION), "Определение", None, None)
        fi.addValue(Utils.enumToString(DefinitionKind.NEGATION), "Отрицание", None, None)
    
    @property
    def name(self) -> str:
        from pullenti.ner.definition.DefinitionReferent import DefinitionReferent
        return DefinitionReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Тезис"
    
    IMAGE_DEF_ID = "defin"
    
    IMAGE_ASS_ID = "assert"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.definition.DefinitionReferent import DefinitionReferent
        if (isinstance(obj, DefinitionReferent)): 
            ki = (Utils.asObjectOrNull(obj, DefinitionReferent)).kind
            if (ki == DefinitionKind.DEFINITION): 
                return MetaDefin.IMAGE_DEF_ID
        return MetaDefin.IMAGE_ASS_ID
    
    _global_meta = None
    
    # static constructor for class MetaDefin
    @staticmethod
    def _static_ctor():
        MetaDefin._global_meta = MetaDefin()

MetaDefin._static_ctor()