# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass

class MetaLetter(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.mail.MailReferent import MailReferent
        MetaLetter._global_meta = MetaLetter()
        MetaLetter._global_meta.add_feature(MailReferent.ATTR_KIND, "Тип блока", 1, 1)
        MetaLetter._global_meta.add_feature(MailReferent.ATTR_TEXT, "Текст блока", 1, 1)
        MetaLetter._global_meta.add_feature(MailReferent.ATTR_REF, "Ссылка на объект", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.mail.MailReferent import MailReferent
        return MailReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Блок письма"
    
    IMAGE_ID = "letter"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaLetter.IMAGE_ID
    
    _global_meta = None