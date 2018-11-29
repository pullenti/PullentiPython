# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.ner.core.AnalyzerData import AnalyzerData


class AnalyzerDataWithOntology(AnalyzerData):
    """ Данные, полученные в ходе обработки, причём с поддержкой механизма онтологий """
    
    def __init__(self) -> None:
        from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
        super().__init__()
        self.local_ontology = IntOntologyCollection()
    
    def registerReferent(self, referent : 'Referent') -> 'Referent':
        li = self.local_ontology.tryAttachByReferent(referent, None, True)
        if (li is not None): 
            for i in range(len(li) - 1, -1, -1):
                if (li[i].canBeGeneralFor(referent) or referent.canBeGeneralFor(li[i])): 
                    del li[i]
        if (li is not None and len(li) > 0): 
            res = li[0]
            if (res != referent): 
                res.mergeSlots(referent, True)
            if (len(li) > 1 and self.kit is not None): 
                i = 1
                while i < len(li): 
                    li[0].mergeSlots(li[i], True)
                    for ta in li[i].occurrence: 
                        li[0].addOccurence(ta)
                    self.kit.replaceReferent(li[i], li[0])
                    self.local_ontology.remove(li[i])
                    i += 1
            if (res._m_ext_referents is not None): 
                res = super().registerReferent(res)
            self.local_ontology.addReferent(res)
            return res
        res = super().registerReferent(referent)
        if (res is None): 
            return None
        self.local_ontology.addReferent(res)
        return res
    
    def removeReferent(self, r : 'Referent') -> None:
        self.local_ontology.remove(r)
        super().removeReferent(r)