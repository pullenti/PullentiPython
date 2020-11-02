# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.semantic.SemFraglink import SemFraglink
from pullenti.semantic.ISemContainer import ISemContainer
from pullenti.semantic.SemGraph import SemGraph
from pullenti.semantic.SemDocument import SemDocument

class SemBlock(ISemContainer):
    """ Блок документа (абзац)
    
    """
    
    def __init__(self, blk : 'SemDocument') -> None:
        self.__m_graph = SemGraph()
        self.m_higher = None;
        self.fragments = list()
        self.links = list()
        self.m_higher = blk
    
    @property
    def graph(self) -> 'SemGraph':
        """ Семантический граф объектов этого блока """
        return self.__m_graph
    
    @property
    def higher(self) -> 'ISemContainer':
        return self.m_higher
    
    @property
    def document(self) -> 'SemDocument':
        return Utils.asObjectOrNull(self.m_higher, SemDocument)
    
    @property
    def begin_char(self) -> int:
        return (0 if len(self.fragments) == 0 else self.fragments[0].begin_char)
    
    @property
    def end_char(self) -> int:
        return (0 if len(self.fragments) == 0 else self.fragments[len(self.fragments) - 1].end_char)
    
    def add_fragments(self, blk : 'SemBlock') -> None:
        for fr in blk.fragments: 
            fr.m_higher = self
            self.fragments.append(fr)
        for li in blk.links: 
            self.links.append(li)
    
    def add_link(self, typ : 'SemFraglinkType', src : 'SemFragment', tgt : 'SemFragment', ques : str=None) -> 'SemFraglink':
        for li in self.links: 
            if (li.typ == typ and li.source == src and li.target == tgt): 
                return li
        res = SemFraglink._new2968(typ, src, tgt, ques)
        self.links.append(res)
        return res
    
    def merge_with(self, blk : 'SemBlock') -> None:
        self.graph.merge_with(blk.graph)
        for fr in blk.fragments: 
            self.fragments.append(fr)
            fr.m_higher = self
        for li in blk.links: 
            self.links.append(li)
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        for fr in self.fragments: 
            spel = fr.spelling
            if (len(spel) > 20): 
                spel = (spel[0:0+20] + "...")
            print("[{0}] ".format(spel), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)