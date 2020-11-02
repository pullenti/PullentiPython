# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import threading
import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.internal.ByteArrayWrapper import ByteArrayWrapper
from pullenti.semantic.utils.DerivateGroup import DerivateGroup
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.semantic.internal.ExplanTreeNode import ExplanTreeNode
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.internal.MorphDeserializer import MorphDeserializer

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
            self._deserialize(mem, True)
            self.__m_inited = True
    
    def init(self, lang_ : 'MorphLang', lazy : bool) -> bool:
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
                    self._deserialize(stream, lazy)
                    self.lang = lang_
                self.__m_inited = True
                return True
        return False
    
    def unload(self) -> None:
        self._m_root = ExplanTreeNode()
        self._m_all_groups.clear()
        self.lang = MorphLang()
    
    def _get_group(self, id0_ : int) -> 'DerivateGroup':
        if (id0_ >= 1 and id0_ <= len(self._m_all_groups)): 
            return self._m_all_groups[id0_ - 1]
        return None
    
    def __load_tree_node(self, tn : 'ExplanTreeNode') -> None:
        with self._m_lock: 
            pos = tn.lazy_pos
            if (pos > 0): 
                wrappos2917 = RefOutArgWrapper(pos)
                tn._deserialize(self.__m_buf, self, True, wrappos2917)
                pos = wrappos2917.value
            tn.lazy_pos = 0
    
    def _deserialize(self, str0_ : io.IOBase, lazy_load : bool) -> None:
        wr = None
        with io.BytesIO() as tmp: 
            MorphDeserializer.deflate_gzip(str0_, tmp)
            wr = ByteArrayWrapper(bytearray(tmp.getvalue()))
            pos = 0
            wrappos2921 = RefOutArgWrapper(pos)
            cou = wr.deserialize_int(wrappos2921)
            pos = wrappos2921.value
            while cou > 0: 
                wrappos2919 = RefOutArgWrapper(pos)
                p1 = wr.deserialize_int(wrappos2919)
                pos = wrappos2919.value
                ew = DerivateGroup()
                if (lazy_load): 
                    ew._lazy_pos = pos
                    pos = p1
                else: 
                    wrappos2918 = RefOutArgWrapper(pos)
                    ew._deserialize(wr, wrappos2918)
                    pos = wrappos2918.value
                ew.id0_ = (len(self._m_all_groups) + 1)
                self._m_all_groups.append(ew)
                cou -= 1
            self._m_root = ExplanTreeNode()
            wrappos2920 = RefOutArgWrapper(pos)
            self._m_root._deserialize(wr, self, lazy_load, wrappos2920)
            pos = wrappos2920.value
        self.__m_buf = wr
    
    def find(self, word : str, try_create : bool, lang_ : 'MorphLang') -> typing.List['DerivateGroup']:
        if (Utils.isNullOrEmpty(word)): 
            return None
        tn = self._m_root
        i = 0
        while i < len(word): 
            k = ord(word[i])
            if (tn.nodes is None): 
                break
            if (not k in tn.nodes): 
                break
            tn = tn.nodes[k]
            if (tn.lazy_pos > 0): 
                self.__load_tree_node(tn)
            i += 1
        li = None
        if (i >= len(word) and tn.groups is not None): 
            li = list()
            for g in tn.groups: 
                li.append(self._get_group(g))
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
        return None