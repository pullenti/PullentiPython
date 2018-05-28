# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper

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
        """ Добавить термин. После добавления в термин нельзя вносить изменений,
         кроме как в значения Tag и Tag2 (иначе потом нужно вызвать Reindex)
        
        Args:
            term(Termin): 
        """
        self.termins.append(term)
        self.__m_hash_canonic = None
        self.reindex(term)
    
    def add_str(self, termins_ : str, tag : object=None, lang : 'MorphLang'=MorphLang(), is_normal_text : bool=False) -> 'Termin':
        """ Добавить строку вместе с морфологическими вариантами
        
        Args:
            termins_(str): 
            tag(object): 
            lang(MorphLang): 
        
        """
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
        """ Переиндексировать термин (если после добавления у него что-либо поменялось)
        
        Args:
            t(Termin): 
        """
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
        for i in range(len(key)):
            ch = ord(key[i])
            if (nod.children is None): 
                nod.children = dict()
            inoutarg603 = RefOutArgWrapper(None)
            inoutres604 = Utils.tryGetValue(nod.children, ch, inoutarg603)
            nn = inoutarg603.value
            if (not inoutres604): 
                nn = TerminCollection.CharNode()
                nod.children[ch] = nn
            nod = nn
        if (nod.termins is None): 
            nod.termins = list()
        if (not t in nod.termins): 
            nod.termins.append(t)
    
    def __remove_from_tree(self, key : str, t : 'Termin') -> None:
        if (key is None): 
            return
        nod = self.__get_root(t.lang, t.lang.is_undefined and LanguageHelper.is_latin(key))
        for i in range(len(key)):
            ch = ord(key[i])
            if (nod.children is None): 
                return
            inoutarg605 = RefOutArgWrapper(None)
            inoutres606 = Utils.tryGetValue(nod.children, ch, inoutarg605)
            nn = inoutarg605.value
            if (not inoutres606): 
                return
            nod = nn
        if (nod.termins is None): 
            return
        if (t in nod.termins): 
            nod.termins.remove(t)
    
    def __find_in_tree(self, key : str, lang : 'MorphLang') -> typing.List['Termin']:
        if (key is None): 
            return None
        nod = self.__get_root(lang, ((lang is None or lang.is_undefined)) and LanguageHelper.is_latin(key))
        for i in range(len(key)):
            ch = ord(key[i])
            if (nod.children is None): 
                return None
            inoutarg607 = RefOutArgWrapper(None)
            inoutres608 = Utils.tryGetValue(nod.children, ch, inoutarg607)
            nn = inoutarg607.value
            if (not inoutres608): 
                return None
            nod = nn
        return nod.termins
    
    def __add_to_hash1(self, key : int, t : 'Termin') -> None:
        li = None
        inoutarg609 = RefOutArgWrapper(None)
        inoutres610 = Utils.tryGetValue(self.__m_hash1, key, inoutarg609)
        li = inoutarg609.value
        if (not inoutres610): 
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
        """ Попытка привязать к аналитическому контейнеру с указанной позиции
        
        Args:
            token(Token): начальная позиция
            pars(TerminParseAttr): параметры выделения
        
        """
        if (len(self.termins) == 0): 
            return None
        li = self.try_parse_all(token, pars)
        if (li is not None): 
            return li[0]
        else: 
            return None
    
    def try_parse_all(self, token : 'Token', pars : 'TerminParseAttr'=TerminParseAttr.NO) -> typing.List['TerminToken']:
        """ Попытка привязать все возможные варианты
        
        Args:
            token(Token): 
            pars(TerminParseAttr): параметры выделения
        
        """
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
        if (tt is None and isinstance(token, ReferentToken)): 
            tt = ((token if isinstance(token, ReferentToken) else None).begin_token if isinstance((token if isinstance(token, ReferentToken) else None).begin_token, TextToken) else None)
        res = None
        was_vars = False
        root = (self.__m_root if main_root else self.__get_root(token.morph.language, token.chars.is_latin_letter))
        if (tt is not None): 
            s = tt.term
            nod = root
            no_vars = False
            len0 = 0
            if (((pars & TerminParseAttr.TERMONLY)) != TerminParseAttr.NO): 
                pass
            elif (tt.invariant_prefix_length <= len(s)): 
                len0 = tt.invariant_prefix_length
                i = 0
                while i < tt.invariant_prefix_length: 
                    ch = ord(s[i])
                    if (nod.children is None): 
                        no_vars = True
                        break
                    inoutarg611 = RefOutArgWrapper(None)
                    inoutres612 = Utils.tryGetValue(nod.children, ch, inoutarg611)
                    nn = inoutarg611.value
                    if (not inoutres612): 
                        no_vars = True
                        break
                    nod = nn
                    i += 1
            if (not no_vars): 
                inoutarg617 = RefOutArgWrapper(res)
                inoutres618 = self.__manage_var(token, pars, s, nod, len0, inoutarg617)
                res = inoutarg617.value
                if (inoutres618): 
                    was_vars = True
                i = 0
                first_pass2610 = True
                while True:
                    if first_pass2610: first_pass2610 = False
                    else: i += 1
                    if (not (i < tt.morph.items_count)): break
                    if (((pars & TerminParseAttr.TERMONLY)) != TerminParseAttr.NO): 
                        continue
                    wf = (tt.morph.get_indexer_item(i) if isinstance(tt.morph.get_indexer_item(i), MorphWordForm) else None)
                    if (wf is None): 
                        continue
                    if (((pars & TerminParseAttr.INDICTIONARYONLY)) != TerminParseAttr.NO): 
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
                        inoutarg613 = RefOutArgWrapper(res)
                        inoutres614 = self.__manage_var(token, pars, wf.normal_case, nod, tt.invariant_prefix_length, inoutarg613)
                        res = inoutarg613.value
                        if (inoutres614): 
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
                    inoutarg615 = RefOutArgWrapper(res)
                    inoutres616 = self.__manage_var(token, pars, wf.normal_full, nod, tt.invariant_prefix_length, inoutarg615)
                    res = inoutarg615.value
                    if (inoutres616): 
                        was_vars = True
        elif (isinstance(token, NumberToken)): 
            inoutarg619 = RefOutArgWrapper(res)
            inoutres620 = self.__manage_var(token, pars, str((token if isinstance(token, NumberToken) else None).value), root, 0, inoutarg619)
            res = inoutarg619.value
            if (inoutres620): 
                was_vars = True
        else: 
            return None
        if (not was_vars and s is not None and len(s) == 1): 
            vars0 = [ ]
            inoutarg621 = RefOutArgWrapper(None)
            inoutres622 = Utils.tryGetValue(self.__m_hash1, ord(s[0]), inoutarg621)
            vars0 = inoutarg621.value
            if (inoutres622): 
                for t in vars0: 
                    if (not t.lang.is_undefined): 
                        if (not token.morph.language.is_undefined): 
                            if ((token.morph.language & t.lang).is_undefined): 
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
            max0 = 0
            for i in range(len(res)):
                if (res[i].length_char > max0): 
                    max0 = res[i].length_char
                    ii = i
            if (ii > 0): 
                v = res[ii]
                del res[ii]
                res.insert(0, v)
        return res
    
    def __manage_var(self, token : 'Token', pars : 'TerminParseAttr', v : str, nod : 'CharNode', i0 : int, res : typing.List['TerminToken']) -> bool:
        for i in range(i0, len(v), 1):
            ch = ord(v[i])
            if (nod.children is None): 
                return False
            inoutarg623 = RefOutArgWrapper(None)
            inoutres624 = Utils.tryGetValue(nod.children, ch, inoutarg623)
            nn = inoutarg623.value
            if (not inoutres624): 
                return False
            nod = nn
        vars0 = nod.termins
        if (vars0 is None or len(vars0) == 0): 
            return False
        for t in vars0: 
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
                    for j in range(len(res.value)):
                        if (res.value[j].termin == ar.termin): 
                            break
                    else: j = len(res.value)
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
                        for j in range(len(res.value)):
                            if (res.value[j].termin == ar.termin): 
                                break
                        else: j = len(res.value)
                        if (j >= len(res.value)): 
                            res.value.append(ar)
        return len(v) > 1
    
    def try_attach(self, termin : 'Termin') -> typing.List['Termin']:
        """ Поискать эквивалентные термины
        
        Args:
            termin(Termin): 
        
        """
        res = None
        for v in termin._get_hash_variants(): 
            vars0 = self.__find_in_tree(v, termin.lang)
            if (vars0 is None): 
                continue
            for t in vars0: 
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
                inoutarg625 = RefOutArgWrapper(None)
                inoutres626 = Utils.tryGetValue(self.__m_hash_canonic, ct, inoutarg625)
                li = inoutarg625.value
                if (not inoutres626): 
                    li = list()
                    self.__m_hash_canonic[ct] = li
                if (not t in li): 
                    li.append(t)
        res = [ ]
        inoutarg627 = RefOutArgWrapper(None)
        inoutres628 = Utils.tryGetValue(self.__m_hash_canonic, text, inoutarg627)
        res = inoutarg627.value
        if (not inoutres628): 
            return None
        else: 
            return res