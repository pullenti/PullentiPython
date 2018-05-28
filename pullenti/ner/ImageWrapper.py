# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 


class ImageWrapper:
    """ Приходится работать через обёртку, так как некоторые реализации .NET не содержат System.Drawing
     (например, для Андроида) """
    
    def __init__(self) -> None:
        self.id0 = None
        self.content = None
        self.image = None

    
    @staticmethod
    def _new2488(_arg1 : str, _arg2 : bytearray) -> 'ImageWrapper':
        res = ImageWrapper()
        res.id0 = _arg1
        res.content = _arg2
        return res