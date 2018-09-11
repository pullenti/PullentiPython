# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.morph.internal.UnicodeInfo import UnicodeInfo


class TextWrapper:
    """ Введено для ускорения Питона! """
    
    def __init__(self, txt : str, to_upper : bool) -> None:
        self.chars = list()
        self.text = None
        self.length = 0
        self.text = txt
        if (to_upper and txt is not None): 
            self.text = txt.upper()
        self.length = (0 if txt is None else len(txt))
        chars_ = UnicodeInfo.ALL_CHARS
        if (txt is not None): 
            i = 0
            while i < len(txt): 
                self.chars.append(chars_[ord(txt[i])])
                i += 1
    
    def __str__(self) -> str:
        return str(self.text)