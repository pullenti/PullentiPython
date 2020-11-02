# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.metadata.Feature import Feature

class ReferentClass:
    """ Описатель класса сущностей """
    
    def __init__(self) -> None:
        self.hide_in_graph = False
        self.__m_features = list()
        self.__m_hash = dict()
    
    @property
    def name(self) -> str:
        """ Строковый идентификатор """
        return "?"
    
    @property
    def caption(self) -> str:
        """ Заголовок (зависит от текущего языка) """
        return None
    
    def __str__(self) -> str:
        return Utils.ifNotNull(self.caption, self.name)
    
    @property
    def features(self) -> typing.List['Feature']:
        """ Атрибуты класса """
        return self.__m_features
    
    def add_feature(self, attr_name : str, attr_caption : str, low_bound : int=0, up_bound : int=0) -> 'Feature':
        """ Добавить атрибут
        
        Args:
            attr_name(str): 
            attr_caption(str): 
            low_bound(int): 
            up_bound(int): 
        
        """
        res = Feature._new1743(attr_name, attr_caption, low_bound, up_bound)
        ind = len(self.__m_features)
        self.__m_features.append(res)
        if (not attr_name in self.__m_hash): 
            self.__m_hash[attr_name] = ind
        else: 
            self.__m_hash[attr_name] = ind
        return self.__m_features[ind]
    
    def find_feature(self, name_ : str) -> 'Feature':
        """ Найти атрибут по его системному имени
        
        Args:
            name_(str): 
        
        """
        wrapind1744 = RefOutArgWrapper(0)
        inoutres1745 = Utils.tryGetValue(self.__m_hash, name_, wrapind1744)
        ind = wrapind1744.value
        if (not inoutres1745): 
            return None
        else: 
            return self.__m_features[ind]
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        """ Вычислить картинку
        
        Args:
            obj(Referent): если null, то общая картинка для типа
        
        Returns:
            str: идентификатор картинки, саму картинку можно будет получить через ProcessorService.GetImageById
        """
        return None