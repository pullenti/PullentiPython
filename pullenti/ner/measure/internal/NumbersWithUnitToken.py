# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.measure.internal.MeasureHelper import MeasureHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.measure.internal.UnitsHelper import UnitsHelper


class NumbersWithUnitToken(MetaToken):
    """ Это для моделирования разных числовых диапазонов + единицы изменерия """
    
    class DiapTyp(IntEnum):
        UNDEFINED = 0
        LS = 0 + 1
        LE = (0 + 1) + 1
        GT = ((0 + 1) + 1) + 1
        GE = (((0 + 1) + 1) + 1) + 1
        FROM = ((((0 + 1) + 1) + 1) + 1) + 1
        TO = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        self.single_val = None
        self.plus_minus = None
        self.plus_minus_percent = False
        self.from_include = False
        self.from_val = None
        self.to_include = False
        self.to_val = None
        self.about = False
        self.units = list()
        super().__init__(b, e0_, None)
    
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
        return Utils.toStringStringIO(res)
    
    def create_refenets_tokens_with_register(self, ad : 'AnalyzerData', name : str, regist : bool=True) -> typing.List['ReferentToken']:
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.measure.MeasureReferent import MeasureReferent
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
        if (regist and ad is not None): 
            mr = (ad.register_referent(mr) if isinstance(ad.register_referent(mr), MeasureReferent) else None)
        res.append(ReferentToken(mr, self.begin_token, self.end_token))
        return res
    
    @staticmethod
    def try_parse_multi(t : 'Token', add_units : 'TerminCollection', can_omit_number : bool=False) -> typing.List['NumbersWithUnitToken']:
        from pullenti.ner.ReferentToken import ReferentToken
        if (t is None or (isinstance(t, ReferentToken))): 
            return None
        mt = NumbersWithUnitToken.try_parse(t, add_units, can_omit_number)
        if (mt is None): 
            return None
        res = list()
        if ((mt.whitespaces_after_count < 2) and MeasureHelper.is_mult_char(mt.end_token.next0_)): 
            mt2 = NumbersWithUnitToken.try_parse(mt.end_token.next0_.next0_, add_units, False)
            if (mt2 is not None): 
                mt3 = None
                if ((mt2.whitespaces_after_count < 2) and MeasureHelper.is_mult_char(mt2.end_token.next0_)): 
                    mt3 = NumbersWithUnitToken.try_parse(mt2.end_token.next0_.next0_, add_units, False)
                if (mt3 is not None and len(mt3.units) > 0): 
                    if (len(mt2.units) == 0): 
                        mt2.units = mt3.units
                if (len(mt2.units) > 0 and len(mt.units) == 0): 
                    mt.units = mt2.units
                res.append(mt)
                res.append(mt2)
                if (mt3 is not None): 
                    res.append(mt3)
                return res
        res.append(mt)
        return res
    
    @staticmethod
    def try_parse(t : 'Token', add_units : 'TerminCollection', can_omit_number : bool=False) -> 'NumbersWithUnitToken':
        return NumbersWithUnitToken.__try_parse(t, add_units, False, can_omit_number)
    
    @staticmethod
    def __try_parse(t : 'Token', add_units : 'TerminCollection', second : bool, can_omit_number : bool) -> 'NumbersWithUnitToken':
        from pullenti.ner.measure.internal.UnitToken import UnitToken
        from pullenti.ner.core.NumberExToken import NumberExToken
        if (t is None): 
            return None
        if (t.is_and and t.next0_ is not None): 
            t = t.next0_
        t0 = t
        about_ = False
        if (t.is_char('~') or t.is_value("ОКОЛО", None) or t.is_value("ПРИМЕРНО", None)): 
            t = t.next0_
            about_ = True
            if (t is None): 
                return None
        if (t0.is_char('(')): 
            mt0 = NumbersWithUnitToken.__try_parse(t.next0_, add_units, False, False)
            if (mt0 is not None and mt0.end_token.next0_ is not None and mt0.end_token.next0_.is_char(')')): 
                if (second): 
                    if (mt0.from_val is not None and mt0.to_val is not None and mt0.from_val == (- mt0.to_val)): 
                        pass
                    else: 
                        return None
                mt0.begin_token = t0
                mt0.end_token = mt0.end_token.next0_
                uu = UnitToken.try_parse_list(mt0.end_token.next0_, add_units)
                if (uu is not None and len(mt0.units) == 0): 
                    mt0.units = uu
                    mt0.end_token = uu[len(uu) - 1].end_token
                return mt0
        plusminus = False
        dty = NumbersWithUnitToken.DiapTyp.UNDEFINED
        uni = None
        tok = NumbersWithUnitToken.M_TERMINS.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            t = tok.end_token.next0_
            dty = (Utils.valToEnum(tok.termin.tag, NumbersWithUnitToken.DiapTyp))
            if (not tok.is_whitespace_after): 
                if (t is not None and t.is_char_of(":")): 
                    pass
                else: 
                    return None
            if (t is not None and t.is_char('(')): 
                uni = UnitToken.try_parse_list(t.next0_, add_units)
                if (uni is not None): 
                    t = uni[len(uni) - 1].end_token.next0_
                    while t is not None:
                        if (t.is_char_of("):")): 
                            t = t.next0_
                        else: 
                            break
                    mt0 = NumbersWithUnitToken.__try_parse(t, add_units, False, can_omit_number)
                    if (mt0 is not None and len(mt0.units) == 0): 
                        mt0.begin_token = t0
                        mt0.units = uni
                        return mt0
        elif (t.is_char('<')): 
            dty = NumbersWithUnitToken.DiapTyp.GT
            t = t.next0_
            if (t is not None and t.is_char('=')): 
                t = t.next0_
                dty = NumbersWithUnitToken.DiapTyp.GE
        elif (t.is_char('>')): 
            dty = NumbersWithUnitToken.DiapTyp.LS
            t = t.next0_
            if (t is not None and t.is_char('=')): 
                t = t.next0_
                dty = NumbersWithUnitToken.DiapTyp.LE
        elif (t.is_char('≤')): 
            dty = NumbersWithUnitToken.DiapTyp.GE
            t = t.next0_
        elif (t.is_char('≥')): 
            dty = NumbersWithUnitToken.DiapTyp.LE
            t = t.next0_
        if (t is not None and t.is_char(':')): 
            t = t.next0_
        if (t is not None): 
            if (t.is_char('+') or t.is_value("ПЛЮС", None)): 
                t = t.next0_
                if (t is not None and not t.is_whitespace_before): 
                    if (t.is_char('+')): 
                        t = t.next0_
                        plusminus = True
                    elif ((t.is_char_of("\\/") and t.next0_ is not None and not t.is_newline_after) and t.next0_.is_hiphen): 
                        t = t.next0_.next0_
                        plusminus = True
            elif (second and ((t.is_char_of("\\/÷…~") or t.is_hiphen))): 
                t = t.next0_
            elif (t.is_char('±')): 
                t = t.next0_
                plusminus = True
            elif ((second and t.is_char('.') and t.next0_ is not None) and t.next0_.is_char('.')): 
                t = t.next0_.next0_
                if (t is not None and t.is_char('.')): 
                    t = t.next0_
        if (t is None): 
            return None
        num = NumberExToken.try_parse_float_number(t, True)
        if (num is None): 
            uni = UnitToken.try_parse_list(t, add_units)
            if (uni is not None): 
                t = uni[len(uni) - 1].end_token.next0_
                delim = False
                while t is not None:
                    if (t.is_char_of(":,")): 
                        delim = True
                        t = t.next0_
                    else: 
                        break
                if (not delim): 
                    if (t is None or not t.is_whitespace_before): 
                        return None
                num = NumberExToken.try_parse_float_number(t, True)
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
                        uni.append(UnitToken._new1521(t, t, u))
                        break
                if (uni is None): 
                    return None
                res = NumbersWithUnitToken._new1522(t0, tt.end_token, about_)
                t = tt.end_token.next0_
            else: 
                if (not can_omit_number): 
                    return None
                if ((uni is not None and len(uni) == 1 and uni[0].begin_token == uni[0].end_token) and uni[0].length_char > 3): 
                    rval = (1)
                    res = NumbersWithUnitToken._new1522(t0, uni[len(uni) - 1].end_token, about_)
                    t = res.end_token.next0_
                else: 
                    return None
        else: 
            if ((t == t0 and t0.is_hiphen and not t.is_whitespace_before) and not t.is_whitespace_after and (num.real_value < 0)): 
                return None
            t = num.end_token.next0_
            res = NumbersWithUnitToken._new1522(t0, num.end_token, about_)
            rval = num.real_value
        if (uni is None): 
            uni = UnitToken.try_parse_list(t, add_units)
            if (uni is not None): 
                res.units = uni
                res.end_token = uni[len(uni) - 1].end_token
                t = res.end_token.next0_
        else: 
            res.units = uni
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
        next0__ = (None if second or plusminus or ((t is not None and t.is_newline_before)) else NumbersWithUnitToken.__try_parse(t, add_units, True, False))
        if (next0__ is not None and ((next0__.to_val is not None or next0__.single_val is not None)) and next0__.from_val is None): 
            if (len(next0__.units) > 0): 
                if (len(res.units) == 0): 
                    res.units = next0__.units
                elif (not UnitToken.can_be_equals(res.units, next0__.units)): 
                    next0__ = (None)
            elif (len(res.units) > 0): 
                next0__ = (None)
            if (next0__ is not None): 
                res.end_token = next0__.end_token
            if (next0__ is not None and next0__.to_val is not None): 
                res.to_val = next0__.to_val
                res.to_include = next0__.to_include
            elif (next0__ is not None and next0__.single_val is not None): 
                res.to_val = next0__.single_val
                res.to_include = True
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
            if (plusminus): 
                res.from_include = True
                res.from_val = (- rval)
                res.to_include = True
                res.to_val = rval
            else: 
                res.single_val = rval
        return res
    
    M_TERMINS = None
    
    M_SPEC = None
    
    @staticmethod
    def _initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        if (NumbersWithUnitToken.M_TERMINS is not None): 
            return
        NumbersWithUnitToken.M_TERMINS = TerminCollection()
        t = Termin._new118("НЕ МЕНЕЕ", NumbersWithUnitToken.DiapTyp.GE)
        t.add_variant("НЕ МЕНЬШЕ", False)
        t.add_variant("НЕ КОРОЧЕ", False)
        t.add_variant("НЕ МЕДЛЕННЕЕ", False)
        t.add_variant("НЕ МЕНЕ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new118("МЕНЕЕ", NumbersWithUnitToken.DiapTyp.LS)
        t.add_variant("МЕНЬШЕ", False)
        t.add_variant("МЕНЕ", False)
        t.add_variant("КОРОЧЕ", False)
        t.add_variant("МЕДЛЕННЕЕ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new118("НЕ БОЛЕЕ", NumbersWithUnitToken.DiapTyp.LE)
        t.add_variant("НЕ БОЛЬШЕ", False)
        t.add_variant("НЕ БОЛЕ", False)
        t.add_variant("НЕ ДЛИННЕЕ", False)
        t.add_variant("НЕ БЫСТРЕЕ", False)
        t.add_variant("НЕ ВЫШЕ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new118("БОЛЕЕ", NumbersWithUnitToken.DiapTyp.GT)
        t.add_variant("БОЛЬШЕ", False)
        t.add_variant("ДЛИННЕЕ", False)
        t.add_variant("БЫСТРЕЕ", False)
        t.add_variant("БОЛЕ", False)
        t.add_variant("ГЛУБЖЕ", False)
        t.add_variant("ВЫШЕ", False)
        t.add_variant("СВЫШЕ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new118("ОТ", NumbersWithUnitToken.DiapTyp.FROM)
        t.add_variant("С", False)
        t.add_variant("C", False)
        t.add_variant("НАЧИНАЯ С", False)
        t.add_variant("НАЧИНАЯ ОТ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new118("ДО", NumbersWithUnitToken.DiapTyp.TO)
        t.add_variant("ПО", False)
        t.add_variant("ЗАКАНЧИВАЯ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        NumbersWithUnitToken.M_SPEC = TerminCollection()
        t = Termin._new120("ПОЛЛИТРА", .5, "литр")
        t.add_variant("ПОЛУЛИТРА", False)
        NumbersWithUnitToken.M_SPEC.add(t)
        t = Termin._new120("ПОЛКИЛО", .5, "килограмм")
        t.add_variant("ПОЛКИЛОГРАММА", False)
        NumbersWithUnitToken.M_SPEC.add(t)
        t = Termin._new120("ПОЛМЕТРА", .5, "метр")
        t.add_variant("ПОЛУМЕТРА", False)
        NumbersWithUnitToken.M_SPEC.add(t)
        t = Termin._new120("ПОЛТОННЫ", .5, "тонна")
        t.add_variant("ПОЛУТОННЫ", False)
        NumbersWithUnitToken.M_SPEC.add(t)
        NumbersWithUnitToken.M_SPEC.add(t)
    
    @staticmethod
    def _new1522(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'NumbersWithUnitToken':
        res = NumbersWithUnitToken(_arg1, _arg2)
        res.about = _arg3
        return res