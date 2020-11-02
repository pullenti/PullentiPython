# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.semantic.internal.AlgoParam import AlgoParam

class AlgoParams:
    
    def __init__(self) -> None:
        self.transitive_coef = 1
        self.next_model = 1
        self.ng_link = 1
        self.list0_ = 2
        self.verb_plural = 2
        self.case_accord = 1
        self.morph_accord = 1
    
    def copy_from(self, src : 'AlgoParams') -> None:
        self.transitive_coef = src.transitive_coef
        self.next_model = src.next_model
        self.ng_link = src.ng_link
        self.list0_ = src.list0_
        self.verb_plural = src.verb_plural
        self.case_accord = src.case_accord
        self.morph_accord = src.morph_accord
    
    def copy_from_params(self) -> None:
        for p in AlgoParams.PARAMS: 
            if (p.name == "TransitiveCoef"): 
                self.transitive_coef = p.value
            elif (p.name == "NextModel"): 
                self.next_model = p.value
            elif (p.name == "NgLink"): 
                self.ng_link = p.value
            elif (p.name == "List"): 
                self.list0_ = p.value
            elif (p.name == "VerbPlural"): 
                self.verb_plural = p.value
            elif (p.name == "CaseAccord"): 
                self.case_accord = p.value
            elif (p.name == "MorphAccord"): 
                self.morph_accord = p.value
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print("TransitiveCoef = {0} \r\n".format(self.transitive_coef), end="", file=tmp, flush=True)
        print("NextModel = {0} \r\n".format(self.next_model), end="", file=tmp, flush=True)
        print("NgLink = {0} \r\n".format(self.ng_link), end="", file=tmp, flush=True)
        print("List = {0} \r\n".format(self.list0_), end="", file=tmp, flush=True)
        print("VerbPlural = {0} \r\n".format(self.verb_plural), end="", file=tmp, flush=True)
        print("CaseAccord = {0} \r\n".format(self.case_accord), end="", file=tmp, flush=True)
        print("MorphAccord = {0} \r\n".format(self.morph_accord), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    PARAMS = None
    
    # static constructor for class AlgoParams
    @staticmethod
    def _static_ctor():
        AlgoParams.PARAMS = list()
        AlgoParams.PARAMS.append(AlgoParam._new2895("TransitiveCoef", 1, 4, 1))
        AlgoParams.PARAMS.append(AlgoParam._new2895("NextModel", 1, 4, 1))
        AlgoParams.PARAMS.append(AlgoParam._new2895("NgLink", 1, 3, 1))
        AlgoParams.PARAMS.append(AlgoParam._new2895("List", 1, 4, 1))
        AlgoParams.PARAMS.append(AlgoParam._new2895("VerbPlural", 1, 4, 1))
        AlgoParams.PARAMS.append(AlgoParam._new2895("CaseAccord", 1, 3, 1))
        AlgoParams.PARAMS.append(AlgoParam._new2895("MorphAccord", 1, 3, 1))

AlgoParams._static_ctor()