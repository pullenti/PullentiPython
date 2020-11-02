# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class CharsInfo:
    """ Информация о символах токена
    
    Символьная информация
    """
    
    def __init__(self) -> None:
        self.value = 0
    
    def __get_value(self, i : int) -> bool:
        return (((((self.value) >> i)) & 1)) != 0
    
    def __set_value(self, i : int, val : bool) -> None:
        if (val): 
            self.value |= ((1 << i))
        else: 
            self.value &= (~ ((1 << i)))
    
    @property
    def is_all_upper(self) -> bool:
        """ Все символы в верхнем регистре """
        return self.__get_value(0)
    @is_all_upper.setter
    def is_all_upper(self, value_) -> bool:
        self.__set_value(0, value_)
        return value_
    
    @property
    def is_all_lower(self) -> bool:
        """ Все символы в нижнем регистре """
        return self.__get_value(1)
    @is_all_lower.setter
    def is_all_lower(self, value_) -> bool:
        self.__set_value(1, value_)
        return value_
    
    @property
    def is_capital_upper(self) -> bool:
        """ Первый символ в верхнем регистре, остальные в нижнем.
        Для однобуквенной комбинации false. """
        return self.__get_value(2)
    @is_capital_upper.setter
    def is_capital_upper(self, value_) -> bool:
        self.__set_value(2, value_)
        return value_
    
    @property
    def is_last_lower(self) -> bool:
        """ Все символы в верхнем регистре, кроме последнего (длина >= 3) """
        return self.__get_value(3)
    @is_last_lower.setter
    def is_last_lower(self, value_) -> bool:
        self.__set_value(3, value_)
        return value_
    
    @property
    def is_letter(self) -> bool:
        """ Это буквы """
        return self.__get_value(4)
    @is_letter.setter
    def is_letter(self, value_) -> bool:
        self.__set_value(4, value_)
        return value_
    
    @property
    def is_latin_letter(self) -> bool:
        """ Это латиница """
        return self.__get_value(5)
    @is_latin_letter.setter
    def is_latin_letter(self, value_) -> bool:
        self.__set_value(5, value_)
        return value_
    
    @property
    def is_cyrillic_letter(self) -> bool:
        """ Это кириллица """
        return self.__get_value(6)
    @is_cyrillic_letter.setter
    def is_cyrillic_letter(self, value_) -> bool:
        self.__set_value(6, value_)
        return value_
    
    def __str__(self) -> str:
        if (not self.is_letter): 
            return "Nonletter"
        tmp_str = io.StringIO()
        if (self.is_all_upper): 
            print("AllUpper", end="", file=tmp_str)
        elif (self.is_all_lower): 
            print("AllLower", end="", file=tmp_str)
        elif (self.is_capital_upper): 
            print("CapitalUpper", end="", file=tmp_str)
        elif (self.is_last_lower): 
            print("LastLower", end="", file=tmp_str)
        else: 
            print("Nonstandard", end="", file=tmp_str)
        if (self.is_latin_letter): 
            print(" Latin", end="", file=tmp_str)
        elif (self.is_cyrillic_letter): 
            print(" Cyrillic", end="", file=tmp_str)
        elif (self.is_letter): 
            print(" Letter", end="", file=tmp_str)
        return Utils.toStringStringIO(tmp_str)
    
    def equals(self, obj : object) -> bool:
        if (not (isinstance(obj, CharsInfo))): 
            return False
        return self.value == obj.value
    
    def __eq__(self : 'CharsInfo', arg2 : 'CharsInfo') -> bool:
        """ Моделирование сравнения ==
        
        Args:
            self(CharsInfo): первый аргумент
            arg2(CharsInfo): второй аргумент
        
        Returns:
            bool: arg1 == arg2
        """
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 == val2
    
    def __ne__(self : 'CharsInfo', arg2 : 'CharsInfo') -> bool:
        """ Моделирование неравенства !=
        
        Args:
            self(CharsInfo): первый аргумент
            arg2(CharsInfo): второй аргумент
        
        Returns:
            bool: arg1 != arg2
        """
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 != val2
    
    @staticmethod
    def _new2360(_arg1 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_capital_upper = _arg1
        return res
    
    @staticmethod
    def _new2541(_arg1 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_cyrillic_letter = _arg1
        return res
    
    @staticmethod
    def _new2547(_arg1 : bool, _arg2 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_cyrillic_letter = _arg1
        res.is_capital_upper = _arg2
        return res
    
    @staticmethod
    def _new2552(_arg1 : bool, _arg2 : bool, _arg3 : bool, _arg4 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_capital_upper = _arg1
        res.is_cyrillic_letter = _arg2
        res.is_latin_letter = _arg3
        res.is_letter = _arg4
        return res
    
    @staticmethod
    def _new2557(_arg1 : int) -> 'CharsInfo':
        res = CharsInfo()
        res.value = _arg1
        return res
    
    @staticmethod
    def _new2576(_arg1 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_latin_letter = _arg1
        return res