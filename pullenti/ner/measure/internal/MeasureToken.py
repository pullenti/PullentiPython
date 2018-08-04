# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.measure.internal.MeasureHelper import MeasureHelper


class MeasureToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        self.nums = None
        self.name = None
        self.internals = list()
        self.is_set = False
        self.reliable = False
        super().__init__(b, e0_, None)
    
    def __str__(self) -> str:
        return "{0}: {1}".format(self.name, str(self.nums))
    
    def create_refenets_tokens_with_register(self, ad : 'AnalyzerData', register : bool=True) -> typing.List['ReferentToken']:
        from pullenti.ner.measure.MeasureReferent import MeasureReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (len(self.internals) == 0 and not self.reliable): 
            if (len(self.nums.units) == 1 and self.nums.units[0].is_doubt and ((self.nums.from_val is None or self.nums.to_val is None))): 
                return None
        res = list()
        if (self.nums is None and len(self.internals) > 0): 
            mr = MeasureReferent()
            templ0 = "1"
            templ = None
            if (self.name is not None): 
                mr.add_slot(MeasureReferent.ATTR_NAME, self.name, False, 0)
            for k in range(len(self.internals)):
                ii = self.internals[k]
                ii.reliable = True
                li = ii.create_refenets_tokens_with_register(ad, False)
                if (li is None): 
                    continue
                res.extend(li)
                mr0 = (res[len(res) - 1].referent if isinstance(res[len(res) - 1].referent, MeasureReferent) else None)
                if (k == 0): 
                    templ0 = mr0.template
                    mr0.template = "1"
                mr0 = (ad.register_referent(mr0) if isinstance(ad.register_referent(mr0), MeasureReferent) else None)
                mr.add_slot(MeasureReferent.ATTR_VALUE, mr0, False, 0)
                if (templ is None): 
                    templ = "1"
                else: 
                    nu = len(mr.get_string_values(MeasureReferent.ATTR_VALUE))
                    templ = "{0}{1}{2}".format(templ, (", " if self.is_set else " × "), nu)
            if (self.is_set): 
                templ = ("{" + templ + "}")
            if (templ0 != "1"): 
                templ = templ0.replace("1", templ)
            mr.template = templ
            res.append(ReferentToken(ad.register_referent(mr), self.begin_token, self.end_token))
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
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
        if (t is None or isinstance(t, ReferentToken)): 
            return None
        mt = NumbersWithUnitToken.try_parse_multi(t, add_units, can_omit_number)
        if (mt is None): 
            return None
        if (len(mt[0].units) == 0): 
            return None
        if (len(mt) == 1 and len(mt[0].units) == 1 and mt[0].units[0].is_doubt): 
            return None
        if (len(mt) == 1): 
            res = MeasureToken._new1504(mt[0].begin_token, mt[len(mt) - 1].end_token, mt[0])
            res.__parse_internals(add_units)
            return res
        res = MeasureToken(mt[0].begin_token, mt[len(mt) - 1].end_token)
        for m in mt: 
            res.internals.append(MeasureToken._new1504(m.begin_token, m.end_token, m))
        return res
    
    def __parse_internals(self, add_units : 'TerminCollection') -> None:
        from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
        from pullenti.ner.measure.internal.UnitToken import UnitToken
        if (self.end_token.next0_ is not None and ((self.end_token.next0_.is_char_of("\\/") or self.end_token.next0_.is_value("ПРИ", None)))): 
            mt1 = MeasureToken.try_parse(self.end_token.next0_.next0_, add_units, True)
            if (mt1 is not None): 
                self.internals.append(mt1)
                self.end_token = mt1.end_token
            else: 
                mt = NumbersWithUnitToken.try_parse(self.end_token.next0_.next0_, add_units, False)
                if (mt is not None and len(mt.units) > 0 and not UnitToken.can_be_equals(self.nums.units, mt.units)): 
                    self.internals.append(MeasureToken._new1504(mt.begin_token, mt.end_token, mt))
                    self.end_token = mt.end_token
    
    @staticmethod
    def try_parse(t : 'Token', add_units : 'TerminCollection', can_be_set : bool=True) -> 'MeasureToken':
        """ Выделение вместе с наименованием
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.core.NounPhraseToken import NounPhraseToken
        from pullenti.ner.core.NumberExToken import NumberExToken
        from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
        from pullenti.ner.measure.internal.UnitToken import UnitToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        if (not ((isinstance(t, TextToken)))): 
            return None
        t0 = t
        whd = None
        minmax = 0
        inoutarg1514 = RefOutArgWrapper(minmax)
        tt = MeasureToken.__is_min_or_max(t0, inoutarg1514)
        minmax = inoutarg1514.value
        if (tt is not None): 
            t = tt.next0_
        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSEPREPOSITION, 0)
        if (npt is None): 
            whd = MeasureToken.__try_parsewhl(t)
            if (whd is not None): 
                npt = NounPhraseToken(t0, whd.end_token)
            elif (t0.is_value("КПД", None)): 
                npt = NounPhraseToken(t0, t0)
            else: 
                return None
        elif (NumberExToken.try_parse_float_number(t, True) is not None): 
            return None
        elif (npt.is_newline_after): 
            return None
        t1 = npt.end_token
        t = npt.end_token
        name_ = MetaToken._new590(npt.begin_token, npt.end_token, npt.morph)
        units = None
        units2 = None
        internals_ = list()
        tt = t1.next0_
        first_pass2968 = True
        while True:
            if first_pass2968: first_pass2968 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_newline_before): 
                break
            inoutarg1508 = RefOutArgWrapper(minmax)
            tt2 = MeasureToken.__is_min_or_max(tt, inoutarg1508)
            minmax = inoutarg1508.value
            if (tt2 is not None): 
                tt = tt2
                t = tt
                t1 = t
                continue
            www = MeasureToken.__try_parsewhl(tt)
            if (www is not None): 
                whd = www
                tt = www.end_token
                t = tt
                t1 = t
                continue
            if (len(internals_) > 0 and tt.is_comma_and): 
                continue
            if (tt.is_value("ПРИ", None) or len(internals_) > 0): 
                mt1 = MeasureToken.try_parse(tt.next0_, add_units, False)
                if (mt1 is not None and mt1.reliable): 
                    internals_.append(mt1)
                    tt = mt1.end_token
                    t = tt
                    t1 = t
                    continue
            mt0 = NumbersWithUnitToken.try_parse(t1, add_units, False)
            if (mt0 is not None): 
                break
            if (((tt.is_comma or tt.is_char('('))) and tt.next0_ is not None): 
                www = MeasureToken.__try_parsewhl(tt.next0_)
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
                uu = UnitToken.try_parse_list(tt.next0_, add_units)
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
                        uu = UnitToken.try_parse_list(t1.next0_.next0_, add_units)
                        if (uu is not None and uu[len(uu) - 1].end_token.next0_ is not None and uu[len(uu) - 1].end_token.next0_.is_char(')')): 
                            units2 = uu
                            tt = uu[len(uu) - 1].end_token.next0_
                            t = tt
                            t1 = t
                            continue
                    if (not uu[0].is_doubt): 
                        break
            if (BracketHelper.can_be_start_of_sequence(tt, False, False)): 
                br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                if (br is not None): 
                    tt = br.end_token
                    t = tt
                    t1 = t
                    continue
            if (tt.is_value("ЯМЗ", None)): 
                pass
            npt2 = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.PARSEPREPOSITION, 0)
            if (npt2 is None): 
                if (tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction): 
                    to = NumbersWithUnitToken._m_termins.try_parse(tt, TerminParseAttr.NO)
                    if (to is not None): 
                        if (isinstance(to.end_token.next0_, TextToken) and to.end_token.next0_.is_letters): 
                            pass
                        else: 
                            break
                    t1 = tt
                    continue
                mc = tt.get_morph_class_in_dictionary()
                if ((isinstance(tt, TextToken) and tt.chars.is_letter and tt.length_char > 1) and (((tt.chars.is_all_upper or mc.is_adverb or mc.is_undefined) or mc.is_adjective))): 
                    t = tt
                    t1 = t
                    if (len(internals_) == 0): 
                        name_.end_token = tt
                    continue
                if (tt.is_comma): 
                    continue
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
        t1 = t1.next0_
        while t1 is not None: 
            if (t1.is_table_control_char): 
                pass
            elif (t1.is_char_of(":,_")): 
                pass
            elif (t1.is_hiphen and t1.is_whitespace_after and t1.is_whitespace_before): 
                pass
            else: 
                break
            t1 = t1.next0_
        if (t1 is None): 
            return None
        mts = NumbersWithUnitToken.try_parse_multi(t1, add_units, False)
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
            res1 = MeasureToken._new1509(t0, mts[len(mts) - 1].end_token, name_.morph, True)
            res1.name = MiscHelper.get_text_value_of_meta_token(name_, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
            for k in range(len(mts)):
                ttt = MeasureToken._new1504(mts[k].begin_token, mts[k].end_token, mts[k])
                if (whd is not None): 
                    nams = (whd.tag if isinstance(whd.tag, list) else None)
                    if (k < len(nams)): 
                        ttt.name = nams[k]
                res1.internals.append(ttt)
            return res1
        if (len(mt.units) == 0 and units is not None): 
            mt.units = units
        if ((minmax < 0) and mt.single_val is not None): 
            mt.from_val = mt.single_val
            mt.from_include = True
            mt.single_val = None
        if (minmax > 0 and mt.single_val is not None): 
            mt.to_val = mt.single_val
            mt.to_include = True
            mt.single_val = None
        if (len(mt.units) == 0): 
            return None
        res = MeasureToken._new1511(t0, mt.end_token, name_.morph, internals_)
        res.name = MiscHelper.get_text_value_of_meta_token(name_, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
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
        mts1 = NumbersWithUnitToken.try_parse_multi(t1, add_units, False)
        if ((mts1 is not None and len(mts1) == 1 and (t1.whitespaces_before_count < 3)) and len(mts1[0].units) > 0 and not UnitToken.can_be_equals(mts[0].units, mts1[0].units)): 
            res.is_set = True
            res.nums = None
            res.internals.append(MeasureToken._new1504(mt.begin_token, mt.end_token, mt))
            res.internals.append(MeasureToken._new1504(mts1[0].begin_token, mts1[0].end_token, mts1[0]))
            res.end_token = mts1[0].end_token
        return res
    
    @staticmethod
    def __is_min_or_max(t : 'Token', res : int) -> 'Token':
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
            t = MeasureToken.__is_min_or_max(t.next0_, res)
            if (t is not None and t.next0_ is not None and t.next0_.is_char(')')): 
                t = t.next0_
            return t
        return None
    
    @staticmethod
    def __try_parsewhl(t : 'Token') -> 'MetaToken':
        """ Это распознавание написаний ГхШхВ
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.TextToken import TextToken
        if (not ((isinstance(t, TextToken)))): 
            return None
        txt = (t if isinstance(t, TextToken) else None).term
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
            return MetaToken._new825(t, t, nams)
        t0 = t
        t1 = t
        while t is not None: 
            if (not ((isinstance(t, TextToken))) or t.whitespaces_before_count > 1): 
                break
            term = (t if isinstance(t, TextToken) else None).term
            nam = None
            if ((t.is_value("ДЛИНА", None) or t.is_value("ДЛИННА", None) or term == "Д") or term == "ДЛ" or term == "ДЛИН"): 
                nam = "ДЛИНА"
            elif ((t.is_value("ШИРИНА", None) or t.is_value("ШИРОТА", None) or term == "Ш") or term == "ШИР" or term == "ШИРИН"): 
                nam = "ШИРИНА"
            elif ((t.is_value("ГЛУБИНА", None) or term == "Г" or term == "ГЛ") or term == "ГЛУБ"): 
                nam = "ГЛУБИНА"
            elif (t.is_value("ВЫСОТА", None) or term == "В" or term == "ВЫС"): 
                nam = "ВЫСОТА"
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
            if (MeasureHelper.is_mult_char(t.next0_) or t.next0_.is_comma): 
                t = t.next0_
            t = t.next0_
        if (nams is None or (len(nams) < 2)): 
            return None
        return MetaToken._new825(t0, t1, nams)

    
    @staticmethod
    def _new1504(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'NumbersWithUnitToken') -> 'MeasureToken':
        res = MeasureToken(_arg1, _arg2)
        res.nums = _arg3
        return res
    
    @staticmethod
    def _new1509(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : bool) -> 'MeasureToken':
        res = MeasureToken(_arg1, _arg2)
        res.morph = _arg3
        res.reliable = _arg4
        return res
    
    @staticmethod
    def _new1511(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : typing.List['MeasureToken']) -> 'MeasureToken':
        res = MeasureToken(_arg1, _arg2)
        res.morph = _arg3
        res.internals = _arg4
        return res