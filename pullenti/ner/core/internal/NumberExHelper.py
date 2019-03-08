﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.ner.Token import Token
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NumberExToken import NumberExToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.BracketHelper import BracketHelper

class NumberExHelper:
    
    @staticmethod
    def try_parse_number_with_postfix(t : 'Token') -> 'NumberExToken':
        """ Выделение стандартных мер, типа: 10 кв.м. """
        if (t is None): 
            return None
        t0 = t
        is_dollar = None
        if (t.length_char == 1 and t.next0_ is not None): 
            is_dollar = NumberHelper._is_money_char(t)
            if ((is_dollar) is not None): 
                t = t.next0_
        nt = Utils.asObjectOrNull(t, NumberToken)
        if (nt is None): 
            if ((not ((isinstance(t.previous, NumberToken))) and t.is_char('(') and (isinstance(t.next0_, NumberToken))) and t.next0_.next0_ is not None and t.next0_.next0_.is_char(')')): 
                toks1 = NumberExHelper._m_postfixes.try_parse(t.next0_.next0_.next0_, TerminParseAttr.NO)
                if (toks1 is not None and (Utils.valToEnum(toks1.termin.tag, NumberExType)) == NumberExType.MONEY): 
                    nt0 = Utils.asObjectOrNull(t.next0_, NumberToken)
                    res = NumberExToken._new473(t, toks1.end_token, nt0.value, nt0.typ, NumberExType.MONEY, nt0.real_value, toks1.begin_token.morph)
                    return NumberExHelper.__correct_money(res, toks1.begin_token)
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is None or not tt.morph.class0_.is_adjective0): 
                return None
            val = tt.term
            i = 4
            first_pass2891 = True
            while True:
                if first_pass2891: first_pass2891 = False
                else: i += 1
                if (not (i < (len(val) - 5))): break
                v = val[0:0+i]
                li = NumberHelper._m_nums.try_attach_str(v, tt.morph.language)
                if (li is None): 
                    continue
                vv = val[i:]
                lii = NumberExHelper._m_postfixes.try_attach_str(vv, tt.morph.language)
                if (lii is not None and len(lii) > 0): 
                    re = NumberExToken._new474(t, t, str((li[0].tag)), NumberSpellingType.WORDS, Utils.valToEnum(lii[0].tag, NumberExType), t.morph)
                    NumberExHelper.__correct_ext_types(re)
                    return re
                break
            return None
        if (t.next0_ is None and is_dollar is None): 
            return None
        f = nt.real_value
        t1 = nt.next0_
        if (((t1 is not None and t1.is_char_of(",."))) or (((isinstance(t1, NumberToken)) and (t1.whitespaces_before_count < 3)))): 
            tt11 = NumberHelper.try_parse_real_number(nt, False)
            if (tt11 is not None): 
                t1 = tt11.end_token.next0_
                f = tt11.real_value
        if (t1 is None): 
            if (is_dollar is None): 
                return None
        elif ((t1.next0_ is not None and t1.next0_.is_value("С", "З") and t1.next0_.next0_ is not None) and t1.next0_.next0_.is_value("ПОЛОВИНА", None)): 
            f += 0.5
            t1 = t1.next0_.next0_
        if (t1 is not None and t1.is_hiphen0 and t1.next0_ is not None): 
            t1 = t1.next0_
        det = False
        altf = f
        if (((isinstance(t1, NumberToken)) and t1.previous is not None and t1.previous.is_hiphen0) and (t1).int_value == 0 and t1.length_char == 2): 
            t1 = t1.next0_
        if ((t1 is not None and t1.next0_ is not None and t1.is_char('(')) and (((isinstance(t1.next0_, NumberToken)) or t1.next0_.is_value("НОЛЬ", None))) and t1.next0_.next0_ is not None): 
            nt1 = Utils.asObjectOrNull(t1.next0_, NumberToken)
            val = 0
            if (nt1 is not None): 
                val = nt1.real_value
            if (math.floor(f) == math.floor(val)): 
                ttt = t1.next0_.next0_
                if (ttt.is_char(')')): 
                    t1 = ttt.next0_
                    det = True
                    if ((isinstance(t1, NumberToken)) and (t1).int_value is not None and (t1).int_value == 0): 
                        t1 = t1.next0_
                elif (((((isinstance(ttt, NumberToken)) and ((ttt).real_value < 100) and ttt.next0_ is not None) and ttt.next0_.is_char('/') and ttt.next0_.next0_ is not None) and ttt.next0_.next0_.get_source_text() == "100" and ttt.next0_.next0_.next0_ is not None) and ttt.next0_.next0_.next0_.is_char(')')): 
                    rest = NumberExHelper.__get_decimal_rest100(f)
                    if ((ttt).int_value is not None and rest == (ttt).int_value): 
                        t1 = ttt.next0_.next0_.next0_.next0_
                        det = True
                elif ((ttt.is_value("ЦЕЛЫХ", None) and (isinstance(ttt.next0_, NumberToken)) and ttt.next0_.next0_ is not None) and ttt.next0_.next0_.next0_ is not None and ttt.next0_.next0_.next0_.is_char(')')): 
                    num2 = Utils.asObjectOrNull(ttt.next0_, NumberToken)
                    altf = num2.real_value
                    if (ttt.next0_.next0_.is_value("ДЕСЯТЫЙ", None)): 
                        altf /= (10)
                    elif (ttt.next0_.next0_.is_value("СОТЫЙ", None)): 
                        altf /= (100)
                    elif (ttt.next0_.next0_.is_value("ТЫСЯЧНЫЙ", None)): 
                        altf /= (1000)
                    elif (ttt.next0_.next0_.is_value("ДЕСЯТИТЫСЯЧНЫЙ", None)): 
                        altf /= (10000)
                    elif (ttt.next0_.next0_.is_value("СТОТЫСЯЧНЫЙ", None)): 
                        altf /= (100000)
                    elif (ttt.next0_.next0_.is_value("МИЛЛИОННЫЙ", None)): 
                        altf /= (1000000)
                    if (altf < 1): 
                        altf += val
                        t1 = ttt.next0_.next0_.next0_.next0_
                        det = True
                else: 
                    toks1 = NumberExHelper._m_postfixes.try_parse(ttt, TerminParseAttr.NO)
                    if (toks1 is not None): 
                        if ((Utils.valToEnum(toks1.termin.tag, NumberExType)) == NumberExType.MONEY): 
                            if (toks1.end_token.next0_ is not None and toks1.end_token.next0_.is_char(')')): 
                                res = NumberExToken._new475(t, toks1.end_token.next0_, nt.value, nt.typ, NumberExType.MONEY, f, altf, toks1.begin_token.morph)
                                return NumberExHelper.__correct_money(res, toks1.begin_token)
                    res2 = NumberExHelper.try_parse_number_with_postfix(t1.next0_)
                    if (res2 is not None and res2.end_token.next0_ is not None and res2.end_token.next0_.is_char(')')): 
                        res2.begin_token = t
                        res2.end_token = res2.end_token.next0_
                        res2.alt_real_value = res2.real_value
                        res2.real_value = f
                        NumberExHelper.__correct_ext_types(res2)
                        if (res2.whitespaces_after_count < 2): 
                            toks2 = NumberExHelper._m_postfixes.try_parse(res2.end_token.next0_, TerminParseAttr.NO)
                            if (toks2 is not None): 
                                if ((Utils.valToEnum(toks2.termin.tag, NumberExType)) == NumberExType.MONEY): 
                                    res2.end_token = toks2.end_token
                        return res2
            elif (nt1 is not None and nt1.typ == NumberSpellingType.WORDS and nt.typ == NumberSpellingType.DIGIT): 
                altf = nt1.real_value
                ttt = t1.next0_.next0_
                if (ttt.is_char(')')): 
                    t1 = ttt.next0_
                    det = True
                if (not det): 
                    altf = f
        if ((t1 is not None and t1.is_char('(') and t1.next0_ is not None) and t1.next0_.is_value("СУММА", None)): 
            br = BracketHelper.try_parse(t1, BracketParseAttr.NO, 100)
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
            if (te.is_hiphen0 and te.next0_ is not None): 
                if (te.next0_.is_value("МИЛЛИОННЫЙ", None)): 
                    f *= (1000000)
                    altf *= (1000000)
                    te = te.next0_
                elif (te.next0_.is_value("МИЛЛИАРДНЫЙ", None)): 
                    f *= (1000000000)
                    altf *= (1000000000)
                    te = te.next0_
            if (not te.is_whitespace_after0 and (isinstance(te.next0_, TextToken))): 
                if (te.next0_.is_value("M", None)): 
                    f *= (1000000)
                    altf *= (1000000)
                    te = te.next0_
                elif (te.next0_.is_value("BN", None)): 
                    f *= (1000000000)
                    altf *= (1000000000)
                    te = te.next0_
            return NumberExToken._new476(t0, te, "", nt.typ, NumberExType.MONEY, f, altf, is_dollar)
        if (t1 is None or ((t1.is_newline_before0 and not det))): 
            return None
        toks = NumberExHelper._m_postfixes.try_parse(t1, TerminParseAttr.NO)
        if ((toks is None and det and (isinstance(t1, NumberToken))) and (t1).value == "0"): 
            toks = NumberExHelper._m_postfixes.try_parse(t1.next0_, TerminParseAttr.NO)
        if (toks is not None): 
            t1 = toks.end_token
            if (not t1.is_char('.') and t1.next0_ is not None and t1.next0_.is_char('.')): 
                if ((isinstance(t1, TextToken)) and t1.is_value(toks.termin.terms[0].canonical_text, None)): 
                    pass
                elif (not t1.chars.is_letter0): 
                    pass
                else: 
                    t1 = t1.next0_
            if (toks.termin.canonic_text == "LTL"): 
                return None
            if (toks.begin_token == t1): 
                if (t1.morph.class0_.is_preposition0 or t1.morph.class0_.is_conjunction0): 
                    if (t1.is_whitespace_before0 and t1.is_whitespace_after0): 
                        return None
            ty = Utils.valToEnum(toks.termin.tag, NumberExType)
            res = NumberExToken._new475(t, t1, nt.value, nt.typ, ty, f, altf, toks.begin_token.morph)
            if (ty != NumberExType.MONEY): 
                NumberExHelper.__correct_ext_types(res)
                return res
            return NumberExHelper.__correct_money(res, toks.begin_token)
        pfx = NumberExHelper.__attach_spec_postfix(t1)
        if (pfx is not None): 
            pfx.begin_token = t
            pfx.value = nt.value
            pfx.typ = nt.typ
            pfx.real_value = f
            pfx.alt_real_value = altf
            return pfx
        if (t1.next0_ is not None and ((t1.morph.class0_.is_preposition0 or t1.morph.class0_.is_conjunction0))): 
            if (t1.is_value("НА", None)): 
                pass
            else: 
                nn = NumberExHelper.try_parse_number_with_postfix(t1.next0_)
                if (nn is not None): 
                    return NumberExToken._new478(t, t, nt.value, nt.typ, nn.ex_typ, f, altf, nn.ex_typ2, nn.ex_typ_param)
        if (not t1.is_whitespace_after0 and (isinstance(t1.next0_, NumberToken)) and (isinstance(t1, TextToken))): 
            term = (t1).term
            ty = NumberExType.UNDEFINED
            if (term == "СМХ" or term == "CMX"): 
                ty = NumberExType.SANTIMETER
            elif (term == "MX" or term == "МХ"): 
                ty = NumberExType.METER
            elif (term == "MMX" or term == "ММХ"): 
                ty = NumberExType.MILLIMETER
            if (ty != NumberExType.UNDEFINED): 
                return NumberExToken._new479(t, t1, nt.value, nt.typ, ty, f, altf, True)
        return None
    
    @staticmethod
    def __get_decimal_rest100(f : float) -> int:
        rest = math.floor(((math.floor(((((f - math.trunc(f)) + 0.0001)) * (10000))))) / 100)
        return rest
    
    @staticmethod
    def try_attach_postfix_only(t : 'Token') -> 'NumberExToken':
        """ Это попробовать только тип (постфикс) без самого числа
        
        Args:
            t(Token): 
        
        """
        if (t is None): 
            return None
        tok = NumberExHelper._m_postfixes.try_parse(t, TerminParseAttr.NO)
        res = None
        if (tok is not None): 
            res = NumberExToken(t, tok.end_token, "", NumberSpellingType.DIGIT, Utils.valToEnum(tok.termin.tag, NumberExType))
        else: 
            res = NumberExHelper.__attach_spec_postfix(t)
        if (res is not None): 
            NumberExHelper.__correct_ext_types(res)
        return res
    
    @staticmethod
    def __attach_spec_postfix(t : 'Token') -> 'NumberExToken':
        if (t is None): 
            return None
        if (t.is_char_of("%")): 
            return NumberExToken(t, t, "", NumberSpellingType.DIGIT, NumberExType.PERCENT)
        money = NumberHelper._is_money_char(t)
        if (money is not None): 
            return NumberExToken._new480(t, t, "", NumberSpellingType.DIGIT, NumberExType.MONEY, money)
        return None
    
    @staticmethod
    def __correct_ext_types(ex : 'NumberExToken') -> None:
        t = ex.end_token.next0_
        if (t is None): 
            return
        ty = ex.ex_typ
        wrapty482 = RefOutArgWrapper(ty)
        tt = NumberExHelper.__corr_ex_typ2(t, wrapty482)
        ty = wrapty482.value
        if (tt is not None): 
            ex.ex_typ = ty
            ex.end_token = tt
            t = tt.next0_
        if (t is None or t.next0_ is None): 
            return
        if (t.is_char_of("/\\") or t.is_value("НА", None)): 
            pass
        else: 
            return
        tok = NumberExHelper._m_postfixes.try_parse(t.next0_, TerminParseAttr.NO)
        if (tok is not None and (((Utils.valToEnum(tok.termin.tag, NumberExType)) != NumberExType.MONEY))): 
            ex.ex_typ2 = (Utils.valToEnum(tok.termin.tag, NumberExType))
            ex.end_token = tok.end_token
            ty = ex.ex_typ2
            wrapty481 = RefOutArgWrapper(ty)
            tt = NumberExHelper.__corr_ex_typ2(ex.end_token.next0_, wrapty481)
            ty = wrapty481.value
            if (tt is not None): 
                ex.ex_typ2 = ty
                ex.end_token = tt
                t = tt.next0_
    
    @staticmethod
    def __corr_ex_typ2(t : 'Token', typ : 'NumberExType') -> 'Token':
        if (t is None): 
            return None
        num = 0
        tt = t
        if (t.is_char('³')): 
            num = 3
        elif (t.is_char('²')): 
            num = 2
        elif (not t.is_whitespace_before0 and (isinstance(t, NumberToken)) and (((t).value == "3" or (t).value == "2"))): 
            num = (t).int_value
        elif ((t.is_char('<') and (isinstance(t.next0_, NumberToken)) and t.next0_.next0_ is not None) and t.next0_.next0_.is_char('>') and (t.next0_).int_value is not None): 
            num = (t.next0_).int_value
            tt = t.next0_.next0_
        if (num == 3): 
            if (typ.value == NumberExType.METER): 
                typ.value = NumberExType.METER3
                return tt
            if (typ.value == NumberExType.SANTIMETER): 
                typ.value = NumberExType.SANTIMETER3
                return tt
        if (num == 2): 
            if (typ.value == NumberExType.METER): 
                typ.value = NumberExType.METER2
                return tt
            if (typ.value == NumberExType.SANTIMETER): 
                typ.value = NumberExType.SANTIMETER2
                return tt
        return None
    
    @staticmethod
    def __correct_money(res : 'NumberExToken', t1 : 'Token') -> 'NumberExToken':
        if (t1 is None): 
            return None
        toks = NumberExHelper._m_postfixes.try_parse_all(t1, TerminParseAttr.NO)
        if (toks is None or len(toks) == 0): 
            return None
        tt = toks[0].end_token.next0_
        r = (None if tt is None else tt.get_referent())
        alpha2 = None
        if (r is not None and r.type_name == "GEO"): 
            alpha2 = r.get_string_value("ALPHA2")
        if (alpha2 is not None and len(toks) > 0): 
            for i in range(len(toks) - 1, -1, -1):
                if (not toks[i].termin.canonic_text.startswith(alpha2)): 
                    del toks[i]
            if (len(toks) == 0): 
                toks = NumberExHelper._m_postfixes.try_parse_all(t1, TerminParseAttr.NO)
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
        if (tt is not None and tt.is_comma_and0): 
            tt = tt.next0_
        if ((isinstance(tt, NumberToken)) and tt.next0_ is not None and (tt.whitespaces_after_count < 4)): 
            tt1 = tt.next0_
            if ((tt1 is not None and tt1.is_char('(') and (isinstance(tt1.next0_, NumberToken))) and tt1.next0_.next0_ is not None and tt1.next0_.next0_.is_char(')')): 
                if ((tt).value == (tt1.next0_).value): 
                    tt1 = tt1.next0_.next0_.next0_
            tok = NumberExHelper.__m_small_money.try_parse(tt1, TerminParseAttr.NO)
            if (tok is None and tt1 is not None and tt1.is_char(')')): 
                tok = NumberExHelper.__m_small_money.try_parse(tt1.next0_, TerminParseAttr.NO)
            if (tok is not None and (tt).int_value is not None): 
                max0_ = tok.termin.tag
                val = (tt).int_value
                if (val < max0_): 
                    f = val
                    f /= (max0_)
                    f0 = res.real_value - (math.floor(res.real_value))
                    re0 = math.floor(((f0 * (100)) + 0.0001))
                    if (re0 > 0 and val != re0): 
                        res.alt_rest_money = val
                    elif (f0 == 0): 
                        res.real_value = res.real_value + f
                    f0 = (res.alt_real_value - (math.floor(res.alt_real_value)))
                    re0 = (math.floor(((f0 * (100)) + 0.0001)))
                    if (re0 > 0 and val != re0): 
                        res.alt_rest_money = val
                    elif (f0 == 0): 
                        res.alt_real_value += f
                    res.end_token = tok.end_token
        elif ((isinstance(tt, TextToken)) and tt.is_value("НОЛЬ", None)): 
            tok = NumberExHelper.__m_small_money.try_parse(tt.next0_, TerminParseAttr.NO)
            if (tok is not None): 
                res.end_token = tok.end_token
        return res
    
    @staticmethod
    def _initialize() -> None:
        if (NumberExHelper._m_postfixes is not None): 
            return
        NumberExHelper._m_postfixes = TerminCollection()
        t = Termin._new483("КВАДРАТНЫЙ МЕТР", MorphLang.RU, True, "кв.м.", NumberExType.METER2)
        t.add_abridge("КВ.МЕТР")
        t.add_abridge("КВ.МЕТРА")
        t.add_abridge("КВ.М.")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("КВАДРАТНИЙ МЕТР", MorphLang.UA, True, "КВ.М.", NumberExType.METER2)
        t.add_abridge("КВ.МЕТР")
        t.add_abridge("КВ.МЕТРА")
        t.add_abridge("КВ.М.")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("КВАДРАТНЫЙ КИЛОМЕТР", MorphLang.RU, True, "кв.км.", NumberExType.KILOMETER2)
        t.add_variant("КВАДРАТНИЙ КІЛОМЕТР", True)
        t.add_abridge("КВ.КМ.")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ГЕКТАР", MorphLang.RU, True, "га", NumberExType.GEKTAR)
        t.add_abridge("ГА")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("АР", MorphLang.RU, True, "ар", NumberExType.AR)
        t.add_variant("СОТКА", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("КУБИЧЕСКИЙ МЕТР", MorphLang.RU, True, "куб.м.", NumberExType.METER3)
        t.add_variant("КУБІЧНИЙ МЕТР", True)
        t.add_abridge("КУБ.МЕТР")
        t.add_abridge("КУБ.М.")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("МЕТР", MorphLang.RU, True, "м.", NumberExType.METER)
        t.add_abridge("М.")
        t.add_abridge("M.")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("МЕТРОВЫЙ", MorphLang.RU, True, "м.", NumberExType.METER)
        t.add_variant("МЕТРОВИЙ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("МИЛЛИМЕТР", MorphLang.RU, True, "мм.", NumberExType.MILLIMETER)
        t.add_abridge("ММ")
        t.add_abridge("MM")
        t.add_variant("МІЛІМЕТР", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("МИЛЛИМЕТРОВЫЙ", MorphLang.RU, True, "мм.", NumberExType.MILLIMETER)
        t.add_variant("МІЛІМЕТРОВИЙ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("САНТИМЕТР", MorphLang.RU, True, "см.", NumberExType.SANTIMETER)
        t.add_abridge("СМ")
        t.add_abridge("CM")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("САНТИМЕТРОВЫЙ", MorphLang.RU, True, "см.", NumberExType.SANTIMETER)
        t.add_variant("САНТИМЕТРОВИЙ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("КВАДРАТНЫЙ САНТИМЕТР", MorphLang.RU, True, "кв.см.", NumberExType.SANTIMETER2)
        t.add_variant("КВАДРАТНИЙ САНТИМЕТР", True)
        t.add_abridge("КВ.СМ.")
        t.add_abridge("СМ.КВ.")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("КУБИЧЕСКИЙ САНТИМЕТР", MorphLang.RU, True, "куб.см.", NumberExType.SANTIMETER3)
        t.add_variant("КУБІЧНИЙ САНТИМЕТР", True)
        t.add_abridge("КУБ.САНТИМЕТР")
        t.add_abridge("КУБ.СМ.")
        t.add_abridge("СМ.КУБ.")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("КИЛОМЕТР", MorphLang.RU, True, "км.", NumberExType.KILOMETER)
        t.add_abridge("КМ")
        t.add_abridge("KM")
        t.add_variant("КІЛОМЕТР", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("КИЛОМЕТРОВЫЙ", MorphLang.RU, True, "км.", NumberExType.KILOMETER)
        t.add_variant("КІЛОМЕТРОВИЙ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("МИЛЯ", MorphLang.RU, True, "миль", NumberExType.KILOMETER)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ГРАММ", MorphLang.RU, True, "гр.", NumberExType.GRAMM)
        t.add_abridge("ГР")
        t.add_abridge("Г")
        t.add_variant("ГРАМ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ГРАММОВЫЙ", MorphLang.RU, True, "гр.", NumberExType.GRAMM)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("КИЛОГРАММ", MorphLang.RU, True, "кг.", NumberExType.KILOGRAM)
        t.add_abridge("КГ")
        t.add_variant("КІЛОГРАМ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("КИЛОГРАММОВЫЙ", MorphLang.RU, True, "кг.", NumberExType.KILOGRAM)
        t.add_variant("КІЛОГРАМОВИЙ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("МИЛЛИГРАММ", MorphLang.RU, True, "мг.", NumberExType.MILLIGRAM)
        t.add_abridge("МГ")
        t.add_variant("МІЛІГРАМ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("МИЛЛИГРАММОВЫЙ", MorphLang.RU, True, "мг.", NumberExType.MILLIGRAM)
        t.add_variant("МИЛЛИГРАМОВЫЙ", True)
        t.add_variant("МІЛІГРАМОВИЙ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ТОННА", MorphLang.RU, True, "т.", NumberExType.TONNA)
        t.add_abridge("Т")
        t.add_abridge("T")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ТОННЫЙ", MorphLang.RU, True, "т.", NumberExType.TONNA)
        t.add_variant("ТОННИЙ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ЛИТР", MorphLang.RU, True, "л.", NumberExType.LITR)
        t.add_abridge("Л")
        t.add_variant("ЛІТР", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ЛИТРОВЫЙ", MorphLang.RU, True, "л.", NumberExType.LITR)
        t.add_variant("ЛІТРОВИЙ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("МИЛЛИЛИТР", MorphLang.RU, True, "мл.", NumberExType.MILLILITR)
        t.add_abridge("МЛ")
        t.add_variant("МІЛІЛІТР", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("МИЛЛИЛИТРОВЫЙ", MorphLang.RU, True, "мл.", NumberExType.MILLILITR)
        t.add_variant("МІЛІЛІТРОВИЙ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ЧАС", MorphLang.RU, True, "ч.", NumberExType.HOUR)
        t.add_abridge("Ч.")
        t.add_variant("ГОДИНА", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("МИНУТА", MorphLang.RU, True, "мин.", NumberExType.MINUTE)
        t.add_abridge("МИН.")
        t.add_variant("ХВИЛИНА", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("СЕКУНДА", MorphLang.RU, True, "сек.", NumberExType.SECOND)
        t.add_abridge("СЕК.")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ГОД", MorphLang.RU, True, "г.", NumberExType.YEAR)
        t.add_abridge("Г.")
        t.add_abridge("ЛЕТ")
        t.add_variant("ЛЕТНИЙ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("МЕСЯЦ", MorphLang.RU, True, "мес.", NumberExType.MONTH)
        t.add_abridge("МЕС.")
        t.add_variant("МЕСЯЧНЫЙ", True)
        t.add_variant("КАЛЕНДАРНЫЙ МЕСЯЦ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ДЕНЬ", MorphLang.RU, True, "дн.", NumberExType.DAY)
        t.add_abridge("ДН.")
        t.add_variant("ДНЕВНЫЙ", True)
        t.add_variant("СУТКИ", True)
        t.add_variant("СУТОЧНЫЙ", True)
        t.add_variant("КАЛЕНДАРНЫЙ ДЕНЬ", True)
        t.add_variant("РАБОЧИЙ ДЕНЬ", True)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("НЕДЕЛЯ", MorphLang.RU, True, "нед.", NumberExType.WEEK)
        t.add_variant("НЕДЕЛЬНЫЙ", True)
        t.add_variant("КАЛЕНДАРНАЯ НЕДЕЛЯ", False)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ПРОЦЕНТ", MorphLang.RU, True, "%", NumberExType.PERCENT)
        t.add_variant("%", False)
        t.add_variant("ПРОЦ", True)
        t.add_abridge("ПРОЦ.")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ШТУКА", MorphLang.RU, True, "шт.", NumberExType.SHUK)
        t.add_variant("ШТ", False)
        t.add_abridge("ШТ.")
        t.add_abridge("ШТ-К")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("УПАКОВКА", MorphLang.RU, True, "уп.", NumberExType.UPAK)
        t.add_variant("УПАК", True)
        t.add_variant("УП", True)
        t.add_abridge("УПАК.")
        t.add_abridge("УП.")
        t.add_abridge("УП-КА")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("РУЛОН", MorphLang.RU, True, "рулон", NumberExType.RULON)
        t.add_variant("РУЛ", True)
        t.add_abridge("РУЛ.")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("НАБОР", MorphLang.RU, True, "набор", NumberExType.NABOR)
        t.add_variant("НАБ", True)
        t.add_abridge("НАБ.")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("КОМПЛЕКТ", MorphLang.RU, True, "компл.", NumberExType.KOMPLEKT)
        t.add_variant("КОМПЛ", True)
        t.add_abridge("КОМПЛ.")
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ПАРА", MorphLang.RU, True, "пар", NumberExType.PARA)
        NumberExHelper._m_postfixes.add(t)
        t = Termin._new483("ФЛАКОН", MorphLang.RU, True, "флак.", NumberExType.FLAKON)
        t.add_variant("ФЛ", True)
        t.add_abridge("ФЛ.")
        t.add_variant("ФЛАК", True)
        t.add_abridge("ФЛАК.")
        NumberExHelper._m_postfixes.add(t)
        for te in NumberExHelper._m_postfixes.termins: 
            ty = Utils.valToEnum(te.tag, NumberExType)
            if (not ty in NumberExHelper._m_normals_typs): 
                NumberExHelper._m_normals_typs[ty] = te.canonic_text
        NumberExHelper.__m_small_money = TerminCollection()
        t = Termin._new143("УСЛОВНАЯ ЕДИНИЦА", "УЕ", NumberExType.MONEY)
        t.add_abridge("У.Е.")
        t.add_abridge("У.E.")
        t.add_abridge("Y.Е.")
        t.add_abridge("Y.E.")
        NumberExHelper._m_postfixes.add(t)
        for k in range(3):
            str0_ = EpNerCoreInternalResourceHelper.get_string(("Money.csv" if k == 0 else ("MoneyUA.csv" if k == 1 else "MoneyEN.csv")))
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
                t.init_by_normal_text(parts[1], lang)
                t.canonic_text = parts[2]
                t.tag = NumberExType.MONEY
                for p in Utils.splitString(parts[0], ',', False): 
                    if (p != parts[1]): 
                        t0 = Termin()
                        t0.init_by_normal_text(p, None)
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
                NumberExHelper._m_postfixes.add(t)
                if (Utils.isNullOrEmpty(parts[3])): 
                    continue
                num = 0
                i = parts[3].find(' ')
                if (i < 2): 
                    continue
                wrapnum528 = RefOutArgWrapper(0)
                inoutres529 = Utils.tryParseInt(parts[3][0:0+i], wrapnum528)
                num = wrapnum528.value
                if (not inoutres529): 
                    continue
                vv = parts[3][i:].strip()
                t = Termin()
                t.init_by_normal_text(parts[4], lang)
                t.tag = (num)
                if (vv != parts[4]): 
                    t0 = Termin()
                    t0.init_by_normal_text(vv, None)
                    t.add_variant_term(t0)
                if (parts[4] == "КОПЕЙКА" or parts[4] == "КОПІЙКА"): 
                    t.add_abridge("КОП.")
                NumberExHelper.__m_small_money.add(t)
    
    _m_postfixes = None
    
    _m_normals_typs = None
    
    __m_small_money = None
    
    # static constructor for class NumberExHelper
    @staticmethod
    def _static_ctor():
        NumberExHelper._m_normals_typs = dict()

NumberExHelper._static_ctor()