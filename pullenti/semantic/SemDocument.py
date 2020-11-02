# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.semantic.ISemContainer import ISemContainer
from pullenti.semantic.SemGraph import SemGraph

class SemDocument(ISemContainer):
    """ Документ
    
    """
    
    def __init__(self) -> None:
        self.__m_graph = SemGraph()
        self.blocks = list()
    
    @property
    def graph(self) -> 'SemGraph':
        """ Семантические объекты уровня документа """
        return self.__m_graph
    
    @property
    def higher(self) -> 'ISemContainer':
        return None
    
    @property
    def begin_char(self) -> int:
        return (0 if len(self.blocks) == 0 else self.blocks[0].begin_char)
    
    @property
    def end_char(self) -> int:
        return (0 if len(self.blocks) == 0 else self.blocks[len(self.blocks) - 1].end_char)
    
    def merge_all_blocks(self) -> None:
        if (len(self.blocks) < 2): 
            return
        i = 1
        while i < len(self.blocks): 
            self.blocks[0].merge_with(self.blocks[i])
            i += 1
        del self.blocks[1:1+len(self.blocks) - 1]