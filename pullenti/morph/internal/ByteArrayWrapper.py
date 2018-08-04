# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 


class ByteArrayWrapper:
    """ Сделан специально для Питона - а то стандартым способом через MemoryStream
     жутко тормозит, придётся делать самим """
    
    def __init__(self, arr : bytearray) -> None:
        self.__m_array = None
        self.__m_pos = 0
        self.__m_len = 0
        self.__m_array = arr
        self.__m_pos = 0
        self.__m_len = len(self.__m_array)
    
    @property
    def iseof(self) -> bool:
        return self.__m_pos >= self.__m_len
    
    def back(self) -> None:
        self.__m_pos -= 1
    
    def seek(self, pos : int) -> None:
        self.__m_pos = pos
    
    @property
    def position(self) -> int:
        return self.__m_pos
    
    def deserialize_byte(self) -> int:
        if (self.__m_pos >= self.__m_len): 
            return 0
        retVal2664 = self.__m_array[self.__m_pos]
        self.__m_pos += 1
        return retVal2664
    
    def deserialize_short(self) -> int:
        if ((self.__m_pos + 1) >= self.__m_len): 
            return 0
        b0 = self.__m_array[self.__m_pos]
        self.__m_pos += 1
        b1 = self.__m_array[self.__m_pos]
        self.__m_pos += 1
        res = b1
        res <<= 8
        return (res | b0)
    
    def deserialize_int(self) -> int:
        if ((self.__m_pos + 1) >= self.__m_len): 
            return 0
        b0 = self.__m_array[self.__m_pos]
        self.__m_pos += 1
        b1 = self.__m_array[self.__m_pos]
        self.__m_pos += 1
        b2 = self.__m_array[self.__m_pos]
        self.__m_pos += 1
        b3 = self.__m_array[self.__m_pos]
        self.__m_pos += 1
        res = b3
        res <<= 8
        res |= b2
        res <<= 8
        res |= b1
        res <<= 8
        return (res | b0)
    
    def deserialize_string(self) -> str:
        if (self.__m_pos >= self.__m_len): 
            return None
        len0_ = self.__m_array[self.__m_pos]
        self.__m_pos += 1
        if (len0_ == 0xFF): 
            return None
        if (len0_ == 0): 
            return ""
        if ((self.__m_pos + len0_) > self.__m_len): 
            return None
        res = self.__m_array[self.__m_pos:self.__m_pos+len0_].decode('utf-8', 'ignore')
        self.__m_pos += len0_
        return res