# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class Feature:
    """ Атрибут класса сущностей """
    
    def __init__(self) -> None:
        self.__name = None;
        self.__caption = None;
        self.__lowerbound = 0
        self.__upperbound = 0
        self.__showasparent = False
        self.inner_values = list()
        self.outer_values = list()
        self.outer_valuesen = list()
        self.outer_valuesua = list()
    
    @property
    def name(self) -> str:
        """ Внутреннее имя """
        return self.__name
    @name.setter
    def name(self, value) -> str:
        self.__name = value
        return self.__name
    
    @property
    def caption(self) -> str:
        """ Заголовок """
        return self.__caption
    @caption.setter
    def caption(self, value) -> str:
        self.__caption = value
        return self.__caption
    
    @property
    def lower_bound(self) -> int:
        """ Минимальное количество """
        return self.__lowerbound
    @lower_bound.setter
    def lower_bound(self, value) -> int:
        self.__lowerbound = value
        return self.__lowerbound
    
    @property
    def upper_bound(self) -> int:
        """ Максимальное количество (0 - неограничено) """
        return self.__upperbound
    @upper_bound.setter
    def upper_bound(self, value) -> int:
        self.__upperbound = value
        return self.__upperbound
    
    @property
    def show_as_parent(self) -> bool:
        """ Это для внутреннего использования """
        return self.__showasparent
    @show_as_parent.setter
    def show_as_parent(self, value) -> bool:
        self.__showasparent = value
        return self.__showasparent
    
    def __str__(self) -> str:
        res = Utils.newStringIO(Utils.ifNotNull(self.caption, self.name))
        if (self.upper_bound > 0 or self.lower_bound > 0): 
            if (self.upper_bound == 0): 
                print("[{0}..*]".format(self.lower_bound), end="", file=res, flush=True)
            elif (self.upper_bound == self.lower_bound): 
                print("[{0}]".format(self.upper_bound), end="", file=res, flush=True)
            else: 
                print("[{0}..{1}]".format(self.lower_bound, self.upper_bound), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def convert_inner_value_to_outer_value(self, inner_value : str, lang : 'MorphLang'=None) -> str:
        if (inner_value is None): 
            return None
        val = str(inner_value)
        i = 0
        while i < len(self.inner_values): 
            if (Utils.compareStrings(self.inner_values[i], val, True) == 0 and (i < len(self.outer_values))): 
                if (lang is not None): 
                    if (lang.is_ua and (i < len(self.outer_valuesua)) and self.outer_valuesua[i] is not None): 
                        return self.outer_valuesua[i]
                    if (lang.is_en and (i < len(self.outer_valuesen)) and self.outer_valuesen[i] is not None): 
                        return self.outer_valuesen[i]
                return self.outer_values[i]
            i += 1
        return inner_value
    
    def convert_outer_value_to_inner_value(self, outer_value : str) -> str:
        if (outer_value is None): 
            return None
        i = 0
        while i < len(self.outer_values): 
            if (Utils.compareStrings(self.outer_values[i], outer_value, True) == 0 and (i < len(self.inner_values))): 
                return self.inner_values[i]
            elif ((i < len(self.outer_valuesua)) and self.outer_valuesua[i] == outer_value): 
                return self.inner_values[i]
            i += 1
        return outer_value
    
    def add_value(self, int_val : str, ext_val : str, ext_val_ua : str=None, ext_val_eng : str=None) -> None:
        self.inner_values.append(int_val)
        self.outer_values.append(ext_val)
        self.outer_valuesua.append(ext_val_ua)
        self.outer_valuesen.append(ext_val_eng)
    
    @staticmethod
    def _new1743(_arg1 : str, _arg2 : str, _arg3 : int, _arg4 : int) -> 'Feature':
        res = Feature()
        res.name = _arg1
        res.caption = _arg2
        res.lower_bound = _arg3
        res.upper_bound = _arg4
        return res