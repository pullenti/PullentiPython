# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender


class NumberHelper:
    """ Работа с числовыми значениями """
    
    @staticmethod
    def _tryParseNumber(token : 'Token') -> 'NumberToken':
        """ Попробовать создать числительное
        
        Args:
            token(Token): 
        
        """
        return NumberHelper.__TryParse(token, -1)
    
    @staticmethod
    def __TryParse(token : 'Token', prev_val : int=-1) -> 'NumberToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.MorphCollection import MorphCollection
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.morph.MorphClass import MorphClass
        if (isinstance(token, NumberToken)): 
            return Utils.asObjectOrNull(token, NumberToken)
        tt = Utils.asObjectOrNull(token, TextToken)
        if (tt is None): 
            return None
        et = tt
        val = -1
        typ = NumberSpellingType.DIGIT
        term = tt.term
        if (str.isdigit(term[0])): 
            wrapval591 = RefOutArgWrapper(0)
            inoutres592 = Utils.tryParseInt(term, wrapval591)
            val = wrapval591.value
            if (not inoutres592): 
                return None
        if (val >= (0)): 
            hiph = False
            if ((isinstance(et.next0_, TextToken)) and et.next0_.is_hiphen): 
                if ((et.whitespaces_after_count < 2) and (et.next0_.whitespaces_after_count < 2)): 
                    et = (Utils.asObjectOrNull(et.next0_, TextToken))
                    hiph = True
            mc = None
            if (hiph or not et.is_whitespace_after): 
                rr = NumberHelper.__analizeNumberTail(Utils.asObjectOrNull(et.next0_, TextToken), val)
                if (rr is None): 
                    et = tt
                else: 
                    mc = rr.morph
                    et = (Utils.asObjectOrNull(rr.end_token, TextToken))
            else: 
                et = tt
            if (et.next0_ is not None and et.next0_.isChar('(')): 
                num2 = NumberHelper._tryParseNumber(et.next0_.next0_)
                if ((num2 is not None and num2.value == val and num2.end_token.next0_ is not None) and num2.end_token.next0_.isChar(')')): 
                    et = (Utils.asObjectOrNull(num2.end_token.next0_, TextToken))
            while (isinstance(et.next0_, TextToken)) and not ((isinstance(et.previous, NumberToken))) and et.is_whitespace_before:
                if (et.whitespaces_after_count != 1): 
                    break
                sss = (Utils.asObjectOrNull(et.next0_, TextToken)).term
                if (sss == "000"): 
                    val *= (1000)
                    et = (Utils.asObjectOrNull(et.next0_, TextToken))
                    continue
                if (str.isdigit(sss[0]) and len(sss) == 3): 
                    val2 = val
                    ttt = et.next0_
                    first_pass2821 = True
                    while True:
                        if first_pass2821: first_pass2821 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        ss = ttt.getSourceText()
                        if (ttt.whitespaces_before_count == 1 and ttt.length_char == 3 and str.isdigit(ss[0])): 
                            wrapii593 = RefOutArgWrapper(0)
                            inoutres594 = Utils.tryParseInt(ss, wrapii593)
                            ii = wrapii593.value
                            if (not inoutres594): 
                                break
                            val2 *= (1000)
                            val2 += (ii)
                            continue
                        if ((ttt.isCharOf(".,") and not ttt.is_whitespace_before and not ttt.is_whitespace_after) and ttt.next0_ is not None and str.isdigit(ttt.next0_.getSourceText()[0])): 
                            if (ttt.next0_.is_whitespace_after and (isinstance(ttt.previous, TextToken))): 
                                et = (Utils.asObjectOrNull(ttt.previous, TextToken))
                                val = val2
                                break
                        break
                break
            for k in range(3):
                if ((isinstance(et.next0_, TextToken)) and et.next0_.chars.is_letter): 
                    tt = (Utils.asObjectOrNull(et.next0_, TextToken))
                    t0 = et
                    coef = 0
                    if (k == 0): 
                        coef = (1000000000)
                        if (tt.isValue("МИЛЛИАРД", "МІЛЬЯРД") or tt.isValue("BILLION", None) or tt.isValue("BN", None)): 
                            et = tt
                            val *= coef
                        elif (tt.isValue("МЛРД", None)): 
                            et = tt
                            val *= coef
                            if ((isinstance(et.next0_, TextToken)) and et.next0_.isChar('.')): 
                                et = (Utils.asObjectOrNull(et.next0_, TextToken))
                        else: 
                            continue
                    elif (k == 1): 
                        coef = (1000000)
                        if (tt.isValue("МИЛЛИОН", "МІЛЬЙОН") or tt.isValue("MILLION", None)): 
                            et = tt
                            val *= coef
                        elif (tt.isValue("МЛН", None)): 
                            et = tt
                            val *= coef
                            if ((isinstance(et.next0_, TextToken)) and et.next0_.isChar('.')): 
                                et = (Utils.asObjectOrNull(et.next0_, TextToken))
                        elif ((isinstance(tt, TextToken)) and (Utils.asObjectOrNull(tt, TextToken)).term == "M"): 
                            if (NumberHelper._isMoneyChar(et.previous) is not None): 
                                et = tt
                                val *= coef
                            else: 
                                break
                        else: 
                            continue
                    else: 
                        coef = (1000)
                        if (tt.isValue("ТЫСЯЧА", "ТИСЯЧА") or tt.isValue("THOUSAND", None)): 
                            et = tt
                            val *= coef
                        elif (tt.isValue("ТЫС", None) or tt.isValue("ТИС", None)): 
                            et = tt
                            val *= coef
                            if ((isinstance(et.next0_, TextToken)) and et.next0_.isChar('.')): 
                                et = (Utils.asObjectOrNull(et.next0_, TextToken))
                        else: 
                            break
                    if (((t0 == token and t0.length_char <= 3 and t0.previous is not None) and not t0.is_whitespace_before and t0.previous.isCharOf(",.")) and not t0.previous.is_whitespace_before and (((isinstance(t0.previous.previous, NumberToken)) or prev_val >= (0)))): 
                        if (t0.length_char == 1): 
                            val = math.floor(val / (10))
                        elif (t0.length_char == 2): 
                            val = math.floor(val / (100))
                        else: 
                            val = math.floor(val / (1000))
                        if (isinstance(t0.previous.previous, NumberToken)): 
                            val += ((Utils.asObjectOrNull(t0.previous.previous, NumberToken)).value * coef)
                        else: 
                            val += (prev_val * coef)
                        token = t0.previous.previous
                    next0_ = NumberHelper.__TryParse(et.next0_, -1)
                    if (next0_ is None or next0_.value >= coef): 
                        break
                    tt1 = next0_.end_token
                    if (((isinstance(tt1.next0_, TextToken)) and not tt1.is_whitespace_after and tt1.next0_.isCharOf(".,")) and not tt1.next0_.is_whitespace_after): 
                        re1 = NumberHelper.__TryParse(tt1.next0_.next0_, next0_.value)
                        if (re1 is not None and re1.begin_token == next0_.begin_token): 
                            next0_ = re1
                    val += next0_.value
                    et = (Utils.asObjectOrNull(next0_.end_token, TextToken))
                    break
            res = NumberToken._new595(token, et, val, typ, mc)
            if (et.next0_ is not None and (res.value < (1000)) and ((et.next0_.is_hiphen or et.next0_.isValue("ДО", None)))): 
                tt1 = et.next0_.next0_
                first_pass2822 = True
                while True:
                    if first_pass2822: first_pass2822 = False
                    else: tt1 = tt1.next0_
                    if (not (tt1 is not None)): break
                    if (not ((isinstance(tt1, TextToken)))): 
                        break
                    if (str.isdigit((Utils.asObjectOrNull(tt1, TextToken)).term[0])): 
                        continue
                    if (tt1.isCharOf(",.") or NumberHelper._isMoneyChar(tt1) is not None): 
                        continue
                    if (tt1.isValue("МИЛЛИОН", "МІЛЬЙОН") or tt1.isValue("МЛН", None) or tt1.isValue("MILLION", None)): 
                        res.value *= (1000000)
                    elif ((tt1.isValue("МИЛЛИАРД", "МІЛЬЯРД") or tt1.isValue("МЛРД", None) or tt1.isValue("BILLION", None)) or tt1.isValue("BN", None)): 
                        res.value *= (1000000000)
                    elif (tt1.isValue("ТЫСЯЧА", "ТИСЯЧА") or tt1.isValue("ТЫС", "ТИС") or tt1.isValue("THOUSAND", None)): 
                        res.value *= (1000)
                    break
            return res
        val = (0)
        et = (None)
        loc_value = 0
        is_adj = False
        jprev = -1
        t = tt
        while t is not None: 
            if (t != tt and t.newlines_before_count > 1): 
                break
            term = t.term
            if (not str.isalpha(term[0])): 
                break
            num = NumberHelper._m_nums.tryParse(t, TerminParseAttr.FULLWORDSONLY)
            if (num is None): 
                break
            j = (num.termin.tag)
            if (jprev > 0 and (jprev < 20) and (j < 20)): 
                break
            is_adj = ((j & NumberHelper.__pril_num_tag_bit)) != 0
            j &= (~ NumberHelper.__pril_num_tag_bit)
            if (is_adj and t != tt): 
                if ((t.isValue("ДЕСЯТЫЙ", None) or t.isValue("СОТЫЙ", None) or t.isValue("ТЫСЯЧНЫЙ", None)) or t.isValue("ДЕСЯТИТЫСЯЧНЫЙ", None) or t.isValue("МИЛЛИОННЫЙ", None)): 
                    break
            if (j >= 1000): 
                if (loc_value == (0)): 
                    loc_value = (1)
                val += (loc_value * (j))
                loc_value = (0)
            else: 
                if (loc_value > (0) and loc_value <= j): 
                    break
                loc_value += (j)
            et = t
            if (j == 1000 or j == 1000000): 
                if ((isinstance(et.next0_, TextToken)) and et.next0_.isChar('.')): 
                    et = Utils.asObjectOrNull(et.next0_, TextToken)
                    t = et
            jprev = j
            t = (Utils.asObjectOrNull(t.next0_, TextToken))
        if (loc_value > (0)): 
            val += loc_value
        if (val == (0) or et is None): 
            return None
        nt = NumberToken(tt, et, val, NumberSpellingType.WORDS)
        if (et.morph is not None): 
            nt.morph = MorphCollection(et.morph)
            for wff in et.morph.items: 
                wf = Utils.asObjectOrNull(wff, MorphWordForm)
                if (wf is not None and wf.misc is not None and "собир." in wf.misc.attrs): 
                    nt.morph.class0_ = MorphClass.NOUN
                    break
            if (not is_adj): 
                nt.morph.removeItems((MorphClass.ADJECTIVE) | MorphClass.NOUN, False)
                if (nt.morph.class0_.is_undefined): 
                    nt.morph.class0_ = MorphClass.NOUN
            if (et.chars.is_latin_letter and is_adj): 
                nt.morph.class0_ = MorphClass.ADJECTIVE
        return nt
    
    @staticmethod
    def tryParseRoman(t : 'Token') -> 'NumberToken':
        """ Попробовать выделить римскую цифру
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        if (isinstance(t, NumberToken)): 
            return Utils.asObjectOrNull(t, NumberToken)
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None or not t.chars.is_letter): 
            return None
        term = tt.term
        if (not NumberHelper.__isRomVal(term)): 
            return None
        if (tt.morph.class0_.is_preposition): 
            if (tt.chars.is_all_lower): 
                return None
        res = NumberToken(t, t, 0, NumberSpellingType.ROMAN)
        nums = list()
        while t is not None: 
            if (t != res.begin_token and t.is_whitespace_before): 
                break
            if (not ((isinstance(t, TextToken)))): 
                break
            term = (Utils.asObjectOrNull(t, TextToken)).term
            if (not NumberHelper.__isRomVal(term)): 
                break
            for s in term: 
                i = NumberHelper.__romVal(s)
                if (i > 0): 
                    nums.append(i)
            res.end_token = t
            t = t.next0_
        if (len(nums) == 0): 
            return None
        i = 0
        while i < len(nums): 
            if ((i + 1) < len(nums)): 
                if (nums[i] == 1 and nums[i + 1] == 5): 
                    res.value += (4)
                    i += 1
                elif (nums[i] == 1 and nums[i + 1] == 10): 
                    res.value += (9)
                    i += 1
                elif (nums[i] == 10 and nums[i + 1] == 50): 
                    res.value += (40)
                    i += 1
                elif (nums[i] == 10 and nums[i + 1] == 100): 
                    res.value += (90)
                    i += 1
                else: 
                    res.value += (nums[i])
            else: 
                res.value += (nums[i])
            i += 1
        hiph = False
        et = res.end_token.next0_
        if (et is None): 
            return res
        if (et.next0_ is not None and et.next0_.is_hiphen): 
            et = et.next0_
            hiph = True
        if (hiph or not et.is_whitespace_after): 
            mc = NumberHelper.__analizeNumberTail(Utils.asObjectOrNull(et.next0_, TextToken), res.value)
            if (mc is not None): 
                res.end_token = mc.end_token
                res.morph = mc.morph
        if ((res.begin_token == res.end_token and res.value == (1) and res.begin_token.chars.is_all_lower) and res.begin_token.morph.language.is_ua): 
            return None
        return res
    
    @staticmethod
    def __romVal(ch : 'char') -> int:
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
    def __isRomVal(str0_ : str) -> bool:
        for ch in str0_: 
            if (NumberHelper.__romVal(ch) < 1): 
                return False
        return True
    
    @staticmethod
    def tryParseRomanBack(token : 'Token') -> 'NumberToken':
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
            nt = NumberHelper.tryParseRoman(t)
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
    def tryParseAge(t : 'Token') -> 'NumberToken':
        """ Это выделение числительных типа 16-летие, 50-летний
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        if (t is None): 
            return None
        nt = Utils.asObjectOrNull(t, NumberToken)
        nt_next = None
        if (nt is not None): 
            nt_next = nt.next0_
        else: 
            if (t.isValue("AGED", None) and (isinstance(t.next0_, NumberToken))): 
                return NumberToken(t, t.next0_, (Utils.asObjectOrNull(t.next0_, NumberToken)).value, NumberSpellingType.AGE)
            nt = NumberHelper.tryParseRoman(t)
            if ((nt) is not None): 
                nt_next = nt.end_token.next0_
        if (nt is not None): 
            if (nt_next is not None): 
                t1 = nt_next
                if (t1.is_hiphen): 
                    t1 = t1.next0_
                if (isinstance(t1, TextToken)): 
                    v = (Utils.asObjectOrNull(t1, TextToken)).term
                    if ((v == "ЛЕТ" or v == "ЛЕТИЯ" or v == "ЛЕТИЕ") or v == "РІЧЧЯ"): 
                        return NumberToken._new595(t, t1, nt.value, NumberSpellingType.AGE, t1.morph)
                    if (t1.isValue("ЛЕТНИЙ", "РІЧНИЙ")): 
                        return NumberToken._new595(t, t1, nt.value, NumberSpellingType.AGE, t1.morph)
                    if (v == "Л" or ((v == "Р" and nt.morph.language.is_ua))): 
                        return NumberToken(t, (t1.next0_ if t1.next0_ is not None and t1.next0_.isChar('.') else t1), nt.value, NumberSpellingType.AGE)
            return None
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        s = tt.term
        if (LanguageHelper.endsWithEx(s, "ЛЕТИЕ", "ЛЕТИЯ", "РІЧЧЯ", None)): 
            term = NumberHelper._m_nums.find(s[0:0+len(s) - 5])
            if (term is not None): 
                return NumberToken._new595(tt, tt, term.tag, NumberSpellingType.AGE, tt.morph)
        s = tt.lemma
        if (LanguageHelper.endsWithEx(s, "ЛЕТНИЙ", "РІЧНИЙ", None, None)): 
            term = NumberHelper._m_nums.find(s[0:0+len(s) - 6])
            if (term is not None): 
                return NumberToken._new595(tt, tt, term.tag, NumberSpellingType.AGE, tt.morph)
        return None
    
    @staticmethod
    def tryParseAnniversary(t : 'Token') -> 'NumberToken':
        """ Выделение годовщин и летий (XX-летие) ... """
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        nt = Utils.asObjectOrNull(t, NumberToken)
        t1 = None
        if (nt is not None): 
            t1 = nt.next0_
        else: 
            nt = NumberHelper.tryParseRoman(t)
            if ((nt) is None): 
                if (isinstance(t, TextToken)): 
                    v = (Utils.asObjectOrNull(t, TextToken)).term
                    num = 0
                    if (v.endswith("ЛЕТИЯ") or v.endswith("ЛЕТИЕ")): 
                        if (v.startswith("ВОСЕМЬСОТ") or v.startswith("ВОСЬМИСОТ")): 
                            num = 800
                    if (num > 0): 
                        return NumberToken(t, t, num, NumberSpellingType.AGE)
                return None
            t1 = nt.end_token.next0_
        if (t1 is None): 
            return None
        if (t1.is_hiphen): 
            t1 = t1.next0_
        if (isinstance(t1, TextToken)): 
            v = (Utils.asObjectOrNull(t1, TextToken)).term
            if ((v == "ЛЕТ" or v == "ЛЕТИЯ" or v == "ЛЕТИЕ") or t1.isValue("ГОДОВЩИНА", None)): 
                return NumberToken(t, t1, nt.value, NumberSpellingType.AGE)
            if (t1.morph.language.is_ua): 
                if (v == "РОКІВ" or v == "РІЧЧЯ" or t1.isValue("РІЧНИЦЯ", None)): 
                    return NumberToken(t, t1, nt.value, NumberSpellingType.AGE)
        return None
    
    __m_samples = None
    
    @staticmethod
    def __analizeNumberTail(tt : 'TextToken', val : int) -> 'MetaToken':
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
            if (((s == "<" or s == "(")) and (isinstance(tt.next0_, TextToken))): 
                s = (Utils.asObjectOrNull(tt.next0_, TextToken)).term
                if ((s == "TH" or s == "ST" or s == "RD") or s == "ND"): 
                    if (tt.next0_.next0_ is not None and tt.next0_.next0_.isCharOf(">)")): 
                        mc = MorphCollection()
                        mc.class0_ = MorphClass.ADJECTIVE
                        mc.language = MorphLang.EN
                        return MetaToken._new600(tt, tt.next0_.next0_, mc)
            return None
        if ((s == "TH" or s == "ST" or s == "RD") or s == "ND"): 
            mc = MorphCollection()
            mc.class0_ = MorphClass.ADJECTIVE
            mc.language = MorphLang.EN
            return MetaToken._new600(tt, tt, mc)
        if (not tt.chars.is_cyrillic_letter): 
            return None
        if (not tt.is_whitespace_after): 
            if (tt.next0_ is not None and tt.next0_.chars.is_letter): 
                return None
            if (tt.length_char == 1 and ((tt.isValue("X", None) or tt.isValue("Х", None)))): 
                return None
        if (not tt.chars.is_all_lower): 
            ss = (Utils.asObjectOrNull(tt, TextToken)).term
            if (ss == "Я" or ss == "Й" or ss == "Е"): 
                pass
            elif (len(ss) == 2 and ((ss[1] == 'Я' or ss[1] == 'Й' or ss[1] == 'Е'))): 
                pass
            else: 
                return None
        if ((Utils.asObjectOrNull(tt, TextToken)).term == "М"): 
            if (tt.previous is None or not tt.previous.is_hiphen): 
                return None
        dig = (val % (10))
        vars0_ = Morphology.getAllWordforms(NumberHelper.__m_samples[dig], MorphLang())
        if (vars0_ is None or len(vars0_) == 0): 
            return None
        for v in vars0_: 
            if (v.class0_.is_adjective and LanguageHelper.endsWith(v.normal_case, s) and v.number != MorphNumber.UNDEFINED): 
                if (mc is None): 
                    mc = MorphCollection()
                ok = False
                for it in mc.items: 
                    if (it.class0_ == v.class0_ and it.number == v.number and ((it.gender == v.gender or v.number == MorphNumber.PLURAL))): 
                        it.case_ = (it.case_) | v.case_
                        ok = True
                        break
                if (not ok): 
                    mc.addItem(MorphBaseInfo(v))
        if (tt.morph.language.is_ua and mc is None and s == "Ї"): 
            mc = MorphCollection()
            mc.addItem(MorphBaseInfo._new602(MorphClass.ADJECTIVE))
        if (mc is not None): 
            return MetaToken._new600(tt, tt, mc)
        if ((((len(s) < 3) and not tt.is_whitespace_before and tt.previous is not None) and tt.previous.is_hiphen and not tt.previous.is_whitespace_before) and tt.whitespaces_after_count == 1 and s != "А"): 
            return MetaToken._new600(tt, tt, MorphCollection._new604(MorphClass.ADJECTIVE))
        return None
    
    @staticmethod
    def getNumberAdjective(value : int, gender : 'MorphGender', num : 'MorphNumber') -> str:
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
    def getNumberRoman(val : int) -> str:
        """ Получить для числа римскую запись
        
        Args:
            val(int): 
        
        """
        if (val > 0 and val <= len(NumberHelper._m_romans)): 
            return NumberHelper._m_romans[val - 1]
        return str(val)
    
    @staticmethod
    def tryParseFloatNumber(t : 'Token') -> 'NumberExToken':
        """ Выделить дробное число
        
        Args:
            t(Token): начальный токен
        
        """
        from pullenti.ner.core.NumberExToken import NumberExToken
        return NumberExToken.tryParseFloatNumber(t, False)
    
    @staticmethod
    def tryParseNumberWithPostfix(t : 'Token') -> 'NumberExToken':
        """ Выделение стандартных мер, типа: 10 кв.м.
        
        Args:
            t(Token): начальный токен
        
        """
        from pullenti.ner.core.NumberExToken import NumberExToken
        return NumberExToken.tryParseNumberWithPostfix(t)
    
    @staticmethod
    def tryAttachPostfixOnly(t : 'Token') -> 'NumberExToken':
        """ Это попробовать только тип (постфикс) без самого числа.
         Например, куб.м.
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.core.NumberExToken import NumberExToken
        return NumberExToken.tryAttachPostfixOnly(t)
    
    @staticmethod
    def _isMoneyChar(t : 'Token') -> str:
        """ Если этообозначение денежной единицы (н-р, $), то возвращает код валюты
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.TextToken import TextToken
        if (not ((isinstance(t, TextToken))) or t.length_char != 1): 
            return None
        ch = (Utils.asObjectOrNull(t, TextToken)).term[0]
        if (ch == '$'): 
            return "USD"
        if (ch == '£' or ch == (chr(0xA3)) or ch == (chr(0x20A4))): 
            return "GBP"
        if (ch == '€'): 
            return "EUR"
        if (ch == '¥' or ch == (chr(0xA5))): 
            return "JPY"
        if (ch == (chr(0x20A9))): 
            return "KRW"
        if (ch == (chr(0xFFE5)) or ch == 'Ұ' or ch == 'Ұ'): 
            return "CNY"
        if (ch == (chr(0x20BD))): 
            return "RUB"
        if (ch == (chr(0x20B4))): 
            return "UAH"
        if (ch == (chr(0x20AB))): 
            return "VND"
        if (ch == (chr(0x20AD))): 
            return "LAK"
        if (ch == (chr(0x20BA))): 
            return "TRY"
        if (ch == (chr(0x20B1))): 
            return "PHP"
        if (ch == (chr(0x17DB))): 
            return "KHR"
        if (ch == (chr(0x20B9))): 
            return "INR"
        if (ch == (chr(0x20A8))): 
            return "IDR"
        if (ch == (chr(0x20B5))): 
            return "GHS"
        if (ch == (chr(0x09F3))): 
            return "BDT"
        if (ch == (chr(0x20B8))): 
            return "KZT"
        if (ch == (chr(0x20AE))): 
            return "MNT"
        if (ch == (chr(0x0192))): 
            return "HUF"
        if (ch == (chr(0x20AA))): 
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
        NumberHelper._m_nums.addStr("ОДИН", 1, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ПЕРВЫЙ", 1 | NumberHelper.__pril_num_tag_bit, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ОДИН", 1, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ПЕРШИЙ", 1 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ОДНА", 1, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ОДНО", 1, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("FIRST", 1 | NumberHelper.__pril_num_tag_bit, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("SEMEL", 1, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("ONE", 1, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("ДВА", 2, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ВТОРОЙ", 2 | NumberHelper.__pril_num_tag_bit, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ДВОЕ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ДВЕ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ДВУХ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ОБА", 2, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ОБЕ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ДВА", 2, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ДРУГИЙ", 2 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ДВОЄ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ДВІ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ДВОХ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ОБОЄ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ОБИДВА", 2, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("SECOND", 2 | NumberHelper.__pril_num_tag_bit, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("BIS", 2, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("TWO", 2, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("ТРИ", 3, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ТРЕТИЙ", 3 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТРЕХ", 3, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ТРОЕ", 3, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ТРИ", 3, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ТРЕТІЙ", 3 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ТРЬОХ", 3, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ТРОЄ", 3, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("THIRD", 3 | NumberHelper.__pril_num_tag_bit, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("TER", 3, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("THREE", 3, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("ЧЕТЫРЕ", 4, MorphLang(), False)
        NumberHelper._m_nums.addStr("ЧЕТВЕРТЫЙ", 4 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ЧЕТЫРЕХ", 4, MorphLang(), False)
        NumberHelper._m_nums.addStr("ЧЕТВЕРО", 4, MorphLang(), False)
        NumberHelper._m_nums.addStr("ЧОТИРИ", 4, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ЧЕТВЕРТИЙ", 4 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ЧОТИРЬОХ", 4, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("FORTH", 4 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("QUATER", 4, MorphLang(), False)
        NumberHelper._m_nums.addStr("FOUR", 4, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("ПЯТЬ", 5, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТЫЙ", 5 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТИ", 5, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТЕРО", 5, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТЬ", 5, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТИЙ", 5 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("FIFTH", 5 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("QUINQUIES", 5, MorphLang(), False)
        NumberHelper._m_nums.addStr("FIVE", 5, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("ШЕСТЬ", 6, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШЕСТОЙ", 6 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШЕСТИ", 6, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШЕСТЕРО", 6, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШІСТЬ", 6, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШОСТИЙ", 6 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("SIX", 6, MorphLang.EN, False)
        NumberHelper._m_nums.addStr("SIXTH", 6 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("SEXIES ", 6, MorphLang(), False)
        NumberHelper._m_nums.addStr("СЕМЬ", 7, MorphLang(), False)
        NumberHelper._m_nums.addStr("СЕДЬМОЙ", 7 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("СЕМИ", 7, MorphLang(), False)
        NumberHelper._m_nums.addStr("СЕМЕРО", 7, MorphLang(), False)
        NumberHelper._m_nums.addStr("СІМ", 7, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СЬОМИЙ", 7 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("SEVEN", 7, MorphLang(), False)
        NumberHelper._m_nums.addStr("SEVENTH", 7 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("SEPTIES", 7, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВОСЕМЬ", 8, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВОСЬМОЙ", 8 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВОСЬМИ", 8, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВОСЬМЕРО", 8, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВІСІМ", 8, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВОСЬМИЙ", 8 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("EIGHT", 8, MorphLang(), False)
        NumberHelper._m_nums.addStr("EIGHTH", 8 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("OCTIES", 8, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТЬ", 9, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТЫЙ", 9 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТИ", 9, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТЕРО", 9, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТЬ", 9, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕВЯТИЙ", 9 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("NINE", 9, MorphLang(), False)
        NumberHelper._m_nums.addStr("NINTH", 9 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("NOVIES", 9, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕСЯТЬ", 10, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕСЯТЫЙ", 10 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕСЯТИ", 10, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕСЯТИРО", 10, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕСЯТЬ", 10, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕСЯТИЙ", 10 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("TEN", 10, MorphLang(), False)
        NumberHelper._m_nums.addStr("TENTH", 10 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("DECIES", 10, MorphLang(), False)
        NumberHelper._m_nums.addStr("ОДИННАДЦАТЬ", 11, MorphLang(), False)
        NumberHelper._m_nums.addStr("ОДИНАДЦАТЬ", 11, MorphLang(), False)
        NumberHelper._m_nums.addStr("ОДИННАДЦАТЫЙ", 11 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ОДИННАДЦАТИ", 11, MorphLang(), False)
        NumberHelper._m_nums.addStr("ОДИННАДЦАТИРО", 11, MorphLang(), False)
        NumberHelper._m_nums.addStr("ОДИНАДЦЯТЬ", 11, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ОДИНАДЦЯТИЙ", 11 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ОДИНАДЦЯТИ", 11, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ELEVEN", 11, MorphLang(), False)
        NumberHelper._m_nums.addStr("ELEVENTH", 11 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВЕНАДЦАТЬ", 12, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВЕНАДЦАТЫЙ", 12 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВЕНАДЦАТИ", 12, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВАНАДЦЯТЬ", 12, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВАНАДЦЯТИЙ", 12 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВАНАДЦЯТИ", 12, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("TWELVE", 12, MorphLang(), False)
        NumberHelper._m_nums.addStr("TWELFTH", 12 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТРИНАДЦАТЬ", 13, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТРИНАДЦАТЫЙ", 13 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТРИНАДЦАТИ", 13, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТРИНАДЦЯТЬ", 13, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРИНАДЦЯТИЙ", 13 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРИНАДЦЯТИ", 13, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("THIRTEEN", 13, MorphLang(), False)
        NumberHelper._m_nums.addStr("THIRTEENTH", 13 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ЧЕТЫРНАДЦАТЬ", 14, MorphLang(), False)
        NumberHelper._m_nums.addStr("ЧЕТЫРНАДЦАТЫЙ", 14 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ЧЕТЫРНАДЦАТИ", 14, MorphLang(), False)
        NumberHelper._m_nums.addStr("ЧОТИРНАДЦЯТЬ", 14, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ЧОТИРНАДЦЯТИЙ", 14 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ЧОТИРНАДЦЯТИ", 14, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("FOURTEEN", 14, MorphLang(), False)
        NumberHelper._m_nums.addStr("FOURTEENTH", 14 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТНАДЦАТЬ", 15, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТНАДЦАТЫЙ", 15 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТНАДЦАТИ", 15, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТНАДЦЯТЬ", 15, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТНАДЦЯТИЙ", 15 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТНАДЦЯТИ", 15, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("FIFTEEN", 15, MorphLang(), False)
        NumberHelper._m_nums.addStr("FIFTEENTH", 15 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШЕСТНАДЦАТЬ", 16, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШЕСТНАДЦАТЫЙ", 16 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШЕСТНАДЦАТИ", 16, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШІСТНАДЦЯТЬ", 16, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШІСТНАДЦЯТИЙ", 16 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШІСТНАДЦЯТИ", 16, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("SIXTEEN", 16, MorphLang(), False)
        NumberHelper._m_nums.addStr("SIXTEENTH", 16 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("СЕМНАДЦАТЬ", 17, MorphLang(), False)
        NumberHelper._m_nums.addStr("СЕМНАДЦАТЫЙ", 17 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("СЕМНАДЦАТИ", 17, MorphLang(), False)
        NumberHelper._m_nums.addStr("СІМНАДЦЯТЬ", 17, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СІМНАДЦЯТИЙ", 17 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СІМНАДЦЯТИ", 17, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("SEVENTEEN", 17, MorphLang(), False)
        NumberHelper._m_nums.addStr("SEVENTEENTH", 17 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВОСЕМНАДЦАТЬ", 18, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВОСЕМНАДЦАТЫЙ", 18 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВОСЕМНАДЦАТИ", 18, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВІСІМНАДЦЯТЬ", 18, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВІСІМНАДЦЯТИЙ", 18 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВІСІМНАДЦЯТИ", 18, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("EIGHTEEN", 18, MorphLang(), False)
        NumberHelper._m_nums.addStr("EIGHTEENTH", 18 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТНАДЦАТЬ", 19, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТНАДЦАТЫЙ", 19 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТНАДЦАТИ", 19, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТНАДЦЯТЬ", 19, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕВЯТНАДЦЯТИЙ", 19 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕВЯТНАДЦЯТИ", 19, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("NINETEEN", 19, MorphLang(), False)
        NumberHelper._m_nums.addStr("NINETEENTH", 19 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВАДЦАТЬ", 20, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВАДЦАТЫЙ", 20 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВАДЦАТИ", 20, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВАДЦЯТЬ", 20, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВАДЦЯТИЙ", 20 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВАДЦЯТИ", 20, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("TWENTY", 20, MorphLang(), False)
        NumberHelper._m_nums.addStr("TWENTIETH", 20 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТРИДЦАТЬ", 30, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТРИДЦАТЫЙ", 30 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТРИДЦАТИ", 30, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТРИДЦЯТЬ", 30, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРИДЦЯТИЙ", 30 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРИДЦЯТИ", 30, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("THIRTY", 30, MorphLang(), False)
        NumberHelper._m_nums.addStr("THIRTIETH", 30 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("СОРОК", 40, MorphLang(), False)
        NumberHelper._m_nums.addStr("СОРОКОВОЙ", 40 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("СОРОКА", 40, MorphLang(), False)
        NumberHelper._m_nums.addStr("СОРОК", 40, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СОРОКОВИЙ", 40 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("FORTY", 40, MorphLang(), False)
        NumberHelper._m_nums.addStr("FORTIETH", 40 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТЬДЕСЯТ", 50, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТИДЕСЯТЫЙ", 50 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТИДЕСЯТИ", 50, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТДЕСЯТ", 50, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТДЕСЯТИЙ", 50 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТДЕСЯТИ", 50, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("FIFTY", 50, MorphLang(), False)
        NumberHelper._m_nums.addStr("FIFTIETH", 50 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШЕСТЬДЕСЯТ", 60, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШЕСТИДЕСЯТЫЙ", 60 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШЕСТИДЕСЯТИ", 60, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШІСТДЕСЯТ", 60, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШЕСИДЕСЯТЫЙ", 60 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШІСТДЕСЯТИ", 60, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("SIXTY", 60, MorphLang(), False)
        NumberHelper._m_nums.addStr("SIXTIETH", 60 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("СЕМЬДЕСЯТ", 70, MorphLang(), False)
        NumberHelper._m_nums.addStr("СЕМИДЕСЯТЫЙ", 70 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("СЕМИДЕСЯТИ", 70, MorphLang(), False)
        NumberHelper._m_nums.addStr("СІМДЕСЯТ", 70, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СІМДЕСЯТИЙ", 70 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СІМДЕСЯТИ", 70, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("SEVENTY", 70, MorphLang(), False)
        NumberHelper._m_nums.addStr("SEVENTIETH", 70 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("SEVENTIES", 70 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВОСЕМЬДЕСЯТ", 80, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВОСЬМИДЕСЯТЫЙ", 80 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВОСЬМИДЕСЯТИ", 80, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВІСІМДЕСЯТ", 80, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВОСЬМИДЕСЯТИЙ", 80 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВІСІМДЕСЯТИ", 80, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("EIGHTY", 80, MorphLang(), False)
        NumberHelper._m_nums.addStr("EIGHTIETH", 80 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("EIGHTIES", 80 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯНОСТО", 90, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯНОСТЫЙ", 90 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯНОСТО", 90, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕВЯНОСТИЙ", 90 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("NINETY", 90, MorphLang(), False)
        NumberHelper._m_nums.addStr("NINETIETH", 90 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("NINETIES", 90 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("СТО", 100, MorphLang(), False)
        NumberHelper._m_nums.addStr("СОТЫЙ", 100 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("СТА", 100, MorphLang(), False)
        NumberHelper._m_nums.addStr("СТО", 100, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СОТИЙ", 100 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("HUNDRED", 100, MorphLang(), False)
        NumberHelper._m_nums.addStr("HUNDREDTH", 100 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВЕСТИ", 200, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВУХСОТЫЙ", 200 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВУХСОТ", 200, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВІСТІ", 200, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВОХСОТИЙ", 200 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВОХСОТ", 200, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРИСТА", 300, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТРЕХСОТЫЙ", 300 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТРЕХСОТ", 300, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТРИСТА", 300, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРЬОХСОТИЙ", 300 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРЬОХСОТ", 300, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ЧЕТЫРЕСТА", 400, MorphLang(), False)
        NumberHelper._m_nums.addStr("ЧЕТЫРЕХСОТЫЙ", 400 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ЧОТИРИСТА", 400, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ЧОТИРЬОХСОТИЙ", 400 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТЬСОТ", 500, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТИСОТЫЙ", 500 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ПЯТСОТ", 500, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТИСОТИЙ", 500 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШЕСТЬСОТ", 600, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШЕСТИСОТЫЙ", 600 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ШІСТСОТ", 600, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШЕСТИСОТИЙ", 600 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СЕМЬСОТ", 700, MorphLang(), False)
        NumberHelper._m_nums.addStr("СЕМИСОТЫЙ", 700 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("СІМСОТ", 700, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СЕМИСОТИЙ", 700 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВОСЕМЬСОТ", 800, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВОСЕМЬСОТЫЙ", 800 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВОСЬМИСОТЫЙ", 800 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ВІСІМСОТ", 800, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВОСЬМИСОТЫЙ", 800 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕВЯТЬСОТ", 900, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТЬСОТЫЙ", 900 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТИСОТЫЙ", 900 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТСОТ", 900, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕВЯТЬСОТЫЙ", 900 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДЕВЯТИСОТИЙ", 900 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТЫС", 1000, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТЫСЯЧА", 1000, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТЫСЯЧНЫЙ", 1000 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ТИС", 1000, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТИСЯЧА", 1000, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТИСЯЧНИЙ", 1000 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВУХТЫСЯЧНЫЙ", 2000 | NumberHelper.__pril_num_tag_bit, MorphLang(), False)
        NumberHelper._m_nums.addStr("ДВОХТИСЯЧНИЙ", 2000 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("МИЛЛИОН", 1000000, MorphLang(), False)
        NumberHelper._m_nums.addStr("МЛН", 1000000, MorphLang(), False)
        NumberHelper._m_nums.addStr("МІЛЬЙОН", 1000000, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("МИЛЛИАРД", 1000000000, MorphLang(), False)
        NumberHelper._m_nums.addStr("МІЛЬЯРД", 1000000000, MorphLang.UA, False)
    
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