# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.morph.internal.UnicodeInfo import UnicodeInfo

class TextWrapper:
    # Введено для ускорения Питона!
    
    def __init__(self, txt : str, to_upper : bool) -> None:
        self.chars = list()
        self.text = None;
        self.length = 0
        if (to_upper and txt is not None): 
            self.text = txt.upper()
        else: 
            self.text = txt
        self.length = (0 if txt is None else len(txt))
        chars_ = UnicodeInfo.ALL_CHARS
        if (txt is not None): 
            i = 0
            while i < len(txt): 
                self.chars.append(chars_[ord(txt[i])])
                i += 1
    
    def __str__(self) -> str:
        return str(self.text)