﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper


class ReferentClass:
    """ Описатель некоторого класса сущностей """
    
    def __init__(self) -> None:
        self.__m_features = list()
        self.__m_attrs = dict()
        self.hide_in_graph = False
    
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
    
    def addFeature(self, attr_name : str, attr_caption : str, low_bound : int=0, up_bound : int=0) -> 'Feature':
        """ Добавить фичу
        
        Args:
            attr_name(str): 
            attr_caption(str): 
            low_bound(int): 
            up_bound(int): 
        
        """
        from pullenti.ner.Feature import Feature
        res = Feature._new2702(attr_name, attr_caption, low_bound, up_bound)
        self.__m_features.append(res)
        if (not attr_name in self.__m_attrs): 
            self.__m_attrs[attr_name] = res
        else: 
            self.__m_attrs[attr_name] = res
        return res
    
    def findFeature(self, name_ : str) -> 'Feature':
        """ Найти атрибут по его системному имени
        
        Args:
            name_(str): 
        
        """
        wrapres2703 = RefOutArgWrapper(None)
        inoutres2704 = Utils.tryGetValue(self.__m_attrs, name_, wrapres2703)
        res = wrapres2703.value
        if (not inoutres2704): 
            return None
        else: 
            return res
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        """ Вычислить картинку
        
        Args:
            obj(Referent): если null, то общая картинка для типа
        
        Returns:
            str: идентификатор картинки, саму картинку можно будет получить через ProcessorService.GetImageById
        """
        return None