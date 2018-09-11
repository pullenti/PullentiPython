# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.unisharp.Utils import Utils


class UnicodeInfo:
    """ Ввели для оптимизации на Питоне. """
    
    ALL_CHARS = None
    
    @staticmethod
    def initialize() -> None:
        pass
    
    def __init__(self, v : int=0) -> None:
        self.__m_value = 0
        self.uni_char = None
        self.code = 0
        self.uni_char = (chr(v))
        self.code = (v)
        self.__m_value = (0)
    
    def __get_value(self, i : int) -> bool:
        return (((((self.__m_value) >> i)) & 1)) != 0
    
    def __set_value(self, i : int, val : bool) -> None:
        if (val): 
            self.__m_value |= ((1 << i))
        else: 
            self.__m_value &= (~ ((1 << i)))
    
    @property
    def is_whitespace(self) -> bool:
        return (((self.__m_value) & 0x1)) != 0
    
    @is_whitespace.setter
    def is_whitespace(self, value) -> bool:
        self.__set_value(0, value)
        return value
    
    @property
    def is_digit(self) -> bool:
        return (((self.__m_value) & 0x2)) != 0
    
    @is_digit.setter
    def is_digit(self, value) -> bool:
        self.__set_value(1, value)
        return value
    
    @property
    def is_letter(self) -> bool:
        return (((self.__m_value) & 0x4)) != 0
    
    @is_letter.setter
    def is_letter(self, value) -> bool:
        self.__set_value(2, value)
        return value
    
    @property
    def is_upper(self) -> bool:
        return (((self.__m_value) & 0x8)) != 0
    
    @is_upper.setter
    def is_upper(self, value) -> bool:
        self.__set_value(3, value)
        return value
    
    @property
    def is_lower(self) -> bool:
        return (((self.__m_value) & 0x10)) != 0
    
    @is_lower.setter
    def is_lower(self, value) -> bool:
        self.__set_value(4, value)
        return value
    
    @property
    def is_latin(self) -> bool:
        return (((self.__m_value) & 0x20)) != 0
    
    @is_latin.setter
    def is_latin(self, value) -> bool:
        self.__set_value(5, value)
        return value
    
    @property
    def is_cyrillic(self) -> bool:
        return (((self.__m_value) & 0x40)) != 0
    
    @is_cyrillic.setter
    def is_cyrillic(self, value) -> bool:
        self.__set_value(6, value)
        return value
    
    @property
    def is_hiphen(self) -> bool:
        return (((self.__m_value) & 0x80)) != 0
    
    @is_hiphen.setter
    def is_hiphen(self, value) -> bool:
        self.__set_value(7, value)
        return value
    
    @property
    def is_vowel(self) -> bool:
        return (((self.__m_value) & 0x100)) != 0
    
    @is_vowel.setter
    def is_vowel(self, value) -> bool:
        self.__set_value(8, value)
        return value
    
    @property
    def is_quot(self) -> bool:
        return (((self.__m_value) & 0x200)) != 0
    
    @is_quot.setter
    def is_quot(self, value) -> bool:
        self.__set_value(9, value)
        return value
    
    @property
    def is_apos(self) -> bool:
        return (((self.__m_value) & 0x400)) != 0
    
    @is_apos.setter
    def is_apos(self, value) -> bool:
        self.__set_value(10, value)
        return value
    
    @property
    def is_udaren(self) -> bool:
        return (((self.__m_value) & 0x800)) != 0
    
    @is_udaren.setter
    def is_udaren(self, value) -> bool:
        self.__set_value(11, value)
        return value
    
    # static constructor for class UnicodeInfo
    @staticmethod
    def _static_ctor():
        UnicodeInfo.ALL_CHARS = list()
        for i in range(0x10000):
            ch = chr(i)
            ui = UnicodeInfo(i)
            if (Utils.isWhitespace(ch)): 
                ui.is_whitespace = True
            elif (str.isdigit(ch)): 
                ui.is_digit = True
            elif (ch == 'º' or ch == '°'): 
                pass
            elif (str.isalpha(ch)): 
                ui.is_letter = True
                if (i >= 0x400 and (i < 0x500)): 
                    ui.is_cyrillic = True
                    if ("АЕЁИОУЮЯЫЭЄІЇЎӘӨҰҮІ".find(ch) >= 0): 
                        ui.is_vowel = True
                elif (i < 0x200): 
                    ui.is_latin = True
                    if ("AEIOUY".find(ch) >= 0): 
                        ui.is_vowel = True
                if (str.isupper(ch)): 
                    ui.is_upper = True
                if (str.islower(ch)): 
                    ui.is_lower = True
            else: 
                if (((((ch == '-' or ch == '–' or ch == '¬') or ch == '-' or ch == (chr(0x00AD))) or ch == (chr(0x2011)) or ch == '-') or ch == '—' or ch == '–') or ch == '−' or ch == '-'): 
                    ui.is_hiphen = True
                if ("\"'`“”’".find(ch) >= 0): 
                    ui.is_quot = True
                if ("'`’".find(ch) >= 0): 
                    ui.is_apos = True
                    ui.is_quot = True
            if (i >= 0x300 and (i < 0x370)): 
                ui.is_udaren = True
            UnicodeInfo.ALL_CHARS.append(ui)

UnicodeInfo._static_ctor()