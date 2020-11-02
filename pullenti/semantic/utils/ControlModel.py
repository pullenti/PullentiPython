# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.semantic.utils.ControlModelQuestion import ControlModelQuestion
from pullenti.semantic.core.SemanticRole import SemanticRole
from pullenti.semantic.utils.ControlModelItemType import ControlModelItemType
from pullenti.semantic.utils.ControlModelItem import ControlModelItem

class ControlModel:
    """ Модель управления """
    
    def __init__(self) -> None:
        self.items = list()
        self.pacients = list()
    
    def __str__(self) -> str:
        res = io.StringIO()
        for it in self.items: 
            if (it.ignorable): 
                continue
            if (res.tell() > 0): 
                print("; ", end="", file=res)
            if (it.typ == ControlModelItemType.WORD): 
                print("{0} = {1}".format(it.word, len(it.links)), end="", file=res, flush=True)
            else: 
                print("{0} = {1}".format(Utils.enumToString(it.typ), len(it.links)), end="", file=res, flush=True)
        for p in self.pacients: 
            print(" ({0})".format(p), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def find_item_by_typ(self, typ : 'ControlModelItemType') -> 'ControlModelItem':
        for it in self.items: 
            if (it.typ == typ): 
                return it
        return None
    
    def _deserialize(self, str0_ : 'ByteArrayWrapper', pos : int) -> None:
        cou = str0_.deserialize_short(pos)
        while cou > 0: 
            it = ControlModelItem()
            b = str0_.deserialize_byte(pos)
            if ((((b) & 0x80)) != 0): 
                it.nominative_can_be_agent_and_pacient = True
            it.typ = (Utils.valToEnum(((b) & 0x7F), ControlModelItemType))
            if (it.typ == ControlModelItemType.WORD): 
                it.word = str0_.deserialize_string(pos)
            licou = str0_.deserialize_short(pos)
            while licou > 0: 
                bi = str0_.deserialize_byte(pos)
                i = bi
                b = str0_.deserialize_byte(pos)
                if (i >= 0 and (i < len(ControlModelQuestion.ITEMS))): 
                    it.links[ControlModelQuestion.ITEMS[i]] = Utils.valToEnum(b, SemanticRole)
                licou -= 1
            self.items.append(it)
            cou -= 1
        cou = str0_.deserialize_short(pos)
        while cou > 0: 
            p = str0_.deserialize_string(pos)
            if (p is not None): 
                self.pacients.append(p)
            cou -= 1