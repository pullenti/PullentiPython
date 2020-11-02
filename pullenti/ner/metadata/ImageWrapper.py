# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


class ImageWrapper:
    """ Приходится работать через обёртку, так как ориентируемся на все платформы и языки """
    
    def __init__(self) -> None:
        self.id0_ = None;
        self.content = None;
        self.image = None;
    
    @staticmethod
    def _new2849(_arg1 : str, _arg2 : bytearray) -> 'ImageWrapper':
        res = ImageWrapper()
        res.id0_ = _arg1
        res.content = _arg2
        return res