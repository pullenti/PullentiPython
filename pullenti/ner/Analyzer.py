﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
import math
from pullenti.unisharp.Misc import ProgressEventArgs
from pullenti.unisharp.Misc import CancelEventArgs
from pullenti.ner.core.AnalyzerData import AnalyzerData


class Analyzer:
    """ Базовый класс для всех семантических анализаторов """
    
    def __init__(self) -> None:
        self._progress = list()
        self._cancel = list()
        self.__last_percent = 0
        self.__persistreferentsregim = False
        self.__ignorethisanalyzer = False
        self._persist_analizer_data = None
    
    def process(self, kit : 'AnalysisKit') -> None:
        pass
    
    @property
    def name(self) -> str:
        """ Уникальное наименование анализатора """
        return None
    
    @property
    def caption(self) -> str:
        """ Заголовок анализатора """
        return None
    
    @property
    def description(self) -> str:
        """ Описание анализатора """
        return None
    
    def __str__(self) -> str:
        return "{0} ({1})".format(self.caption, self.name)
    
    def clone(self) -> 'Analyzer':
        return None
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        """ Список поддерживаемых типов объектов (сущностей), которые выделяет анализатор """
        return list()
    
    @property
    def images(self) -> typing.List[tuple]:
        """ Список изображений объектов """
        return None
    
    @property
    def is_specific(self) -> bool:
        """ Признак специфического анализатора (предназначенного для конкретной предметной области).
         Специфические анализаторы по умолчанию не добавляются в процессор (Processor) """
        return False
    
    def create_referent(self, type0_ : str) -> 'Referent':
        return None
    
    __empty_list = None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        """ Список имён типов объектов из других картриджей, которые желательно предварительно выделить (для управления приоритетом применения правил) """
        return Analyzer.__empty_list
    
    @property
    def progress_weight(self) -> int:
        """ Сколько примерно времени работает анализатор по сравнению с другими (в условных единицах) """
        return 0
    
    def _on_progress(self, pos : int, max0_ : int, kit : 'AnalysisKit') -> bool:
        ret = True
        if (self._progress.__len__() > 0): 
            if (pos >= 0 and pos <= max0_ and max0_ > 0): 
                percent = pos
                percent *= (100)
                percent = math.floor(percent / (max0_))
                if (percent != self.__last_percent): 
                    arg = ProgressEventArgs(percent, None)
                    for iiid in range(len(self._progress)): self._progress[iiid].call(self, arg)
                    if (self._cancel.__len__() > 0): 
                        cea = CancelEventArgs()
                        for iiid in range(len(self._cancel)): self._cancel[iiid].call(kit, cea)
                        ret = not cea.cancel
                self.__last_percent = percent
        return ret
    
    def _on_message(self, message : object) -> bool:
        if (self._progress.__len__() > 0): 
            for iiid in range(len(self._progress)): self._progress[iiid].call(self, ProgressEventArgs(-1, message))
        return True
    
    @property
    def _persist_referents_regim(self) -> bool:
        """ Включить режим накопления выделяемых сущностей при обработке разных SourceOfText
         (то есть локальные сущности будут накапливаться) """
        return self.__persistreferentsregim
    
    @_persist_referents_regim.setter
    def _persist_referents_regim(self, value) -> bool:
        self.__persistreferentsregim = value
        return self.__persistreferentsregim
    
    @property
    def ignore_this_analyzer(self) -> bool:
        """ При установке в true будет игнорироваться при обработке (для отладки) """
        return self.__ignorethisanalyzer
    
    @ignore_this_analyzer.setter
    def ignore_this_analyzer(self, value) -> bool:
        self.__ignorethisanalyzer = value
        return self.__ignorethisanalyzer
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        return AnalyzerData()
    
    def _process_referent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        return None
    
    def process_ontology_item(self, begin : 'Token') -> 'ReferentToken':
        return None
    
    # static constructor for class Analyzer
    @staticmethod
    def _static_ctor():
        Analyzer.__empty_list = list()

Analyzer._static_ctor()