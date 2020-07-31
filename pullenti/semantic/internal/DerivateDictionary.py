﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import threading
import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.semantic.utils.DerivateGroup import DerivateGroup
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphLang import MorphLang
from pullenti.semantic.internal.ExplanTreeNode import ExplanTreeNode
from pullenti.semantic.internal.DeserializeHelper import DeserializeHelper

class DerivateDictionary:
    
    def __init__(self) -> None:
        self.lang = None;
        self.__m_inited = False
        self.__m_buf = None;
        self._m_root = ExplanTreeNode()
        self._m_all_groups = list()
        self._m_lock = threading.Lock()
    
    def load(self, dat : bytearray) -> None:
        with io.BytesIO(dat) as mem: 
            self._m_all_groups.clear()
            self._m_root = ExplanTreeNode()
            self.__m_buf = DeserializeHelper.deserializedd(mem, self, True)
            self.__m_inited = True
    
    def init(self, lang_ : 'MorphLang') -> bool:
        if (self.__m_inited): 
            return True
        # ignored: assembly = 
        rsname = "d_{0}.dat".format(str(lang_))
        names = Utils.getResourcesNames('pullenti.semantic.utils.properties', '.dat')
        for n in names: 
            if (Utils.endsWithString(n, rsname, True)): 
                inf = Utils.getResourceInfo('pullenti.semantic.utils.properties', n)
                if (inf is None): 
                    continue
                with Utils.getResourceStream('pullenti.semantic.utils.properties', n) as stream: 
                    stream.seek(0, io.SEEK_SET)
                    self._m_all_groups.clear()
                    self.__m_buf = DeserializeHelper.deserializedd(stream, self, True)
                    self.lang = lang_
                self.__m_inited = True
                return True
        return False
    
    def unload(self) -> None:
        self._m_root = ExplanTreeNode()
        self._m_all_groups.clear()
        self.lang = MorphLang()
    
    def add(self, dg : 'DerivateGroup') -> None:
        self._m_all_groups.append(dg)
        for w in dg.words: 
            if (w.spelling is None): 
                continue
            tn = self._m_root
            i = 0
            while i < len(w.spelling): 
                k = ord(w.spelling[i])
                tn1 = None
                if (tn.nodes is None): 
                    tn.nodes = dict()
                wraptn12985 = RefOutArgWrapper(None)
                inoutres2986 = Utils.tryGetValue(tn.nodes, k, wraptn12985)
                tn1 = wraptn12985.value
                if (not inoutres2986): 
                    tn1 = ExplanTreeNode()
                    tn.nodes[k] = tn1
                tn = tn1
                i += 1
            tn._add_group(dg)
    
    def __load_tree_node(self, tn : 'ExplanTreeNode') -> None:
        with self._m_lock: 
            pos = tn.lazy_pos
            if (pos > 0): 
                wrappos2987 = RefOutArgWrapper(pos)
                DeserializeHelper.deserialize_tree_node(self.__m_buf, self, tn, True, wrappos2987)
                pos = wrappos2987.value
            tn.lazy_pos = 0
    
    def find(self, word : str, try_create : bool, lang_ : 'MorphLang') -> typing.List['DerivateGroup']:
        if (Utils.isNullOrEmpty(word)): 
            return None
        tn = self._m_root
        i = 0
        while i < len(word): 
            k = ord(word[i])
            tn1 = None
            if (tn.nodes is None): 
                break
            wraptn12988 = RefOutArgWrapper(None)
            inoutres2989 = Utils.tryGetValue(tn.nodes, k, wraptn12988)
            tn1 = wraptn12988.value
            if (not inoutres2989): 
                break
            tn = tn1
            if (tn.lazy_pos > 0): 
                self.__load_tree_node(tn)
            i += 1
        res = (None if i < len(word) else tn.groups)
        li = None
        if (isinstance(res, list)): 
            li = list(Utils.asObjectOrNull(res, list))
            gen = False
            nogen = False
            for g in li: 
                if (g.is_generated): 
                    gen = True
                else: 
                    nogen = True
            if (gen and nogen): 
                for i in range(len(li) - 1, -1, -1):
                    if (li[i].is_generated): 
                        del li[i]
                else: i = -1
        elif (isinstance(res, DerivateGroup)): 
            li = list()
            li.append(Utils.asObjectOrNull(res, DerivateGroup))
        if (li is not None and lang_ is not None and not lang_.is_undefined): 
            for i in range(len(li) - 1, -1, -1):
                if (not li[i].contains_word(word, lang_)): 
                    del li[i]
            else: i = -1
        if (li is not None and len(li) > 0): 
            return li
        if (len(word) < 4): 
            return None
        ch0 = word[len(word) - 1]
        ch1 = word[len(word) - 2]
        ch2 = word[len(word) - 3]
        if (ch0 == 'О' or ((ch0 == 'И' and ch1 == 'К'))): 
            word1 = word[0:0+len(word) - 1]
            li = self.find(word1 + "ИЙ", False, lang_)
            if ((li) is not None): 
                return li
            li = self.find(word1 + "ЫЙ", False, lang_)
            if ((li) is not None): 
                return li
            if (ch0 == 'О' and ch1 == 'Н'): 
                li = self.find(word1 + "СКИЙ", False, lang_)
                if ((li) is not None): 
                    return li
        elif (((ch0 == 'Я' or ch0 == 'Ь')) and ((word[len(word) - 2] == 'С'))): 
            word1 = word[0:0+len(word) - 2]
            if (word1 == "ЯТЬ"): 
                return None
            li = self.find(word1, False, lang_)
            if ((li) is not None): 
                return li
        elif (ch0 == 'Е' and ch1 == 'Ь'): 
            word1 = word[0:0+len(word) - 2] + "ИЕ"
            li = self.find(word1, False, lang_)
            if ((li) is not None): 
                return li
        elif (ch0 == 'Й' and ch2 == 'Н' and try_create): 
            ch3 = word[len(word) - 4]
            word1 = None
            if (ch3 != 'Н'): 
                if (LanguageHelper.is_cyrillic_vowel(ch3)): 
                    word1 = (word[0:0+len(word) - 3] + "Н" + word[len(word) - 3:])
            else: 
                word1 = (word[0:0+len(word) - 4] + word[len(word) - 3:])
            if (word1 is not None): 
                li = self.find(word1, False, lang_)
                if ((li) is not None): 
                    return li
        if (ch0 == 'Й' and ch1 == 'О'): 
            word2 = word[0:0+len(word) - 2]
            li = self.find(word2 + "ИЙ", False, lang_)
            if ((li) is not None): 
                return li
            li = self.find(word2 + "ЫЙ", False, lang_)
            if ((li) is not None): 
                return li
        if (not try_create): 
            return None
        len0_ = len(word) - 4
        i = 1
        first_pass4054 = True
        while True:
            if first_pass4054: first_pass4054 = False
            else: i += 1
            if (not (i <= len0_)): break
            rest = word[i:]
            li1 = self.find(rest, False, lang_)
            if (li1 is None): 
                continue
            pref = word[0:0+i]
            gen = list()
            for dg in li1: 
                if (not dg.is_dummy and not dg.is_generated): 
                    if (dg.not_generate): 
                        if (len(rest) < 5): 
                            continue
                    gg = dg.create_by_prefix(pref, lang_)
                    if (gg is not None): 
                        gen.append(gg)
                        self.add(gg)
            if (len(gen) == 0): 
                return None
            return gen
        return None