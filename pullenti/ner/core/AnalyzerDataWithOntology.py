# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection

class AnalyzerDataWithOntology(AnalyzerData):
    # Данные, полученные в ходе обработки, причём с поддержкой механизма онтологий
    
    def __init__(self) -> None:
        super().__init__()
        self.local_ontology = IntOntologyCollection()
    
    def register_referent(self, referent : 'Referent') -> 'Referent':
        li = self.local_ontology.try_attach_by_referent(referent, None, True)
        if (li is not None): 
            for i in range(len(li) - 1, -1, -1):
                if (li[i].can_be_general_for(referent) or referent.can_be_general_for(li[i])): 
                    del li[i]
        if (li is not None and len(li) > 0): 
            res = li[0]
            if (res != referent): 
                res.merge_slots(referent, True)
            if (len(li) > 1 and self.kit is not None): 
                i = 1
                while i < len(li): 
                    li[0].merge_slots(li[i], True)
                    for ta in li[i].occurrence: 
                        li[0].add_occurence(ta)
                    self.kit.replace_referent(li[i], li[0])
                    self.local_ontology.remove(li[i])
                    i += 1
            if (res._m_ext_referents is not None): 
                res = super().register_referent(res)
            self.local_ontology.add_referent(res)
            return res
        res = super().register_referent(referent)
        if (res is None): 
            return None
        self.local_ontology.add_referent(res)
        return res
    
    def remove_referent(self, r : 'Referent') -> None:
        self.local_ontology.remove(r)
        super().remove_referent(r)