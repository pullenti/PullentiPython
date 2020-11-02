# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Token import Token
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.measure.internal.UnitsFactors import UnitsFactors
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.measure.MeasureReferent import MeasureReferent
from pullenti.ner.Referent import Referent
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.measure.MeasureKind import MeasureKind
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.measure.internal.UnitsHelper import UnitsHelper
from pullenti.ner.measure.UnitReferent import UnitReferent
from pullenti.ner.measure.internal.MeasureHelper import MeasureHelper
from pullenti.ner.measure.internal.Unit import Unit
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class UnitToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.unit = None;
        self.pow0_ = 1
        self.is_doubt = False
        self.keyword = None;
        self.ext_onto = None;
        self.unknown_name = None;
    
    def __str__(self) -> str:
        res = Utils.ifNotNull(self.unknown_name, ((str(self.unit) if self.ext_onto is None else str(self.ext_onto))))
        if (self.pow0_ != 1): 
            res = "{0}<{1}>".format(res, self.pow0_)
        if (self.is_doubt): 
            res += "?"
        if (self.keyword is not None): 
            res = "{0} (<-{1})".format(res, self.keyword.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
        return res
    
    @staticmethod
    def can_be_equals(ut1 : typing.List['UnitToken'], ut2 : typing.List['UnitToken']) -> bool:
        if (len(ut1) != len(ut2)): 
            return False
        i = 0
        while i < len(ut1): 
            if (ut1[i].unit != ut2[i].unit or ut1[i].ext_onto != ut2[i].ext_onto): 
                return False
            if (ut1[i].pow0_ != ut2[i].pow0_): 
                return False
            i += 1
        return True
    
    @staticmethod
    def calc_kind(units : typing.List['UnitToken']) -> 'MeasureKind':
        if (units is None or len(units) == 0): 
            return MeasureKind.UNDEFINED
        u0 = units[0]
        if (u0.unit is None): 
            return MeasureKind.UNDEFINED
        if (len(units) == 1): 
            if (u0.pow0_ == 1): 
                return u0.unit.kind
            if (u0.pow0_ == 2): 
                if (u0.unit.kind == MeasureKind.LENGTH): 
                    return MeasureKind.AREA
            if (u0.pow0_ == 3): 
                if (u0.unit.kind == MeasureKind.LENGTH): 
                    return MeasureKind.VOLUME
            return MeasureKind.UNDEFINED
        if (len(units) == 2): 
            if (units[1].unit is None): 
                return MeasureKind.UNDEFINED
            if ((u0.unit.kind == MeasureKind.LENGTH and u0.pow0_ == 1 and units[1].unit.kind == MeasureKind.TIME) and units[1].pow0_ == -1): 
                return MeasureKind.SPEED
        return MeasureKind.UNDEFINED
    
    @staticmethod
    def __create_referent(u : 'Unit') -> 'UnitReferent':
        ur = UnitReferent()
        ur.add_slot(UnitReferent.ATTR_NAME, u.name_cyr, False, 0)
        ur.add_slot(UnitReferent.ATTR_NAME, u.name_lat, False, 0)
        ur.add_slot(UnitReferent.ATTR_FULLNAME, u.fullname_cyr, False, 0)
        ur.add_slot(UnitReferent.ATTR_FULLNAME, u.fullname_lat, False, 0)
        ur.tag = u
        ur._m_unit = u
        return ur
    
    def create_referent_with_register(self, ad : 'AnalyzerData') -> 'UnitReferent':
        ur = self.ext_onto
        if (self.unit is not None): 
            ur = UnitToken.__create_referent(self.unit)
        elif (self.unknown_name is not None): 
            ur = UnitReferent()
            ur.add_slot(UnitReferent.ATTR_NAME, self.unknown_name, False, 0)
            ur.is_unknown = True
        if (self.pow0_ != 1): 
            ur.add_slot(UnitReferent.ATTR_POW, str(self.pow0_), False, 0)
        owns = list()
        owns.append(ur)
        if (self.unit is not None): 
            uu = self.unit.base_unit
            while uu is not None: 
                ur0 = UnitToken.__create_referent(uu)
                owns.append(ur0)
                uu = uu.base_unit
        for i in range(len(owns) - 1, -1, -1):
            if (ad is not None): 
                owns[i] = (Utils.asObjectOrNull(ad.register_referent(owns[i]), UnitReferent))
            if (i > 0): 
                owns[i - 1].add_slot(UnitReferent.ATTR_BASEUNIT, owns[i], False, 0)
                if (owns[i - 1].tag.base_multiplier != 0): 
                    owns[i - 1].add_slot(UnitReferent.ATTR_BASEFACTOR, NumberHelper.double_to_string(owns[i - 1].tag.base_multiplier), False, 0)
        return owns[0]
    
    @staticmethod
    def try_parse_list(t : 'Token', add_units : 'TerminCollection', parse_unknown_units : bool=False) -> typing.List['UnitToken']:
        ut = UnitToken.try_parse(t, add_units, None, parse_unknown_units)
        if (ut is None): 
            return None
        res = list()
        res.append(ut)
        tt = ut.end_token.next0_
        while tt is not None: 
            ut = UnitToken.try_parse(tt, add_units, res[len(res) - 1], True)
            if (ut is None): 
                break
            if (ut.unit is not None and ut.unit.kind != MeasureKind.UNDEFINED): 
                if (res[len(res) - 1].unit is not None and res[len(res) - 1].unit.kind == ut.unit.kind): 
                    break
            res.append(ut)
            tt = ut.end_token
            if (len(res) > 2): 
                break
            tt = tt.next0_
        i = 0
        while i < len(res): 
            if (res[i].unit is not None and res[i].unit.base_unit is not None and res[i].unit.mult_unit is not None): 
                ut2 = UnitToken(res[i].begin_token, res[i].end_token)
                ut2.unit = res[i].unit.mult_unit
                res.insert(i + 1, ut2)
                res[i].unit = res[i].unit.base_unit
            i += 1
        if (len(res) > 1): 
            for r in res: 
                r.is_doubt = False
        return res
    
    @staticmethod
    def try_parse(t : 'Token', add_units : 'TerminCollection', prev : 'UnitToken', parse_unknown_units : bool=False) -> 'UnitToken':
        if (t is None): 
            return None
        t0 = t
        pow0__ = 1
        is_neg = False
        if ((t.is_char_of("\\/") or t.is_value("НА", None) or t.is_value("OF", None)) or t.is_value("PER", None)): 
            is_neg = True
            t = t.next0_
        elif (t.is_value("В", None) and prev is not None): 
            is_neg = True
            t = t.next0_
        elif (MeasureHelper.is_mult_char(t)): 
            t = t.next0_
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        if (tt.term == "КВ" or tt.term == "КВАДР" or tt.is_value("КВАДРАТНЫЙ", None)): 
            pow0__ = 2
            tt = (Utils.asObjectOrNull(tt.next0_, TextToken))
            if (tt is not None and tt.is_char('.')): 
                tt = (Utils.asObjectOrNull(tt.next0_, TextToken))
            if (tt is None): 
                return None
        elif (tt.term == "КУБ" or tt.term == "КУБИЧ" or tt.is_value("КУБИЧЕСКИЙ", None)): 
            pow0__ = 3
            tt = (Utils.asObjectOrNull(tt.next0_, TextToken))
            if (tt is not None and tt.is_char('.')): 
                tt = (Utils.asObjectOrNull(tt.next0_, TextToken))
            if (tt is None): 
                return None
        elif (tt.term == "µ"): 
            res = UnitToken.try_parse(tt.next0_, add_units, prev, False)
            if (res is not None): 
                for u in UnitsHelper.UNITS: 
                    if (u.factor == UnitsFactors.MICRO and Utils.compareStrings("мк" + u.name_cyr, res.unit.name_cyr, True) == 0): 
                        res.unit = u
                        res.begin_token = tt
                        res.pow0_ = pow0__
                        if (is_neg): 
                            res.pow0_ = (- pow0__)
                        return res
        toks = UnitsHelper.TERMINS.try_parse_all(tt, TerminParseAttr.NO)
        if (toks is not None): 
            if ((prev is not None and tt == t0 and len(toks) == 1) and t.is_whitespace_before): 
                return None
            if (toks[0].begin_token == toks[0].end_token and tt.morph.class0_.is_preposition and (tt.whitespaces_after_count < 3)): 
                if (NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.PARSEPREPOSITION, 0, None) is not None): 
                    return None
                if (isinstance(tt.next0_, NumberToken)): 
                    if (tt.next0_.typ != NumberSpellingType.DIGIT): 
                        return None
                nex = UnitToken.try_parse(tt.next0_, add_units, None, False)
                if (nex is not None): 
                    return None
            if (toks[0].begin_token == toks[0].end_token and ((toks[0].begin_token.is_value("М", None) or toks[0].begin_token.is_value("M", None))) and toks[0].begin_token.chars.is_all_lower): 
                if (prev is not None and prev.unit is not None and prev.unit.kind == MeasureKind.LENGTH): 
                    res = UnitToken._new1622(t0, toks[0].end_token, UnitsHelper.UMINUTE)
                    res.pow0_ = pow0__
                    if (is_neg): 
                        res.pow0_ = (- pow0__)
                    return res
            uts = list()
            for tok in toks: 
                res = UnitToken._new1622(t0, tok.end_token, Utils.asObjectOrNull(tok.termin.tag, Unit))
                res.pow0_ = pow0__
                if (is_neg): 
                    res.pow0_ = (- pow0__)
                if (res.unit.base_multiplier == 1000000 and (isinstance(t0, TextToken)) and str.islower(t0.get_source_text()[0])): 
                    for u in UnitsHelper.UNITS: 
                        if (u.factor == UnitsFactors.MILLI and Utils.compareStrings(u.name_cyr, res.unit.name_cyr, True) == 0): 
                            res.unit = u
                            break
                res.__correct()
                res.__check_doubt()
                uts.append(res)
            max0_ = 0
            best = None
            for ut in uts: 
                if (ut.keyword is not None): 
                    if (ut.keyword.begin_char >= max0_): 
                        max0_ = ut.keyword.begin_char
                        best = ut
            if (best is not None): 
                return best
            for ut in uts: 
                if (not ut.is_doubt): 
                    return ut
            return uts[0]
        t1 = None
        if (t.is_char_of("º°")): 
            t1 = t
        elif ((t.is_char('<') and t.next0_ is not None and t.next0_.next0_ is not None) and t.next0_.next0_.is_char('>') and ((t.next0_.is_value("О", None) or t.next0_.is_value("O", None) or (((isinstance(t.next0_, NumberToken)) and t.next0_.value == "0"))))): 
            t1 = t.next0_.next0_
        if (t1 is not None): 
            res = UnitToken._new1622(t0, t1, UnitsHelper.UGRADUS)
            res.__check_doubt()
            t = t1.next0_
            if (t is not None and t.is_comma): 
                t = t.next0_
            if (t is not None and t.is_value("ПО", None)): 
                t = t.next0_
            if (isinstance(t, TextToken)): 
                vv = t.term
                if (vv == "C" or vv == "С" or vv.startswith("ЦЕЛЬС")): 
                    res.unit = UnitsHelper.UGRADUSC
                    res.is_doubt = False
                    res.end_token = t
                if (vv == "F" or vv.startswith("ФАР")): 
                    res.unit = UnitsHelper.UGRADUSF
                    res.is_doubt = False
                    res.end_token = t
            return res
        if ((isinstance(t, TextToken)) and ((t.is_value("ОС", None) or t.is_value("OC", None)))): 
            str0_ = t.get_source_text()
            if (str0_ == "оС" or str0_ == "oC"): 
                res = UnitToken._new1734(t, t, UnitsHelper.UGRADUSC, False)
                return res
        if (t.is_char('%')): 
            tt1 = t.next0_
            if (tt1 is not None and tt1.is_char('(')): 
                tt1 = tt1.next0_
            if ((isinstance(tt1, TextToken)) and tt1.term.startswith("ОБ")): 
                re = UnitToken._new1622(t, tt1, UnitsHelper.UALCO)
                if (re.end_token.next0_ is not None and re.end_token.next0_.is_char('.')): 
                    re.end_token = re.end_token.next0_
                if (re.end_token.next0_ is not None and re.end_token.next0_.is_char(')') and t.next0_.is_char('(')): 
                    re.end_token = re.end_token.next0_
                return re
            return UnitToken._new1622(t, t, UnitsHelper.UPERCENT)
        if (add_units is not None): 
            tok = add_units.try_parse(t, TerminParseAttr.NO)
            if (tok is not None): 
                res = UnitToken._new1737(t0, tok.end_token, Utils.asObjectOrNull(tok.termin.tag, UnitReferent))
                if (tok.end_token.next0_ is not None and tok.end_token.next0_.is_char('.')): 
                    tok.end_token = tok.end_token.next0_
                res.pow0_ = pow0__
                if (is_neg): 
                    res.pow0_ = (- pow0__)
                res.__correct()
                return res
        if (not parse_unknown_units): 
            return None
        if ((t.whitespaces_before_count > 2 or not t.chars.is_letter or t.length_char > 5) or not (isinstance(t, TextToken))): 
            return None
        if (MiscHelper.can_be_start_of_sentence(t)): 
            return None
        t1 = t
        if (t.next0_ is not None and t.next0_.is_char('.')): 
            t1 = t
        ok = False
        if (t1.next0_ is None or t1.whitespaces_after_count > 2): 
            ok = True
        elif (t1.next0_.is_comma or t1.next0_.is_char_of("\\/") or t1.next0_.is_table_control_char): 
            ok = True
        elif (MeasureHelper.is_mult_char(t1.next0_)): 
            ok = True
        if (not ok): 
            return None
        mc = t.get_morph_class_in_dictionary()
        if (mc.is_undefined): 
            pass
        elif (t.length_char > 7): 
            return None
        res1 = UnitToken._new1738(t0, t1, pow0__, True)
        res1.unknown_name = t.get_source_text()
        res1.__correct()
        return res1
    
    def __correct(self) -> None:
        t = self.end_token.next0_
        if (t is None): 
            return
        num = 0
        neg = self.pow0_ < 0
        if (t.is_char('³')): 
            num = 3
        elif (t.is_char('²')): 
            num = 2
        elif (not t.is_whitespace_before and (isinstance(t, NumberToken)) and ((t.value == "3" or t.value == "2"))): 
            num = t.int_value
        elif ((t.is_char('<') and (isinstance(t.next0_, NumberToken)) and t.next0_.int_value is not None) and t.next0_.next0_ is not None and t.next0_.next0_.is_char('>')): 
            num = t.next0_.int_value
            t = t.next0_.next0_
        elif (((t.is_char('<') and t.next0_ is not None and t.next0_.is_hiphen) and (isinstance(t.next0_.next0_, NumberToken)) and t.next0_.next0_.int_value is not None) and t.next0_.next0_.next0_ is not None and t.next0_.next0_.next0_.is_char('>')): 
            num = t.next0_.next0_.int_value
            neg = True
            t = t.next0_.next0_.next0_
        else: 
            if (t.is_value("B", None) and t.next0_ is not None): 
                t = t.next0_
            if ((t.is_value("КВ", None) or t.is_value("КВАДР", None) or t.is_value("КВАДРАТНЫЙ", None)) or t.is_value("КВАДРАТ", None)): 
                num = 2
                if (t.next0_ is not None and t.next0_.is_char('.')): 
                    t = t.next0_
            elif (t.is_value("КУБ", None) or t.is_value("КУБИЧ", None) or t.is_value("КУБИЧЕСКИЙ", None)): 
                num = 3
                if (t.next0_ is not None and t.next0_.is_char('.')): 
                    t = t.next0_
        if (num != 0): 
            self.pow0_ = num
            if (neg): 
                self.pow0_ = (- num)
            self.end_token = t
        t = self.end_token.next0_
        if ((t is not None and t.is_value("ПО", None) and t.next0_ is not None) and t.next0_.is_value("U", None)): 
            self.end_token = t.next0_
    
    def __check_doubt(self) -> None:
        self.is_doubt = False
        if (self.pow0_ != 1): 
            return
        if (self.begin_token.length_char < 3): 
            self.is_doubt = True
            if ((self.begin_token.chars.is_capital_upper or self.begin_token.chars.is_all_upper or self.begin_token.chars.is_last_lower) or self.begin_token.chars.is_all_lower): 
                pass
            elif (len(self.unit.psevdo) > 0): 
                pass
            else: 
                self.is_doubt = False
        cou = 0
        t = self.begin_token.previous
        first_pass3800 = True
        while True:
            if first_pass3800: first_pass3800 = False
            else: t = t.previous; cou += 1
            if (not (t is not None and (cou < 30))): break
            mr = Utils.asObjectOrNull(t.get_referent(), MeasureReferent)
            if (mr is not None): 
                for s in mr.slots: 
                    if (isinstance(s.value, UnitReferent)): 
                        ur = Utils.asObjectOrNull(s.value, UnitReferent)
                        u = self.unit
                        while u is not None: 
                            if (ur.find_slot(UnitReferent.ATTR_NAME, u.name_cyr, True) is not None): 
                                self.is_doubt = False
                            elif (len(self.unit.psevdo) > 0): 
                                for uu in self.unit.psevdo: 
                                    if (ur.find_slot(UnitReferent.ATTR_NAME, uu.name_cyr, True) is not None): 
                                        self.unit = uu
                                        self.is_doubt = False
                                        return
                            u = u.base_unit
            if (not (isinstance(t, TextToken)) or (t.length_char < 3)): 
                continue
            u = self.unit
            while u is not None: 
                for k in u.keywords: 
                    if (t.is_value(k, None)): 
                        self.keyword = t
                        self.is_doubt = False
                        return
                for uu in u.psevdo: 
                    for k in uu.keywords: 
                        if (t.is_value(k, None)): 
                            self.unit = uu
                            self.keyword = t
                            self.is_doubt = False
                            return
                u = u.base_unit
    
    @staticmethod
    def out_units(units : typing.List['UnitToken']) -> str:
        if (units is None or len(units) == 0): 
            return None
        res = io.StringIO()
        print(units[0].unit.name_cyr, end="", file=res)
        if (units[0].pow0_ != 1): 
            print("<{0}>".format(units[0].pow0_), end="", file=res, flush=True)
        i = 1
        while i < len(units): 
            mnem = units[i].unit.name_cyr
            pow0__ = units[i].pow0_
            if (pow0__ < 0): 
                print("/{0}".format(mnem), end="", file=res, flush=True)
                if (pow0__ != -1): 
                    print("<{0}>".format(- pow0__), end="", file=res, flush=True)
            else: 
                print("*{0}".format(mnem), end="", file=res, flush=True)
                if (pow0__ > 1): 
                    print("<{0}>".format(pow0__), end="", file=res, flush=True)
            i += 1
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def _new1622(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Unit') -> 'UnitToken':
        res = UnitToken(_arg1, _arg2)
        res.unit = _arg3
        return res
    
    @staticmethod
    def _new1734(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Unit', _arg4 : bool) -> 'UnitToken':
        res = UnitToken(_arg1, _arg2)
        res.unit = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new1737(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'UnitReferent') -> 'UnitToken':
        res = UnitToken(_arg1, _arg2)
        res.ext_onto = _arg3
        return res
    
    @staticmethod
    def _new1738(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : bool) -> 'UnitToken':
        res = UnitToken(_arg1, _arg2)
        res.pow0_ = _arg3
        res.is_doubt = _arg4
        return res