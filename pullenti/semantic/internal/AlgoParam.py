# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import math

class AlgoParam:
    
    def __init__(self) -> None:
        self.name = None;
        self.value = 0
        self.min0_ = 0
        self.max0_ = 0
        self.delta = 0
    
    @property
    def count(self) -> int:
        return (math.floor((((self.max0_ - self.min0_)) / self.delta))) + 1
    
    def __str__(self) -> str:
        return "{0}={1} [{2} .. {3}] by {4}".format(self.name, self.value, self.min0_, self.max0_, self.delta)
    
    @staticmethod
    def _new2895(_arg1 : str, _arg2 : float, _arg3 : float, _arg4 : float) -> 'AlgoParam':
        res = AlgoParam()
        res.name = _arg1
        res.min0_ = _arg2
        res.max0_ = _arg3
        res.delta = _arg4
        return res