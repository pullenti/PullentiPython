# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.definition.DefinitionKind import DefinitionKind


class MetaDefin(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.definition.DefinitionReferent import DefinitionReferent
        super().__init__()
        self.add_feature(DefinitionReferent.ATTR_TERMIN, "Термин", 1, 0)
        self.add_feature(DefinitionReferent.ATTR_TERMIN_ADD, "Дополнение термина", 0, 0)
        self.add_feature(DefinitionReferent.ATTR_VALUE, "Значение", 1, 0)
        self.add_feature(DefinitionReferent.ATTR_MISC, "Мелочь", 0, 0)
        self.add_feature(DefinitionReferent.ATTR_DECREE, "Ссылка на НПА", 0, 0)
        fi = self.add_feature(DefinitionReferent.ATTR_KIND, "Тип", 1, 1)
        fi.add_value(Utils.enumToString(DefinitionKind.ASSERTATION), "Утверждение", None, None)
        fi.add_value(Utils.enumToString(DefinitionKind.DEFINITION), "Определение", None, None)
        fi.add_value(Utils.enumToString(DefinitionKind.NEGATION), "Отрицание", None, None)
    
    @property
    def name(self) -> str:
        from pullenti.ner.definition.DefinitionReferent import DefinitionReferent
        return DefinitionReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Тезис"
    
    IMAGE_DEF_ID = "defin"
    
    IMAGE_ASS_ID = "assert"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.definition.DefinitionReferent import DefinitionReferent
        if (isinstance(obj, DefinitionReferent)): 
            ki = (obj if isinstance(obj, DefinitionReferent) else None).kind
            if (ki == DefinitionKind.DEFINITION): 
                return MetaDefin.IMAGE_DEF_ID
        return MetaDefin.IMAGE_ASS_ID
    
    _global_meta = None
    
    # static constructor for class MetaDefin
    @staticmethod
    def _static_ctor():
        MetaDefin._global_meta = MetaDefin()

MetaDefin._static_ctor()