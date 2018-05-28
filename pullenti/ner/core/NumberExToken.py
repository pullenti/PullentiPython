# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import math
import io
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.internal.ResourceHelper import ResourceHelper


class NumberExToken(NumberToken):
    """ Число с стандартный постфиксом (мерой длины, вес, деньги и т.п.) """
    
    def __init__(self, begin : 'Token', end : 'Token', val : int, typ_ : 'NumberSpellingType', ex_typ_ : 'NumberExType') -> None:
        self.real_value = 0
        self.alt_real_value = 0
        self.alt_rest_money = 0
        self.ex_typ = NumberExType.UNDEFINED
        self.ex_typ2 = NumberExType.UNDEFINED
        self.ex_typ_param = None
        self.mult_after = False
        super().__init__(begin, end, val, typ_, None)
        self.value = val
        self.typ = typ_
        self.ex_typ = ex_typ_
    
    @staticmethod
    def __try_parse_float(t : 'NumberToken', d : float) -> 'Token':
        from pullenti.ner.TextToken import TextToken
        d.value = 0
        if (t is None or t.next0 is None or t.typ != NumberSpellingType.DIGIT): 
            return None
        ns = None
        sps = None
        t1 = t
        first_pass2603 = True
        while True:
            if first_pass2603: first_pass2603 = False
            else: t1 = t1.next0
            if (not (t1 is not None)): break
            if (t1.next0 is None): 
                break
            if ((isinstance(t1.next0, NumberToken) and (t1.whitespaces_after_count < 3) and (t1.next0 if isinstance(t1.next0, NumberToken) else None).typ == NumberSpellingType.DIGIT) and t1.next0.length_char == 3): 
                if (ns is None): 
                    ns = list()
                    ns.append(t)
                    sps = list()
                elif (sps[0] != ' '): 
                    return None
                ns.append(t1.next0 if isinstance(t1.next0, NumberToken) else None)
                sps.append(' ')
                continue
            if ((t1.next0.is_char_of(",.") and isinstance(t1.next0.next0, NumberToken) and (t1.next0.next0 if isinstance(t1.next0.next0, NumberToken) else None).typ == NumberSpellingType.DIGIT) and (t1.whitespaces_after_count < 2) and (t1.next0.whitespaces_after_count < 2)): 
                if (ns is None): 
                    ns = list()
                    ns.append(t)
                    sps = list()
                elif (t1.next0.is_whitespace_after and t1.next0.next0.length_char != 3 and ((('.' if t1.next0.is_char('.') else ','))) == sps[len(sps) - 1]): 
                    break
                ns.append(t1.next0.next0 if isinstance(t1.next0.next0, NumberToken) else None)
                sps.append(('.' if t1.next0.is_char('.') else ','))
                t1 = t1.next0
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
                        if (isinstance(ns[1].end_token, TextToken) and (ns[1].end_token if isinstance(ns[1].end_token, TextToken) else None).term.endswith("000")): 
                            return None
            elif (ns[0].length_char > 3 or ns[0].value == 0): 
                is_last_drob = True
            else: 
                ok = True
                if (len(ns) == 2 and ns[1].length_char == 3): 
                    ttt = NumberExToken.__m_postfixes.try_parse(ns[1].end_token.next0, TerminParseAttr.NO)
                    if (ttt is not None and Utils.valToEnum(ttt.termin.tag, NumberExType) == NumberExType.MONEY): 
                        is_last_drob = False
                        ok = False
                        not_set_drob = False
                    elif (ns[1].end_token.next0 is not None and ns[1].end_token.next0.is_char('(') and isinstance(ns[1].end_token.next0.next0, NumberToken)): 
                        nt1 = (ns[1].end_token.next0.next0 if isinstance(ns[1].end_token.next0.next0, NumberToken) else None)
                        if (nt1.value == ((ns[0].value * 1000) + ns[1].value)): 
                            is_last_drob = False
                            ok = False
                            not_set_drob = False
                if (ok): 
                    if ("pt" in t.kit.processor.misc_data): 
                        m_prev_point_char = t.kit.processor.misc_data["pt"]
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
        for i in range(len(ns)):
            if ((i < (len(ns) - 1)) or not is_last_drob): 
                if (i == 0): 
                    d.value = ns[i].value
                else: 
                    d.value = ((d.value * 1000) + ns[i].value)
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
                        d.value *= 10
                        kkk += 1
                    f2 = ns[i].value
                    kkk = 0
                    while kkk < ns[i].begin_token.length_char: 
                        f2 /= 10
                        kkk += 1
                    d.value += f2
                else: 
                    f2 = ns[i].value
                    kkk = 0
                    while kkk < ns[i].length_char: 
                        f2 /= 10
                        kkk += 1
                    d.value += f2
        if ("pt" in t.kit.processor.misc_data): 
            t.kit.processor.misc_data["pt"] = m_prev_point_char
        else: 
            t.kit.processor.misc_data["pt"] = m_prev_point_char
        return ns[len(ns) - 1]
    
    @staticmethod
    def try_parse_float_number(t : 'Token') -> 'NumberExToken':
        """ Это разделитель дроби по-умолчанию, используется для случаев, когда невозможно принять однозначного решения.
         Устанавливается на основе последнего успешного анализа. """
        is_not = False
        t0 = t
        if (t is not None and t.is_hiphen): 
            t = t.next0
            is_not = True
        if (not ((isinstance(t, NumberToken)))): 
            return None
        inoutarg490 = RefOutArgWrapper(None)
        tt = NumberExToken.__try_parse_float(t if isinstance(t, NumberToken) else None, inoutarg490)
        d = inoutarg490.value
        if (tt is None): 
            if (t.next0 is None or t.is_whitespace_after or t.next0.chars.is_letter): 
                tt = t
                d = (t if isinstance(t, NumberToken) else None).value
            else: 
                return None
        if (is_not): 
            d = (- d)
        return NumberExToken._new489(t0, tt, 0, NumberSpellingType.DIGIT, NumberExType.UNDEFINED, d)
    
    @staticmethod
    def try_parse_number_with_postfix(t : 'Token') -> 'NumberExToken':
        """ Выделение стандартных мер, типа: 10 кв.м. """
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        if (t is None): 
            return None
        t0 = t
        is_dollar = None
        if (t.length_char == 1 and t.next0 is not None): 
            is_dollar = NumberHelper._is_money_char(t)
            if ((is_dollar) is not None): 
                t = t.next0
        nt = (t if isinstance(t, NumberToken) else None)
        if (nt is None): 
            if ((not ((isinstance(t.previous, NumberToken))) and t.is_char('(') and isinstance(t.next0, NumberToken)) and t.next0.next0 is not None and t.next0.next0.is_char(')')): 
                toks1 = NumberExToken.__m_postfixes.try_parse(t.next0.next0.next0, TerminParseAttr.NO)
                if (toks1 is not None and Utils.valToEnum(toks1.termin.tag, NumberExType) == NumberExType.MONEY): 
                    nt0 = (t.next0 if isinstance(t.next0, NumberToken) else None)
                    res = NumberExToken._new491(t, toks1.end_token, nt0.value, nt0.typ, NumberExType.MONEY, nt0.value, nt0.value, toks1.begin_token.morph)
                    return NumberExToken.__correct_money(res, toks1.begin_token)
            tt = (t if isinstance(t, TextToken) else None)
            if (tt is None or not tt.morph.class0.is_adjective): 
                return None
            val = tt.term
            i = 4
            first_pass2604 = True
            while True:
                if first_pass2604: first_pass2604 = False
                else: i += 1
                if (not (i < (len(val) - 5))): break
                v = val[0 : (i)]
                li = NumberHelper._m_nums.try_attach_str(v, tt.morph.language)
                if (li is None): 
                    continue
                vv = val[i : ]
                lii = NumberExToken.__m_postfixes.try_attach_str(vv, tt.morph.language)
                if (lii is not None and len(lii) > 0): 
                    re = NumberExToken._new492(t, t, li[0].tag, NumberSpellingType.WORDS, Utils.valToEnum(lii[0].tag, NumberExType), t.morph)
                    re.real_value = re.value
                    NumberExToken.__correct_ext_types(re)
                    return re
                break
            return None
        if (t.next0 is None and is_dollar is None): 
            return None
        f = nt.value
        cel = nt.value
        t1 = nt.next0
        if (((t1 is not None and t1.is_char_of(",."))) or ((isinstance(t1, NumberToken) and (t1.whitespaces_before_count < 3)))): 
            inoutarg493 = RefOutArgWrapper(None)
            tt11 = NumberExToken.__try_parse_float(nt, inoutarg493)
            d = inoutarg493.value
            if (tt11 is not None): 
                t1 = tt11.next0
                f = d
        if (t1 is None): 
            if (is_dollar is None): 
                return None
        elif ((t1.next0 is not None and t1.next0.is_value("С", "З") and t1.next0.next0 is not None) and t1.next0.next0.is_value("ПОЛОВИНА", None)): 
            f += 0.5
            t1 = t1.next0.next0
        if (t1 is not None and t1.is_hiphen and t1.next0 is not None): 
            t1 = t1.next0
        det = False
        altf = f
        if ((t1 is not None and t1.next0 is not None and t1.is_char('(')) and ((isinstance(t1.next0, NumberToken) or t1.next0.is_value("НОЛЬ", None))) and t1.next0.next0 is not None): 
            nt1 = (t1.next0 if isinstance(t1.next0, NumberToken) else None)
            val = 0
            if (nt1 is not None): 
                val = nt1.value
            if (math.floor(f) == val): 
                ttt = t1.next0.next0
                if (ttt.is_char(')')): 
                    t1 = ttt.next0
                    det = True
                elif ((((isinstance(ttt, NumberToken) and ((ttt if isinstance(ttt, NumberToken) else None).value < 100) and ttt.next0 is not None) and ttt.next0.is_char('/') and ttt.next0.next0 is not None) and ttt.next0.next0.get_source_text() == "100" and ttt.next0.next0.next0 is not None) and ttt.next0.next0.next0.is_char(')')): 
                    rest = NumberExToken.__get_decimal_rest100(f)
                    if (rest == (ttt if isinstance(ttt, NumberToken) else None).value): 
                        t1 = ttt.next0.next0.next0.next0
                        det = True
                elif ((ttt.is_value("ЦЕЛЫХ", None) and isinstance(ttt.next0, NumberToken) and ttt.next0.next0 is not None) and ttt.next0.next0.next0 is not None and ttt.next0.next0.next0.is_char(')')): 
                    num2 = (ttt.next0 if isinstance(ttt.next0, NumberToken) else None)
                    altf = num2.value
                    if (ttt.next0.next0.is_value("ДЕСЯТЫЙ", None)): 
                        altf /= 10
                    elif (ttt.next0.next0.is_value("СОТЫЙ", None)): 
                        altf /= 100
                    elif (ttt.next0.next0.is_value("ТЫСЯЧНЫЙ", None)): 
                        altf /= 1000
                    elif (ttt.next0.next0.is_value("ДЕСЯТИТЫСЯЧНЫЙ", None)): 
                        altf /= 10000
                    elif (ttt.next0.next0.is_value("СТОТЫСЯЧНЫЙ", None)): 
                        altf /= 100000
                    elif (ttt.next0.next0.is_value("МИЛЛИОННЫЙ", None)): 
                        altf /= 1000000
                    if (altf < 1): 
                        altf += val
                        t1 = ttt.next0.next0.next0.next0
                        det = True
                else: 
                    toks1 = NumberExToken.__m_postfixes.try_parse(ttt, TerminParseAttr.NO)
                    if (toks1 is not None): 
                        if (Utils.valToEnum(toks1.termin.tag, NumberExType) == NumberExType.MONEY): 
                            if (toks1.end_token.next0 is not None and toks1.end_token.next0.is_char(')')): 
                                res = NumberExToken._new491(t, toks1.end_token.next0, nt.value, nt.typ, NumberExType.MONEY, f, altf, toks1.begin_token.morph)
                                return NumberExToken.__correct_money(res, toks1.begin_token)
                    res2 = NumberExToken.try_parse_number_with_postfix(t1.next0)
                    if (res2 is not None and res2.end_token.next0 is not None and res2.end_token.next0.is_char(')')): 
                        if (res2.value == math.floor(f)): 
                            res2.begin_token = t
                            res2.end_token = res2.end_token.next0
                            res2.alt_real_value = res2.real_value
                            res2.real_value = f
                            NumberExToken.__correct_ext_types(res2)
                            if (res2.whitespaces_after_count < 2): 
                                toks2 = NumberExToken.__m_postfixes.try_parse(res2.end_token.next0, TerminParseAttr.NO)
                                if (toks2 is not None): 
                                    if (Utils.valToEnum(toks2.termin.tag, NumberExType) == NumberExType.MONEY): 
                                        res2.end_token = toks2.end_token
                            return res2
            elif (nt1 is not None and nt1.typ == NumberSpellingType.WORDS and nt.typ == NumberSpellingType.DIGIT): 
                altf = nt1.value
                ttt = t1.next0.next0
                if (ttt.is_char(')')): 
                    t1 = ttt.next0
                    det = True
                if (not det): 
                    altf = f
        if ((t1 is not None and t1.is_char('(') and t1.next0 is not None) and t1.next0.is_value("СУММА", None)): 
            br = BracketHelper.try_parse(t1, BracketParseAttr.NO, 100)
            if (br is not None): 
                t1 = br.end_token.next0
        if (is_dollar is not None): 
            te = None
            if (t1 is not None): 
                te = t1.previous
            else: 
                t1 = t0
                while t1 is not None: 
                    if (t1.next0 is None): 
                        te = t1
                    t1 = t1.next0
            if (te is None): 
                return None
            val = nt.value
            if (te.is_hiphen and te.next0 is not None): 
                if (te.next0.is_value("МИЛЛИОННЫЙ", None)): 
                    val *= 1000000
                    f *= 1000000
                    altf *= 1000000
                    te = te.next0
                elif (te.next0.is_value("МИЛЛИАРДНЫЙ", None)): 
                    val *= 1000000000
                    f *= 1000000000
                    altf *= 1000000000
                    te = te.next0
            if (not te.is_whitespace_after and isinstance(te.next0, TextToken)): 
                if (te.next0.is_value("M", None)): 
                    val *= 1000000
                    f *= 1000000
                    altf *= 1000000
                    te = te.next0
                elif (te.next0.is_value("BN", None)): 
                    val *= 1000000000
                    f *= 1000000000
                    altf *= 1000000000
                    te = te.next0
            return NumberExToken._new495(t0, te, val, nt.typ, NumberExType.MONEY, f, altf, is_dollar)
        if (t1 is None or ((t1.is_newline_before and not det))): 
            return None
        toks = NumberExToken.__m_postfixes.try_parse(t1, TerminParseAttr.NO)
        if ((toks is None and det and isinstance(t1, NumberToken)) and (t1 if isinstance(t1, NumberToken) else None).value == 0): 
            toks = NumberExToken.__m_postfixes.try_parse(t1.next0, TerminParseAttr.NO)
        if (toks is not None): 
            t1 = toks.end_token
            if (not t1.is_char('.') and t1.next0 is not None and t1.next0.is_char('.')): 
                if (isinstance(t1, TextToken) and t1.is_value(toks.termin.terms[0].canonical_text, None)): 
                    pass
                else: 
                    t1 = t1.next0
            if (toks.termin.canonic_text == "LTL"): 
                return None
            if (toks.begin_token == t1): 
                if (t1.morph.class0.is_preposition or t1.morph.class0.is_conjunction): 
                    if (t1.is_whitespace_before and t1.is_whitespace_after): 
                        return None
            ty = Utils.valToEnum(toks.termin.tag, NumberExType)
            res = NumberExToken._new491(t, t1, nt.value, nt.typ, ty, f, altf, toks.begin_token.morph)
            if (ty != NumberExType.MONEY): 
                NumberExToken.__correct_ext_types(res)
                return res
            return NumberExToken.__correct_money(res, toks.begin_token)
        if (t1.is_char('%')): 
            return NumberExToken._new497(t, t1, nt.value, nt.typ, NumberExType.PERCENT, f, altf)
        money = NumberHelper._is_money_char(t1)
        if (money is not None): 
            return NumberExToken._new495(t, t1, nt.value, nt.typ, NumberExType.MONEY, f, altf, money)
        if (t1.next0 is not None and ((t1.morph.class0.is_preposition or t1.morph.class0.is_conjunction))): 
            if (t1.is_value("НА", None)): 
                pass
            else: 
                nn = NumberExToken.try_parse_number_with_postfix(t1.next0)
                if (nn is not None): 
                    return NumberExToken._new499(t, t, nt.value, nt.typ, nn.ex_typ, f, altf, nn.ex_typ2, nn.ex_typ_param)
        if (not t1.is_whitespace_after and isinstance(t1.next0, NumberToken) and isinstance(t1, TextToken)): 
            term = (t1 if isinstance(t1, TextToken) else None).term
            ty = NumberExType.UNDEFINED
            if (term == "СМХ" or term == "CMX"): 
                ty = NumberExType.SANTIMETER
            elif (term == "MX" or term == "МХ"): 
                ty = NumberExType.METER
            elif (term == "MMX" or term == "ММХ"): 
                ty = NumberExType.MILLIMETER
            if (ty != NumberExType.UNDEFINED): 
                return NumberExToken._new500(t, t1, nt.value, nt.typ, ty, f, altf, True)
        return None
    
    @staticmethod
    def __get_decimal_rest100(f : float) -> int:
        rest = math.floor(((math.floor(((((f - math.trunc(f)) + 0.0001)) * 10000)))) / 100)
        return rest
    
    @staticmethod
    def try_attach_postfix_only(t : 'Token') -> 'NumberExToken':
        """ Это попробовать только тип (постфикс) без самого числа
        
        Args:
            t(Token): 
        
        """
        tok = NumberExToken.__m_postfixes.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        res = NumberExToken(t, tok.end_token, 0, NumberSpellingType.DIGIT, Utils.valToEnum(tok.termin.tag, NumberExType))
        NumberExToken.__correct_ext_types(res)
        return res
    
    @staticmethod
    def __correct_ext_types(ex : 'NumberExToken') -> None:
        t = ex.end_token.next0
        if (t is None or t.next0 is None): 
            return
        ty = ex.ex_typ
        inoutarg502 = RefOutArgWrapper(ty)
        tt = NumberExToken.__corr_ex_typ2(t, inoutarg502)
        ty = inoutarg502.value
        if (tt is not None): 
            ex.ex_typ = ty
            ex.end_token = tt
            t = tt.next0
        if (t is None or t.next0 is None): 
            return
        if (t.is_char_of("/\\") or t.is_value("НА", None)): 
            pass
        else: 
            return
        tok = NumberExToken.__m_postfixes.try_parse(t.next0, TerminParseAttr.NO)
        if (tok is not None and ((Utils.valToEnum(tok.termin.tag, NumberExType) != NumberExType.MONEY))): 
            ex.ex_typ2 = Utils.valToEnum(tok.termin.tag, NumberExType)
            ex.end_token = tok.end_token
            ty = ex.ex_typ2
            inoutarg501 = RefOutArgWrapper(ty)
            tt = NumberExToken.__corr_ex_typ2(ex.end_token.next0, inoutarg501)
            ty = inoutarg501.value
            if (tt is not None): 
                ex.ex_typ2 = ty
                ex.end_token = tt
                t = tt.next0
    
    @staticmethod
    def __corr_ex_typ2(t : 'Token', typ_ : 'NumberExType') -> 'Token':
        if (t is None): 
            return None
        num = 0
        tt = t
        if (t.is_char('³')): 
            num = 3
        elif (t.is_char('²')): 
            num = 2
        elif (not t.is_whitespace_before and isinstance(t, NumberToken) and (((t if isinstance(t, NumberToken) else None).value == 3 or (t if isinstance(t, NumberToken) else None).value == 2))): 
            num = (t if isinstance(t, NumberToken) else None).value
        elif ((t.is_char('<') and isinstance(t.next0, NumberToken) and t.next0.next0 is not None) and t.next0.next0.is_char('>')): 
            num = (t.next0 if isinstance(t.next0, NumberToken) else None).value
            tt = t.next0.next0
        if (num == 3): 
            if (typ_.value == NumberExType.METER): 
                typ_.value = NumberExType.METER3
                return tt
            if (typ_.value == NumberExType.SANTIMETER): 
                typ_.value = NumberExType.SANTIMETER3
                return tt
        if (num == 2): 
            if (typ_.value == NumberExType.METER): 
                typ_.value = NumberExType.METER2
                return tt
            if (typ_.value == NumberExType.SANTIMETER): 
                typ_.value = NumberExType.SANTIMETER2
                return tt
        return None
    
    @staticmethod
    def __correct_money(res : 'NumberExToken', t1 : 'Token') -> 'NumberExToken':
        from pullenti.ner.TextToken import TextToken
        if (t1 is None): 
            return None
        toks = NumberExToken.__m_postfixes.try_parse_all(t1, TerminParseAttr.NO)
        if (toks is None or len(toks) == 0): 
            return None
        tt = toks[0].end_token.next0
        r = (None if tt is None else tt.get_referent())
        alpha2 = None
        if (r is not None and r.type_name == "GEO"): 
            alpha2 = r.get_string_value("ALPHA2")
        if (alpha2 is not None and len(toks) > 0): 
            for i in range(len(toks) - 1, -1, -1):
                if (not toks[i].termin.canonic_text.startswith(alpha2)): 
                    del toks[i]
            if (len(toks) == 0): 
                toks = NumberExToken.__m_postfixes.try_parse_all(t1, TerminParseAttr.NO)
        if (len(toks) > 1): 
            alpha2 = None
            str0 = toks[0].termin.terms[0].canonical_text
            if (str0 == "РУБЛЬ" or str0 == "RUBLE"): 
                alpha2 = "RU"
            elif (str0 == "ДОЛЛАР" or str0 == "ДОЛАР" or str0 == "DOLLAR"): 
                alpha2 = "US"
            elif (str0 == "ФУНТ" or str0 == "POUND"): 
                alpha2 = "UK"
            if (alpha2 is not None): 
                for i in range(len(toks) - 1, -1, -1):
                    if (not toks[i].termin.canonic_text.startswith(alpha2)): 
                        del toks[i]
            alpha2 = None
        if (len(toks) < 1): 
            return None
        res.ex_typ_param = toks[0].termin.canonic_text
        if (alpha2 is not None and tt is not None): 
            res.end_token = tt
        tt = res.end_token.next0
        if (tt is not None and tt.is_comma_and): 
            tt = tt.next0
        if (isinstance(tt, NumberToken) and tt.next0 is not None and (tt.whitespaces_after_count < 4)): 
            tt1 = tt.next0
            if ((tt1 is not None and tt1.is_char('(') and isinstance(tt1.next0, NumberToken)) and tt1.next0.next0 is not None and tt1.next0.next0.is_char(')')): 
                if ((tt if isinstance(tt, NumberToken) else None).value == (tt1.next0 if isinstance(tt1.next0, NumberToken) else None).value): 
                    tt1 = tt1.next0.next0.next0
            tok = NumberExToken.__m_small_money.try_parse(tt1, TerminParseAttr.NO)
            if (tok is None and tt1 is not None and tt1.is_char(')')): 
                tok = NumberExToken.__m_small_money.try_parse(tt1.next0, TerminParseAttr.NO)
            if (tok is not None): 
                max0 = tok.termin.tag
                val = (tt if isinstance(tt, NumberToken) else None).value
                if (val < max0): 
                    f = val
                    f /= max0
                    f0 = res.real_value - math.floor(res.real_value)
                    re0 = math.floor(((f0 * 100) + 0.0001))
                    if (re0 > 0 and val != re0): 
                        res.alt_rest_money = val
                    elif (f0 == 0): 
                        res.real_value += f
                    f0 = (res.alt_real_value - math.floor(res.alt_real_value))
                    re0 = math.floor(((f0 * 100) + 0.0001))
                    if (re0 > 0 and val != re0): 
                        res.alt_rest_money = val
                    elif (f0 == 0): 
                        res.alt_real_value += f
                    res.end_token = tok.end_token
        elif (isinstance(tt, TextToken) and tt.is_value("НОЛЬ", None)): 
            tok = NumberExToken.__m_small_money.try_parse(tt.next0, TerminParseAttr.NO)
            if (tok is not None): 
                res.end_token = tok.end_token
        return res
    
    def normalize_value(self, ty : 'NumberExType') -> float:
        val = self.real_value
        ety = self.ex_typ
        if (ty.value == ety): 
            return val
        if (self.ex_typ2 != NumberExType.UNDEFINED): 
            return val
        if (ty.value == NumberExType.GRAMM): 
            if (self.ex_typ == NumberExType.KILOGRAM): 
                val *= 1000
                ety = ty.value
            elif (self.ex_typ == NumberExType.MILLIGRAM): 
                val /= 1000
                ety = ty.value
            elif (self.ex_typ == NumberExType.TONNA): 
                val *= 1000000
                ety = ty.value
        elif (ty.value == NumberExType.KILOGRAM): 
            if (self.ex_typ == NumberExType.GRAMM): 
                val /= 1000
                ety = ty.value
            elif (self.ex_typ == NumberExType.TONNA): 
                val *= 1000
                ety = ty.value
        elif (ty.value == NumberExType.TONNA): 
            if (self.ex_typ == NumberExType.KILOGRAM): 
                val /= 1000
                ety = ty.value
            elif (self.ex_typ == NumberExType.GRAMM): 
                val /= 1000000
                ety = ty.value
        elif (ty.value == NumberExType.MILLIMETER): 
            if (self.ex_typ == NumberExType.SANTIMETER): 
                val *= 10
                ety = ty.value
            elif (self.ex_typ == NumberExType.METER): 
                val *= 1000
                ety = ty.value
        elif (ty.value == NumberExType.SANTIMETER): 
            if (self.ex_typ == NumberExType.MILLIMETER): 
                val *= 10
                ety = ty.value
            elif (self.ex_typ == NumberExType.METER): 
                val *= 100
                ety = ty.value
        elif (ty.value == NumberExType.METER): 
            if (self.ex_typ == NumberExType.KILOMETER): 
                val *= 1000
                ety = ty.value
        elif (ty.value == NumberExType.LITR): 
            if (self.ex_typ == NumberExType.MILLILITR): 
                val /= 1000
                ety = ty.value
        elif (ty.value == NumberExType.MILLILITR): 
            if (self.ex_typ == NumberExType.LITR): 
                val *= 1000
                ety = ty.value
        elif (ty.value == NumberExType.GEKTAR): 
            if (self.ex_typ == NumberExType.METER2): 
                val /= 10000
                ety = ty.value
            elif (self.ex_typ == NumberExType.AR): 
                val /= 100
                ety = ty.value
            elif (self.ex_typ == NumberExType.KILOMETER2): 
                val *= 100
                ety = ty.value
        elif (ty.value == NumberExType.KILOMETER2): 
            if (self.ex_typ == NumberExType.GEKTAR): 
                val /= 100
                ety = ty.value
            elif (self.ex_typ == NumberExType.AR): 
                val /= 10000
                ety = ty.value
            elif (self.ex_typ == NumberExType.METER2): 
                val /= 1000000
                ety = ty.value
        elif (ty.value == NumberExType.METER2): 
            if (self.ex_typ == NumberExType.AR): 
                val *= 100
                ety = ty.value
            elif (self.ex_typ == NumberExType.GEKTAR): 
                val *= 10000
                ety = ty.value
            elif (self.ex_typ == NumberExType.KILOMETER2): 
                val *= 1000000
                ety = ty.value
        elif (ty.value == NumberExType.DAY): 
            if (self.ex_typ == NumberExType.YEAR): 
                val *= 365
                ety = ty.value
            elif (self.ex_typ == NumberExType.MONTH): 
                val *= 30
                ety = ty.value
            elif (self.ex_typ == NumberExType.WEEK): 
                val *= 7
                ety = ty.value
        ty.value = ety
        return val
    
    @staticmethod
    def convert_to_string(d : float) -> str:
        lo = math.floor(d)
        if (lo == 0): 
            return str(d).replace(",", ".")
        rest = d - lo
        if (rest < 0.000000001): 
            return str(lo)
        return str(d).replace(",", ".")
    
    @staticmethod
    def ex_typ_to_string(ty : 'NumberExType', ty2 : 'NumberExType'=NumberExType.UNDEFINED) -> str:
        if (ty2 != NumberExType.UNDEFINED): 
            return "{0}/{1}".format(NumberExToken.ex_typ_to_string(ty, NumberExType.UNDEFINED), NumberExToken.ex_typ_to_string(ty2, NumberExType.UNDEFINED))
        swichVal = ty
        if (swichVal == NumberExType.PERCENT): 
            return "%"
        elif (swichVal == NumberExType.GRAMM): 
            return "ГР."
        elif (swichVal == NumberExType.KILOGRAM): 
            return "КГ."
        elif (swichVal == NumberExType.KILOMETER): 
            return "КМ."
        elif (swichVal == NumberExType.METER): 
            return "М."
        elif (swichVal == NumberExType.METER2): 
            return "КВ.М."
        elif (swichVal == NumberExType.AR): 
            return "АР"
        elif (swichVal == NumberExType.GEKTAR): 
            return "ГА"
        elif (swichVal == NumberExType.KILOMETER2): 
            return "КВ.КМ."
        elif (swichVal == NumberExType.METER3): 
            return "КУБ.М."
        elif (swichVal == NumberExType.MILLIGRAM): 
            return "МГ."
        elif (swichVal == NumberExType.MILLIMETER): 
            return "ММ."
        elif (swichVal == NumberExType.SANTIMETER): 
            return "СМ."
        elif (swichVal == NumberExType.SANTIMETER2): 
            return "КВ.СМ."
        elif (swichVal == NumberExType.SANTIMETER3): 
            return "КУБ.СМ."
        elif (swichVal == NumberExType.TONNA): 
            return "Т."
        elif (swichVal == NumberExType.MILLILITR): 
            return "МЛ."
        elif (swichVal == NumberExType.LITR): 
            return "Л."
        elif (swichVal == NumberExType.HOUR): 
            return "Ч."
        elif (swichVal == NumberExType.MINUTE): 
            return "МИН."
        elif (swichVal == NumberExType.SECOND): 
            return "СЕК."
        elif (swichVal == NumberExType.MONEY): 
            return "деньги"
        elif (swichVal == NumberExType.YEAR): 
            return "ЛЕТ"
        elif (swichVal == NumberExType.WEEK): 
            return "НЕД."
        elif (swichVal == NumberExType.MONTH): 
            return "МЕС."
        elif (swichVal == NumberExType.DAY): 
            return "ДН."
        elif (swichVal == NumberExType.SHUK): 
            return "ШТ."
        elif (swichVal == NumberExType.UPAK): 
            return "УП."
        elif (swichVal == NumberExType.RULON): 
            return "РУЛОН"
        elif (swichVal == NumberExType.KOMPLEKT): 
            return "КОМПЛЕКТ"
        elif (swichVal == NumberExType.NABOR): 
            return "НАБОР"
        elif (swichVal == NumberExType.PARA): 
            return "ПАР"
        elif (swichVal == NumberExType.FLAKON): 
            return "ФЛАКОН"
        return ""
    
    def __str__(self) -> str:
        return "{0}{1}".format(self.real_value, Utils.ifNotNull(self.ex_typ_param, NumberExToken.ex_typ_to_string(self.ex_typ, self.ex_typ2)))
    
    @staticmethod
    def _initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (NumberExToken.__m_postfixes is not None): 
            return
        NumberExToken.__m_postfixes = TerminCollection()
        t = Termin._new503("КВАДРАТНЫЙ МЕТР", MorphLang.RU, True, "КВ.М.", NumberExType.METER2)
        t.add_abridge("КВ.МЕТР")
        t.add_abridge("КВ.МЕТРА")
        t.add_abridge("КВ.М.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("КВАДРАТНИЙ МЕТР", MorphLang.UA, True, "КВ.М.", NumberExType.METER2)
        t.add_abridge("КВ.МЕТР")
        t.add_abridge("КВ.МЕТРА")
        t.add_abridge("КВ.М.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("КВАДРАТНЫЙ КИЛОМЕТР", MorphLang.RU, True, "КВ.КМ.", NumberExType.KILOMETER2)
        t.add_variant("КВАДРАТНИЙ КІЛОМЕТР", True)
        t.add_abridge("КВ.КМ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ГЕКТАР", MorphLang.RU, True, "ГА", NumberExType.GEKTAR)
        t.add_abridge("ГА")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("АР", MorphLang.RU, True, "АР", NumberExType.AR)
        t.add_variant("СОТКА", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("КУБИЧЕСКИЙ МЕТР", MorphLang.RU, True, "КУБ.М.", NumberExType.METER3)
        t.add_variant("КУБІЧНИЙ МЕТР", True)
        t.add_abridge("КУБ.МЕТР")
        t.add_abridge("КУБ.М.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("МЕТР", MorphLang.RU, True, "М.", NumberExType.METER)
        t.add_abridge("М.")
        t.add_abridge("M.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("МЕТРОВЫЙ", MorphLang.RU, True, "М.", NumberExType.METER)
        t.add_variant("МЕТРОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("МИЛЛИМЕТР", MorphLang.RU, True, "ММ.", NumberExType.MILLIMETER)
        t.add_abridge("ММ")
        t.add_abridge("MM")
        t.add_variant("МІЛІМЕТР", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("МИЛЛИМЕТРОВЫЙ", MorphLang.RU, True, "ММ.", NumberExType.MILLIMETER)
        t.add_variant("МІЛІМЕТРОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("САНТИМЕТР", MorphLang.RU, True, "СМ.", NumberExType.SANTIMETER)
        t.add_abridge("СМ")
        t.add_abridge("CM")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("САНТИМЕТРОВЫЙ", MorphLang.RU, True, "СМ.", NumberExType.SANTIMETER)
        t.add_variant("САНТИМЕТРОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("КВАДРАТНЫЙ САНТИМЕТР", MorphLang.RU, True, "КВ.СМ.", NumberExType.SANTIMETER2)
        t.add_variant("КВАДРАТНИЙ САНТИМЕТР", True)
        t.add_abridge("КВ.СМ.")
        t.add_abridge("СМ.КВ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("КУБИЧЕСКИЙ САНТИМЕТР", MorphLang.RU, True, "КУБ.СМ.", NumberExType.SANTIMETER3)
        t.add_variant("КУБІЧНИЙ САНТИМЕТР", True)
        t.add_abridge("КУБ.САНТИМЕТР")
        t.add_abridge("КУБ.СМ.")
        t.add_abridge("СМ.КУБ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("КИЛОМЕТР", MorphLang.RU, True, "КМ.", NumberExType.KILOMETER)
        t.add_abridge("КМ")
        t.add_abridge("KM")
        t.add_variant("КІЛОМЕТР", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("КИЛОМЕТРОВЫЙ", MorphLang.RU, True, "КМ.", NumberExType.KILOMETER)
        t.add_variant("КІЛОМЕТРОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ГРАММ", MorphLang.RU, True, "ГР.", NumberExType.GRAMM)
        t.add_abridge("ГР")
        t.add_abridge("Г")
        t.add_variant("ГРАМ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ГРАММОВЫЙ", MorphLang.RU, True, "ГР.", NumberExType.GRAMM)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("КИЛОГРАММ", MorphLang.RU, True, "КГ.", NumberExType.KILOGRAM)
        t.add_abridge("КГ")
        t.add_variant("КІЛОГРАМ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("КИЛОГРАММОВЫЙ", MorphLang.RU, True, "КГ.", NumberExType.KILOGRAM)
        t.add_variant("КІЛОГРАМОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("МИЛЛИГРАММ", MorphLang.RU, True, "МГ.", NumberExType.MILLIGRAM)
        t.add_abridge("МГ")
        t.add_variant("МІЛІГРАМ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("МИЛЛИГРАММОВЫЙ", MorphLang.RU, True, "МГ.", NumberExType.MILLIGRAM)
        t.add_variant("МИЛЛИГРАМОВЫЙ", True)
        t.add_variant("МІЛІГРАМОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ТОННА", MorphLang.RU, True, "Т.", NumberExType.TONNA)
        t.add_abridge("Т")
        t.add_abridge("T")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ТОННЫЙ", MorphLang.RU, True, "Т.", NumberExType.TONNA)
        t.add_variant("ТОННИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ЛИТР", MorphLang.RU, True, "Л.", NumberExType.LITR)
        t.add_abridge("Л")
        t.add_variant("ЛІТР", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ЛИТРОВЫЙ", MorphLang.RU, True, "Л.", NumberExType.LITR)
        t.add_variant("ЛІТРОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("МИЛЛИЛИТР", MorphLang.RU, True, "МЛ.", NumberExType.MILLILITR)
        t.add_abridge("МЛ")
        t.add_variant("МІЛІЛІТР", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("МИЛЛИЛИТРОВЫЙ", MorphLang.RU, True, "МЛ.", NumberExType.MILLILITR)
        t.add_variant("МІЛІЛІТРОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ВОЛЬТ", MorphLang.RU, True, "В", NumberExType.VOLT)
        t.add_variant("VOLT", True)
        t.add_abridge("V")
        t.add_abridge("В")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("КИЛОВОЛЬТ", MorphLang.RU, True, "КВ", NumberExType.KILOVOLT)
        t.add_variant("KILOVOLT", True)
        t.add_abridge("KV")
        t.add_abridge("КВ")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("МЕГАВОЛЬТ", MorphLang.RU, True, "МВ", NumberExType.MEGAVOLT)
        t.add_variant("MEGAVOLT", True)
        t.add_abridge("MV")
        t.add_abridge("МВ")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ВАТТ", MorphLang.RU, True, "ВТ", NumberExType.WATT)
        t.add_variant("WATT", True)
        t.add_abridge("W")
        t.add_abridge("ВТ")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("КИЛОВАТТ", MorphLang.RU, True, "КВТ", NumberExType.KILOWATT)
        t.add_variant("KILOVOLT", True)
        t.add_abridge("KV")
        t.add_abridge("КВ")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("МЕГАВАТТ", MorphLang.RU, True, "МВТ", NumberExType.MEGAWATT)
        t.add_variant("MEGAWATT", True)
        t.add_abridge("MW")
        t.add_abridge("МВТ")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ЧАС", MorphLang.RU, True, "Ч.", NumberExType.HOUR)
        t.add_abridge("Ч.")
        t.add_variant("ГОДИНА", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("МИНУТА", MorphLang.RU, True, "МИН.", NumberExType.MINUTE)
        t.add_abridge("МИН.")
        t.add_variant("ХВИЛИНА", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("СЕКУНДА", MorphLang.RU, True, "СЕК.", NumberExType.SECOND)
        t.add_abridge("СЕК.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ГОД", MorphLang.RU, True, "Г.", NumberExType.YEAR)
        t.add_abridge("Г.")
        t.add_abridge("ЛЕТ")
        t.add_variant("ЛЕТНИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("МЕСЯЦ", MorphLang.RU, True, "МЕС.", NumberExType.MONTH)
        t.add_abridge("МЕС.")
        t.add_variant("МЕСЯЧНЫЙ", True)
        t.add_variant("КАЛЕНДАРНЫЙ МЕСЯЦ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ДЕНЬ", MorphLang.RU, True, "ДН.", NumberExType.DAY)
        t.add_abridge("ДН.")
        t.add_variant("ДНЕВНЫЙ", True)
        t.add_variant("СУТКИ", True)
        t.add_variant("СУТОЧНЫЙ", True)
        t.add_variant("КАЛЕНДАРНЫЙ ДЕНЬ", True)
        t.add_variant("РАБОЧИЙ ДЕНЬ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("НЕДЕЛЯ", MorphLang.RU, True, "НЕД.", NumberExType.WEEK)
        t.add_variant("НЕДЕЛЬНЫЙ", True)
        t.add_variant("КАЛЕНДАРНАЯ НЕДЕЛЯ", False)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ПРОЦЕНТ", MorphLang.RU, True, "%", NumberExType.PERCENT)
        t.add_variant("%", False)
        t.add_variant("ПРОЦ", True)
        t.add_abridge("ПРОЦ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ШТУКА", MorphLang.RU, True, "ШТ.", NumberExType.SHUK)
        t.add_variant("ШТ", False)
        t.add_abridge("ШТ.")
        t.add_abridge("ШТ-К")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("УПАКОВКА", MorphLang.RU, True, "УП.", NumberExType.UPAK)
        t.add_variant("УПАК", True)
        t.add_variant("УП", True)
        t.add_abridge("УПАК.")
        t.add_abridge("УП.")
        t.add_abridge("УП-КА")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("РУЛОН", MorphLang.RU, True, "РУЛОН", NumberExType.RULON)
        t.add_variant("РУЛ", True)
        t.add_abridge("РУЛ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("НАБОР", MorphLang.RU, True, "НАБОР", NumberExType.NABOR)
        t.add_variant("НАБ", True)
        t.add_abridge("НАБ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("КОМПЛЕКТ", MorphLang.RU, True, "КОМПЛЕКТ", NumberExType.KOMPLEKT)
        t.add_variant("КОМПЛ", True)
        t.add_abridge("КОМПЛ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ПАРА", MorphLang.RU, True, "ПАР", NumberExType.PARA)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new503("ФЛАКОН", MorphLang.RU, True, "ФЛАКОН", NumberExType.FLAKON)
        t.add_variant("ФЛ", True)
        t.add_abridge("ФЛ.")
        t.add_variant("ФЛАК", True)
        t.add_abridge("ФЛАК.")
        NumberExToken.__m_postfixes.add(t)
        NumberExToken.__m_small_money = TerminCollection()
        t = Termin._new142("УСЛОВНАЯ ЕДИНИЦА", "УЕ", NumberExType.MONEY)
        t.add_abridge("У.Е.")
        t.add_abridge("У.E.")
        t.add_abridge("Y.Е.")
        t.add_abridge("Y.E.")
        NumberExToken.__m_postfixes.add(t)
        for k in range(3):
            str0 = ResourceHelper.get_string(("Money.csv" if k == 0 else ("MoneyUA.csv" if k == 1 else "MoneyEN.csv")))
            if (str0 is None): 
                continue
            lang = (MorphLang.RU if k == 0 else (MorphLang.UA if k == 1 else MorphLang.EN))
            if (str0 is None): 
                continue
            try: 
                with io.StringIO(str0) as tr: 
                    while True:
                        line = Utils.readLineIO(tr)
                        if (line is None): 
                            break
                        if (Utils.isNullOrEmpty(line)): 
                            continue
                        parts = Utils.splitString(line.upper(), ';', False)
                        if (parts is None or len(parts) != 5): 
                            continue
                        if (Utils.isNullOrEmpty(parts[1]) or Utils.isNullOrEmpty(parts[2])): 
                            continue
                        t = Termin()
                        t.init_by_normal_text(parts[1], lang)
                        t.canonic_text = parts[2]
                        t.tag = NumberExType.MONEY
                        for p in Utils.splitString(parts[0], ',', False): 
                            if (p != parts[1]): 
                                t0 = Termin()
                                t0.init_by_normal_text(p, MorphLang())
                                t.add_variant_term(t0)
                        if (parts[1] == "РУБЛЬ"): 
                            t.add_abridge("РУБ.")
                        elif (parts[1] == "ГРИВНЯ"): 
                            t.add_abridge("ГРН.")
                        elif (parts[1] == "ДОЛЛАР"): 
                            t.add_abridge("ДОЛ.")
                            t.add_abridge("ДОЛЛ.")
                        elif (parts[1] == "ДОЛАР"): 
                            t.add_abridge("ДОЛ.")
                        NumberExToken.__m_postfixes.add(t)
                        if (Utils.isNullOrEmpty(parts[3])): 
                            continue
                        num = 0
                        i = parts[3].find(' ')
                        if (i < 2): 
                            continue
                        inoutarg553 = RefOutArgWrapper(None)
                        inoutres554 = Utils.tryParseInt(parts[3][0 : (i)], inoutarg553)
                        num = inoutarg553.value
                        if (not inoutres554): 
                            continue
                        vv = parts[3][i : ].strip()
                        t = Termin()
                        t.init_by_normal_text(parts[4], lang)
                        t.tag = num
                        if (vv != parts[4]): 
                            t0 = Termin()
                            t0.init_by_normal_text(vv, MorphLang())
                            t.add_variant_term(t0)
                        if (parts[4] == "КОПЕЙКА" or parts[4] == "КОПІЙКА"): 
                            t.add_abridge("КОП.")
                        NumberExToken.__m_small_money.add(t)
            except Exception as ex: 
                pass
    
    __m_postfixes = None
    
    __m_small_money = None

    
    @staticmethod
    def _new489(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        return res
    
    @staticmethod
    def _new491(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : 'MorphCollection') -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.morph = _arg8
        return res
    
    @staticmethod
    def _new492(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : 'MorphCollection') -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new495(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : str) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.ex_typ_param = _arg8
        return res
    
    @staticmethod
    def _new497(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        return res
    
    @staticmethod
    def _new499(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : 'NumberExType', _arg9 : str) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.ex_typ2 = _arg8
        res.ex_typ_param = _arg9
        return res
    
    @staticmethod
    def _new500(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : bool) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.mult_after = _arg8
        return res