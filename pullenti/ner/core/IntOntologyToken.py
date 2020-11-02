# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.MetaToken import MetaToken

class IntOntologyToken(MetaToken):
    # Это привязка элемента внутренней отнологии к тексту
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.item = None;
        self.termin = None;
    
    @staticmethod
    def _new491(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'IntOntologyItem', _arg4 : 'Termin', _arg5 : 'MorphCollection') -> 'IntOntologyToken':
        res = IntOntologyToken(_arg1, _arg2)
        res.item = _arg3
        res.termin = _arg4
        res.morph = _arg5
        return res