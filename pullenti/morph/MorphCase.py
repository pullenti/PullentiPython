# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils


class MorphCase:
    """ Падеж """
    
    def __init__(self, val : 'MorphCase'=None) -> None:
        self.value = 0
        self.value = (0)
        if (val is not None): 
            self.value = val.value
    
    @property
    def is_undefined(self) -> bool:
        return self.value == (0)
    @is_undefined.setter
    def is_undefined(self, value_) -> bool:
        self.value = (0)
        return value_
    
    def __getValue(self, i : int) -> bool:
        return (((((self.value) >> i)) & 1)) != 0
    
    def __setValue(self, i : int, val : bool) -> None:
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
    
    GENITIVE = None
    
    DATIVE = None
    
    ACCUSATIVE = None
    
    INSTRUMENTAL = None
    
    PREPOSITIONAL = None
    
    VOCATIVE = None
    
    PARTIAL = None
    
    COMMON = None
    
    POSSESSIVE = None
    
    ALL_CASES = None
    
    @property
    def is_nominative(self) -> bool:
        """ Именительный """
        return self.__getValue(0)
    @is_nominative.setter
    def is_nominative(self, value_) -> bool:
        self.__setValue(0, value_)
        return value_
    
    @property
    def is_genitive(self) -> bool:
        """ Родительный """
        return self.__getValue(1)
    @is_genitive.setter
    def is_genitive(self, value_) -> bool:
        self.__setValue(1, value_)
        return value_
    
    @property
    def is_dative(self) -> bool:
        """ Дательный """
        return self.__getValue(2)
    @is_dative.setter
    def is_dative(self, value_) -> bool:
        self.__setValue(2, value_)
        return value_
    
    @property
    def is_accusative(self) -> bool:
        """ Винительный """
        return self.__getValue(3)
    @is_accusative.setter
    def is_accusative(self, value_) -> bool:
        self.__setValue(3, value_)
        return value_
    
    @property
    def is_instrumental(self) -> bool:
        """ Творительный """
        return self.__getValue(4)
    @is_instrumental.setter
    def is_instrumental(self, value_) -> bool:
        self.__setValue(4, value_)
        return value_
    
    @property
    def is_prepositional(self) -> bool:
        """ Предложный """
        return self.__getValue(5)
    @is_prepositional.setter
    def is_prepositional(self, value_) -> bool:
        self.__setValue(5, value_)
        return value_
    
    @property
    def is_vocative(self) -> bool:
        """ Звательный """
        return self.__getValue(6)
    @is_vocative.setter
    def is_vocative(self, value_) -> bool:
        self.__setValue(6, value_)
        return value_
    
    @property
    def is_partial(self) -> bool:
        """ Частичный """
        return self.__getValue(7)
    @is_partial.setter
    def is_partial(self, value_) -> bool:
        self.__setValue(7, value_)
        return value_
    
    @property
    def is_common(self) -> bool:
        """ Общий (для английского) """
        return self.__getValue(8)
    @is_common.setter
    def is_common(self, value_) -> bool:
        self.__setValue(8, value_)
        return value_
    
    @property
    def is_possessive(self) -> bool:
        """ Притяжательный (для английского) """
        return self.__getValue(9)
    @is_possessive.setter
    def is_possessive(self, value_) -> bool:
        self.__setValue(9, value_)
        return value_
    
    __m_names = None
    
    def __str__(self) -> str:
        tmp_str = io.StringIO()
        i = 0
        while i < len(MorphCase.__m_names): 
            if (self.__getValue(i)): 
                if (tmp_str.tell() > 0): 
                    print("|", end="", file=tmp_str)
                print(MorphCase.__m_names[i], end="", file=tmp_str)
            i += 1
        return Utils.toStringStringIO(tmp_str)
    
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
                    res.__setValue(i, True)
                    break
                i += 1
        return res
    
    def equals(self, obj : object) -> bool:
        if (not ((isinstance(obj, MorphCase)))): 
            return False
        return self.value == (obj).value
    
    def __hash__(self) -> int:
        return self.value
    
    def __and__(self : 'MorphCase', arg2 : 'MorphCase') -> 'MorphCase':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphCase._new48(((val1) & (val2)))
    
    def __or__(self : 'MorphCase', arg2 : 'MorphCase') -> 'MorphCase':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphCase._new48(((val1) | (val2)))
    
    def __xor__(self : 'MorphCase', arg2 : 'MorphCase') -> 'MorphCase':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphCase._new48(((val1) ^ (val2)))
    
    def __eq__(self : 'MorphCase', arg2 : 'MorphCase') -> bool:
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 == val2
    
    def __ne__(self : 'MorphCase', arg2 : 'MorphCase') -> bool:
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 != val2
    
    @staticmethod
    def _new48(_arg1 : int) -> 'MorphCase':
        res = MorphCase()
        res.value = _arg1
        return res
    
    # static constructor for class MorphCase
    @staticmethod
    def _static_ctor():
        MorphCase.UNDEFINED = MorphCase._new48(0)
        MorphCase.NOMINATIVE = MorphCase._new48(1)
        MorphCase.GENITIVE = MorphCase._new48(2)
        MorphCase.DATIVE = MorphCase._new48(4)
        MorphCase.ACCUSATIVE = MorphCase._new48(8)
        MorphCase.INSTRUMENTAL = MorphCase._new48(0x10)
        MorphCase.PREPOSITIONAL = MorphCase._new48(0x20)
        MorphCase.VOCATIVE = MorphCase._new48(0x40)
        MorphCase.PARTIAL = MorphCase._new48(0x80)
        MorphCase.COMMON = MorphCase._new48(0x100)
        MorphCase.POSSESSIVE = MorphCase._new48(0x200)
        MorphCase.ALL_CASES = MorphCase._new48(0x3FF)
        MorphCase.__m_names = ["именит.", "родит.", "дател.", "винит.", "творит.", "предлож.", "зват.", "частич.", "общ.", "притяж."]

MorphCase._static_ctor()