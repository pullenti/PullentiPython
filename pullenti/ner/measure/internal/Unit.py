# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.measure.internal.UnitsFactors import UnitsFactors


class Unit:
    """ Единица измерения (задаётся в "базе") """
    
    def __init__(self, name_cyr_ : str, name_lat_ : str, fname_cyr : str, fname_lan : str) -> None:
        self.name_cyr = None
        self.name_lat = None
        self.fullname_cyr = None
        self.fullname_lat = None
        self.base_unit = None
        self.mult_unit = None
        self.base_multiplier = 0
        self.factor = UnitsFactors.NO
        self.keywords = list()
        self.name_cyr = name_cyr_
        self.name_lat = name_lat_
        self.fullname_cyr = fname_cyr
        self.fullname_lat = fname_lan
    
    def __str__(self) -> str:
        return self.name_cyr
    
    @staticmethod
    def _new1537(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : str, _arg5 : 'Unit', _arg6 : float) -> 'Unit':
        res = Unit(_arg1, _arg2, _arg3, _arg4)
        res.base_unit = _arg5
        res.base_multiplier = _arg6
        return res
    
    @staticmethod
    def _new1579(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : str, _arg5 : 'Unit', _arg6 : 'Unit') -> 'Unit':
        res = Unit(_arg1, _arg2, _arg3, _arg4)
        res.base_unit = _arg5
        res.mult_unit = _arg6
        return res
    
    @staticmethod
    def _new1601(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : str, _arg5 : 'UnitsFactors', _arg6 : float, _arg7 : 'Unit') -> 'Unit':
        res = Unit(_arg1, _arg2, _arg3, _arg4)
        res.factor = _arg5
        res.base_multiplier = _arg6
        res.base_unit = _arg7
        return res