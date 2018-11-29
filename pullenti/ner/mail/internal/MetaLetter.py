# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.ner.ReferentClass import ReferentClass


class MetaLetter(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.mail.MailReferent import MailReferent
        super().__init__()
        self.addFeature(MailReferent.ATTR_KIND, "Тип блока", 1, 1)
        self.addFeature(MailReferent.ATTR_TEXT, "Текст блока", 1, 1)
        self.addFeature(MailReferent.ATTR_REF, "Ссылка на объект", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.mail.MailReferent import MailReferent
        return MailReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Блок письма"
    
    IMAGE_ID = "letter"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MetaLetter.IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaLetter
    @staticmethod
    def _static_ctor():
        MetaLetter._global_meta = MetaLetter()

MetaLetter._static_ctor()