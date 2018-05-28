# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.resume.internal.ResumeTokenType import ResumeTokenType


class ResumeToken(MetaToken):
    """ Это для поддержки резюме """
    
    def __init__(self, b : 'Token', e0 : 'Token') -> None:
        self.typ = ResumeTokenType.UNDEFINED
        self.refs = list()
        super().__init__(b, e0, None)
    
    @staticmethod
    def try_parse(t : 'Token', prev : 'ResumeToken'=None) -> 'ResumeToken':
        if (t is None): 
            return None
        return None