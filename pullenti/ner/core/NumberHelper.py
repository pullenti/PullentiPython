# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import math
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender


class NumberHelper:
    """ Работа с числовыми значениями """
    
    @staticmethod
    def _try_parse(token : 'Token') -> 'NumberToken':
        """ Попробовать создать числительное
        
        Args:
            token(Token): 
        
        """
        return NumberHelper.__try_parse(token, -1)
    
    @staticmethod
    def __try_parse(token : 'Token', prev_val : int=-1) -> 'NumberToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.MorphCollection import MorphCollection
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.morph.MorphClass import MorphClass
        if (isinstance(token, NumberToken)): 
            return (token if isinstance(token, NumberToken) else None)
        tt = (token if isinstance(token, TextToken) else None)
        if (tt is None): 
            return None
        et = tt
        val = -1
        typ = NumberSpellingType.DIGIT
        term = tt.term
        if (term[0].isdigit()): 
            inoutarg555 = RefOutArgWrapper(None)
            inoutres556 = Utils.tryParseInt(term, inoutarg555)
            val = inoutarg555.value
            if (not inoutres556): 
                return None
        if (val >= 0): 
            hiph = False
            if (isinstance(et.next0, TextToken) and et.next0.is_hiphen): 
                if ((et.whitespaces_after_count < 2) and (et.next0.whitespaces_after_count < 2)): 
                    et = (et.next0 if isinstance(et.next0, TextToken) else None)
                    hiph = True
            mc = None
            if (hiph or not et.is_whitespace_after): 
                rr = NumberHelper.__analize_number_tail(et.next0 if isinstance(et.next0, TextToken) else None, val)
                if (rr is None): 
                    et = tt
                else: 
                    mc = rr.morph
                    et = (rr.end_token if isinstance(rr.end_token, TextToken) else None)
            else: 
                et = tt
            if (et.next0 is not None and et.next0.is_char('(')): 
                num2 = NumberHelper._try_parse(et.next0.next0)
                if ((num2 is not None and num2.value == val and num2.end_token.next0 is not None) and num2.end_token.next0.is_char(')')): 
                    et = (num2.end_token.next0 if isinstance(num2.end_token.next0, TextToken) else None)
            while isinstance(et.next0, TextToken) and not ((isinstance(et.previous, NumberToken))) and et.is_whitespace_before:
                if (et.whitespaces_after_count != 1): 
                    break
                sss = (et.next0 if isinstance(et.next0, TextToken) else None).term
                if (sss == "000"): 
                    val *= 1000
                    et = (et.next0 if isinstance(et.next0, TextToken) else None)
                    continue
                if (sss[0].isdigit() and len(sss) == 3): 
                    val2 = val
                    ttt = et.next0
                    first_pass2605 = True
                    while True:
                        if first_pass2605: first_pass2605 = False
                        else: ttt = ttt.next0
                        if (not (ttt is not None)): break
                        ss = ttt.get_source_text()
                        if (ttt.whitespaces_before_count == 1 and ttt.length_char == 3 and ss[0].isdigit()): 
                            inoutarg557 = RefOutArgWrapper(None)
                            inoutres558 = Utils.tryParseInt(ss, inoutarg557)
                            ii = inoutarg557.value
                            if (not inoutres558): 
                                break
                            val2 *= 1000
                            val2 += ii
                            continue
                        if ((ttt.is_char_of(".,") and not ttt.is_whitespace_before and not ttt.is_whitespace_after) and ttt.next0 is not None and ttt.next0.get_source_text()[0].isdigit()): 
                            if (ttt.next0.is_whitespace_after and isinstance(ttt.previous, TextToken)): 
                                et = (ttt.previous if isinstance(ttt.previous, TextToken) else None)
                                val = val2
                                break
                        break
                break
            for k in range(3):
                if (isinstance(et.next0, TextToken) and et.next0.chars.is_letter): 
                    tt = (et.next0 if isinstance(et.next0, TextToken) else None)
                    t0 = et
                    coef = 0
                    if (k == 0): 
                        coef = 1000000000
                        if (tt.is_value("МИЛЛИАРД", "МІЛЬЯРД") or tt.is_value("BILLION", None) or tt.is_value("BN", None)): 
                            et = tt
                            val *= coef
                        elif (tt.is_value("МЛРД", None)): 
                            et = tt
                            val *= coef
                            if (isinstance(et.next0, TextToken) and et.next0.is_char('.')): 
                                et = (et.next0 if isinstance(et.next0, TextToken) else None)
                        else: 
                            continue
                    elif (k == 1): 
                        coef = 1000000
                        if (tt.is_value("МИЛЛИОН", "МІЛЬЙОН") or tt.is_value("MILLION", None)): 
                            et = tt
                            val *= coef
                        elif (tt.is_value("МЛН", None)): 
                            et = tt
                            val *= coef
                            if (isinstance(et.next0, TextToken) and et.next0.is_char('.')): 
                                et = (et.next0 if isinstance(et.next0, TextToken) else None)
                        elif (isinstance(tt, TextToken) and (tt if isinstance(tt, TextToken) else None).term == "M"): 
                            if (NumberHelper._is_money_char(et.previous) is not None): 
                                et = tt
                                val *= coef
                            else: 
                                break
                        else: 
                            continue
                    else: 
                        coef = 1000
                        if (tt.is_value("ТЫСЯЧА", "ТИСЯЧА") or tt.is_value("THOUSAND", None)): 
                            et = tt
                            val *= coef
                        elif (tt.is_value("ТЫС", None) or tt.is_value("ТИС", None)): 
                            et = tt
                            val *= coef
                            if (isinstance(et.next0, TextToken) and et.next0.is_char('.')): 
                                et = (et.next0 if isinstance(et.next0, TextToken) else None)
                        else: 
                            break
                    if (((t0 == token and t0.length_char <= 3 and t0.previous is not None) and not t0.is_whitespace_before and t0.previous.is_char_of(",.")) and not t0.previous.is_whitespace_before and ((isinstance(t0.previous.previous, NumberToken) or prev_val >= 0))): 
                        if (t0.length_char == 1): 
                            val = math.floor(val / 10)
                        elif (t0.length_char == 2): 
                            val = math.floor(val / 100)
                        else: 
                            val = math.floor(val / 1000)
                        if (isinstance(t0.previous.previous, NumberToken)): 
                            val += ((t0.previous.previous if isinstance(t0.previous.previous, NumberToken) else None).value * coef)
                        else: 
                            val += (prev_val * coef)
                        token = t0.previous.previous
                    next0 = NumberHelper.__try_parse(et.next0, -1)
                    if (next0 is None or next0.value >= coef): 
                        break
                    tt1 = next0.end_token
                    if ((isinstance(tt1.next0, TextToken) and not tt1.is_whitespace_after and tt1.next0.is_char_of(".,")) and not tt1.next0.is_whitespace_after): 
                        re1 = NumberHelper.__try_parse(tt1.next0.next0, next0.value)
                        if (re1 is not None and re1.begin_token == next0.begin_token): 
                            next0 = re1
                    val += next0.value
                    et = (next0.end_token if isinstance(next0.end_token, TextToken) else None)
                    break
            res = NumberToken._new559(token, et, val, typ, mc)
            if (et.next0 is not None and (res.value < 1000) and ((et.next0.is_hiphen or et.next0.is_value("ДО", None)))): 
                tt1 = et.next0.next0
                first_pass2606 = True
                while True:
                    if first_pass2606: first_pass2606 = False
                    else: tt1 = tt1.next0
                    if (not (tt1 is not None)): break
                    if (not ((isinstance(tt1, TextToken)))): 
                        break
                    if ((tt1 if isinstance(tt1, TextToken) else None).term[0].isdigit()): 
                        continue
                    if (tt1.is_char_of(",.") or NumberHelper._is_money_char(tt1) is not None): 
                        continue
                    if (tt1.is_value("МИЛЛИОН", "МІЛЬЙОН") or tt1.is_value("МЛН", None) or tt1.is_value("MILLION", None)): 
                        res.value *= 1000000
                    elif ((tt1.is_value("МИЛЛИАРД", "МІЛЬЯРД") or tt1.is_value("МЛРД", None) or tt1.is_value("BILLION", None)) or tt1.is_value("BN", None)): 
                        res.value *= 1000000000
                    elif (tt1.is_value("ТЫСЯЧА", "ТИСЯЧА") or tt1.is_value("ТЫС", "ТИС") or tt1.is_value("THOUSAND", None)): 
                        res.value *= 1000
                    break
            return res
        val = 0
        et = None
        loc_value = 0
        is_adj = False
        jprev = -1
        t = tt
        while t is not None: 
            if (t != tt and t.newlines_before_count > 1): 
                break
            term = t.term
            if (not term[0].isalpha()): 
                break
            num = NumberHelper._m_nums.try_parse(t, TerminParseAttr.FULLWORDSONLY)
            if (num is None): 
                break
            j = num.termin.tag
            if (jprev > 0 and (jprev < 20) and (j < 20)): 
                break
            is_adj = ((j & NumberHelper.__pril_num_tag_bit)) != 0
            j &= (~ NumberHelper.__pril_num_tag_bit)
            if (is_adj and t != tt): 
                if ((t.is_value("ДЕСЯТЫЙ", None) or t.is_value("СОТЫЙ", None) or t.is_value("ТЫСЯЧНЫЙ", None)) or t.is_value("ДЕСЯТИТЫСЯЧНЫЙ", None) or t.is_value("МИЛЛИОННЫЙ", None)): 
                    break
            if (j >= 1000): 
                if (loc_value == 0): 
                    loc_value = 1
                val += (loc_value * j)
                loc_value = 0
            else: 
                if (loc_value > 0 and loc_value <= j): 
                    break
                loc_value += j
            et = t
            if (j == 1000 or j == 1000000): 
                if (isinstance(et.next0, TextToken) and et.next0.is_char('.')): 
                    et = (et.next0 if isinstance(et.next0, TextToken) else None)
                    t = et
            jprev = j
            t = (t.next0 if isinstance(t.next0, TextToken) else None)
        if (loc_value > 0): 
            val += loc_value
        if (val == 0 or et is None): 
            return None
        nt = NumberToken(tt, et, val, NumberSpellingType.WORDS)
        if (et.morph is not None): 
            nt.morph = MorphCollection(et.morph)
            for wff in et.morph.items: 
                wf = (wff if isinstance(wff, MorphWordForm) else None)
                if (wf is not None and wf.misc is not None and "собир." in wf.misc.attrs): 
                    nt.morph.class0 = MorphClass.NOUN
                    break
            if (not is_adj): 
                nt.morph.remove_items(MorphClass.ADJECTIVE | MorphClass.NOUN, False)
                if (nt.morph.class0.is_undefined): 
                    nt.morph.class0 = MorphClass.NOUN
            if (et.chars.is_latin_letter and is_adj): 
                nt.morph.class0 = MorphClass.ADJECTIVE
        return nt
    
    @staticmethod
    def try_parse_roman(t : 'Token') -> 'NumberToken':
        """ Попробовать выделить римскую цифру
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        if (isinstance(t, NumberToken)): 
            return (t if isinstance(t, NumberToken) else None)
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None or not t.chars.is_letter): 
            return None
        term = tt.term
        if (not NumberHelper.__is_rom_val(term)): 
            return None
        if (tt.morph.class0.is_preposition): 
            if (tt.chars.is_all_lower): 
                return None
        res = NumberToken(t, t, 0, NumberSpellingType.ROMAN)
        nums = list()
        while t is not None: 
            if (t != res.begin_token and t.is_whitespace_before): 
                break
            if (not ((isinstance(t, TextToken)))): 
                break
            term = (t if isinstance(t, TextToken) else None).term
            if (not NumberHelper.__is_rom_val(term)): 
                break
            for s in term: 
                i = NumberHelper.__rom_val(s)
                if (i > 0): 
                    nums.append(i)
            res.end_token = t
            t = t.next0
        if (len(nums) == 0): 
            return None
        i = 0
        while i < len(nums): 
            if ((i + 1) < len(nums)): 
                if (nums[i] == 1 and nums[i + 1] == 5): 
                    res.value += 4
                    i += 1
                elif (nums[i] == 1 and nums[i + 1] == 10): 
                    res.value += 9
                    i += 1
                elif (nums[i] == 10 and nums[i + 1] == 50): 
                    res.value += 40
                    i += 1
                elif (nums[i] == 10 and nums[i + 1] == 100): 
                    res.value += 90
                    i += 1
                else: 
                    res.value += nums[i]
            else: 
                res.value += nums[i]
            i += 1
        hiph = False
        et = res.end_token.next0
        if (et is None): 
            return res
        if (et.next0 is not None and et.next0.is_hiphen): 
            et = et.next0
            hiph = True
        if (hiph or not et.is_whitespace_after): 
            mc = NumberHelper.__analize_number_tail(et.next0 if isinstance(et.next0, TextToken) else None, res.value)
            if (mc is not None): 
                res.end_token = mc.end_token
                res.morph = mc.morph
        if ((res.begin_token == res.end_token and res.value == 1 and res.begin_token.chars.is_all_lower) and res.begin_token.morph.language.is_ua): 
            return None
        return res
    
    @staticmethod
    def __rom_val(ch : 'char') -> int:
        if (ch == 'Х' or ch == 'X'): 
            return 10
        if (ch == 'І' or ch == 'I'): 
            return 1
        if (ch == 'V'): 
            return 5
        if (ch == 'L'): 
            return 50
        if (ch == 'C' or ch == 'С'): 
            return 100
        return 0
    
    @staticmethod
    def __is_rom_val(str0 : str) -> bool:
        for ch in str0: 
            if (NumberHelper.__rom_val(ch) < 1): 
                return False
        return True
    
    @staticmethod
    def try_parse_roman_back(token : 'Token') -> 'NumberToken':
        """ Выделить римскую цифру с token в обратном порядке
        
        Args:
            token(Token): 
        
        """
        t = token
        if (t is None): 
            return None
        if ((t.chars.is_all_lower and t.previous is not None and t.previous.is_hiphen) and t.previous.previous is not None): 
            t = token.previous.previous
        res = None
        while t is not None: 
            nt = NumberHelper.try_parse_roman(t)
            if (nt is not None): 
                if (nt.end_token == token): 
                    res = nt
                else: 
                    break
            if (t.is_whitespace_after): 
                break
            t = t.previous
        return res
    
    @staticmethod
    def try_parse_age(t : 'Token') -> 'NumberToken':
        """ Это выделение числительных типа 16-летие, 50-летний
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        if (t is None): 
            return None
        nt = (t if isinstance(t, NumberToken) else None)
        nt_next = None
        if (nt is not None): 
            nt_next = nt.next0
        else: 
            if (t.is_value("AGED", None) and isinstance(t.next0, NumberToken)): 
                return NumberToken(t, t.next0, (t.next0 if isinstance(t.next0, NumberToken) else None).value, NumberSpellingType.AGE)
            nt = NumberHelper.try_parse_roman(t)
            if ((nt) is not None): 
                nt_next = nt.end_token.next0
        if (nt is not None): 
            if (nt_next is not None): 
                t1 = nt_next
                if (t1.is_hiphen): 
                    t1 = t1.next0
                if (isinstance(t1, TextToken)): 
                    v = (t1 if isinstance(t1, TextToken) else None).term
                    if ((v == "ЛЕТ" or v == "ЛЕТИЯ" or v == "ЛЕТИЕ") or v == "РІЧЧЯ"): 
                        return NumberToken._new559(t, t1, nt.value, NumberSpellingType.AGE, t1.morph)
                    if (t1.is_value("ЛЕТНИЙ", "РІЧНИЙ")): 
                        return NumberToken._new559(t, t1, nt.value, NumberSpellingType.AGE, t1.morph)
                    if (v == "Л" or ((v == "Р" and nt.morph.language.is_ua))): 
                        return NumberToken(t, (t1.next0 if t1.next0 is not None and t1.next0.is_char('.') else t1), nt.value, NumberSpellingType.AGE)
            return None
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None): 
            return None
        s = tt.term
        if (LanguageHelper.ends_with_ex(s, "ЛЕТИЕ", "ЛЕТИЯ", "РІЧЧЯ", None)): 
            term = NumberHelper._m_nums.find(s[0 : (len(s) - 5)])
            if (term is not None): 
                return NumberToken._new559(tt, tt, term.tag, NumberSpellingType.AGE, tt.morph)
        s = tt.lemma
        if (LanguageHelper.ends_with_ex(s, "ЛЕТНИЙ", "РІЧНИЙ", None, None)): 
            term = NumberHelper._m_nums.find(s[0 : (len(s) - 6)])
            if (term is not None): 
                return NumberToken._new559(tt, tt, term.tag, NumberSpellingType.AGE, tt.morph)
        return None
    
    @staticmethod
    def try_parse_anniversary(t : 'Token') -> 'NumberToken':
        """ Выделение годовщин и летий (XX-летие) ... """
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        nt = (t if isinstance(t, NumberToken) else None)
        t1 = None
        if (nt is not None): 
            t1 = nt.next0
        else: 
            nt = NumberHelper.try_parse_roman(t)
            if ((nt) is None): 
                if (isinstance(t, TextToken)): 
                    v = (t if isinstance(t, TextToken) else None).term
                    num = 0
                    if (v.endswith("ЛЕТИЯ") or v.endswith("ЛЕТИЕ")): 
                        if (v.startswith("ВОСЕМЬСОТ") or v.startswith("ВОСЬМИСОТ")): 
                            num = 800
                    if (num > 0): 
                        return NumberToken(t, t, num, NumberSpellingType.AGE)
                return None
            t1 = nt.end_token.next0
        if (t1 is None): 
            return None
        if (t1.is_hiphen): 
            t1 = t1.next0
        if (isinstance(t1, TextToken)): 
            v = (t1 if isinstance(t1, TextToken) else None).term
            if ((v == "ЛЕТ" or v == "ЛЕТИЯ" or v == "ЛЕТИЕ") or t1.is_value("ГОДОВЩИНА", None)): 
                return NumberToken(t, t1, nt.value, NumberSpellingType.AGE)
            if (t1.morph.language.is_ua): 
                if (v == "РОКІВ" or v == "РІЧЧЯ" or t1.is_value("РІЧНИЦЯ", None)): 
                    return NumberToken(t, t1, nt.value, NumberSpellingType.AGE)
        return None
    
    __m_samples = None
    
    @staticmethod
    def __analize_number_tail(tt : 'TextToken', val : int) -> 'MetaToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphBaseInfo import MorphBaseInfo
        from pullenti.ner.MorphCollection import MorphCollection
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.ner.MetaToken import MetaToken
        from pullenti.morph.Morphology import Morphology
        if (not ((isinstance(tt, TextToken)))): 
            return None
        s = tt.term
        mc = None
        if (not tt.chars.is_letter): 
            if (((s == "<" or s == "(")) and isinstance(tt.next0, TextToken)): 
                s = (tt.next0 if isinstance(tt.next0, TextToken) else None).term
                if ((s == "TH" or s == "ST" or s == "RD") or s == "ND"): 
                    if (tt.next0.next0 is not None and tt.next0.next0.is_char_of(">)")): 
                        mc = MorphCollection()
                        mc.class0 = MorphClass.ADJECTIVE
                        mc.language = MorphLang.EN
                        return MetaToken._new564(tt, tt.next0.next0, mc)
            return None
        if ((s == "TH" or s == "ST" or s == "RD") or s == "ND"): 
            mc = MorphCollection()
            mc.class0 = MorphClass.ADJECTIVE
            mc.language = MorphLang.EN
            return MetaToken._new564(tt, tt, mc)
        if (not tt.chars.is_cyrillic_letter): 
            return None
        if (not tt.is_whitespace_after): 
            if (tt.next0 is not None and tt.next0.chars.is_letter): 
                return None
            if (tt.length_char == 1 and ((tt.is_value("X", None) or tt.is_value("Х", None)))): 
                return None
        if (not tt.chars.is_all_lower): 
            ss = (tt if isinstance(tt, TextToken) else None).term
            if (ss == "Я" or ss == "Й" or ss == "Е"): 
                pass
            elif (len(ss) == 2 and ((ss[1] == 'Я' or ss[1] == 'Й' or ss[1] == 'Е'))): 
                pass
            else: 
                return None
        if ((tt if isinstance(tt, TextToken) else None).term == "М"): 
            if (tt.previous is None or not tt.previous.is_hiphen): 
                return None
        dig = (val % 10)
        vars0 = Morphology.get_all_wordforms(NumberHelper.__m_samples[dig], MorphLang())
        if (vars0 is None or len(vars0) == 0): 
            return None
        for v in vars0: 
            if (v.class0.is_adjective and LanguageHelper.ends_with(v.normal_case, s) and v.number != MorphNumber.UNDEFINED): 
                if (mc is None): 
                    mc = MorphCollection()
                ok = False
                for it in mc.items: 
                    if (it.class0 == v.class0 and it.number == v.number and ((it.gender == v.gender or v.number == MorphNumber.PLURAL))): 
                        it.case |= v.case
                        ok = True
                        break
                if (not ok): 
                    mc.add_item(MorphBaseInfo(v))
        if (tt.morph.language.is_ua and mc is None and s == "Ї"): 
            mc = MorphCollection()
            mc.add_item(MorphBaseInfo._new566(MorphClass.ADJECTIVE))
        if (mc is not None): 
            return MetaToken._new564(tt, tt, mc)
        if ((((len(s) < 3) and not tt.is_whitespace_before and tt.previous is not None) and tt.previous.is_hiphen and not tt.previous.is_whitespace_before) and tt.whitespaces_after_count == 1 and s != "А"): 
            return MetaToken._new564(tt, tt, MorphCollection._new568(MorphClass.ADJECTIVE))
        return None
    
    @staticmethod
    def get_number_adjective(value : int, gender : 'MorphGender', num : 'MorphNumber') -> str:
        """ Преобразовать число в числительное, записанное буквами, в соотв. роде и числе.
         Например, 5 жен.ед. - ПЯТАЯ,  26 мн. - ДВАДЦАТЬ ШЕСТЫЕ
        
        Args:
            value(int): значение
            gender(MorphGender): род
            num(MorphNumber): число
        
        """
        if ((value < 1) or value >= 100): 
            return None
        words = None
        if (num == MorphNumber.PLURAL): 
            words = NumberHelper.__m_plural_number_words
        elif (gender == MorphGender.FEMINIE): 
            words = NumberHelper.__m_woman_number_words
        elif (gender == MorphGender.NEUTER): 
            words = NumberHelper.__m_neutral_number_words
        else: 
            words = NumberHelper.__m_man_number_words
        if (value < 20): 
            return words[value - 1]
        i = math.floor(value / 10)
        j = value % 10
        i -= 2
        if (i >= len(NumberHelper.__m_dec_dumber_words)): 
            return None
        if (j > 0): 
            return "{0} {1}".format(NumberHelper.__m_dec_dumber_words[i], words[j - 1])
        decs = None
        if (num == MorphNumber.PLURAL): 
            decs = NumberHelper.__m_plural_dec_dumber_words
        elif (gender == MorphGender.FEMINIE): 
            decs = NumberHelper.__m_woman_dec_dumber_words
        elif (gender == MorphGender.NEUTER): 
            decs = NumberHelper.__m_neutral_dec_dumber_words
        else: 
            decs = NumberHelper.__m_man_dec_dumber_words
        return decs[i]
    
    __m_man_number_words = None
    
    __m_neutral_number_words = None
    
    __m_woman_number_words = None
    
    __m_plural_number_words = None
    
    __m_dec_dumber_words = None
    
    __m_man_dec_dumber_words = None
    
    __m_woman_dec_dumber_words = None
    
    __m_neutral_dec_dumber_words = None
    
    __m_plural_dec_dumber_words = None
    
    _m_romans = None
    
    @staticmethod
    def get_number_roman(val : int) -> str:
        """ Получить для числа римскую запись
        
        Args:
            val(int): 
        
        """
        if (val > 0 and val <= len(NumberHelper._m_romans)): 
            return NumberHelper._m_romans[val - 1]
        return str(val)
    
    @staticmethod
    def try_parse_float_number(t : 'Token') -> 'NumberExToken':
        """ Выделить дробное число
        
        Args:
            t(Token): начальный токен
        
        """
        from pullenti.ner.core.NumberExToken import NumberExToken
        return NumberExToken.try_parse_float_number(t)
    
    @staticmethod
    def try_parse_number_with_postfix(t : 'Token') -> 'NumberExToken':
        """ Выделение стандартных мер, типа: 10 кв.м.
        
        Args:
            t(Token): начальный токен
        
        """
        from pullenti.ner.core.NumberExToken import NumberExToken
        return NumberExToken.try_parse_number_with_postfix(t)
    
    @staticmethod
    def try_attach_postfix_only(t : 'Token') -> 'NumberExToken':
        """ Это попробовать только тип (постфикс) без самого числа.
         Например, куб.м.
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.core.NumberExToken import NumberExToken
        return NumberExToken.try_attach_postfix_only(t)
    
    @staticmethod
    def _is_money_char(t : 'Token') -> str:
        """ Если этообозначение денежной единицы (н-р, $), то возвращает код валюты
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.TextToken import TextToken
        if (not ((isinstance(t, TextToken))) or t.length_char != 1): 
            return None
        ch = (t if isinstance(t, TextToken) else None).term[0]
        if (ch == '$'): 
            return "USD"
        if (ch == '£' or ch == chr(0xA3) or ch == chr(0x20A4)): 
            return "GBP"
        if (ch == '€'): 
            return "EUR"
        if (ch == '¥' or ch == chr(0xA5)): 
            return "JPY"
        if (ch == chr(0x20A9)): 
            return "KRW"
        if (ch == chr(0xFFE5) or ch == 'Ұ' or ch == 'Ұ'): 
            return "CNY"
        if (ch == chr(0x20BD)): 
            return "RUB"
        if (ch == chr(0x20B4)): 
            return "UAH"
        if (ch == chr(0x20AB)): 
            return "VND"
        if (ch == chr(0x20AD)): 
            return "LAK"
        if (ch == chr(0x20BA)): 
            return "TRY"
        if (ch == chr(0x20B1)): 
            return "PHP"
        if (ch == chr(0x17DB)): 
            return "KHR"
        if (ch == chr(0x20B9)): 
            return "INR"
        if (ch == chr(0x20A8)): 
            return "IDR"
        if (ch == chr(0x20B5)): 
            return "GHS"
        if (ch == chr(0x09F3)): 
            return "BDT"
        if (ch == chr(0x20B8)): 
            return "KZT"
        if (ch == chr(0x20AE)): 
            return "MNT"
        if (ch == chr(0x0192)): 
            return "HUF"
        if (ch == chr(0x20AA)): 
            return "ILS"
        return None
    
    __pril_num_tag_bit = 0x40000000
    
    @staticmethod
    def _initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.morph.MorphLang import MorphLang
        if (NumberHelper._m_nums is not None): 
            return
        NumberHelper._m_nums = TerminCollection()
        NumberHelper._m_nums.all_add_strs_normalized = True
        NumberHelper._m_nums.add_str("ОДИН", 1, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ПЕРВЫЙ", 1 | NumberHelper.__pril_num_tag_bit, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ОДИН", 1, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("ПЕРШИЙ", 1 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("ОДНА", 1, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ОДНО", 1, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("FIRST", 1 | NumberHelper.__pril_num_tag_bit, MorphLang.EN, True)
        NumberHelper._m_nums.add_str("SEMEL", 1, MorphLang.EN, True)
        NumberHelper._m_nums.add_str("ONE", 1, MorphLang.EN, True)
        NumberHelper._m_nums.add_str("ДВА", 2, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ВТОРОЙ", 2 | NumberHelper.__pril_num_tag_bit, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ДВОЕ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ДВЕ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ДВУХ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ОБА", 2, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ОБЕ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ДВА", 2, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("ДРУГИЙ", 2 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("ДВОЄ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("ДВІ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("ДВОХ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("ОБОЄ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("ОБИДВА", 2, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("SECOND", 2 | NumberHelper.__pril_num_tag_bit, MorphLang.EN, True)
        NumberHelper._m_nums.add_str("BIS", 2, MorphLang.EN, True)
        NumberHelper._m_nums.add_str("TWO", 2, MorphLang.EN, True)
        NumberHelper._m_nums.add_str("ТРИ", 3, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ТРЕТИЙ", 3 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТРЕХ", 3, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ТРОЕ", 3, MorphLang.RU, True)
        NumberHelper._m_nums.add_str("ТРИ", 3, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("ТРЕТІЙ", 3 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("ТРЬОХ", 3, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("ТРОЄ", 3, MorphLang.UA, True)
        NumberHelper._m_nums.add_str("THIRD", 3 | NumberHelper.__pril_num_tag_bit, MorphLang.EN, True)
        NumberHelper._m_nums.add_str("TER", 3, MorphLang.EN, True)
        NumberHelper._m_nums.add_str("THREE", 3, MorphLang.EN, True)
        NumberHelper._m_nums.add_str("ЧЕТЫРЕ", 4, MorphLang(), False)
        NumberHelper._m_nums.add_str("ЧЕТВЕРТЫЙ", 4 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ЧЕТЫРЕХ", 4, MorphLang(), False)
        NumberHelper._m_nums.add_str("ЧЕТВЕРО", 4, MorphLang(), False)
        NumberHelper._m_nums.add_str("ЧОТИРИ", 4, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ЧЕТВЕРТИЙ", 4 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ЧОТИРЬОХ", 4, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("FORTH", 4 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("QUATER", 4, MorphLang(), False)
        NumberHelper._m_nums.add_str("FOUR", 4, MorphLang.EN, True)
        NumberHelper._m_nums.add_str("ПЯТЬ", 5, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТЫЙ", 5 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТИ", 5, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТЕРО", 5, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТЬ", 5, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ПЯТИЙ", 5 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("FIFTH", 5 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("QUINQUIES", 5, MorphLang(), False)
        NumberHelper._m_nums.add_str("FIVE", 5, MorphLang.EN, True)
        NumberHelper._m_nums.add_str("ШЕСТЬ", 6, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШЕСТОЙ", 6 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШЕСТИ", 6, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШЕСТЕРО", 6, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШІСТЬ", 6, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ШОСТИЙ", 6 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("SIX", 6, MorphLang.EN, False)
        NumberHelper._m_nums.add_str("SIXTH", 6 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("SEXIES ", 6, MorphLang(), False)
        NumberHelper._m_nums.add_str("СЕМЬ", 7, MorphLang(), False)
        NumberHelper._m_nums.add_str("СЕДЬМОЙ", 7 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("СЕМИ", 7, MorphLang(), False)
        NumberHelper._m_nums.add_str("СЕМЕРО", 7, MorphLang(), False)
        NumberHelper._m_nums.add_str("СІМ", 7, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("СЬОМИЙ", 7 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("SEVEN", 7, MorphLang(), False)
        NumberHelper._m_nums.add_str("SEVENTH", 7 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("SEPTIES", 7, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВОСЕМЬ", 8, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВОСЬМОЙ", 8 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВОСЬМИ", 8, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВОСЬМЕРО", 8, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВІСІМ", 8, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ВОСЬМИЙ", 8 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("EIGHT", 8, MorphLang(), False)
        NumberHelper._m_nums.add_str("EIGHTH", 8 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("OCTIES", 8, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТЬ", 9, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТЫЙ", 9 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТИ", 9, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТЕРО", 9, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТЬ", 9, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДЕВЯТИЙ", 9 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("NINE", 9, MorphLang(), False)
        NumberHelper._m_nums.add_str("NINTH", 9 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("NOVIES", 9, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕСЯТЬ", 10, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕСЯТЫЙ", 10 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕСЯТИ", 10, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕСЯТИРО", 10, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕСЯТЬ", 10, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДЕСЯТИЙ", 10 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("TEN", 10, MorphLang(), False)
        NumberHelper._m_nums.add_str("TENTH", 10 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("DECIES", 10, MorphLang(), False)
        NumberHelper._m_nums.add_str("ОДИННАДЦАТЬ", 11, MorphLang(), False)
        NumberHelper._m_nums.add_str("ОДИННАДЦАТЫЙ", 11 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ОДИННАДЦАТИ", 11, MorphLang(), False)
        NumberHelper._m_nums.add_str("ОДИННАДЦАТИРО", 11, MorphLang(), False)
        NumberHelper._m_nums.add_str("ОДИНАДЦЯТЬ", 11, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ОДИНАДЦЯТИЙ", 11 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ОДИНАДЦЯТИ", 11, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ELEVEN", 11, MorphLang(), False)
        NumberHelper._m_nums.add_str("ELEVENTH", 11 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВЕНАДЦАТЬ", 12, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВЕНАДЦАТЫЙ", 12 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВЕНАДЦАТИ", 12, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВАНАДЦЯТЬ", 12, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДВАНАДЦЯТИЙ", 12 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДВАНАДЦЯТИ", 12, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("TWELVE", 12, MorphLang(), False)
        NumberHelper._m_nums.add_str("TWELFTH", 12 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТРИНАДЦАТЬ", 13, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТРИНАДЦАТЫЙ", 13 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТРИНАДЦАТИ", 13, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТРИНАДЦЯТЬ", 13, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ТРИНАДЦЯТИЙ", 13 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ТРИНАДЦЯТИ", 13, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("THIRTEEN", 13, MorphLang(), False)
        NumberHelper._m_nums.add_str("THIRTEENTH", 13 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ЧЕТЫРНАДЦАТЬ", 14, MorphLang(), False)
        NumberHelper._m_nums.add_str("ЧЕТЫРНАДЦАТЫЙ", 14 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ЧЕТЫРНАДЦАТИ", 14, MorphLang(), False)
        NumberHelper._m_nums.add_str("ЧОТИРНАДЦЯТЬ", 14, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ЧОТИРНАДЦЯТИЙ", 14 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ЧОТИРНАДЦЯТИ", 14, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("FOURTEEN", 14, MorphLang(), False)
        NumberHelper._m_nums.add_str("FOURTEENTH", 14 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТНАДЦАТЬ", 15, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТНАДЦАТЫЙ", 15 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТНАДЦАТИ", 15, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТНАДЦЯТЬ", 15, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ПЯТНАДЦЯТИЙ", 15 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ПЯТНАДЦЯТИ", 15, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("FIFTEEN", 15, MorphLang(), False)
        NumberHelper._m_nums.add_str("FIFTEENTH", 15 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШЕСТНАДЦАТЬ", 16, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШЕСТНАДЦАТЫЙ", 16 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШЕСТНАДЦАТИ", 16, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШІСТНАДЦЯТЬ", 16, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ШІСТНАДЦЯТИЙ", 16 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ШІСТНАДЦЯТИ", 16, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("SIXTEEN", 16, MorphLang(), False)
        NumberHelper._m_nums.add_str("SIXTEENTH", 16 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("СЕМНАДЦАТЬ", 17, MorphLang(), False)
        NumberHelper._m_nums.add_str("СЕМНАДЦАТЫЙ", 17 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("СЕМНАДЦАТИ", 17, MorphLang(), False)
        NumberHelper._m_nums.add_str("СІМНАДЦЯТЬ", 17, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("СІМНАДЦЯТИЙ", 17 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("СІМНАДЦЯТИ", 17, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("SEVENTEEN", 17, MorphLang(), False)
        NumberHelper._m_nums.add_str("SEVENTEENTH", 17 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВОСЕМНАДЦАТЬ", 18, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВОСЕМНАДЦАТЫЙ", 18 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВОСЕМНАДЦАТИ", 18, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВІСІМНАДЦЯТЬ", 18, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ВІСІМНАДЦЯТИЙ", 18 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ВІСІМНАДЦЯТИ", 18, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("EIGHTEEN", 18, MorphLang(), False)
        NumberHelper._m_nums.add_str("EIGHTEENTH", 18 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТНАДЦАТЬ", 19, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТНАДЦАТЫЙ", 19 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТНАДЦАТИ", 19, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТНАДЦЯТЬ", 19, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДЕВЯТНАДЦЯТИЙ", 19 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДЕВЯТНАДЦЯТИ", 19, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("NINETEEN", 19, MorphLang(), False)
        NumberHelper._m_nums.add_str("NINETEENTH", 19 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВАДЦАТЬ", 20, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВАДЦАТЫЙ", 20 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВАДЦАТИ", 20, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВАДЦЯТЬ", 20, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДВАДЦЯТИЙ", 20 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДВАДЦЯТИ", 20, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("TWENTY", 20, MorphLang(), False)
        NumberHelper._m_nums.add_str("TWENTIETH", 20 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТРИДЦАТЬ", 30, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТРИДЦАТЫЙ", 30 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТРИДЦАТИ", 30, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТРИДЦЯТЬ", 30, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ТРИДЦЯТИЙ", 30 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ТРИДЦЯТИ", 30, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("THIRTY", 30, MorphLang(), False)
        NumberHelper._m_nums.add_str("THIRTIETH", 30 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("СОРОК", 40, MorphLang(), False)
        NumberHelper._m_nums.add_str("СОРОКОВОЙ", 40 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("СОРОКА", 40, MorphLang(), False)
        NumberHelper._m_nums.add_str("СОРОК", 40, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("СОРОКОВИЙ", 40 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("FORTY", 40, MorphLang(), False)
        NumberHelper._m_nums.add_str("FORTIETH", 40 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТЬДЕСЯТ", 50, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТИДЕСЯТЫЙ", 50 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТИДЕСЯТИ", 50, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТДЕСЯТ", 50, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ПЯТДЕСЯТИЙ", 50 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ПЯТДЕСЯТИ", 50, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("FIFTY", 50, MorphLang(), False)
        NumberHelper._m_nums.add_str("FIFTIETH", 50 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШЕСТЬДЕСЯТ", 60, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШЕСТИДЕСЯТЫЙ", 60 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШЕСТИДЕСЯТИ", 60, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШІСТДЕСЯТ", 60, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ШЕСИДЕСЯТЫЙ", 60 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ШІСТДЕСЯТИ", 60, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("SIXTY", 60, MorphLang(), False)
        NumberHelper._m_nums.add_str("SIXTIETH", 60 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("СЕМЬДЕСЯТ", 70, MorphLang(), False)
        NumberHelper._m_nums.add_str("СЕМИДЕСЯТЫЙ", 70 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("СЕМИДЕСЯТИ", 70, MorphLang(), False)
        NumberHelper._m_nums.add_str("СІМДЕСЯТ", 70, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("СІМДЕСЯТИЙ", 70 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("СІМДЕСЯТИ", 70, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("SEVENTY", 70, MorphLang(), False)
        NumberHelper._m_nums.add_str("SEVENTIETH", 70 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("SEVENTIES", 70 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВОСЕМЬДЕСЯТ", 80, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВОСЬМИДЕСЯТЫЙ", 80 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВОСЬМИДЕСЯТИ", 80, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВІСІМДЕСЯТ", 80, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ВОСЬМИДЕСЯТИЙ", 80 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ВІСІМДЕСЯТИ", 80, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("EIGHTY", 80, MorphLang(), False)
        NumberHelper._m_nums.add_str("EIGHTIETH", 80 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("EIGHTIES", 80 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯНОСТО", 90, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯНОСТЫЙ", 90 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯНОСТО", 90, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДЕВЯНОСТИЙ", 90 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("NINETY", 90, MorphLang(), False)
        NumberHelper._m_nums.add_str("NINETIETH", 90 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("NINETIES", 90 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("СТО", 100, MorphLang(), False)
        NumberHelper._m_nums.add_str("СОТЫЙ", 100 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("СТА", 100, MorphLang(), False)
        NumberHelper._m_nums.add_str("СТО", 100, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("СОТИЙ", 100 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("HUNDRED", 100, MorphLang(), False)
        NumberHelper._m_nums.add_str("HUNDREDTH", 100 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВЕСТИ", 200, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВУХСОТЫЙ", 200 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВУХСОТ", 200, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВІСТІ", 200, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДВОХСОТИЙ", 200 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДВОХСОТ", 200, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ТРИСТА", 300, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТРЕХСОТЫЙ", 300 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТРЕХСОТ", 300, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТРИСТА", 300, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ТРЬОХСОТИЙ", 300 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ТРЬОХСОТ", 300, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ЧЕТЫРЕСТА", 400, MorphLang(), False)
        NumberHelper._m_nums.add_str("ЧЕТЫРЕХСОТЫЙ", 400 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ЧОТИРИСТА", 400, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ЧОТИРЬОХСОТИЙ", 400 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ПЯТЬСОТ", 500, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТИСОТЫЙ", 500 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ПЯТСОТ", 500, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ПЯТИСОТИЙ", 500 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ШЕСТЬСОТ", 600, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШЕСТИСОТЫЙ", 600 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ШІСТСОТ", 600, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ШЕСТИСОТИЙ", 600 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("СЕМЬСОТ", 700, MorphLang(), False)
        NumberHelper._m_nums.add_str("СЕМИСОТЫЙ", 700 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("СІМСОТ", 700, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("СЕМИСОТИЙ", 700 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ВОСЕМЬСОТ", 800, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВОСЕМЬСОТЫЙ", 800 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВОСЬМИСОТЫЙ", 800 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ВІСІМСОТ", 800, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ВОСЬМИСОТЫЙ", 800 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДЕВЯТЬСОТ", 900, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТЬСОТЫЙ", 900 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТИСОТЫЙ", 900 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТСОТ", 900, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДЕВЯТЬСОТЫЙ", 900 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДЕВЯТИСОТИЙ", 900 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ТЫС", 1000, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТЫСЯЧА", 1000, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТЫСЯЧНЫЙ", 1000 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ТИС", 1000, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ТИСЯЧА", 1000, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ТИСЯЧНИЙ", 1000 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("ДВУХТЫСЯЧНЫЙ", 2000 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.add_str("ДВОХТИСЯЧНИЙ", 2000 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("МИЛЛИОН", 1000000, MorphLang(), False)
        NumberHelper._m_nums.add_str("МЛН", 1000000, MorphLang(), False)
        NumberHelper._m_nums.add_str("МІЛЬЙОН", 1000000, MorphLang.UA, False)
        NumberHelper._m_nums.add_str("МИЛЛИАРД", 1000000000, MorphLang(), False)
        NumberHelper._m_nums.add_str("МІЛЬЯРД", 1000000000, MorphLang.UA, False)
    
    _m_nums = None
    
    # static constructor for class NumberHelper
    @staticmethod
    def _static_ctor():
        NumberHelper.__m_samples = ["ДЕСЯТЫЙ", "ПЕРВЫЙ", "ВТОРОЙ", "ТРЕТИЙ", "ЧЕТВЕРТЫЙ", "ПЯТЫЙ", "ШЕСТОЙ", "СЕДЬМОЙ", "ВОСЬМОЙ", "ДЕВЯТЫЙ"]
        NumberHelper.__m_man_number_words = ["ПЕРВЫЙ", "ВТОРОЙ", "ТРЕТИЙ", "ЧЕТВЕРТЫЙ", "ПЯТЫЙ", "ШЕСТОЙ", "СЕДЬМОЙ", "ВОСЬМОЙ", "ДЕВЯТЫЙ", "ДЕСЯТЫЙ", "ОДИННАДЦАТЫЙ", "ДВЕНАДЦАТЫЙ", "ТРИНАДЦАТЫЙ", "ЧЕТЫРНАДЦАТЫЙ", "ПЯТНАДЦАТЫЙ", "ШЕСТНАДЦАТЫЙ", "СЕМНАДЦАТЫЙ", "ВОСЕМНАДЦАТЫЙ", "ДЕВЯТНАДЦАТЫЙ"]
        NumberHelper.__m_neutral_number_words = ["ПЕРВОЕ", "ВТОРОЕ", "ТРЕТЬЕ", "ЧЕТВЕРТОЕ", "ПЯТОЕ", "ШЕСТОЕ", "СЕДЬМОЕ", "ВОСЬМОЕ", "ДЕВЯТОЕ", "ДЕСЯТОЕ", "ОДИННАДЦАТОЕ", "ДВЕНАДЦАТОЕ", "ТРИНАДЦАТОЕ", "ЧЕТЫРНАДЦАТОЕ", "ПЯТНАДЦАТОЕ", "ШЕСТНАДЦАТОЕ", "СЕМНАДЦАТОЕ", "ВОСЕМНАДЦАТОЕ", "ДЕВЯТНАДЦАТОЕ"]
        NumberHelper.__m_woman_number_words = ["ПЕРВАЯ", "ВТОРАЯ", "ТРЕТЬЯ", "ЧЕТВЕРТАЯ", "ПЯТАЯ", "ШЕСТАЯ", "СЕДЬМАЯ", "ВОСЬМАЯ", "ДЕВЯТАЯ", "ДЕСЯТАЯ", "ОДИННАДЦАТАЯ", "ДВЕНАДЦАТАЯ", "ТРИНАДЦАТАЯ", "ЧЕТЫРНАДЦАТАЯ", "ПЯТНАДЦАТАЯ", "ШЕСТНАДЦАТАЯ", "СЕМНАДЦАТАЯ", "ВОСЕМНАДЦАТАЯ", "ДЕВЯТНАДЦАТАЯ"]
        NumberHelper.__m_plural_number_words = ["ПЕРВЫЕ", "ВТОРЫЕ", "ТРЕТЬИ", "ЧЕТВЕРТЫЕ", "ПЯТЫЕ", "ШЕСТЫЕ", "СЕДЬМЫЕ", "ВОСЬМЫЕ", "ДЕВЯТЫЕ", "ДЕСЯТЫЕ", "ОДИННАДЦАТЫЕ", "ДВЕНАДЦАТЫЕ", "ТРИНАДЦАТЫЕ", "ЧЕТЫРНАДЦАТЫЕ", "ПЯТНАДЦАТЫЕ", "ШЕСТНАДЦАТЫЕ", "СЕМНАДЦАТЫЕ", "ВОСЕМНАДЦАТЫЕ", "ДЕВЯТНАДЦАТЫЕ"]
        NumberHelper.__m_dec_dumber_words = ["ДВАДЦАТЬ", "ТРИДЦАТЬ", "СОРОК", "ПЯТЬДЕСЯТ", "ШЕСТЬДЕСЯТ", "СЕМЬДЕСЯТ", "ВОСЕМЬДЕСЯТ", "ДЕВЯНОСТО"]
        NumberHelper.__m_man_dec_dumber_words = ["ДВАДЦАТЫЙ", "ТРИДЦАТЫЙ", "СОРОКОВОЙ", "ПЯТЬДЕСЯТЫЙ", "ШЕСТЬДЕСЯТЫЙ", "СЕМЬДЕСЯТЫЙ", "ВОСЕМЬДЕСЯТЫЙ", "ДЕВЯНОСТЫЙ"]
        NumberHelper.__m_woman_dec_dumber_words = ["ДВАДЦАТАЯ", "ТРИДЦАТАЯ", "СОРОКОВАЯ", "ПЯТЬДЕСЯТАЯ", "ШЕСТЬДЕСЯТАЯ", "СЕМЬДЕСЯТАЯ", "ВОСЕМЬДЕСЯТАЯ", "ДЕВЯНОСТАЯ"]
        NumberHelper.__m_neutral_dec_dumber_words = ["ДВАДЦАТОЕ", "ТРИДЦАТОЕ", "СОРОКОВОЕ", "ПЯТЬДЕСЯТОЕ", "ШЕСТЬДЕСЯТОЕ", "СЕМЬДЕСЯТОЕ", "ВОСЕМЬДЕСЯТОЕ", "ДЕВЯНОСТОЕ"]
        NumberHelper.__m_plural_dec_dumber_words = ["ДВАДЦАТЫЕ", "ТРИДЦАТЫЕ", "СОРОКОВЫЕ", "ПЯТЬДЕСЯТЫЕ", "ШЕСТЬДЕСЯТЫЕ", "СЕМЬДЕСЯТЫЕ", "ВОСЕМЬДЕСЯТЫЕ", "ДЕВЯНОСТЫЕ"]
        NumberHelper._m_romans = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX"]

NumberHelper._static_ctor()