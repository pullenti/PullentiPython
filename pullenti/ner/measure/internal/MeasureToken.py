# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.measure.MeasureKind import MeasureKind
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr


class MeasureToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.nums = None;
        self.name = None;
        self.internals = list()
        self.is_set = False
        self.reliable = False
    
    def __str__(self) -> str:
        return "{0}: {1}".format(self.name, str(self.nums))
    
    def createRefenetsTokensWithRegister(self, ad : 'AnalyzerData', register : bool=True) -> typing.List['ReferentToken']:
        from pullenti.ner.measure.MeasureReferent import MeasureReferent
        from pullenti.ner.measure.UnitReferent import UnitReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (len(self.internals) == 0 and not self.reliable): 
            if (len(self.nums.units) == 1 and self.nums.units[0].is_doubt and ((self.nums.from_val is None or self.nums.to_val is None))): 
                return None
        res = list()
        if (((self.nums is None or self.nums.plus_minus_percent)) and len(self.internals) > 0): 
            mr = MeasureReferent()
            templ0 = "1"
            templ = None
            if (self.name is not None): 
                mr.addSlot(MeasureReferent.ATTR_NAME, self.name, False, 0)
            ints = list()
            k = 0
            first_pass3048 = True
            while True:
                if first_pass3048: first_pass3048 = False
                else: k += 1
                if (not (k < len(self.internals))): break
                ii = self.internals[k]
                ii.reliable = True
                li = ii.createRefenetsTokensWithRegister(ad, False)
                if (li is None): 
                    continue
                res.extend(li)
                mr0 = Utils.asObjectOrNull(res[len(res) - 1].referent, MeasureReferent)
                if (k == 0): 
                    templ0 = mr0.template
                    mr0.template = "1"
                mr0 = (Utils.asObjectOrNull(ad.registerReferent(mr0), MeasureReferent))
                mr.addSlot(MeasureReferent.ATTR_VALUE, mr0, False, 0)
                ints.append(mr0)
                if (templ is None): 
                    templ = "1"
                else: 
                    nu = len(mr.getStringValues(MeasureReferent.ATTR_VALUE))
                    templ = "{0}{1}{2}".format(templ, (", " if self.is_set else " × "), nu)
            if (self.is_set): 
                templ = ("{" + templ + "}")
            if (templ0 != "1"): 
                templ = templ0.replace("1", templ)
            if (self.nums is not None and self.nums.plus_minus_percent and self.nums.single_val is not None): 
                templ = "[{0} ±{1}%]".format(templ, len(self.internals) + 1)
                mr.addValue(self.nums.single_val)
            mr.template = templ
            has_length = False
            uref = None
            i = 0
            while i < len(ints): 
                if (ints[i].kind == MeasureKind.LENGTH): 
                    has_length = True
                    uref = (Utils.asObjectOrNull(ints[i].getSlotValue(MeasureReferent.ATTR_UNIT), UnitReferent))
                elif (len(ints[i].units) > 0): 
                    break
                i += 1
            if (len(ints) > 1 and has_length and uref is not None): 
                for ii in ints: 
                    if (ii.findSlot(MeasureReferent.ATTR_UNIT, None, True) is None): 
                        ii.addSlot(MeasureReferent.ATTR_UNIT, uref, False, 0)
                        ii.kind = MeasureKind.LENGTH
            if (len(ints) == 3): 
                if (ints[0].kind == MeasureKind.LENGTH and ints[1].kind == MeasureKind.LENGTH and ints[2].kind == MeasureKind.LENGTH): 
                    mr.kind = MeasureKind.VOLUME
                elif (len(ints[0].units) == 0 and len(ints[1].units) == 0 and len(ints[2].units) == 0): 
                    nam = mr.getStringValue(MeasureReferent.ATTR_NAME)
                    if (nam is not None): 
                        if ("РАЗМЕР" in nam or "ГАБАРИТ" in nam): 
                            mr.kind = MeasureKind.VOLUME
            if (len(ints) == 2): 
                if (ints[0].kind == MeasureKind.LENGTH and ints[1].kind == MeasureKind.LENGTH): 
                    mr.kind = MeasureKind.AREA
            res.append(ReferentToken(ad.registerReferent(mr), self.begin_token, self.end_token))
            return res
        re2 = self.nums.createRefenetsTokensWithRegister(ad, self.name, register)
        for ii in self.internals: 
            li = ii.createRefenetsTokensWithRegister(ad, True)
            if (li is None): 
                continue
            res.extend(li)
            re2[len(re2) - 1].referent.addSlot(MeasureReferent.ATTR_REF, res[len(res) - 1].referent, False, 0)
        re2[len(re2) - 1].begin_token = self.begin_token
        re2[len(re2) - 1].end_token = self.end_token
        res.extend(re2)
        return res
    
    @staticmethod
    def tryParseMinimal(t : 'Token', add_units : 'TerminCollection', can_omit_number : bool=False) -> 'MeasureToken':
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
        if (t is None or (isinstance(t, ReferentToken))): 
            return None
        mt = NumbersWithUnitToken.tryParseMulti(t, add_units, can_omit_number, False)
        if (mt is None): 
            return None
        if (len(mt[0].units) == 0): 
            return None
        if (len(mt) == 1 and len(mt[0].units) == 1 and mt[0].units[0].is_doubt): 
            return None
        if (len(mt) == 1): 
            res = MeasureToken._new1519(mt[0].begin_token, mt[len(mt) - 1].end_token, mt[0])
            res.__parseInternals(add_units)
            return res
        res = MeasureToken(mt[0].begin_token, mt[len(mt) - 1].end_token)
        for m in mt: 
            res.internals.append(MeasureToken._new1519(m.begin_token, m.end_token, m))
        return res
    
    def __parseInternals(self, add_units : 'TerminCollection') -> None:
        from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
        from pullenti.ner.measure.internal.UnitToken import UnitToken
        if (self.end_token.next0_ is not None and ((self.end_token.next0_.isCharOf("\\/") or self.end_token.next0_.isValue("ПРИ", None)))): 
            mt1 = MeasureToken.tryParse(self.end_token.next0_.next0_, add_units, True)
            if (mt1 is not None): 
                self.internals.append(mt1)
                self.end_token = mt1.end_token
            else: 
                mt = NumbersWithUnitToken.tryParse(self.end_token.next0_.next0_, add_units, False, False)
                if (mt is not None and len(mt.units) > 0 and not UnitToken.canBeEquals(self.nums.units, mt.units)): 
                    self.internals.append(MeasureToken._new1519(mt.begin_token, mt.end_token, mt))
                    self.end_token = mt.end_token
    
    @staticmethod
    def tryParse(t : 'Token', add_units : 'TerminCollection', can_be_set : bool=True) -> 'MeasureToken':
        """ Выделение вместе с наименованием
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.core.NounPhraseToken import NounPhraseToken
        from pullenti.ner.core.NumberExToken import NumberExToken
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        from pullenti.ner.measure.internal.UnitToken import UnitToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        if (not ((isinstance(t, TextToken)))): 
            return None
        t0 = t
        whd = None
        minmax = 0
        wrapminmax1529 = RefOutArgWrapper(minmax)
        tt = NumbersWithUnitToken._isMinOrMax(t0, wrapminmax1529)
        minmax = wrapminmax1529.value
        if (tt is not None): 
            t = tt.next0_
        npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.PARSEPREPOSITION, 0)
        if (npt is None): 
            whd = NumbersWithUnitToken._tryParseWHL(t)
            if (whd is not None): 
                npt = NounPhraseToken(t0, whd.end_token)
            elif (t0.isValue("КПД", None)): 
                npt = NounPhraseToken(t0, t0)
            elif ((isinstance(t0, TextToken)) and t0.length_char > 3 and t0.getMorphClassInDictionary().is_undefined): 
                npt = NounPhraseToken(t0, t0)
            else: 
                return None
        elif (NumberExToken.tryParseFloatNumber(t, True) is not None): 
            return None
        else: 
            dtok = DateItemToken.tryAttach(t, None)
            if (dtok is not None): 
                return None
        t1 = npt.end_token
        t = npt.end_token
        name_ = MetaToken._new600(npt.begin_token, npt.end_token, npt.morph)
        units = None
        units2 = None
        internals_ = list()
        not0_ = False
        tt = t1.next0_
        first_pass3049 = True
        while True:
            if first_pass3049: first_pass3049 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_newline_before): 
                break
            wrapminmax1523 = RefOutArgWrapper(minmax)
            tt2 = NumbersWithUnitToken._isMinOrMax(tt, wrapminmax1523)
            minmax = wrapminmax1523.value
            if (tt2 is not None): 
                tt = tt2
                t = tt
                t1 = t
                continue
            if ((tt.isValue("БЫТЬ", None) or tt.isValue("ДОЛЖЕН", None) or tt.isValue("ДОЛЖНЫЙ", None)) or tt.isValue("МОЖЕТ", None) or ((tt.isValue("СОСТАВЛЯТЬ", None) and not tt.getMorphClassInDictionary().is_adjective))): 
                t = tt
                t1 = t
                if (tt.previous.isValue("НЕ", None)): 
                    not0_ = True
                continue
            www = NumbersWithUnitToken._tryParseWHL(tt)
            if (www is not None): 
                whd = www
                tt = www.end_token
                t = tt
                t1 = t
                continue
            if (len(internals_) > 0 and tt.is_comma_and): 
                continue
            if (tt.isValue("ПРИ", None) or len(internals_) > 0): 
                mt1 = MeasureToken.tryParse(tt.next0_, add_units, False)
                if (mt1 is not None and mt1.reliable): 
                    internals_.append(mt1)
                    tt = mt1.end_token
                    t = tt
                    t1 = t
                    continue
            mt0 = NumbersWithUnitToken.tryParse(tt, add_units, False, False)
            if (mt0 is not None): 
                break
            if (((tt.is_comma or tt.isChar('('))) and tt.next0_ is not None): 
                www = NumbersWithUnitToken._tryParseWHL(tt.next0_)
                if (www is not None): 
                    whd = www
                    tt = www.end_token
                    t = tt
                    t1 = t
                    if (tt.next0_ is not None and tt.next0_.is_comma): 
                        tt = tt.next0_
                        t1 = tt
                    if (tt.next0_ is not None and tt.next0_.isChar(')')): 
                        tt = tt.next0_
                        t1 = tt
                        continue
                uu = UnitToken.tryParseList(tt.next0_, add_units)
                if (uu is not None): 
                    t = uu[len(uu) - 1].end_token
                    t1 = t
                    units = uu
                    if (tt.isChar('(') and t1.next0_ is not None and t1.next0_.isChar(')')): 
                        tt = t1.next0_
                        t = tt
                        t1 = t
                        continue
                    elif (t1.next0_ is not None and t1.next0_.isChar('(')): 
                        uu = UnitToken.tryParseList(t1.next0_.next0_, add_units)
                        if (uu is not None and uu[len(uu) - 1].end_token.next0_ is not None and uu[len(uu) - 1].end_token.next0_.isChar(')')): 
                            units2 = uu
                            tt = uu[len(uu) - 1].end_token.next0_
                            t = tt
                            t1 = t
                            continue
                    if (uu is not None and len(uu) > 0 and not uu[0].is_doubt): 
                        break
            if (BracketHelper.canBeStartOfSequence(tt, False, False)): 
                br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                if (br is not None): 
                    tt = br.end_token
                    t = tt
                    t1 = t
                    continue
            if (tt.isValue("НЕ", None) and tt.next0_ is not None): 
                mc = tt.next0_.getMorphClassInDictionary()
                if (mc.is_adverb or mc.is_misc): 
                    break
                continue
            if (tt.isValue("ЯМЗ", None)): 
                pass
            npt2 = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.PARSEPREPOSITION, 0)
            if (npt2 is None): 
                if (tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction): 
                    to = NumbersWithUnitToken.M_TERMINS.tryParse(tt, TerminParseAttr.NO)
                    if (to is not None): 
                        if ((isinstance(to.end_token.next0_, TextToken)) and to.end_token.next0_.is_letters): 
                            pass
                        else: 
                            break
                    t1 = tt
                    continue
                mc = tt.getMorphClassInDictionary()
                if (((isinstance(tt, TextToken)) and tt.chars.is_letter and tt.length_char > 1) and (((tt.chars.is_all_upper or mc.is_adverb or mc.is_undefined) or mc.is_adjective))): 
                    uu = UnitToken.tryParseList(tt, add_units)
                    if (uu is not None): 
                        if (uu[0].length_char > 2 or len(uu) > 1): 
                            units = uu
                            t = uu[len(uu) - 1].end_token
                            t1 = t
                            break
                    t = tt
                    t1 = t
                    if (len(internals_) == 0): 
                        name_.end_token = tt
                    continue
                if (tt.is_comma): 
                    continue
                if (tt.isChar('.')): 
                    if (not MiscHelper.canBeStartOfSentence(tt.next0_)): 
                        continue
                    uu = UnitToken.tryParseList(tt.next0_, add_units)
                    if (uu is not None): 
                        if (uu[0].length_char > 2 or len(uu) > 1): 
                            units = uu
                            t = uu[len(uu) - 1].end_token
                            t1 = t
                            break
                break
            tt = npt2.end_token
            t = tt
            t1 = t
            if (len(internals_) > 0): 
                pass
            elif (t.isValue("ПРЕДЕЛ", None) or t.isValue("ГРАНИЦА", None) or t.isValue("ДИАПАЗОН", None)): 
                pass
            elif (t.chars.is_letter): 
                name_.end_token = t1
        t1 = t1.next0_
        first_pass3050 = True
        while True:
            if first_pass3050: first_pass3050 = False
            else: t1 = t1.next0_
            if (not (t1 is not None)): break
            if (t1.is_table_control_char): 
                pass
            elif (t1.isCharOf(":,_")): 
                www = NumbersWithUnitToken._tryParseWHL(t1.next0_)
                if (www is not None): 
                    whd = www
                    t = www.end_token
                    t1 = t
                    continue
            elif (t1.is_hiphen and t1.is_whitespace_after and t1.is_whitespace_before): 
                pass
            else: 
                break
        if (t1 is None): 
            return None
        mts = NumbersWithUnitToken.tryParseMulti(t1, add_units, False, not0_)
        if (mts is None): 
            return None
        mt = mts[0]
        if (name_.begin_token.morph.class0_.is_preposition): 
            name_.begin_token = name_.begin_token.next0_
        if (len(mts) > 1 and len(internals_) == 0): 
            if (len(mt.units) == 0): 
                if (units is not None): 
                    for m in mts: 
                        m.units = units
            res1 = MeasureToken._new1524(t0, mts[len(mts) - 1].end_token, name_.morph, True)
            res1.name = MiscHelper.getTextValueOfMetaToken(name_, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
            k = 0
            while k < len(mts): 
                ttt = MeasureToken._new1519(mts[k].begin_token, mts[k].end_token, mts[k])
                if (whd is not None): 
                    nams = Utils.asObjectOrNull(whd.tag, list)
                    if (k < len(nams)): 
                        ttt.name = nams[k]
                res1.internals.append(ttt)
                k += 1
            tt1 = res1.end_token.next0_
            if (tt1 is not None and tt1.isChar('±')): 
                nn = NumbersWithUnitToken._tryParse(tt1, add_units, True, False)
                if (nn is not None and nn.plus_minus_percent): 
                    res1.end_token = nn.end_token
                    res1.nums = nn
            return res1
        if (not mt.is_whitespace_before): 
            if (mt.begin_token.previous is None): 
                return None
            if (mt.begin_token.previous.isCharOf(":),")): 
                pass
            else: 
                return None
        if (len(mt.units) == 0 and units is not None): 
            mt.units = units
            if (mt.div_num is not None and len(units) > 1 and len(mt.div_num.units) == 0): 
                i = 1
                while i < len(units): 
                    if (units[i].pow0_ == -1): 
                        j = i
                        while j < len(units): 
                            mt.div_num.units.append(units[j])
                            units[j].pow0_ = (- units[j].pow0_)
                            j += 1
                        del mt.units[i:i+len(units) - i]
                        break
                    i += 1
        if ((minmax < 0) and mt.single_val is not None): 
            mt.from_val = mt.single_val
            mt.from_include = True
            mt.single_val = (None)
        if (minmax > 0 and mt.single_val is not None): 
            mt.to_val = mt.single_val
            mt.to_include = True
            mt.single_val = (None)
        if (len(mt.units) == 0): 
            return None
        res = MeasureToken._new1526(t0, mt.end_token, name_.morph, internals_)
        if (((not t0.is_whitespace_before and t0.previous is not None and t0 == name_.begin_token) and t0.previous.is_hiphen and not t0.previous.is_whitespace_before) and (isinstance(t0.previous.previous, TextToken))): 
            name_.begin_token = res.begin_token = name_.begin_token.previous.previous
        res.name = MiscHelper.getTextValueOfMetaToken(name_, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
        res.nums = mt
        for u in res.nums.units: 
            if (u.keyword is not None): 
                if (u.keyword.begin_char >= res.begin_char): 
                    res.reliable = True
        res.__parseInternals(add_units)
        if (len(res.internals) > 0 or not can_be_set): 
            return res
        t1 = res.end_token.next0_
        if (t1 is not None and t1.is_comma_and): 
            t1 = t1.next0_
        mts1 = NumbersWithUnitToken.tryParseMulti(t1, add_units, False, False)
        if ((mts1 is not None and len(mts1) == 1 and (t1.whitespaces_before_count < 3)) and len(mts1[0].units) > 0 and not UnitToken.canBeEquals(mts[0].units, mts1[0].units)): 
            res.is_set = True
            res.nums = (None)
            res.internals.append(MeasureToken._new1519(mt.begin_token, mt.end_token, mt))
            res.internals.append(MeasureToken._new1519(mts1[0].begin_token, mts1[0].end_token, mts1[0]))
            res.end_token = mts1[0].end_token
        return res
    
    @staticmethod
    def _new1519(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'NumbersWithUnitToken') -> 'MeasureToken':
        res = MeasureToken(_arg1, _arg2)
        res.nums = _arg3
        return res
    
    @staticmethod
    def _new1524(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : bool) -> 'MeasureToken':
        res = MeasureToken(_arg1, _arg2)
        res.morph = _arg3
        res.reliable = _arg4
        return res
    
    @staticmethod
    def _new1526(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : typing.List['MeasureToken']) -> 'MeasureToken':
        res = MeasureToken(_arg1, _arg2)
        res.morph = _arg3
        res.internals = _arg4
        return res