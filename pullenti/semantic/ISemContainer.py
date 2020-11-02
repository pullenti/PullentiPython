# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


class ISemContainer:
    """ Интерфейс владельца семантического графа """
    
    @property
    def graph(self) -> 'SemGraph':
        """ Сам граф объектов и связей """
        return None
    
    @property
    def higher(self) -> 'ISemContainer':
        """ Вышестоящий элемент """
        return None
    
    @property
    def begin_char(self) -> int:
        """ Начальная позиция в тексте """
        return None
    
    @property
    def end_char(self) -> int:
        """ Конечная позиция в тексте """
        return None