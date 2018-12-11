# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

class MorphLang:
    """ Язык(и) """
    
    def __init__(self, lng : 'MorphLang'=None) -> None:
        self.value = 0
        self.value = (0)
        if (lng is not None): 
            self.value = lng.value
    
    def __getValue(self, i : int) -> bool:
        return (((((self.value) >> i)) & 1)) != 0
    
    def __setValue(self, i : int, val : bool) -> None:
        if (val): 
            self.value |= ((1 << i))
        else: 
            self.value &= (~ ((1 << i)))
    
    @property
    def is_undefined(self) -> bool:
        """ Неопределённый язык """
        return self.value == (0)
    @is_undefined.setter
    def is_undefined(self, value_) -> bool:
        self.value = (0)
        return value_
    
    @property
    def is_ru(self) -> bool:
        """ Русский язык """
        return self.__getValue(0)
    @is_ru.setter
    def is_ru(self, value_) -> bool:
        self.__setValue(0, value_)
        return value_
    
    @property
    def is_ua(self) -> bool:
        """ Украинский язык """
        return self.__getValue(1)
    @is_ua.setter
    def is_ua(self, value_) -> bool:
        self.__setValue(1, value_)
        return value_
    
    @property
    def is_by(self) -> bool:
        """ Белорусский язык """
        return self.__getValue(2)
    @is_by.setter
    def is_by(self, value_) -> bool:
        self.__setValue(2, value_)
        return value_
    
    @property
    def is_cyrillic(self) -> bool:
        """ Русский, украинский, белорусский или казахский язык """
        return (self.is_ru | self.is_ua | self.is_by) | self.is_kz
    
    @property
    def is_en(self) -> bool:
        """ Английский язык """
        return self.__getValue(3)
    @is_en.setter
    def is_en(self, value_) -> bool:
        self.__setValue(3, value_)
        return value_
    
    @property
    def is_it(self) -> bool:
        """ Итальянский язык """
        return self.__getValue(4)
    @is_it.setter
    def is_it(self, value_) -> bool:
        self.__setValue(4, value_)
        return value_
    
    @property
    def is_kz(self) -> bool:
        """ Казахский язык """
        return self.__getValue(5)
    @is_kz.setter
    def is_kz(self, value_) -> bool:
        self.__setValue(5, value_)
        return value_
    
    __m_names = None
    
    def __str__(self) -> str:
        tmp_str = io.StringIO()
        i = 0
        while i < len(MorphLang.__m_names): 
            if (self.__getValue(i)): 
                if (tmp_str.tell() > 0): 
                    print(";", end="", file=tmp_str)
                print(MorphLang.__m_names[i], end="", file=tmp_str)
            i += 1
        return Utils.toStringStringIO(tmp_str)
    
    def equals(self, obj : object) -> bool:
        if (not ((isinstance(obj, MorphLang)))): 
            return False
        return self.value == (obj).value
    
    def __hash__(self) -> int:
        return self.value
    
    @staticmethod
    def tryParse(str0_ : str, lang : 'MorphLang') -> bool:
        """ Преобразовать из строки
        
        Args:
            str0_(str): 
            lang(MorphLang): 
        
        """
        lang.value = MorphLang()
        while not Utils.isNullOrEmpty(str0_):
            i = 0
            while i < len(MorphLang.__m_names): 
                if (Utils.startsWithString(str0_, MorphLang.__m_names[i], True)): 
                    break
                i += 1
            if (i >= len(MorphLang.__m_names)): 
                break
            lang.value.value |= ((1 << i))
            i = 2
            while i < len(str0_): 
                if (str.isalpha(str0_[i])): 
                    break
                i += 1
            if (i >= len(str0_)): 
                break
            str0_ = str0_[i:]
        if (lang.value.is_undefined): 
            return False
        return True
    
    def __and__(self : 'MorphLang', arg2 : 'MorphLang') -> 'MorphLang':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphLang._new6(((val1) & (val2)))
    
    def __or__(self : 'MorphLang', arg2 : 'MorphLang') -> 'MorphLang':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphLang._new6(((val1) | (val2)))
    
    def __eq__(self : 'MorphLang', arg2 : 'MorphLang') -> bool:
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 == val2
    
    def __ne__(self : 'MorphLang', arg2 : 'MorphLang') -> bool:
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 != val2
    
    UNKNOWN = None
    
    RU = None
    
    UA = None
    
    BY = None
    
    EN = None
    
    IT = None
    
    KZ = None
    
    @staticmethod
    def _new6(_arg1 : int) -> 'MorphLang':
        res = MorphLang()
        res.value = _arg1
        return res
    
    @staticmethod
    def _new77(_arg1 : bool) -> 'MorphLang':
        res = MorphLang()
        res.is_ru = _arg1
        return res
    
    @staticmethod
    def _new78(_arg1 : bool) -> 'MorphLang':
        res = MorphLang()
        res.is_ua = _arg1
        return res
    
    @staticmethod
    def _new79(_arg1 : bool) -> 'MorphLang':
        res = MorphLang()
        res.is_by = _arg1
        return res
    
    @staticmethod
    def _new80(_arg1 : bool) -> 'MorphLang':
        res = MorphLang()
        res.is_en = _arg1
        return res
    
    @staticmethod
    def _new81(_arg1 : bool) -> 'MorphLang':
        res = MorphLang()
        res.is_it = _arg1
        return res
    
    @staticmethod
    def _new82(_arg1 : bool) -> 'MorphLang':
        res = MorphLang()
        res.is_kz = _arg1
        return res
    
    # static constructor for class MorphLang
    @staticmethod
    def _static_ctor():
        MorphLang.__m_names = ["RU", "UA", "BY", "EN", "IT", "KZ"]
        MorphLang.UNKNOWN = MorphLang()
        MorphLang.RU = MorphLang._new77(True)
        MorphLang.UA = MorphLang._new78(True)
        MorphLang.BY = MorphLang._new79(True)
        MorphLang.EN = MorphLang._new80(True)
        MorphLang.IT = MorphLang._new81(True)
        MorphLang.KZ = MorphLang._new82(True)

MorphLang._static_ctor()