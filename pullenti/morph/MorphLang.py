# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils


class MorphLang:
    """ Язык(и) """
    
    def __init__(self, lng : 'MorphLang'=None) -> None:
        self.value = 0
        self.value = 0
        if (lng is not None): 
            self.value = lng.value
    
    def __get_value(self, i : int) -> bool:
        return ((((self.value >> i)) & 1)) != 0
    
    def __set_value(self, i : int, val : bool) -> None:
        if (val): 
            self.value |= (1 << i)
        else: 
            self.value &= ~ ((1 << i))
    
    @property
    def is_undefined(self) -> bool:
        """ Неопределённый язык """
        return self.value == 0
    
    @is_undefined.setter
    def is_undefined(self, value_) -> bool:
        self.value = 0
        return value_
    
    @property
    def is_ru(self) -> bool:
        """ Русский язык """
        return self.__get_value(0)
    
    @is_ru.setter
    def is_ru(self, value_) -> bool:
        self.__set_value(0, value_)
        return value_
    
    @property
    def is_ua(self) -> bool:
        """ Украинский язык """
        return self.__get_value(1)
    
    @is_ua.setter
    def is_ua(self, value_) -> bool:
        self.__set_value(1, value_)
        return value_
    
    @property
    def is_by(self) -> bool:
        """ Белорусский язык """
        return self.__get_value(2)
    
    @is_by.setter
    def is_by(self, value_) -> bool:
        self.__set_value(2, value_)
        return value_
    
    @property
    def is_cyrillic(self) -> bool:
        """ Русский, украинский, белорусский или казахский язык """
        return (self.is_ru | self.is_ua | self.is_by) | self.is_kz
    
    @property
    def is_en(self) -> bool:
        """ Английский язык """
        return self.__get_value(3)
    
    @is_en.setter
    def is_en(self, value_) -> bool:
        self.__set_value(3, value_)
        return value_
    
    @property
    def is_it(self) -> bool:
        """ Итальянский язык """
        return self.__get_value(4)
    
    @is_it.setter
    def is_it(self, value_) -> bool:
        self.__set_value(4, value_)
        return value_
    
    @property
    def is_kz(self) -> bool:
        """ Казахский язык """
        return self.__get_value(5)
    
    @is_kz.setter
    def is_kz(self, value_) -> bool:
        self.__set_value(5, value_)
        return value_
    
    __m_names = None
    
    def __str__(self) -> str:
        tmp_str = Utils.newStringIO(None)
        i = 0
        while i < len(MorphLang.__m_names): 
            if (self.__get_value(i)): 
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
    def try_parse(str0_ : str, lang : 'MorphLang') -> bool:
        """ Преобразовать из строки
        
        Args:
            str0_(str): 
            lang(MorphLang): 
        
        """
        lang.value = MorphLang()
        while not Utils.isNullOrEmpty(str0_):
            i = 0
            while i < len(MorphLang.__m_names): 
                if (str0_.upper().startswith(MorphLang.__m_names[i].upper())): 
                    break
                i += 1
            if (i >= len(MorphLang.__m_names)): 
                break
            lang.value.value |= (1 << i)
            for i in range(2, len(str0_), 1):
                if (str0_[i].isalpha()): 
                    break
            else: i = len(str0_)
            if (i >= len(str0_)): 
                break
            str0_ = str0_[i : ]
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
        return MorphLang._new6((val1 & val2))
    
    def __or__(self : 'MorphLang', arg2 : 'MorphLang') -> 'MorphLang':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphLang._new6((val1 | val2))
    
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
    """ Неопределённое """
    
    RU = None
    """ Русский """
    
    UA = None
    """ Украинский """
    
    BY = None
    """ Белорусский """
    
    EN = None
    """ Английский """
    
    IT = None
    """ Итальянский """
    
    KZ = None
    """ Казахский """

    
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