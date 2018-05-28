# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.core.Termin import Termin
from pullenti.morph.MorphLang import MorphLang


class TerrTermin(Termin):
    
    def __init__(self, source : str, lang_ : 'MorphLang'=MorphLang()) -> None:
        self.is_state = False
        self.is_region = False
        self.is_adjective = False
        self.is_always_prefix = False
        self.is_doubt = False
        self.is_moscow_region = False
        self.is_strong = False
        self.is_specific_prefix = False
        self.is_sovet = False
        super().__init__(None, lang_, False)
        self.init_by_normal_text(source, lang_)

    
    @staticmethod
    def _new1116(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        return res
    
    @staticmethod
    def _new1117(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        return res
    
    @staticmethod
    def _new1118(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        res.is_doubt = _arg3
        return res
    
    @staticmethod
    def _new1119(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new1122(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        res.is_adjective = _arg3
        return res
    
    @staticmethod
    def _new1123(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        res.is_adjective = _arg4
        return res
    
    @staticmethod
    def _new1124(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        return res
    
    @staticmethod
    def _new1127(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        return res
    
    @staticmethod
    def _new1128(_arg1 : str, _arg2 : bool, _arg3 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new1129(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1134(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_always_prefix = _arg3
        return res
    
    @staticmethod
    def _new1136(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_always_prefix = _arg4
        return res
    
    @staticmethod
    def _new1145(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_strong = _arg3
        return res
    
    @staticmethod
    def _new1148(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_strong = _arg4
        return res
    
    @staticmethod
    def _new1151(_arg1 : str, _arg2 : str, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.canonic_text = _arg2
        res.is_sovet = _arg3
        return res
    
    @staticmethod
    def _new1154(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_adjective = _arg3
        return res
    
    @staticmethod
    def _new1155(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_adjective = _arg4
        return res
    
    @staticmethod
    def _new1156(_arg1 : str, _arg2 : bool, _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_specific_prefix = _arg3
        res.is_always_prefix = _arg4
        return res
    
    @staticmethod
    def _new1157(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool, _arg5 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_specific_prefix = _arg4
        res.is_always_prefix = _arg5
        return res
    
    @staticmethod
    def _new1158(_arg1 : str, _arg2 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.acronym = _arg2
        return res
    
    @staticmethod
    def _new1159(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_moscow_region = _arg2
        return res