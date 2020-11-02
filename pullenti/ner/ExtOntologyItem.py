# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
from pullenti.ner.ProcessorService import ProcessorService

class ExtOntologyItem:
    """ Элемент внешней онтологии """
    
    def __init__(self, caption : str=None) -> None:
        self.ext_id = None;
        self.type_name = None;
        self.referent = None;
        self._refs = None
        self.__m_caption = None;
        self.__m_caption = caption
    
    def __str__(self) -> str:
        if (self.__m_caption is not None): 
            return self.__m_caption
        elif (self.referent is None): 
            return "{0}: ?".format(Utils.ifNotNull(self.type_name, "?"))
        else: 
            res = str(self.referent)
            if (self.referent.parent_referent is not None): 
                str1 = str(self.referent.parent_referent)
                if (not str1 in res): 
                    res = (res + "; " + str1)
            return res
    
    def _serialize(self, stream : io.IOBase) -> None:
        SerializerHelper.serialize_string(stream, (None if self.ext_id is None else str(self.ext_id)))
        SerializerHelper.serialize_string(stream, self.__m_caption)
        if (self._refs is None): 
            SerializerHelper.serialize_int(stream, 0)
        else: 
            SerializerHelper.serialize_int(stream, len(self._refs))
            id0_ = 1
            for r in self._refs: 
                r.tag = id0_
                id0_ += 1
            for r in self._refs: 
                r.occurrence.clear()
                SerializerHelper.serialize_string(stream, r.type_name)
                r.serialize(stream)
        self.referent.occurrence.clear()
        SerializerHelper.serialize_string(stream, self.type_name)
        self.referent.serialize(stream)
    
    def _deserialize(self, stream : io.IOBase) -> None:
        self.ext_id = (SerializerHelper.deserialize_string(stream))
        self.__m_caption = SerializerHelper.deserialize_string(stream)
        cou = SerializerHelper.deserialize_int(stream)
        if (cou > 0): 
            self._refs = list()
            while cou > 0: 
                typ = SerializerHelper.deserialize_string(stream)
                r = ProcessorService.create_referent(typ)
                r.deserialize(stream, self._refs, None)
                self._refs.append(r)
                cou -= 1
        self.type_name = SerializerHelper.deserialize_string(stream)
        self.referent = ProcessorService.create_referent(self.type_name)
        self.referent.deserialize(stream, self._refs, None)
    
    @staticmethod
    def _new2803(_arg1 : object, _arg2 : 'Referent', _arg3 : str) -> 'ExtOntologyItem':
        res = ExtOntologyItem()
        res.ext_id = _arg1
        res.referent = _arg2
        res.type_name = _arg3
        return res