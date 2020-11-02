# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


class CanonicDecreeRefUri:
    
    def __init__(self, txt : str) -> None:
        self.ref = None;
        self.begin_char = 0
        self.end_char = 0
        self.is_diap = False
        self.is_adopted = False
        self.type_with_geo = None;
        self.text = None;
        self.text = txt
    
    def __str__(self) -> str:
        return ("?" if self.text is None else self.text[self.begin_char:self.begin_char+(self.end_char + 1) - self.begin_char])
    
    @staticmethod
    def _new833(_arg1 : str, _arg2 : 'Referent', _arg3 : int, _arg4 : int) -> 'CanonicDecreeRefUri':
        res = CanonicDecreeRefUri(_arg1)
        res.ref = _arg2
        res.begin_char = _arg3
        res.end_char = _arg4
        return res
    
    @staticmethod
    def _new835(_arg1 : str, _arg2 : 'Referent', _arg3 : int, _arg4 : int, _arg5 : bool) -> 'CanonicDecreeRefUri':
        res = CanonicDecreeRefUri(_arg1)
        res.ref = _arg2
        res.begin_char = _arg3
        res.end_char = _arg4
        res.is_diap = _arg5
        return res