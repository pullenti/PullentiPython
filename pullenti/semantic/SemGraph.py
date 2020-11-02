# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.semantic.SemLink import SemLink

class SemGraph:
    """ Семантический граф
    
    """
    
    def __init__(self) -> None:
        self.owner = None;
        self.objects = list()
        self.links = list()
    
    @property
    def higher(self) -> 'SemGraph':
        """ Вышележащий граф (граф у вышележащего владельца) """
        if (self.owner is not None and self.owner.higher is not None): 
            return self.owner.higher.graph
        else: 
            return None
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print("{0}obj {1}links: ".format(len(self.objects), len(self.links)), end="", file=tmp, flush=True)
        for li in self.links: 
            if (li != self.links[0]): 
                print("; ", end="", file=tmp)
            print(li, end="", file=tmp)
            if (tmp.tell() > 100): 
                break
        if (len(self.links) == 0): 
            for o in self.objects: 
                if (o != self.objects[0]): 
                    print("; ", end="", file=tmp)
                print(o, end="", file=tmp)
                if (tmp.tell() > 100): 
                    break
        return Utils.toStringStringIO(tmp)
    
    def add_link(self, typ : 'SemLinkType', src : 'SemObject', tgt : 'SemObject', ques : str=None, or0_ : bool=False, prep : str=None) -> 'SemLink':
        if (src is None or tgt is None): 
            return None
        for li in src.graph.links: 
            if (li.typ == typ and li.source == src and li.target == tgt): 
                return li
        if (src.graph != tgt.graph): 
            for li in tgt.graph.links: 
                if (li.typ == typ and li.source == src and li.target == tgt): 
                    return li
        if (tgt.morph.normal_case == "ДОМ"): 
            pass
        res = SemLink._new2969(self, src, tgt, typ, ques, or0_, prep)
        self.links.append(res)
        return res
    
    def remove_link(self, li : 'SemLink') -> None:
        if (li in self.links): 
            self.links.remove(li)
        if (li in li.source.links_from): 
            li.source.links_from.remove(li)
        if (li in li.target.links_to): 
            li.target.links_to.remove(li)
        if (li.alt_link is not None and li.alt_link.alt_link == li): 
            li.alt_link.alt_link = (None)
    
    def merge_with(self, gr : 'SemGraph') -> None:
        for o in gr.objects: 
            if (not o in self.objects): 
                self.objects.append(o)
                o.graph = self
        for li in gr.links: 
            if (not li in self.links): 
                self.links.append(li)
    
    def remove_object(self, obj : 'SemObject') -> None:
        for li in obj.links_from: 
            if (li in li.target.links_to): 
                li.target.links_to.remove(li)
            if (li in self.links): 
                self.links.remove(li)
            elif (li in li.target.graph.links): 
                li.target.graph.links.remove(li)
        for li in obj.links_to: 
            if (li in li.source.links_from): 
                li.source.links_from.remove(li)
            if (li in self.links): 
                self.links.remove(li)
            elif (li in li.source.graph.links): 
                li.source.graph.links.remove(li)
        if (obj in self.objects): 
            self.objects.remove(obj)