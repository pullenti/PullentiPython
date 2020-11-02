# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class MorphCase:
    """ Падеж """
    
    def __init__(self) -> None:
        self.value = 0
    
    @property
    def is_undefined(self) -> bool:
        return self.value == (0)
    @is_undefined.setter
    def is_undefined(self, value_) -> bool:
        self.value = (0)
        return value_
    
    def __get_value(self, i : int) -> bool:
        return (((((self.value) >> i)) & 1)) != 0
    
    def __set_value(self, i : int, val : bool) -> None:
        if (val): 
            self.value |= ((1 << i))
        else: 
            self.value &= (~ ((1 << i)))
    
    @property
    def count(self) -> int:
        """ Количество падежей """
        if (self.value == (0)): 
            return 0
        cou = 0
        for i in range(12):
            if ((((self.value) & ((1 << i)))) != 0): 
                cou += 1
        return cou
    
    UNDEFINED = None
    
    NOMINATIVE = None
    """ Именительный падеж """
    
    GENITIVE = None
    """ Родительный падеж """
    
    DATIVE = None
    """ Дательный падеж """
    
    ACCUSATIVE = None
    """ Винительный падеж """
    
    INSTRUMENTAL = None
    """ Творительный падеж """
    
    PREPOSITIONAL = None
    """ Предложный падеж """
    
    VOCATIVE = None
    """ Звательный падеж """
    
    PARTIAL = None
    """ Частичный падеж """
    
    COMMON = None
    """ Общий падеж """
    
    POSSESSIVE = None
    """ Притяжательный падеж """
    
    ALL_CASES = None
    """ Все падежи одновременно """
    
    @property
    def is_nominative(self) -> bool:
        """ Именительный """
        return self.__get_value(0)
    @is_nominative.setter
    def is_nominative(self, value_) -> bool:
        self.__set_value(0, value_)
        return value_
    
    @property
    def is_genitive(self) -> bool:
        """ Родительный """
        return self.__get_value(1)
    @is_genitive.setter
    def is_genitive(self, value_) -> bool:
        self.__set_value(1, value_)
        return value_
    
    @property
    def is_dative(self) -> bool:
        """ Дательный """
        return self.__get_value(2)
    @is_dative.setter
    def is_dative(self, value_) -> bool:
        self.__set_value(2, value_)
        return value_
    
    @property
    def is_accusative(self) -> bool:
        """ Винительный """
        return self.__get_value(3)
    @is_accusative.setter
    def is_accusative(self, value_) -> bool:
        self.__set_value(3, value_)
        return value_
    
    @property
    def is_instrumental(self) -> bool:
        """ Творительный """
        return self.__get_value(4)
    @is_instrumental.setter
    def is_instrumental(self, value_) -> bool:
        self.__set_value(4, value_)
        return value_
    
    @property
    def is_prepositional(self) -> bool:
        """ Предложный """
        return self.__get_value(5)
    @is_prepositional.setter
    def is_prepositional(self, value_) -> bool:
        self.__set_value(5, value_)
        return value_
    
    @property
    def is_vocative(self) -> bool:
        """ Звательный """
        return self.__get_value(6)
    @is_vocative.setter
    def is_vocative(self, value_) -> bool:
        self.__set_value(6, value_)
        return value_
    
    @property
    def is_partial(self) -> bool:
        """ Частичный """
        return self.__get_value(7)
    @is_partial.setter
    def is_partial(self, value_) -> bool:
        self.__set_value(7, value_)
        return value_
    
    @property
    def is_common(self) -> bool:
        """ Общий (для английского) """
        return self.__get_value(8)
    @is_common.setter
    def is_common(self, value_) -> bool:
        self.__set_value(8, value_)
        return value_
    
    @property
    def is_possessive(self) -> bool:
        """ Притяжательный (для английского) """
        return self.__get_value(9)
    @is_possessive.setter
    def is_possessive(self, value_) -> bool:
        self.__set_value(9, value_)
        return value_
    
    def __str__(self) -> str:
        tmp_str = io.StringIO()
        if (self.is_nominative): 
            print("именит.|", end="", file=tmp_str)
        if (self.is_genitive): 
            print("родит.|", end="", file=tmp_str)
        if (self.is_dative): 
            print("дател.|", end="", file=tmp_str)
        if (self.is_accusative): 
            print("винит.|", end="", file=tmp_str)
        if (self.is_instrumental): 
            print("творит.|", end="", file=tmp_str)
        if (self.is_prepositional): 
            print("предлож.|", end="", file=tmp_str)
        if (self.is_vocative): 
            print("зват.|", end="", file=tmp_str)
        if (self.is_partial): 
            print("частич.|", end="", file=tmp_str)
        if (self.is_common): 
            print("общ.|", end="", file=tmp_str)
        if (self.is_possessive): 
            print("притяж.|", end="", file=tmp_str)
        if (tmp_str.tell() > 0): 
            Utils.setLengthStringIO(tmp_str, tmp_str.tell() - 1)
        return Utils.toStringStringIO(tmp_str)
    
    __m_names = None
    
    @staticmethod
    def parse(str0_ : str) -> 'MorphCase':
        """ Восстановить падежи из строки, полученной ToString
        
        Args:
            str0_(str): 
        
        """
        res = MorphCase()
        if (Utils.isNullOrEmpty(str0_)): 
            return res
        for s in Utils.splitString(str0_, '|', False): 
            i = 0
            while i < len(MorphCase.__m_names): 
                if (s == MorphCase.__m_names[i]): 
                    res.__set_value(i, True)
                    break
                i += 1
        return res
    
    def equals(self, obj : object) -> bool:
        if (not (isinstance(obj, MorphCase))): 
            return False
        return self.value == obj.value
    
    def __hash__(self) -> int:
        return self.value
    
    def __and__(self : 'MorphCase', arg2 : 'MorphCase') -> 'MorphCase':
        """ Моделирование побитного "AND"
        
        Args:
            self(MorphCase): первый аргумент
            arg2(MorphCase): второй аргумент
        
        Returns:
            MorphCase: arg1 & arg2
        """
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphCase._new29(((val1) & (val2)))
    
    def __or__(self : 'MorphCase', arg2 : 'MorphCase') -> 'MorphCase':
        """ Моделирование побитного "OR"
        
        Args:
            self(MorphCase): первый аргумент
            arg2(MorphCase): второй аргумент
        
        Returns:
            MorphCase: arg1 | arg2
        """
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphCase._new29(((val1) | (val2)))
    
    def __xor__(self : 'MorphCase', arg2 : 'MorphCase') -> 'MorphCase':
        """ Моделирование побитного "XOR"
        
        Args:
            self(MorphCase): первый аргумент
            arg2(MorphCase): второй аргумент
        
        Returns:
            MorphCase: arg1 ^ arg2
        """
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphCase._new29(((val1) ^ (val2)))
    
    def __eq__(self : 'MorphCase', arg2 : 'MorphCase') -> bool:
        """ Моделирование сравнения ==
        
        Args:
            self(MorphCase): первый аргумент
            arg2(MorphCase): второй аргумент
        
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
    
    def __ne__(self : 'MorphCase', arg2 : 'MorphCase') -> bool:
        """ Моделирование неравенства !=
        
        Args:
            self(MorphCase): первый аргумент
            arg2(MorphCase): второй аргумент
        
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
    def _new29(_arg1 : int) -> 'MorphCase':
        res = MorphCase()
        res.value = _arg1
        return res
    
    # static constructor for class MorphCase
    @staticmethod
    def _static_ctor():
        MorphCase.UNDEFINED = MorphCase._new29(0)
        MorphCase.NOMINATIVE = MorphCase._new29(1)
        MorphCase.GENITIVE = MorphCase._new29(2)
        MorphCase.DATIVE = MorphCase._new29(4)
        MorphCase.ACCUSATIVE = MorphCase._new29(8)
        MorphCase.INSTRUMENTAL = MorphCase._new29(0x10)
        MorphCase.PREPOSITIONAL = MorphCase._new29(0x20)
        MorphCase.VOCATIVE = MorphCase._new29(0x40)
        MorphCase.PARTIAL = MorphCase._new29(0x80)
        MorphCase.COMMON = MorphCase._new29(0x100)
        MorphCase.POSSESSIVE = MorphCase._new29(0x200)
        MorphCase.ALL_CASES = MorphCase._new29(0x3FF)
        MorphCase.__m_names = ["именит.", "родит.", "дател.", "винит.", "творит.", "предлож.", "зват.", "частич.", "общ.", "притяж."]

MorphCase._static_ctor()