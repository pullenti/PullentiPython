# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


class ImageWrapper:
    """ Приходится работать через обёртку, так как некоторые реализации .NET не содержат System.Drawing
     (например, для Андроида) """
    
    def __init__(self) -> None:
        self.id0_ = None;
        self.content = None;
        self.image = None;
    
    @staticmethod
    def _new2815(_arg1 : str, _arg2 : bytearray) -> 'ImageWrapper':
        res = ImageWrapper()
        res.id0_ = _arg1
        res.content = _arg2
        return res