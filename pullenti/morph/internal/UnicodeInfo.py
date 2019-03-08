# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

class UnicodeInfo:
    """ Ввели для оптимизации на Питоне. """
    
    ALL_CHARS = None
    
    @staticmethod
    def initialize() -> None:
        pass
    
    def __init__(self, v : int=0) -> None:
        self.__m_value = 0
        self.uni_char = None;
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
    def is_whitespace0(self) -> bool:
        return (((self.__m_value) & 0x1)) != 0
    @is_whitespace0.setter
    def is_whitespace0(self, value) -> bool:
        self.__set_value(0, value)
        return value
    
    @property
    def is_digit0(self) -> bool:
        return (((self.__m_value) & 0x2)) != 0
    @is_digit0.setter
    def is_digit0(self, value) -> bool:
        self.__set_value(1, value)
        return value
    
    @property
    def is_letter0(self) -> bool:
        return (((self.__m_value) & 0x4)) != 0
    @is_letter0.setter
    def is_letter0(self, value) -> bool:
        self.__set_value(2, value)
        return value
    
    @property
    def is_upper0(self) -> bool:
        return (((self.__m_value) & 0x8)) != 0
    @is_upper0.setter
    def is_upper0(self, value) -> bool:
        self.__set_value(3, value)
        return value
    
    @property
    def is_lower0(self) -> bool:
        return (((self.__m_value) & 0x10)) != 0
    @is_lower0.setter
    def is_lower0(self, value) -> bool:
        self.__set_value(4, value)
        return value
    
    @property
    def is_latin0(self) -> bool:
        return (((self.__m_value) & 0x20)) != 0
    @is_latin0.setter
    def is_latin0(self, value) -> bool:
        self.__set_value(5, value)
        return value
    
    @property
    def is_cyrillic0(self) -> bool:
        return (((self.__m_value) & 0x40)) != 0
    @is_cyrillic0.setter
    def is_cyrillic0(self, value) -> bool:
        self.__set_value(6, value)
        return value
    
    @property
    def is_hiphen0(self) -> bool:
        return (((self.__m_value) & 0x80)) != 0
    @is_hiphen0.setter
    def is_hiphen0(self, value) -> bool:
        self.__set_value(7, value)
        return value
    
    @property
    def is_vowel0(self) -> bool:
        return (((self.__m_value) & 0x100)) != 0
    @is_vowel0.setter
    def is_vowel0(self, value) -> bool:
        self.__set_value(8, value)
        return value
    
    @property
    def is_quot0(self) -> bool:
        return (((self.__m_value) & 0x200)) != 0
    @is_quot0.setter
    def is_quot0(self, value) -> bool:
        self.__set_value(9, value)
        return value
    
    @property
    def is_apos0(self) -> bool:
        return (((self.__m_value) & 0x400)) != 0
    @is_apos0.setter
    def is_apos0(self, value) -> bool:
        self.__set_value(10, value)
        return value
    
    @property
    def is_udaren0(self) -> bool:
        return (((self.__m_value) & 0x800)) != 0
    @is_udaren0.setter
    def is_udaren0(self, value) -> bool:
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
                ui.is_whitespace0 = True
            elif (str.isdigit(ch)): 
                ui.is_digit0 = True
            elif (ch == 'º' or ch == '°'): 
                pass
            elif (str.isalpha(ch)): 
                ui.is_letter0 = True
                if (i >= 0x400 and (i < 0x500)): 
                    ui.is_cyrillic0 = True
                    if ("АЕЁИОУЮЯЫЭЄІЇЎӘӨҰҮІ".find(ch) >= 0): 
                        ui.is_vowel0 = True
                elif (i < 0x200): 
                    ui.is_latin0 = True
                    if ("AEIOUY".find(ch) >= 0): 
                        ui.is_vowel0 = True
                if (str.isupper(ch)): 
                    ui.is_upper0 = True
                if (str.islower(ch)): 
                    ui.is_lower0 = True
            else: 
                if (((((ch == '-' or ch == '–' or ch == '¬') or ch == '-' or ch == (chr(0x00AD))) or ch == (chr(0x2011)) or ch == '-') or ch == '—' or ch == '–') or ch == '−' or ch == '-'): 
                    ui.is_hiphen0 = True
                if ("\"'`“”’".find(ch) >= 0): 
                    ui.is_quot0 = True
                if ("'`’".find(ch) >= 0): 
                    ui.is_apos0 = True
                    ui.is_quot0 = True
            if (i >= 0x300 and (i < 0x370)): 
                ui.is_udaren0 = True
            UnicodeInfo.ALL_CHARS.append(ui)

UnicodeInfo._static_ctor()