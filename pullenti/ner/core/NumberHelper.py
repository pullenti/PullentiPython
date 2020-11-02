# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import math
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.core.NumberExToken import NumberExToken
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.Token import Token
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection

class NumberHelper:
    """ Работа с числовыми значениями
    
    Хелпер числовых представлений
    """
    
    @staticmethod
    def _try_parse_number(token : 'Token') -> 'NumberToken':
        """ Попробовать создать числительное (без знака, целочисленное).
        Внимание! Этот метод всегда вызывается процессором при формировании цепочки токенов в методе Process(),
        так что все NumberToken уже созданы в основной цепочке, сфорированной для текста.
        
        Args:
            token(Token): начальный токен
        
        Returns:
            NumberToken: число-метатокен
        """
        return NumberHelper.__try_parse(token, None)
    
    @staticmethod
    def __try_parse(token : 'Token', prev_val : 'NumberToken'=None) -> 'NumberToken':
        if (isinstance(token, NumberToken)): 
            return Utils.asObjectOrNull(token, NumberToken)
        tt = Utils.asObjectOrNull(token, TextToken)
        if (tt is None): 
            return None
        et = tt
        val = None
        typ = NumberSpellingType.DIGIT
        term = tt.term
        if (str.isdigit(term[0])): 
            val = term
        if (val is not None): 
            hiph = False
            if ((isinstance(et.next0_, TextToken)) and et.next0_.is_hiphen): 
                if ((et.whitespaces_after_count < 2) and (et.next0_.whitespaces_after_count < 2)): 
                    et = (Utils.asObjectOrNull(et.next0_, TextToken))
                    hiph = True
            mc = None
            if (hiph or not et.is_whitespace_after): 
                rr = NumberHelper.__analize_number_tail(Utils.asObjectOrNull(et.next0_, TextToken), val)
                if (rr is None): 
                    et = tt
                else: 
                    mc = rr.morph
                    et = (Utils.asObjectOrNull(rr.end_token, TextToken))
            else: 
                et = tt
            if (et.next0_ is not None and et.next0_.is_char('(')): 
                num2 = NumberHelper._try_parse_number(et.next0_.next0_)
                if ((num2 is not None and num2.value == val and num2.end_token.next0_ is not None) and num2.end_token.next0_.is_char(')')): 
                    et = (Utils.asObjectOrNull(num2.end_token.next0_, TextToken))
            while (isinstance(et.next0_, TextToken)) and not (isinstance(et.previous, NumberToken)) and et.is_whitespace_before:
                if (et.whitespaces_after_count != 1): 
                    break
                sss = et.next0_.term
                if (sss == "000"): 
                    val = (val + "000")
                    et = (Utils.asObjectOrNull(et.next0_, TextToken))
                    continue
                if (str.isdigit(sss[0]) and len(sss) == 3): 
                    val2 = val
                    ttt = et.next0_
                    first_pass3554 = True
                    while True:
                        if first_pass3554: first_pass3554 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        ss = ttt.get_source_text()
                        if (ttt.whitespaces_before_count == 1 and ttt.length_char == 3 and str.isdigit(ss[0])): 
                            wrapii502 = RefOutArgWrapper(0)
                            inoutres503 = Utils.tryParseInt(ss, wrapii502)
                            ii = wrapii502.value
                            if (not inoutres503): 
                                break
                            val2 += ss
                            continue
                        if ((ttt.is_char_of(".,") and not ttt.is_whitespace_before and not ttt.is_whitespace_after) and ttt.next0_ is not None and str.isdigit(ttt.next0_.get_source_text()[0])): 
                            if (ttt.next0_.is_whitespace_after and (isinstance(ttt.previous, TextToken))): 
                                et = (Utils.asObjectOrNull(ttt.previous, TextToken))
                                val = val2
                                break
                        if (((((ttt.is_value("МИЛЛИАРД", "МІЛЬЯРД") or ttt.is_value("BILLION", None) or ttt.is_value("BN", None)) or ttt.is_value("МЛРД", None) or ttt.is_value("МИЛЛИОН", "МІЛЬЙОН")) or ttt.is_value("MILLION", None) or ttt.is_value("МЛН", None)) or ttt.is_value("ТЫСЯЧА", "ТИСЯЧА") or ttt.is_value("THOUSAND", None)) or ttt.is_value("ТЫС", None) or ttt.is_value("ТИС", None)): 
                            et = (Utils.asObjectOrNull(ttt.previous, TextToken))
                            val = val2
                            break
                        break
                break
            for k in range(3):
                if ((isinstance(et.next0_, TextToken)) and et.next0_.chars.is_letter): 
                    tt = (Utils.asObjectOrNull(et.next0_, TextToken))
                    t0 = et
                    coef = None
                    if (k == 0): 
                        coef = "000000000"
                        if (tt.is_value("МИЛЛИАРД", "МІЛЬЯРД") or tt.is_value("BILLION", None) or tt.is_value("BN", None)): 
                            et = tt
                            val += coef
                        elif (tt.is_value("МЛРД", None)): 
                            et = tt
                            val += coef
                            if ((isinstance(et.next0_, TextToken)) and et.next0_.is_char('.')): 
                                et = (Utils.asObjectOrNull(et.next0_, TextToken))
                        else: 
                            continue
                    elif (k == 1): 
                        coef = "000000"
                        if (tt.is_value("МИЛЛИОН", "МІЛЬЙОН") or tt.is_value("MILLION", None)): 
                            et = tt
                            val += coef
                        elif (tt.is_value("МЛН", None)): 
                            et = tt
                            val += coef
                            if ((isinstance(et.next0_, TextToken)) and et.next0_.is_char('.')): 
                                et = (Utils.asObjectOrNull(et.next0_, TextToken))
                        elif ((isinstance(tt, TextToken)) and tt.term == "M"): 
                            if (NumberHelper._is_money_char(et.previous) is not None): 
                                et = tt
                                val += coef
                            else: 
                                break
                        else: 
                            continue
                    else: 
                        coef = "000"
                        if (tt.is_value("ТЫСЯЧА", "ТИСЯЧА") or tt.is_value("THOUSAND", None)): 
                            et = tt
                            val += coef
                        elif (tt.is_value("ТЫС", None) or tt.is_value("ТИС", None)): 
                            et = tt
                            val += coef
                            if ((isinstance(et.next0_, TextToken)) and et.next0_.is_char('.')): 
                                et = (Utils.asObjectOrNull(et.next0_, TextToken))
                        else: 
                            break
                    if (((t0 == token and t0.length_char <= 3 and t0.previous is not None) and not t0.is_whitespace_before and t0.previous.is_char_of(",.")) and not t0.previous.is_whitespace_before and (((isinstance(t0.previous.previous, NumberToken)) or prev_val is not None))): 
                        if (t0.length_char == 1): 
                            val = val[0:0+len(val) - 1]
                        elif (t0.length_char == 2): 
                            val = val[0:0+len(val) - 2]
                        else: 
                            val = val[0:0+len(val) - 3]
                        hi = (t0.previous.previous.value if isinstance(t0.previous.previous, NumberToken) else prev_val.value)
                        cou = len(coef) - len(val)
                        while cou > 0: 
                            hi = (hi + "0")
                            cou -= 1
                        val = (hi + val)
                        token = t0.previous.previous
                    next0_ = NumberHelper.__try_parse(et.next0_, None)
                    if (next0_ is None or len(next0_.value) > len(coef)): 
                        break
                    tt1 = next0_.end_token
                    if (((isinstance(tt1.next0_, TextToken)) and not tt1.is_whitespace_after and tt1.next0_.is_char_of(".,")) and not tt1.next0_.is_whitespace_after): 
                        re1 = NumberHelper.__try_parse(tt1.next0_.next0_, next0_)
                        if (re1 is not None and re1.begin_token == next0_.begin_token): 
                            next0_ = re1
                    if (len(val) > len(next0_.value)): 
                        val = val[0:0+len(val) - len(next0_.value)]
                    val += next0_.value
                    et = (Utils.asObjectOrNull(next0_.end_token, TextToken))
                    break
            res = NumberToken._new504(token, et, val, typ, mc)
            if (et.next0_ is not None and (len(res.value) < 4) and ((et.next0_.is_hiphen or et.next0_.is_value("ДО", None)))): 
                tt1 = et.next0_.next0_
                first_pass3555 = True
                while True:
                    if first_pass3555: first_pass3555 = False
                    else: tt1 = tt1.next0_
                    if (not (tt1 is not None)): break
                    if (not (isinstance(tt1, TextToken))): 
                        break
                    if (str.isdigit(tt1.term[0])): 
                        continue
                    if (tt1.is_char_of(",.") or NumberHelper._is_money_char(tt1) is not None): 
                        continue
                    if (tt1.is_value("МИЛЛИОН", "МІЛЬЙОН") or tt1.is_value("МЛН", None) or tt1.is_value("MILLION", None)): 
                        res.value = res.value + "000000"
                    elif ((tt1.is_value("МИЛЛИАРД", "МІЛЬЯРД") or tt1.is_value("МЛРД", None) or tt1.is_value("BILLION", None)) or tt1.is_value("BN", None)): 
                        res.value = res.value + "000000000"
                    elif (tt1.is_value("ТЫСЯЧА", "ТИСЯЧА") or tt1.is_value("ТЫС", "ТИС") or tt1.is_value("THOUSAND", None)): 
                        res.value = res.value + "1000"
                    break
            return res
        int_val = 0
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
            num = NumberHelper._m_nums.try_parse(t, TerminParseAttr.FULLWORDSONLY)
            if (num is None): 
                break
            j = (num.termin.tag)
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
                int_val += (loc_value * j)
                loc_value = 0
            else: 
                if (loc_value > 0 and loc_value <= j): 
                    break
                loc_value += j
            et = t
            if (j == 1000 or j == 1000000): 
                if ((isinstance(et.next0_, TextToken)) and et.next0_.is_char('.')): 
                    et = Utils.asObjectOrNull(et.next0_, TextToken)
                    t = et
            jprev = j
            t = (Utils.asObjectOrNull(t.next0_, TextToken))
        if (loc_value > 0): 
            int_val += loc_value
        if (int_val == 0 or et is None): 
            return None
        nt = NumberToken(tt, et, str(int_val), NumberSpellingType.WORDS)
        if (et.morph is not None): 
            nt.morph = MorphCollection(et.morph)
            for wff in et.morph.items: 
                wf = Utils.asObjectOrNull(wff, MorphWordForm)
                if (wf is not None and wf.misc is not None and "собир." in wf.misc.attrs): 
                    nt.morph.class0_ = MorphClass.NOUN
                    break
            if (not is_adj): 
                nt.morph.remove_items((MorphClass.ADJECTIVE) | MorphClass.NOUN, False)
                if (nt.morph.class0_.is_undefined): 
                    nt.morph.class0_ = MorphClass.NOUN
            if (et.chars.is_latin_letter and is_adj): 
                nt.morph.class0_ = MorphClass.ADJECTIVE
        return nt
    
    @staticmethod
    def try_parse_roman(t : 'Token') -> 'NumberToken':
        """ Попробовать выделить число в римской записи
        
        Args:
            t(Token): начальный токен
        
        Returns:
            NumberToken: числовой метатокен или null
        
        """
        if (isinstance(t, NumberToken)): 
            return Utils.asObjectOrNull(t, NumberToken)
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None or not t.chars.is_letter): 
            return None
        term = tt.term
        if (not NumberHelper.__is_rom_val(term)): 
            return None
        if (tt.morph.class0_.is_preposition): 
            if (tt.chars.is_all_lower): 
                return None
        res = NumberToken(t, t, "", NumberSpellingType.ROMAN)
        nums = list()
        val = 0
        while t is not None: 
            if (t != res.begin_token and t.is_whitespace_before): 
                break
            if (not (isinstance(t, TextToken))): 
                break
            term = t.term
            if (not NumberHelper.__is_rom_val(term)): 
                break
            for s in term: 
                i = NumberHelper.__rom_val(s)
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
                    val += 4
                    i += 1
                elif (nums[i] == 1 and nums[i + 1] == 10): 
                    val += 9
                    i += 1
                elif (nums[i] == 10 and nums[i + 1] == 50): 
                    val += 40
                    i += 1
                elif (nums[i] == 10 and nums[i + 1] == 100): 
                    val += 90
                    i += 1
                else: 
                    val += nums[i]
            else: 
                val += nums[i]
            i += 1
        res.int_value = val
        hiph = False
        et = res.end_token.next0_
        if (et is None): 
            return res
        if (et.next0_ is not None and et.next0_.is_hiphen): 
            et = et.next0_
            hiph = True
        if (hiph or not et.is_whitespace_after): 
            mc = NumberHelper.__analize_number_tail(Utils.asObjectOrNull(et.next0_, TextToken), res.value)
            if (mc is not None): 
                res.end_token = mc.end_token
                res.morph = mc.morph
        if ((res.begin_token == res.end_token and val == 1 and res.begin_token.chars.is_all_lower) and res.begin_token.morph.language.is_ua): 
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
    def __is_rom_val(str0_ : str) -> bool:
        for ch in str0_: 
            if (NumberHelper.__rom_val(ch) < 1): 
                return False
        return True
    
    @staticmethod
    def try_parse_roman_back(token : 'Token') -> 'NumberToken':
        """ Выделить число в римской записи в обратном порядке
        
        Args:
            token(Token): токен на предполагаемой римской цифрой
        
        Returns:
            NumberToken: число-метатокен или null
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
            t(Token): начальный токен
        
        Returns:
            NumberToken: числовой метатокен или null
        """
        if (t is None): 
            return None
        nt = Utils.asObjectOrNull(t, NumberToken)
        nt_next = None
        if (nt is not None): 
            nt_next = nt.next0_
        else: 
            if (t.is_value("AGED", None) and (isinstance(t.next0_, NumberToken))): 
                return NumberToken(t, t.next0_, t.next0_.value, NumberSpellingType.AGE)
            nt = NumberHelper.try_parse_roman(t)
            if ((nt) is not None): 
                nt_next = nt.end_token.next0_
        if (nt is not None): 
            if (nt_next is not None): 
                t1 = nt_next
                if (t1.is_hiphen): 
                    t1 = t1.next0_
                if (isinstance(t1, TextToken)): 
                    v = t1.term
                    if ((v == "ЛЕТ" or v == "ЛЕТИЯ" or v == "ЛЕТИЕ") or v == "РІЧЧЯ"): 
                        return NumberToken._new504(t, t1, nt.value, NumberSpellingType.AGE, t1.morph)
                    if (t1.is_value("ЛЕТНИЙ", "РІЧНИЙ")): 
                        return NumberToken._new504(t, t1, nt.value, NumberSpellingType.AGE, t1.morph)
                    if (v == "Л" or ((v == "Р" and nt.morph.language.is_ua))): 
                        return NumberToken(t, (t1.next0_ if t1.next0_ is not None and t1.next0_.is_char('.') else t1), nt.value, NumberSpellingType.AGE)
            return None
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        s = tt.term
        if (LanguageHelper.ends_with_ex(s, "ЛЕТИЕ", "ЛЕТИЯ", "РІЧЧЯ", None)): 
            term = NumberHelper._m_nums.find(s[0:0+len(s) - 5])
            if (term is not None): 
                return NumberToken._new504(tt, tt, str(term.tag), NumberSpellingType.AGE, tt.morph)
        s = tt.lemma
        if (LanguageHelper.ends_with_ex(s, "ЛЕТНИЙ", "РІЧНИЙ", None, None)): 
            term = NumberHelper._m_nums.find(s[0:0+len(s) - 6])
            if (term is not None): 
                return NumberToken._new504(tt, tt, str(term.tag), NumberSpellingType.AGE, tt.morph)
        return None
    
    @staticmethod
    def try_parse_anniversary(t : 'Token') -> 'NumberToken':
        """ Выделение годовщин и летий (XX-летие) ...
        
        Args:
            t(Token): начальный токен
        
        Returns:
            NumberToken: числовой метатокен или null
        """
        nt = Utils.asObjectOrNull(t, NumberToken)
        t1 = None
        if (nt is not None): 
            t1 = nt.next0_
        else: 
            nt = NumberHelper.try_parse_roman(t)
            if ((nt) is None): 
                if (isinstance(t, TextToken)): 
                    v = t.term
                    num = 0
                    if (v.endswith("ЛЕТИЯ") or v.endswith("ЛЕТИЕ")): 
                        if (v.startswith("ВОСЕМЬСОТ") or v.startswith("ВОСЬМИСОТ")): 
                            num = 800
                    if (num > 0): 
                        return NumberToken(t, t, str(num), NumberSpellingType.AGE)
                return None
            t1 = nt.end_token.next0_
        if (t1 is None): 
            return None
        if (t1.is_hiphen): 
            t1 = t1.next0_
        if (isinstance(t1, TextToken)): 
            v = t1.term
            if ((v == "ЛЕТ" or v == "ЛЕТИЯ" or v == "ЛЕТИЕ") or t1.is_value("ГОДОВЩИНА", None)): 
                return NumberToken(t, t1, nt.value, NumberSpellingType.AGE)
            if (t1.morph.language.is_ua): 
                if (v == "РОКІВ" or v == "РІЧЧЯ" or t1.is_value("РІЧНИЦЯ", None)): 
                    return NumberToken(t, t1, nt.value, NumberSpellingType.AGE)
        return None
    
    __m_samples = None
    
    @staticmethod
    def __analize_number_tail(tt : 'TextToken', val : str) -> 'MetaToken':
        if (not (isinstance(tt, TextToken))): 
            return None
        s = tt.term
        mc = None
        if (not tt.chars.is_letter): 
            if (((s == "<" or s == "(")) and (isinstance(tt.next0_, TextToken))): 
                s = tt.next0_.term
                if ((s == "TH" or s == "ST" or s == "RD") or s == "ND"): 
                    if (tt.next0_.next0_ is not None and tt.next0_.next0_.is_char_of(">)")): 
                        mc = MorphCollection()
                        mc.class0_ = MorphClass.ADJECTIVE
                        mc.language = MorphLang.EN
                        return MetaToken._new509(tt, tt.next0_.next0_, mc)
            return None
        if ((s == "TH" or s == "ST" or s == "RD") or s == "ND"): 
            mc = MorphCollection()
            mc.class0_ = MorphClass.ADJECTIVE
            mc.language = MorphLang.EN
            return MetaToken._new509(tt, tt, mc)
        if (not tt.chars.is_cyrillic_letter): 
            return None
        if (not tt.is_whitespace_after): 
            if (tt.next0_ is not None and tt.next0_.chars.is_letter): 
                return None
            if (tt.length_char == 1 and ((tt.is_value("X", None) or tt.is_value("Х", None)))): 
                return None
        if (not tt.chars.is_all_lower): 
            ss = tt.term
            if (ss == "Я" or ss == "Й" or ss == "Е"): 
                pass
            elif (len(ss) == 2 and ((ss[1] == 'Я' or ss[1] == 'Й' or ss[1] == 'Е'))): 
                pass
            else: 
                return None
        if (tt.term == "М"): 
            if (tt.previous is None or not tt.previous.is_hiphen): 
                return None
        if (Utils.isNullOrEmpty(val)): 
            return None
        dig = ((ord(val[len(val) - 1])) - (ord('0')))
        if ((dig < 0) or dig >= 10): 
            return None
        vars0_ = MorphologyService.get_all_wordforms(NumberHelper.__m_samples[dig], None)
        if (vars0_ is None or len(vars0_) == 0): 
            return None
        for v in vars0_: 
            if (v.class0_.is_adjective and LanguageHelper.ends_with(v.normal_case, s) and v.number != MorphNumber.UNDEFINED): 
                if (mc is None): 
                    mc = MorphCollection()
                ok = False
                for it in mc.items: 
                    if (it.class0_ == v.class0_ and it.number == v.number and ((it.gender == v.gender or v.number == MorphNumber.PLURAL))): 
                        it.case_ = (it.case_) | v.case_
                        ok = True
                        break
                if (not ok): 
                    mm = MorphBaseInfo()
                    mm.copy_from(v)
                    mc.add_item(mm)
        if (tt.morph.language.is_ua and mc is None and s == "Ї"): 
            mc = MorphCollection()
            mc.add_item(MorphBaseInfo._new511(MorphClass.ADJECTIVE))
        if (mc is not None): 
            return MetaToken._new509(tt, tt, mc)
        if ((((len(s) < 3) and not tt.is_whitespace_before and tt.previous is not None) and tt.previous.is_hiphen and not tt.previous.is_whitespace_before) and tt.whitespaces_after_count == 1 and s != "А"): 
            return MetaToken._new509(tt, tt, MorphCollection._new513(MorphClass.ADJECTIVE))
        return None
    
    @staticmethod
    def __try_parse_float(t : 'NumberToken', d : float, no_ws : bool) -> 'Token':
        from pullenti.ner.core.internal.NumberExHelper import NumberExHelper
        d.value = (0)
        if (t is None or t.next0_ is None or t.typ != NumberSpellingType.DIGIT): 
            return None
        tt = t.begin_token
        while tt is not None and tt.end_char <= t.end_char: 
            if ((isinstance(tt, TextToken)) and tt.chars.is_letter): 
                return None
            tt = tt.next0_
        kit = t.kit
        ns = None
        sps = None
        t1 = t
        first_pass3556 = True
        while True:
            if first_pass3556: first_pass3556 = False
            else: t1 = t1.next0_
            if (not (t1 is not None)): break
            if (t1.next0_ is None): 
                break
            if (((isinstance(t1.next0_, NumberToken)) and (t1.whitespaces_after_count < 3) and t1.next0_.typ == NumberSpellingType.DIGIT) and t1.next0_.length_char == 3): 
                if (ns is None): 
                    ns = list()
                    ns.append(t)
                    sps = list()
                elif (sps[0] != ' '): 
                    return None
                ns.append(Utils.asObjectOrNull(t1.next0_, NumberToken))
                sps.append(' ')
                continue
            if ((t1.next0_.is_char_of(",.") and (isinstance(t1.next0_.next0_, NumberToken)) and t1.next0_.next0_.typ == NumberSpellingType.DIGIT) and (t1.whitespaces_after_count < 2) and (t1.next0_.whitespaces_after_count < 2)): 
                if (no_ws): 
                    if (t1.is_whitespace_after or t1.next0_.is_whitespace_after): 
                        break
                if (ns is None): 
                    ns = list()
                    ns.append(t)
                    sps = list()
                elif (t1.next0_.is_whitespace_after and t1.next0_.next0_.length_char != 3 and ((('.' if t1.next0_.is_char('.') else ','))) == sps[len(sps) - 1]): 
                    break
                ns.append(Utils.asObjectOrNull(t1.next0_.next0_, NumberToken))
                sps.append(('.' if t1.next0_.is_char('.') else ','))
                t1 = t1.next0_
                continue
            break
        if (sps is None): 
            return None
        is_last_drob = False
        not_set_drob = False
        merge = False
        m_prev_point_char = '.'
        if (len(sps) == 1): 
            if (sps[0] == ' '): 
                is_last_drob = False
            elif (ns[1].length_char != 3): 
                is_last_drob = True
                if (len(ns) == 2): 
                    if (ns[1].end_token.chars.is_letter): 
                        merge = True
                    elif (ns[1].end_token.is_char('.') and ns[1].end_token.previous is not None and ns[1].end_token.previous.chars.is_letter): 
                        merge = True
                    if (ns[1].is_whitespace_before): 
                        if ((isinstance(ns[1].end_token, TextToken)) and ns[1].end_token.term.endswith("000")): 
                            return None
            elif (ns[0].length_char > 3 or ns[0].real_value == 0): 
                is_last_drob = True
            else: 
                ok = True
                if (len(ns) == 2 and ns[1].length_char == 3): 
                    ttt = NumberExHelper._m_postfixes.try_parse(ns[1].end_token.next0_, TerminParseAttr.NO)
                    if (ttt is not None and (Utils.valToEnum(ttt.termin.tag, NumberExType)) == NumberExType.MONEY): 
                        is_last_drob = False
                        ok = False
                        not_set_drob = False
                    elif (ns[1].end_token.next0_ is not None and ns[1].end_token.next0_.is_char('(') and (isinstance(ns[1].end_token.next0_.next0_, NumberToken))): 
                        nt1 = Utils.asObjectOrNull(ns[1].end_token.next0_.next0_, NumberToken)
                        if (nt1.real_value == (((ns[0].real_value * (1000)) + ns[1].real_value))): 
                            is_last_drob = False
                            ok = False
                            not_set_drob = False
                if (ok): 
                    if ("pt" in t.kit.misc_data): 
                        m_prev_point_char = (t.kit.misc_data["pt"])
                    if (m_prev_point_char == sps[0]): 
                        is_last_drob = True
                        not_set_drob = True
                    else: 
                        is_last_drob = False
                        not_set_drob = True
        else: 
            last = sps[len(sps) - 1]
            if (last == ' ' and sps[0] != last): 
                return None
            i = 0
            while i < (len(sps) - 1): 
                if (sps[i] != sps[0]): 
                    return None
                elif (ns[i + 1].length_char != 3): 
                    return None
                i += 1
            if (sps[0] != last): 
                is_last_drob = True
            elif (ns[len(ns) - 1].length_char != 3): 
                return None
            if (ns[0].length_char > 3): 
                return None
        i = 0
        while i < len(ns): 
            if ((i < (len(ns) - 1)) or not is_last_drob): 
                if (i == 0): 
                    d.value = ns[i].real_value
                else: 
                    d.value = ((d.value * (1000)) + ns[i].real_value)
                if (i == (len(ns) - 1) and not not_set_drob): 
                    if (sps[len(sps) - 1] == ','): 
                        m_prev_point_char = '.'
                    elif (sps[len(sps) - 1] == '.'): 
                        m_prev_point_char = ','
            else: 
                if (not not_set_drob): 
                    m_prev_point_char = sps[len(sps) - 1]
                    if (m_prev_point_char == ','): 
                        pass
                if (merge): 
                    sss = str(ns[i].value)
                    kkk = 0
                    while kkk < (len(sss) - ns[i].begin_token.length_char): 
                        d.value *= (10)
                        kkk += 1
                    f2 = ns[i].real_value
                    kkk = 0
                    while kkk < ns[i].begin_token.length_char: 
                        f2 /= (10)
                        kkk += 1
                    d.value += f2
                else: 
                    f2 = ns[i].real_value
                    kkk = 0
                    while kkk < ns[i].length_char: 
                        f2 /= (10)
                        kkk += 1
                    d.value += f2
            i += 1
        if ("pt" in kit.misc_data): 
            kit.misc_data["pt"] = (m_prev_point_char)
        else: 
            kit.misc_data["pt"] = m_prev_point_char
        return ns[len(ns) - 1]
    
    @staticmethod
    def try_parse_real_number(t : 'Token', can_be_integer : bool=False, no_whitespace : bool=False) -> 'NumberToken':
        """ Выделить действительное число, знак также выделяется,
        разделители дроби могут быть точка или запятая, разделителями тысячных
        могут быть точки, пробелы и запятые.
        
        Args:
            t(Token): начальный токен
            can_be_integer(bool): число может быть целым
            no_whitespace(bool): не должно быть пробелов
        
        Returns:
            NumberToken: числовой метатокен или null
        
        """
        is_not = False
        t0 = t
        if (t is not None): 
            if (t.is_hiphen or t.is_value("МИНУС", None)): 
                t = t.next0_
                is_not = True
            elif (t.is_char('+') or t.is_value("ПЛЮС", None)): 
                t = t.next0_
        if ((isinstance(t, TextToken)) and ((t.is_value("НОЛЬ", None) or t.is_value("НУЛЬ", None)))): 
            if (t.next0_ is None): 
                return NumberToken(t, t, "0", NumberSpellingType.WORDS)
            if (t.next0_.is_value("ЦЕЛЫЙ", None)): 
                t = t.next0_
            res0 = NumberToken(t, t.next0_, "0", NumberSpellingType.WORDS)
            t = t.next0_
            if ((isinstance(t, NumberToken)) and t.int_value is not None): 
                val = t.int_value
                if (t.next0_ is not None and val > 0): 
                    if (t.next0_.is_value("ДЕСЯТЫЙ", None)): 
                        res0.end_token = t.next0_
                        res0.real_value = (val) / (10)
                    elif (t.next0_.is_value("СОТЫЙ", None)): 
                        res0.end_token = t.next0_
                        res0.real_value = (val) / (100)
                    elif (t.next0_.is_value("ТЫСЯЧНЫЙ", None)): 
                        res0.end_token = t.next0_
                        res0.real_value = (val) / (1000)
                if (res0.real_value == 0): 
                    res0.end_token = t
                    res0.value = "0.{0}".format(val)
            return res0
        if (isinstance(t, TextToken)): 
            tok = NumberHelper.__m_after_points.try_parse(t, TerminParseAttr.NO)
            if (tok is not None): 
                res0 = NumberExToken(t, tok.end_token, None, NumberSpellingType.WORDS, NumberExType.UNDEFINED)
                res0.real_value = (tok.termin.tag)
                return res0
        if (t is None): 
            return None
        if (not (isinstance(t, NumberToken))): 
            if (t.is_value("СОТНЯ", None)): 
                return NumberToken(t, t, "100", NumberSpellingType.WORDS)
            if (t.is_value("ТЫЩА", None) or t.is_value("ТЫСЯЧА", None)): 
                return NumberToken(t, t, "1000", NumberSpellingType.WORDS)
            return None
        if (t.next0_ is not None and t.next0_.is_value("ЦЕЛЫЙ", None) and (((isinstance(t.next0_.next0_, NumberToken)) or (((isinstance(t.next0_.next0_, TextToken)) and t.next0_.next0_.is_value("НОЛЬ", None)))))): 
            res0 = NumberExToken(t, t.next0_, t.value, NumberSpellingType.WORDS, NumberExType.UNDEFINED)
            t = t.next0_.next0_
            val = 0
            if (isinstance(t, TextToken)): 
                res0.end_token = t
                t = t.next0_
            if (isinstance(t, NumberToken)): 
                res0.end_token = t
                val = t.real_value
                t = t.next0_
            if (t is not None): 
                if (t.is_value("ДЕСЯТЫЙ", None)): 
                    res0.end_token = t
                    res0.real_value = (((val) / (10))) + res0.real_value
                elif (t.is_value("СОТЫЙ", None)): 
                    res0.end_token = t
                    res0.real_value = (((val) / (100))) + res0.real_value
                elif (t.is_value("ТЫСЯЧНЫЙ", None)): 
                    res0.end_token = t
                    res0.real_value = (((val) / (1000))) + res0.real_value
            if (res0.real_value == 0): 
                str0_ = "0.{0}".format(val)
                dd = 0
                wrapdd517 = RefOutArgWrapper(0)
                inoutres518 = Utils.tryParseFloat(str0_, wrapdd517)
                dd = wrapdd517.value
                if (inoutres518): 
                    pass
                else: 
                    wrapdd515 = RefOutArgWrapper(0)
                    inoutres516 = Utils.tryParseFloat(str0_.replace('.', ','), wrapdd515)
                    dd = wrapdd515.value
                    if (inoutres516): 
                        pass
                    else: 
                        return None
                res0.real_value = dd + res0.real_value
            return res0
        wrapd520 = RefOutArgWrapper(0)
        tt = NumberHelper.__try_parse_float(Utils.asObjectOrNull(t, NumberToken), wrapd520, no_whitespace)
        d = wrapd520.value
        if (tt is None): 
            if ((t.next0_ is None or t.is_whitespace_after or t.next0_.chars.is_letter) or can_be_integer): 
                tt = t
                d = t.real_value
            else: 
                return None
        if (is_not): 
            d = (- d)
        if (tt.next0_ is not None and tt.next0_.is_value("ДЕСЯТОК", None)): 
            d *= (10)
            tt = tt.next0_
        return NumberExToken._new519(t0, tt, "", NumberSpellingType.DIGIT, NumberExType.UNDEFINED, d)
    
    @staticmethod
    def get_number_adjective(value : int, gender : 'MorphGender', num : 'MorphNumber') -> str:
        """ Преобразовать целое число в записанное буквами числительное в нужном роде и числе именительного падежа.
        Например, 5 жен.ед. - ПЯТАЯ,  26 мн. - ДВАДЦАТЬ ШЕСТЫЕ.
        
        Args:
            value(int): целочисленное значение
            gender(MorphGender): род
            num(MorphNumber): число
        
        Returns:
            str: значение
        
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
    
    __m_100words = None
    
    __m_10words = None
    
    __m_1words = None
    
    _m_romans = None
    
    @staticmethod
    def get_number_roman(val : int) -> str:
        """ Получить для числа римскую запись
        
        Args:
            val(int): целое число
        
        Returns:
            str: римская запись
        """
        if (val > 0 and val <= len(NumberHelper._m_romans)): 
            return NumberHelper._m_romans[val - 1]
        return str(val)
    
    @staticmethod
    def get_number_string(val : int, units : str=None) -> str:
        """ Получить строковое представление целого числа. Например, GetNumberString(38, "попугай") => "тридцать восемь попугаев".
        
        Args:
            val(int): значение
            units(str): единицы измерения (если не null, то они тоже будут преобразовываться в нужное число)
        
        Returns:
            str: строковое представление (пока на русском языке)
        """
        from pullenti.ner.core.MiscHelper import MiscHelper
        if (val < 0): 
            return "минус " + NumberHelper.get_number_string(- val, units)
        if (val >= 1000000000): 
            vv = math.floor(val / 1000000000)
            res = NumberHelper.get_number_string(vv, "миллиард")
            vv = (val % 1000000000)
            if (vv != 0): 
                res = "{0} {1}".format(res, NumberHelper.get_number_string(vv, units))
            elif (units is not None): 
                res = "{0} {1}".format(res, MiscHelper.get_text_morph_var_by_case_and_number_ex(units, MorphCase.GENITIVE, MorphNumber.PLURAL, None))
            return res.lower()
        if (val >= 1000000): 
            vv = math.floor(val / 1000000)
            res = NumberHelper.get_number_string(vv, "миллион")
            vv = (val % 1000000)
            if (vv != 0): 
                res = "{0} {1}".format(res, NumberHelper.get_number_string(vv, units))
            elif (units is not None): 
                res = "{0} {1}".format(res, MiscHelper.get_text_morph_var_by_case_and_number_ex(units, MorphCase.GENITIVE, MorphNumber.PLURAL, None))
            return res.lower()
        if (val >= 1000): 
            vv = math.floor(val / 1000)
            res = NumberHelper.get_number_string(vv, "тысяча")
            vv = (val % 1000)
            if (vv != 0): 
                res = "{0} {1}".format(res, NumberHelper.get_number_string(vv, units))
            elif (units is not None): 
                res = "{0} {1}".format(res, MiscHelper.get_text_morph_var_by_case_and_number_ex(units, MorphCase.GENITIVE, MorphNumber.PLURAL, None))
            return res.lower()
        if (val >= 100): 
            vv = math.floor(val / 100)
            res = NumberHelper.__m_100words[vv - 1]
            vv = (val % 100)
            if (vv != 0): 
                res = "{0} {1}".format(res, NumberHelper.get_number_string(vv, units))
            elif (units is not None): 
                res = "{0} {1}".format(res, MiscHelper.get_text_morph_var_by_case_and_number_ex(units, MorphCase.GENITIVE, MorphNumber.PLURAL, None))
            return res.lower()
        if (val >= 20): 
            vv = math.floor(val / 10)
            res = NumberHelper.__m_10words[vv - 1]
            vv = (val % 10)
            if (vv != 0): 
                res = "{0} {1}".format(res, NumberHelper.get_number_string(vv, units))
            elif (units is not None): 
                res = "{0} {1}".format(res, MiscHelper.get_text_morph_var_by_case_and_number_ex(units, MorphCase.GENITIVE, MorphNumber.PLURAL, None))
            return res.lower()
        if (units is not None): 
            if (val == 1): 
                bi = MorphologyService.get_word_base_info(units.upper(), None, False, False)
                if (((bi.gender) & (MorphGender.FEMINIE)) == (MorphGender.FEMINIE)): 
                    return "одна " + units
                if (((bi.gender) & (MorphGender.NEUTER)) == (MorphGender.NEUTER)): 
                    return "одно " + units
                return "один " + units
            if (val == 2): 
                bi = MorphologyService.get_word_base_info(units.upper(), None, False, False)
                if (((bi.gender) & (MorphGender.FEMINIE)) == (MorphGender.FEMINIE)): 
                    return "две " + MiscHelper.get_text_morph_var_by_case_and_number_ex(units, None, MorphNumber.PLURAL, None)
            return "{0} {1}".format(NumberHelper.__m_1words[val].lower(), MiscHelper.get_text_morph_var_by_case_and_number_ex(units, MorphCase.GENITIVE, MorphNumber.UNDEFINED, str(val)))
        return NumberHelper.__m_1words[val].lower()
    
    @staticmethod
    def try_parse_number_with_postfix(t : 'Token') -> 'NumberExToken':
        # Выделение стандартных мер, типа: 10 кв.м.
        # УСТАРЕЛО. Вместо этого лучше использовать возможности MeasureReferent.
        from pullenti.ner.core.internal.NumberExHelper import NumberExHelper
        return NumberExHelper.try_parse_number_with_postfix(t)
    
    @staticmethod
    def try_parse_postfix_only(t : 'Token') -> 'NumberExToken':
        # Это попробовать только тип (постфикс) без самого числа.
        # Например, куб.м.
        from pullenti.ner.core.internal.NumberExHelper import NumberExHelper
        return NumberExHelper.try_attach_postfix_only(t)
    
    @staticmethod
    def _is_money_char(t : 'Token') -> str:
        # Если это обозначение денежной единицы (н-р, $), то возвращает код валюты
        if (not (isinstance(t, TextToken)) or t.length_char != 1): 
            return None
        ch = t.term[0]
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
    
    @staticmethod
    def string_to_double(str0_ : str) -> float:
        """ Для парсинга действительного числа из строки используйте эту функцию,
        которая работает назависимо от локализьных настроек и на всех языках программирования.
        
        Args:
            str0_(str): строка с действительным числом
        
        Returns:
            float: double-число или null
        
        """
        if (str0_ == "NaN"): 
            return math.nan
        wrapres523 = RefOutArgWrapper(0)
        inoutres524 = Utils.tryParseFloat(str0_, wrapres523)
        res = wrapres523.value
        if (inoutres524): 
            return res
        wrapres521 = RefOutArgWrapper(0)
        inoutres522 = Utils.tryParseFloat(str0_.replace('.', ','), wrapres521)
        res = wrapres521.value
        if (inoutres522): 
            return res
        return None
    
    @staticmethod
    def double_to_string(d : float) -> str:
        """ Независимо от языка и локальных настроек выводит действительное число в строку,
        разделитель - всегда точка. Ситуация типа 1.0000000001 или 23.7299999999999,
        случающиеся на разных языках, округляются куда надо.
        
        Args:
            d(float): число
        
        Returns:
            str: строковый результат
        
        """
        if (math.isnan(d)): 
            return "NaN"
        res = None
        if (math.trunc(d) == 0.0): 
            res = str(d).replace(",", ".")
        else: 
            rest = math.fabs(d - math.trunc(d))
            if ((rest < 0.000000001) and rest > 0): 
                res = str(math.trunc(d))
                if ((res.find('E') < 0) and (res.find('e') < 0)): 
                    ii = res.find('.')
                    if (ii < 0): 
                        ii = res.find(',')
                    if (ii > 0): 
                        return res[0:0+ii]
                    else: 
                        return res
            else: 
                res = str(d).replace(",", ".")
        if (res.endswith(".0")): 
            res = res[0:0+len(res) - 2]
        i = res.find('e')
        if (i < 0): 
            i = res.find('E')
        if (i > 0): 
            exp0_ = 0
            neg = False
            jj = i + 1
            while jj < len(res): 
                if (res[jj] == '+'): 
                    pass
                elif (res[jj] == '-'): 
                    neg = True
                else: 
                    exp0_ = ((exp0_ * 10) + (((ord(res[jj])) - (ord('0')))))
                jj += 1
            res = res[0:0+i]
            if (res.endswith(".0")): 
                res = res[0:0+len(res) - 2]
            nneg = False
            if (res[0] == '-'): 
                nneg = True
                res = res[1:]
            v1 = io.StringIO()
            v2 = io.StringIO()
            i = res.find('.')
            if (i < 0): 
                print(res, end="", file=v1)
            else: 
                print(res[0:0+i], end="", file=v1)
                print(res[i + 1:], end="", file=v2)
            while exp0_ > 0: 
                if (neg): 
                    if (v1.tell() > 0): 
                        Utils.insertStringIO(v2, 0, Utils.getCharAtStringIO(v1, v1.tell() - 1))
                        Utils.setLengthStringIO(v1, v1.tell() - 1)
                    else: 
                        Utils.insertStringIO(v2, 0, '0')
                elif (v2.tell() > 0): 
                    print(Utils.getCharAtStringIO(v2, 0), end="", file=v1)
                    Utils.removeStringIO(v2, 0, 1)
                else: 
                    print('0', end="", file=v1)
                exp0_ -= 1
            if (v2.tell() == 0): 
                res = Utils.toStringStringIO(v1)
            elif (v1.tell() == 0): 
                res = ("0." + Utils.toStringStringIO(v2))
            else: 
                res = "{0}.{1}".format(Utils.toStringStringIO(v1), Utils.toStringStringIO(v2))
            if (nneg): 
                res = ("-" + res)
        i = res.find('.')
        if (i < 0): 
            return res
        i += 1
        j = (i + 1)
        while j < len(res): 
            if (res[j] == '9'): 
                k = 0
                jj = j
                while jj < len(res): 
                    if (res[jj] != '9'): 
                        break
                    else: 
                        k += 1
                    jj += 1
                if (jj >= len(res) or ((jj == (len(res) - 1) and res[jj] == '8'))): 
                    if (k > 5): 
                        while j > i: 
                            if (res[j] != '9'): 
                                if (res[j] != '.'): 
                                    return "{0}{1}".format(res[0:0+j], (((ord(res[j])) - (ord('0')))) + 1)
                            j -= 1
                        break
            j += 1
        return res
    
    __pril_num_tag_bit = 0x40000000
    
    @staticmethod
    def _initialize() -> None:
        if (NumberHelper._m_nums is not None): 
            return
        NumberHelper._m_nums = TerminCollection()
        NumberHelper._m_nums.all_add_strs_normalized = True
        NumberHelper._m_nums.add_string("ОДИН", 1, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ПЕРВЫЙ", 1 | NumberHelper.__pril_num_tag_bit, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ОДИН", 1, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("ПЕРШИЙ", 1 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("ОДНА", 1, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ОДНО", 1, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("FIRST", 1 | NumberHelper.__pril_num_tag_bit, MorphLang.EN, True)
        NumberHelper._m_nums.add_string("SEMEL", 1, MorphLang.EN, True)
        NumberHelper._m_nums.add_string("ONE", 1, MorphLang.EN, True)
        NumberHelper._m_nums.add_string("ДВА", 2, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ВТОРОЙ", 2 | NumberHelper.__pril_num_tag_bit, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ДВОЕ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ДВЕ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ДВУХ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ОБА", 2, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ОБЕ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ДВА", 2, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("ДРУГИЙ", 2 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("ДВОЄ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("ДВІ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("ДВОХ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("ОБОЄ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("ОБИДВА", 2, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("SECOND", 2 | NumberHelper.__pril_num_tag_bit, MorphLang.EN, True)
        NumberHelper._m_nums.add_string("BIS", 2, MorphLang.EN, True)
        NumberHelper._m_nums.add_string("TWO", 2, MorphLang.EN, True)
        NumberHelper._m_nums.add_string("ТРИ", 3, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ТРЕТИЙ", 3 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ТРЕХ", 3, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ТРОЕ", 3, MorphLang.RU, True)
        NumberHelper._m_nums.add_string("ТРИ", 3, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("ТРЕТІЙ", 3 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("ТРЬОХ", 3, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("ТРОЄ", 3, MorphLang.UA, True)
        NumberHelper._m_nums.add_string("THIRD", 3 | NumberHelper.__pril_num_tag_bit, MorphLang.EN, True)
        NumberHelper._m_nums.add_string("TER", 3, MorphLang.EN, True)
        NumberHelper._m_nums.add_string("THREE", 3, MorphLang.EN, True)
        NumberHelper._m_nums.add_string("ЧЕТЫРЕ", 4, None, False)
        NumberHelper._m_nums.add_string("ЧЕТВЕРТЫЙ", 4 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ЧЕТЫРЕХ", 4, None, False)
        NumberHelper._m_nums.add_string("ЧЕТВЕРО", 4, None, False)
        NumberHelper._m_nums.add_string("ЧОТИРИ", 4, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ЧЕТВЕРТИЙ", 4 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ЧОТИРЬОХ", 4, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("FORTH", 4 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("QUATER", 4, None, False)
        NumberHelper._m_nums.add_string("FOUR", 4, MorphLang.EN, True)
        NumberHelper._m_nums.add_string("ПЯТЬ", 5, None, False)
        NumberHelper._m_nums.add_string("ПЯТЫЙ", 5 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ПЯТИ", 5, None, False)
        NumberHelper._m_nums.add_string("ПЯТЕРО", 5, None, False)
        NumberHelper._m_nums.add_string("ПЯТЬ", 5, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ПЯТИЙ", 5 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("FIFTH", 5 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("QUINQUIES", 5, None, False)
        NumberHelper._m_nums.add_string("FIVE", 5, MorphLang.EN, True)
        NumberHelper._m_nums.add_string("ШЕСТЬ", 6, None, False)
        NumberHelper._m_nums.add_string("ШЕСТОЙ", 6 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ШЕСТИ", 6, None, False)
        NumberHelper._m_nums.add_string("ШЕСТЕРО", 6, None, False)
        NumberHelper._m_nums.add_string("ШІСТЬ", 6, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ШОСТИЙ", 6 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("SIX", 6, MorphLang.EN, False)
        NumberHelper._m_nums.add_string("SIXTH", 6 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("SEXIES ", 6, None, False)
        NumberHelper._m_nums.add_string("СЕМЬ", 7, None, False)
        NumberHelper._m_nums.add_string("СЕДЬМОЙ", 7 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("СЕМИ", 7, None, False)
        NumberHelper._m_nums.add_string("СЕМЕРО", 7, None, False)
        NumberHelper._m_nums.add_string("СІМ", 7, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("СЬОМИЙ", 7 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("SEVEN", 7, None, False)
        NumberHelper._m_nums.add_string("SEVENTH", 7 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("SEPTIES", 7, None, False)
        NumberHelper._m_nums.add_string("ВОСЕМЬ", 8, None, False)
        NumberHelper._m_nums.add_string("ВОСЬМОЙ", 8 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ВОСЬМИ", 8, None, False)
        NumberHelper._m_nums.add_string("ВОСЬМЕРО", 8, None, False)
        NumberHelper._m_nums.add_string("ВІСІМ", 8, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ВОСЬМИЙ", 8 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("EIGHT", 8, None, False)
        NumberHelper._m_nums.add_string("EIGHTH", 8 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("OCTIES", 8, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТЬ", 9, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТЫЙ", 9 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТИ", 9, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТЕРО", 9, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТЬ", 9, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДЕВЯТИЙ", 9 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("NINE", 9, None, False)
        NumberHelper._m_nums.add_string("NINTH", 9 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("NOVIES", 9, None, False)
        NumberHelper._m_nums.add_string("ДЕСЯТЬ", 10, None, False)
        NumberHelper._m_nums.add_string("ДЕСЯТЫЙ", 10 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДЕСЯТИ", 10, None, False)
        NumberHelper._m_nums.add_string("ДЕСЯТИРО", 10, None, False)
        NumberHelper._m_nums.add_string("ДЕСЯТЬ", 10, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДЕСЯТИЙ", 10 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("TEN", 10, None, False)
        NumberHelper._m_nums.add_string("TENTH", 10 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("DECIES", 10, None, False)
        NumberHelper._m_nums.add_string("ОДИННАДЦАТЬ", 11, None, False)
        NumberHelper._m_nums.add_string("ОДИНАДЦАТЬ", 11, None, False)
        NumberHelper._m_nums.add_string("ОДИННАДЦАТЫЙ", 11 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ОДИННАДЦАТИ", 11, None, False)
        NumberHelper._m_nums.add_string("ОДИННАДЦАТИРО", 11, None, False)
        NumberHelper._m_nums.add_string("ОДИНАДЦЯТЬ", 11, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ОДИНАДЦЯТИЙ", 11 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ОДИНАДЦЯТИ", 11, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ELEVEN", 11, None, False)
        NumberHelper._m_nums.add_string("ELEVENTH", 11 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДВЕНАДЦАТЬ", 12, None, False)
        NumberHelper._m_nums.add_string("ДВЕНАДЦАТЫЙ", 12 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДВЕНАДЦАТИ", 12, None, False)
        NumberHelper._m_nums.add_string("ДВАНАДЦЯТЬ", 12, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДВАНАДЦЯТИЙ", 12 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДВАНАДЦЯТИ", 12, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("TWELVE", 12, None, False)
        NumberHelper._m_nums.add_string("TWELFTH", 12 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ТРИНАДЦАТЬ", 13, None, False)
        NumberHelper._m_nums.add_string("ТРИНАДЦАТЫЙ", 13 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ТРИНАДЦАТИ", 13, None, False)
        NumberHelper._m_nums.add_string("ТРИНАДЦЯТЬ", 13, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ТРИНАДЦЯТИЙ", 13 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ТРИНАДЦЯТИ", 13, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("THIRTEEN", 13, None, False)
        NumberHelper._m_nums.add_string("THIRTEENTH", 13 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ЧЕТЫРНАДЦАТЬ", 14, None, False)
        NumberHelper._m_nums.add_string("ЧЕТЫРНАДЦАТЫЙ", 14 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ЧЕТЫРНАДЦАТИ", 14, None, False)
        NumberHelper._m_nums.add_string("ЧОТИРНАДЦЯТЬ", 14, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ЧОТИРНАДЦЯТИЙ", 14 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ЧОТИРНАДЦЯТИ", 14, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("FOURTEEN", 14, None, False)
        NumberHelper._m_nums.add_string("FOURTEENTH", 14 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ПЯТНАДЦАТЬ", 15, None, False)
        NumberHelper._m_nums.add_string("ПЯТНАДЦАТЫЙ", 15 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ПЯТНАДЦАТИ", 15, None, False)
        NumberHelper._m_nums.add_string("ПЯТНАДЦЯТЬ", 15, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ПЯТНАДЦЯТИЙ", 15 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ПЯТНАДЦЯТИ", 15, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("FIFTEEN", 15, None, False)
        NumberHelper._m_nums.add_string("FIFTEENTH", 15 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ШЕСТНАДЦАТЬ", 16, None, False)
        NumberHelper._m_nums.add_string("ШЕСТНАДЦАТЫЙ", 16 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ШЕСТНАДЦАТИ", 16, None, False)
        NumberHelper._m_nums.add_string("ШІСТНАДЦЯТЬ", 16, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ШІСТНАДЦЯТИЙ", 16 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ШІСТНАДЦЯТИ", 16, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("SIXTEEN", 16, None, False)
        NumberHelper._m_nums.add_string("SIXTEENTH", 16 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("СЕМНАДЦАТЬ", 17, None, False)
        NumberHelper._m_nums.add_string("СЕМНАДЦАТЫЙ", 17 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("СЕМНАДЦАТИ", 17, None, False)
        NumberHelper._m_nums.add_string("СІМНАДЦЯТЬ", 17, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("СІМНАДЦЯТИЙ", 17 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("СІМНАДЦЯТИ", 17, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("SEVENTEEN", 17, None, False)
        NumberHelper._m_nums.add_string("SEVENTEENTH", 17 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ВОСЕМНАДЦАТЬ", 18, None, False)
        NumberHelper._m_nums.add_string("ВОСЕМНАДЦАТЫЙ", 18 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ВОСЕМНАДЦАТИ", 18, None, False)
        NumberHelper._m_nums.add_string("ВІСІМНАДЦЯТЬ", 18, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ВІСІМНАДЦЯТИЙ", 18 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ВІСІМНАДЦЯТИ", 18, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("EIGHTEEN", 18, None, False)
        NumberHelper._m_nums.add_string("EIGHTEENTH", 18 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТНАДЦАТЬ", 19, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТНАДЦАТЫЙ", 19 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТНАДЦАТИ", 19, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТНАДЦЯТЬ", 19, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДЕВЯТНАДЦЯТИЙ", 19 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДЕВЯТНАДЦЯТИ", 19, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("NINETEEN", 19, None, False)
        NumberHelper._m_nums.add_string("NINETEENTH", 19 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДВАДЦАТЬ", 20, None, False)
        NumberHelper._m_nums.add_string("ДВАДЦАТЫЙ", 20 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДВАДЦАТИ", 20, None, False)
        NumberHelper._m_nums.add_string("ДВАДЦЯТЬ", 20, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДВАДЦЯТИЙ", 20 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДВАДЦЯТИ", 20, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("TWENTY", 20, None, False)
        NumberHelper._m_nums.add_string("TWENTIETH", 20 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ТРИДЦАТЬ", 30, None, False)
        NumberHelper._m_nums.add_string("ТРИДЦАТЫЙ", 30 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ТРИДЦАТИ", 30, None, False)
        NumberHelper._m_nums.add_string("ТРИДЦЯТЬ", 30, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ТРИДЦЯТИЙ", 30 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ТРИДЦЯТИ", 30, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("THIRTY", 30, None, False)
        NumberHelper._m_nums.add_string("THIRTIETH", 30 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("СОРОК", 40, None, False)
        NumberHelper._m_nums.add_string("СОРОКОВОЙ", 40 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("СОРОКА", 40, None, False)
        NumberHelper._m_nums.add_string("СОРОК", 40, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("СОРОКОВИЙ", 40 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("FORTY", 40, None, False)
        NumberHelper._m_nums.add_string("FORTIETH", 40 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ПЯТЬДЕСЯТ", 50, None, False)
        NumberHelper._m_nums.add_string("ПЯТИДЕСЯТЫЙ", 50 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ПЯТИДЕСЯТИ", 50, None, False)
        NumberHelper._m_nums.add_string("ПЯТДЕСЯТ", 50, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ПЯТДЕСЯТИЙ", 50 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ПЯТДЕСЯТИ", 50, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("FIFTY", 50, None, False)
        NumberHelper._m_nums.add_string("FIFTIETH", 50 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ШЕСТЬДЕСЯТ", 60, None, False)
        NumberHelper._m_nums.add_string("ШЕСТИДЕСЯТЫЙ", 60 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ШЕСТИДЕСЯТИ", 60, None, False)
        NumberHelper._m_nums.add_string("ШІСТДЕСЯТ", 60, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ШЕСИДЕСЯТЫЙ", 60 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ШІСТДЕСЯТИ", 60, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("SIXTY", 60, None, False)
        NumberHelper._m_nums.add_string("SIXTIETH", 60 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("СЕМЬДЕСЯТ", 70, None, False)
        NumberHelper._m_nums.add_string("СЕМИДЕСЯТЫЙ", 70 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("СЕМИДЕСЯТИ", 70, None, False)
        NumberHelper._m_nums.add_string("СІМДЕСЯТ", 70, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("СІМДЕСЯТИЙ", 70 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("СІМДЕСЯТИ", 70, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("SEVENTY", 70, None, False)
        NumberHelper._m_nums.add_string("SEVENTIETH", 70 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("SEVENTIES", 70 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ВОСЕМЬДЕСЯТ", 80, None, False)
        NumberHelper._m_nums.add_string("ВОСЬМИДЕСЯТЫЙ", 80 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ВОСЬМИДЕСЯТИ", 80, None, False)
        NumberHelper._m_nums.add_string("ВІСІМДЕСЯТ", 80, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ВОСЬМИДЕСЯТИЙ", 80 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ВІСІМДЕСЯТИ", 80, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("EIGHTY", 80, None, False)
        NumberHelper._m_nums.add_string("EIGHTIETH", 80 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("EIGHTIES", 80 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯНОСТО", 90, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯНОСТЫЙ", 90 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯНОСТО", 90, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДЕВЯНОСТИЙ", 90 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("NINETY", 90, None, False)
        NumberHelper._m_nums.add_string("NINETIETH", 90 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("NINETIES", 90 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("СТО", 100, None, False)
        NumberHelper._m_nums.add_string("СОТЫЙ", 100 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("СТА", 100, None, False)
        NumberHelper._m_nums.add_string("СТО", 100, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("СОТИЙ", 100 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("HUNDRED", 100, None, False)
        NumberHelper._m_nums.add_string("HUNDREDTH", 100 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДВЕСТИ", 200, None, False)
        NumberHelper._m_nums.add_string("ДВУХСОТЫЙ", 200 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДВУХСОТ", 200, None, False)
        NumberHelper._m_nums.add_string("ДВІСТІ", 200, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДВОХСОТИЙ", 200 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДВОХСОТ", 200, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ТРИСТА", 300, None, False)
        NumberHelper._m_nums.add_string("ТРЕХСОТЫЙ", 300 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ТРЕХСОТ", 300, None, False)
        NumberHelper._m_nums.add_string("ТРИСТА", 300, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ТРЬОХСОТИЙ", 300 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ТРЬОХСОТ", 300, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ЧЕТЫРЕСТА", 400, None, False)
        NumberHelper._m_nums.add_string("ЧЕТЫРЕХСОТЫЙ", 400 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ЧОТИРИСТА", 400, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ЧОТИРЬОХСОТИЙ", 400 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ПЯТЬСОТ", 500, None, False)
        NumberHelper._m_nums.add_string("ПЯТИСОТЫЙ", 500 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ПЯТСОТ", 500, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ПЯТИСОТИЙ", 500 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ШЕСТЬСОТ", 600, None, False)
        NumberHelper._m_nums.add_string("ШЕСТИСОТЫЙ", 600 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ШІСТСОТ", 600, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ШЕСТИСОТИЙ", 600 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("СЕМЬСОТ", 700, None, False)
        NumberHelper._m_nums.add_string("СЕМИСОТЫЙ", 700 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("СІМСОТ", 700, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("СЕМИСОТИЙ", 700 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ВОСЕМЬСОТ", 800, None, False)
        NumberHelper._m_nums.add_string("ВОСЕМЬСОТЫЙ", 800 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ВОСЬМИСОТЫЙ", 800 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ВІСІМСОТ", 800, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ВОСЬМИСОТЫЙ", 800 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДЕВЯТЬСОТ", 900, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТЬСОТЫЙ", 900 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТИСОТЫЙ", 900 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТСОТ", 900, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДЕВЯТЬСОТЫЙ", 900 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДЕВЯТИСОТИЙ", 900 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ТЫС", 1000, None, False)
        NumberHelper._m_nums.add_string("ТЫСЯЧА", 1000, None, False)
        NumberHelper._m_nums.add_string("ТЫСЯЧНЫЙ", 1000 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ТИС", 1000, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ТИСЯЧА", 1000, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ТИСЯЧНИЙ", 1000 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("ДВУХТЫСЯЧНЫЙ", 2000 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.add_string("ДВОХТИСЯЧНИЙ", 2000 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("МИЛЛИОН", 1000000, None, False)
        NumberHelper._m_nums.add_string("МЛН", 1000000, None, False)
        NumberHelper._m_nums.add_string("МІЛЬЙОН", 1000000, MorphLang.UA, False)
        NumberHelper._m_nums.add_string("МИЛЛИАРД", 1000000000, None, False)
        NumberHelper._m_nums.add_string("МІЛЬЯРД", 1000000000, MorphLang.UA, False)
        NumberHelper.__m_after_points = TerminCollection()
        t = Termin._new100("ПОЛОВИНА", 0.5)
        t.add_variant("ОДНА ВТОРАЯ", False)
        t.add_variant("ПОЛ", False)
        NumberHelper.__m_after_points.add(t)
        t = Termin._new100("ТРЕТЬ", 0.33)
        t.add_variant("ОДНА ТРЕТЬ", False)
        NumberHelper.__m_after_points.add(t)
        t = Termin._new100("ЧЕТВЕРТЬ", 0.25)
        t.add_variant("ОДНА ЧЕТВЕРТАЯ", False)
        NumberHelper.__m_after_points.add(t)
        t = Termin._new100("ПЯТАЯ ЧАСТЬ", 0.2)
        t.add_variant("ОДНА ПЯТАЯ", False)
        NumberHelper.__m_after_points.add(t)
    
    _m_nums = None
    
    __m_after_points = None
    
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
        NumberHelper.__m_100words = ["СТО", "ДВЕСТИ", "ТРИСТА", "ЧЕТЫРЕСТА", "ПЯТЬСОТ", "ШЕСТЬСОТ", "СЕМЬСОТ", "ВОСЕМЬСОТ", "ДЕВЯТЬСОТ"]
        NumberHelper.__m_10words = ["ДЕСЯТЬ", "ДВАДЦАТЬ", "ТРИДЦАТЬ", "СОРОК", "ПЯТЬДЕСЯТ", "ШЕСТЬДЕСЯТ", "СЕМЬДЕСЯТ", "ВОСЕМЬДЕСЯТ", "ДЕВЯНОСТО"]
        NumberHelper.__m_1words = ["НОЛЬ", "ОДИН", "ДВА", "ТРИ", "ЧЕТЫРЕ", "ПЯТЬ", "ШЕСТЬ", "СЕМЬ", "ВОСЕМЬ", "ДЕВЯТЬ", "ДЕСЯТЬ", "ОДИННАДЦАТЬ", "ДВЕНАДЦАТЬ", "ТРИНАДЦАТЬ", "ЧЕТЫРНАДЦАТЬ", "ПЯТНАДЦАТЬ", "ШЕСТНАДЦАТЬ", "СЕМНАДЦАТЬ", "ВОСЕМНАДЦАТЬ", "ДЕВЯТНАДЦАТЬ"]
        NumberHelper._m_romans = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX"]

NumberHelper._static_ctor()