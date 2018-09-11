# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass


class MetaDocBlockInfo(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.old.DocumentBlockReferent import DocumentBlockReferent
        super().__init__()
        self.add_feature(DocumentBlockReferent.ATTR_NAME, "Название", 0, 0)
        self.add_feature(DocumentBlockReferent.ATTR_TYPE, "Тип", 0, 0)
        self.add_feature(DocumentBlockReferent.ATTR_CONTENT, "Содержимое (текст)", 0, 0)
        self.add_feature(DocumentBlockReferent.ATTR_PARENT, "Владелец", 0, 1)
        self.add_feature(DocumentBlockReferent.ATTR_CHILD, "Внутренний блок", 0, 0)
        self.add_feature(DocumentBlockReferent.ATTR_NUMBER, "Номер", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.old.DocumentBlockReferent import DocumentBlockReferent
        return DocumentBlockReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Блок документа"
    
    BLOCK_IMAGE_ID = "block_text"
    
    DOC_IMAGE_ID = "block_doc"
    
    CHAPTER_IMAGE_ID = "block_parent"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.old.DocumentBlockReferent import DocumentBlockReferent
        db = (obj if isinstance(obj, DocumentBlockReferent) else None)
        if (db is None): 
            return MetaDocBlockInfo.BLOCK_IMAGE_ID
        if (db.find_slot(DocumentBlockReferent.ATTR_PARENT, None, True) is None): 
            return MetaDocBlockInfo.DOC_IMAGE_ID
        if (db.find_slot(DocumentBlockReferent.ATTR_CONTENT, None, True) is not None): 
            return MetaDocBlockInfo.BLOCK_IMAGE_ID
        return MetaDocBlockInfo.CHAPTER_IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaDocBlockInfo
    @staticmethod
    def _static_ctor():
        MetaDocBlockInfo._global_meta = MetaDocBlockInfo()

MetaDocBlockInfo._static_ctor()