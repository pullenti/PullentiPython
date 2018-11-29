# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.business.internal.FundsItemTyp import FundsItemTyp
from pullenti.ner.business.FundsKind import FundsKind
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.org.OrganizationKind import OrganizationKind


class FundsItemToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.typ = FundsItemTyp.UNDEFINED
        self.kind = FundsKind.UNDEFINED
        self.ref = None
        self.float_val = 0
        self.long_val = 0
        self.string_val = None;
    
    def __str__(self) -> str:
        res = io.StringIO()
        print(self.typ, end="", file=res)
        if (self.kind != FundsKind.UNDEFINED): 
            print(" K={0}".format(Utils.enumToString(self.kind)), end="", file=res, flush=True)
        if (self.float_val > 0): 
            print(" F={0}".format(self.float_val), end="", file=res, flush=True)
        if (self.long_val > (0)): 
            print(" L={0}".format(self.long_val), end="", file=res, flush=True)
        if (self.ref is not None): 
            print(" R={0}".format(str(self.ref)), end="", file=res, flush=True)
        if (self.string_val is not None): 
            print(" S={0}".format(self.string_val), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    __m_act_types = None
    
    @staticmethod
    def tryParse(t : 'Token', prev : 'FundsItemToken'=None) -> 'FundsItemToken':
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.org.OrganizationAnalyzer import OrganizationAnalyzer
        from pullenti.ner.business.FundsReferent import FundsReferent
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.NumberExToken import NumberExToken
        if (t is None): 
            return None
        typ0 = FundsItemTyp.UNDEFINED
        tt = t
        first_pass2775 = True
        while True:
            if first_pass2775: first_pass2775 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.morph.class0_.is_preposition or tt.morph.class0_.is_adverb): 
                continue
            if ((tt.isValue("СУММА", None) or tt.isValue("ОКОЛО", None) or tt.isValue("БОЛЕЕ", None)) or tt.isValue("МЕНЕЕ", None) or tt.isValue("СВЫШЕ", None)): 
                continue
            if ((tt.isValue("НОМИНАЛ", None) or tt.isValue("ЦЕНА", None) or tt.isValue("СТОИМОСТЬ", None)) or tt.isValue("СТОИТЬ", None)): 
                typ0 = FundsItemTyp.PRICE
                continue
            if (tt.isValue("НОМИНАЛЬНАЯ", None) or tt.isValue("ОБЩАЯ", None)): 
                continue
            if (tt.isValue("СОСТАВЛЯТЬ", None)): 
                continue
            re = tt.getReferent()
            if (isinstance(re, OrganizationReferent)): 
                return FundsItemToken._new429(t, tt, FundsItemTyp.ORG, re)
            if (isinstance(re, MoneyReferent)): 
                if (typ0 == FundsItemTyp.UNDEFINED): 
                    typ0 = FundsItemTyp.SUM
                if ((tt.next0_ is not None and tt.next0_.isValue("ЗА", None) and tt.next0_.next0_ is not None) and ((tt.next0_.next0_.isValue("АКЦИЯ", None) or tt.next0_.next0_.isValue("АКЦІЯ", None)))): 
                    typ0 = FundsItemTyp.PRICE
                res = FundsItemToken._new429(t, tt, typ0, re)
                return res
            if (re is not None): 
                break
            npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.noun.isValue("ПАКЕТ", None)): 
                npt = NounPhraseHelper.tryParse(npt.end_token.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                res = None
                if (npt.noun.isValue("АКЦІЯ", None) or npt.noun.isValue("АКЦИЯ", None)): 
                    res = FundsItemToken._new431(t, npt.end_token, FundsItemTyp.NOUN, FundsKind.STOCK)
                    if (len(npt.adjectives) > 0): 
                        for v in FundsItemToken.__m_act_types: 
                            if (npt.adjectives[0].isValue(v, None)): 
                                res.string_val = npt.getNormalCaseText(MorphClass(), True, MorphGender.UNDEFINED, False).lower()
                                if (res.string_val == "голосовавшая акция"): 
                                    res.string_val = "голосующая акция"
                                break
                elif (((npt.noun.isValue("БУМАГА", None) or npt.noun.isValue("ПАПІР", None))) and npt.end_token.previous is not None and ((npt.end_token.previous.isValue("ЦЕННЫЙ", None) or npt.end_token.previous.isValue("ЦІННИЙ", None)))): 
                    res = FundsItemToken._new432(t, npt.end_token, FundsItemTyp.NOUN, FundsKind.STOCK, "ценные бумаги")
                elif (((npt.noun.isValue("КАПИТАЛ", None) or npt.noun.isValue("КАПІТАЛ", None))) and len(npt.adjectives) > 0 and ((npt.adjectives[0].isValue("УСТАВНОЙ", None) or npt.adjectives[0].isValue("УСТАВНЫЙ", None) or npt.adjectives[0].isValue("СТАТУТНИЙ", None)))): 
                    res = FundsItemToken._new431(t, npt.end_token, FundsItemTyp.NOUN, FundsKind.CAPITAL)
                if (res is not None): 
                    rt = res.kit.processReferent(OrganizationAnalyzer.ANALYZER_NAME, res.end_token.next0_)
                    if (rt is not None): 
                        res.ref = rt.referent
                        res.end_token = rt.end_token
                    return res
            if (prev is not None and prev.typ == FundsItemTyp.COUNT): 
                val = None
                for v in FundsItemToken.__m_act_types: 
                    if (tt.isValue(v, None)): 
                        val = v
                        break
                if (val is not None): 
                    cou = 0
                    ok = False
                    ttt = tt.previous
                    first_pass2776 = True
                    while True:
                        if first_pass2776: first_pass2776 = False
                        else: ttt = ttt.previous
                        if (not (ttt is not None)): break
                        cou += 1
                        if ((cou) > 100): 
                            break
                        refs = ttt.getReferents()
                        if (refs is None): 
                            continue
                        for r in refs: 
                            if (isinstance(r, FundsReferent)): 
                                ok = True
                                break
                        if (ok): 
                            break
                    cou = 0
                    if (not ok): 
                        ttt = tt.next0_
                        while ttt is not None: 
                            cou += 1
                            if ((cou) > 100): 
                                break
                            fi = FundsItemToken.tryParse(ttt, None)
                            if (fi is not None and fi.kind == FundsKind.STOCK): 
                                ok = True
                                break
                            ttt = ttt.next0_
                    if (ok): 
                        res = FundsItemToken._new434(t, tt, FundsKind.STOCK, FundsItemTyp.NOUN)
                        res.string_val = "{0}ая акция".format(val[0:0+len(val) - 2].lower())
                        return res
            if (isinstance(tt, NumberToken)): 
                num = NumberExToken.tryParseNumberWithPostfix(tt)
                if (num is not None): 
                    if (tt.previous is not None and tt.previous.isValue("НА", None)): 
                        break
                    if (num.ex_typ == NumberExType.PERCENT): 
                        res = FundsItemToken._new435(t, num.end_token, FundsItemTyp.PERCENT, num.real_value)
                        t = num.end_token.next0_
                        if (t is not None and ((t.isChar('+') or t.isValue("ПЛЮС", None))) and (isinstance(t.next0_, NumberToken))): 
                            res.end_token = t.next0_
                            t = res.end_token.next0_
                        if ((t is not None and t.is_hiphen and t.next0_ is not None) and t.next0_.chars.is_all_lower and not t.is_whitespace_after): 
                            t = t.next0_.next0_
                        if (t is not None and ((t.isValue("ДОЛЯ", None) or t.isValue("ЧАСТКА", None)))): 
                            res.end_token = t
                        return res
                    break
                t1 = tt
                if (t1.next0_ is not None and t1.next0_.isValue("ШТУКА", None)): 
                    t1 = t1.next0_
                return FundsItemToken._new436(t, t1, FundsItemTyp.COUNT, (Utils.asObjectOrNull(tt, NumberToken)).value)
            break
        return None
    
    @staticmethod
    def tryAttach(t : 'Token') -> 'ReferentToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.business.FundsReferent import FundsReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        if (t is None): 
            return None
        f = FundsItemToken.tryParse(t, None)
        if (f is None): 
            return None
        if (f.typ == FundsItemTyp.ORG): 
            return None
        if (f.typ == FundsItemTyp.PRICE or f.typ == FundsItemTyp.PERCENT or f.typ == FundsItemTyp.COUNT): 
            if (t.previous is not None and t.previous.isCharOf(",.") and (isinstance(t.previous.previous, NumberToken))): 
                return None
        li = list()
        li.append(f)
        is_in_br = False
        tt = f.end_token.next0_
        first_pass2777 = True
        while True:
            if first_pass2777: first_pass2777 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if ((tt.is_whitespace_before and tt.previous is not None and tt.previous.isChar('.')) and tt.chars.is_capital_upper): 
                break
            f0 = FundsItemToken.tryParse(tt, f)
            if (f0 is not None): 
                if (f0.kind == FundsKind.CAPITAL and is_in_br): 
                    for l_ in li: 
                        if (l_.typ == FundsItemTyp.NOUN): 
                            f0.kind = l_.kind
                            break
                f = f0
                li.append(f)
                tt = f.end_token
                continue
            if (tt.isChar('(')): 
                is_in_br = True
                continue
            if (tt.isChar(')')): 
                if (is_in_br or ((t.previous is not None and t.previous.isChar('(')))): 
                    is_in_br = False
                    li[len(li) - 1].end_token = tt
                    continue
            if (tt.morph.class0_.is_verb or tt.morph.class0_.is_adverb): 
                continue
            break
        funds = FundsReferent()
        res = ReferentToken(funds, t, t)
        org_prob = None
        i = 0
        while i < len(li): 
            if (li[i].typ == FundsItemTyp.NOUN): 
                funds.kind = li[i].kind
                if (li[i].string_val is not None): 
                    funds.typ = li[i].string_val
                if (isinstance(li[i].ref, OrganizationReferent)): 
                    org_prob = (Utils.asObjectOrNull(li[i].ref, OrganizationReferent))
                res.end_token = li[i].end_token
            elif (li[i].typ == FundsItemTyp.COUNT): 
                if (funds.count > (0) or li[i].long_val == (0)): 
                    break
                funds.count = li[i].long_val
                res.end_token = li[i].end_token
            elif (li[i].typ == FundsItemTyp.ORG): 
                if (funds.source is not None and funds.source != li[i].ref): 
                    break
                funds.source = Utils.asObjectOrNull(li[i].ref, OrganizationReferent)
                res.end_token = li[i].end_token
            elif (li[i].typ == FundsItemTyp.PERCENT): 
                if (funds.percent > 0 or li[i].float_val == 0): 
                    break
                funds.percent = li[i].float_val
                res.end_token = li[i].end_token
            elif (li[i].typ == FundsItemTyp.SUM): 
                if (funds.sum0_ is not None): 
                    break
                funds.sum0_ = Utils.asObjectOrNull(li[i].ref, MoneyReferent)
                res.end_token = li[i].end_token
            elif (li[i].typ == FundsItemTyp.PRICE): 
                if (funds.price is not None): 
                    break
                funds.price = Utils.asObjectOrNull(li[i].ref, MoneyReferent)
                res.end_token = li[i].end_token
            else: 
                break
            i += 1
        if (funds.percent > 0 and funds.source is not None and funds.kind == FundsKind.UNDEFINED): 
            funds.kind = FundsKind.STOCK
        if (not funds._checkCorrect()): 
            return None
        if (funds.source is None): 
            cou = 0
            tt = res.begin_token.previous
            while tt is not None: 
                cou += 1
                if ((cou) > 500): 
                    break
                if (tt.is_newline_after): 
                    cou += 10
                fr = Utils.asObjectOrNull(tt.getReferent(), FundsReferent)
                if (fr is not None and fr.source is not None): 
                    funds.source = fr.source
                    break
                tt = tt.previous
        if (funds.source is None and org_prob is not None): 
            funds.source = org_prob
        if (funds.source is None): 
            cou = 0
            tt = res.begin_token.previous
            while tt is not None: 
                cou += 1
                if ((cou) > 300): 
                    break
                if (tt.is_newline_after): 
                    cou += 10
                refs = tt.getReferents()
                if (refs is not None): 
                    for r in refs: 
                        if (isinstance(r, OrganizationReferent)): 
                            ki = (Utils.asObjectOrNull(r, OrganizationReferent)).kind
                            if (ki == OrganizationKind.JUSTICE or ki == OrganizationKind.GOVENMENT): 
                                continue
                            funds.source = Utils.asObjectOrNull(r, OrganizationReferent)
                            cou = 10000
                            break
                tt = tt.previous
        return res
    
    @staticmethod
    def _new429(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FundsItemTyp', _arg4 : 'Referent') -> 'FundsItemToken':
        res = FundsItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        return res
    
    @staticmethod
    def _new431(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FundsItemTyp', _arg4 : 'FundsKind') -> 'FundsItemToken':
        res = FundsItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.kind = _arg4
        return res
    
    @staticmethod
    def _new432(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FundsItemTyp', _arg4 : 'FundsKind', _arg5 : str) -> 'FundsItemToken':
        res = FundsItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.kind = _arg4
        res.string_val = _arg5
        return res
    
    @staticmethod
    def _new434(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FundsKind', _arg4 : 'FundsItemTyp') -> 'FundsItemToken':
        res = FundsItemToken(_arg1, _arg2)
        res.kind = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new435(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FundsItemTyp', _arg4 : float) -> 'FundsItemToken':
        res = FundsItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.float_val = _arg4
        return res
    
    @staticmethod
    def _new436(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FundsItemTyp', _arg4 : int) -> 'FundsItemToken':
        res = FundsItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.long_val = _arg4
        return res
    
    # static constructor for class FundsItemToken
    @staticmethod
    def _static_ctor():
        FundsItemToken.__m_act_types = list(["ОБЫКНОВЕННЫЙ", "ПРИВИЛЕГИРОВАННЫЙ", "ГОЛОСУЮЩИЙ", "ЗВИЧАЙНИЙ", "ПРИВІЛЕЙОВАНОГО", "ГОЛОСУЄ"])

FundsItemToken._static_ctor()