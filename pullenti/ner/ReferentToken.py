# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.TextAnnotation import TextAnnotation

class ReferentToken(MetaToken):
    """ Токен, соответствующий сущности
    Токен сущности
    """
    
    def __init__(self, entity : 'Referent', begin : 'Token', end : 'Token', kit_ : 'AnalysisKit'=None) -> None:
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
    
    def get_referent(self) -> 'Referent':
        return self.referent
    
    def get_referents(self) -> typing.List['Referent']:
        res = list()
        if (self.referent is not None): 
            res.append(self.referent)
        ri = super().get_referents()
        if (ri is not None): 
            res.extend(ri)
        return res
    
    def save_to_local_ontology(self) -> None:
        if (self.data is None): 
            return
        r = self.data.register_referent(self.referent)
        self.data = (None)
        if (r is not None): 
            self.referent = r
            anno = TextAnnotation()
            anno.sofa = self.kit.sofa
            anno.occurence_of = self.referent
            anno.begin_char = self.begin_char
            anno.end_char = self.end_char
            self.referent.add_occurence(anno)
    
    def set_default_local_onto(self, proc : 'Processor') -> None:
        if (self.referent is None or self.kit is None or proc is None): 
            return
        for a in proc.analyzers: 
            if (a.create_referent(self.referent.type_name) is not None): 
                self.data = self.kit.get_analyzer_data(a)
                break
    
    def _replace_referent(self, old_referent : 'Referent', new_referent : 'Referent') -> None:
        if (self.referent == old_referent): 
            self.referent = new_referent
        if (self.end_token is None): 
            return
        t = self.begin_token
        while t is not None: 
            if (t.end_char > self.end_char): 
                break
            if (isinstance(t, ReferentToken)): 
                t._replace_referent(old_referent, new_referent)
            if (t == self.end_token): 
                break
            t = t.next0_
    
    def _serialize(self, stream : io.IOBase) -> None:
        super()._serialize(stream)
        id0_ = 0
        if (self.referent is not None and (isinstance(self.referent.tag, int))): 
            id0_ = (self.referent.tag)
        SerializerHelper.serialize_int(stream, id0_)
    
    def _deserialize(self, stream : io.IOBase, kit_ : 'AnalysisKit', vers : int) -> None:
        super()._deserialize(stream, kit_, vers)
        id0_ = SerializerHelper.deserialize_int(stream)
        if (id0_ > 0): 
            self.referent = kit_.entities[id0_ - 1]
    
    @staticmethod
    def _new97(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AnalyzerData') -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.data = _arg4
        return res
    
    @staticmethod
    def _new734(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'MorphCollection') -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new736(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : object) -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.tag = _arg4
        return res
    
    @staticmethod
    def _new1270(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'MorphCollection', _arg5 : 'AnalyzerData') -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.morph = _arg4
        res.data = _arg5
        return res
    
    @staticmethod
    def _new2480(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'MorphCollection', _arg5 : int) -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.morph = _arg4
        res.misc_attrs = _arg5
        return res
    
    @staticmethod
    def _new2581(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : int) -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.misc_attrs = _arg4
        return res
    
    @staticmethod
    def _new2591(_arg1 : 'Referent', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'MorphCollection', _arg5 : object) -> 'ReferentToken':
        res = ReferentToken(_arg1, _arg2, _arg3)
        res.morph = _arg4
        res.tag = _arg5
        return res