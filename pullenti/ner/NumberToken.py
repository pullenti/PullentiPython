# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import math
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.morph.MorphGender import MorphGender

class NumberToken(MetaToken):
    """ Числовой токен (числительное) """
    
    def __init__(self, begin : 'Token', end : 'Token', val : str, typ_ : 'NumberSpellingType', kit_ : 'AnalysisKit'=None) -> None:
        super().__init__(begin, end, kit_)
        self.__m_value = None;
        self.__m_int_val = None
        self.__m_real_val = 0
        self.typ = NumberSpellingType.DIGIT
        self.value = val
        self.typ = typ_
    
    @property
    def value(self) -> str:
        """ Числовое значение (если действительное, то с точкой - разделителем дробных). """
        return self.__m_value
    @value.setter
    def value(self, value_) -> str:
        from pullenti.ner.core.NumberHelper import NumberHelper
        self.__m_value = (Utils.ifNotNull(value_, ""))
        if (len(self.__m_value) > 2 and self.__m_value.endswith(".0")): 
            self.__m_value = self.__m_value[0:0+len(self.__m_value) - 2]
        while len(self.__m_value) > 1 and self.__m_value[0] == '0' and self.__m_value[1] != '.':
            self.__m_value = self.__m_value[1:]
        wrapn2798 = RefOutArgWrapper(0)
        inoutres2799 = Utils.tryParseInt(self.__m_value, wrapn2798)
        n = wrapn2798.value
        if (inoutres2799): 
            self.__m_int_val = n
        else: 
            self.__m_int_val = (None)
        d = NumberHelper.string_to_double(self.__m_value)
        if (d is None): 
            self.__m_real_val = math.nan
        else: 
            self.__m_real_val = d
        return value_
    
    @property
    def int_value(self) -> int:
        """ Целочисленное 32-х битное значение.
         Число может быть большое и не умещаться в Int, тогда вернёт null.
         Если есть дробная часть, то тоже вернёт null.
         Long не используется, так как не поддерживается в Javascript """
        return self.__m_int_val
    @int_value.setter
    def int_value(self, value_) -> int:
        self.value = str(value_)
        return value_
    
    @property
    def real_value(self) -> float:
        """ Получить действительное значение из Value. Если не удалось, то NaN. """
        return self.__m_real_val
    @real_value.setter
    def real_value(self, value_) -> float:
        from pullenti.ner.core.NumberHelper import NumberHelper
        self.value = NumberHelper.double_to_string(value_)
        return value_
    
    @property
    def is_number(self) -> bool:
        return True
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0} {1}".format(self.value, Utils.enumToString(self.typ)), end="", file=res, flush=True)
        if (self.morph is not None): 
            print(" {0}".format(str(self.morph)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def get_normal_case_text(self, mc : 'MorphClass'=None, single_number : bool=False, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        return str(self.value)
    
    def _serialize(self, stream : io.IOBase) -> None:
        from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
        super()._serialize(stream)
        SerializerHelper.serialize_string(stream, self.__m_value)
        SerializerHelper.serialize_int(stream, self.typ)
    
    def _deserialize(self, stream : io.IOBase, kit_ : 'AnalysisKit', vers : int) -> None:
        from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
        super()._deserialize(stream, kit_, vers)
        if (vers == 0): 
            buf = Utils.newArrayOfBytes(8, 0)
            Utils.readIO(stream, buf, 0, 8)
            lo = int.from_bytes(buf[0:0+8], byteorder="little")
            self.value = str(lo)
        else: 
            self.value = SerializerHelper.deserialize_string(stream)
        self.typ = (Utils.valToEnum(SerializerHelper.deserialize_int(stream), NumberSpellingType))
    
    @staticmethod
    def _new568(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'MorphCollection') -> 'NumberToken':
        res = NumberToken(_arg1, _arg2, _arg3, _arg4)
        res.morph = _arg5
        return res