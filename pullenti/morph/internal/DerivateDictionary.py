# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.morph.internal.ExplanTreeNode import ExplanTreeNode
from pullenti.morph.internal.ExplanSerializeHelper import ExplanSerializeHelper
from pullenti.morph.DerivateGroup import DerivateGroup
from pullenti.morph.LanguageHelper import LanguageHelper


class DerivateDictionary:
    
    def __init__(self) -> None:
        self.lang = None
        self.__m_inited = False
        self._m_root = ExplanTreeNode()
        self._m_all_groups = list()
    
    def init(self, lang_ : 'MorphLang') -> bool:
        if (self.__m_inited): 
            return True
        # ignored: assembly = .
        rsname = "d_{0}.dat".format(str(lang_))
        names = Utils.getResourcesNames('pullenti.morph.properties', '.dat')
        for n in names: 
            if (n.upper().endswith(rsname.upper())): 
                inf = Utils.getResourceInfo('pullenti.morph.properties', n)
                if (inf is None): 
                    continue
                with Utils.getResourceStream('pullenti.morph.properties', n) as stream: 
                    stream.seek(0, io.SEEK_SET)
                    self._m_all_groups.clear()
                    ExplanSerializeHelper.deserializedd(stream, self, True)
                    self.lang = lang_
                self.__m_inited = True
                return True
        return False
    
    def unload(self) -> None:
        from pullenti.morph.MorphLang import MorphLang
        self._m_root = ExplanTreeNode()
        self._m_all_groups.clear()
        self.lang = MorphLang()
    
    def add(self, dg : 'DerivateGroup') -> None:
        self._m_all_groups.append(dg)
        for w in dg.words: 
            if (w.spelling is None): 
                continue
            tn = self._m_root
            for i in range(len(w.spelling)):
                k = ord(w.spelling[i])
                tn1 = None
                if (tn.nodes is None): 
                    tn.nodes = dict()
                inoutarg1 = RefOutArgWrapper(None)
                inoutres2 = Utils.tryGetValue(tn.nodes, k, inoutarg1)
                tn1 = inoutarg1.value
                if (not inoutres2): 
                    tn1 = ExplanTreeNode()
                    tn.nodes[k] = tn1
                tn = tn1
            tn._add_group(dg)
    
    def find(self, word : str, try_create : bool, lang_ : 'MorphLang') -> typing.List['DerivateGroup']:
        if (Utils.isNullOrEmpty(word)): 
            return None
        tn = self._m_root
        for i in range(len(word)):
            k = ord(word[i])
            tn1 = None
            if (tn.nodes is None): 
                break
            inoutarg3 = RefOutArgWrapper(None)
            inoutres4 = Utils.tryGetValue(tn.nodes, k, inoutarg3)
            tn1 = inoutarg3.value
            if (not inoutres4): 
                break
            tn = tn1
            if (tn._lazy is not None): 
                tn._load()
        else: i = len(word)
        res = (None if i < len(word) else tn.groups)
        li = None
        if (isinstance(res, list)): 
            li = list(res if isinstance(res, list) else None)
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
            li.append(res if isinstance(res, DerivateGroup) else None)
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
            word1 = word[0 : (len(word) - 1)]
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
            word1 = word[0 : (len(word) - 2)]
            if (word1 == "ЯТЬ"): 
                return None
            li = self.find(word1, False, lang_)
            if ((li) is not None): 
                return li
        elif (ch0 == 'Е' and ch1 == 'Ь'): 
            word1 = word[0 : (len(word) - 2)] + "ИЕ"
            li = self.find(word1, False, lang_)
            if ((li) is not None): 
                return li
        elif (ch0 == 'Й' and ch2 == 'Н' and try_create): 
            ch3 = word[len(word) - 4]
            word1 = None
            if (ch3 != 'Н'): 
                if (LanguageHelper.is_cyrillic_vowel(ch3)): 
                    word1 = (word[0 : (len(word) - 3)] + "Н" + word[len(word) - 3 : ])
            else: 
                word1 = (word[0 : (len(word) - 4)] + word[len(word) - 3 : ])
            if (word1 is not None): 
                li = self.find(word1, False, lang_)
                if ((li) is not None): 
                    return li
        if (ch0 == 'Й' and ch1 == 'О'): 
            word2 = word[0 : (len(word) - 2)]
            li = self.find(word2 + "ИЙ", False, lang_)
            if ((li) is not None): 
                return li
            li = self.find(word2 + "ЫЙ", False, lang_)
            if ((li) is not None): 
                return li
        if (not try_create): 
            return None
        len0 = len(word) - 4
        i = 1
        first_pass2512 = True
        while True:
            if first_pass2512: first_pass2512 = False
            else: i += 1
            if (not (i <= len0)): break
            rest = word[i : ]
            li1 = self.find(rest, False, lang_)
            if (li1 is None): 
                continue
            pref = word[0 : (i)]
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