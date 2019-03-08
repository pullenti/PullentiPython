# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
from pullenti.unisharp.Utils import Utils

class NextModelItemStatistic:
    
    class Comparer(object):
        
        def __init__(self, words_ : typing.List[tuple]) -> None:
            self.__words = None;
            self.__words = words_
        
        def compare(self, x : str, y : str) -> int:
            xn = self.__words[x]
            yn = self.__words[y]
            if (xn > yn): 
                return -1
            if (xn < yn): 
                return 1
            return 0
    
    def __init__(self) -> None:
        self.count = 0
        self.words = dict()
    
    def add(self, w : str) -> None:
        self.count += 1
        if (not w in self.words): 
            self.words[w] = 1
        else: 
            self.words[w] += 1
    
    def __str__(self) -> str:
        words_ = list(self.words.keys())
        tmp = io.StringIO()
        for w in words_: 
            if (tmp.tell() > 100): 
                print("...", end="", file=tmp)
                break
            if (tmp.tell() > 0): 
                print(" ", end="", file=tmp)
            print("{0}:{1}".format(self.words[w], w), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)