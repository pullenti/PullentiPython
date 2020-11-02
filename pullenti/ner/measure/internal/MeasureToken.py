# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.date.internal.DateItemToken import DateItemToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.Referent import Referent
from pullenti.ner.measure.UnitReferent import UnitReferent
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.measure.MeasureKind import MeasureKind
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.NounPhraseToken import NounPhraseToken
from pullenti.ner.measure.MeasureReferent import MeasureReferent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
from pullenti.ner.measure.internal.UnitToken import UnitToken
from pullenti.ner.core.BracketHelper import BracketHelper

class MeasureToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.nums = None;
        self.name = None;
        self.internals = list()
        self.internal_ex = None;
        self.is_set = False
        self.reliable = False
        self.is_empty = False
    
    def __str__(self) -> str:
        return "{0}: {1}".format(self.name, str(self.nums))
    
    def get_norm_values(self) -> str:
        li = self.create_refenets_tokens_with_register(None, False)
        if (li is None or (len(li) < 1)): 
            return None
        mr = Utils.asObjectOrNull(li[len(li) - 1].referent, MeasureReferent)
        if (mr is None): 
            return None
        return mr.to_string(True, None, 0)
    
    def create_refenets_tokens_with_register(self, ad : 'AnalyzerData', register : bool=True) -> typing.List['ReferentToken']:
        if (len(self.internals) == 0 and not self.reliable): 
            if (len(self.nums.units) == 1 and self.nums.units[0].is_doubt): 
                if (self.nums.units[0].unknown_name is not None): 
                    pass
                elif (self.nums.is_newline_before): 
                    pass
                elif (self.nums.units[0].begin_token.length_char > 1 and self.nums.units[0].begin_token.get_morph_class_in_dictionary().is_undefined): 
                    pass
                elif (self.nums.from_val is None or self.nums.to_val is None): 
                    return None
        res = list()
        if (((self.nums is None or self.nums.plus_minus_percent)) and len(self.internals) > 0): 
            li_ex = None
            if (self.internal_ex is not None): 
                li_ex = self.internal_ex.create_refenets_tokens_with_register(ad, True)
                if (li_ex is not None): 
                    res.extend(li_ex)
            mr = MeasureReferent()
            templ0 = "1"
            templ = None
            if (self.name is not None): 
                mr.add_slot(MeasureReferent.ATTR_NAME, self.name, False, 0)
            ints = list()
            k = 0
            first_pass3796 = True
            while True:
                if first_pass3796: first_pass3796 = False
                else: k += 1
                if (not (k < len(self.internals))): break
                ii = self.internals[k]
                ii.reliable = True
                li = ii.create_refenets_tokens_with_register(ad, False)
                if (li is None): 
                    continue
                res.extend(li)
                mr0 = Utils.asObjectOrNull(res[len(res) - 1].referent, MeasureReferent)
                if (li_ex is not None): 
                    mr0.add_slot(MeasureReferent.ATTR_REF, li_ex[len(li_ex) - 1], False, 0)
                if (k == 0 and not self.is_empty): 
                    templ0 = mr0.template
                    mr0.template = "1"
                if (ad is not None): 
                    mr0 = (Utils.asObjectOrNull(ad.register_referent(mr0), MeasureReferent))
                mr.add_slot(MeasureReferent.ATTR_VALUE, mr0, False, 0)
                ints.append(mr0)
                if (templ is None): 
                    templ = "1"
                else: 
                    nu = len(mr.get_string_values(MeasureReferent.ATTR_VALUE))
                    templ = "{0}{1}{2}".format(templ, (", " if self.is_set else " × "), nu)
            if (self.is_set): 
                templ = ("{" + templ + "}")
            if (templ0 != "1"): 
                templ = templ0.replace("1", templ)
            if (self.nums is not None and self.nums.plus_minus_percent and self.nums.single_val is not None): 
                templ = "[{0} ±{1}%]".format(templ, len(self.internals) + 1)
                mr.add_value(self.nums.single_val)
            mr.template = templ
            has_length = False
            uref = None
            i = 0
            while i < len(ints): 
                if (ints[i].kind == MeasureKind.LENGTH): 
                    has_length = True
                    uref = (Utils.asObjectOrNull(ints[i].get_slot_value(MeasureReferent.ATTR_UNIT), UnitReferent))
                elif (len(ints[i].units) > 0): 
                    break
                i += 1
            if (len(ints) > 1 and has_length and uref is not None): 
                for ii in ints: 
                    if (ii.find_slot(MeasureReferent.ATTR_UNIT, None, True) is None): 
                        ii.add_slot(MeasureReferent.ATTR_UNIT, uref, False, 0)
                        ii.kind = MeasureKind.LENGTH
            if (len(ints) == 3): 
                if (ints[0].kind == MeasureKind.LENGTH and ints[1].kind == MeasureKind.LENGTH and ints[2].kind == MeasureKind.LENGTH): 
                    mr.kind = MeasureKind.VOLUME
                elif (len(ints[0].units) == 0 and len(ints[1].units) == 0 and len(ints[2].units) == 0): 
                    nam = mr.get_string_value(MeasureReferent.ATTR_NAME)
                    if (nam is not None): 
                        if ("РАЗМЕР" in nam or "ГАБАРИТ" in nam): 
                            mr.kind = MeasureKind.VOLUME
            if (len(ints) == 2): 
                if (ints[0].kind == MeasureKind.LENGTH and ints[1].kind == MeasureKind.LENGTH): 
                    mr.kind = MeasureKind.AREA
            if (not self.is_empty): 
                if (ad is not None): 
                    mr = (Utils.asObjectOrNull(ad.register_referent(mr), MeasureReferent))
                res.append(ReferentToken(mr, self.begin_token, self.end_token))
            return res
        re2 = self.nums.create_refenets_tokens_with_register(ad, self.name, register)
        for ii in self.internals: 
            li = ii.create_refenets_tokens_with_register(ad, True)
            if (li is None): 
                continue
            res.extend(li)
            re2[len(re2) - 1].referent.add_slot(MeasureReferent.ATTR_REF, res[len(res) - 1].referent, False, 0)
        re2[len(re2) - 1].begin_token = self.begin_token
        re2[len(re2) - 1].end_token = self.end_token
        res.extend(re2)
        return res
    
    @staticmethod
    def try_parse_minimal(t : 'Token', add_units : 'TerminCollection', can_omit_number : bool=False) -> 'MeasureToken':
        if (t is None or (isinstance(t, ReferentToken))): 
            return None
        mt = NumbersWithUnitToken.try_parse_multi(t, add_units, can_omit_number, False, False, False)
        if (mt is None): 
            return None
        if (len(mt[0].units) == 0): 
            return None
        if ((len(mt) == 1 and len(mt[0].units) == 1 and mt[0].units[0].is_doubt) and not mt[0].is_newline_before): 
            return None
        if (len(mt) == 1): 
            res = MeasureToken._new1608(mt[0].begin_token, mt[len(mt) - 1].end_token, mt[0])
            res.__parse_internals(add_units)
            return res
        res = MeasureToken(mt[0].begin_token, mt[len(mt) - 1].end_token)
        for m in mt: 
            res.internals.append(MeasureToken._new1608(m.begin_token, m.end_token, m))
        return res
    
    def __parse_internals(self, add_units : 'TerminCollection') -> None:
        if (self.end_token.next0_ is not None and ((self.end_token.next0_.is_char_of("\\/") or self.end_token.next0_.is_value("ПРИ", None)))): 
            mt1 = MeasureToken.try_parse(self.end_token.next0_.next0_, add_units, True, False, False, False)
            if (mt1 is not None): 
                self.internals.append(mt1)
                self.end_token = mt1.end_token
            else: 
                mt = NumbersWithUnitToken.try_parse(self.end_token.next0_.next0_, add_units, False, False, False, False)
                if (mt is not None and len(mt.units) > 0 and not UnitToken.can_be_equals(self.nums.units, mt.units)): 
                    self.internals.append(MeasureToken._new1608(mt.begin_token, mt.end_token, mt))
                    self.end_token = mt.end_token
    
    @staticmethod
    def try_parse(t : 'Token', add_units : 'TerminCollection', can_be_set : bool=True, can_units_absent : bool=False, is_resctriction : bool=False, is_subval : bool=False) -> 'MeasureToken':
        """ Выделение вместе с наименованием
        
        Args:
            t(Token): 
        
        """
        if (not (isinstance(t, TextToken))): 
            return None
        if (t.is_table_control_char): 
            return None
        t0 = t
        whd = None
        minmax = 0
        wrapminmax1621 = RefOutArgWrapper(minmax)
        tt = NumbersWithUnitToken._is_min_or_max(t0, wrapminmax1621)
        minmax = wrapminmax1621.value
        if (tt is not None): 
            t = tt.next0_
        npt = NounPhraseHelper.try_parse(t, Utils.valToEnum((NounPhraseParseAttr.PARSEPREPOSITION) | (NounPhraseParseAttr.IGNOREBRACKETS), NounPhraseParseAttr), 0, None)
        if (npt is None): 
            whd = NumbersWithUnitToken._try_parsewhl(t)
            if (whd is not None): 
                npt = NounPhraseToken(t0, whd.end_token)
            elif (t0.is_value("КПД", None)): 
                npt = NounPhraseToken(t0, t0)
            elif ((isinstance(t0, TextToken)) and t0.length_char > 3 and t0.get_morph_class_in_dictionary().is_undefined): 
                npt = NounPhraseToken(t0, t0)
            elif (t0.is_value("T", None) and t0.chars.is_all_lower): 
                npt = NounPhraseToken(t0, t0)
                t = t0
                if (t.next0_ is not None and t.next0_.is_char('=')): 
                    npt.end_token = t.next0_
            elif ((isinstance(t0, TextToken)) and t0.chars.is_letter and is_subval): 
                if (NumbersWithUnitToken.try_parse(t, add_units, False, False, False, False) is not None): 
                    return None
                npt = NounPhraseToken(t0, t0)
                t = t0.next0_
                while t is not None: 
                    if (t.whitespaces_before_count > 2): 
                        break
                    elif (not (isinstance(t, TextToken))): 
                        break
                    elif (not t.chars.is_letter): 
                        br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                        if (br is not None): 
                            t = br.end_token
                            npt.end_token = t
                        else: 
                            break
                    elif (NumbersWithUnitToken.try_parse(t, add_units, False, False, False, False) is not None): 
                        break
                    else: 
                        npt.end_token = t
                    t = t.next0_
            else: 
                return None
        elif (NumberHelper.try_parse_real_number(t, True, False) is not None): 
            return None
        else: 
            dtok = DateItemToken.try_attach(t, None, False)
            if (dtok is not None): 
                return None
        t1 = npt.end_token
        t = npt.end_token
        name_ = MetaToken._new509(npt.begin_token, npt.end_token, npt.morph)
        units = None
        units2 = None
        internals_ = list()
        not0_ = False
        tt = t1.next0_
        first_pass3797 = True
        while True:
            if first_pass3797: first_pass3797 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_newline_before): 
                break
            if (tt.is_table_control_char): 
                break
            wrapminmax1613 = RefOutArgWrapper(minmax)
            tt2 = NumbersWithUnitToken._is_min_or_max(tt, wrapminmax1613)
            minmax = wrapminmax1613.value
            if (tt2 is not None): 
                tt = tt2
                t = tt
                t1 = t
                continue
            if ((tt.is_value("БЫТЬ", None) or tt.is_value("ДОЛЖЕН", None) or tt.is_value("ДОЛЖНЫЙ", None)) or tt.is_value("МОЖЕТ", None) or ((tt.is_value("СОСТАВЛЯТЬ", None) and not tt.get_morph_class_in_dictionary().is_adjective))): 
                t = tt
                t1 = t
                if (tt.previous.is_value("НЕ", None)): 
                    not0_ = True
                continue
            www = NumbersWithUnitToken._try_parsewhl(tt)
            if (www is not None): 
                whd = www
                tt = www.end_token
                t = tt
                t1 = t
                continue
            if (tt.is_value("ПРИ", None)): 
                mt1 = MeasureToken.try_parse(tt.next0_, add_units, False, False, True, False)
                if (mt1 is not None): 
                    internals_.append(mt1)
                    tt = mt1.end_token
                    t = tt
                    t1 = t
                    continue
                n1 = NumbersWithUnitToken.try_parse(tt.next0_, add_units, False, False, False, False)
                if (n1 is not None and len(n1.units) > 0): 
                    mt1 = MeasureToken._new1608(n1.begin_token, n1.end_token, n1)
                    internals_.append(mt1)
                    tt = mt1.end_token
                    t = tt
                    t1 = t
                    continue
            if (tt.is_value("ПО", None) and tt.next0_ is not None and tt.next0_.is_value("U", None)): 
                tt = tt.next0_
                t = tt
                t1 = t
                continue
            if (len(internals_) > 0): 
                if (tt.is_char(':')): 
                    break
                mt1 = MeasureToken.try_parse(tt.next0_, add_units, False, False, True, False)
                if (mt1 is not None and mt1.reliable): 
                    internals_.append(mt1)
                    tt = mt1.end_token
                    t = tt
                    t1 = t
                    continue
            if ((isinstance(tt, NumberToken)) and tt.typ == NumberSpellingType.WORDS): 
                npt3 = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.PARSENUMERICASADJECTIVE, 0, None)
                if (npt3 is not None): 
                    tt = npt3.end_token
                    t1 = tt
                    if (len(internals_) == 0): 
                        name_.end_token = t1
                    continue
            if (((tt.is_hiphen and not tt.is_whitespace_before and not tt.is_whitespace_after) and (isinstance(tt.next0_, NumberToken)) and (isinstance(tt.previous, TextToken))) and tt.previous.chars.is_all_upper): 
                t = tt.next0_
                tt = t
                t1 = tt
                if (len(internals_) == 0): 
                    name_.end_token = t1
                continue
            if (((isinstance(tt, NumberToken)) and not tt.is_whitespace_before and (isinstance(tt.previous, TextToken))) and tt.previous.chars.is_all_upper): 
                t = tt
                t1 = t
                if (len(internals_) == 0): 
                    name_.end_token = t1
                continue
            if ((((isinstance(tt, NumberToken)) and not tt.is_whitespace_after and tt.next0_.is_hiphen) and not tt.next0_.is_whitespace_after and (isinstance(tt.next0_.next0_, TextToken))) and tt.next0_.next0_.length_char > 2): 
                tt = tt.next0_.next0_
                t = tt
                t1 = t
                npt1 = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                if (npt1 is not None and npt1.end_char > tt.end_char): 
                    tt = npt1.end_token
                    t = tt
                    t1 = t
                if (len(internals_) == 0): 
                    name_.end_token = t1
                continue
            if ((isinstance(tt, NumberToken)) and tt.previous is not None): 
                if (tt.previous.is_value("USB", None)): 
                    t = tt
                    t1 = t
                    if (len(internals_) == 0): 
                        name_.end_token = t1
                    ttt = tt.next0_
                    while ttt is not None: 
                        if (ttt.is_whitespace_before): 
                            break
                        if (ttt.is_char_of(",:")): 
                            break
                        tt = ttt
                        t = tt
                        t1 = t
                        if (len(internals_) == 0): 
                            name_.end_token = t1
                        ttt = ttt.next0_
                    continue
            mt0 = NumbersWithUnitToken.try_parse(tt, add_units, False, False, False, False)
            if (mt0 is not None): 
                npt1 = NounPhraseHelper.try_parse(tt, Utils.valToEnum((NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.PARSEPREPOSITION), NounPhraseParseAttr), 0, None)
                if (npt1 is not None and npt1.end_char > mt0.end_char): 
                    tt = npt1.end_token
                    t = tt
                    t1 = t
                    if (len(internals_) == 0): 
                        name_.end_token = t1
                    continue
                break
            if (((tt.is_comma or tt.is_char('('))) and tt.next0_ is not None): 
                www = NumbersWithUnitToken._try_parsewhl(tt.next0_)
                if (www is not None): 
                    whd = www
                    tt = www.end_token
                    t = tt
                    t1 = t
                    if (tt.next0_ is not None and tt.next0_.is_comma): 
                        tt = tt.next0_
                        t1 = tt
                    if (tt.next0_ is not None and tt.next0_.is_char(')')): 
                        tt = tt.next0_
                        t1 = tt
                        continue
                uu = UnitToken.try_parse_list(tt.next0_, add_units, False)
                if (uu is not None): 
                    t = uu[len(uu) - 1].end_token
                    t1 = t
                    units = uu
                    if (tt.is_char('(') and t1.next0_ is not None and t1.next0_.is_char(')')): 
                        tt = t1.next0_
                        t = tt
                        t1 = t
                        continue
                    elif (t1.next0_ is not None and t1.next0_.is_char('(')): 
                        uu = UnitToken.try_parse_list(t1.next0_.next0_, add_units, False)
                        if (uu is not None and uu[len(uu) - 1].end_token.next0_ is not None and uu[len(uu) - 1].end_token.next0_.is_char(')')): 
                            units2 = uu
                            tt = uu[len(uu) - 1].end_token.next0_
                            t = tt
                            t1 = t
                            continue
                        www = NumbersWithUnitToken._try_parsewhl(t1.next0_)
                        if (www is not None): 
                            whd = www
                            tt = www.end_token
                            t = tt
                            t1 = t
                            continue
                    if (uu is not None and len(uu) > 0 and not uu[0].is_doubt): 
                        break
                    if (t1.next0_ is not None): 
                        if (t1.next0_.is_table_control_char or t1.is_newline_after): 
                            break
                    units = (None)
            if (BracketHelper.can_be_start_of_sequence(tt, False, False) and not (isinstance(tt.next0_, NumberToken))): 
                br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                if (br is not None): 
                    tt = br.end_token
                    t = tt
                    t1 = t
                    continue
            if (tt.is_value("НЕ", None) and tt.next0_ is not None): 
                mc = tt.next0_.get_morph_class_in_dictionary()
                if (mc.is_adverb or mc.is_misc): 
                    break
                continue
            if (tt.is_value("ЯМЗ", None)): 
                pass
            npt2 = NounPhraseHelper.try_parse(tt, Utils.valToEnum((NounPhraseParseAttr.PARSEPREPOSITION) | (NounPhraseParseAttr.IGNOREBRACKETS) | (NounPhraseParseAttr.PARSEPRONOUNS), NounPhraseParseAttr), 0, None)
            if (npt2 is None): 
                if (tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction): 
                    to = NumbersWithUnitToken.M_TERMINS.try_parse(tt, TerminParseAttr.NO)
                    if (to is not None): 
                        if ((isinstance(to.end_token.next0_, TextToken)) and to.end_token.next0_.is_letters): 
                            pass
                        else: 
                            break
                    t1 = tt
                    continue
                mc = tt.get_morph_class_in_dictionary()
                if (((isinstance(tt, TextToken)) and tt.chars.is_letter and tt.length_char > 1) and (((tt.chars.is_all_upper or mc.is_adverb or mc.is_undefined) or mc.is_adjective))): 
                    uu = UnitToken.try_parse_list(tt, add_units, False)
                    if (uu is not None): 
                        if (uu[0].length_char > 1 or len(uu) > 1): 
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
                if (tt.is_char('.')): 
                    if (not MiscHelper.can_be_start_of_sentence(tt.next0_)): 
                        continue
                    uu = UnitToken.try_parse_list(tt.next0_, add_units, False)
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
            elif (t.is_value("ПРЕДЕЛ", None) or t.is_value("ГРАНИЦА", None) or t.is_value("ДИАПАЗОН", None)): 
                pass
            elif (t.chars.is_letter): 
                name_.end_token = t1
        t11 = t1
        t1 = t1.next0_
        first_pass3798 = True
        while True:
            if first_pass3798: first_pass3798 = False
            else: t1 = t1.next0_
            if (not (t1 is not None)): break
            if (t1.is_table_control_char): 
                pass
            elif (t1.is_char_of(":,_")): 
                if (is_resctriction): 
                    return None
                www = NumbersWithUnitToken._try_parsewhl(t1.next0_)
                if (www is not None): 
                    whd = www
                    t = www.end_token
                    t1 = t
                    continue
                uu = UnitToken.try_parse_list(t1.next0_, add_units, False)
                if (uu is not None): 
                    if (uu[0].length_char > 1 or len(uu) > 1): 
                        units = uu
                        t = uu[len(uu) - 1].end_token
                        t1 = t
                        continue
                if (t1.is_char(':')): 
                    li = list()
                    ttt = t1.next0_
                    first_pass3799 = True
                    while True:
                        if first_pass3799: first_pass3799 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        if (ttt.is_hiphen or ttt.is_table_control_char): 
                            continue
                        if ((isinstance(ttt, TextToken)) and not ttt.chars.is_letter): 
                            continue
                        mt1 = MeasureToken.try_parse(ttt, add_units, True, True, False, True)
                        if (mt1 is None): 
                            break
                        li.append(mt1)
                        ttt = mt1.end_token
                        if (ttt.next0_ is not None and ttt.next0_.is_char(';')): 
                            ttt = ttt.next0_
                        if (ttt.is_char(';')): 
                            pass
                        elif (ttt.is_newline_after and mt1.is_newline_before): 
                            pass
                        else: 
                            break
                    if (len(li) > 1): 
                        res0 = MeasureToken._new1614(t0, li[len(li) - 1].end_token, li, True)
                        if (internals_ is not None and len(internals_) > 0): 
                            res0.internal_ex = internals_[0]
                        nam = MiscHelper.get_text_value_of_meta_token(name_, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                        li[0].begin_token = t0
                        for v in li: 
                            v.name = "{0} ({1})".format(nam, Utils.ifNotNull(v.name, "")).strip()
                            if (v.nums is not None and len(v.nums.units) == 0 and units is not None): 
                                v.nums.units = units
                        return res0
            elif (t1.is_hiphen and t1.is_whitespace_after and t1.is_whitespace_before): 
                pass
            elif (t1.is_hiphen and t1.next0_ is not None and t1.next0_.is_char('(')): 
                pass
            else: 
                break
        if (t1 is None): 
            return None
        mts = NumbersWithUnitToken.try_parse_multi(t1, add_units, False, not0_, True, is_resctriction)
        if (mts is None): 
            if (units is not None and len(units) > 0): 
                if (t1 is None or t1.previous.is_char(':')): 
                    mts = list()
                    if (t1 is None): 
                        t1 = t11
                        while t1 is not None and t1.next0_ is not None: 
                            pass
                            t1 = t1.next0_
                    else: 
                        t1 = t1.previous
                    mts.append(NumbersWithUnitToken._new1615(t0, t1, math.nan))
            if (mts is None): 
                return None
        mt = mts[0]
        if (mt.begin_token == mt.end_token and not (isinstance(mt.begin_token, NumberToken))): 
            return None
        if (not is_subval and name_.begin_token.morph.class0_.is_preposition): 
            name_.begin_token = name_.begin_token.next0_
        if (mt.whl is not None): 
            whd = mt.whl
        for kk in range(10):
            if (whd is not None and whd.end_token == name_.end_token): 
                name_.end_token = whd.begin_token.previous
                continue
            if (units is not None): 
                if (units[len(units) - 1].end_token == name_.end_token): 
                    name_.end_token = units[0].begin_token.previous
                    continue
            break
        if (len(mts) > 1 and len(internals_) == 0): 
            if (len(mt.units) == 0): 
                if (units is not None): 
                    for m in mts: 
                        m.units = units
            res1 = MeasureToken._new1616(t0, mts[len(mts) - 1].end_token, name_.morph, True)
            res1.name = MiscHelper.get_text_value_of_meta_token(name_, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
            k = 0
            while k < len(mts): 
                ttt = MeasureToken._new1608(mts[k].begin_token, mts[k].end_token, mts[k])
                if (whd is not None): 
                    nams = Utils.asObjectOrNull(whd.tag, list)
                    if (k < len(nams)): 
                        ttt.name = nams[k]
                res1.internals.append(ttt)
                k += 1
            tt1 = res1.end_token.next0_
            if (tt1 is not None and tt1.is_char('±')): 
                nn = NumbersWithUnitToken._try_parse(tt1, add_units, True, False, False)
                if (nn is not None and nn.plus_minus_percent): 
                    res1.end_token = nn.end_token
                    res1.nums = nn
                    if (len(nn.units) > 0 and units is None and len(mt.units) == 0): 
                        for m in mts: 
                            m.units = nn.units
            return res1
        if (not mt.is_whitespace_before): 
            if (mt.begin_token.previous is None): 
                return None
            if (mt.begin_token.previous.is_char_of(":),") or mt.begin_token.previous.is_table_control_char or mt.begin_token.previous.is_value("IP", None)): 
                pass
            elif (mt.begin_token.is_hiphen and len(mt.units) > 0 and not mt.units[0].is_doubt): 
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
            units = UnitToken.try_parse_list(mt.end_token.next0_, add_units, True)
            if (units is None): 
                if (can_units_absent): 
                    pass
                else: 
                    return None
            else: 
                mt.units = units
        res = MeasureToken._new1618(t0, mt.end_token, name_.morph, internals_)
        if (((not t0.is_whitespace_before and t0.previous is not None and t0 == name_.begin_token) and t0.previous.is_hiphen and not t0.previous.is_whitespace_before) and (isinstance(t0.previous.previous, TextToken))): 
            name_.begin_token = res.begin_token = name_.begin_token.previous.previous
        res.name = MiscHelper.get_text_value_of_meta_token(name_, (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE if not is_subval else GetTextAttr.NO))
        res.nums = mt
        for u in res.nums.units: 
            if (u.keyword is not None): 
                if (u.keyword.begin_char >= res.begin_char): 
                    res.reliable = True
        res.__parse_internals(add_units)
        if (len(res.internals) > 0 or not can_be_set): 
            return res
        t1 = res.end_token.next0_
        if (t1 is not None and t1.is_comma_and): 
            t1 = t1.next0_
        mts1 = NumbersWithUnitToken.try_parse_multi(t1, add_units, False, False, False, False)
        if ((mts1 is not None and len(mts1) == 1 and (t1.whitespaces_before_count < 3)) and len(mts1[0].units) > 0 and not UnitToken.can_be_equals(mts[0].units, mts1[0].units)): 
            res.is_set = True
            res.nums = (None)
            res.internals.append(MeasureToken._new1608(mt.begin_token, mt.end_token, mt))
            res.internals.append(MeasureToken._new1608(mts1[0].begin_token, mts1[0].end_token, mts1[0]))
            res.end_token = mts1[0].end_token
        return res
    
    @staticmethod
    def _new1608(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'NumbersWithUnitToken') -> 'MeasureToken':
        res = MeasureToken(_arg1, _arg2)
        res.nums = _arg3
        return res
    
    @staticmethod
    def _new1614(_arg1 : 'Token', _arg2 : 'Token', _arg3 : typing.List['MeasureToken'], _arg4 : bool) -> 'MeasureToken':
        res = MeasureToken(_arg1, _arg2)
        res.internals = _arg3
        res.is_empty = _arg4
        return res
    
    @staticmethod
    def _new1616(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : bool) -> 'MeasureToken':
        res = MeasureToken(_arg1, _arg2)
        res.morph = _arg3
        res.reliable = _arg4
        return res
    
    @staticmethod
    def _new1618(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : typing.List['MeasureToken']) -> 'MeasureToken':
        res = MeasureToken(_arg1, _arg2)
        res.morph = _arg3
        res.internals = _arg4
        return res