# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.semantic.core.SemanticRole import SemanticRole

class SemanticLink(object):
    """ Семантическая связь двух элементов
    Семантическая связь
    """
    
    def __init__(self) -> None:
        self.master = None;
        self.slave = None;
        self.question = None;
        self.role = SemanticRole.COMMON
        self.is_passive = False
        self.rank = 0
        self.modelled = False
        self.idiom = False
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.modelled): 
            print("?", end="", file=res)
        if (self.idiom): 
            print("!", end="", file=res)
        if (self.role != SemanticRole.COMMON): 
            print("{0}: ".format(Utils.enumToString(self.role)), end="", file=res, flush=True)
        if (self.is_passive): 
            print("Passive ", end="", file=res)
        if (self.rank > 0): 
            print("{0} ".format(self.rank), end="", file=res, flush=True)
        if (self.question is not None): 
            print("{0}? ".format(self.question.spelling_ex), end="", file=res, flush=True)
        print("[{0}] <- [{1}]".format(("?" if self.master is None else str(self.master)), ("?" if self.slave is None else str(self.slave))), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def compareTo(self, other : 'SemanticLink') -> int:
        if (self.rank > other.rank): 
            return -1
        if (self.rank < other.rank): 
            return 1
        return 0
    
    @staticmethod
    def _new2869(_arg1 : bool, _arg2 : 'MetaToken', _arg3 : 'MetaToken', _arg4 : float, _arg5 : 'ControlModelQuestion') -> 'SemanticLink':
        res = SemanticLink()
        res.modelled = _arg1
        res.master = _arg2
        res.slave = _arg3
        res.rank = _arg4
        res.question = _arg5
        return res
    
    @staticmethod
    def _new2870(_arg1 : 'SemanticRole', _arg2 : 'MetaToken', _arg3 : 'MetaToken', _arg4 : float) -> 'SemanticLink':
        res = SemanticLink()
        res.role = _arg1
        res.master = _arg2
        res.slave = _arg3
        res.rank = _arg4
        return res
    
    @staticmethod
    def _new2871(_arg1 : float, _arg2 : 'ControlModelQuestion') -> 'SemanticLink':
        res = SemanticLink()
        res.rank = _arg1
        res.question = _arg2
        return res
    
    @staticmethod
    def _new2872(_arg1 : 'ControlModelQuestion', _arg2 : 'SemanticRole', _arg3 : bool) -> 'SemanticLink':
        res = SemanticLink()
        res.question = _arg1
        res.role = _arg2
        res.idiom = _arg3
        return res
    
    @staticmethod
    def _new2873(_arg1 : bool, _arg2 : 'SemanticRole', _arg3 : float, _arg4 : 'ControlModelQuestion', _arg5 : bool) -> 'SemanticLink':
        res = SemanticLink()
        res.modelled = _arg1
        res.role = _arg2
        res.rank = _arg3
        res.question = _arg4
        res.is_passive = _arg5
        return res
    
    @staticmethod
    def _new2874(_arg1 : 'SemanticRole', _arg2 : float, _arg3 : 'ControlModelQuestion', _arg4 : bool) -> 'SemanticLink':
        res = SemanticLink()
        res.role = _arg1
        res.rank = _arg2
        res.question = _arg3
        res.is_passive = _arg4
        return res
    
    @staticmethod
    def _new2875(_arg1 : 'SemanticRole', _arg2 : float, _arg3 : 'ControlModelQuestion') -> 'SemanticLink':
        res = SemanticLink()
        res.role = _arg1
        res.rank = _arg2
        res.question = _arg3
        return res
    
    @staticmethod
    def _new2878(_arg1 : 'ControlModelQuestion', _arg2 : float, _arg3 : 'SemanticRole') -> 'SemanticLink':
        res = SemanticLink()
        res.question = _arg1
        res.rank = _arg2
        res.role = _arg3
        return res
    
    @staticmethod
    def _new2879(_arg1 : bool, _arg2 : 'SemanticRole', _arg3 : float, _arg4 : 'ControlModelQuestion') -> 'SemanticLink':
        res = SemanticLink()
        res.modelled = _arg1
        res.role = _arg2
        res.rank = _arg3
        res.question = _arg4
        return res
    
    @staticmethod
    def _new2880(_arg1 : 'SemanticRole', _arg2 : 'ControlModelQuestion', _arg3 : bool) -> 'SemanticLink':
        res = SemanticLink()
        res.role = _arg1
        res.question = _arg2
        res.idiom = _arg3
        return res