# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import threading
import io
import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.morph.internal.MorphTreeNode import MorphTreeNode
from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber


class MorphEngine:
    
    def __init__(self) -> None:
        from pullenti.morph.MorphLang import MorphLang
        self._m_lock = threading.Lock()
        self.language = MorphLang()
        self.m_root = MorphTreeNode()
        self.m_root_reverce = MorphTreeNode()
        self._m_vars_hash = dict()
        self._m_vars = list()
        self.m_rules = list()
    
    def initialize(self, lang : 'MorphLang') -> bool:
        if (not self.language.is_undefined): 
            return False
        with self._m_lock: 
            if (not self.language.is_undefined): 
                return False
            self.language = lang
            # ignored: assembly = .
            rsname = "m_{0}.dat".format(str(lang))
            names = Utils.getResourcesNames('pullenti.morph.internal.properties', '.dat')
            for n in names: 
                if (n.upper().endswith(rsname.upper())): 
                    inf = Utils.getResourceInfo('pullenti.morph.internal.properties', n)
                    if (inf is None): 
                        continue
                    with Utils.getResourceStream('pullenti.morph.internal.properties', n) as stream: 
                        stream.seek(0, io.SEEK_SET)
                        MorphSerializeHelper.deserialize_all(stream, self, False, True)
                    return True
            return False
    
    def process(self, word : str) -> typing.List['MorphWordForm']:
        """ Обработка одного слова
        
        Args:
            word(str): слово должно быть в верхнем регистре
        
        """
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.morph.MorphClass import MorphClass
        if (Utils.isNullOrEmpty(word)): 
            return None
        res = None
        if (len(word) > 1): 
            for i in range(len(word)):
                ch = word[i]
                if (LanguageHelper.is_cyrillic_vowel(ch) or LanguageHelper.is_latin_vowel(ch)): 
                    break
            else: i = len(word)
            if (i >= len(word)): 
                return res
        mvs = [ ]
        tn = self.m_root
        i = 0
        while i <= len(word): 
            if (tn._lazy is not None): 
                tn._load()
            if (tn.rules is not None): 
                word_begin = None
                word_end = None
                if (i == 0): 
                    word_end = word
                elif (i < len(word)): 
                    word_end = word[i : ]
                else: 
                    word_end = ""
                if (res is None): 
                    res = list()
                for r in tn.rules: 
                    inoutarg15 = RefOutArgWrapper(None)
                    inoutres16 = Utils.tryGetValue(r.variants, word_end, inoutarg15)
                    mvs = inoutarg15.value
                    if (inoutres16): 
                        if (word_begin is None): 
                            if (i == len(word)): 
                                word_begin = word
                            elif (i > 0): 
                                word_begin = word[0 : (i)]
                            else: 
                                word_begin = ""
                        r.process_result(res, word_begin, mvs)
            if (tn.nodes is None or i >= len(word)): 
                break
            ch = ord(word[i])
            inoutarg17 = RefOutArgWrapper(None)
            inoutres18 = Utils.tryGetValue(tn.nodes, ch, inoutarg17)
            tn = inoutarg17.value
            if (not inoutres18): 
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
            for j in range(len(word)):
                if (LanguageHelper.is_cyrillic_vowel(word[j])): 
                    gl += 1
                else: 
                    sog += 1
            if ((gl < 2) or (sog < 2)): 
                need_test_unknown_vars = False
        if (need_test_unknown_vars and res is not None and len(res) == 1): 
            if (res[0].class0_.is_verb): 
                if ("н.вр." in res[0].misc.attrs and "нес.в." in res[0].misc.attrs and not "страд.з." in res[0].misc.attrs): 
                    need_test_unknown_vars = False
                elif ("б.вр." in res[0].misc.attrs and "сов.в." in res[0].misc.attrs): 
                    need_test_unknown_vars = False
                elif (res[0].normal_case is not None and LanguageHelper.ends_with(res[0].normal_case, "СЯ")): 
                    need_test_unknown_vars = False
            if (res[0].class0_.is_undefined and "прдктв." in res[0].misc.attrs): 
                need_test_unknown_vars = False
        if (need_test_unknown_vars): 
            if (self.m_root_reverce is None): 
                return res
            tn = self.m_root_reverce
            tn0 = None
            for i in range(len(word) - 1, -1, -1):
                if (tn._lazy is not None): 
                    tn._load()
                ch = ord(word[i])
                if (tn.nodes is None): 
                    break
                inoutarg19 = RefOutArgWrapper(None)
                inoutres20 = Utils.tryGetValue(tn.nodes, ch, inoutarg19)
                next0_ = inoutarg19.value
                if (not inoutres20): 
                    break
                tn = next0_
                if (tn._lazy is not None): 
                    tn._load()
                if (tn.reverce_variants is not None): 
                    tn0 = tn
                    break
            else: i = -1
            if (tn0 is not None): 
                glas = i < 4
                while i >= 0: 
                    if (LanguageHelper.is_cyrillic_vowel(word[i]) or LanguageHelper.is_latin_vowel(word[i])): 
                        glas = True
                        break
                    i -= 1
                if (glas): 
                    for mv in tn0.reverce_variants: 
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
                        r = MorphWordForm(mv, word)
                        if (not MorphWordForm._has_morph_equals(res, r)): 
                            r.undef_coef = mv.coef
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
        MorphEngine.__sort(res, word)
        for v in res: 
            if (v.normal_case is None): 
                v.normal_case = word
            if (v.class0_.is_verb): 
                if (v.normal_full is None and LanguageHelper.ends_with(v.normal_case, "ТЬСЯ")): 
                    v.normal_full = v.normal_case[0 : (len(v.normal_case) - 2)]
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
                if (r.undef_coef > 100 and r.class0_ == MorphClass.ADJECTIVE): 
                    r.undef_coef = 0
        if (len(res) == 0): 
            return None
        return res
    
    def get_all_wordforms(self, word : str) -> typing.List['MorphWordForm']:
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.morph.MorphClass import MorphClass
        res = list()
        tn = self.m_root
        i = 0
        while i <= len(word): 
            if (tn._lazy is not None): 
                tn._load()
            if (tn.rules is not None): 
                word_begin = ""
                word_end = ""
                if (i > 0): 
                    word_begin = word[0 : (i)]
                else: 
                    word_end = word
                if (i < len(word)): 
                    word_end = word[i : ]
                else: 
                    word_begin = word
                for r in tn.rules: 
                    if (word_end in r.variants): 
                        for vl in r.variants_list: 
                            for v in vl: 
                                wf = MorphWordForm(v, None)
                                if (not MorphWordForm._has_morph_equals(res, wf)): 
                                    wf.normal_case = (word_begin + v.tail)
                                    wf.undef_coef = 0
                                    res.append(wf)
            if (tn.nodes is None or i >= len(word)): 
                break
            ch = ord(word[i])
            inoutarg21 = RefOutArgWrapper(None)
            inoutres22 = Utils.tryGetValue(tn.nodes, ch, inoutarg21)
            tn = inoutarg21.value
            if (not inoutres22): 
                break
            i += 1
        i = 0
        first_pass2669 = True
        while True:
            if first_pass2669: first_pass2669 = False
            else: i += 1
            if (not (i < len(res))): break
            wf = res[i]
            if (wf.contains_attr("инф.", MorphClass())): 
                continue
            j = i + 1
            first_pass2670 = True
            while True:
                if first_pass2670: first_pass2670 = False
                else: j += 1
                if (not (j < len(res))): break
                wf1 = res[j]
                if (wf1.contains_attr("инф.", MorphClass())): 
                    continue
                if ((wf.class0_ == wf1.class0_ and wf.gender == wf1.gender and wf.number == wf1.number) and wf.normal_case == wf1.normal_case): 
                    wf.case |= wf1.case
                    del res[j]
                    j -= 1
        i = 0
        first_pass2671 = True
        while True:
            if first_pass2671: first_pass2671 = False
            else: i += 1
            if (not (i < len(res))): break
            wf = res[i]
            if (wf.contains_attr("инф.", MorphClass())): 
                continue
            j = i + 1
            first_pass2672 = True
            while True:
                if first_pass2672: first_pass2672 = False
                else: j += 1
                if (not (j < len(res))): break
                wf1 = res[j]
                if (wf1.contains_attr("инф.", MorphClass())): 
                    continue
                if ((wf.class0_ == wf1.class0_ and wf.case == wf1.case and wf.number == wf1.number) and wf.normal_case == wf1.normal_case): 
                    wf.gender |= wf1.gender
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
            if (tn._lazy is not None): 
                tn._load()
            if (tn.rules is not None): 
                word_begin = ""
                word_end = ""
                if (i > 0): 
                    word_begin = word[0 : (i)]
                else: 
                    word_end = word
                if (i < len(word)): 
                    word_end = word[i : ]
                else: 
                    word_begin = word
                for r in tn.rules: 
                    if (word_end in r.variants): 
                        for li in r.variants_list: 
                            for v in li: 
                                if (((cla.value & v.class0_.value)) != 0 and v.normal_tail is not None): 
                                    if (cas.is_undefined): 
                                        if (v.case.is_nominative or v.case.is_undefined): 
                                            pass
                                        else: 
                                            continue
                                    elif ((v.case & cas).is_undefined): 
                                        continue
                                    sur = cla.is_proper_surname
                                    sur0 = v.class0_.is_proper_surname
                                    if (sur or sur0): 
                                        if (sur != sur0): 
                                            continue
                                    find = True
                                    if (gender != MorphGender.UNDEFINED): 
                                        if (((gender & v.gender)) == MorphGender.UNDEFINED): 
                                            continue
                                    if (num != MorphNumber.UNDEFINED): 
                                        if (((num & v.number)) == MorphNumber.UNDEFINED): 
                                            continue
                                    re = word_begin + v.tail
                                    co = 0
                                    if (add_info is not None): 
                                        co = v.calc_eq_coef(add_info)
                                    if (res is None or co > max_coef): 
                                        res = re
                                        max_coef = co
                                    if (max_coef == 0): 
                                        if ((word_begin + v.normal_tail) == word): 
                                            return re
            if (tn.nodes is None or i >= len(word)): 
                break
            ch = ord(word[i])
            inoutarg23 = RefOutArgWrapper(None)
            inoutres24 = Utils.tryGetValue(tn.nodes, ch, inoutarg23)
            tn = inoutarg23.value
            if (not inoutres24): 
                break
            i += 1
        if (find): 
            return res
        tn = self.m_root_reverce
        tn0 = None
        for i in range(len(word) - 1, -1, -1):
            if (tn._lazy is not None): 
                tn._load()
            ch = ord(word[i])
            if (tn.nodes is None): 
                break
            inoutarg25 = RefOutArgWrapper(None)
            inoutres26 = Utils.tryGetValue(tn.nodes, ch, inoutarg25)
            next0_ = inoutarg25.value
            if (not inoutres26): 
                break
            tn = next0_
            if (tn._lazy is not None): 
                tn._load()
            if (tn.reverce_variants is not None): 
                tn0 = tn
                break
        else: i = -1
        if (tn0 is None): 
            return None
        for mv in tn0.reverce_variants: 
            if (((mv.class0_.value & cla.value)) != 0 and mv.rule is not None): 
                if (len(mv.tail) > 0 and not LanguageHelper.ends_with(word, mv.tail)): 
                    continue
                word_begin = word[0 : (len(word) - len(mv.tail))]
                for liv in mv.rule.variants_list: 
                    for v in liv: 
                        if (((v.class0_.value & cla.value)) != 0): 
                            sur = cla.is_proper_surname
                            sur0 = v.class0_.is_proper_surname
                            if (sur or sur0): 
                                if (sur != sur0): 
                                    continue
                            if (not cas.is_undefined): 
                                if ((cas & v.case).is_undefined and not v.case.is_undefined): 
                                    continue
                            if (num != MorphNumber.UNDEFINED): 
                                if (v.number != MorphNumber.UNDEFINED): 
                                    if (((v.number & num)) == MorphNumber.UNDEFINED): 
                                        continue
                            if (gender != MorphGender.UNDEFINED): 
                                if (v.gender != MorphGender.UNDEFINED): 
                                    if (((v.gender & gender)) == MorphGender.UNDEFINED): 
                                        continue
                            res = (word_begin + v.tail)
                            if (res == word): 
                                return word
                            return res
        if (cla.is_proper_surname): 
            if ((gender == MorphGender.FEMINIE and cla.is_proper_surname and not cas.is_undefined) and not cas.is_nominative): 
                if (word.endswith("ВА") or word.endswith("НА")): 
                    if (cas.is_accusative): 
                        return word[0 : (len(word) - 1)] + "У"
                    return word[0 : (len(word) - 1)] + "ОЙ"
            if (gender == MorphGender.FEMINIE): 
                last = word[len(word) - 1]
                if (last == 'А' or last == 'Я' or last == 'О'): 
                    return word
                if (LanguageHelper.is_cyrillic_vowel(last)): 
                    return word[0 : (len(word) - 1)] + "А"
                elif (last == 'Й'): 
                    return word[0 : (len(word) - 2)] + "АЯ"
                else: 
                    return word + "А"
        return res
    
    def correct_word_by_morph(self, word : str) -> str:
        vars0_ = list()
        tmp = Utils.newStringIO(len(word))
        for ch in range(1, len(word), 1):
            Utils.setLengthStringIO(tmp, 0)
            print(word, end="", file=tmp)
            Utils.setCharAtStringIO(tmp, ch, '*')
            var = self.__check_corr_var(Utils.toStringStringIO(tmp), self.m_root, 0)
            if (var is not None): 
                if (not var in vars0_): 
                    vars0_.append(var)
        if (len(vars0_) == 0): 
            for ch in range(1, len(word), 1):
                Utils.setLengthStringIO(tmp, 0)
                print(word, end="", file=tmp)
                Utils.insertStringIO(tmp, ch, '*')
                var = self.__check_corr_var(Utils.toStringStringIO(tmp), self.m_root, 0)
                if (var is not None): 
                    if (not var in vars0_): 
                        vars0_.append(var)
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
        first_pass2673 = True
        while True:
            if first_pass2673: first_pass2673 = False
            else: i += 1
            if (not (i <= len(word))): break
            if (tn._lazy is not None): 
                tn._load()
            if (tn.rules is not None): 
                word_begin = ""
                word_end = ""
                if (i > 0): 
                    word_begin = word[0 : (i)]
                else: 
                    word_end = word
                if (i < len(word)): 
                    word_end = word[i : ]
                else: 
                    word_begin = word
                for r in tn.rules: 
                    if (word_end in r.variants): 
                        return word_begin + word_end
                    if (('*') in word_end): 
                        for v in r.variants_key: 
                            if (len(v) == len(word_end)): 
                                for j in range(len(v)):
                                    if (word_end[j] == '*' or word_end[j] == v[j]): 
                                        pass
                                    else: 
                                        break
                                else: j = len(v)
                                if (j >= len(v)): 
                                    return word_begin + v
            if (tn.nodes is None or i >= len(word)): 
                break
            ch = ord(word[i])
            if (ch != 0x2A): 
                inoutarg27 = RefOutArgWrapper(None)
                inoutres28 = Utils.tryGetValue(tn.nodes, ch, inoutarg27)
                tn = inoutarg27.value
                if (inoutres28): 
                    continue
                break
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
        from pullenti.morph.MorphWordForm import MorphWordForm
        tn = self.m_root_reverce
        tn0 = None
        nodes_with_vars = None
        for i in range(len(word) - 1, -1, -1):
            if (tn._lazy is not None): 
                tn._load()
            ch = ord(word[i])
            if (tn.nodes is None): 
                break
            inoutarg29 = RefOutArgWrapper(None)
            inoutres30 = Utils.tryGetValue(tn.nodes, ch, inoutarg29)
            next0_ = inoutarg29.value
            if (not inoutres30): 
                break
            tn = next0_
            if (tn._lazy is not None): 
                tn._load()
            if (tn.reverce_variants is not None): 
                if (nodes_with_vars is None): 
                    nodes_with_vars = list()
                nodes_with_vars.append(tn)
                tn0 = tn
        else: i = -1
        if (nodes_with_vars is None): 
            return
        for j in range(len(nodes_with_vars) - 1, -1, -1):
            tn = nodes_with_vars[j]
            if (tn._lazy is not None): 
                tn._load()
            ok = False
            for v in tn.reverce_variants: 
                if (geo and v.class0_.is_proper_geo): 
                    pass
                elif (not geo and v.class0_.is_proper_surname): 
                    pass
                else: 
                    continue
                r = MorphWordForm(v, word)
                if (not MorphWordForm._has_morph_equals(res, r)): 
                    r.undef_coef = v.coef
                    res.append(r)
                ok = True
            if (ok): 
                break
    
    @staticmethod
    def __compare(x : 'MorphWordForm', y : 'MorphWordForm') -> int:
        if (x.is_in_dictionary and not y.is_in_dictionary): 
            return -1
        if (not x.is_in_dictionary and y.is_in_dictionary): 
            return 1
        if (x.undef_coef > 0): 
            if (x.undef_coef > (y.undef_coef * 2)): 
                return -1
            if ((x.undef_coef * 2) < y.undef_coef): 
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
        cx = MorphEngine.__calc_coef(x)
        cy = MorphEngine.__calc_coef(y)
        if (cx > cy): 
            return -1
        if (cx < cy): 
            return 1
        if (x.number == MorphNumber.PLURAL and y.number != MorphNumber.PLURAL): 
            return 1
        if (y.number == MorphNumber.PLURAL and x.number != MorphNumber.PLURAL): 
            return -1
        return 0
    
    @staticmethod
    def __calc_coef(wf : 'MorphWordForm') -> int:
        k = 0
        if (not wf.case.is_undefined): 
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
    
    @staticmethod
    def __sort(res : typing.List['MorphWordForm'], word : str) -> None:
        if (res is None or (len(res) < 2)): 
            return
        for k in range(len(res)):
            ch = False
            i = 0
            while i < (len(res) - 1): 
                j = MorphEngine.__compare(res[i], res[i + 1])
                if (j > 0): 
                    r = res[i]
                    res[i] = res[i + 1]
                    res[i + 1] = r
                    ch = True
                i += 1
            if (not ch): 
                break
        i = 0
        while i < (len(res) - 1): 
            j = i + 1
            first_pass2674 = True
            while True:
                if first_pass2674: first_pass2674 = False
                else: j += 1
                if (not (j < len(res))): break
                if (MorphEngine.__comp1(res[i], res[j])): 
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
    
    @staticmethod
    def __comp1(r1 : 'MorphWordForm', r2 : 'MorphWordForm') -> bool:
        if (r1.number != r2.number or r1.gender != r2.gender): 
            return False
        if (r1.case != r2.case): 
            return False
        if (r1.normal_case != r2.normal_case): 
            return False
        return True
    
    def register_morph_info(self, var : 'MorphMiscInfo') -> 'MorphMiscInfo':
        key = str(var)
        inoutarg31 = RefOutArgWrapper(None)
        inoutres32 = Utils.tryGetValue(self._m_vars_hash, key, inoutarg31)
        v = inoutarg31.value
        if (inoutres32): 
            return v
        self._m_vars_hash[key] = var
        self._m_vars.append(var)
        return var
    
    def _reset(self) -> None:
        from pullenti.morph.MorphLang import MorphLang
        self.m_root = MorphTreeNode()
        self.m_root_reverce = MorphTreeNode()
        self._m_vars = list()
        self._m_vars_hash = dict()
        self.language = MorphLang()