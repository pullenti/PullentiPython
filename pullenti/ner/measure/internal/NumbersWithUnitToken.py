# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
import math
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.measure.MeasureKind import MeasureKind
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.TextToken import TextToken
from pullenti.ner.measure.internal.MeasureHelper import MeasureHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.measure.internal.Unit import Unit
from pullenti.ner.measure.internal.UnitsHelper import UnitsHelper
from pullenti.ner.measure.MeasureReferent import MeasureReferent
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.measure.internal.UnitToken import UnitToken

class NumbersWithUnitToken(MetaToken):
    # Это для моделирования разных числовых диапазонов + единицы изменерия
    
    class DiapTyp(IntEnum):
        UNDEFINED = 0
        LS = 1
        LE = 2
        GT = 3
        GE = 4
        FROM = 5
        TO = 6
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.single_val = None
        self.plus_minus = None
        self.plus_minus_percent = False
        self.from_include = False
        self.from_val = None
        self.to_include = False
        self.to_val = None
        self.about = False
        self.not0_ = False
        self.whl = None;
        self.units = list()
        self.div_num = None;
        self.is_age = False
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.single_val is not None): 
            if (self.plus_minus is not None): 
                print("[{0} ±{1}{2}]".format(self.single_val, self.plus_minus, ("%" if self.plus_minus_percent else "")), end="", file=res, flush=True)
            else: 
                print(self.single_val, end="", file=res)
        else: 
            if (self.from_val is not None): 
                print("{0}{1}".format(('[' if self.from_include else ']'), self.from_val), end="", file=res, flush=True)
            else: 
                print("]", end="", file=res)
            print(" .. ", end="", file=res)
            if (self.to_val is not None): 
                print("{0}{1}".format(self.to_val, (']' if self.to_include else '[')), end="", file=res, flush=True)
            else: 
                print("[", end="", file=res)
        for u in self.units: 
            print(" {0}".format(str(u)), end="", file=res, flush=True)
        if (self.div_num is not None): 
            print(" / ", end="", file=res)
            print(self.div_num, end="", file=res)
        return Utils.toStringStringIO(res)
    
    def create_refenets_tokens_with_register(self, ad : 'AnalyzerData', name : str, regist : bool=True) -> typing.List['ReferentToken']:
        if (name == "T ="): 
            name = "ТЕМПЕРАТУРА"
        res = list()
        for u in self.units: 
            rt = ReferentToken(u.create_referent_with_register(ad), u.begin_token, u.end_token)
            res.append(rt)
        mr = MeasureReferent()
        templ = "1"
        if (self.single_val is not None): 
            mr.add_value(self.single_val)
            if (self.plus_minus is not None): 
                templ = "[1 ±2{0}]".format(("%" if self.plus_minus_percent else ""))
                mr.add_value(self.plus_minus)
            elif (self.about): 
                templ = "~1"
        else: 
            if (self.not0_ and ((self.from_val is None or self.to_val is None))): 
                b = self.from_include
                self.from_include = self.to_include
                self.to_include = b
                v = self.from_val
                self.from_val = self.to_val
                self.to_val = v
            num = 1
            if (self.from_val is not None): 
                mr.add_value(self.from_val)
                templ = ("[1" if self.from_include else "]1")
                num += 1
            else: 
                templ = "]"
            if (self.to_val is not None): 
                mr.add_value(self.to_val)
                templ = "{0} .. {1}{2}".format(templ, num, (']' if self.to_include else '['))
            else: 
                templ += " .. ["
        mr.template = templ
        for rt in res: 
            mr.add_slot(MeasureReferent.ATTR_UNIT, rt.referent, False, 0)
        if (name is not None): 
            mr.add_slot(MeasureReferent.ATTR_NAME, name, False, 0)
        if (self.div_num is not None): 
            dn = self.div_num.create_refenets_tokens_with_register(ad, None, True)
            res.extend(dn)
            mr.add_slot(MeasureReferent.ATTR_REF, dn[len(dn) - 1].referent, False, 0)
        ki = UnitToken.calc_kind(self.units)
        if (ki != MeasureKind.UNDEFINED): 
            mr.kind = ki
        if (regist and ad is not None): 
            mr = (Utils.asObjectOrNull(ad.register_referent(mr), MeasureReferent))
        res.append(ReferentToken(mr, self.begin_token, self.end_token))
        return res
    
    @staticmethod
    def try_parse_multi(t : 'Token', add_units : 'TerminCollection', can_omit_number : bool=False, not0__ : bool=False, can_be_non : bool=False, is_resctriction : bool=False) -> typing.List['NumbersWithUnitToken']:
        if (t is None or (isinstance(t, ReferentToken))): 
            return None
        tt0 = t
        if (tt0.is_char('(')): 
            whd = NumbersWithUnitToken._try_parsewhl(tt0)
            if (whd is not None): 
                tt0 = whd.end_token
            res0 = NumbersWithUnitToken.try_parse_multi(tt0.next0_, add_units, False, can_omit_number, can_be_non, False)
            if (res0 is not None): 
                res0[0].whl = whd
                tt2 = res0[len(res0) - 1].end_token.next0_
                if (tt2 is not None and tt2.is_char_of(",")): 
                    tt2 = tt2.next0_
                if (whd is not None): 
                    return res0
                if (tt2 is not None and tt2.is_char(')')): 
                    res0[len(res0) - 1].end_token = tt2
                    return res0
        mt = NumbersWithUnitToken.try_parse(t, add_units, can_omit_number, not0__, can_be_non, is_resctriction)
        if (mt is None): 
            return None
        res = list()
        nnn = None
        if (mt.whitespaces_after_count < 2): 
            if (MeasureHelper.is_mult_char(mt.end_token.next0_)): 
                nnn = mt.end_token.next0_.next0_
            elif ((isinstance(mt.end_token, NumberToken)) and MeasureHelper.is_mult_char(mt.end_token.end_token)): 
                nnn = mt.end_token.next0_
        if (nnn is not None): 
            mt2 = NumbersWithUnitToken.try_parse(nnn, add_units, not0__, False, False, False)
            if (mt2 is not None): 
                mt3 = None
                nnn = (None)
                if (mt2.whitespaces_after_count < 2): 
                    if (MeasureHelper.is_mult_char(mt2.end_token.next0_)): 
                        nnn = mt2.end_token.next0_.next0_
                    elif ((isinstance(mt2.end_token, NumberToken)) and MeasureHelper.is_mult_char(mt2.end_token.end_token)): 
                        nnn = mt2.end_token.next0_
                if (nnn is not None): 
                    mt3 = NumbersWithUnitToken.try_parse(nnn, add_units, False, False, False, False)
                if (mt3 is None): 
                    tt2 = mt2.end_token.next0_
                    if (tt2 is not None and not tt2.is_whitespace_before): 
                        if (not tt2.is_char_of(",.;")): 
                            return None
                if (mt3 is not None and len(mt3.units) > 0): 
                    if (len(mt2.units) == 0): 
                        mt2.units = mt3.units
                res.append(mt)
                if (mt2 is not None): 
                    if (len(mt2.units) > 0 and len(mt.units) == 0): 
                        mt.units = mt2.units
                    res.append(mt2)
                    if (mt3 is not None): 
                        res.append(mt3)
                return res
        if ((not mt.is_whitespace_after and MeasureHelper.is_mult_char_end(mt.end_token.next0_) and (isinstance(mt.end_token.next0_.next0_, NumberToken))) and len(mt.units) == 0): 
            utxt = mt.end_token.next0_.term
            utxt = utxt[0:0+len(utxt) - 1]
            terms = UnitsHelper.TERMINS.find_termins_by_string(utxt, None)
            if (terms is not None and len(terms) > 0): 
                mt.units.append(UnitToken._new1622(mt.end_token.next0_, mt.end_token.next0_, Utils.asObjectOrNull(terms[0].tag, Unit)))
                mt.end_token = mt.end_token.next0_
                res1 = NumbersWithUnitToken.try_parse_multi(mt.end_token.next0_, add_units, False, False, False, False)
                if (res1 is not None): 
                    res1.insert(0, mt)
                    return res1
        res.append(mt)
        return res
    
    @staticmethod
    def try_parse(t : 'Token', add_units : 'TerminCollection', can_omit_number : bool=False, not0__ : bool=False, can_be_nan : bool=False, is_resctriction : bool=False) -> 'NumbersWithUnitToken':
        """ Попробовать выделить с указанной позиции
        
        Args:
            t(Token): 
        
        """
        if (t is None): 
            return None
        res = NumbersWithUnitToken._try_parse(t, add_units, is_resctriction, can_omit_number, can_be_nan)
        if (res is not None): 
            res.not0_ = not0__
        return res
    
    @staticmethod
    def _is_min_or_max(t : 'Token', res : int) -> 'Token':
        if (t is None): 
            return None
        if (t.is_value("МИНИМАЛЬНЫЙ", None) or t.is_value("МИНИМУМ", None) or t.is_value("MINIMUM", None)): 
            res.value = -1
            return t
        if (t.is_value("MIN", None) or t.is_value("МИН", None)): 
            res.value = -1
            if (t.next0_ is not None and t.next0_.is_char('.')): 
                t = t.next0_
            return t
        if (t.is_value("МАКСИМАЛЬНЫЙ", None) or t.is_value("МАКСИМУМ", None) or t.is_value("MAXIMUM", None)): 
            res.value = 1
            return t
        if (t.is_value("MAX", None) or t.is_value("МАКС", None) or t.is_value("МАХ", None)): 
            res.value = 1
            if (t.next0_ is not None and t.next0_.is_char('.')): 
                t = t.next0_
            return t
        if (t.is_char('(')): 
            t = NumbersWithUnitToken._is_min_or_max(t.next0_, res)
            if (t is not None and t.next0_ is not None and t.next0_.is_char(')')): 
                t = t.next0_
            return t
        return None
    
    @staticmethod
    def _try_parse(t : 'Token', add_units : 'TerminCollection', second : bool, can_omit_number : bool, can_be_nan : bool) -> 'NumbersWithUnitToken':
        if (t is None): 
            return None
        while t is not None:
            if (t.is_comma_and or t.is_value("НО", None)): 
                t = t.next0_
            else: 
                break
        t0 = t
        about_ = False
        has_keyw = False
        is_diap_keyw = False
        min_max = 0
        wrapmin_max1629 = RefOutArgWrapper(min_max)
        ttt = NumbersWithUnitToken._is_min_or_max(t, wrapmin_max1629)
        min_max = wrapmin_max1629.value
        if (ttt is not None): 
            t = ttt.next0_
            if (t is None): 
                return None
        if (t is None): 
            return None
        if (t.is_char('~') or t.is_value("ОКОЛО", None) or t.is_value("ПРИМЕРНО", None)): 
            t = t.next0_
            about_ = True
            has_keyw = True
            if (t is None): 
                return None
        if (t.is_value("В", None) and t.next0_ is not None): 
            if (t.next0_.is_value("ПРЕДЕЛ", None) or t.is_value("ДИАПАЗОН", None)): 
                t = t.next0_.next0_
                if (t is None): 
                    return None
                is_diap_keyw = True
        if (t0.is_char('(')): 
            mt0 = NumbersWithUnitToken._try_parse(t.next0_, add_units, False, False, False)
            if (mt0 is not None and mt0.end_token.next0_ is not None and mt0.end_token.next0_.is_char(')')): 
                if (second): 
                    if (mt0.from_val is not None and mt0.to_val is not None and mt0.from_val == (- mt0.to_val)): 
                        pass
                    else: 
                        return None
                mt0.begin_token = t0
                mt0.end_token = mt0.end_token.next0_
                uu = UnitToken.try_parse_list(mt0.end_token.next0_, add_units, False)
                if (uu is not None and len(mt0.units) == 0): 
                    mt0.units = uu
                    mt0.end_token = uu[len(uu) - 1].end_token
                return mt0
        plusminus = False
        unit_before = False
        is_age_ = False
        dty = NumbersWithUnitToken.DiapTyp.UNDEFINED
        whd = None
        uni = None
        tok = (None if NumbersWithUnitToken.M_TERMINS is None else NumbersWithUnitToken.M_TERMINS.try_parse(t, TerminParseAttr.NO))
        if (tok is not None): 
            if (tok.end_token.is_value("СТАРШЕ", None) or tok.end_token.is_value("МЛАДШЕ", None)): 
                is_age_ = True
            t = tok.end_token.next0_
            dty = (Utils.valToEnum(tok.termin.tag, NumbersWithUnitToken.DiapTyp))
            has_keyw = True
            if (not tok.is_whitespace_after): 
                if (t is None): 
                    return None
                if (isinstance(t, NumberToken)): 
                    if (tok.begin_token == tok.end_token and not tok.chars.is_all_lower): 
                        return None
                elif (t.is_comma and t.next0_ is not None and t.next0_.is_value("ЧЕМ", None)): 
                    t = t.next0_.next0_
                    if (t is not None and t.morph.class0_.is_preposition): 
                        t = t.next0_
                elif (t.is_char_of(":,(") or t.is_table_control_char): 
                    pass
                else: 
                    return None
            if (t is not None and t.is_char('(')): 
                uni = UnitToken.try_parse_list(t.next0_, add_units, False)
                if (uni is not None): 
                    t = uni[len(uni) - 1].end_token.next0_
                    while t is not None:
                        if (t.is_char_of("):")): 
                            t = t.next0_
                        else: 
                            break
                    mt0 = NumbersWithUnitToken._try_parse(t, add_units, False, can_omit_number, False)
                    if (mt0 is not None and len(mt0.units) == 0): 
                        mt0.begin_token = t0
                        mt0.units = uni
                        return mt0
                whd = NumbersWithUnitToken._try_parsewhl(t)
                if (whd is not None): 
                    t = whd.end_token.next0_
            elif (t is not None and t.is_value("IP", None)): 
                uni = UnitToken.try_parse_list(t, add_units, False)
                if (uni is not None): 
                    t = uni[len(uni) - 1].end_token.next0_
            if ((t is not None and t.is_hiphen and t.is_whitespace_before) and t.is_whitespace_after): 
                t = t.next0_
        elif (t.is_char('<')): 
            dty = NumbersWithUnitToken.DiapTyp.LS
            t = t.next0_
            has_keyw = True
            if (t is not None and t.is_char('=')): 
                t = t.next0_
                dty = NumbersWithUnitToken.DiapTyp.LE
        elif (t.is_char('>')): 
            dty = NumbersWithUnitToken.DiapTyp.GT
            t = t.next0_
            has_keyw = True
            if (t is not None and t.is_char('=')): 
                t = t.next0_
                dty = NumbersWithUnitToken.DiapTyp.GE
        elif (t.is_char('≤')): 
            dty = NumbersWithUnitToken.DiapTyp.LE
            has_keyw = True
            t = t.next0_
        elif (t.is_char('≥')): 
            dty = NumbersWithUnitToken.DiapTyp.GE
            has_keyw = True
            t = t.next0_
        elif (t.is_value("IP", None)): 
            uni = UnitToken.try_parse_list(t, add_units, False)
            if (uni is not None): 
                t = uni[len(uni) - 1].end_token.next0_
        elif (t.is_value("ЗА", None) and (isinstance(t.next0_, NumberToken))): 
            dty = NumbersWithUnitToken.DiapTyp.GE
            t = t.next0_
        while t is not None and ((t.is_char_of(":,") or t.is_value("ЧЕМ", None) or t.is_table_control_char)):
            t = t.next0_
        if (t is not None): 
            if (t.is_char('+') or t.is_value("ПЛЮС", None)): 
                t = t.next0_
                if (t is not None and not t.is_whitespace_before): 
                    if (t.is_hiphen): 
                        t = t.next0_
                        plusminus = True
                    elif ((t.is_char_of("\\/") and t.next0_ is not None and not t.is_newline_after) and t.next0_.is_hiphen): 
                        t = t.next0_.next0_
                        plusminus = True
            elif (second and ((t.is_char_of("\\/÷…~")))): 
                t = t.next0_
            elif ((t.is_hiphen and t == t0 and not second) and NumbersWithUnitToken.M_TERMINS.try_parse(t.next0_, TerminParseAttr.NO) is not None): 
                tok = NumbersWithUnitToken.M_TERMINS.try_parse(t.next0_, TerminParseAttr.NO)
                t = tok.end_token.next0_
                dty = (Utils.valToEnum(tok.termin.tag, NumbersWithUnitToken.DiapTyp))
            elif (t.is_hiphen and t == t0 and ((t.is_whitespace_after or second))): 
                t = t.next0_
            elif (t.is_char('±')): 
                t = t.next0_
                plusminus = True
                has_keyw = True
            elif ((second and t.is_char('.') and t.next0_ is not None) and t.next0_.is_char('.')): 
                t = t.next0_.next0_
                if (t is not None and t.is_char('.')): 
                    t = t.next0_
        num = NumberHelper.try_parse_real_number(t, True, False)
        if (num is None): 
            uni = UnitToken.try_parse_list(t, add_units, False)
            if (uni is not None): 
                unit_before = True
                t = uni[len(uni) - 1].end_token.next0_
                delim = False
                while t is not None:
                    if (t.is_char_of(":,")): 
                        delim = True
                        t = t.next0_
                    elif (t.is_hiphen and t.is_whitespace_after): 
                        delim = True
                        t = t.next0_
                    else: 
                        break
                if (not delim): 
                    if (t is None): 
                        if (has_keyw and can_be_nan): 
                            pass
                        else: 
                            return None
                    elif (not t.is_whitespace_before): 
                        return None
                    if (t.next0_ is not None and t.is_hiphen and t.is_whitespace_after): 
                        delim = True
                        t = t.next0_
                num = NumberHelper.try_parse_real_number(t, True, False)
        res = None
        rval = 0
        if (num is None): 
            tt = NumbersWithUnitToken.M_SPEC.try_parse(t, TerminParseAttr.NO)
            if (tt is not None): 
                rval = (tt.termin.tag)
                unam = tt.termin.tag2
                for u in UnitsHelper.UNITS: 
                    if (u.fullname_cyr == unam): 
                        uni = list()
                        uni.append(UnitToken._new1622(t, t, u))
                        break
                if (uni is None): 
                    return None
                res = NumbersWithUnitToken._new1624(t0, tt.end_token, about_)
                t = tt.end_token.next0_
            else: 
                if (not can_omit_number and not has_keyw and not can_be_nan): 
                    return None
                if ((uni is not None and len(uni) == 1 and uni[0].begin_token == uni[0].end_token) and uni[0].length_char > 3): 
                    rval = (1)
                    res = NumbersWithUnitToken._new1624(t0, uni[len(uni) - 1].end_token, about_)
                    t = res.end_token.next0_
                elif (has_keyw and can_be_nan): 
                    rval = math.nan
                    res = NumbersWithUnitToken._new1624(t0, t0, about_)
                    if (t is not None): 
                        res.end_token = t.previous
                    else: 
                        t = t0
                        while t is not None: 
                            res.end_token = t
                            t = t.next0_
                else: 
                    return None
        else: 
            if ((t == t0 and t0.is_hiphen and not t.is_whitespace_before) and not t.is_whitespace_after and (num.real_value < 0)): 
                num = NumberHelper.try_parse_real_number(t.next0_, True, False)
                if (num is None): 
                    return None
            if (t == t0 and (isinstance(t, NumberToken)) and t.morph.class0_.is_adjective): 
                nn = Utils.asObjectOrNull(t.end_token, TextToken)
                if (nn is None): 
                    return None
                norm = nn.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                if ((norm.endswith("Ь") or norm == "ЧЕТЫРЕ" or norm == "ТРИ") or norm == "ДВА"): 
                    pass
                else: 
                    mi = MorphologyService.get_word_base_info("КОКО" + nn.term, None, False, False)
                    if (mi.class0_.is_adjective): 
                        return None
            t = num.end_token.next0_
            res = NumbersWithUnitToken._new1624(t0, num.end_token, about_)
            rval = num.real_value
        if (uni is None): 
            uni = UnitToken.try_parse_list(t, add_units, False)
            if (uni is not None): 
                if ((plusminus and second and len(uni) >= 1) and uni[0].unit == UnitsHelper.UPERCENT): 
                    res.end_token = uni[0].end_token
                    res.plus_minus_percent = True
                    tt1 = uni[0].end_token.next0_
                    uni = UnitToken.try_parse_list(tt1, add_units, False)
                    if (uni is not None): 
                        res.units = uni
                        res.end_token = uni[len(uni) - 1].end_token
                else: 
                    res.units = uni
                    res.end_token = uni[len(uni) - 1].end_token
                t = res.end_token.next0_
        else: 
            res.units = uni
            if (len(uni) > 1): 
                uni1 = UnitToken.try_parse_list(t, add_units, False)
                if (((uni1 is not None and uni1[0].unit == uni[0].unit and (len(uni1) < len(uni))) and uni[len(uni1)].pow0_ == -1 and uni1[len(uni1) - 1].end_token.next0_ is not None) and uni1[len(uni1) - 1].end_token.next0_.is_char_of("/\\")): 
                    num2 = NumbersWithUnitToken._try_parse(uni1[len(uni1) - 1].end_token.next0_.next0_, add_units, False, False, False)
                    if (num2 is not None and num2.units is not None and num2.units[0].unit == uni[len(uni1)].unit): 
                        res.units = uni1
                        res.div_num = num2
                        res.end_token = num2.end_token
        res.whl = whd
        if (dty != NumbersWithUnitToken.DiapTyp.UNDEFINED): 
            if (dty == NumbersWithUnitToken.DiapTyp.GE or dty == NumbersWithUnitToken.DiapTyp.FROM): 
                res.from_include = True
                res.from_val = rval
            elif (dty == NumbersWithUnitToken.DiapTyp.GT): 
                res.from_include = False
                res.from_val = rval
            elif (dty == NumbersWithUnitToken.DiapTyp.LE or dty == NumbersWithUnitToken.DiapTyp.TO): 
                res.to_include = True
                res.to_val = rval
            elif (dty == NumbersWithUnitToken.DiapTyp.LS): 
                res.to_include = False
                res.to_val = rval
        is_second_max = False
        if (not second): 
            iii = 0
            wrapiii1628 = RefOutArgWrapper(iii)
            ttt = NumbersWithUnitToken._is_min_or_max(t, wrapiii1628)
            iii = wrapiii1628.value
            if (ttt is not None and iii > 0): 
                is_second_max = True
                t = ttt.next0_
        next0__ = (None if second or plusminus or ((t is not None and ((t.is_table_control_char or t.is_newline_before)))) else NumbersWithUnitToken._try_parse(t, add_units, True, False, can_be_nan))
        if (next0__ is not None and (isinstance(t.previous, NumberToken))): 
            if (MeasureHelper.is_mult_char(t.previous.end_token)): 
                next0__ = (None)
        if (next0__ is not None and ((next0__.to_val is not None or next0__.single_val is not None)) and next0__.from_val is None): 
            if ((((next0__.begin_token.is_char('+') and next0__.single_val is not None and not math.isnan(next0__.single_val)) and next0__.end_token.next0_ is not None and next0__.end_token.next0_.is_char_of("\\/")) and next0__.end_token.next0_.next0_ is not None and next0__.end_token.next0_.next0_.is_hiphen) and not has_keyw and not math.isnan(rval)): 
                next2 = NumbersWithUnitToken._try_parse(next0__.end_token.next0_.next0_.next0_, add_units, True, False, False)
                if (next2 is not None and next2.single_val is not None and not math.isnan(next2.single_val)): 
                    res.from_val = (rval - next2.single_val)
                    res.from_include = True
                    res.to_val = (rval + next0__.single_val)
                    res.to_include = True
                    if (next2.units is not None and len(res.units) == 0): 
                        res.units = next2.units
                    res.end_token = next2.end_token
                    return res
            if (len(next0__.units) > 0): 
                if (len(res.units) == 0): 
                    res.units = next0__.units
                elif (not UnitToken.can_be_equals(res.units, next0__.units)): 
                    next0__ = (None)
            elif (len(res.units) > 0 and not unit_before and not next0__.plus_minus_percent): 
                next0__ = (None)
            if (next0__ is not None): 
                res.end_token = next0__.end_token
            if (next0__ is not None and next0__.to_val is not None): 
                res.to_val = next0__.to_val
                res.to_include = next0__.to_include
            elif (next0__ is not None and next0__.single_val is not None): 
                if (next0__.begin_token.is_char_of("/\\")): 
                    res.div_num = next0__
                    res.single_val = rval
                    return res
                elif (next0__.plus_minus_percent): 
                    res.single_val = rval
                    res.plus_minus = next0__.single_val
                    res.plus_minus_percent = True
                    res.to_include = True
                else: 
                    res.to_val = next0__.single_val
                    res.to_include = True
            if (next0__ is not None): 
                if (res.from_val is None): 
                    res.from_val = rval
                    res.from_include = True
                return res
        elif ((next0__ is not None and next0__.from_val is not None and next0__.to_val is not None) and next0__.to_val == (- next0__.from_val)): 
            if (len(next0__.units) == 1 and next0__.units[0].unit == UnitsHelper.UPERCENT and len(res.units) > 0): 
                res.single_val = rval
                res.plus_minus = next0__.to_val
                res.plus_minus_percent = True
                res.end_token = next0__.end_token
                return res
            if (len(next0__.units) == 0): 
                res.single_val = rval
                res.plus_minus = next0__.to_val
                res.end_token = next0__.end_token
                return res
            res.from_val = (next0__.from_val + rval)
            res.from_include = True
            res.to_val = (next0__.to_val + rval)
            res.to_include = True
            res.end_token = next0__.end_token
            if (len(next0__.units) > 0): 
                res.units = next0__.units
            return res
        if (dty == NumbersWithUnitToken.DiapTyp.UNDEFINED): 
            if (plusminus and ((not res.plus_minus_percent or not second))): 
                res.from_include = True
                res.from_val = (- rval)
                res.to_include = True
                res.to_val = rval
            else: 
                res.single_val = rval
                res.plus_minus_percent = plusminus
        if (is_age_): 
            res.is_age = True
        return res
    
    @staticmethod
    def _try_parsewhl(t : 'Token') -> 'MetaToken':
        """ Это распознавание написаний ГхШхВ
        
        Args:
            t(Token): 
        
        """
        if (not (isinstance(t, TextToken))): 
            return None
        if (t.is_char_of(":-")): 
            re0 = NumbersWithUnitToken._try_parsewhl(t.next0_)
            if (re0 is not None): 
                return re0
        if (t.is_char_of("(")): 
            re0 = NumbersWithUnitToken._try_parsewhl(t.next0_)
            if (re0 is not None): 
                if (re0.end_token.next0_ is not None and re0.end_token.next0_.is_char(')')): 
                    re0.begin_token = t
                    re0.end_token = re0.end_token.next0_
                    return re0
        txt = t.term
        nams = None
        if (len(txt) == 5 and ((txt[1] == 'Х' or txt[1] == 'X')) and ((txt[3] == 'Х' or txt[3] == 'X'))): 
            nams = list()
            for i in range(3):
                ch = txt[i * 2]
                if (ch == 'Г'): 
                    nams.append("ГЛУБИНА")
                elif (ch == 'В' or ch == 'H' or ch == 'Н'): 
                    nams.append("ВЫСОТА")
                elif (ch == 'Ш' or ch == 'B' or ch == 'W'): 
                    nams.append("ШИРИНА")
                elif (ch == 'Д' or ch == 'L'): 
                    nams.append("ДЛИНА")
                elif (ch == 'D'): 
                    nams.append("ДИАМЕТР")
                else: 
                    return None
            return MetaToken._new836(t, t, nams)
        t0 = t
        t1 = t
        while t is not None: 
            if (not (isinstance(t, TextToken)) or ((t.whitespaces_before_count > 1 and t != t0))): 
                break
            term = t.term
            if (term.endswith("X") or term.endswith("Х")): 
                term = term[0:0+len(term) - 1]
            nam = None
            if (((t.is_value("ДЛИНА", None) or t.is_value("ДЛИННА", None) or term == "Д") or term == "ДЛ" or term == "ДЛИН") or term == "L"): 
                nam = "ДЛИНА"
            elif (((t.is_value("ШИРИНА", None) or t.is_value("ШИРОТА", None) or term == "Ш") or term == "ШИР" or term == "ШИРИН") or term == "W" or term == "B"): 
                nam = "ШИРИНА"
            elif ((t.is_value("ГЛУБИНА", None) or term == "Г" or term == "ГЛ") or term == "ГЛУБ"): 
                nam = "ГЛУБИНА"
            elif ((t.is_value("ВЫСОТА", None) or term == "В" or term == "ВЫС") or term == "H" or term == "Н"): 
                nam = "ВЫСОТА"
            elif (t.is_value("ДИАМЕТР", None) or term == "D" or term == "ДИАМ"): 
                nam = "ДИАМЕТР"
            else: 
                break
            if (nams is None): 
                nams = list()
            nams.append(nam)
            t1 = t
            if (t.next0_ is not None and t.next0_.is_char('.')): 
                t = t.next0_
                t1 = t
            if (t.next0_ is None): 
                break
            if (MeasureHelper.is_mult_char(t.next0_) or t.next0_.is_comma or t.next0_.is_char_of("\\/")): 
                t = t.next0_
            t = t.next0_
        if (nams is None or (len(nams) < 2)): 
            return None
        return MetaToken._new836(t0, t1, nams)
    
    M_TERMINS = None
    
    M_SPEC = None
    
    @staticmethod
    def _initialize() -> None:
        if (NumbersWithUnitToken.M_TERMINS is not None): 
            return
        NumbersWithUnitToken.M_TERMINS = TerminCollection()
        t = Termin._new100("НЕ МЕНЕЕ", NumbersWithUnitToken.DiapTyp.GE)
        t.add_variant("НЕ МЕНЬШЕ", False)
        t.add_variant("НЕ КОРОЧЕ", False)
        t.add_variant("НЕ МЕДЛЕННЕЕ", False)
        t.add_variant("НЕ НИЖЕ", False)
        t.add_variant("НЕ МОЛОЖЕ", False)
        t.add_variant("НЕ ДЕШЕВЛЕ", False)
        t.add_variant("НЕ РЕЖЕ", False)
        t.add_variant("НЕ МЕНЕ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new100("МЕНЕЕ", NumbersWithUnitToken.DiapTyp.LS)
        t.add_variant("МЕНЬШЕ", False)
        t.add_variant("МЕНЕ", False)
        t.add_variant("КОРОЧЕ", False)
        t.add_variant("МЕДЛЕННЕЕ", False)
        t.add_variant("НИЖЕ", False)
        t.add_variant("МЛАДШЕ", False)
        t.add_variant("ДЕШЕВЛЕ", False)
        t.add_variant("РЕЖЕ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new100("НЕ БОЛЕЕ", NumbersWithUnitToken.DiapTyp.LE)
        t.add_variant("НЕ БОЛЬШЕ", False)
        t.add_variant("НЕ БОЛЕ", False)
        t.add_variant("НЕ ДЛИННЕЕ", False)
        t.add_variant("НЕ БЫСТРЕЕ", False)
        t.add_variant("НЕ ВЫШЕ", False)
        t.add_variant("НЕ ПОЗДНЕЕ", False)
        t.add_variant("НЕ ДОЛЬШЕ", False)
        t.add_variant("НЕ СТАРШЕ", False)
        t.add_variant("НЕ ДОРОЖЕ", False)
        t.add_variant("НЕ ЧАЩЕ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new100("БОЛЕЕ", NumbersWithUnitToken.DiapTyp.GT)
        t.add_variant("БОЛЬШЕ", False)
        t.add_variant("ДЛИННЕЕ", False)
        t.add_variant("БЫСТРЕЕ", False)
        t.add_variant("БОЛЕ", False)
        t.add_variant("ЧАЩЕ", False)
        t.add_variant("ГЛУБЖЕ", False)
        t.add_variant("ВЫШЕ", False)
        t.add_variant("СВЫШЕ", False)
        t.add_variant("СТАРШЕ", False)
        t.add_variant("ДОРОЖЕ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new100("ОТ", NumbersWithUnitToken.DiapTyp.FROM)
        t.add_variant("С", False)
        t.add_variant("C", False)
        t.add_variant("НАЧИНАЯ С", False)
        t.add_variant("НАЧИНАЯ ОТ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new100("ДО", NumbersWithUnitToken.DiapTyp.TO)
        t.add_variant("ПО", False)
        t.add_variant("ЗАКАНЧИВАЯ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new100("НЕ ХУЖЕ", NumbersWithUnitToken.DiapTyp.UNDEFINED)
        NumbersWithUnitToken.M_TERMINS.add(t)
        NumbersWithUnitToken.M_SPEC = TerminCollection()
        t = Termin._new102("ПОЛЛИТРА", 0.5, "литр")
        t.add_variant("ПОЛУЛИТРА", False)
        NumbersWithUnitToken.M_SPEC.add(t)
        t = Termin._new102("ПОЛКИЛО", 0.5, "килограмм")
        t.add_variant("ПОЛКИЛОГРАММА", False)
        NumbersWithUnitToken.M_SPEC.add(t)
        t = Termin._new102("ПОЛМЕТРА", 0.5, "метр")
        t.add_variant("ПОЛУМЕТРА", False)
        NumbersWithUnitToken.M_SPEC.add(t)
        t = Termin._new102("ПОЛТОННЫ", 0.5, "тонна")
        t.add_variant("ПОЛУТОННЫ", False)
        NumbersWithUnitToken.M_SPEC.add(t)
        NumbersWithUnitToken.M_SPEC.add(t)
    
    @staticmethod
    def _new1615(_arg1 : 'Token', _arg2 : 'Token', _arg3 : float) -> 'NumbersWithUnitToken':
        res = NumbersWithUnitToken(_arg1, _arg2)
        res.single_val = _arg3
        return res
    
    @staticmethod
    def _new1624(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'NumbersWithUnitToken':
        res = NumbersWithUnitToken(_arg1, _arg2)
        res.about = _arg3
        return res