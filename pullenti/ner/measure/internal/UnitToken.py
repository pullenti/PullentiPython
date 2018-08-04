# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.measure.internal.Unit import Unit
from pullenti.ner.measure.internal.MeasureHelper import MeasureHelper
from pullenti.ner.measure.internal.UnitsHelper import UnitsHelper
from pullenti.ner.measure.internal.UnitsFactors import UnitsFactors
from pullenti.ner.core.TerminParseAttr import TerminParseAttr


class UnitToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        self.unit = None
        self.pow0_ = 1
        self.is_doubt = False
        self.keyword = None
        self.ext_onto = None
        super().__init__(b, e0_, None)
    
    def __str__(self) -> str:
        from pullenti.morph.MorphClass import MorphClass
        res = (str(self.unit) if self.ext_onto is None else str(self.ext_onto))
        if (self.pow0_ != 1): 
            res = "{0}<{1}>".format(res, self.pow0_)
        if (self.is_doubt): 
            res += "?"
        if (self.keyword is not None): 
            res = "{0} (<-{1})".format(res, self.keyword.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False))
        return res
    
    @staticmethod
    def can_be_equals(ut1 : typing.List['UnitToken'], ut2 : typing.List['UnitToken']) -> bool:
        if (len(ut1) != len(ut2)): 
            return False
        for i in range(len(ut1)):
            if (ut1[i].unit != ut2[i].unit or ut1[i].ext_onto != ut2[i].ext_onto): 
                return False
            if (ut1[i].pow0_ != ut2[i].pow0_): 
                return False
        return True
    
    @staticmethod
    def __create_referent(u : 'Unit') -> 'UnitReferent':
        from pullenti.ner.measure.UnitReferent import UnitReferent
        ur = UnitReferent()
        ur.add_slot(UnitReferent.ATTR_NAME, u.name_cyr, False, 0)
        ur.add_slot(UnitReferent.ATTR_NAME, u.name_lat, False, 0)
        ur.add_slot(UnitReferent.ATTR_FULLNAME, u.fullname_cyr, False, 0)
        ur.add_slot(UnitReferent.ATTR_FULLNAME, u.fullname_lat, False, 0)
        ur.tag = u
        ur._m_unit = u
        return ur
    
    def create_referent_with_register(self, ad : 'AnalyzerData') -> 'UnitReferent':
        from pullenti.ner.measure.UnitReferent import UnitReferent
        ur = self.ext_onto
        if (self.unit is not None): 
            ur = UnitToken.__create_referent(self.unit)
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
                owns[i] = (ad.register_referent(owns[i]) if isinstance(ad.register_referent(owns[i]), UnitReferent) else None)
            if (i > 0): 
                owns[i - 1].add_slot(UnitReferent.ATTR_BASEUNIT, owns[i], False, 0)
                if ((owns[i - 1].tag if isinstance(owns[i - 1].tag, Unit) else None).base_multiplier != 0): 
                    owns[i - 1].add_slot(UnitReferent.ATTR_BASEFACTOR, MeasureHelper.double_to_string((owns[i - 1].tag if isinstance(owns[i - 1].tag, Unit) else None).base_multiplier), False, 0)
        return owns[0]
    
    @staticmethod
    def try_parse_list(t : 'Token', add_units : 'TerminCollection') -> typing.List['UnitToken']:
        ut = UnitToken.try_parse(t, add_units, None)
        if (ut is None): 
            return None
        res = list()
        res.append(ut)
        tt = ut.end_token.next0_
        while tt is not None: 
            ut = UnitToken.try_parse(tt, add_units, res[len(res) - 1])
            if (ut is None): 
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
    def try_parse(t : 'Token', add_units : 'TerminCollection', prev : 'UnitToken') -> 'UnitToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.measure.UnitReferent import UnitReferent
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
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None): 
            return None
        if (tt.term == "КВ" or tt.term == "КВАДР" or tt.is_value("КВАДРАТНЫЙ", None)): 
            pow0__ = 2
            tt = (tt.next0_ if isinstance(tt.next0_, TextToken) else None)
            if (tt is not None and tt.is_char('.')): 
                tt = (tt.next0_ if isinstance(tt.next0_, TextToken) else None)
            if (tt is None): 
                return None
        elif (tt.term == "КУБ" or tt.term == "КУБИЧ" or tt.is_value("КУБИЧЕСКИЙ", None)): 
            pow0__ = 3
            tt = (tt.next0_ if isinstance(tt.next0_, TextToken) else None)
            if (tt is not None and tt.is_char('.')): 
                tt = (tt.next0_ if isinstance(tt.next0_, TextToken) else None)
            if (tt is None): 
                return None
        elif (tt.term == "µ"): 
            res = UnitToken.try_parse(tt.next0_, add_units, prev)
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
            uts = list()
            for tok in toks: 
                res = UnitToken._new1517(t0, tok.end_token, (tok.termin.tag if isinstance(tok.termin.tag, Unit) else None))
                res.pow0_ = pow0__
                if (is_neg): 
                    res.pow0_ = (- pow0__)
                if (res.unit.base_multiplier == 1000000 and isinstance(t0, TextToken) and (t0 if isinstance(t0, TextToken) else None).get_source_text()[0].islower()): 
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
        elif ((t.is_char('<') and t.next0_ is not None and t.next0_.next0_ is not None) and t.next0_.next0_.is_char('>') and ((t.next0_.is_value("О", None) or t.next0_.is_value("O", None) or ((isinstance(t.next0_, NumberToken) and (t.next0_ if isinstance(t.next0_, NumberToken) else None).value == 0))))): 
            t1 = t.next0_.next0_
        if (t1 is not None): 
            res = UnitToken._new1517(t0, t1, UnitsHelper.UGRADUS)
            res.__check_doubt()
            t = t1.next0_
            if (t is not None and t.is_comma): 
                t = t.next0_
            if (t is not None and t.is_value("ПО", None)): 
                t = t.next0_
            if (isinstance(t, TextToken)): 
                vv = (t if isinstance(t, TextToken) else None).term
                if (vv == "C" or vv == "С" or vv.startswith("ЦЕЛЬС")): 
                    res.unit = UnitsHelper.UGRADUSC
                    res.is_doubt = False
                    res.end_token = t
                if (vv == "F" or vv.startswith("ФАР")): 
                    res.unit = UnitsHelper.UGRADUSF
                    res.is_doubt = False
                    res.end_token = t
            return res
        if (t.is_char('%')): 
            return UnitToken._new1517(t, t, UnitsHelper.UPERCENT)
        if (add_units is not None): 
            tok = add_units.try_parse(t, TerminParseAttr.NO)
            if (tok is not None): 
                res = UnitToken._new1598(t0, tok.end_token, (tok.termin.tag if isinstance(tok.termin.tag, UnitReferent) else None))
                if (tok.end_token.next0_ is not None and tok.end_token.next0_.is_char('.')): 
                    tok.end_token = tok.end_token.next0_
                res.pow0_ = pow0__
                if (is_neg): 
                    res.pow0_ = (- pow0__)
                res.__correct()
                return res
        return None
    
    def __correct(self) -> None:
        from pullenti.ner.NumberToken import NumberToken
        t = self.end_token.next0_
        if (t is None): 
            return
        num = 0
        neg = self.pow0_ < 0
        if (t.is_char('³')): 
            num = 3
        elif (t.is_char('²')): 
            num = 2
        elif (not t.is_whitespace_before and isinstance(t, NumberToken) and (((t if isinstance(t, NumberToken) else None).value == 3 or (t if isinstance(t, NumberToken) else None).value == 2))): 
            num = (t if isinstance(t, NumberToken) else None).value
        elif ((t.is_char('<') and isinstance(t.next0_, NumberToken) and t.next0_.next0_ is not None) and t.next0_.next0_.is_char('>')): 
            num = (t.next0_ if isinstance(t.next0_, NumberToken) else None).value
            t = t.next0_.next0_
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
    
    def __check_doubt(self) -> None:
        from pullenti.ner.measure.MeasureReferent import MeasureReferent
        from pullenti.ner.measure.UnitReferent import UnitReferent
        from pullenti.ner.TextToken import TextToken
        self.is_doubt = False
        if (self.pow0_ != 1): 
            return
        if (self.begin_token.length_char < 3): 
            self.is_doubt = True
        cou = 0
        t = self.begin_token.previous
        first_pass2969 = True
        while True:
            if first_pass2969: first_pass2969 = False
            else: t = t.previous; cou += 1
            if (not (t is not None and (cou < 30))): break
            mr = (t.get_referent() if isinstance(t.get_referent(), MeasureReferent) else None)
            if (mr is not None): 
                for s in mr.slots: 
                    if (isinstance(s.value, UnitReferent)): 
                        ur = (s.value if isinstance(s.value, UnitReferent) else None)
                        u = self.unit
                        while u is not None: 
                            if (ur.find_slot(UnitReferent.ATTR_NAME, u.name_cyr, True) is not None): 
                                self.is_doubt = False
                            u = u.base_unit
            if (not ((isinstance(t, TextToken))) or (t.length_char < 3)): 
                continue
            u = self.unit
            while u is not None: 
                for k in u.keywords: 
                    if (t.is_value(k, None)): 
                        self.keyword = t
                        self.is_doubt = False
                        return
                u = u.base_unit

    
    @staticmethod
    def _new1517(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Unit') -> 'UnitToken':
        res = UnitToken(_arg1, _arg2)
        res.unit = _arg3
        return res
    
    @staticmethod
    def _new1598(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'UnitReferent') -> 'UnitToken':
        res = UnitToken(_arg1, _arg2)
        res.ext_onto = _arg3
        return res