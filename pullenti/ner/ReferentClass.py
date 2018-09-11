# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

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
    
    def add_feature(self, attr_name : str, attr_caption : str, low_bound : int=0, up_bound : int=0) -> 'Feature':
        from pullenti.ner.Feature import Feature
        res = Feature._new2664(attr_name, attr_caption, low_bound, up_bound)
        self.__m_features.append(res)
        if (not attr_name in self.__m_attrs): 
            self.__m_attrs[attr_name] = res
        else: 
            self.__m_attrs[attr_name] = res
        return res
    
    def find_feature(self, name_ : str) -> 'Feature':
        inoutarg2665 = RefOutArgWrapper(None)
        inoutres2666 = Utils.tryGetValue(self.__m_attrs, name_, inoutarg2665)
        res = inoutarg2665.value
        if (not inoutres2666): 
            return None
        else: 
            return res
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return None