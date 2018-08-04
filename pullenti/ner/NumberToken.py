# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.ntopy.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.internal.SerializerHelper import SerializerHelper


class NumberToken(MetaToken):
    """ Числовой токен (числительное) """
    
    def __init__(self, begin : 'Token', end : 'Token', val : int, typ_ : 'NumberSpellingType', kit_ : 'AnalysisKit'=None) -> None:
        self.value = 0
        self.typ = NumberSpellingType.DIGIT
        super().__init__(begin, end, kit_)
        self.value = val
        self.typ = typ_
    
    @property
    def is_number(self) -> bool:
        return True
    
    def __str__(self) -> str:
        res = Utils.newStringIO(None)
        print("{0} {1}".format(self.value, Utils.enumToString(self.typ)), end="", file=res, flush=True)
        if (self.morph is not None): 
            print(" {0}".format(str(self.morph)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def get_normal_case_text(self, mc : 'MorphClass'=MorphClass(), single_number : bool=False, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        return str(self.value)
    
    def _serialize(self, stream : io.IOBase) -> None:
        super()._serialize(stream)
        Utils.writeIO(stream, (self.value).to_bytes(8, byteorder="little"), 0, 8)
        SerializerHelper.serialize_int(stream, self.typ)
    
    def _deserialize(self, stream : io.IOBase, kit_ : 'AnalysisKit') -> None:
        super()._deserialize(stream, kit_)
        buf = Utils.newArrayOfBytes(8, 0)
        Utils.readIO(stream, buf, 0, 8)
        self.value = int.from_bytes(buf[0:0+8], byteorder="little")
        self.typ = Utils.valToEnum(SerializerHelper.deserialize_int(stream), NumberSpellingType)

    
    @staticmethod
    def _new585(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'MorphCollection') -> 'NumberToken':
        res = NumberToken(_arg1, _arg2, _arg3, _arg4)
        res.morph = _arg5
        return res