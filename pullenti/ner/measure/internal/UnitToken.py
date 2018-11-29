# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.measure.MeasureKind import MeasureKind
from pullenti.ner.measure.internal.Unit import Unit
from pullenti.ner.measure.internal.MeasureHelper import MeasureHelper
from pullenti.ner.measure.internal.UnitsHelper import UnitsHelper
from pullenti.ner.measure.internal.UnitsFactors import UnitsFactors
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType


class UnitToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.unit = None;
        self.pow0_ = 1
        self.is_doubt = False
        self.keyword = None;
        self.ext_onto = None;
    
    def __str__(self) -> str:
        from pullenti.morph.MorphClass import MorphClass
        res = (str(self.unit) if self.ext_onto is None else str(self.ext_onto))
        if (self.pow0_ != 1): 
            res = "{0}<{1}>".format(res, self.pow0_)
        if (self.is_doubt): 
            res += "?"
        if (self.keyword is not None): 
            res = "{0} (<-{1})".format(res, self.keyword.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False))
        return res
    
    @staticmethod
    def canBeEquals(ut1 : typing.List['UnitToken'], ut2 : typing.List['UnitToken']) -> bool:
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
    def calcKind(units : typing.List['UnitToken']) -> 'MeasureKind':
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
    def __createReferent(u : 'Unit') -> 'UnitReferent':
        from pullenti.ner.measure.UnitReferent import UnitReferent
        ur = UnitReferent()
        ur.addSlot(UnitReferent.ATTR_NAME, u.name_cyr, False, 0)
        ur.addSlot(UnitReferent.ATTR_NAME, u.name_lat, False, 0)
        ur.addSlot(UnitReferent.ATTR_FULLNAME, u.fullname_cyr, False, 0)
        ur.addSlot(UnitReferent.ATTR_FULLNAME, u.fullname_lat, False, 0)
        ur.tag = u
        ur._m_unit = u
        return ur
    
    def createReferentWithRegister(self, ad : 'AnalyzerData') -> 'UnitReferent':
        from pullenti.ner.measure.UnitReferent import UnitReferent
        ur = self.ext_onto
        if (self.unit is not None): 
            ur = UnitToken.__createReferent(self.unit)
        if (self.pow0_ != 1): 
            ur.addSlot(UnitReferent.ATTR_POW, str(self.pow0_), False, 0)
        owns = list()
        owns.append(ur)
        if (self.unit is not None): 
            uu = self.unit.base_unit
            while uu is not None: 
                ur0 = UnitToken.__createReferent(uu)
                owns.append(ur0)
                uu = uu.base_unit
        for i in range(len(owns) - 1, -1, -1):
            if (ad is not None): 
                owns[i] = (Utils.asObjectOrNull(ad.registerReferent(owns[i]), UnitReferent))
            if (i > 0): 
                owns[i - 1].addSlot(UnitReferent.ATTR_BASEUNIT, owns[i], False, 0)
                if ((Utils.asObjectOrNull(owns[i - 1].tag, Unit)).base_multiplier != 0): 
                    owns[i - 1].addSlot(UnitReferent.ATTR_BASEFACTOR, MeasureHelper.doubleToString((Utils.asObjectOrNull(owns[i - 1].tag, Unit)).base_multiplier), False, 0)
        return owns[0]
    
    @staticmethod
    def tryParseList(t : 'Token', add_units : 'TerminCollection') -> typing.List['UnitToken']:
        ut = UnitToken.tryParse(t, add_units, None)
        if (ut is None): 
            return None
        res = list()
        res.append(ut)
        tt = ut.end_token.next0_
        while tt is not None: 
            ut = UnitToken.tryParse(tt, add_units, res[len(res) - 1])
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
    def tryParse(t : 'Token', add_units : 'TerminCollection', prev : 'UnitToken') -> 'UnitToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.measure.UnitReferent import UnitReferent
        if (t is None): 
            return None
        t0 = t
        pow0__ = 1
        is_neg = False
        if ((t.isCharOf("\\/") or t.isValue("НА", None) or t.isValue("OF", None)) or t.isValue("PER", None)): 
            is_neg = True
            t = t.next0_
        elif (t.isValue("В", None) and prev is not None): 
            is_neg = True
            t = t.next0_
        elif (MeasureHelper.isMultChar(t)): 
            t = t.next0_
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        if (tt.term == "КВ" or tt.term == "КВАДР" or tt.isValue("КВАДРАТНЫЙ", None)): 
            pow0__ = 2
            tt = (Utils.asObjectOrNull(tt.next0_, TextToken))
            if (tt is not None and tt.isChar('.')): 
                tt = (Utils.asObjectOrNull(tt.next0_, TextToken))
            if (tt is None): 
                return None
        elif (tt.term == "КУБ" or tt.term == "КУБИЧ" or tt.isValue("КУБИЧЕСКИЙ", None)): 
            pow0__ = 3
            tt = (Utils.asObjectOrNull(tt.next0_, TextToken))
            if (tt is not None and tt.isChar('.')): 
                tt = (Utils.asObjectOrNull(tt.next0_, TextToken))
            if (tt is None): 
                return None
        elif (tt.term == "µ"): 
            res = UnitToken.tryParse(tt.next0_, add_units, prev)
            if (res is not None): 
                for u in UnitsHelper.UNITS: 
                    if (u.factor == UnitsFactors.MICRO and Utils.compareStrings("мк" + u.name_cyr, res.unit.name_cyr, True) == 0): 
                        res.unit = u
                        res.begin_token = tt
                        res.pow0_ = pow0__
                        if (is_neg): 
                            res.pow0_ = (- pow0__)
                        return res
        toks = UnitsHelper.TERMINS.tryParseAll(tt, TerminParseAttr.NO)
        if (toks is not None): 
            if ((prev is not None and tt == t0 and len(toks) == 1) and t.is_whitespace_before): 
                return None
            if (toks[0].begin_token == toks[0].end_token and tt.morph.class0_.is_preposition and (tt.whitespaces_after_count < 3)): 
                if (NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.PARSEPREPOSITION, 0) is not None): 
                    return None
                if (isinstance(tt.next0_, NumberToken)): 
                    if ((Utils.asObjectOrNull(tt.next0_, NumberToken)).typ != NumberSpellingType.DIGIT): 
                        return None
            uts = list()
            for tok in toks: 
                res = UnitToken._new1530(t0, tok.end_token, Utils.asObjectOrNull(tok.termin.tag, Unit))
                res.pow0_ = pow0__
                if (is_neg): 
                    res.pow0_ = (- pow0__)
                if (res.unit.base_multiplier == 1000000 and (isinstance(t0, TextToken)) and str.islower((Utils.asObjectOrNull(t0, TextToken)).getSourceText()[0])): 
                    for u in UnitsHelper.UNITS: 
                        if (u.factor == UnitsFactors.MILLI and Utils.compareStrings(u.name_cyr, res.unit.name_cyr, True) == 0): 
                            res.unit = u
                            break
                res.__correct()
                res.__checkDoubt()
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
        if (t.isCharOf("º°")): 
            t1 = t
        elif ((t.isChar('<') and t.next0_ is not None and t.next0_.next0_ is not None) and t.next0_.next0_.isChar('>') and ((t.next0_.isValue("О", None) or t.next0_.isValue("O", None) or (((isinstance(t.next0_, NumberToken)) and (Utils.asObjectOrNull(t.next0_, NumberToken)).value == (0)))))): 
            t1 = t.next0_.next0_
        if (t1 is not None): 
            res = UnitToken._new1530(t0, t1, UnitsHelper.UGRADUS)
            res.__checkDoubt()
            t = t1.next0_
            if (t is not None and t.is_comma): 
                t = t.next0_
            if (t is not None and t.isValue("ПО", None)): 
                t = t.next0_
            if (isinstance(t, TextToken)): 
                vv = (Utils.asObjectOrNull(t, TextToken)).term
                if (vv == "C" or vv == "С" or vv.startswith("ЦЕЛЬС")): 
                    res.unit = UnitsHelper.UGRADUSC
                    res.is_doubt = False
                    res.end_token = t
                if (vv == "F" or vv.startswith("ФАР")): 
                    res.unit = UnitsHelper.UGRADUSF
                    res.is_doubt = False
                    res.end_token = t
            return res
        if (t.isChar('%')): 
            tt1 = t.next0_
            if (tt1 is not None and tt1.isChar('(')): 
                tt1 = tt1.next0_
            if ((isinstance(tt1, TextToken)) and (Utils.asObjectOrNull(tt1, TextToken)).term.startswith("ОБ")): 
                re = UnitToken._new1530(t, tt1, UnitsHelper.UALCO)
                if (re.end_token.next0_ is not None and re.end_token.next0_.isChar('.')): 
                    re.end_token = re.end_token.next0_
                if (re.end_token.next0_ is not None and re.end_token.next0_.isChar(')') and t.next0_.isChar('(')): 
                    re.end_token = re.end_token.next0_
                return re
            return UnitToken._new1530(t, t, UnitsHelper.UPERCENT)
        if (add_units is not None): 
            tok = add_units.tryParse(t, TerminParseAttr.NO)
            if (tok is not None): 
                res = UnitToken._new1634(t0, tok.end_token, Utils.asObjectOrNull(tok.termin.tag, UnitReferent))
                if (tok.end_token.next0_ is not None and tok.end_token.next0_.isChar('.')): 
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
        if (t.isChar('³')): 
            num = 3
        elif (t.isChar('²')): 
            num = 2
        elif (not t.is_whitespace_before and (isinstance(t, NumberToken)) and (((Utils.asObjectOrNull(t, NumberToken)).value == (3) or (Utils.asObjectOrNull(t, NumberToken)).value == (2)))): 
            num = ((Utils.asObjectOrNull(t, NumberToken)).value)
        elif ((t.isChar('<') and (isinstance(t.next0_, NumberToken)) and t.next0_.next0_ is not None) and t.next0_.next0_.isChar('>')): 
            num = ((Utils.asObjectOrNull(t.next0_, NumberToken)).value)
            t = t.next0_.next0_
        else: 
            if (t.isValue("B", None) and t.next0_ is not None): 
                t = t.next0_
            if ((t.isValue("КВ", None) or t.isValue("КВАДР", None) or t.isValue("КВАДРАТНЫЙ", None)) or t.isValue("КВАДРАТ", None)): 
                num = 2
                if (t.next0_ is not None and t.next0_.isChar('.')): 
                    t = t.next0_
            elif (t.isValue("КУБ", None) or t.isValue("КУБИЧ", None) or t.isValue("КУБИЧЕСКИЙ", None)): 
                num = 3
                if (t.next0_ is not None and t.next0_.isChar('.')): 
                    t = t.next0_
        if (num != 0): 
            self.pow0_ = num
            if (neg): 
                self.pow0_ = (- num)
            self.end_token = t
    
    def __checkDoubt(self) -> None:
        from pullenti.ner.measure.MeasureReferent import MeasureReferent
        from pullenti.ner.measure.UnitReferent import UnitReferent
        from pullenti.ner.TextToken import TextToken
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
        first_pass3051 = True
        while True:
            if first_pass3051: first_pass3051 = False
            else: t = t.previous; cou += 1
            if (not (t is not None and (cou < 30))): break
            mr = Utils.asObjectOrNull(t.getReferent(), MeasureReferent)
            if (mr is not None): 
                for s in mr.slots: 
                    if (isinstance(s.value, UnitReferent)): 
                        ur = Utils.asObjectOrNull(s.value, UnitReferent)
                        u = self.unit
                        while u is not None: 
                            if (ur.findSlot(UnitReferent.ATTR_NAME, u.name_cyr, True) is not None): 
                                self.is_doubt = False
                            elif (len(self.unit.psevdo) > 0): 
                                for uu in self.unit.psevdo: 
                                    if (ur.findSlot(UnitReferent.ATTR_NAME, uu.name_cyr, True) is not None): 
                                        self.unit = uu
                                        self.is_doubt = False
                                        return
                            u = u.base_unit
            if (not ((isinstance(t, TextToken))) or (t.length_char < 3)): 
                continue
            u = self.unit
            while u is not None: 
                for k in u.keywords: 
                    if (t.isValue(k, None)): 
                        self.keyword = t
                        self.is_doubt = False
                        return
                for uu in u.psevdo: 
                    for k in uu.keywords: 
                        if (t.isValue(k, None)): 
                            self.unit = uu
                            self.keyword = t
                            self.is_doubt = False
                            return
                u = u.base_unit
    
    @staticmethod
    def _new1530(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Unit') -> 'UnitToken':
        res = UnitToken(_arg1, _arg2)
        res.unit = _arg3
        return res
    
    @staticmethod
    def _new1634(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'UnitReferent') -> 'UnitToken':
        res = UnitToken(_arg1, _arg2)
        res.ext_onto = _arg3
        return res