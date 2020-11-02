# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.semantic.SemFraglinkType import SemFraglinkType

class SemFraglink:
    """ Связь между фрагментами """
    
    def __init__(self) -> None:
        self.typ = SemFraglinkType.UNDEFINED
        self.source = None;
        self.target = None;
        self.question = None;
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.typ != SemFraglinkType.UNDEFINED): 
            print("{0} ".format(Utils.enumToString(self.typ)), end="", file=tmp, flush=True)
        if (self.question is not None): 
            print("{0}? ".format(self.question), end="", file=tmp, flush=True)
        if (self.source is not None): 
            print("{0} ".format(str(self.source)), end="", file=tmp, flush=True)
        if (self.target is not None): 
            print("-> {0}".format(str(self.target)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def _new2968(_arg1 : 'SemFraglinkType', _arg2 : 'SemFragment', _arg3 : 'SemFragment', _arg4 : str) -> 'SemFraglink':
        res = SemFraglink()
        res.typ = _arg1
        res.source = _arg2
        res.target = _arg3
        res.question = _arg4
        return res