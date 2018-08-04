# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass


class MetaChat(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.chat.ChatReferent import ChatReferent
        super().__init__()
        self.add_feature(ChatReferent.ATTR_TYPE, "Тип", 1, 1)
        self.add_feature(ChatReferent.ATTR_VALUE, "Значение", 0, 1)
        self.add_feature(ChatReferent.ATTR_NOT, "Отрицание", 0, 1)
        self.add_feature(ChatReferent.ATTR_VERBTYPE, "Тип глагола", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.chat.ChatReferent import ChatReferent
        return ChatReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Элемент диалога"
    
    IMAGE_ID = "chat"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaChat.IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaChat
    @staticmethod
    def _static_ctor():
        MetaChat._global_meta = MetaChat()

MetaChat._static_ctor()