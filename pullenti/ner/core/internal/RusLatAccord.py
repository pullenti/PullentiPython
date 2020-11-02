# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.LanguageHelper import LanguageHelper

class RusLatAccord:
    
    def __init__(self, ru : str, la : str, brus : bool=True, blat : bool=True) -> None:
        self.rus = None;
        self.lat = None;
        self.rus_to_lat = False
        self.lat_to_rus = False
        self.on_tail = False
        self.rus = ru.upper()
        self.lat = la.upper()
        self.rus_to_lat = brus
        self.lat_to_rus = blat
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print("'{0}'".format(self.rus), end="", file=tmp, flush=True)
        if (self.rus_to_lat and self.lat_to_rus): 
            print(" <-> ", end="", file=tmp)
        elif (self.rus_to_lat): 
            print(" -> ", end="", file=tmp)
        elif (self.lat_to_rus): 
            print(" <- ", end="", file=tmp)
        print("'{0}'".format(self.lat), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    __m_accords = None
    
    @staticmethod
    def __get_accords() -> typing.List['RusLatAccord']:
        if (RusLatAccord.__m_accords is not None): 
            return RusLatAccord.__m_accords
        RusLatAccord.__m_accords = list()
        RusLatAccord.__m_accords.append(RusLatAccord("а", "a"))
        RusLatAccord.__m_accords.append(RusLatAccord("а", "aa"))
        RusLatAccord.__m_accords.append(RusLatAccord("б", "b"))
        RusLatAccord.__m_accords.append(RusLatAccord("в", "v"))
        RusLatAccord.__m_accords.append(RusLatAccord("в", "w"))
        RusLatAccord.__m_accords.append(RusLatAccord("г", "g"))
        RusLatAccord.__m_accords.append(RusLatAccord("д", "d"))
        RusLatAccord.__m_accords.append(RusLatAccord("е", "e"))
        RusLatAccord.__m_accords.append(RusLatAccord("е", "yo"))
        RusLatAccord.__m_accords.append(RusLatAccord("е", "io"))
        RusLatAccord.__m_accords.append(RusLatAccord("е", "jo"))
        RusLatAccord.__m_accords.append(RusLatAccord("ж", "j"))
        RusLatAccord.__m_accords.append(RusLatAccord("дж", "j"))
        RusLatAccord.__m_accords.append(RusLatAccord("з", "z"))
        RusLatAccord.__m_accords.append(RusLatAccord("и", "e"))
        RusLatAccord.__m_accords.append(RusLatAccord("и", "i"))
        RusLatAccord.__m_accords.append(RusLatAccord("и", "y"))
        RusLatAccord.__m_accords.append(RusLatAccord("и", "ea"))
        RusLatAccord.__m_accords.append(RusLatAccord("й", "i"))
        RusLatAccord.__m_accords.append(RusLatAccord("й", "y"))
        RusLatAccord.__m_accords.append(RusLatAccord("к", "c"))
        RusLatAccord.__m_accords.append(RusLatAccord("к", "k"))
        RusLatAccord.__m_accords.append(RusLatAccord("к", "ck"))
        RusLatAccord.__m_accords.append(RusLatAccord("кс", "x"))
        RusLatAccord.__m_accords.append(RusLatAccord("л", "l"))
        RusLatAccord.__m_accords.append(RusLatAccord("м", "m"))
        RusLatAccord.__m_accords.append(RusLatAccord("н", "n"))
        RusLatAccord.__m_accords.append(RusLatAccord("о", "a"))
        RusLatAccord.__m_accords.append(RusLatAccord("о", "o"))
        RusLatAccord.__m_accords.append(RusLatAccord("о", "ow"))
        RusLatAccord.__m_accords.append(RusLatAccord("о", "oh"))
        RusLatAccord.__m_accords.append(RusLatAccord("п", "p"))
        RusLatAccord.__m_accords.append(RusLatAccord("р", "r"))
        RusLatAccord.__m_accords.append(RusLatAccord("с", "s"))
        RusLatAccord.__m_accords.append(RusLatAccord("с", "c"))
        RusLatAccord.__m_accords.append(RusLatAccord("т", "t"))
        RusLatAccord.__m_accords.append(RusLatAccord("у", "u"))
        RusLatAccord.__m_accords.append(RusLatAccord("у", "w"))
        RusLatAccord.__m_accords.append(RusLatAccord("ф", "f"))
        RusLatAccord.__m_accords.append(RusLatAccord("ф", "ph"))
        RusLatAccord.__m_accords.append(RusLatAccord("х", "h"))
        RusLatAccord.__m_accords.append(RusLatAccord("х", "kh"))
        RusLatAccord.__m_accords.append(RusLatAccord("ц", "ts"))
        RusLatAccord.__m_accords.append(RusLatAccord("ц", "c"))
        RusLatAccord.__m_accords.append(RusLatAccord("ч", "ch"))
        RusLatAccord.__m_accords.append(RusLatAccord("ш", "sh"))
        RusLatAccord.__m_accords.append(RusLatAccord("щ", "shch"))
        RusLatAccord.__m_accords.append(RusLatAccord("ы", "i"))
        RusLatAccord.__m_accords.append(RusLatAccord("э", "e"))
        RusLatAccord.__m_accords.append(RusLatAccord("э", "a"))
        RusLatAccord.__m_accords.append(RusLatAccord("ю", "iu"))
        RusLatAccord.__m_accords.append(RusLatAccord("ю", "ju"))
        RusLatAccord.__m_accords.append(RusLatAccord("ю", "yu"))
        RusLatAccord.__m_accords.append(RusLatAccord("ю", "ew"))
        RusLatAccord.__m_accords.append(RusLatAccord("я", "ia"))
        RusLatAccord.__m_accords.append(RusLatAccord("я", "ja"))
        RusLatAccord.__m_accords.append(RusLatAccord("я", "ya"))
        RusLatAccord.__m_accords.append(RusLatAccord("ъ", ""))
        RusLatAccord.__m_accords.append(RusLatAccord("ь", ""))
        RusLatAccord.__m_accords.append(RusLatAccord("", "gh"))
        RusLatAccord.__m_accords.append(RusLatAccord("", "h"))
        RusLatAccord.__m_accords.append(RusLatAccord._new465("", "e", True))
        RusLatAccord.__m_accords.append(RusLatAccord("еи", "ei"))
        RusLatAccord.__m_accords.append(RusLatAccord("аи", "ai"))
        RusLatAccord.__m_accords.append(RusLatAccord("ай", "i"))
        RusLatAccord.__m_accords.append(RusLatAccord("уи", "ui"))
        RusLatAccord.__m_accords.append(RusLatAccord("уи", "w"))
        RusLatAccord.__m_accords.append(RusLatAccord("ои", "oi"))
        RusLatAccord.__m_accords.append(RusLatAccord("ей", "ei"))
        RusLatAccord.__m_accords.append(RusLatAccord("ей", "ey"))
        RusLatAccord.__m_accords.append(RusLatAccord("ай", "ai"))
        RusLatAccord.__m_accords.append(RusLatAccord("ай", "ay"))
        RusLatAccord.__m_accords.append(RusLatAccord(" ", " "))
        RusLatAccord.__m_accords.append(RusLatAccord("-", "-"))
        return RusLatAccord.__m_accords
    
    @staticmethod
    def __is_pref(str0_ : str, i : int, pref : str) -> bool:
        if ((len(pref) + i) > len(str0_)): 
            return False
        j = 0
        while j < len(pref): 
            if (pref[j] != str0_[i + j]): 
                return False
            j += 1
        return True
    
    @staticmethod
    def __get_vars_pref(rus_ : str, ri : int, lat_ : str, li : int) -> typing.List['RusLatAccord']:
        res = None
        for a in RusLatAccord.__get_accords(): 
            if (RusLatAccord.__is_pref(rus_, ri, a.rus) and RusLatAccord.__is_pref(lat_, li, a.lat) and a.rus_to_lat): 
                if (a.on_tail): 
                    if ((ri + len(a.rus)) < len(rus_)): 
                        continue
                    if ((li + len(a.lat)) < len(lat_)): 
                        continue
                if (res is None): 
                    res = list()
                res.append(a)
        return res
    
    @staticmethod
    def get_variants(rus_or_lat : str) -> typing.List[str]:
        """ Сформировать всевозможные варианты написаний на другой раскладке
        
        Args:
            rus_or_lat(str): слово на кириллице или латинице
        
        """
        res = list()
        if (Utils.isNullOrEmpty(rus_or_lat)): 
            return res
        rus_or_lat = rus_or_lat.upper()
        is_rus = LanguageHelper.is_cyrillic_char(rus_or_lat[0])
        stack = list()
        i = 0
        while i < len(rus_or_lat): 
            li = list()
            maxlen = 0
            for a in RusLatAccord.__get_accords(): 
                pref = None
                if (is_rus and len(a.rus) > 0): 
                    pref = a.rus
                elif (not is_rus and len(a.lat) > 0): 
                    pref = a.lat
                else: 
                    continue
                if (len(pref) < maxlen): 
                    continue
                if (not RusLatAccord.__is_pref(rus_or_lat, i, pref)): 
                    continue
                if (a.on_tail): 
                    if ((len(pref) + i) < len(rus_or_lat)): 
                        continue
                if (len(pref) > maxlen): 
                    maxlen = len(pref)
                    li.clear()
                li.append(a)
            if (len(li) == 0 or maxlen == 0): 
                return res
            stack.append(li)
            i += (maxlen - 1)
            i += 1
        if (len(stack) == 0): 
            return res
        ind = list()
        i = 0
        while i < len(stack): 
            ind.append(0)
            i += 1
        tmp = io.StringIO()
        while True:
            Utils.setLengthStringIO(tmp, 0)
            i = 0
            while i < len(ind): 
                a = stack[i][ind[i]]
                print((a.lat if is_rus else a.rus), end="", file=tmp)
                i += 1
            ok = True
            if (not is_rus): 
                i = 0
                while i < tmp.tell(): 
                    if (Utils.getCharAtStringIO(tmp, i) == 'Й'): 
                        if (i == 0): 
                            ok = False
                            break
                        if (not LanguageHelper.is_cyrillic_vowel(Utils.getCharAtStringIO(tmp, i - 1))): 
                            ok = False
                            break
                    i += 1
            if (ok): 
                res.append(Utils.toStringStringIO(tmp))
            for i in range(len(ind) - 1, -1, -1):
                ind[i] += 1
                if (ind[i] < len(stack[i])): 
                    break
                else: 
                    ind[i] = 0
            else: i = -1
            if (i < 0): 
                break
        return res
    
    @staticmethod
    def can_be_equals(rus_ : str, lat_ : str) -> bool:
        if (Utils.isNullOrEmpty(rus_) or Utils.isNullOrEmpty(lat_)): 
            return False
        rus_ = rus_.upper()
        lat_ = lat_.upper()
        vs = RusLatAccord.__get_vars_pref(rus_, 0, lat_, 0)
        if (vs is None): 
            return False
        stack = list()
        stack.append(vs)
        while len(stack) > 0:
            if (len(stack) == 0): 
                break
            ri = 0
            li = 0
            for s in stack: 
                ri += len(s[0].rus)
                li += len(s[0].lat)
            if (ri >= len(rus_) and li >= len(lat_)): 
                return True
            vs = RusLatAccord.__get_vars_pref(rus_, ri, lat_, li)
            if (vs is not None): 
                stack.insert(0, vs)
                continue
            while len(stack) > 0:
                del stack[0][0]
                if (len(stack[0]) > 0): 
                    break
                del stack[0]
        return False
    
    @staticmethod
    def find_accords_rus_to_lat(txt : str, pos : int, res : typing.List[str]) -> int:
        """ Вернёт длину привязки
        
        Args:
            txt(str): 
            pos(int): 
            res(typing.List[str]): 
        
        """
        if (pos >= len(txt)): 
            return 0
        ch0 = txt[pos]
        ok = False
        if ((pos + 1) < len(txt)): 
            ch1 = txt[pos + 1]
            for a in RusLatAccord.__get_accords(): 
                if ((a.rus_to_lat and len(a.rus) == 2 and a.rus[0] == ch0) and a.rus[1] == ch1): 
                    res.append(a.lat)
                    ok = True
            if (ok): 
                return 2
        for a in RusLatAccord.__get_accords(): 
            if (a.rus_to_lat and len(a.rus) == 1 and a.rus[0] == ch0): 
                res.append(a.lat)
                ok = True
        if (ok): 
            return 1
        return 0
    
    @staticmethod
    def find_accords_lat_to_rus(txt : str, pos : int, res : typing.List[str]) -> int:
        if (pos >= len(txt)): 
            return 0
        max_len = 0
        for a in RusLatAccord.__get_accords(): 
            if (a.lat_to_rus and len(a.lat) >= max_len): 
                i = 0
                while i < len(a.lat): 
                    if ((pos + i) >= len(txt)): 
                        break
                    if (txt[pos + i] != a.lat[i]): 
                        break
                    i += 1
                if ((i < len(a.lat)) or (len(a.lat) < 1)): 
                    continue
                if (len(a.lat) > max_len): 
                    res.clear()
                    max_len = len(a.lat)
                res.append(a.rus)
        return max_len
    
    @staticmethod
    def _new465(_arg1 : str, _arg2 : str, _arg3 : bool) -> 'RusLatAccord':
        res = RusLatAccord(_arg1, _arg2)
        res.on_tail = _arg3
        return res