# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.titlepage.internal.MetaTitleInfo import MetaTitleInfo


class MetaDocument(MetaTitleInfo):
    
    def __init__(self) -> None:
        from pullenti.ner.old.DocumentBlockReferent import DocumentBlockReferent
        super().__init__()
        self.add_feature(DocumentBlockReferent.ATTR_CHILD, "Внутренний блок", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.old.DocumentReferent import DocumentReferent
        return DocumentReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Документ"
    
    DOC_IMAGE_ID = "doc"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaDocument.DOC_IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaDocument
    @staticmethod
    def _static_ctor():
        MetaDocument._global_meta = MetaDocument()

MetaDocument._static_ctor()