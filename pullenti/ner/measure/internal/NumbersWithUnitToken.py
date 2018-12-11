# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.measure.internal.Unit import Unit
from pullenti.ner.TextToken import TextToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.measure.internal.UnitsHelper import UnitsHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.Referent import Referent
from pullenti.ner.measure.internal.MeasureHelper import MeasureHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.NumberExToken import NumberExToken
from pullenti.ner.measure.MeasureKind import MeasureKind
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.measure.MeasureReferent import MeasureReferent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.measure.internal.UnitToken import UnitToken

class NumbersWithUnitToken(MetaToken):
    """ Это для моделирования разных числовых диапазонов + единицы изменерия """
    
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
        self.units = list()
        self.div_num = None;
    
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
    
    def createRefenetsTokensWithRegister(self, ad : 'AnalyzerData', name : str, regist : bool=True) -> typing.List['ReferentToken']:
        res = list()
        for u in self.units: 
            rt = ReferentToken(u.createReferentWithRegister(ad), u.begin_token, u.end_token)
            res.append(rt)
        mr = MeasureReferent()
        templ = "1"
        if (self.single_val is not None): 
            mr.addValue(self.single_val)
            if (self.plus_minus is not None): 
                templ = "[1 ±2{0}]".format(("%" if self.plus_minus_percent else ""))
                mr.addValue(self.plus_minus)
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
                mr.addValue(self.from_val)
                templ = ("[1" if self.from_include else "]1")
                num += 1
            else: 
                templ = "]"
            if (self.to_val is not None): 
                mr.addValue(self.to_val)
                templ = "{0} .. {1}{2}".format(templ, num, (']' if self.to_include else '['))
            else: 
                templ += " .. ["
        mr.template = templ
        for rt in res: 
            mr.addSlot(MeasureReferent.ATTR_UNIT, rt.referent, False, 0)
        if (name is not None): 
            mr.addSlot(MeasureReferent.ATTR_NAME, name, False, 0)
        if (self.div_num is not None): 
            dn = self.div_num.createRefenetsTokensWithRegister(ad, None, True)
            res.extend(dn)
            mr.addSlot(MeasureReferent.ATTR_REF, dn[len(dn) - 1].referent, False, 0)
        ki = UnitToken.calcKind(self.units)
        if (ki != MeasureKind.UNDEFINED): 
            mr.kind = ki
        if (regist and ad is not None): 
            mr = (Utils.asObjectOrNull(ad.registerReferent(mr), MeasureReferent))
        res.append(ReferentToken(mr, self.begin_token, self.end_token))
        return res
    
    @staticmethod
    def tryParseMulti(t : 'Token', add_units : 'TerminCollection', can_omit_number : bool=False, not0__ : bool=False) -> typing.List['NumbersWithUnitToken']:
        if (t is None or (isinstance(t, ReferentToken))): 
            return None
        if (t.isChar('(')): 
            res0 = NumbersWithUnitToken.tryParseMulti(t.next0_, add_units, False, can_omit_number)
            if (res0 is not None and res0[len(res0) - 1].end_token.next0_ is not None and res0[len(res0) - 1].end_token.next0_.isChar(')')): 
                res0[len(res0) - 1].end_token = res0[len(res0) - 1].end_token.next0_
                return res0
        mt = NumbersWithUnitToken.tryParse(t, add_units, can_omit_number, not0__)
        if (mt is None): 
            return None
        res = list()
        if ((mt.whitespaces_after_count < 2) and MeasureHelper.isMultChar(mt.end_token.next0_)): 
            mt2 = NumbersWithUnitToken.tryParse(mt.end_token.next0_.next0_, add_units, not0__, False)
            if (mt2 is not None): 
                mt3 = None
                if ((mt2.whitespaces_after_count < 2) and MeasureHelper.isMultChar(mt2.end_token.next0_)): 
                    mt3 = NumbersWithUnitToken.tryParse(mt2.end_token.next0_.next0_, add_units, False, False)
                if (mt3 is None): 
                    tt2 = mt2.end_token.next0_
                    if (tt2 is not None and not tt2.is_whitespace_before): 
                        if (not tt2.isCharOf(",.;")): 
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
        if ((not mt.is_whitespace_after and MeasureHelper.isMultCharEnd(mt.end_token.next0_) and (isinstance(mt.end_token.next0_.next0_, NumberToken))) and len(mt.units) == 0): 
            utxt = (mt.end_token.next0_).term
            utxt = utxt[0:0+len(utxt) - 1]
            terms = UnitsHelper.TERMINS.tryAttachStr(utxt, None)
            if (terms is not None and len(terms) > 0): 
                mt.units.append(UnitToken._new1530(mt.end_token.next0_, mt.end_token.next0_, Utils.asObjectOrNull(terms[0].tag, Unit)))
                mt.end_token = mt.end_token.next0_
                res1 = NumbersWithUnitToken.tryParseMulti(mt.end_token.next0_, add_units, False, False)
                if (res1 is not None): 
                    res1.insert(0, mt)
                    return res1
        res.append(mt)
        return res
    
    @staticmethod
    def tryParse(t : 'Token', add_units : 'TerminCollection', can_omit_number : bool=False, not0__ : bool=False) -> 'NumbersWithUnitToken':
        """ Попробовать выделить с указанной позиции
        
        Args:
            t(Token): 
        
        """
        if (t is None): 
            return None
        res = NumbersWithUnitToken._tryParse(t, add_units, False, can_omit_number)
        if (res is not None): 
            res.not0_ = not0__
        return res
    
    @staticmethod
    def _isMinOrMax(t : 'Token', res : int) -> 'Token':
        if (t is None): 
            return None
        if (t.isValue("МИНИМАЛЬНЫЙ", None) or t.isValue("МИНИМУМ", None) or t.isValue("MINIMUM", None)): 
            res.value = -1
            return t
        if (t.isValue("MIN", None) or t.isValue("МИН", None)): 
            res.value = -1
            if (t.next0_ is not None and t.next0_.isChar('.')): 
                t = t.next0_
            return t
        if (t.isValue("МАКСИМАЛЬНЫЙ", None) or t.isValue("МАКСИМУМ", None) or t.isValue("MAXIMUM", None)): 
            res.value = 1
            return t
        if (t.isValue("MAX", None) or t.isValue("МАКС", None) or t.isValue("МАХ", None)): 
            res.value = 1
            if (t.next0_ is not None and t.next0_.isChar('.')): 
                t = t.next0_
            return t
        if (t.isChar('(')): 
            t = NumbersWithUnitToken._isMinOrMax(t.next0_, res)
            if (t is not None and t.next0_ is not None and t.next0_.isChar(')')): 
                t = t.next0_
            return t
        return None
    
    @staticmethod
    def _tryParse(t : 'Token', add_units : 'TerminCollection', second : bool, can_omit_number : bool) -> 'NumbersWithUnitToken':
        if (t is None): 
            return None
        while t is not None:
            if (t.is_comma_and or t.isValue("НО", None)): 
                t = t.next0_
            else: 
                break
        t0 = t
        about_ = False
        min_max = 0
        wrapmin_max1536 = RefOutArgWrapper(min_max)
        ttt = NumbersWithUnitToken._isMinOrMax(t, wrapmin_max1536)
        min_max = wrapmin_max1536.value
        if (ttt is not None): 
            t = ttt.next0_
            if (t is None): 
                return None
        if (t.isChar('~') or t.isValue("ОКОЛО", None) or t.isValue("ПРИМЕРНО", None)): 
            t = t.next0_
            about_ = True
            if (t is None): 
                return None
        if (t0.isChar('(')): 
            mt0 = NumbersWithUnitToken._tryParse(t.next0_, add_units, False, False)
            if (mt0 is not None and mt0.end_token.next0_ is not None and mt0.end_token.next0_.isChar(')')): 
                if (second): 
                    if (mt0.from_val is not None and mt0.to_val is not None and mt0.from_val == (- mt0.to_val)): 
                        pass
                    else: 
                        return None
                mt0.begin_token = t0
                mt0.end_token = mt0.end_token.next0_
                uu = UnitToken.tryParseList(mt0.end_token.next0_, add_units)
                if (uu is not None and len(mt0.units) == 0): 
                    mt0.units = uu
                    mt0.end_token = uu[len(uu) - 1].end_token
                return mt0
        plusminus = False
        unit_before = False
        dty = NumbersWithUnitToken.DiapTyp.UNDEFINED
        uni = None
        tok = NumbersWithUnitToken.M_TERMINS.tryParse(t, TerminParseAttr.NO)
        if (tok is not None): 
            t = tok.end_token.next0_
            dty = (Utils.valToEnum(tok.termin.tag, NumbersWithUnitToken.DiapTyp))
            if (not tok.is_whitespace_after): 
                if (t is None): 
                    return None
                if (t.isCharOf(":")): 
                    pass
                elif (isinstance(t, NumberToken)): 
                    pass
                elif (t.is_comma and t.next0_ is not None and t.next0_.isValue("ЧЕМ", None)): 
                    t = t.next0_.next0_
                    if (t is not None and t.morph.class0_.is_preposition): 
                        t = t.next0_
                else: 
                    return None
            if (t is not None and t.isChar('(')): 
                uni = UnitToken.tryParseList(t.next0_, add_units)
                if (uni is not None): 
                    t = uni[len(uni) - 1].end_token.next0_
                    while t is not None:
                        if (t.isCharOf("):")): 
                            t = t.next0_
                        else: 
                            break
                    mt0 = NumbersWithUnitToken._tryParse(t, add_units, False, can_omit_number)
                    if (mt0 is not None and len(mt0.units) == 0): 
                        mt0.begin_token = t0
                        mt0.units = uni
                        return mt0
        elif (t.isChar('<')): 
            dty = NumbersWithUnitToken.DiapTyp.LS
            t = t.next0_
            if (t is not None and t.isChar('=')): 
                t = t.next0_
                dty = NumbersWithUnitToken.DiapTyp.LE
        elif (t.isChar('>')): 
            dty = NumbersWithUnitToken.DiapTyp.GT
            t = t.next0_
            if (t is not None and t.isChar('=')): 
                t = t.next0_
                dty = NumbersWithUnitToken.DiapTyp.GE
        elif (t.isChar('≤')): 
            dty = NumbersWithUnitToken.DiapTyp.LE
            t = t.next0_
        elif (t.isChar('≥')): 
            dty = NumbersWithUnitToken.DiapTyp.GE
            t = t.next0_
        if (t is not None and t.isChar(':')): 
            t = t.next0_
        if (t is not None): 
            if (t.isChar('+') or t.isValue("ПЛЮС", None)): 
                t = t.next0_
                if (t is not None and not t.is_whitespace_before): 
                    if (t.is_hiphen): 
                        t = t.next0_
                        plusminus = True
                    elif ((t.isCharOf("\\/") and t.next0_ is not None and not t.is_newline_after) and t.next0_.is_hiphen): 
                        t = t.next0_.next0_
                        plusminus = True
            elif (second and ((t.isCharOf("\\/÷…~")))): 
                t = t.next0_
            elif ((t.is_hiphen and t == t0 and not second) and NumbersWithUnitToken.M_TERMINS.tryParse(t.next0_, TerminParseAttr.NO) is not None): 
                tok = NumbersWithUnitToken.M_TERMINS.tryParse(t.next0_, TerminParseAttr.NO)
                t = tok.end_token.next0_
                dty = (Utils.valToEnum(tok.termin.tag, NumbersWithUnitToken.DiapTyp))
            elif (t.is_hiphen and t == t0 and ((t.is_whitespace_after or second))): 
                t = t.next0_
            elif (t.isChar('±')): 
                t = t.next0_
                plusminus = True
            elif ((second and t.isChar('.') and t.next0_ is not None) and t.next0_.isChar('.')): 
                t = t.next0_.next0_
                if (t is not None and t.isChar('.')): 
                    t = t.next0_
        if (t is None): 
            return None
        num = NumberExToken.tryParseFloatNumber(t, True)
        if (num is None): 
            uni = UnitToken.tryParseList(t, add_units)
            if (uni is not None): 
                unit_before = True
                t = uni[len(uni) - 1].end_token.next0_
                delim = False
                while t is not None:
                    if (t.isCharOf(":,")): 
                        delim = True
                        t = t.next0_
                    else: 
                        break
                if (not delim): 
                    if (t is None or not t.is_whitespace_before): 
                        return None
                    if (t.next0_ is not None and t.is_hiphen and t.is_whitespace_after): 
                        delim = True
                        t = t.next0_
                num = NumberExToken.tryParseFloatNumber(t, True)
        res = None
        rval = 0
        if (num is None): 
            tt = NumbersWithUnitToken.M_SPEC.tryParse(t, TerminParseAttr.NO)
            if (tt is not None): 
                rval = (tt.termin.tag)
                unam = tt.termin.tag2
                for u in UnitsHelper.UNITS: 
                    if (u.fullname_cyr == unam): 
                        uni = list()
                        uni.append(UnitToken._new1530(t, t, u))
                        break
                if (uni is None): 
                    return None
                res = NumbersWithUnitToken._new1532(t0, tt.end_token, about_)
                t = tt.end_token.next0_
            else: 
                if (not can_omit_number): 
                    return None
                if ((uni is not None and len(uni) == 1 and uni[0].begin_token == uni[0].end_token) and uni[0].length_char > 3): 
                    rval = (1)
                    res = NumbersWithUnitToken._new1532(t0, uni[len(uni) - 1].end_token, about_)
                    t = res.end_token.next0_
                else: 
                    return None
        else: 
            if ((t == t0 and t0.is_hiphen and not t.is_whitespace_before) and not t.is_whitespace_after and (num.real_value < 0)): 
                return None
            t = num.end_token.next0_
            res = NumbersWithUnitToken._new1532(t0, num.end_token, about_)
            rval = num.real_value
        if (uni is None): 
            uni = UnitToken.tryParseList(t, add_units)
            if (uni is not None): 
                if ((plusminus and second and len(uni) == 1) and uni[0].unit == UnitsHelper.UPERCENT): 
                    res.end_token = uni[len(uni) - 1].end_token
                    res.plus_minus_percent = True
                    tt1 = uni[0].end_token.next0_
                    uni = UnitToken.tryParseList(tt1, add_units)
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
                uni1 = UnitToken.tryParseList(t, add_units)
                if (((uni1 is not None and uni1[0].unit == uni[0].unit and (len(uni1) < len(uni))) and uni[len(uni1)].pow0_ == -1 and uni1[len(uni1) - 1].end_token.next0_ is not None) and uni1[len(uni1) - 1].end_token.next0_.isCharOf("/\\")): 
                    num2 = NumbersWithUnitToken._tryParse(uni1[len(uni1) - 1].end_token.next0_.next0_, add_units, False, False)
                    if (num2 is not None and num2.units is not None and num2.units[0].unit == uni[len(uni1)].unit): 
                        res.units = uni1
                        res.div_num = num2
                        res.end_token = num2.end_token
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
            wrapiii1535 = RefOutArgWrapper(iii)
            ttt = NumbersWithUnitToken._isMinOrMax(t, wrapiii1535)
            iii = wrapiii1535.value
            if (ttt is not None and iii > 0): 
                is_second_max = True
                t = ttt.next0_
        next0__ = (None if second or plusminus or ((t is not None and t.is_newline_before)) else NumbersWithUnitToken._tryParse(t, add_units, True, False))
        if (next0__ is not None and ((next0__.to_val is not None or next0__.single_val is not None)) and next0__.from_val is None): 
            if (len(next0__.units) > 0): 
                if (len(res.units) == 0): 
                    res.units = next0__.units
                elif (not UnitToken.canBeEquals(res.units, next0__.units)): 
                    next0__ = (None)
            elif (len(res.units) > 0 and not unit_before and not next0__.plus_minus_percent): 
                next0__ = (None)
            if (next0__ is not None): 
                res.end_token = next0__.end_token
            if (next0__ is not None and next0__.to_val is not None): 
                res.to_val = next0__.to_val
                res.to_include = next0__.to_include
            elif (next0__ is not None and next0__.single_val is not None): 
                if (next0__.begin_token.isCharOf("/\\")): 
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
        return res
    
    @staticmethod
    def _tryParseWHL(t : 'Token') -> 'MetaToken':
        """ Это распознавание написаний ГхШхВ
        
        Args:
            t(Token): 
        
        """
        if (not ((isinstance(t, TextToken)))): 
            return None
        if (t.isCharOf(":-")): 
            re0 = NumbersWithUnitToken._tryParseWHL(t.next0_)
            if (re0 is not None): 
                return re0
        if (t.isCharOf("(")): 
            re0 = NumbersWithUnitToken._tryParseWHL(t.next0_)
            if (re0 is not None): 
                if (re0.end_token.next0_ is not None and re0.end_token.next0_.isChar(')')): 
                    re0.begin_token = t
                    re0.end_token = re0.end_token.next0_
                    return re0
        txt = (t).term
        nams = None
        if (len(txt) == 5 and txt[1] == 'Х' and txt[3] == 'Х'): 
            nams = list()
            for i in range(3):
                ch = txt[i * 2]
                if (ch == 'Г'): 
                    nams.append("ГЛУБИНА")
                elif (ch == 'В'): 
                    nams.append("ВЫСОТА")
                elif (ch == 'Ш'): 
                    nams.append("ШИРИНА")
                elif (ch == 'Д'): 
                    nams.append("ДЛИНА")
                else: 
                    return None
            return MetaToken._new836(t, t, nams)
        t0 = t
        t1 = t
        while t is not None: 
            if (not ((isinstance(t, TextToken))) or ((t.whitespaces_before_count > 1 and t != t0))): 
                break
            term = (t).term
            nam = None
            if ((t.isValue("ДЛИНА", None) or t.isValue("ДЛИННА", None) or term == "Д") or term == "ДЛ" or term == "ДЛИН"): 
                nam = "ДЛИНА"
            elif ((t.isValue("ШИРИНА", None) or t.isValue("ШИРОТА", None) or term == "Ш") or term == "ШИР" or term == "ШИРИН"): 
                nam = "ШИРИНА"
            elif ((t.isValue("ГЛУБИНА", None) or term == "Г" or term == "ГЛ") or term == "ГЛУБ"): 
                nam = "ГЛУБИНА"
            elif (t.isValue("ВЫСОТА", None) or term == "В" or term == "ВЫС"): 
                nam = "ВЫСОТА"
            else: 
                break
            if (nams is None): 
                nams = list()
            nams.append(nam)
            t1 = t
            if (t.next0_ is not None and t.next0_.isChar('.')): 
                t = t.next0_
                t1 = t
            if (t.next0_ is None): 
                break
            if (MeasureHelper.isMultChar(t.next0_) or t.next0_.is_comma or t.next0_.isCharOf("\\/")): 
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
        t = Termin._new118("НЕ МЕНЕЕ", NumbersWithUnitToken.DiapTyp.GE)
        t.addVariant("НЕ МЕНЬШЕ", False)
        t.addVariant("НЕ КОРОЧЕ", False)
        t.addVariant("НЕ МЕДЛЕННЕЕ", False)
        t.addVariant("НЕ НИЖЕ", False)
        t.addVariant("НЕ МЕНЕ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new118("МЕНЕЕ", NumbersWithUnitToken.DiapTyp.LS)
        t.addVariant("МЕНЬШЕ", False)
        t.addVariant("МЕНЕ", False)
        t.addVariant("КОРОЧЕ", False)
        t.addVariant("МЕДЛЕННЕЕ", False)
        t.addVariant("НИЖЕ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new118("НЕ БОЛЕЕ", NumbersWithUnitToken.DiapTyp.LE)
        t.addVariant("НЕ БОЛЬШЕ", False)
        t.addVariant("НЕ БОЛЕ", False)
        t.addVariant("НЕ ДЛИННЕЕ", False)
        t.addVariant("НЕ БЫСТРЕЕ", False)
        t.addVariant("НЕ ВЫШЕ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new118("БОЛЕЕ", NumbersWithUnitToken.DiapTyp.GT)
        t.addVariant("БОЛЬШЕ", False)
        t.addVariant("ДЛИННЕЕ", False)
        t.addVariant("БЫСТРЕЕ", False)
        t.addVariant("БОЛЕ", False)
        t.addVariant("ГЛУБЖЕ", False)
        t.addVariant("ВЫШЕ", False)
        t.addVariant("СВЫШЕ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new118("ОТ", NumbersWithUnitToken.DiapTyp.FROM)
        t.addVariant("С", False)
        t.addVariant("C", False)
        t.addVariant("НАЧИНАЯ С", False)
        t.addVariant("НАЧИНАЯ ОТ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new118("ДО", NumbersWithUnitToken.DiapTyp.TO)
        t.addVariant("ПО", False)
        t.addVariant("ЗАКАНЧИВАЯ", False)
        NumbersWithUnitToken.M_TERMINS.add(t)
        t = Termin._new118("НЕ ХУЖЕ", NumbersWithUnitToken.DiapTyp.UNDEFINED)
        NumbersWithUnitToken.M_TERMINS.add(t)
        NumbersWithUnitToken.M_SPEC = TerminCollection()
        t = Termin._new120("ПОЛЛИТРА", .5, "литр")
        t.addVariant("ПОЛУЛИТРА", False)
        NumbersWithUnitToken.M_SPEC.add(t)
        t = Termin._new120("ПОЛКИЛО", .5, "килограмм")
        t.addVariant("ПОЛКИЛОГРАММА", False)
        NumbersWithUnitToken.M_SPEC.add(t)
        t = Termin._new120("ПОЛМЕТРА", .5, "метр")
        t.addVariant("ПОЛУМЕТРА", False)
        NumbersWithUnitToken.M_SPEC.add(t)
        t = Termin._new120("ПОЛТОННЫ", .5, "тонна")
        t.addVariant("ПОЛУТОННЫ", False)
        NumbersWithUnitToken.M_SPEC.add(t)
        NumbersWithUnitToken.M_SPEC.add(t)
    
    @staticmethod
    def _new1532(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'NumbersWithUnitToken':
        res = NumbersWithUnitToken(_arg1, _arg2)
        res.about = _arg3
        return res