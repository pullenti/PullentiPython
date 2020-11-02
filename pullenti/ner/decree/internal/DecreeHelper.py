# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import datetime
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.money.MoneyReferent import MoneyReferent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.decree.internal.CanonicDecreeRefUri import CanonicDecreeRefUri
from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
from pullenti.ner.decree.DecreeKind import DecreeKind
from pullenti.ner.decree.DecreeReferent import DecreeReferent
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.decree.internal.PartToken import PartToken
from pullenti.ner.decree.internal.DecreeToken import DecreeToken

class DecreeHelper:
    # Некоторые полезные функции для НПА
    
    @staticmethod
    def parse_date_time(str0_ : str) -> datetime.datetime:
        if (Utils.isNullOrEmpty(str0_)): 
            return None
        try: 
            prts = Utils.splitString(str0_, '.', False)
            wrapy831 = RefOutArgWrapper(0)
            inoutres832 = Utils.tryParseInt(prts[0], wrapy831)
            y = wrapy831.value
            if (not inoutres832): 
                return None
            mon = 0
            day = 0
            if (len(prts) > 1): 
                wrapmon829 = RefOutArgWrapper(0)
                inoutres830 = Utils.tryParseInt(prts[1], wrapmon829)
                mon = wrapmon829.value
                if (inoutres830): 
                    if (len(prts) > 2): 
                        wrapday828 = RefOutArgWrapper(0)
                        Utils.tryParseInt(prts[2], wrapday828)
                        day = wrapday828.value
            if (mon <= 0): 
                mon = 1
            if (day <= 0): 
                day = 1
            if (day > Utils.lastDayOfMonth(y, mon)): 
                day = Utils.lastDayOfMonth(y, mon)
            return datetime.datetime(y, mon, day, 0, 0, 0)
        except Exception as ex: 
            pass
        return None
    
    @staticmethod
    def try_create_canonic_decree_ref_uri(t : 'Token') -> 'CanonicDecreeRefUri':
        """ Это для оформления ссылок по некоторым стандартам (когда гиперссылкой нужно выделить не всю сущность,
        а лишь некоторую её часть)
        
        Args:
            t(Token): 
        
        """
        if (not (isinstance(t, ReferentToken))): 
            return None
        dr = Utils.asObjectOrNull(t.get_referent(), DecreeReferent)
        if (dr is not None): 
            if (dr.kind == DecreeKind.PUBLISHER): 
                return None
            res = CanonicDecreeRefUri._new833(t.kit.sofa.text, dr, t.begin_char, t.end_char)
            if ((t.previous is not None and t.previous.is_char('(') and t.next0_ is not None) and t.next0_.is_char(')')): 
                return res
            if (t.misc_attrs != 0): 
                return res
            rt = Utils.asObjectOrNull(t, ReferentToken)
            if (rt.begin_token.is_char('(') and rt.end_token.is_char(')')): 
                res = CanonicDecreeRefUri._new833(t.kit.sofa.text, dr, rt.begin_token.next0_.begin_char, rt.end_token.previous.end_char)
                return res
            next_decree_items = None
            if ((t.next0_ is not None and t.next0_.is_comma_and and (isinstance(t.next0_.next0_, ReferentToken))) and (isinstance(t.next0_.next0_.get_referent(), DecreeReferent))): 
                next_decree_items = DecreeToken.try_attach_list(t.next0_.next0_.begin_token, None, 10, False)
                if (next_decree_items is not None and len(next_decree_items) > 1): 
                    i = 0
                    while i < (len(next_decree_items) - 1): 
                        if (next_decree_items[i].is_newline_after): 
                            del next_decree_items[i + 1:i + 1+len(next_decree_items) - i - 1]
                            break
                        i += 1
            was_typ = False
            was_num = False
            tt = t.begin_token
            first_pass3583 = True
            while True:
                if first_pass3583: first_pass3583 = False
                else: tt = tt.next0_
                if (not (tt is not None and tt.end_char <= t.end_char)): break
                if (tt.begin_char == t.begin_char and tt.is_char('(') and tt.next0_ is not None): 
                    res.begin_char = tt.next0_.begin_char
                if (tt.is_char('(') and tt.next0_ is not None and tt.next0_.is_value("ДАЛЕЕ", None)): 
                    if (res.end_char >= tt.begin_char): 
                        res.end_char = tt.previous.end_char
                    break
                if (tt.end_char == t.end_char and tt.is_char(')')): 
                    res.end_char = tt.previous.end_char
                    tt1 = tt.previous
                    while tt1 is not None and tt1.begin_char >= res.begin_char: 
                        if (tt1.is_char('(') and tt1.previous is not None): 
                            if (res.begin_char < tt1.previous.begin_char): 
                                res.end_char = tt1.previous.end_char
                        tt1 = tt1.previous
                li = DecreeToken.try_attach_list(tt, None, 10, False)
                if (li is not None and len(li) > 0): 
                    ii = 0
                    while ii < (len(li) - 1): 
                        if (li[ii].typ == DecreeToken.ItemType.TYP and li[ii + 1].typ == DecreeToken.ItemType.TERR): 
                            res.type_with_geo = MiscHelper.get_text_value(li[ii].begin_token, li[ii + 1].end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE)
                        ii += 1
                    if ((next_decree_items is not None and len(next_decree_items) > 1 and (len(next_decree_items) < len(li))) and next_decree_items[0].typ != DecreeToken.ItemType.TYP): 
                        d = len(li) - len(next_decree_items)
                        j = 0
                        while j < len(next_decree_items): 
                            if (next_decree_items[j].typ != li[d + j].typ): 
                                break
                            j += 1
                        if (j >= len(next_decree_items)): 
                            del li[0:0+d]
                            res.begin_char = li[0].begin_char
                    elif ((next_decree_items is not None and len(next_decree_items) == 1 and next_decree_items[0].typ == DecreeToken.ItemType.NAME) and len(li) == 2 and li[1].typ == DecreeToken.ItemType.NAME): 
                        res.begin_char = li[1].begin_char
                        res.end_char = li[1].end_char
                        break
                    elif ((next_decree_items is not None and len(next_decree_items) == 1 and next_decree_items[0].typ == DecreeToken.ItemType.NUMBER) and li[len(li) - 1].typ == DecreeToken.ItemType.NUMBER): 
                        res.begin_char = li[len(li) - 1].begin_char
                        res.end_char = li[len(li) - 1].end_char
                    i = 0
                    first_pass3584 = True
                    while True:
                        if first_pass3584: first_pass3584 = False
                        else: i += 1
                        if (not (i < len(li))): break
                        l_ = li[i]
                        if (l_.begin_char > t.end_char): 
                            del li[i:i+len(li) - i]
                            break
                        if (l_.typ == DecreeToken.ItemType.NAME): 
                            if (not was_num): 
                                if (dr.kind == DecreeKind.CONTRACT): 
                                    continue
                                if (((i + 1) < len(li)) and ((li[i + 1].typ == DecreeToken.ItemType.DATE or li[i + 1].typ == DecreeToken.ItemType.NUMBER))): 
                                    continue
                            ee = l_.begin_token.previous.end_char
                            if (ee > res.begin_char and (ee < res.end_char)): 
                                res.end_char = ee
                            break
                        if (l_.typ == DecreeToken.ItemType.NUMBER): 
                            was_num = True
                        if (i == 0): 
                            if (l_.typ == DecreeToken.ItemType.TYP): 
                                was_typ = True
                            elif (l_.typ == DecreeToken.ItemType.OWNER or l_.typ == DecreeToken.ItemType.ORG): 
                                if (((i + 1) < len(li)) and ((li[1].typ == DecreeToken.ItemType.DATE or li[1].typ == DecreeToken.ItemType.NUMBER))): 
                                    was_typ = True
                            if (was_typ): 
                                tt0 = l_.begin_token.previous
                                if (tt0 is not None and tt0.is_char('.')): 
                                    tt0 = tt0.previous
                                if (tt0 is not None and ((tt0.is_value("УТВЕРЖДЕННЫЙ", None) or tt0.is_value("УТВЕРДИТЬ", None) or tt0.is_value("УТВ", None)))): 
                                    if (l_.begin_char > res.begin_char): 
                                        res.begin_char = l_.begin_char
                                        if (res.end_char < res.begin_char): 
                                            res.end_char = t.end_char
                                        res.is_adopted = True
                    if (len(li) > 0): 
                        tt = li[len(li) - 1].end_token
                        if (tt.is_char(')')): 
                            tt = tt.previous
                        continue
                if (was_typ): 
                    na = DecreeToken.try_attach_name(tt, dr.typ0, True, False)
                    if (na is not None and tt.begin_char > t.begin_char): 
                        tt1 = na.end_token.next0_
                        if (tt1 is not None and tt1.is_char_of(",()")): 
                            tt1 = tt1.next0_
                        if (tt1 is not None and (tt1.end_char < t.end_char)): 
                            if (tt1.is_value("УТВЕРЖДЕННЫЙ", None) or tt1.is_value("УТВЕРДИТЬ", None) or tt1.is_value("УТВ", None)): 
                                tt = tt1
                                continue
                        if (tt.previous is not None and tt.previous.is_char(':') and na.end_char <= res.end_char): 
                            res.begin_char = tt.begin_char
                            break
                        if (tt.previous.end_char > res.begin_char): 
                            res.end_char = tt.previous.end_char
                            break
            return res
        dpr = Utils.asObjectOrNull(t.get_referent(), DecreePartReferent)
        if (dpr is None): 
            return None
        if ((t.previous is not None and t.previous.is_hiphen and (isinstance(t.previous.previous, ReferentToken))) and (isinstance(t.previous.previous.get_referent(), DecreePartReferent))): 
            if (DecreePartReferent.create_range_referent(Utils.asObjectOrNull(t.previous.previous.get_referent(), DecreePartReferent), dpr) is not None): 
                return None
        t1 = t
        has_diap = False
        diap_ref = None
        if ((t.next0_ is not None and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, ReferentToken))) and (isinstance(t.next0_.next0_.get_referent(), DecreePartReferent))): 
            diap = DecreePartReferent.create_range_referent(Utils.asObjectOrNull(dpr, DecreePartReferent), Utils.asObjectOrNull(t.next0_.next0_.get_referent(), DecreePartReferent))
            if (diap is not None): 
                dpr = diap
                has_diap = True
                t1 = t.next0_.next0_
                diap_ref = (Utils.asObjectOrNull(t1, ReferentToken))
        res = CanonicDecreeRefUri._new835(t.kit.sofa.text, dpr, t.begin_char, t1.end_char, has_diap)
        if ((t.previous is not None and t.previous.is_char('(') and t1.next0_ is not None) and t1.next0_.is_char(')')): 
            return res
        tt = t.begin_token
        while tt is not None and tt.end_char <= t.end_char: 
            if (isinstance(tt.get_referent(), DecreeReferent)): 
                if (tt.begin_char > t.begin_char): 
                    res.end_char = tt.previous.end_char
                    if (tt.previous.morph.class0_.is_preposition and tt.previous.previous is not None): 
                        res.end_char = tt.previous.previous.end_char
                elif (tt.end_char < t.end_char): 
                    res.begin_char = tt.begin_char
                break
            tt = tt.next0_
        has_same_before = DecreeHelper.__has_same_decree(t, dpr, True)
        has_same_after = DecreeHelper.__has_same_decree(t, dpr, False)
        ptmin = PartToken.ItemType.PREFIX
        ptmin2 = PartToken.ItemType.PREFIX
        max0_ = 0
        max2 = 0
        for s in dpr.slots: 
            pt = PartToken._get_type_by_attr_name(s.type_name)
            if (pt == PartToken.ItemType.PREFIX): 
                continue
            co = PartToken._get_rank(pt)
            if (co < 1): 
                if (pt == PartToken.ItemType.PART and dpr.find_slot(DecreePartReferent.ATTR_CLAUSE, None, True) is not None): 
                    co = PartToken._get_rank(PartToken.ItemType.PARAGRAPH)
                else: 
                    continue
            if (co > max0_): 
                max2 = max0_
                ptmin2 = ptmin
                max0_ = co
                ptmin = pt
            elif (co > max2): 
                max2 = co
                ptmin2 = pt
        if (ptmin != PartToken.ItemType.PREFIX): 
            tt = t.begin_token
            while tt is not None and tt.end_char <= res.end_char: 
                if (tt.begin_char >= res.begin_char): 
                    pt = PartToken.try_attach(tt, None, False, False)
                    if (pt is not None and pt.typ == ptmin): 
                        res.begin_char = pt.begin_char
                        res.end_char = pt.end_char
                        if (pt.typ == PartToken.ItemType.APPENDIX and pt.end_token.is_value("К", None) and pt.begin_token != pt.end_token): 
                            res.end_char = pt.end_token.previous.end_char
                        if (pt.end_char == t.end_char): 
                            if ((t.next0_ is not None and t.next0_.is_comma_and and (isinstance(t.next0_.next0_, ReferentToken))) and (isinstance(t.next0_.next0_.get_referent(), DecreePartReferent))): 
                                tt1 = t.next0_.next0_.begin_token
                                ok = True
                                if (tt1.chars.is_letter): 
                                    ok = False
                                if (ok): 
                                    for v in pt.values: 
                                        res.begin_char = v.begin_char
                                        res.end_char = v.end_char
                                        break
                        if (not has_diap): 
                            return res
                        break
                tt = tt.next0_
            if (has_diap and diap_ref is not None): 
                tt = diap_ref.begin_token
                while tt is not None and tt.end_char <= diap_ref.end_char: 
                    if (tt.is_char(',')): 
                        break
                    if (tt != diap_ref.begin_token and tt.is_whitespace_before): 
                        break
                    res.end_char = tt.end_char
                    tt = tt.next0_
                return res
        if (((has_same_before or has_same_after)) and ptmin != PartToken.ItemType.PREFIX): 
            tt = t.begin_token
            first_pass3585 = True
            while True:
                if first_pass3585: first_pass3585 = False
                else: tt = tt.next0_
                if (not (tt is not None and tt.end_char <= res.end_char)): break
                if (tt.begin_char >= res.begin_char): 
                    pt = (PartToken.try_attach(tt, None, False, False) if not has_same_before else None)
                    if (pt is not None): 
                        if (pt.typ == ptmin): 
                            for v in pt.values: 
                                res.begin_char = v.begin_char
                                res.end_char = v.end_char
                                return res
                        tt = pt.end_token
                        continue
                    if ((isinstance(tt, NumberToken)) and tt.begin_char == res.begin_char): 
                        res.end_char = tt.end_char
                        while tt is not None and tt.next0_ is not None: 
                            if (not tt.next0_.is_char('.') or tt.is_whitespace_after or tt.next0_.is_whitespace_after): 
                                break
                            if (not (isinstance(tt.next0_.next0_, NumberToken))): 
                                break
                            tt = tt.next0_.next0_
                            res.end_char = tt.end_char
                        if (tt.next0_ is not None and tt.next0_.is_hiphen): 
                            if (isinstance(tt.next0_.next0_, NumberToken)): 
                                tt = tt.next0_.next0_
                                res.end_char = tt.end_char
                                while tt is not None and tt.next0_ is not None: 
                                    if (not tt.next0_.is_char('.') or tt.is_whitespace_after or tt.next0_.is_whitespace_after): 
                                        break
                                    if (not (isinstance(tt.next0_.next0_, NumberToken))): 
                                        break
                                    tt = tt.next0_.next0_
                                    res.end_char = tt.end_char
                            elif (tt.next0_.next0_ is not None and (isinstance(tt.next0_.next0_.get_referent(), DecreePartReferent)) and has_diap): 
                                res.end_char = tt.next0_.next0_.begin_token.end_char
                        return res
                    if (BracketHelper.can_be_start_of_sequence(tt, True, False) and tt.begin_char == res.begin_char and has_same_before): 
                        br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                        if (br is not None and br.end_token.previous == tt.next0_): 
                            res.end_char = br.end_char
                            return res
            return res
        if (not has_same_before and not has_same_after and ptmin != PartToken.ItemType.PREFIX): 
            tt = t.begin_token
            while tt is not None and tt.end_char <= res.end_char: 
                if (tt.begin_char >= res.begin_char): 
                    pts = PartToken.try_attach_list(tt, False, 40)
                    if (pts is None or len(pts) == 0): 
                        break
                    i = 0
                    while i < len(pts): 
                        if (pts[i].typ == ptmin): 
                            res.begin_char = pts[i].begin_char
                            res.end_char = pts[i].end_char
                            tt = pts[i].end_token
                            if (tt.next0_ is not None and tt.next0_.is_hiphen): 
                                if (isinstance(tt.next0_.next0_, NumberToken)): 
                                    res.end_char = tt.next0_.next0_.end_char
                                elif (tt.next0_.next0_ is not None and (isinstance(tt.next0_.next0_.get_referent(), DecreePartReferent)) and has_diap): 
                                    res.end_char = tt.next0_.next0_.begin_token.end_char
                            return res
                        i += 1
                tt = tt.next0_
        return res
    
    @staticmethod
    def __has_same_decree(t : 'Token', dpr : 'DecreePartReferent', before : bool) -> bool:
        if (((t.previous if before else t.next0_)) is None): 
            return False
        t = (((t.previous if before else t.next0_)))
        if (t.is_comma_and or t.morph.class0_.is_conjunction): 
            pass
        else: 
            return False
        t = (((t.previous if before else t.next0_)))
        if (t is None): 
            return False
        dpr0 = Utils.asObjectOrNull(t.get_referent(), DecreePartReferent)
        if (dpr0 is None): 
            return False
        if (dpr0.owner != dpr.owner): 
            return False
        if (dpr0.owner is None): 
            if (dpr0.local_typ != dpr.local_typ): 
                return False
        for s in dpr0.slots: 
            if (PartToken._get_type_by_attr_name(s.type_name) != PartToken.ItemType.PREFIX): 
                if (dpr.find_slot(s.type_name, None, True) is None): 
                    return False
        for s in dpr.slots: 
            if (PartToken._get_type_by_attr_name(s.type_name) != PartToken.ItemType.PREFIX): 
                if (dpr0.find_slot(s.type_name, None, True) is None): 
                    return False
        return True
    
    @staticmethod
    def __out_money(m : 'MoneyReferent') -> str:
        res = str(m)
        res = res.replace('.', ' ').replace("RUR", "руб.").replace("RUB", "руб.")
        return res
    
    @staticmethod
    def check_nds(t : 'Token', nds : float=18, nds_mustbe_money : bool=False) -> 'MetaToken':
        """ Проверка корректности НДС для суммы
        
        Args:
            t(Token): Указывает на значение, для которой должно далее следовать НДС
            nds(float): 
        
        """
        if (t is None or nds <= 0): 
            return None
        m = Utils.asObjectOrNull(t.get_referent(), MoneyReferent)
        if (m is None): 
            return None
        has_nds = False
        has_nds_perc = False
        has_all = False
        incl = False
        m1 = None
        ndst0 = None
        ndst1 = None
        tt = t.next0_
        first_pass3586 = True
        while True:
            if first_pass3586: first_pass3586 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_value("НДС", None)): 
                has_nds = True
                ndst1 = tt
                ndst0 = ndst1
                continue
            if (isinstance(tt, ReferentToken)): 
                m1 = (Utils.asObjectOrNull(tt.get_referent(), MoneyReferent))
                break
            if (isinstance(tt, NumberToken)): 
                ne = NumberHelper.try_parse_number_with_postfix(tt)
                if (ne is not None and ne.ex_typ == NumberExType.PERCENT): 
                    if (math.fabs(ne.real_value - nds) > 0.0001): 
                        ok = False
                        if (has_nds): 
                            ok = True
                        if (ok): 
                            return MetaToken._new836(tt, ne.end_token, "Размер НДС должен быть {0}%, а не {1}%".format(nds, ne.real_value))
                    ndst1 = ne.end_token
                    tt = ndst1
                    has_nds_perc = True
                    continue
            if (tt.is_value("ВСЕГО", None)): 
                has_all = True
                continue
            if (tt.is_value("ТОМ", None) or tt.is_value("ЧИСЛО", None) or tt.is_value("ВКЛЮЧАЯ", None)): 
                incl = True
                continue
            if ((tt.is_value("КРОМЕ", None) or tt.is_value("ТОГО", None) or tt.is_value("РАЗМЕР", None)) or tt.is_value("СУММА", None) or tt.is_value("СТАВКА", None)): 
                continue
            if (((tt.is_value("Т", None) and tt.next0_ is not None and tt.next0_.is_char('.')) and tt.next0_.next0_ is not None and tt.next0_.next0_.is_value("Ч", None)) and tt.next0_.next0_.next0_ is not None and tt.next0_.next0_.next0_.is_char('.')): 
                incl = True
                tt = tt.next0_.next0_.next0_
                continue
            if (not tt.chars.is_letter or tt.morph.class0_.is_preposition): 
                continue
            break
        if (not has_nds): 
            return None
        if (m1 is None): 
            if (nds_mustbe_money): 
                return MetaToken._new836(ndst0, ndst1, "Размер НДС должен быть в денежном выражении")
            return None
        if (has_all): 
            return None
        must_be = m.real_value
        must_be = (must_be * ((nds / (100))))
        if (incl): 
            must_be /= (((1) + ((nds / (100)))))
        dd = must_be * (100)
        dd -= (math.floor(dd))
        dd /= (100)
        must_be -= dd
        if (dd >= 0.005): 
            must_be += 0.01
        real = m1.real_value
        delta = must_be - real
        if (delta < 0): 
            delta = (- delta)
        if (delta > 0.011): 
            if ((delta < 1) and m1.rest == 0 and m.rest == 0): 
                pass
            else: 
                mr = MoneyReferent._new838(m1.currency, must_be)
                return MetaToken._new836(t, tt, "Размер НДС должен быть {0}, а не {1}".format(DecreeHelper.__out_money(mr), DecreeHelper.__out_money(m1)))
        if (incl): 
            return None
        m2 = None
        has_all = False
        tt = tt.next0_
        first_pass3587 = True
        while True:
            if first_pass3587: first_pass3587 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (isinstance(tt, ReferentToken)): 
                m2 = (Utils.asObjectOrNull(tt.get_referent(), MoneyReferent))
                break
            if (not tt.chars.is_letter or tt.morph.class0_.is_preposition): 
                continue
            if (tt.is_value("ВСЕГО", None)): 
                has_all = True
                continue
            if (tt.is_value("НДС", None) or tt.is_value("ВМЕСТЕ", None)): 
                continue
            break
        if (m2 is not None and has_all): 
            must_be = (m.real_value + m1.real_value)
            delta = (must_be - m2.real_value)
            if (delta < 0): 
                delta = (- delta)
            if (delta > 0.01): 
                mr = MoneyReferent._new838(m1.currency, must_be)
                err = "Всего с НДС должно быть {0}, а не {1}".format(DecreeHelper.__out_money(mr), DecreeHelper.__out_money(m2))
                return MetaToken._new836(t, tt, err)
        return None