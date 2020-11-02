# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.Referent import Referent
from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken

class PersonPropAnalyzer(Analyzer):
    
    def __init__(self) -> None:
        super().__init__()
        self.ignore_this_analyzer = True
    
    ANALYZER_NAME = "PERSONPROPERTY"
    
    @property
    def name(self) -> str:
        return PersonPropAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Используется внутренним образом"
    
    def clone(self) -> 'Analyzer':
        return PersonPropAnalyzer()
    
    def process_referent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        pat = PersonAttrToken.try_attach(begin, None, PersonAttrToken.PersonAttrAttachAttrs.INPROCESS)
        if (pat is not None and pat.prop_ref is not None): 
            return ReferentToken._new2591(pat.prop_ref, pat.begin_token, pat.end_token, pat.morph, pat)
        return None