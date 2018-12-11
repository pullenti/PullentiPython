# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.resume.internal.ResumeTokenType import ResumeTokenType

class ResumeToken(MetaToken):
    """ Это для поддержки резюме """
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.typ = ResumeTokenType.UNDEFINED
        self.refs = list()
    
    @staticmethod
    def tryParse(t : 'Token', prev : 'ResumeToken'=None) -> 'ResumeToken':
        if (t is None): 
            return None
        return None