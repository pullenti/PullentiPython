# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.ner.MetaToken import MetaToken

class Quantity(MetaToken):
    """ Количественная характеристика.
     Тут предстоит очень много сделать (сложная модель диапазонов, составных значений и пр.) """
    
    def __init__(self, spelling_ : str, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.spelling = None;
        self.spelling = spelling_
    
    def __str__(self) -> str:
        return self.spelling