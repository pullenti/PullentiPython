# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
from pullenti.unisharp.Utils import Utils

class AnalysisResult:
    """ Результат анализа """
    
    def __init__(self) -> None:
        self.__m_sofas = list()
        self.__m_entities = list()
        self.first_token = None;
        self.ontology = None;
        self.base_language = None;
        self.__m_log = list()
        self.exceptions = list()
        self.is_timeout_breaked = False
    
    @property
    def sofas(self) -> typing.List['SourceOfAnalysis']:
        """ Входные анализируемые тексты """
        return self.__m_sofas
    
    @property
    def entities(self) -> typing.List['Referent']:
        """ Выделенные сущности """
        return self.__m_entities
    
    @property
    def log0_(self) -> typing.List[str]:
        """ Это некоторые информационные сообщения """
        return self.__m_log
    
    def _addException(self, ex : Exception) -> None:
        str0_ = str(ex)
        for e0_ in self.exceptions: 
            if (str(e0_) == str0_): 
                return
        self.exceptions.append(ex)
    
    def __str__(self) -> str:
        res = io.StringIO()
        len0_ = 0
        for s in self.sofas: 
            len0_ += len(s.text)
        print("Общая длина {0} знаков".format(len0_), end="", file=res, flush=True)
        if (len(self.sofas) > 1): 
            print(" в {0} текстах".format(len(self.sofas)), end="", file=res, flush=True)
        if (self.base_language is not None): 
            print(", базовый язык {0}".format(str(self.base_language)), end="", file=res, flush=True)
        print(", найдено {0} сущностей".format(len(self.entities)), end="", file=res, flush=True)
        if (self.is_timeout_breaked): 
            print(", прервано по таймауту", end="", file=res)
        return Utils.toStringStringIO(res)