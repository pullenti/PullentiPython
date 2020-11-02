# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing

from pullenti.ner.measure.internal.UnitsFactors import UnitsFactors
from pullenti.ner.measure.MeasureKind import MeasureKind

class Unit:
    # Единица измерения (задаётся в "базе")
    
    def __init__(self, name_cyr_ : str, name_lat_ : str, fname_cyr : str, fname_lan : str) -> None:
        self.name_cyr = None;
        self.name_lat = None;
        self.fullname_cyr = None;
        self.fullname_lat = None;
        self.kind = MeasureKind.UNDEFINED
        self.base_unit = None;
        self.mult_unit = None;
        self.base_multiplier = 0
        self.factor = UnitsFactors.NO
        self.keywords = list()
        self.psevdo = list()
        self.name_cyr = name_cyr_
        self.name_lat = name_lat_
        self.fullname_cyr = fname_cyr
        self.fullname_lat = fname_lan
    
    def __str__(self) -> str:
        return self.name_cyr
    
    @staticmethod
    def _new1643(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : str, _arg5 : 'MeasureKind') -> 'Unit':
        res = Unit(_arg1, _arg2, _arg3, _arg4)
        res.kind = _arg5
        return res
    
    @staticmethod
    def _new1647(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : str, _arg5 : 'Unit', _arg6 : float, _arg7 : 'MeasureKind') -> 'Unit':
        res = Unit(_arg1, _arg2, _arg3, _arg4)
        res.base_unit = _arg5
        res.base_multiplier = _arg6
        res.kind = _arg7
        return res
    
    @staticmethod
    def _new1694(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : str, _arg5 : 'Unit', _arg6 : float) -> 'Unit':
        res = Unit(_arg1, _arg2, _arg3, _arg4)
        res.base_unit = _arg5
        res.base_multiplier = _arg6
        return res
    
    @staticmethod
    def _new1702(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : str, _arg5 : 'Unit', _arg6 : 'Unit') -> 'Unit':
        res = Unit(_arg1, _arg2, _arg3, _arg4)
        res.base_unit = _arg5
        res.mult_unit = _arg6
        return res
    
    @staticmethod
    def _new1729(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : str, _arg5 : 'UnitsFactors', _arg6 : float, _arg7 : 'Unit', _arg8 : 'MeasureKind', _arg9 : typing.List[str]) -> 'Unit':
        res = Unit(_arg1, _arg2, _arg3, _arg4)
        res.factor = _arg5
        res.base_multiplier = _arg6
        res.base_unit = _arg7
        res.kind = _arg8
        res.keywords = _arg9
        return res