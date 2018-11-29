# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.internal.SerializerHelper import SerializerHelper


class ReferentToken(MetaToken):
    """ Токен, соответствующий сущности """
    
    def __init__(self, entity : 'Referent', begin : 'Token', end : 'Token', kit_ : 'AnalysisKit'=None) -> None:
        from pullenti.ner.MorphCollection import MorphCollection
        super().__init__(begin, end, kit_)
        self.referent = None;
        self.data = None;
        self.misc_attrs = 0
        self.referent = entity
        if (self.morph is None): 
            self.morph = MorphCollection()
    
    def __str__(self) -> str:
        res = Utils.newStringIO(("Null" if self.referent is None else str(self.referent)))
        if (self.morph is not None): 
            print(" {0}".format(str(self.morph)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def is_referent(self) -> bool:
        return True
    
    def saveToLocalOntology(self) -> None:
        from pullenti.ner.TextAnnotation import TextAnnotation
        if (self.data is None): 
            return
        r = self.data.registerReferent(self.referent)
        self.data = (None)
        if (r is not None): 
            self.referent = r
            anno = TextAnnotation()
            anno.sofa = self.kit.sofa
            anno.occurence_of = self.referent
            anno.begin_char = self.begin_char
            anno.end_char = self.end_char
            self.referent.addOccurence(anno)
    
    def setDefaultLocalOnto(self, proc : 'Processor') -> None:
        if (self.referent is None or self.kit is None or proc is None): 
            return
        for a in proc.analyzers: 
            if (a.createReferent(self.referent.type_name) is not None): 
                self.data = self.kit.getAnalyzerData(a)
                break
    
    def _replaceReferent(self, old_referent : 'Referent', new_referent : 'Referent') -> None:
        if (self.referent == old_referent): 
            self.referent = new_referent
        if (self.end_token is None): 
            return
        t = self.begin_token
        while t is not None: 
            if (t.end_char > self.end_char): 
                break
            if (isinstance(t, ReferentToken)): 
                (Utils.asObjectOrNull(t, ReferentToken))._replaceReferent(old_referent, new_referent)
            if (t == self.end_token): 
                break
            t = t.next0_
    
    def _serialize(self, stream : io.IOBase) -> None:
        super()._serialize(stream)
        id0_ = 0
        if (self.referent is not None and (isinstance(self.referent.tag, int))): 
            id0_ = (self.referent.tag)
        SerializerHelper.serializeInt(stream, id0_)
    
    def _deserialize(self, stream : io.IOBase, kit_ : 'AnalysisKit') -> None:
        super()._deserialize(stream, kit_)
        id0_ = SerializerHelper.deserializeInt(stream)
        if (id0_ > 0): 
            self.referent = kit_.entities[id0_ - 1]
    
    @staticmethod
    def _new115(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AnalyzerData') -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.data = _arg4
        return res
    
    @staticmethod
    def _new746(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'MorphCollection') -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new748(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : object) -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.tag = _arg4
        return res
    
    @staticmethod
    def _new1252(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'MorphCollection', _arg5 : 'AnalyzerData') -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.morph = _arg4
        res.data = _arg5
        return res
    
    @staticmethod
    def _new2341(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'MorphCollection', _arg5 : int) -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.morph = _arg4
        res.misc_attrs = _arg5
        return res
    
    @staticmethod
    def _new2440(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : int) -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.misc_attrs = _arg4
        return res
    
    @staticmethod
    def _new2450(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'MorphCollection', _arg5 : object) -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.morph = _arg4
        res.tag = _arg5
        return res