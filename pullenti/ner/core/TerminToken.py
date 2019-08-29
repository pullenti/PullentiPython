# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.ner.MetaToken import MetaToken

class TerminToken(MetaToken):
    """ Результат привязки термина """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.termin = None;
        self.abridge_without_point = False
    
    @staticmethod
    def _new626(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'TerminToken':
        res = TerminToken(_arg1, _arg2)
        res.abridge_without_point = _arg3
        return res
    
    @staticmethod
    def _new629(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Termin') -> 'TerminToken':
        res = TerminToken(_arg1, _arg2)
        res.termin = _arg3
        return res
    
    @staticmethod
    def _new634(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection') -> 'TerminToken':
        res = TerminToken(_arg1, _arg2)
        res.morph = _arg3
        return res
    
    @staticmethod
    def _new640(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : 'Termin') -> 'TerminToken':
        res = TerminToken(_arg1, _arg2)
        res.morph = _arg3
        res.termin = _arg4
        return res