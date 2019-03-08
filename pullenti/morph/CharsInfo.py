# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphClass import MorphClass

class CharsInfo:
    """ Информация о символах токена """
    
    def __init__(self, ci : 'CharsInfo'=None) -> None:
        self.value = 0
        self.value = (0)
        if (ci is not None): 
            self.value = ci.value
    
    def __get_value(self, i : int) -> bool:
        return (((((self.value) >> i)) & 1)) != 0
    
    def __set_value(self, i : int, val : bool) -> None:
        if (val): 
            self.value |= ((1 << i))
        else: 
            self.value &= (~ ((1 << i)))
    
    @property
    def is_all_upper0(self) -> bool:
        """ Все символы в верхнем регистре """
        return self.__get_value(0)
    @is_all_upper0.setter
    def is_all_upper0(self, value_) -> bool:
        self.__set_value(0, value_)
        return value_
    
    @property
    def is_all_lower0(self) -> bool:
        """ Все символы в нижнем регистре """
        return self.__get_value(1)
    @is_all_lower0.setter
    def is_all_lower0(self, value_) -> bool:
        self.__set_value(1, value_)
        return value_
    
    @property
    def is_capital_upper0(self) -> bool:
        """ ПЕрвый символ в верхнем регистре, остальные в нижнем.
         Для однобуквенной комбинации false. """
        return self.__get_value(2)
    @is_capital_upper0.setter
    def is_capital_upper0(self, value_) -> bool:
        self.__set_value(2, value_)
        return value_
    
    @property
    def is_last_lower0(self) -> bool:
        """ Все символы в верхнеи регистре, кроме последнего (длина >= 3) """
        return self.__get_value(3)
    @is_last_lower0.setter
    def is_last_lower0(self, value_) -> bool:
        self.__set_value(3, value_)
        return value_
    
    @property
    def is_letter0(self) -> bool:
        """ Это буквы """
        return self.__get_value(4)
    @is_letter0.setter
    def is_letter0(self, value_) -> bool:
        self.__set_value(4, value_)
        return value_
    
    @property
    def is_latin_letter0(self) -> bool:
        """ Это латиница """
        return self.__get_value(5)
    @is_latin_letter0.setter
    def is_latin_letter0(self, value_) -> bool:
        self.__set_value(5, value_)
        return value_
    
    @property
    def is_cyrillic_letter0(self) -> bool:
        """ Это кириллица """
        return self.__get_value(6)
    @is_cyrillic_letter0.setter
    def is_cyrillic_letter0(self, value_) -> bool:
        self.__set_value(6, value_)
        return value_
    
    def __str__(self) -> str:
        if (not self.is_letter0): 
            return "Nonletter"
        tmp_str = io.StringIO()
        if (self.is_all_upper0): 
            print("AllUpper", end="", file=tmp_str)
        elif (self.is_all_lower0): 
            print("AllLower", end="", file=tmp_str)
        elif (self.is_capital_upper0): 
            print("CapitalUpper", end="", file=tmp_str)
        elif (self.is_last_lower0): 
            print("LastLower", end="", file=tmp_str)
        else: 
            print("Nonstandard", end="", file=tmp_str)
        if (self.is_latin_letter0): 
            print(" Latin", end="", file=tmp_str)
        elif (self.is_cyrillic_letter0): 
            print(" Cyrillic", end="", file=tmp_str)
        elif (self.is_letter0): 
            print(" Letter", end="", file=tmp_str)
        return Utils.toStringStringIO(tmp_str)
    
    def equals(self, obj : object) -> bool:
        if (not ((isinstance(obj, MorphClass)))): 
            return False
        return self.value == (obj).value
    
    def __eq__(self : 'CharsInfo', arg2 : 'CharsInfo') -> bool:
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 == val2
    
    def __ne__(self : 'CharsInfo', arg2 : 'CharsInfo') -> bool:
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 != val2
    
    @staticmethod
    def _new2309(_arg1 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_capital_upper0 = _arg1
        return res
    
    @staticmethod
    def _new2484(_arg1 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_cyrillic_letter0 = _arg1
        return res
    
    @staticmethod
    def _new2490(_arg1 : bool, _arg2 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_cyrillic_letter0 = _arg1
        res.is_capital_upper0 = _arg2
        return res
    
    @staticmethod
    def _new2495(_arg1 : bool, _arg2 : bool, _arg3 : bool, _arg4 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_capital_upper0 = _arg1
        res.is_cyrillic_letter0 = _arg2
        res.is_latin_letter0 = _arg3
        res.is_letter0 = _arg4
        return res
    
    @staticmethod
    def _new2518(_arg1 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_latin_letter0 = _arg1
        return res
    
    @staticmethod
    def _new2761(_arg1 : int) -> 'CharsInfo':
        res = CharsInfo()
        res.value = _arg1
        return res