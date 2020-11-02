# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

class AnalysisResult:
    """ Результат анализа
    
    """
    
    def __init__(self) -> None:
        self.__m_sofa = None;
        self.__m_entities = list()
        self.first_token = None;
        self.ontology = None;
        self.base_language = None;
        self.__m_log = list()
        self.exceptions = list()
        self.is_timeout_breaked = False
    
    @property
    def sofa(self) -> 'SourceOfAnalysis':
        """ Анализируемый текст """
        return self.__m_sofa
    @sofa.setter
    def sofa(self, value) -> 'SourceOfAnalysis':
        self.__m_sofa = value
        return value
    
    @property
    def entities(self) -> typing.List['Referent']:
        """ Выделенные сущности """
        return self.__m_entities
    
    @property
    def log0_(self) -> typing.List[str]:
        """ Это некоторые информационные сообщения """
        return self.__m_log
    
    def _add_exception(self, ex : Exception) -> None:
        str0_ = str(ex)
        for e0_ in self.exceptions: 
            if (str(e0_) == str0_): 
                return
        self.exceptions.append(ex)
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("Общая длина {0} знаков".format(len(self.sofa.text)), end="", file=res, flush=True)
        if (self.base_language is not None): 
            print(", базовый язык {0}".format(str(self.base_language)), end="", file=res, flush=True)
        print(", найдено {0} сущностей".format(len(self.entities)), end="", file=res, flush=True)
        if (self.is_timeout_breaked): 
            print(", прервано по таймауту", end="", file=res)
        return Utils.toStringStringIO(res)