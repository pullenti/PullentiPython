# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.ner.ReferentClass import ReferentClass

class MetaChat(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.chat.ChatReferent import ChatReferent
        MetaChat._global_meta = MetaChat()
        MetaChat._global_meta.addFeature(ChatReferent.ATTR_TYPE, "Тип", 1, 1)
        MetaChat._global_meta.addFeature(ChatReferent.ATTR_VALUE, "Значение", 0, 1)
        MetaChat._global_meta.addFeature(ChatReferent.ATTR_NOT, "Отрицание", 0, 1)
        MetaChat._global_meta.addFeature(ChatReferent.ATTR_VERBTYPE, "Тип глагола", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.chat.ChatReferent import ChatReferent
        return ChatReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Элемент диалога"
    
    IMAGE_ID = "chat"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MetaChat.IMAGE_ID
    
    _global_meta = None