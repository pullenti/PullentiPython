# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.core.Termin import Termin

class TerrTermin(Termin):
    
    def __init__(self, source : str, lang_ : 'MorphLang'=None) -> None:
        super().__init__(None, lang_, False)
        self.is_state = False
        self.is_region = False
        self.is_adjective = False
        self.is_always_prefix = False
        self.is_doubt = False
        self.is_moscow_region = False
        self.is_strong = False
        self.is_specific_prefix = False
        self.is_sovet = False
        self.init_by_normal_text(source, lang_)
    
    @staticmethod
    def _new1193(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        return res
    
    @staticmethod
    def _new1194(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        return res
    
    @staticmethod
    def _new1195(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        res.is_doubt = _arg3
        return res
    
    @staticmethod
    def _new1196(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new1199(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        res.is_adjective = _arg3
        return res
    
    @staticmethod
    def _new1200(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        res.is_adjective = _arg4
        return res
    
    @staticmethod
    def _new1201(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        return res
    
    @staticmethod
    def _new1204(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        return res
    
    @staticmethod
    def _new1205(_arg1 : str, _arg2 : bool, _arg3 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new1206(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1212(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_always_prefix = _arg3
        return res
    
    @staticmethod
    def _new1216(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_always_prefix = _arg4
        return res
    
    @staticmethod
    def _new1225(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_strong = _arg3
        return res
    
    @staticmethod
    def _new1228(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_strong = _arg4
        return res
    
    @staticmethod
    def _new1231(_arg1 : str, _arg2 : str, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.canonic_text = _arg2
        res.is_sovet = _arg3
        return res
    
    @staticmethod
    def _new1234(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_adjective = _arg3
        return res
    
    @staticmethod
    def _new1235(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_adjective = _arg4
        return res
    
    @staticmethod
    def _new1236(_arg1 : str, _arg2 : bool, _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_specific_prefix = _arg3
        res.is_always_prefix = _arg4
        return res
    
    @staticmethod
    def _new1237(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool, _arg5 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_specific_prefix = _arg4
        res.is_always_prefix = _arg5
        return res
    
    @staticmethod
    def _new1238(_arg1 : str, _arg2 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.acronym = _arg2
        return res
    
    @staticmethod
    def _new1239(_arg1 : str, _arg2 : str, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.acronym = _arg2
        res.is_region = _arg3
        return res
    
    @staticmethod
    def _new1241(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_moscow_region = _arg2
        return res