# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import math
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.internal.SerializerHelper import SerializerHelper

class SourceOfAnalysis:
    """ Анализируемый текст, точнее, обёртка над ним
    
    Источник анализа
    """
    
    @property
    def text(self) -> str:
        """ Исходный плоский текст """
        return self.__text
    @text.setter
    def text(self, value) -> str:
        self.__text = value
        return self.__text
    
    @property
    def tag(self) -> object:
        """ Используется произвольным образом """
        return self.__tag
    @tag.setter
    def tag(self, value) -> object:
        self.__tag = value
        return self.__tag
    
    def __init__(self, txt : str) -> None:
        """ Создать контейнер на основе плоского текста.
        При создании будут автоматически сделаны транслитеральные замены, если они будут найдены.
        
        Args:
            txt(str): Анализируемый текст
        """
        self.__text = None;
        self.__tag = None;
        self.clear_dust = False
        self.crlf_corrected_count = 0
        self.do_word_correction_by_morph = False
        self.do_words_merging_by_morph = True
        self.create_number_tokens = True
        self.correction_dict = None
        self.__m_total_transliteral_substitutions = 0
        if (Utils.isNullOrEmpty(txt)): 
            self.text = ""
            return
        self.text = txt
    
    def __do_cr_lf_correction(self, txt : str) -> str:
        # Это анализ случаев принудительно отформатированного текста
        cou = 0
        total_len = 0
        i = 0
        first_pass3928 = True
        while True:
            if first_pass3928: first_pass3928 = False
            else: i += 1
            if (not (i < len(txt))): break
            ch = txt[i]
            if ((ord(ch)) != 0xD and (ord(ch)) != 0xA): 
                continue
            len0_ = 0
            last_char = ch
            j = (i + 1)
            while j < len(txt): 
                ch = txt[j]
                if ((ord(ch)) == 0xD or (ord(ch)) == 0xA): 
                    break
                elif ((ord(ch)) == 0x9): 
                    len0_ += 5
                else: 
                    last_char = ch
                    len0_ += 1
                j += 1
            if (j >= len(txt)): 
                break
            if (len0_ < 30): 
                continue
            if (last_char != '.' and last_char != ':' and last_char != ';'): 
                next_is_dig = False
                k = j + 1
                while k < len(txt): 
                    if (not Utils.isWhitespace(txt[k])): 
                        if (str.isdigit(txt[k])): 
                            next_is_dig = True
                        break
                    k += 1
                if (not next_is_dig): 
                    cou += 1
                    total_len += len0_
            i = j
        if (cou < 4): 
            return txt
        total_len = math.floor(total_len / cou)
        if ((total_len < 50) or total_len > 100): 
            return txt
        tmp = Utils.newStringIO(txt)
        i = 0
        while i < tmp.tell(): 
            ch = Utils.getCharAtStringIO(tmp, i)
            len0_ = 0
            last_char = ch
            j = (i + 1)
            while j < tmp.tell(): 
                ch = Utils.getCharAtStringIO(tmp, j)
                if ((ord(ch)) == 0xD or (ord(ch)) == 0xA): 
                    break
                elif ((ord(ch)) == 0x9): 
                    len0_ += 5
                else: 
                    last_char = ch
                    len0_ += 1
                j += 1
            if (j >= tmp.tell()): 
                break
            for jj in range(j - 1, -1, -1):
                last_char = Utils.getCharAtStringIO(tmp, jj)
                if (not Utils.isWhitespace(last_char)): 
                    break
            else: jj = -1
            not_single = False
            jj = (j + 1)
            if ((jj < tmp.tell()) and (ord(Utils.getCharAtStringIO(tmp, j))) == 0xD and (ord(Utils.getCharAtStringIO(tmp, jj))) == 0xA): 
                jj += 1
            while jj < tmp.tell(): 
                ch = Utils.getCharAtStringIO(tmp, jj)
                if (not Utils.isWhitespace(ch)): 
                    break
                if ((ord(ch)) == 0xD or (ord(ch)) == 0xA): 
                    not_single = True
                    break
                jj += 1
            if (((not not_single and len0_ > (total_len - 20) and (len0_ < (total_len + 10))) and last_char != '.' and last_char != ':') and last_char != ';'): 
                Utils.setCharAtStringIO(tmp, j, ' ')
                self.crlf_corrected_count += 1
                if ((j + 1) < tmp.tell()): 
                    ch = Utils.getCharAtStringIO(tmp, j + 1)
                    if ((ord(ch)) == 0xA): 
                        Utils.setCharAtStringIO(tmp, j + 1, ' ')
                        j += 1
            i = (j - 1)
            i += 1
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def __do_transliteral_correction(txt : io.StringIO, info : io.StringIO) -> int:
        # Произвести транслитеральную коррекцию
        stat = 0
        pref_rus_word = False
        i = 0
        while i < txt.tell(): 
            if (str.isalpha(Utils.getCharAtStringIO(txt, i))): 
                rus = 0
                pure_lat = 0
                unknown = 0
                j = i
                while j < txt.tell(): 
                    ch = Utils.getCharAtStringIO(txt, j)
                    if (not str.isalpha(ch)): 
                        break
                    code = ord(ch)
                    if (code >= 0x400 and (code < 0x500)): 
                        rus += 1
                    elif (SourceOfAnalysis.__m_lat_chars.find(ch) >= 0): 
                        unknown += 1
                    else: 
                        pure_lat += 1
                    j += 1
                if (((unknown > 0 and rus > 0)) or ((unknown > 0 and pure_lat == 0 and pref_rus_word))): 
                    if (info is not None): 
                        if (info.tell() > 0): 
                            print("\r\n", end="", file=info)
                        k = i
                        while k < j: 
                            print(Utils.getCharAtStringIO(txt, k), end="", file=info)
                            k += 1
                        print(": ", end="", file=info)
                    k = i
                    while k < j: 
                        ii = SourceOfAnalysis.__m_lat_chars.find(Utils.getCharAtStringIO(txt, k))
                        if (ii >= 0): 
                            if (info is not None): 
                                print("{0}->{1} ".format(Utils.getCharAtStringIO(txt, k), SourceOfAnalysis.__m_rus_chars[ii]), end="", file=info, flush=True)
                            Utils.setCharAtStringIO(txt, k, SourceOfAnalysis.__m_rus_chars[ii])
                        k += 1
                    stat += unknown
                    pref_rus_word = True
                else: 
                    pref_rus_word = rus > 0
                i = j
            i += 1
        return stat
    
    __m_lat_chars = "ABEKMHOPCTYXaekmopctyx"
    
    __m_rus_chars = "АВЕКМНОРСТУХаекморстух"
    
    @staticmethod
    def __calc_transliteral_statistics(txt : str, info : io.StringIO) -> int:
        if (txt is None): 
            return 0
        tmp = Utils.newStringIO(txt)
        return SourceOfAnalysis.__do_transliteral_correction(tmp, info)
    
    @property
    def __total_transliteral_substitutions(self) -> int:
        return self.__m_total_transliteral_substitutions
    
    def substring(self, position : int, length : int) -> str:
        """ Извлечь фрагмент из исходного текста. Переходы на новую строку заменяются пробелами.
        
        Args:
            position(int): начальная позиция
            length(int): длина
        
        Returns:
            str: фрагмент
        """
        if (length < 0): 
            length = (len(self.text) - position)
        if ((position + length) <= len(self.text) and length > 0): 
            res = self.text[position:position+length]
            if (res.find("\r\n") >= 0): 
                res = res.replace("\r\n", " ")
            if (res.find('\n') >= 0): 
                res = res.replace("\n", " ")
            return res
        return "Position + Length > Text.Length"
    
    def calc_whitespace_distance_between_positions(self, pos_from : int, pos_to : int) -> int:
        # Вычислить расстояние в символах между соседними элементами
        if (pos_from == (pos_to + 1)): 
            return 0
        if (pos_from > pos_to or (pos_from < 0) or pos_to >= len(self.text)): 
            return -1
        res = 0
        i = pos_from
        while i <= pos_to: 
            ch = self.text[i]
            if (not Utils.isWhitespace(ch)): 
                return -1
            if (ch == '\r' or ch == '\n'): 
                res += 10
            elif (ch == '\t'): 
                res += 5
            else: 
                res += 1
            i += 1
        return res
    
    def serialize(self, stream : io.IOBase) -> None:
        SerializerHelper.serialize_string(stream, self.text)
    
    def deserialize(self, stream : io.IOBase) -> None:
        self.text = SerializerHelper.deserialize_string(stream)
    
    @staticmethod
    def _new494(_arg1 : str, _arg2 : bool) -> 'SourceOfAnalysis':
        res = SourceOfAnalysis(_arg1)
        res.create_number_tokens = _arg2
        return res