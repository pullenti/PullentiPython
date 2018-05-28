# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ner.titlepage.TitlePageReferent import TitlePageReferent



class DocumentReferent(TitlePageReferent):
    
    def __init__(self) -> None:
        from pullenti.ner.old.internal.MetaDocument import MetaDocument
        super().__init__(DocumentReferent.OBJ_TYPENAME)
        self.instance_of = MetaDocument._global_meta
    
    OBJ_TYPENAME = "DOCUMENT"
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        from pullenti.ner.Referent import Referent
        return obj == self
    
    @property
    def children(self) -> typing.List['DocumentBlockReferent']:
        from pullenti.ner.old.DocumentBlockReferent import DocumentBlockReferent
        res = list()
        for s in self.slots: 
            if (s.type_name == DocumentBlockReferent.ATTR_CHILD): 
                if (isinstance(s.value, DocumentBlockReferent)): 
                    res.append(s.value if isinstance(s.value, DocumentBlockReferent) else None)
        return res