# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.semantic.SemLinkType import SemLinkType

class SemLink:
    """ Семантическая связь между объектами """
    
    def __init__(self, gr : 'SemGraph', src : 'SemObject', tgt : 'SemObject') -> None:
        self.graph = None;
        self.typ = SemLinkType.UNDEFINED
        self.__m_source = None;
        self._m_target = None;
        self.alt_link = None;
        self.question = None;
        self.preposition = None;
        self.is_or = False
        self.tag = None;
        self.graph = gr
        self.__m_source = src
        self._m_target = tgt
        src.links_from.append(self)
        tgt.links_to.append(self)
    
    @property
    def source(self) -> 'SemObject':
        """ Объект начала связи """
        return self.__m_source
    
    @property
    def target(self) -> 'SemObject':
        """ Объект конца связи """
        return self._m_target
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.alt_link is not None): 
            print("??? ", end="", file=tmp)
        if (self.is_or): 
            print("OR ", end="", file=tmp)
        if (self.typ != SemLinkType.UNDEFINED): 
            print(Utils.enumToString(self.typ), end="", file=tmp)
        if (self.question is not None): 
            print(" {0}?".format(self.question), end="", file=tmp, flush=True)
        if (self.source is not None): 
            print(" {0}".format(str(self.source)), end="", file=tmp, flush=True)
        if (self.target is not None): 
            print(" -> {0}".format(str(self.target)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def _new2969(_arg1 : 'SemGraph', _arg2 : 'SemObject', _arg3 : 'SemObject', _arg4 : 'SemLinkType', _arg5 : str, _arg6 : bool, _arg7 : str) -> 'SemLink':
        res = SemLink(_arg1, _arg2, _arg3)
        res.typ = _arg4
        res.question = _arg5
        res.is_or = _arg6
        res.preposition = _arg7
        return res