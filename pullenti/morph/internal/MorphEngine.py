# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import threading
import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphTense import MorphTense
from pullenti.morph.MorphVoice import MorphVoice
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphMood import MorphMood
from pullenti.morph.MorphPerson import MorphPerson
from pullenti.morph.internal.ByteArrayWrapper import ByteArrayWrapper
from pullenti.morph.internal.MorphDeserializer import MorphDeserializer
from pullenti.morph.internal.MorphRule import MorphRule
from pullenti.morph.internal.MorphTreeNode import MorphTreeNode
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphMiscInfo import MorphMiscInfo
from pullenti.morph.MorphWordForm import MorphWordForm

class MorphEngine:
    
    def __init__(self) -> None:
        self._m_lock = threading.Lock()
        self.__m_lazy_buf = None;
        self.m_root = MorphTreeNode()
        self.m_root_reverce = MorphTreeNode()
        self.__m_rules = list()
        self.__m_misc_infos = list()
        self.language = MorphLang()
    
    def __get_lazy_buf(self) -> 'ByteArrayWrapper':
        return self.__m_lazy_buf
    
    def add_rule(self, r : 'MorphRule') -> None:
        self.__m_rules.append(r)
    
    def get_rule(self, id0_ : int) -> 'MorphRule':
        if (id0_ > 0 and id0_ <= len(self.__m_rules)): 
            return self.__m_rules[id0_ - 1]
        return None
    
    def get_mut_rule(self, id0_ : int) -> 'MorphRule':
        if (id0_ > 0 and id0_ <= len(self.__m_rules)): 
            return self.__m_rules[id0_ - 1]
        return None
    
    def get_rule_var(self, rid : int, vid : int) -> 'MorphRuleVariant':
        r = self.get_rule(rid)
        if (r is None): 
            return None
        return r.find_var(vid)
    
    def add_misc_info(self, mi : 'MorphMiscInfo') -> None:
        if (mi.id0_ == 0): 
            mi.id0_ = (len(self.__m_misc_infos) + 1)
        self.__m_misc_infos.append(mi)
    
    def get_misc_info(self, id0_ : int) -> 'MorphMiscInfo':
        if (id0_ > 0 and id0_ <= len(self.__m_misc_infos)): 
            return self.__m_misc_infos[id0_ - 1]
        return None
    
    def initialize(self, lang : 'MorphLang', lazy_load : bool) -> bool:
        if (not self.language.is_undefined): 
            return False
        with self._m_lock: 
            if (not self.language.is_undefined): 
                return False
            self.language = lang
            # ignored: assembly = 
            rsname = "m_{0}.dat".format(str(lang))
            names = Utils.getResourcesNames('pullenti.morph.internal.properties', '.dat')
            for n in names: 
                if (Utils.endsWithString(n, rsname, True)): 
                    inf = Utils.getResourceInfo('pullenti.morph.internal.properties', n)
                    if (inf is None): 
                        continue
                    with Utils.getResourceStream('pullenti.morph.internal.properties', n) as stream: 
                        stream.seek(0, io.SEEK_SET)
                        self.deserialize(stream, False, lazy_load)
                    return True
            return False
    
    def __load_tree_node(self, tn : 'MorphTreeNode') -> None:
        with self._m_lock: 
            pos = tn.lazy_pos
            if (pos > 0): 
                wrappos8 = RefOutArgWrapper(pos)
                tn._deserialize_lazy(self.__m_lazy_buf, self, wrappos8)
                pos = wrappos8.value
            tn.lazy_pos = 0
    
    def process(self, word : str) -> typing.List['MorphWordForm']:
        """ Обработка одного слова
        
        Args:
            word(str): слово должно быть в верхнем регистре
        
        """
        if (Utils.isNullOrEmpty(word)): 
            return None
        res = None
        if (len(word) > 1): 
            i = 0
            while i < len(word): 
                ch = word[i]
                if (LanguageHelper.is_cyrillic_vowel(ch) or LanguageHelper.is_latin_vowel(ch)): 
                    break
                i += 1
            if (i >= len(word)): 
                return res
        mvs = [ ]
        tn = self.m_root
        i = 0
        while i <= len(word): 
            if (tn.lazy_pos > 0): 
                self.__load_tree_node(tn)
            if (tn.rule_ids is not None): 
                word_begin = None
                word_end = None
                if (i == 0): 
                    word_end = word
                elif (i < len(word)): 
                    word_end = word[i:]
                else: 
                    word_end = ""
                if (res is None): 
                    res = list()
                for rid in tn.rule_ids: 
                    r = self.get_rule(rid)
                    mvs = r.get_vars(word_end)
                    if (mvs is None): 
                        continue
                    if (word_begin is None): 
                        if (i == len(word)): 
                            word_begin = word
                        elif (i > 0): 
                            word_begin = word[0:0+i]
                        else: 
                            word_begin = ""
                    self.__process_result(res, word_begin, mvs)
            if (tn.nodes is None or i >= len(word)): 
                break
            ch = ord(word[i])
            wraptn9 = RefOutArgWrapper(None)
            inoutres10 = Utils.tryGetValue(tn.nodes, ch, wraptn9)
            tn = wraptn9.value
            if (not inoutres10): 
                break
            i += 1
        need_test_unknown_vars = True
        if (res is not None): 
            for r in res: 
                if ((r.class0_.is_pronoun or r.class0_.is_noun or r.class0_.is_adjective) or (r.class0_.is_misc and r.class0_.is_conjunction) or r.class0_.is_preposition): 
                    need_test_unknown_vars = False
                elif (r.class0_.is_adverb and r.normal_case is not None): 
                    if (not LanguageHelper.ends_with_ex(r.normal_case, "О", "А", None, None)): 
                        need_test_unknown_vars = False
                    elif (r.normal_case == "МНОГО"): 
                        need_test_unknown_vars = False
                elif (r.class0_.is_verb and len(res) > 1): 
                    ok = False
                    for rr in res: 
                        if (rr != r and rr.class0_ != r.class0_): 
                            ok = True
                            break
                    if (ok and not LanguageHelper.ends_with(word, "ИМ")): 
                        need_test_unknown_vars = False
        if (need_test_unknown_vars and LanguageHelper.is_cyrillic_char(word[0])): 
            gl = 0
            sog = 0
            j = 0
            while j < len(word): 
                if (LanguageHelper.is_cyrillic_vowel(word[j])): 
                    gl += 1
                else: 
                    sog += 1
                j += 1
            if ((gl < 2) or (sog < 2)): 
                need_test_unknown_vars = False
        if (need_test_unknown_vars and res is not None and len(res) == 1): 
            if (res[0].class0_.is_verb): 
                if ("н.вр." in res[0].misc.attrs and "нес.в." in res[0].misc.attrs and not "страд.з." in res[0].misc.attrs): 
                    need_test_unknown_vars = False
                elif ("б.вр." in res[0].misc.attrs and "сов.в." in res[0].misc.attrs): 
                    need_test_unknown_vars = False
                elif ("инф." in res[0].misc.attrs and "сов.в." in res[0].misc.attrs): 
                    need_test_unknown_vars = False
                elif (res[0].normal_case is not None and LanguageHelper.ends_with(res[0].normal_case, "СЯ")): 
                    need_test_unknown_vars = False
            if (res[0].class0_.is_undefined and "прдктв." in res[0].misc.attrs): 
                need_test_unknown_vars = False
        if (need_test_unknown_vars): 
            if (self.m_root_reverce is None): 
                return res
            tn = self.m_root_reverce
            tn0 = self.m_root_reverce
            for i in range(len(word) - 1, -1, -1):
                if (tn.lazy_pos > 0): 
                    self.__load_tree_node(tn)
                ch = ord(word[i])
                if (tn.nodes is None): 
                    break
                if (not ch in tn.nodes): 
                    break
                tn = tn.nodes[ch]
                if (tn.lazy_pos > 0): 
                    self.__load_tree_node(tn)
                if (tn.reverce_variants is not None): 
                    tn0 = tn
                    break
            else: i = -1
            if (tn0 != self.m_root_reverce): 
                glas = i < 4
                while i >= 0: 
                    if (LanguageHelper.is_cyrillic_vowel(word[i]) or LanguageHelper.is_latin_vowel(word[i])): 
                        glas = True
                        break
                    i -= 1
                if (glas): 
                    for mvref in tn0.reverce_variants: 
                        mv = self.get_rule_var(mvref.rule_id, mvref.variant_id)
                        if (mv is None): 
                            continue
                        if (((not mv.class0_.is_verb and not mv.class0_.is_adjective and not mv.class0_.is_noun) and not mv.class0_.is_proper_surname and not mv.class0_.is_proper_geo) and not mv.class0_.is_proper_secname): 
                            continue
                        ok = False
                        for rr in res: 
                            if (rr.is_in_dictionary): 
                                if (rr.class0_ == mv.class0_ or rr.class0_.is_noun): 
                                    ok = True
                                    break
                                if (not mv.class0_.is_adjective and rr.class0_.is_verb): 
                                    ok = True
                                    break
                        if (ok): 
                            continue
                        if (len(mv.tail) > 0 and not LanguageHelper.ends_with(word, mv.tail)): 
                            continue
                        r = MorphWordForm(mv, word, self.get_misc_info(mv.misc_info_id))
                        if (not r._has_morph_equals(res)): 
                            r.undef_coef = mvref.coef
                            if (res is None): 
                                res = list()
                            res.append(r)
        if (word == "ПРИ" and res is not None): 
            for i in range(len(res) - 1, -1, -1):
                if (res[i].class0_.is_proper_geo): 
                    del res[i]
            else: i = -1
        if (res is None or len(res) == 0): 
            return None
        self.__sort(res, word)
        for v in res: 
            if (v.normal_case is None): 
                v.normal_case = word
            if (v.class0_.is_verb): 
                if (v.normal_full is None and LanguageHelper.ends_with(v.normal_case, "ТЬСЯ")): 
                    v.normal_full = v.normal_case[0:0+len(v.normal_case) - 2]
            v.language = self.language
            if (v.class0_.is_preposition): 
                v.normal_case = LanguageHelper.normalize_preposition(v.normal_case)
        mc = MorphClass()
        for i in range(len(res) - 1, -1, -1):
            if (not res[i].is_in_dictionary and res[i].class0_.is_adjective and len(res) > 1): 
                if ("к.ф." in res[i].misc.attrs or "неизм." in res[i].misc.attrs): 
                    del res[i]
                    continue
            if (res[i].is_in_dictionary): 
                mc.value |= res[i].class0_.value
        else: i = -1
        if (mc == MorphClass.VERB and len(res) > 1): 
            for r in res: 
                if (r.undef_coef > (100) and r.class0_ == MorphClass.ADJECTIVE): 
                    r.undef_coef = (0)
        if (len(res) == 0): 
            return None
        return res
    
    def __process_result(self, res : typing.List['MorphWordForm'], word_begin : str, mvs : typing.List['MorphRuleVariant']) -> None:
        for mv in mvs: 
            r = MorphWordForm(mv, None, self.get_misc_info(mv.misc_info_id))
            if (mv.normal_tail is not None and len(mv.normal_tail) > 0 and mv.normal_tail[0] != '-'): 
                r.normal_case = (word_begin + mv.normal_tail)
            else: 
                r.normal_case = word_begin
            if (mv.full_normal_tail is not None): 
                if (len(mv.full_normal_tail) > 0 and mv.full_normal_tail[0] != '-'): 
                    r.normal_full = (word_begin + mv.full_normal_tail)
                else: 
                    r.normal_full = word_begin
            if (not r._has_morph_equals(res)): 
                r.undef_coef = (0)
                res.append(r)
    
    def get_all_wordforms(self, word : str) -> typing.List['MorphWordForm']:
        res = list()
        tn = self.m_root
        i = 0
        while i <= len(word): 
            if (tn.lazy_pos > 0): 
                self.__load_tree_node(tn)
            if (tn.rule_ids is not None): 
                word_begin = ""
                word_end = ""
                if (i > 0): 
                    word_begin = word[0:0+i]
                else: 
                    word_end = word
                if (i < len(word)): 
                    word_end = word[i:]
                else: 
                    word_begin = word
                for rid in tn.rule_ids: 
                    r = self.get_rule(rid)
                    if (r.contains_var(word_end)): 
                        for vl in r.morph_vars: 
                            for v in vl: 
                                wf = MorphWordForm(v, None, self.get_misc_info(v.misc_info_id))
                                if (not wf._has_morph_equals(res)): 
                                    wf.normal_case = (word_begin + v.tail)
                                    wf.undef_coef = (0)
                                    res.append(wf)
            if (tn.nodes is None or i >= len(word)): 
                break
            ch = ord(word[i])
            wraptn11 = RefOutArgWrapper(None)
            inoutres12 = Utils.tryGetValue(tn.nodes, ch, wraptn11)
            tn = wraptn11.value
            if (not inoutres12): 
                break
            i += 1
        i = 0
        first_pass3476 = True
        while True:
            if first_pass3476: first_pass3476 = False
            else: i += 1
            if (not (i < len(res))): break
            wf = res[i]
            if (wf.contains_attr("инф.", None)): 
                continue
            cas = wf.case_
            j = i + 1
            first_pass3477 = True
            while True:
                if first_pass3477: first_pass3477 = False
                else: j += 1
                if (not (j < len(res))): break
                wf1 = res[j]
                if (wf1.contains_attr("инф.", None)): 
                    continue
                if ((wf.class0_ == wf1.class0_ and wf.gender == wf1.gender and wf.number == wf1.number) and wf.normal_case == wf1.normal_case): 
                    cas |= wf1.case_
                    del res[j]
                    j -= 1
            if (cas != wf.case_): 
                res[i].case_ = cas
        i = 0
        first_pass3478 = True
        while True:
            if first_pass3478: first_pass3478 = False
            else: i += 1
            if (not (i < len(res))): break
            wf = res[i]
            if (wf.contains_attr("инф.", None)): 
                continue
            j = i + 1
            first_pass3479 = True
            while True:
                if first_pass3479: first_pass3479 = False
                else: j += 1
                if (not (j < len(res))): break
                wf1 = res[j]
                if (wf1.contains_attr("инф.", None)): 
                    continue
                if ((wf.class0_ == wf1.class0_ and wf.case_ == wf1.case_ and wf.number == wf1.number) and wf.normal_case == wf1.normal_case): 
                    wf.gender = Utils.valToEnum((wf.gender) | (wf1.gender), MorphGender)
                    del res[j]
                    j -= 1
        return res
    
    def get_wordform(self, word : str, cla : 'MorphClass', gender : 'MorphGender', cas : 'MorphCase', num : 'MorphNumber', add_info : 'MorphWordForm') -> str:
        tn = self.m_root
        find = False
        res = None
        max_coef = -10
        i = 0
        while i <= len(word): 
            if (tn.lazy_pos > 0): 
                self.__load_tree_node(tn)
            if (tn.rule_ids is not None): 
                word_begin = ""
                word_end = ""
                if (i > 0): 
                    word_begin = word[0:0+i]
                else: 
                    word_end = word
                if (i < len(word)): 
                    word_end = word[i:]
                else: 
                    word_begin = word
                for rid in tn.rule_ids: 
                    r = self.get_rule(rid)
                    if (r is not None and r.contains_var(word_end)): 
                        for li in r.morph_vars: 
                            for v in li: 
                                if ((((cla.value) & (v.class0_.value))) != 0 and v.normal_tail is not None): 
                                    if (cas.is_undefined): 
                                        if (v.case_.is_nominative or v.case_.is_undefined): 
                                            pass
                                        else: 
                                            continue
                                    elif (((v.case_) & cas).is_undefined): 
                                        continue
                                    sur = cla.is_proper_surname
                                    sur0 = v.class0_.is_proper_surname
                                    if (sur or sur0): 
                                        if (sur != sur0): 
                                            continue
                                    find = True
                                    if (gender != MorphGender.UNDEFINED): 
                                        if (((gender) & (v.gender)) == (MorphGender.UNDEFINED)): 
                                            if (num == MorphNumber.PLURAL): 
                                                pass
                                            else: 
                                                continue
                                    if (num != MorphNumber.UNDEFINED): 
                                        if (((num) & (v.number)) == (MorphNumber.UNDEFINED)): 
                                            continue
                                    re = word_begin + v.tail
                                    co = 0
                                    if (add_info is not None): 
                                        co = self.__calc_eq_coef(v, add_info)
                                    if (res is None or co > max_coef): 
                                        res = re
                                        max_coef = co
                                    if (max_coef == 0): 
                                        if ((word_begin + v.normal_tail) == word): 
                                            return word_begin + v.tail
            if (tn.nodes is None or i >= len(word)): 
                break
            ch = ord(word[i])
            wraptn13 = RefOutArgWrapper(None)
            inoutres14 = Utils.tryGetValue(tn.nodes, ch, wraptn13)
            tn = wraptn13.value
            if (not inoutres14): 
                break
            i += 1
        if (find): 
            return res
        tn = self.m_root_reverce
        tn0 = self.m_root_reverce
        for i in range(len(word) - 1, -1, -1):
            if (tn.lazy_pos > 0): 
                self.__load_tree_node(tn)
            ch = ord(word[i])
            if (tn.nodes is None): 
                break
            if (not ch in tn.nodes): 
                break
            tn = tn.nodes[ch]
            if (tn.lazy_pos > 0): 
                self.__load_tree_node(tn)
            if (tn.reverce_variants is not None): 
                tn0 = tn
                break
        else: i = -1
        if (tn0 == self.m_root_reverce): 
            return None
        for mvr in tn0.reverce_variants: 
            rule = self.get_rule(mvr.rule_id)
            if (rule is None): 
                continue
            mv = rule.find_var(mvr.variant_id)
            if (mv is None): 
                continue
            if ((((mv.class0_.value) & (cla.value))) != 0): 
                if (len(mv.tail) > 0 and not LanguageHelper.ends_with(word, mv.tail)): 
                    continue
                word_begin = word[0:0+len(word) - len(mv.tail)]
                for liv in rule.morph_vars: 
                    for v in liv: 
                        if ((((v.class0_.value) & (cla.value))) != 0): 
                            sur = cla.is_proper_surname
                            sur0 = v.class0_.is_proper_surname
                            if (sur or sur0): 
                                if (sur != sur0): 
                                    continue
                            if (not cas.is_undefined): 
                                if (((cas) & v.case_).is_undefined and not v.case_.is_undefined): 
                                    continue
                            if (num != MorphNumber.UNDEFINED): 
                                if (v.number != MorphNumber.UNDEFINED): 
                                    if (((v.number) & (num)) == (MorphNumber.UNDEFINED)): 
                                        continue
                            if (gender != MorphGender.UNDEFINED): 
                                if (v.gender != MorphGender.UNDEFINED): 
                                    if (((v.gender) & (gender)) == (MorphGender.UNDEFINED)): 
                                        continue
                            if (add_info is not None): 
                                if (self.__calc_eq_coef(v, add_info) < 0): 
                                    continue
                            res = (word_begin + v.tail)
                            if (res == word): 
                                return word
                            return res
        if (cla.is_proper_surname): 
            if ((gender == MorphGender.FEMINIE and cla.is_proper_surname and not cas.is_undefined) and not cas.is_nominative): 
                if (word.endswith("ВА") or word.endswith("НА")): 
                    if (cas.is_accusative): 
                        return word[0:0+len(word) - 1] + "У"
                    return word[0:0+len(word) - 1] + "ОЙ"
            if (gender == MorphGender.FEMINIE): 
                last = word[len(word) - 1]
                if (last == 'А' or last == 'Я' or last == 'О'): 
                    return word
                if (LanguageHelper.is_cyrillic_vowel(last)): 
                    return word[0:0+len(word) - 1] + "А"
                elif (last == 'Й'): 
                    return word[0:0+len(word) - 2] + "АЯ"
                else: 
                    return word + "А"
        return res
    
    def correct_word_by_morph(self, word : str) -> str:
        vars0_ = list()
        tmp = Utils.newStringIO(len(word))
        ch = 1
        while ch < len(word): 
            Utils.setLengthStringIO(tmp, 0)
            print(word, end="", file=tmp)
            Utils.setCharAtStringIO(tmp, ch, '*')
            var = self.__check_corr_var(Utils.toStringStringIO(tmp), self.m_root, 0)
            if (var is not None): 
                if (not var in vars0_): 
                    vars0_.append(var)
            ch += 1
        if (len(vars0_) == 0): 
            ch = 1
            while ch < len(word): 
                Utils.setLengthStringIO(tmp, 0)
                print(word, end="", file=tmp)
                Utils.insertStringIO(tmp, ch, '*')
                var = self.__check_corr_var(Utils.toStringStringIO(tmp), self.m_root, 0)
                if (var is not None): 
                    if (not var in vars0_): 
                        vars0_.append(var)
                ch += 1
        if (len(vars0_) == 0): 
            ch = 1
            while ch < (len(word) - 1): 
                Utils.setLengthStringIO(tmp, 0)
                print(word, end="", file=tmp)
                Utils.removeStringIO(tmp, ch, 1)
                var = self.__check_corr_var(Utils.toStringStringIO(tmp), self.m_root, 0)
                if (var is not None): 
                    if (not var in vars0_): 
                        vars0_.append(var)
                ch += 1
        if (len(vars0_) != 1): 
            return None
        return vars0_[0]
    
    def __check_corr_var(self, word : str, tn : 'MorphTreeNode', i : int) -> str:
        first_pass3480 = True
        while True:
            if first_pass3480: first_pass3480 = False
            else: i += 1
            if (not (i <= len(word))): break
            if (tn.lazy_pos > 0): 
                self.__load_tree_node(tn)
            if (tn.rule_ids is not None): 
                word_begin = ""
                word_end = ""
                if (i > 0): 
                    word_begin = word[0:0+i]
                else: 
                    word_end = word
                if (i < len(word)): 
                    word_end = word[i:]
                else: 
                    word_begin = word
                for rid in tn.rule_ids: 
                    r = self.get_rule(rid)
                    if (r.contains_var(word_end)): 
                        return word_begin + word_end
                    if (word_end.find('*') >= 0): 
                        for v in r.tails: 
                            if (len(v) == len(word_end)): 
                                j = 0
                                while j < len(v): 
                                    if (word_end[j] == '*' or word_end[j] == v[j]): 
                                        pass
                                    else: 
                                        break
                                    j += 1
                                if (j >= len(v)): 
                                    return word_begin + v
            if (tn.nodes is None or i >= len(word)): 
                break
            ch = ord(word[i])
            if (ch != (0x2A)): 
                if (not ch in tn.nodes): 
                    break
                tn = tn.nodes[ch]
                continue
            if (tn.nodes is not None): 
                for tnn in tn.nodes.items(): 
                    ww = word.replace('*', chr(tnn[0]))
                    res = self.__check_corr_var(ww, tnn[1], i + 1)
                    if (res is not None): 
                        return res
            break
        return None
    
    def process_surname_variants(self, word : str, res : typing.List['MorphWordForm']) -> None:
        self.__process_proper_variants(word, res, False)
    
    def process_geo_variants(self, word : str, res : typing.List['MorphWordForm']) -> None:
        self.__process_proper_variants(word, res, True)
    
    def __process_proper_variants(self, word : str, res : typing.List['MorphWordForm'], geo : bool) -> None:
        tn = self.m_root_reverce
        nodes_with_vars = None
        for i in range(len(word) - 1, -1, -1):
            if (tn.lazy_pos > 0): 
                self.__load_tree_node(tn)
            ch = ord(word[i])
            if (tn.nodes is None): 
                break
            if (not ch in tn.nodes): 
                break
            tn = tn.nodes[ch]
            if (tn.lazy_pos > 0): 
                self.__load_tree_node(tn)
            if (tn.reverce_variants is not None): 
                if (nodes_with_vars is None): 
                    nodes_with_vars = list()
                nodes_with_vars.append(tn)
        else: i = -1
        if (nodes_with_vars is None): 
            return
        for j in range(len(nodes_with_vars) - 1, -1, -1):
            tn = nodes_with_vars[j]
            if (tn.lazy_pos > 0): 
                self.__load_tree_node(tn)
            ok = False
            for vr in tn.reverce_variants: 
                v = self.get_rule_var(vr.rule_id, vr.variant_id)
                if (v is None): 
                    continue
                if (geo and v.class0_.is_proper_geo): 
                    pass
                elif (not geo and v.class0_.is_proper_surname): 
                    pass
                else: 
                    continue
                r = MorphWordForm(v, word, self.get_misc_info(v.misc_info_id))
                if (not r._has_morph_equals(res)): 
                    r.undef_coef = vr.coef
                    res.append(r)
                ok = True
            if (ok): 
                break
    
    def __compare(self, x : 'MorphWordForm', y : 'MorphWordForm') -> int:
        if (x.is_in_dictionary and not y.is_in_dictionary): 
            return -1
        if (not x.is_in_dictionary and y.is_in_dictionary): 
            return 1
        if (x.undef_coef > (0)): 
            if (x.undef_coef > ((y.undef_coef) * 2)): 
                return -1
            if (((x.undef_coef) * 2) < y.undef_coef): 
                return 1
        if (x.class0_ != y.class0_): 
            if ((x.class0_.is_preposition or x.class0_.is_conjunction or x.class0_.is_pronoun) or x.class0_.is_personal_pronoun): 
                return -1
            if ((y.class0_.is_preposition or y.class0_.is_conjunction or y.class0_.is_pronoun) or y.class0_.is_personal_pronoun): 
                return 1
            if (x.class0_.is_verb): 
                return 1
            if (y.class0_.is_verb): 
                return -1
            if (x.class0_.is_noun): 
                return -1
            if (y.class0_.is_noun): 
                return 1
        cx = self.__calc_coef(x)
        cy = self.__calc_coef(y)
        if (cx > cy): 
            return -1
        if (cx < cy): 
            return 1
        if (x.number == MorphNumber.PLURAL and y.number != MorphNumber.PLURAL): 
            return 1
        if (y.number == MorphNumber.PLURAL and x.number != MorphNumber.PLURAL): 
            return -1
        return 0
    
    def __calc_coef(self, wf : 'MorphWordForm') -> int:
        k = 0
        if (not wf.case_.is_undefined): 
            k += 1
        if (wf.gender != MorphGender.UNDEFINED): 
            k += 1
        if (wf.number != MorphNumber.UNDEFINED): 
            k += 1
        if (wf.misc.is_synonym_form): 
            k -= 3
        if (wf.normal_case is None or (len(wf.normal_case) < 4)): 
            return k
        if (wf.class0_.is_adjective and wf.number != MorphNumber.PLURAL): 
            last = wf.normal_case[len(wf.normal_case) - 1]
            last1 = wf.normal_case[len(wf.normal_case) - 2]
            ok = False
            if (wf.gender == MorphGender.FEMINIE): 
                if (last == 'Я'): 
                    ok = True
            if (wf.gender == MorphGender.MASCULINE): 
                if (last == 'Й'): 
                    if (last1 == 'И'): 
                        k += 1
                    ok = True
            if (wf.gender == MorphGender.NEUTER): 
                if (last == 'Е'): 
                    ok = True
            if (ok): 
                if (LanguageHelper.is_cyrillic_vowel(last1)): 
                    k += 1
        elif (wf.class0_.is_adjective and wf.number == MorphNumber.PLURAL): 
            last = wf.normal_case[len(wf.normal_case) - 1]
            last1 = wf.normal_case[len(wf.normal_case) - 2]
            if (last == 'Й' or last == 'Е'): 
                k += 1
        return k
    
    def __calc_eq_coef(self, v : 'MorphRuleVariant', wf : 'MorphWordForm') -> int:
        if (wf.class0_.value != (0)): 
            if ((((v.class0_.value) & (wf.class0_.value))) == 0): 
                return -1
        if (v.misc_info_id != wf.misc.id0_): 
            vi = self.get_misc_info(v.misc_info_id)
            if (vi.mood != MorphMood.UNDEFINED and wf.misc.mood != MorphMood.UNDEFINED): 
                if (vi.mood != wf.misc.mood): 
                    return -1
            if (vi.tense != MorphTense.UNDEFINED and wf.misc.tense != MorphTense.UNDEFINED): 
                if (((vi.tense) & (wf.misc.tense)) == (MorphTense.UNDEFINED)): 
                    return -1
            if (vi.voice != MorphVoice.UNDEFINED and wf.misc.voice != MorphVoice.UNDEFINED): 
                if (vi.voice != wf.misc.voice): 
                    return -1
            if (vi.person != MorphPerson.UNDEFINED and wf.misc.person != MorphPerson.UNDEFINED): 
                if (((vi.person) & (wf.misc.person)) == (MorphPerson.UNDEFINED)): 
                    return -1
            return 0
        if (not v.check_accord(wf, False, False)): 
            return -1
        return 1
    
    def __sort(self, res : typing.List['MorphWordForm'], word : str) -> None:
        if (res is None or (len(res) < 2)): 
            return
        k = 0
        while k < len(res): 
            ch = False
            i = 0
            while i < (len(res) - 1): 
                j = self.__compare(res[i], res[i + 1])
                if (j > 0): 
                    r1 = res[i]
                    r2 = res[i + 1]
                    res[i] = r2
                    res[i + 1] = r1
                    ch = True
                i += 1
            if (not ch): 
                break
            k += 1
        i = 0
        while i < (len(res) - 1): 
            j = i + 1
            first_pass3481 = True
            while True:
                if first_pass3481: first_pass3481 = False
                else: j += 1
                if (not (j < len(res))): break
                if (self.__comp1(res[i], res[j])): 
                    if ((res[i].class0_.is_adjective and res[j].class0_.is_noun and not res[j].is_in_dictionary) and not res[i].is_in_dictionary): 
                        del res[j]
                    elif ((res[i].class0_.is_noun and res[j].class0_.is_adjective and not res[j].is_in_dictionary) and not res[i].is_in_dictionary): 
                        del res[i]
                    elif (res[i].class0_.is_adjective and res[j].class0_.is_pronoun): 
                        del res[i]
                    elif (res[i].class0_.is_pronoun and res[j].class0_.is_adjective): 
                        if (res[j].normal_full == "ОДИН" or res[j].normal_case == "ОДИН"): 
                            continue
                        del res[j]
                    else: 
                        continue
                    i -= 1
                    break
            i += 1
    
    def __comp1(self, r1 : 'MorphWordForm', r2 : 'MorphWordForm') -> bool:
        if (r1.number != r2.number or r1.gender != r2.gender): 
            return False
        if (r1.case_ != r2.case_): 
            return False
        if (r1.normal_case != r2.normal_case): 
            return False
        return True
    
    def deserialize(self, str0 : io.IOBase, ignore_rev_tree : bool, lazy_load : bool) -> None:
        tmp = io.BytesIO()
        MorphDeserializer.deflate_gzip(str0, tmp)
        arr = bytearray(tmp.getvalue())
        buf = ByteArrayWrapper(arr)
        pos = 0
        wrappos23 = RefOutArgWrapper(pos)
        cou = buf.deserialize_int(wrappos23)
        pos = wrappos23.value
        while cou > 0: 
            mi = MorphMiscInfo()
            wrappos15 = RefOutArgWrapper(pos)
            mi._deserialize(buf, wrappos15)
            pos = wrappos15.value
            self.add_misc_info(mi)
            cou -= 1
        wrappos22 = RefOutArgWrapper(pos)
        cou = buf.deserialize_int(wrappos22)
        pos = wrappos22.value
        while cou > 0: 
            wrappos17 = RefOutArgWrapper(pos)
            p1 = buf.deserialize_int(wrappos17)
            pos = wrappos17.value
            r = MorphRule()
            if (lazy_load): 
                r.lazy_pos = pos
                pos = p1
            else: 
                wrappos16 = RefOutArgWrapper(pos)
                r._deserialize(buf, wrappos16)
                pos = wrappos16.value
            self.add_rule(r)
            cou -= 1
        root = MorphTreeNode()
        if (lazy_load): 
            wrappos18 = RefOutArgWrapper(pos)
            root._deserialize_lazy(buf, self, wrappos18)
            pos = wrappos18.value
        else: 
            wrappos19 = RefOutArgWrapper(pos)
            root._deserialize(buf, wrappos19)
            pos = wrappos19.value
        self.m_root = root
        if (not ignore_rev_tree): 
            root_rev = MorphTreeNode()
            if (lazy_load): 
                wrappos20 = RefOutArgWrapper(pos)
                root_rev._deserialize_lazy(buf, self, wrappos20)
                pos = wrappos20.value
            else: 
                wrappos21 = RefOutArgWrapper(pos)
                root_rev._deserialize(buf, wrappos21)
                pos = wrappos21.value
            self.m_root_reverce = root_rev
        tmp.close()
        if (lazy_load): 
            self.__m_lazy_buf = buf