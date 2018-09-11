# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr


class TerminCollection:
    """ Коллекций некоторых обозначений, терминов """
    
    class CharNode:
        
        def __init__(self) -> None:
            self.children = None
            self.termins = None
    
    def __init__(self) -> None:
        self.termins = list()
        self.all_add_strs_normalized = False
        self.__m_root = TerminCollection.CharNode()
        self.__m_root_ua = TerminCollection.CharNode()
        self.__m_hash1 = dict()
        self.__m_hash_canonic = None
    
    def add(self, term : 'Termin') -> None:
        self.termins.append(term)
        self.__m_hash_canonic = (None)
        self.reindex(term)
    
    def add_str(self, termins_ : str, tag : object=None, lang : 'MorphLang'=MorphLang(), is_normal_text : bool=False) -> 'Termin':
        from pullenti.ner.core.Termin import Termin
        t = Termin(termins_, lang, is_normal_text or self.all_add_strs_normalized)
        t.tag = tag
        if (tag is not None and len(t.terms) == 1): 
            pass
        self.add(t)
        return t
    
    def __get_root(self, lang : 'MorphLang', is_lat : bool) -> 'CharNode':
        if (lang is not None and lang.is_ua and not lang.is_ru): 
            return self.__m_root_ua
        return self.__m_root
    
    def reindex(self, t : 'Termin') -> None:
        if (t is None): 
            return
        if (len(t.terms) > 20): 
            pass
        if (t.acronym_smart is not None): 
            self.__add_to_hash1(ord(t.acronym_smart[0]), t)
        if (t.abridges is not None): 
            for a in t.abridges: 
                if (len(a.parts[0].value) == 1): 
                    self.__add_to_hash1(ord(a.parts[0].value[0]), t)
        for v in t._get_hash_variants(): 
            self.__add_to_tree(v, t)
        if (t.additional_vars is not None): 
            for av in t.additional_vars: 
                av.ignore_terms_order = t.ignore_terms_order
                for v in av._get_hash_variants(): 
                    self.__add_to_tree(v, t)
    
    def remove(self, t : 'Termin') -> None:
        for v in t._get_hash_variants(): 
            self.__remove_from_tree(v, t)
        for li in self.__m_hash1.values(): 
            for tt in li: 
                if (tt == t): 
                    li.remove(tt)
                    break
        i = Utils.indexOfList(self.termins, t, 0)
        if (i >= 0): 
            del self.termins[i]
    
    def __add_to_tree(self, key : str, t : 'Termin') -> None:
        if (key is None): 
            return
        nod = self.__get_root(t.lang, t.lang.is_undefined and LanguageHelper.is_latin(key))
        i = 0
        while i < len(key): 
            ch = ord(key[i])
            if (nod.children is None): 
                nod.children = dict()
            inoutarg629 = RefOutArgWrapper(None)
            inoutres630 = Utils.tryGetValue(nod.children, ch, inoutarg629)
            nn = inoutarg629.value
            if (not inoutres630): 
                nn = TerminCollection.CharNode()
                nod.children[ch] = nn
            nod = nn
            i += 1
        if (nod.termins is None): 
            nod.termins = list()
        if (not t in nod.termins): 
            nod.termins.append(t)
    
    def __remove_from_tree(self, key : str, t : 'Termin') -> None:
        if (key is None): 
            return
        nod = self.__get_root(t.lang, t.lang.is_undefined and LanguageHelper.is_latin(key))
        i = 0
        while i < len(key): 
            ch = ord(key[i])
            if (nod.children is None): 
                return
            inoutarg631 = RefOutArgWrapper(None)
            inoutres632 = Utils.tryGetValue(nod.children, ch, inoutarg631)
            nn = inoutarg631.value
            if (not inoutres632): 
                return
            nod = nn
            i += 1
        if (nod.termins is None): 
            return
        if (t in nod.termins): 
            nod.termins.remove(t)
    
    def __find_in_tree(self, key : str, lang : 'MorphLang') -> typing.List['Termin']:
        if (key is None): 
            return None
        nod = self.__get_root(lang, ((lang is None or lang.is_undefined)) and LanguageHelper.is_latin(key))
        i = 0
        while i < len(key): 
            ch = ord(key[i])
            if (nod.children is None): 
                return None
            inoutarg633 = RefOutArgWrapper(None)
            inoutres634 = Utils.tryGetValue(nod.children, ch, inoutarg633)
            nn = inoutarg633.value
            if (not inoutres634): 
                return None
            nod = nn
            i += 1
        return nod.termins
    
    def __add_to_hash1(self, key : int, t : 'Termin') -> None:
        li = None
        inoutarg635 = RefOutArgWrapper(None)
        inoutres636 = Utils.tryGetValue(self.__m_hash1, key, inoutarg635)
        li = inoutarg635.value
        if (not inoutres636): 
            li = list()
            self.__m_hash1[key] = li
        if (not t in li): 
            li.append(t)
    
    def find(self, key : str) -> 'Termin':
        if (Utils.isNullOrEmpty(key)): 
            return None
        li = [ ]
        if (LanguageHelper.is_latin_char(key[0])): 
            li = self.__find_in_tree(key, MorphLang.EN)
        else: 
            li = self.__find_in_tree(key, MorphLang.RU)
            if (li is None): 
                li = self.__find_in_tree(key, MorphLang.UA)
        return (li[0] if li is not None and len(li) > 0 else None)
    
    def try_parse(self, token : 'Token', pars : 'TerminParseAttr'=TerminParseAttr.NO) -> 'TerminToken':
        if (len(self.termins) == 0): 
            return None
        li = self.try_parse_all(token, pars)
        if (li is not None): 
            return li[0]
        else: 
            return None
    
    def try_parse_all(self, token : 'Token', pars : 'TerminParseAttr'=TerminParseAttr.NO) -> typing.List['TerminToken']:
        if (token is None): 
            return None
        re = self.__try_attach_all_(token, pars, False)
        if (re is None and token.morph.language.is_ua): 
            re = self.__try_attach_all_(token, pars, True)
        return re
    
    def __try_attach_all_(self, token : 'Token', pars : 'TerminParseAttr'=TerminParseAttr.NO, main_root : bool=False) -> typing.List['TerminToken']:
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.ner.NumberToken import NumberToken
        if (len(self.termins) == 0 or token is None): 
            return None
        s = None
        tt = (token if isinstance(token, TextToken) else None)
        if (tt is None and (isinstance(token, ReferentToken))): 
            tt = ((token if isinstance(token, ReferentToken) else None).begin_token if isinstance((token if isinstance(token, ReferentToken) else None).begin_token, TextToken) else None)
        res = None
        was_vars = False
        root = (self.__m_root if main_root else self.__get_root(token.morph.language, token.chars.is_latin_letter))
        if (tt is not None): 
            s = tt.term
            nod = root
            no_vars = False
            len0 = 0
            if ((((pars) & (TerminParseAttr.TERMONLY))) != (TerminParseAttr.NO)): 
                pass
            elif (tt.invariant_prefix_length <= len(s)): 
                len0 = (tt.invariant_prefix_length)
                i = 0
                while i < tt.invariant_prefix_length: 
                    ch = ord(s[i])
                    if (nod.children is None): 
                        no_vars = True
                        break
                    inoutarg637 = RefOutArgWrapper(None)
                    inoutres638 = Utils.tryGetValue(nod.children, ch, inoutarg637)
                    nn = inoutarg637.value
                    if (not inoutres638): 
                        no_vars = True
                        break
                    nod = nn
                    i += 1
            if (not no_vars): 
                inoutarg643 = RefOutArgWrapper(res)
                inoutres644 = self.__manage_var(token, pars, s, nod, len0, inoutarg643)
                res = inoutarg643.value
                if (inoutres644): 
                    was_vars = True
                i = 0
                first_pass3718 = True
                while True:
                    if first_pass3718: first_pass3718 = False
                    else: i += 1
                    if (not (i < tt.morph.items_count)): break
                    if ((((pars) & (TerminParseAttr.TERMONLY))) != (TerminParseAttr.NO)): 
                        continue
                    wf = (tt.morph.get_indexer_item(i) if isinstance(tt.morph.get_indexer_item(i), MorphWordForm) else None)
                    if (wf is None): 
                        continue
                    if ((((pars) & (TerminParseAttr.INDICTIONARYONLY))) != (TerminParseAttr.NO)): 
                        if (not wf.is_in_dictionary): 
                            continue
                    ok = True
                    if (wf.normal_case is None or wf.normal_case == s): 
                        ok = False
                    else: 
                        j = 0
                        while j < i: 
                            wf2 = (tt.morph.get_indexer_item(j) if isinstance(tt.morph.get_indexer_item(j), MorphWordForm) else None)
                            if (wf2 is not None): 
                                if (wf2.normal_case == wf.normal_case or wf2.normal_full == wf.normal_case): 
                                    break
                            j += 1
                        if (j < i): 
                            ok = False
                    if (ok): 
                        inoutarg639 = RefOutArgWrapper(res)
                        inoutres640 = self.__manage_var(token, pars, wf.normal_case, nod, tt.invariant_prefix_length, inoutarg639)
                        res = inoutarg639.value
                        if (inoutres640): 
                            was_vars = True
                    if (wf.normal_full is None or wf.normal_full == wf.normal_case or wf.normal_full == s): 
                        continue
                    j = 0
                    while j < i: 
                        wf2 = (tt.morph.get_indexer_item(j) if isinstance(tt.morph.get_indexer_item(j), MorphWordForm) else None)
                        if (wf2 is not None and wf2.normal_full == wf.normal_full): 
                            break
                        j += 1
                    if (j < i): 
                        continue
                    inoutarg641 = RefOutArgWrapper(res)
                    inoutres642 = self.__manage_var(token, pars, wf.normal_full, nod, tt.invariant_prefix_length, inoutarg641)
                    res = inoutarg641.value
                    if (inoutres642): 
                        was_vars = True
        elif (isinstance(token, NumberToken)): 
            inoutarg645 = RefOutArgWrapper(res)
            inoutres646 = self.__manage_var(token, pars, str((token if isinstance(token, NumberToken) else None).value), root, 0, inoutarg645)
            res = inoutarg645.value
            if (inoutres646): 
                was_vars = True
        else: 
            return None
        if (not was_vars and s is not None and len(s) == 1): 
            vars0_ = [ ]
            inoutarg647 = RefOutArgWrapper(None)
            inoutres648 = Utils.tryGetValue(self.__m_hash1, ord(s[0]), inoutarg647)
            vars0_ = inoutarg647.value
            if (inoutres648): 
                for t in vars0_: 
                    if (not t.lang.is_undefined): 
                        if (not token.morph.language.is_undefined): 
                            if (((token.morph.language) & t.lang).is_undefined): 
                                continue
                    ar = t.try_parse(tt, TerminParseAttr.NO)
                    if (ar is None): 
                        continue
                    ar.termin = t
                    if (res is None): 
                        res = list()
                        res.append(ar)
                    elif (ar.tokens_count > res[0].tokens_count): 
                        res.clear()
                        res.append(ar)
                    elif (ar.tokens_count == res[0].tokens_count): 
                        res.append(ar)
        if (res is not None): 
            ii = 0
            max0_ = 0
            i = 0
            while i < len(res): 
                if (res[i].length_char > max0_): 
                    max0_ = res[i].length_char
                    ii = i
                i += 1
            if (ii > 0): 
                v = res[ii]
                del res[ii]
                res.insert(0, v)
        return res
    
    def __manage_var(self, token : 'Token', pars : 'TerminParseAttr', v : str, nod : 'CharNode', i0 : int, res : typing.List['TerminToken']) -> bool:
        i = i0
        while i < len(v): 
            ch = ord(v[i])
            if (nod.children is None): 
                return False
            inoutarg649 = RefOutArgWrapper(None)
            inoutres650 = Utils.tryGetValue(nod.children, ch, inoutarg649)
            nn = inoutarg649.value
            if (not inoutres650): 
                return False
            nod = nn
            i += 1
        vars0_ = nod.termins
        if (vars0_ is None or len(vars0_) == 0): 
            return False
        for t in vars0_: 
            ar = t.try_parse(token, pars)
            if (ar is not None): 
                ar.termin = t
                if (res.value is None): 
                    res.value = list()
                    res.value.append(ar)
                elif (ar.tokens_count > res.value[0].tokens_count): 
                    res.value.clear()
                    res.value.append(ar)
                elif (ar.tokens_count == res.value[0].tokens_count): 
                    j = 0
                    while j < len(res.value): 
                        if (res.value[j].termin == ar.termin): 
                            break
                        j += 1
                    if (j >= len(res.value)): 
                        res.value.append(ar)
            if (t.additional_vars is not None): 
                for av in t.additional_vars: 
                    ar = av.try_parse(token, pars)
                    if (ar is None): 
                        continue
                    ar.termin = t
                    if (res.value is None): 
                        res.value = list()
                        res.value.append(ar)
                    elif (ar.tokens_count > res.value[0].tokens_count): 
                        res.value.clear()
                        res.value.append(ar)
                    elif (ar.tokens_count == res.value[0].tokens_count): 
                        j = 0
                        while j < len(res.value): 
                            if (res.value[j].termin == ar.termin): 
                                break
                            j += 1
                        if (j >= len(res.value)): 
                            res.value.append(ar)
        return len(v) > 1
    
    def try_attach(self, termin : 'Termin') -> typing.List['Termin']:
        res = None
        for v in termin._get_hash_variants(): 
            vars0_ = self.__find_in_tree(v, termin.lang)
            if (vars0_ is None): 
                continue
            for t in vars0_: 
                if (t.is_equal(termin)): 
                    if (res is None): 
                        res = list()
                    if (not t in res): 
                        res.append(t)
        return res
    
    def try_attach_str(self, termin : str, lang : 'MorphLang'=MorphLang()) -> typing.List['Termin']:
        return self.__find_in_tree(termin, lang)
    
    def find_termin_by_canonic_text(self, text : str) -> typing.List['Termin']:
        if (self.__m_hash_canonic is None): 
            self.__m_hash_canonic = dict()
            for t in self.termins: 
                ct = t.canonic_text
                li = [ ]
                inoutarg651 = RefOutArgWrapper(None)
                inoutres652 = Utils.tryGetValue(self.__m_hash_canonic, ct, inoutarg651)
                li = inoutarg651.value
                if (not inoutres652): 
                    li = list()
                    self.__m_hash_canonic[ct] = li
                if (not t in li): 
                    li.append(t)
        res = [ ]
        inoutarg653 = RefOutArgWrapper(None)
        inoutres654 = Utils.tryGetValue(self.__m_hash_canonic, text, inoutarg653)
        res = inoutarg653.value
        if (not inoutres654): 
            return None
        else: 
            return res