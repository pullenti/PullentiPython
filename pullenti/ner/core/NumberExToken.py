# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.Token import Token
from pullenti.ner.TextToken import TextToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.BracketHelper import BracketHelper

class NumberExToken(NumberToken):
    """ Число с стандартный постфиксом (мерой длины, вес, деньги и т.п.) """
    
    def __init__(self, begin : 'Token', end : 'Token', val : int, typ_ : 'NumberSpellingType', ex_typ_ : 'NumberExType'=NumberExType.UNDEFINED) -> None:
        super().__init__(begin, end, val, typ_, None)
        self.real_value = 0
        self.alt_real_value = 0
        self.alt_rest_money = 0
        self.ex_typ = NumberExType.UNDEFINED
        self.ex_typ2 = NumberExType.UNDEFINED
        self.ex_typ_param = None;
        self.mult_after = False
        self.value = val
        self.typ = typ_
        self.ex_typ = ex_typ_
    
    @staticmethod
    def __tryParseFloat(t : 'NumberToken', d : float) -> 'Token':
        d.value = (0)
        if (t is None or t.next0_ is None or t.typ != NumberSpellingType.DIGIT): 
            return None
        kit_ = t.kit
        ns = None
        sps = None
        t1 = t
        first_pass2819 = True
        while True:
            if first_pass2819: first_pass2819 = False
            else: t1 = t1.next0_
            if (not (t1 is not None)): break
            if (t1.next0_ is None): 
                break
            if (((isinstance(t1.next0_, NumberToken)) and (t1.whitespaces_after_count < 3) and (t1.next0_).typ == NumberSpellingType.DIGIT) and t1.next0_.length_char == 3): 
                if (ns is None): 
                    ns = list()
                    ns.append(t)
                    sps = list()
                elif (sps[0] != ' '): 
                    return None
                ns.append(Utils.asObjectOrNull(t1.next0_, NumberToken))
                sps.append(' ')
                continue
            if ((t1.next0_.isCharOf(",.") and (isinstance(t1.next0_.next0_, NumberToken)) and (t1.next0_.next0_).typ == NumberSpellingType.DIGIT) and (t1.whitespaces_after_count < 2) and (t1.next0_.whitespaces_after_count < 2)): 
                if (ns is None): 
                    ns = list()
                    ns.append(t)
                    sps = list()
                elif (t1.next0_.is_whitespace_after and t1.next0_.next0_.length_char != 3 and ((('.' if t1.next0_.isChar('.') else ','))) == sps[len(sps) - 1]): 
                    break
                ns.append(Utils.asObjectOrNull(t1.next0_.next0_, NumberToken))
                sps.append(('.' if t1.next0_.isChar('.') else ','))
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
                    elif (ns[1].end_token.isChar('.') and ns[1].end_token.previous is not None and ns[1].end_token.previous.chars.is_letter): 
                        merge = True
                    if (ns[1].is_whitespace_before): 
                        if ((isinstance(ns[1].end_token, TextToken)) and (ns[1].end_token).term.endswith("000")): 
                            return None
            elif (ns[0].length_char > 3 or ns[0].value == (0)): 
                is_last_drob = True
            else: 
                ok = True
                if (len(ns) == 2 and ns[1].length_char == 3): 
                    ttt = NumberExToken.__m_postfixes.tryParse(ns[1].end_token.next0_, TerminParseAttr.NO)
                    if (ttt is not None and (Utils.valToEnum(ttt.termin.tag, NumberExType)) == NumberExType.MONEY): 
                        is_last_drob = False
                        ok = False
                        not_set_drob = False
                    elif (ns[1].end_token.next0_ is not None and ns[1].end_token.next0_.isChar('(') and (isinstance(ns[1].end_token.next0_.next0_, NumberToken))): 
                        nt1 = (Utils.asObjectOrNull(ns[1].end_token.next0_.next0_, NumberToken))
                        if (nt1.value == ((ns[0].value * (1000)) + ns[1].value)): 
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
        i = 0
        while i < len(ns): 
            if ((i < (len(ns) - 1)) or not is_last_drob): 
                if (i == 0): 
                    d.value = (ns[i].value)
                else: 
                    d.value = ((d.value * (1000)) + (ns[i].value))
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
                    f2 = (ns[i].value)
                    kkk = 0
                    while kkk < ns[i].begin_token.length_char: 
                        f2 /= (10)
                        kkk += 1
                    d.value += f2
                else: 
                    f2 = (ns[i].value)
                    kkk = 0
                    while kkk < ns[i].length_char: 
                        f2 /= (10)
                        kkk += 1
                    d.value += f2
            i += 1
        if ("pt" in kit_.misc_data): 
            kit_.misc_data["pt"] = (m_prev_point_char)
        else: 
            kit_.misc_data["pt"] = m_prev_point_char
        return ns[len(ns) - 1]
    
    @staticmethod
    def tryParseFloatNumber(t : 'Token', can_be_integer : bool=False) -> 'NumberExToken':
        """ Это разделитель дроби по-умолчанию, используется для случаев, когда невозможно принять однозначного решения.
         Устанавливается на основе последнего успешного анализа. """
        is_not = False
        t0 = t
        if (t is not None): 
            if (t.is_hiphen or t.isValue("МИНУС", None)): 
                t = t.next0_
                is_not = True
            elif (t.isChar('+') or t.isValue("ПЛЮС", None)): 
                t = t.next0_
        if ((isinstance(t, TextToken)) and ((t.isValue("НОЛЬ", None) or t.isValue("НУЛЬ", None))) and t.next0_ is not None): 
            if (t.next0_.isValue("ЦЕЛЫЙ", None)): 
                t = t.next0_
            res0 = NumberExToken(t, t.next0_, 0, NumberSpellingType.WORDS, NumberExType.UNDEFINED)
            t = t.next0_
            if (isinstance(t, NumberToken)): 
                val = (t).value
                if (t.next0_ is not None and val > (0)): 
                    if (t.next0_.isValue("ДЕСЯТЫЙ", None)): 
                        res0.end_token = t.next0_
                        res0.real_value = ((val) / (10))
                    elif (t.next0_.isValue("СОТЫЙ", None)): 
                        res0.end_token = t.next0_
                        res0.real_value = ((val) / (100))
                    elif (t.next0_.isValue("ТЫСЯЧНЫЙ", None)): 
                        res0.end_token = t.next0_
                        res0.real_value = ((val) / (1000))
                if (res0.real_value == 0): 
                    res0.end_token = t
                    str0_ = "0.{0}".format(val)
                    dd = 0
                    wrapdd519 = RefOutArgWrapper(0)
                    inoutres520 = Utils.tryParseFloat(str0_, wrapdd519)
                    dd = wrapdd519.value
                    if (inoutres520): 
                        pass
                    else: 
                        wrapdd517 = RefOutArgWrapper(0)
                        inoutres518 = Utils.tryParseFloat(str0_.replace('.', ','), wrapdd517)
                        dd = wrapdd517.value
                        if (inoutres518): 
                            pass
                        else: 
                            return None
                    res0.real_value = dd
            return res0
        if (isinstance(t, TextToken)): 
            tok = NumberExToken.__m_after_points.tryParse(t, TerminParseAttr.NO)
            if (tok is not None): 
                res0 = NumberExToken(t, tok.end_token, 0, NumberSpellingType.WORDS, NumberExType.UNDEFINED)
                res0.real_value = ((tok.termin.tag))
                return res0
        if (not ((isinstance(t, NumberToken)))): 
            return None
        if (t.next0_ is not None and t.next0_.isValue("ЦЕЛЫЙ", None) and (((isinstance(t.next0_.next0_, NumberToken)) or (((isinstance(t.next0_.next0_, TextToken)) and t.next0_.next0_.isValue("НОЛЬ", None)))))): 
            res0 = NumberExToken(t, t.next0_, (t).value, NumberSpellingType.WORDS, NumberExType.UNDEFINED)
            t = t.next0_.next0_
            val = 0
            if (isinstance(t, TextToken)): 
                res0.end_token = t
                t = t.next0_
            if (isinstance(t, NumberToken)): 
                res0.end_token = t
                val = (t).value
                t = t.next0_
            if (t is not None): 
                if (t.isValue("ДЕСЯТЫЙ", None)): 
                    res0.end_token = t
                    res0.real_value = ((((val) / (10))) + (res0.value))
                elif (t.isValue("СОТЫЙ", None)): 
                    res0.end_token = t
                    res0.real_value = ((((val) / (100))) + (res0.value))
                elif (t.isValue("ТЫСЯЧНЫЙ", None)): 
                    res0.end_token = t
                    res0.real_value = ((((val) / (1000))) + (res0.value))
            if (res0.real_value == 0): 
                str0_ = "0.{0}".format(val)
                dd = 0
                wrapdd523 = RefOutArgWrapper(0)
                inoutres524 = Utils.tryParseFloat(str0_, wrapdd523)
                dd = wrapdd523.value
                if (inoutres524): 
                    pass
                else: 
                    wrapdd521 = RefOutArgWrapper(0)
                    inoutres522 = Utils.tryParseFloat(str0_.replace('.', ','), wrapdd521)
                    dd = wrapdd521.value
                    if (inoutres522): 
                        pass
                    else: 
                        return None
                res0.real_value = (dd + (res0.value))
            return res0
        wrapd526 = RefOutArgWrapper(0)
        tt = NumberExToken.__tryParseFloat(Utils.asObjectOrNull(t, NumberToken), wrapd526)
        d = wrapd526.value
        if (tt is None): 
            if ((t.next0_ is None or t.is_whitespace_after or t.next0_.chars.is_letter) or can_be_integer): 
                tt = t
                d = ((t).value)
            else: 
                return None
        if (is_not): 
            d = (- d)
        return NumberExToken._new525(t0, tt, 0, NumberSpellingType.DIGIT, NumberExType.UNDEFINED, d)
    
    @staticmethod
    def tryParseNumberWithPostfix(t : 'Token') -> 'NumberExToken':
        """ Выделение стандартных мер, типа: 10 кв.м. """
        if (t is None): 
            return None
        t0 = t
        is_dollar = None
        if (t.length_char == 1 and t.next0_ is not None): 
            is_dollar = NumberHelper._isMoneyChar(t)
            if ((is_dollar) is not None): 
                t = t.next0_
        nt = Utils.asObjectOrNull(t, NumberToken)
        if (nt is None): 
            if ((not ((isinstance(t.previous, NumberToken))) and t.isChar('(') and (isinstance(t.next0_, NumberToken))) and t.next0_.next0_ is not None and t.next0_.next0_.isChar(')')): 
                toks1 = NumberExToken.__m_postfixes.tryParse(t.next0_.next0_.next0_, TerminParseAttr.NO)
                if (toks1 is not None and (Utils.valToEnum(toks1.termin.tag, NumberExType)) == NumberExType.MONEY): 
                    nt0 = Utils.asObjectOrNull(t.next0_, NumberToken)
                    res = NumberExToken._new527(t, toks1.end_token, nt0.value, nt0.typ, NumberExType.MONEY, nt0.value, nt0.value, toks1.begin_token.morph)
                    return NumberExToken.__correctMoney(res, toks1.begin_token)
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is None or not tt.morph.class0_.is_adjective): 
                return None
            val = tt.term
            i = 4
            first_pass2820 = True
            while True:
                if first_pass2820: first_pass2820 = False
                else: i += 1
                if (not (i < (len(val) - 5))): break
                v = val[0:0+i]
                li = NumberHelper._m_nums.tryAttachStr(v, tt.morph.language)
                if (li is None): 
                    continue
                vv = val[i:]
                lii = NumberExToken.__m_postfixes.tryAttachStr(vv, tt.morph.language)
                if (lii is not None and len(lii) > 0): 
                    re = NumberExToken._new528(t, t, li[0].tag, NumberSpellingType.WORDS, Utils.valToEnum(lii[0].tag, NumberExType), t.morph)
                    re.real_value = (re.value)
                    NumberExToken.__correctExtTypes(re)
                    return re
                break
            return None
        if (t.next0_ is None and is_dollar is None): 
            return None
        f = nt.value
        cel = nt.value
        t1 = nt.next0_
        if (((t1 is not None and t1.isCharOf(",."))) or (((isinstance(t1, NumberToken)) and (t1.whitespaces_before_count < 3)))): 
            wrapd529 = RefOutArgWrapper(0)
            tt11 = NumberExToken.__tryParseFloat(nt, wrapd529)
            d = wrapd529.value
            if (tt11 is not None): 
                t1 = tt11.next0_
                f = d
        if (t1 is None): 
            if (is_dollar is None): 
                return None
        elif ((t1.next0_ is not None and t1.next0_.isValue("С", "З") and t1.next0_.next0_ is not None) and t1.next0_.next0_.isValue("ПОЛОВИНА", None)): 
            f += .5
            t1 = t1.next0_.next0_
        if (t1 is not None and t1.is_hiphen and t1.next0_ is not None): 
            t1 = t1.next0_
        det = False
        altf = f
        if (((isinstance(t1, NumberToken)) and t1.previous is not None and t1.previous.is_hiphen) and (t1).value == (0) and t1.length_char == 2): 
            t1 = t1.next0_
        if ((t1 is not None and t1.next0_ is not None and t1.isChar('(')) and (((isinstance(t1.next0_, NumberToken)) or t1.next0_.isValue("НОЛЬ", None))) and t1.next0_.next0_ is not None): 
            nt1 = Utils.asObjectOrNull(t1.next0_, NumberToken)
            val = 0
            if (nt1 is not None): 
                val = nt1.value
            if ((math.floor(f)) == val): 
                ttt = t1.next0_.next0_
                if (ttt.isChar(')')): 
                    t1 = ttt.next0_
                    det = True
                elif (((((isinstance(ttt, NumberToken)) and ((ttt).value < (100)) and ttt.next0_ is not None) and ttt.next0_.isChar('/') and ttt.next0_.next0_ is not None) and ttt.next0_.next0_.getSourceText() == "100" and ttt.next0_.next0_.next0_ is not None) and ttt.next0_.next0_.next0_.isChar(')')): 
                    rest = NumberExToken.__getDecimalRest100(f)
                    if (rest == (ttt).value): 
                        t1 = ttt.next0_.next0_.next0_.next0_
                        det = True
                elif ((ttt.isValue("ЦЕЛЫХ", None) and (isinstance(ttt.next0_, NumberToken)) and ttt.next0_.next0_ is not None) and ttt.next0_.next0_.next0_ is not None and ttt.next0_.next0_.next0_.isChar(')')): 
                    num2 = Utils.asObjectOrNull(ttt.next0_, NumberToken)
                    altf = (num2.value)
                    if (ttt.next0_.next0_.isValue("ДЕСЯТЫЙ", None)): 
                        altf /= (10)
                    elif (ttt.next0_.next0_.isValue("СОТЫЙ", None)): 
                        altf /= (100)
                    elif (ttt.next0_.next0_.isValue("ТЫСЯЧНЫЙ", None)): 
                        altf /= (1000)
                    elif (ttt.next0_.next0_.isValue("ДЕСЯТИТЫСЯЧНЫЙ", None)): 
                        altf /= (10000)
                    elif (ttt.next0_.next0_.isValue("СТОТЫСЯЧНЫЙ", None)): 
                        altf /= (100000)
                    elif (ttt.next0_.next0_.isValue("МИЛЛИОННЫЙ", None)): 
                        altf /= (1000000)
                    if (altf < 1): 
                        altf += (val)
                        t1 = ttt.next0_.next0_.next0_.next0_
                        det = True
                else: 
                    toks1 = NumberExToken.__m_postfixes.tryParse(ttt, TerminParseAttr.NO)
                    if (toks1 is not None): 
                        if ((Utils.valToEnum(toks1.termin.tag, NumberExType)) == NumberExType.MONEY): 
                            if (toks1.end_token.next0_ is not None and toks1.end_token.next0_.isChar(')')): 
                                res = NumberExToken._new527(t, toks1.end_token.next0_, nt.value, nt.typ, NumberExType.MONEY, f, altf, toks1.begin_token.morph)
                                return NumberExToken.__correctMoney(res, toks1.begin_token)
                    res2 = NumberExToken.tryParseNumberWithPostfix(t1.next0_)
                    if (res2 is not None and res2.end_token.next0_ is not None and res2.end_token.next0_.isChar(')')): 
                        if (res2.value == (math.floor(f))): 
                            res2.begin_token = t
                            res2.end_token = res2.end_token.next0_
                            res2.alt_real_value = res2.real_value
                            res2.real_value = f
                            NumberExToken.__correctExtTypes(res2)
                            if (res2.whitespaces_after_count < 2): 
                                toks2 = NumberExToken.__m_postfixes.tryParse(res2.end_token.next0_, TerminParseAttr.NO)
                                if (toks2 is not None): 
                                    if ((Utils.valToEnum(toks2.termin.tag, NumberExType)) == NumberExType.MONEY): 
                                        res2.end_token = toks2.end_token
                            return res2
            elif (nt1 is not None and nt1.typ == NumberSpellingType.WORDS and nt.typ == NumberSpellingType.DIGIT): 
                altf = (nt1.value)
                ttt = t1.next0_.next0_
                if (ttt.isChar(')')): 
                    t1 = ttt.next0_
                    det = True
                if (not det): 
                    altf = f
        if ((t1 is not None and t1.isChar('(') and t1.next0_ is not None) and t1.next0_.isValue("СУММА", None)): 
            br = BracketHelper.tryParse(t1, BracketParseAttr.NO, 100)
            if (br is not None): 
                t1 = br.end_token.next0_
        if (is_dollar is not None): 
            te = None
            if (t1 is not None): 
                te = t1.previous
            else: 
                t1 = t0
                while t1 is not None: 
                    if (t1.next0_ is None): 
                        te = t1
                    t1 = t1.next0_
            if (te is None): 
                return None
            val = nt.value
            if (te.is_hiphen and te.next0_ is not None): 
                if (te.next0_.isValue("МИЛЛИОННЫЙ", None)): 
                    val *= (1000000)
                    f *= (1000000)
                    altf *= (1000000)
                    te = te.next0_
                elif (te.next0_.isValue("МИЛЛИАРДНЫЙ", None)): 
                    val *= (1000000000)
                    f *= (1000000000)
                    altf *= (1000000000)
                    te = te.next0_
            if (not te.is_whitespace_after and (isinstance(te.next0_, TextToken))): 
                if (te.next0_.isValue("M", None)): 
                    val *= (1000000)
                    f *= (1000000)
                    altf *= (1000000)
                    te = te.next0_
                elif (te.next0_.isValue("BN", None)): 
                    val *= (1000000000)
                    f *= (1000000000)
                    altf *= (1000000000)
                    te = te.next0_
            return NumberExToken._new531(t0, te, val, nt.typ, NumberExType.MONEY, f, altf, is_dollar)
        if (t1 is None or ((t1.is_newline_before and not det))): 
            return None
        toks = NumberExToken.__m_postfixes.tryParse(t1, TerminParseAttr.NO)
        if ((toks is None and det and (isinstance(t1, NumberToken))) and (t1).value == (0)): 
            toks = NumberExToken.__m_postfixes.tryParse(t1.next0_, TerminParseAttr.NO)
        if (toks is not None): 
            t1 = toks.end_token
            if (not t1.isChar('.') and t1.next0_ is not None and t1.next0_.isChar('.')): 
                if ((isinstance(t1, TextToken)) and t1.isValue(toks.termin.terms[0].canonical_text, None)): 
                    pass
                elif (not t1.chars.is_letter): 
                    pass
                else: 
                    t1 = t1.next0_
            if (toks.termin.canonic_text == "LTL"): 
                return None
            if (toks.begin_token == t1): 
                if (t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction): 
                    if (t1.is_whitespace_before and t1.is_whitespace_after): 
                        return None
            ty = Utils.valToEnum(toks.termin.tag, NumberExType)
            res = NumberExToken._new527(t, t1, nt.value, nt.typ, ty, f, altf, toks.begin_token.morph)
            if (ty != NumberExType.MONEY): 
                NumberExToken.__correctExtTypes(res)
                return res
            return NumberExToken.__correctMoney(res, toks.begin_token)
        pfx = NumberExToken.__attachSpecPostfix(t1)
        if (pfx is not None): 
            pfx.begin_token = t
            pfx.value = nt.value
            pfx.typ = nt.typ
            pfx.real_value = f
            pfx.alt_real_value = altf
            return pfx
        if (t1.next0_ is not None and ((t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction))): 
            if (t1.isValue("НА", None)): 
                pass
            else: 
                nn = NumberExToken.tryParseNumberWithPostfix(t1.next0_)
                if (nn is not None): 
                    return NumberExToken._new533(t, t, nt.value, nt.typ, nn.ex_typ, f, altf, nn.ex_typ2, nn.ex_typ_param)
        if (not t1.is_whitespace_after and (isinstance(t1.next0_, NumberToken)) and (isinstance(t1, TextToken))): 
            term = (t1).term
            ty = NumberExType.UNDEFINED
            if (term == "СМХ" or term == "CMX"): 
                ty = NumberExType.SANTIMETER
            elif (term == "MX" or term == "МХ"): 
                ty = NumberExType.METER
            elif (term == "MMX" or term == "ММХ"): 
                ty = NumberExType.MILLIMETER
            if (ty != NumberExType.UNDEFINED): 
                return NumberExToken._new534(t, t1, nt.value, nt.typ, ty, f, altf, True)
        return None
    
    @staticmethod
    def __getDecimalRest100(f : float) -> int:
        rest = math.floor(((math.floor(((((f - math.trunc(f)) + .0001)) * (10000))))) / 100)
        return rest
    
    @staticmethod
    def tryAttachPostfixOnly(t : 'Token') -> 'NumberExToken':
        """ Это попробовать только тип (постфикс) без самого числа
        
        Args:
            t(Token): 
        
        """
        if (t is None): 
            return None
        tok = NumberExToken.__m_postfixes.tryParse(t, TerminParseAttr.NO)
        res = None
        if (tok is not None): 
            res = NumberExToken(t, tok.end_token, 0, NumberSpellingType.DIGIT, Utils.valToEnum(tok.termin.tag, NumberExType))
        else: 
            res = NumberExToken.__attachSpecPostfix(t)
        if (res is not None): 
            NumberExToken.__correctExtTypes(res)
        return res
    
    @staticmethod
    def __attachSpecPostfix(t : 'Token') -> 'NumberExToken':
        if (t is None): 
            return None
        if (t.isCharOf("%")): 
            return NumberExToken(t, t, 0, NumberSpellingType.DIGIT, NumberExType.PERCENT)
        money = NumberHelper._isMoneyChar(t)
        if (money is not None): 
            return NumberExToken._new535(t, t, 0, NumberSpellingType.DIGIT, NumberExType.MONEY, money)
        return None
    
    @staticmethod
    def __correctExtTypes(ex : 'NumberExToken') -> None:
        t = ex.end_token.next0_
        if (t is None): 
            return
        ty = ex.ex_typ
        wrapty537 = RefOutArgWrapper(ty)
        tt = NumberExToken.__corrExTyp2(t, wrapty537)
        ty = wrapty537.value
        if (tt is not None): 
            ex.ex_typ = ty
            ex.end_token = tt
            t = tt.next0_
        if (t is None or t.next0_ is None): 
            return
        if (t.isCharOf("/\\") or t.isValue("НА", None)): 
            pass
        else: 
            return
        tok = NumberExToken.__m_postfixes.tryParse(t.next0_, TerminParseAttr.NO)
        if (tok is not None and (((Utils.valToEnum(tok.termin.tag, NumberExType)) != NumberExType.MONEY))): 
            ex.ex_typ2 = (Utils.valToEnum(tok.termin.tag, NumberExType))
            ex.end_token = tok.end_token
            ty = ex.ex_typ2
            wrapty536 = RefOutArgWrapper(ty)
            tt = NumberExToken.__corrExTyp2(ex.end_token.next0_, wrapty536)
            ty = wrapty536.value
            if (tt is not None): 
                ex.ex_typ2 = ty
                ex.end_token = tt
                t = tt.next0_
    
    @staticmethod
    def __corrExTyp2(t : 'Token', typ_ : 'NumberExType') -> 'Token':
        if (t is None): 
            return None
        num = 0
        tt = t
        if (t.isChar('³')): 
            num = 3
        elif (t.isChar('²')): 
            num = 2
        elif (not t.is_whitespace_before and (isinstance(t, NumberToken)) and (((t).value == (3) or (t).value == (2)))): 
            num = ((t).value)
        elif ((t.isChar('<') and (isinstance(t.next0_, NumberToken)) and t.next0_.next0_ is not None) and t.next0_.next0_.isChar('>')): 
            num = ((t.next0_).value)
            tt = t.next0_.next0_
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
    def __correctMoney(res : 'NumberExToken', t1 : 'Token') -> 'NumberExToken':
        if (t1 is None): 
            return None
        toks = NumberExToken.__m_postfixes.tryParseAll(t1, TerminParseAttr.NO)
        if (toks is None or len(toks) == 0): 
            return None
        tt = toks[0].end_token.next0_
        r = (None if tt is None else tt.getReferent())
        alpha2 = None
        if (r is not None and r.type_name == "GEO"): 
            alpha2 = r.getStringValue("ALPHA2")
        if (alpha2 is not None and len(toks) > 0): 
            for i in range(len(toks) - 1, -1, -1):
                if (not toks[i].termin.canonic_text.startswith(alpha2)): 
                    del toks[i]
            if (len(toks) == 0): 
                toks = NumberExToken.__m_postfixes.tryParseAll(t1, TerminParseAttr.NO)
        if (len(toks) > 1): 
            alpha2 = (None)
            str0_ = toks[0].termin.terms[0].canonical_text
            if (str0_ == "РУБЛЬ" or str0_ == "RUBLE"): 
                alpha2 = "RU"
            elif (str0_ == "ДОЛЛАР" or str0_ == "ДОЛАР" or str0_ == "DOLLAR"): 
                alpha2 = "US"
            elif (str0_ == "ФУНТ" or str0_ == "POUND"): 
                alpha2 = "UK"
            if (alpha2 is not None): 
                for i in range(len(toks) - 1, -1, -1):
                    if (not toks[i].termin.canonic_text.startswith(alpha2)): 
                        del toks[i]
            alpha2 = (None)
        if (len(toks) < 1): 
            return None
        res.ex_typ_param = toks[0].termin.canonic_text
        if (alpha2 is not None and tt is not None): 
            res.end_token = tt
        tt = res.end_token.next0_
        if (tt is not None and tt.is_comma_and): 
            tt = tt.next0_
        if ((isinstance(tt, NumberToken)) and tt.next0_ is not None and (tt.whitespaces_after_count < 4)): 
            tt1 = tt.next0_
            if ((tt1 is not None and tt1.isChar('(') and (isinstance(tt1.next0_, NumberToken))) and tt1.next0_.next0_ is not None and tt1.next0_.next0_.isChar(')')): 
                if ((tt).value == (tt1.next0_).value): 
                    tt1 = tt1.next0_.next0_.next0_
            tok = NumberExToken.__m_small_money.tryParse(tt1, TerminParseAttr.NO)
            if (tok is None and tt1 is not None and tt1.isChar(')')): 
                tok = NumberExToken.__m_small_money.tryParse(tt1.next0_, TerminParseAttr.NO)
            if (tok is not None): 
                max0_ = tok.termin.tag
                val = (tt).value
                if (val < max0_): 
                    f = val
                    f /= (max0_)
                    f0 = res.real_value - (math.floor(res.real_value))
                    re0 = math.floor(((f0 * (100)) + .0001))
                    if (re0 > 0 and val != re0): 
                        res.alt_rest_money = val
                    elif (f0 == 0): 
                        res.real_value += f
                    f0 = (res.alt_real_value - (math.floor(res.alt_real_value)))
                    re0 = (math.floor(((f0 * (100)) + .0001)))
                    if (re0 > 0 and val != re0): 
                        res.alt_rest_money = val
                    elif (f0 == 0): 
                        res.alt_real_value += f
                    res.end_token = tok.end_token
        elif ((isinstance(tt, TextToken)) and tt.isValue("НОЛЬ", None)): 
            tok = NumberExToken.__m_small_money.tryParse(tt.next0_, TerminParseAttr.NO)
            if (tok is not None): 
                res.end_token = tok.end_token
        return res
    
    def normalizeValue(self, ty : 'NumberExType') -> float:
        val = self.real_value
        ety = self.ex_typ
        if (ty.value == ety): 
            return val
        if (self.ex_typ2 != NumberExType.UNDEFINED): 
            return val
        if (ty.value == NumberExType.GRAMM): 
            if (self.ex_typ == NumberExType.KILOGRAM): 
                val *= (1000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.MILLIGRAM): 
                val /= (1000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.TONNA): 
                val *= (1000000)
                ety = ty.value
        elif (ty.value == NumberExType.KILOGRAM): 
            if (self.ex_typ == NumberExType.GRAMM): 
                val /= (1000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.TONNA): 
                val *= (1000)
                ety = ty.value
        elif (ty.value == NumberExType.TONNA): 
            if (self.ex_typ == NumberExType.KILOGRAM): 
                val /= (1000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.GRAMM): 
                val /= (1000000)
                ety = ty.value
        elif (ty.value == NumberExType.MILLIMETER): 
            if (self.ex_typ == NumberExType.SANTIMETER): 
                val *= (10)
                ety = ty.value
            elif (self.ex_typ == NumberExType.METER): 
                val *= (1000)
                ety = ty.value
        elif (ty.value == NumberExType.SANTIMETER): 
            if (self.ex_typ == NumberExType.MILLIMETER): 
                val *= (10)
                ety = ty.value
            elif (self.ex_typ == NumberExType.METER): 
                val *= (100)
                ety = ty.value
        elif (ty.value == NumberExType.METER): 
            if (self.ex_typ == NumberExType.KILOMETER): 
                val *= (1000)
                ety = ty.value
        elif (ty.value == NumberExType.LITR): 
            if (self.ex_typ == NumberExType.MILLILITR): 
                val /= (1000)
                ety = ty.value
        elif (ty.value == NumberExType.MILLILITR): 
            if (self.ex_typ == NumberExType.LITR): 
                val *= (1000)
                ety = ty.value
        elif (ty.value == NumberExType.GEKTAR): 
            if (self.ex_typ == NumberExType.METER2): 
                val /= (10000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.AR): 
                val /= (100)
                ety = ty.value
            elif (self.ex_typ == NumberExType.KILOMETER2): 
                val *= (100)
                ety = ty.value
        elif (ty.value == NumberExType.KILOMETER2): 
            if (self.ex_typ == NumberExType.GEKTAR): 
                val /= (100)
                ety = ty.value
            elif (self.ex_typ == NumberExType.AR): 
                val /= (10000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.METER2): 
                val /= (1000000)
                ety = ty.value
        elif (ty.value == NumberExType.METER2): 
            if (self.ex_typ == NumberExType.AR): 
                val *= (100)
                ety = ty.value
            elif (self.ex_typ == NumberExType.GEKTAR): 
                val *= (10000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.KILOMETER2): 
                val *= (1000000)
                ety = ty.value
        elif (ty.value == NumberExType.DAY): 
            if (self.ex_typ == NumberExType.YEAR): 
                val *= (365)
                ety = ty.value
            elif (self.ex_typ == NumberExType.MONTH): 
                val *= (30)
                ety = ty.value
            elif (self.ex_typ == NumberExType.WEEK): 
                val *= (7)
                ety = ty.value
        ty.value = ety
        return val
    
    @staticmethod
    def convertToString(d : float) -> str:
        lo = math.floor(d)
        res = None
        if (lo == (0)): 
            res = str(d).replace(",", ".")
            if (res.endswith(".0")): 
                res = res[0:0+len(res) - 2]
        else: 
            rest = math.fabs(d - (lo))
            if (rest < .000000001): 
                return str(lo)
            res = str(d).replace(",", ".")
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
                                    return "{0}{1}".format(res[0:0+j], ((((ord(res[j])) - (ord('0'))))) + 1)
                            j -= 1
                        break
            j += 1
        return res
    
    @staticmethod
    def exTypToString(ty : 'NumberExType', ty2 : 'NumberExType'=NumberExType.UNDEFINED) -> str:
        if (ty2 != NumberExType.UNDEFINED): 
            return "{0}/{1}".format(NumberExToken.exTypToString(ty, NumberExType.UNDEFINED), NumberExToken.exTypToString(ty2, NumberExType.UNDEFINED))
        wrapres538 = RefOutArgWrapper(None)
        inoutres539 = Utils.tryGetValue(NumberExToken.__m_normals_typs, ty, wrapres538)
        res = wrapres538.value
        if (inoutres539): 
            return res
        return "?"
    
    def __str__(self) -> str:
        return "{0}{1}".format(self.real_value, Utils.ifNotNull(self.ex_typ_param, NumberExToken.exTypToString(self.ex_typ, self.ex_typ2)))
    
    __m_normals_typs = None
    
    @staticmethod
    def _initialize() -> None:
        if (NumberExToken.__m_postfixes is not None): 
            return
        NumberExToken.__m_after_points = TerminCollection()
        t = Termin._new118("ПОЛОВИНА", .5)
        t.addVariant("ОДНА ВТОРАЯ", False)
        t.addVariant("ПОЛ", False)
        NumberExToken.__m_after_points.add(t)
        t = Termin._new118("ТРЕТЬ", .33)
        t.addVariant("ОДНА ТРЕТЬ", False)
        NumberExToken.__m_after_points.add(t)
        t = Termin._new118("ЧЕТВЕРТЬ", .25)
        t.addVariant("ОДНА ЧЕТВЕРТАЯ", False)
        NumberExToken.__m_after_points.add(t)
        t = Termin._new118("ПЯТАЯ ЧАСТЬ", .2)
        t.addVariant("ОДНА ПЯТАЯ", False)
        NumberExToken.__m_after_points.add(t)
        NumberExToken.__m_postfixes = TerminCollection()
        t = Termin._new544("КВАДРАТНЫЙ МЕТР", MorphLang.RU, True, "кв.м.", NumberExType.METER2)
        t.addAbridge("КВ.МЕТР")
        t.addAbridge("КВ.МЕТРА")
        t.addAbridge("КВ.М.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("КВАДРАТНИЙ МЕТР", MorphLang.UA, True, "КВ.М.", NumberExType.METER2)
        t.addAbridge("КВ.МЕТР")
        t.addAbridge("КВ.МЕТРА")
        t.addAbridge("КВ.М.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("КВАДРАТНЫЙ КИЛОМЕТР", MorphLang.RU, True, "кв.км.", NumberExType.KILOMETER2)
        t.addVariant("КВАДРАТНИЙ КІЛОМЕТР", True)
        t.addAbridge("КВ.КМ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ГЕКТАР", MorphLang.RU, True, "га", NumberExType.GEKTAR)
        t.addAbridge("ГА")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("АР", MorphLang.RU, True, "ар", NumberExType.AR)
        t.addVariant("СОТКА", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("КУБИЧЕСКИЙ МЕТР", MorphLang.RU, True, "куб.м.", NumberExType.METER3)
        t.addVariant("КУБІЧНИЙ МЕТР", True)
        t.addAbridge("КУБ.МЕТР")
        t.addAbridge("КУБ.М.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("МЕТР", MorphLang.RU, True, "м.", NumberExType.METER)
        t.addAbridge("М.")
        t.addAbridge("M.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("МЕТРОВЫЙ", MorphLang.RU, True, "м.", NumberExType.METER)
        t.addVariant("МЕТРОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("МИЛЛИМЕТР", MorphLang.RU, True, "мм.", NumberExType.MILLIMETER)
        t.addAbridge("ММ")
        t.addAbridge("MM")
        t.addVariant("МІЛІМЕТР", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("МИЛЛИМЕТРОВЫЙ", MorphLang.RU, True, "мм.", NumberExType.MILLIMETER)
        t.addVariant("МІЛІМЕТРОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("САНТИМЕТР", MorphLang.RU, True, "см.", NumberExType.SANTIMETER)
        t.addAbridge("СМ")
        t.addAbridge("CM")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("САНТИМЕТРОВЫЙ", MorphLang.RU, True, "см.", NumberExType.SANTIMETER)
        t.addVariant("САНТИМЕТРОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("КВАДРАТНЫЙ САНТИМЕТР", MorphLang.RU, True, "кв.см.", NumberExType.SANTIMETER2)
        t.addVariant("КВАДРАТНИЙ САНТИМЕТР", True)
        t.addAbridge("КВ.СМ.")
        t.addAbridge("СМ.КВ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("КУБИЧЕСКИЙ САНТИМЕТР", MorphLang.RU, True, "куб.см.", NumberExType.SANTIMETER3)
        t.addVariant("КУБІЧНИЙ САНТИМЕТР", True)
        t.addAbridge("КУБ.САНТИМЕТР")
        t.addAbridge("КУБ.СМ.")
        t.addAbridge("СМ.КУБ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("КИЛОМЕТР", MorphLang.RU, True, "км.", NumberExType.KILOMETER)
        t.addAbridge("КМ")
        t.addAbridge("KM")
        t.addVariant("КІЛОМЕТР", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("КИЛОМЕТРОВЫЙ", MorphLang.RU, True, "км.", NumberExType.KILOMETER)
        t.addVariant("КІЛОМЕТРОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("МИЛЯ", MorphLang.RU, True, "миль", NumberExType.KILOMETER)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ГРАММ", MorphLang.RU, True, "гр.", NumberExType.GRAMM)
        t.addAbridge("ГР")
        t.addAbridge("Г")
        t.addVariant("ГРАМ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ГРАММОВЫЙ", MorphLang.RU, True, "гр.", NumberExType.GRAMM)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("КИЛОГРАММ", MorphLang.RU, True, "кг.", NumberExType.KILOGRAM)
        t.addAbridge("КГ")
        t.addVariant("КІЛОГРАМ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("КИЛОГРАММОВЫЙ", MorphLang.RU, True, "кг.", NumberExType.KILOGRAM)
        t.addVariant("КІЛОГРАМОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("МИЛЛИГРАММ", MorphLang.RU, True, "мг.", NumberExType.MILLIGRAM)
        t.addAbridge("МГ")
        t.addVariant("МІЛІГРАМ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("МИЛЛИГРАММОВЫЙ", MorphLang.RU, True, "мг.", NumberExType.MILLIGRAM)
        t.addVariant("МИЛЛИГРАМОВЫЙ", True)
        t.addVariant("МІЛІГРАМОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ТОННА", MorphLang.RU, True, "т.", NumberExType.TONNA)
        t.addAbridge("Т")
        t.addAbridge("T")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ТОННЫЙ", MorphLang.RU, True, "т.", NumberExType.TONNA)
        t.addVariant("ТОННИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ЛИТР", MorphLang.RU, True, "л.", NumberExType.LITR)
        t.addAbridge("Л")
        t.addVariant("ЛІТР", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ЛИТРОВЫЙ", MorphLang.RU, True, "л.", NumberExType.LITR)
        t.addVariant("ЛІТРОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("МИЛЛИЛИТР", MorphLang.RU, True, "мл.", NumberExType.MILLILITR)
        t.addAbridge("МЛ")
        t.addVariant("МІЛІЛІТР", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("МИЛЛИЛИТРОВЫЙ", MorphLang.RU, True, "мл.", NumberExType.MILLILITR)
        t.addVariant("МІЛІЛІТРОВИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ЧАС", MorphLang.RU, True, "ч.", NumberExType.HOUR)
        t.addAbridge("Ч.")
        t.addVariant("ГОДИНА", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("МИНУТА", MorphLang.RU, True, "мин.", NumberExType.MINUTE)
        t.addAbridge("МИН.")
        t.addVariant("ХВИЛИНА", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("СЕКУНДА", MorphLang.RU, True, "сек.", NumberExType.SECOND)
        t.addAbridge("СЕК.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ГОД", MorphLang.RU, True, "г.", NumberExType.YEAR)
        t.addAbridge("Г.")
        t.addAbridge("ЛЕТ")
        t.addVariant("ЛЕТНИЙ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("МЕСЯЦ", MorphLang.RU, True, "мес.", NumberExType.MONTH)
        t.addAbridge("МЕС.")
        t.addVariant("МЕСЯЧНЫЙ", True)
        t.addVariant("КАЛЕНДАРНЫЙ МЕСЯЦ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ДЕНЬ", MorphLang.RU, True, "дн.", NumberExType.DAY)
        t.addAbridge("ДН.")
        t.addVariant("ДНЕВНЫЙ", True)
        t.addVariant("СУТКИ", True)
        t.addVariant("СУТОЧНЫЙ", True)
        t.addVariant("КАЛЕНДАРНЫЙ ДЕНЬ", True)
        t.addVariant("РАБОЧИЙ ДЕНЬ", True)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("НЕДЕЛЯ", MorphLang.RU, True, "нед.", NumberExType.WEEK)
        t.addVariant("НЕДЕЛЬНЫЙ", True)
        t.addVariant("КАЛЕНДАРНАЯ НЕДЕЛЯ", False)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ПРОЦЕНТ", MorphLang.RU, True, "%", NumberExType.PERCENT)
        t.addVariant("%", False)
        t.addVariant("ПРОЦ", True)
        t.addAbridge("ПРОЦ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ШТУКА", MorphLang.RU, True, "шт.", NumberExType.SHUK)
        t.addVariant("ШТ", False)
        t.addAbridge("ШТ.")
        t.addAbridge("ШТ-К")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("УПАКОВКА", MorphLang.RU, True, "уп.", NumberExType.UPAK)
        t.addVariant("УПАК", True)
        t.addVariant("УП", True)
        t.addAbridge("УПАК.")
        t.addAbridge("УП.")
        t.addAbridge("УП-КА")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("РУЛОН", MorphLang.RU, True, "рулон", NumberExType.RULON)
        t.addVariant("РУЛ", True)
        t.addAbridge("РУЛ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("НАБОР", MorphLang.RU, True, "набор", NumberExType.NABOR)
        t.addVariant("НАБ", True)
        t.addAbridge("НАБ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("КОМПЛЕКТ", MorphLang.RU, True, "компл.", NumberExType.KOMPLEKT)
        t.addVariant("КОМПЛ", True)
        t.addAbridge("КОМПЛ.")
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ПАРА", MorphLang.RU, True, "пар", NumberExType.PARA)
        NumberExToken.__m_postfixes.add(t)
        t = Termin._new544("ФЛАКОН", MorphLang.RU, True, "флак.", NumberExType.FLAKON)
        t.addVariant("ФЛ", True)
        t.addAbridge("ФЛ.")
        t.addVariant("ФЛАК", True)
        t.addAbridge("ФЛАК.")
        NumberExToken.__m_postfixes.add(t)
        for te in NumberExToken.__m_postfixes.termins: 
            ty = Utils.valToEnum(te.tag, NumberExType)
            if (not ty in NumberExToken.__m_normals_typs): 
                NumberExToken.__m_normals_typs[ty] = te.canonic_text
        NumberExToken.__m_small_money = TerminCollection()
        t = Termin._new142("УСЛОВНАЯ ЕДИНИЦА", "УЕ", NumberExType.MONEY)
        t.addAbridge("У.Е.")
        t.addAbridge("У.E.")
        t.addAbridge("Y.Е.")
        t.addAbridge("Y.E.")
        NumberExToken.__m_postfixes.add(t)
        for k in range(3):
            str0_ = EpNerCoreInternalResourceHelper.getString(("Money.csv" if k == 0 else ("MoneyUA.csv" if k == 1 else "MoneyEN.csv")))
            if (str0_ is None): 
                continue
            lang = (MorphLang.RU if k == 0 else (MorphLang.UA if k == 1 else MorphLang.EN))
            if (str0_ is None): 
                continue
            for line0 in Utils.splitString(str0_, '\n', False): 
                line = line0.strip()
                if (Utils.isNullOrEmpty(line)): 
                    continue
                parts = Utils.splitString(line.upper(), ';', False)
                if (parts is None or len(parts) != 5): 
                    continue
                if (Utils.isNullOrEmpty(parts[1]) or Utils.isNullOrEmpty(parts[2])): 
                    continue
                t = Termin()
                t.initByNormalText(parts[1], lang)
                t.canonic_text = parts[2]
                t.tag = NumberExType.MONEY
                for p in Utils.splitString(parts[0], ',', False): 
                    if (p != parts[1]): 
                        t0 = Termin()
                        t0.initByNormalText(p, None)
                        t.addVariantTerm(t0)
                if (parts[1] == "РУБЛЬ"): 
                    t.addAbridge("РУБ.")
                elif (parts[1] == "ГРИВНЯ"): 
                    t.addAbridge("ГРН.")
                elif (parts[1] == "ДОЛЛАР"): 
                    t.addAbridge("ДОЛ.")
                    t.addAbridge("ДОЛЛ.")
                elif (parts[1] == "ДОЛАР"): 
                    t.addAbridge("ДОЛ.")
                NumberExToken.__m_postfixes.add(t)
                if (Utils.isNullOrEmpty(parts[3])): 
                    continue
                num = 0
                i = parts[3].find(' ')
                if (i < 2): 
                    continue
                wrapnum589 = RefOutArgWrapper(0)
                inoutres590 = Utils.tryParseInt(parts[3][0:0+i], wrapnum589)
                num = wrapnum589.value
                if (not inoutres590): 
                    continue
                vv = parts[3][i:].strip()
                t = Termin()
                t.initByNormalText(parts[4], lang)
                t.tag = (num)
                if (vv != parts[4]): 
                    t0 = Termin()
                    t0.initByNormalText(vv, None)
                    t.addVariantTerm(t0)
                if (parts[4] == "КОПЕЙКА" or parts[4] == "КОПІЙКА"): 
                    t.addAbridge("КОП.")
                NumberExToken.__m_small_money.add(t)
    
    __m_postfixes = None
    
    __m_small_money = None
    
    __m_after_points = None
    
    @staticmethod
    def _new525(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        return res
    
    @staticmethod
    def _new527(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : 'MorphCollection') -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.morph = _arg8
        return res
    
    @staticmethod
    def _new528(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : 'MorphCollection') -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new531(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : str) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.ex_typ_param = _arg8
        return res
    
    @staticmethod
    def _new533(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : 'NumberExType', _arg9 : str) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.ex_typ2 = _arg8
        res.ex_typ_param = _arg9
        return res
    
    @staticmethod
    def _new534(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : bool) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.mult_after = _arg8
        return res
    
    @staticmethod
    def _new535(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : str) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.ex_typ_param = _arg6
        return res
    
    # static constructor for class NumberExToken
    @staticmethod
    def _static_ctor():
        NumberExToken.__m_normals_typs = dict()

NumberExToken._static_ctor()