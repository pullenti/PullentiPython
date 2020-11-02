# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.semantic.core.SemanticRole import SemanticRole
from pullenti.semantic.utils.ControlModelItemType import ControlModelItemType

class ControlModelItem:
    """ Элемент модели управления """
    
    def __init__(self) -> None:
        self.typ = ControlModelItemType.WORD
        self.word = None;
        self.links = dict()
        self.nominative_can_be_agent_and_pacient = False
        self.ignorable = False
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.ignorable): 
            print("IGNORE ", end="", file=res)
        if (self.typ != ControlModelItemType.WORD): 
            print("{0}: ".format(Utils.enumToString(self.typ)), end="", file=res, flush=True)
        else: 
            print("{0}: ".format(Utils.ifNotNull(self.word, "?")), end="", file=res, flush=True)
        for li in self.links.items(): 
            if (li[1] == SemanticRole.AGENT): 
                print("аг:", end="", file=res)
            elif (li[1] == SemanticRole.PACIENT): 
                print("пац:", end="", file=res)
            elif (li[1] == SemanticRole.STRONG): 
                print("сильн:", end="", file=res)
            print("{0}? ".format(li[0].spelling), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)