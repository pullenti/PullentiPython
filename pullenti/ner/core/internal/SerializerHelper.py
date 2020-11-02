# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Token import Token
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.TextToken import TextToken

class SerializerHelper:
    
    @staticmethod
    def serialize_int(stream : io.IOBase, val : int) -> None:
        Utils.writeIO(stream, (val).to_bytes(4, byteorder="little"), 0, 4)
    
    @staticmethod
    def deserialize_int(stream : io.IOBase) -> int:
        buf = Utils.newArrayOfBytes(4, 0)
        Utils.readIO(stream, buf, 0, 4)
        return int.from_bytes(buf[0:0+2], byteorder="little")
    
    @staticmethod
    def serialize_short(stream : io.IOBase, val : int) -> None:
        Utils.writeIO(stream, (val).to_bytes(2, byteorder="little"), 0, 2)
    
    @staticmethod
    def deserialize_short(stream : io.IOBase) -> int:
        buf = Utils.newArrayOfBytes(2, 0)
        Utils.readIO(stream, buf, 0, 2)
        return int.from_bytes(buf[0:0+2], byteorder="little")
    
    @staticmethod
    def serialize_string(stream : io.IOBase, val : str) -> None:
        if (val is None): 
            SerializerHelper.serialize_int(stream, -1)
            return
        if (Utils.isNullOrEmpty(val)): 
            SerializerHelper.serialize_int(stream, 0)
            return
        data = val.encode("UTF-8", 'ignore')
        SerializerHelper.serialize_int(stream, len(data))
        Utils.writeIO(stream, data, 0, len(data))
    
    @staticmethod
    def deserialize_string(stream : io.IOBase) -> str:
        len0_ = SerializerHelper.deserialize_int(stream)
        if (len0_ < 0): 
            return None
        if (len0_ == 0): 
            return ""
        data = Utils.newArrayOfBytes(len0_, 0)
        Utils.readIO(stream, data, 0, len(data))
        return data.decode("UTF-8", 'ignore')
    
    @staticmethod
    def serialize_tokens(stream : io.IOBase, t : 'Token', max_char : int) -> None:
        cou = 0
        tt = t
        while tt is not None: 
            if (max_char > 0 and tt.end_char > max_char): 
                break
            cou += 1
            tt = tt.next0_
        SerializerHelper.serialize_int(stream, cou)
        while cou > 0: 
            SerializerHelper.serialize_token(stream, t)
            cou -= 1; t = t.next0_
    
    @staticmethod
    def deserialize_tokens(stream : io.IOBase, kit : 'AnalysisKit', vers : int) -> 'Token':
        from pullenti.ner.MetaToken import MetaToken
        cou = SerializerHelper.deserialize_int(stream)
        if (cou == 0): 
            return None
        res = None
        prev = None
        first_pass3533 = True
        while True:
            if first_pass3533: first_pass3533 = False
            else: cou -= 1
            if (not (cou > 0)): break
            t = SerializerHelper.__deserialize_token(stream, kit, vers)
            if (t is None): 
                continue
            if (res is None): 
                res = t
            if (prev is not None): 
                t.previous = prev
            prev = t
        t = res
        while t is not None: 
            if (isinstance(t, MetaToken)): 
                SerializerHelper.__corr_prev_next(Utils.asObjectOrNull(t, MetaToken), t.previous, t.next0_)
            t = t.next0_
        return res
    
    @staticmethod
    def __corr_prev_next(mt : 'MetaToken', prev : 'Token', next0_ : 'Token') -> None:
        from pullenti.ner.MetaToken import MetaToken
        mt.begin_token._m_previous = prev
        mt.end_token._m_next = next0_
        t = mt.begin_token
        while t is not None and t.end_char <= mt.end_char: 
            if (isinstance(t, MetaToken)): 
                SerializerHelper.__corr_prev_next(Utils.asObjectOrNull(t, MetaToken), t.previous, t.next0_)
            t = t.next0_
    
    @staticmethod
    def serialize_token(stream : io.IOBase, t : 'Token') -> None:
        from pullenti.ner.MetaToken import MetaToken
        from pullenti.ner.ReferentToken import ReferentToken
        typ = 0
        if (isinstance(t, TextToken)): 
            typ = (1)
        elif (isinstance(t, NumberToken)): 
            typ = (2)
        elif (isinstance(t, ReferentToken)): 
            typ = (3)
        elif (isinstance(t, MetaToken)): 
            typ = (4)
        SerializerHelper.serialize_short(stream, typ)
        if (typ == (0)): 
            return
        t._serialize(stream)
        if (isinstance(t, MetaToken)): 
            SerializerHelper.serialize_tokens(stream, t.begin_token, t.end_char)
    
    @staticmethod
    def __deserialize_token(stream : io.IOBase, kit : 'AnalysisKit', vers : int) -> 'Token':
        from pullenti.ner.MetaToken import MetaToken
        from pullenti.ner.ReferentToken import ReferentToken
        typ = SerializerHelper.deserialize_short(stream)
        if (typ == (0)): 
            return None
        t = None
        if (typ == (1)): 
            t = (TextToken(None, kit))
        elif (typ == (2)): 
            t = (NumberToken(None, None, None, NumberSpellingType.DIGIT, kit))
        elif (typ == (3)): 
            t = (ReferentToken(None, None, None, kit))
        else: 
            t = (MetaToken(None, None, kit))
        t._deserialize(stream, kit, vers)
        if (isinstance(t, MetaToken)): 
            tt = SerializerHelper.deserialize_tokens(stream, kit, vers)
            if (tt is not None): 
                t._m_begin_token = tt
                while tt is not None: 
                    t._m_end_token = tt
                    tt = tt.next0_
        return t