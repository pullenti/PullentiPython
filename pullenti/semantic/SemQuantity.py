# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.MetaToken import MetaToken

class SemQuantity(MetaToken):
    """ Количественная характеристика. Планируется переработка этого класса
    (поддержка сложной модели диапазонов, составных значений и пр.).
    Количество
    """
    
    def __init__(self, spelling_ : str, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.spelling = None;
        self.spelling = spelling_
    
    def __str__(self) -> str:
        return self.spelling