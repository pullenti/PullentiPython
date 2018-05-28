# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.ntopy.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.business.internal.FundsItemTyp import FundsItemTyp
from pullenti.ner.business.FundsKind import FundsKind
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.org.OrganizationKind import OrganizationKind


class FundsItemToken(MetaToken):
    
    def __init__(self, b : 'Token', e0 : 'Token') -> None:
        self.typ = FundsItemTyp.UNDEFINED
        self.kind = FundsKind.UNDEFINED
        self.ref = None
        self.float_val = 0
        self.long_val = 0
        self.string_val = None
        super().__init__(b, e0, None)
    
    def __str__(self) -> str:
        res = Utils.newStringIO(None)
        print(self.typ, end="", file=res)
        if (self.kind != FundsKind.UNDEFINED): 
            print(" K={0}".format(Utils.enumToString(self.kind)), end="", file=res, flush=True)
        if (self.float_val > 0): 
            print(" F={0}".format(self.float_val), end="", file=res, flush=True)
        if (self.long_val > 0): 
            print(" L={0}".format(self.long_val), end="", file=res, flush=True)
        if (self.ref is not None): 
            print(" R={0}".format(str(self.ref)), end="", file=res, flush=True)
        if (self.string_val is not None): 
            print(" S={0}".format(self.string_val), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    __m_act_types = None
    
    @staticmethod
    def try_parse(t : 'Token', prev : 'FundsItemToken'=None) -> 'FundsItemToken':
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
        first_pass2565 = True
        while True:
            if first_pass2565: first_pass2565 = False
            else: tt = tt.next0
            if (not (tt is not None)): break
            if (tt.morph.class0.is_preposition or tt.morph.class0.is_adverb): 
                continue
            if ((tt.is_value("СУММА", None) or tt.is_value("ОКОЛО", None) or tt.is_value("БОЛЕЕ", None)) or tt.is_value("МЕНЕЕ", None) or tt.is_value("СВЫШЕ", None)): 
                continue
            if ((tt.is_value("НОМИНАЛ", None) or tt.is_value("ЦЕНА", None) or tt.is_value("СТОИМОСТЬ", None)) or tt.is_value("СТОИТЬ", None)): 
                typ0 = FundsItemTyp.PRICE
                continue
            if (tt.is_value("НОМИНАЛЬНАЯ", None) or tt.is_value("ОБЩАЯ", None)): 
                continue
            if (tt.is_value("СОСТАВЛЯТЬ", None)): 
                continue
            re = tt.get_referent()
            if (isinstance(re, OrganizationReferent)): 
                return FundsItemToken._new428(t, tt, FundsItemTyp.ORG, re)
            if (isinstance(re, MoneyReferent)): 
                if (typ0 == FundsItemTyp.UNDEFINED): 
                    typ0 = FundsItemTyp.SUM
                if ((tt.next0 is not None and tt.next0.is_value("ЗА", None) and tt.next0.next0 is not None) and ((tt.next0.next0.is_value("АКЦИЯ", None) or tt.next0.next0.is_value("АКЦІЯ", None)))): 
                    typ0 = FundsItemTyp.PRICE
                res = FundsItemToken._new428(t, tt, typ0, re)
                return res
            if (re is not None): 
                break
            npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.noun.is_value("ПАКЕТ", None)): 
                npt = NounPhraseHelper.try_parse(npt.end_token.next0, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                res = None
                if (npt.noun.is_value("АКЦІЯ", None) or npt.noun.is_value("АКЦИЯ", None)): 
                    res = FundsItemToken._new430(t, npt.end_token, FundsItemTyp.NOUN, FundsKind.STOCK)
                    if (len(npt.adjectives) > 0): 
                        for v in FundsItemToken.__m_act_types: 
                            if (npt.adjectives[0].is_value(v, None)): 
                                res.string_val = npt.get_normal_case_text(MorphClass(), True, MorphGender.UNDEFINED, False).lower()
                                if (res.string_val == "голосовавшая акция"): 
                                    res.string_val = "голосующая акция"
                                break
                elif (((npt.noun.is_value("БУМАГА", None) or npt.noun.is_value("ПАПІР", None))) and npt.end_token.previous is not None and ((npt.end_token.previous.is_value("ЦЕННЫЙ", None) or npt.end_token.previous.is_value("ЦІННИЙ", None)))): 
                    res = FundsItemToken._new431(t, npt.end_token, FundsItemTyp.NOUN, FundsKind.STOCK, "ценные бумаги")
                elif (((npt.noun.is_value("КАПИТАЛ", None) or npt.noun.is_value("КАПІТАЛ", None))) and len(npt.adjectives) > 0 and ((npt.adjectives[0].is_value("УСТАВНОЙ", None) or npt.adjectives[0].is_value("УСТАВНЫЙ", None) or npt.adjectives[0].is_value("СТАТУТНИЙ", None)))): 
                    res = FundsItemToken._new430(t, npt.end_token, FundsItemTyp.NOUN, FundsKind.CAPITAL)
                if (res is not None): 
                    rt = res.kit.process_referent(OrganizationAnalyzer.ANALYZER_NAME, res.end_token.next0)
                    if (rt is not None): 
                        res.ref = rt.referent
                        res.end_token = rt.end_token
                    return res
            if (prev is not None and prev.typ == FundsItemTyp.COUNT): 
                val = None
                for v in FundsItemToken.__m_act_types: 
                    if (tt.is_value(v, None)): 
                        val = v
                        break
                if (val is not None): 
                    cou = 0
                    ok = False
                    ttt = tt.previous
                    first_pass2566 = True
                    while True:
                        if first_pass2566: first_pass2566 = False
                        else: ttt = ttt.previous
                        if (not (ttt is not None)): break
                        cou += 1
                        if ((cou) > 100): 
                            break
                        refs = ttt.get_referents()
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
                        ttt = tt.next0
                        while ttt is not None: 
                            cou += 1
                            if ((cou) > 100): 
                                break
                            fi = FundsItemToken.try_parse(ttt, None)
                            if (fi is not None and fi.kind == FundsKind.STOCK): 
                                ok = True
                                break
                            ttt = ttt.next0
                    if (ok): 
                        res = FundsItemToken._new433(t, tt, FundsKind.STOCK, FundsItemTyp.NOUN)
                        res.string_val = "{0}ая акция".format(val[0 : (len(val) - 2)].lower())
                        return res
            if (isinstance(tt, NumberToken)): 
                num = NumberExToken.try_parse_number_with_postfix(tt)
                if (num is not None): 
                    if (tt.previous is not None and tt.previous.is_value("НА", None)): 
                        break
                    if (num.ex_typ == NumberExType.PERCENT): 
                        res = FundsItemToken._new434(t, num.end_token, FundsItemTyp.PERCENT, num.real_value)
                        t = num.end_token.next0
                        if (t is not None and ((t.is_char('+') or t.is_value("ПЛЮС", None))) and isinstance(t.next0, NumberToken)): 
                            res.end_token = t.next0
                            t = res.end_token.next0
                        if ((t is not None and t.is_hiphen and t.next0 is not None) and t.next0.chars.is_all_lower and not t.is_whitespace_after): 
                            t = t.next0.next0
                        if (t is not None and ((t.is_value("ДОЛЯ", None) or t.is_value("ЧАСТКА", None)))): 
                            res.end_token = t
                        return res
                    break
                t1 = tt
                if (t1.next0 is not None and t1.next0.is_value("ШТУКА", None)): 
                    t1 = t1.next0
                return FundsItemToken._new435(t, t1, FundsItemTyp.COUNT, (tt if isinstance(tt, NumberToken) else None).value)
            break
        return None
    
    @staticmethod
    def try_attach(t : 'Token') -> 'ReferentToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.business.FundsReferent import FundsReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        if (t is None): 
            return None
        f = FundsItemToken.try_parse(t, None)
        if (f is None): 
            return None
        if (f.typ == FundsItemTyp.ORG): 
            return None
        if (f.typ == FundsItemTyp.PRICE or f.typ == FundsItemTyp.PERCENT or f.typ == FundsItemTyp.COUNT): 
            if (t.previous is not None and t.previous.is_char_of(",.") and isinstance(t.previous.previous, NumberToken)): 
                return None
        li = list()
        li.append(f)
        is_in_br = False
        tt = f.end_token.next0
        first_pass2567 = True
        while True:
            if first_pass2567: first_pass2567 = False
            else: tt = tt.next0
            if (not (tt is not None)): break
            if ((tt.is_whitespace_before and tt.previous is not None and tt.previous.is_char('.')) and tt.chars.is_capital_upper): 
                break
            f0 = FundsItemToken.try_parse(tt, f)
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
            if (tt.is_char('(')): 
                is_in_br = True
                continue
            if (tt.is_char(')')): 
                if (is_in_br or ((t.previous is not None and t.previous.is_char('(')))): 
                    is_in_br = False
                    li[len(li) - 1].end_token = tt
                    continue
            if (tt.morph.class0.is_verb or tt.morph.class0.is_adverb): 
                continue
            break
        funds = FundsReferent()
        res = ReferentToken(funds, t, t)
        org_prob = None
        for i in range(len(li)):
            if (li[i].typ == FundsItemTyp.NOUN): 
                funds.kind = li[i].kind
                if (li[i].string_val is not None): 
                    funds.typ = li[i].string_val
                if (isinstance(li[i].ref, OrganizationReferent)): 
                    org_prob = (li[i].ref if isinstance(li[i].ref, OrganizationReferent) else None)
                res.end_token = li[i].end_token
            elif (li[i].typ == FundsItemTyp.COUNT): 
                if (funds.count > 0 or li[i].long_val == 0): 
                    break
                funds.count = li[i].long_val
                res.end_token = li[i].end_token
            elif (li[i].typ == FundsItemTyp.ORG): 
                if (funds.source is not None and funds.source != li[i].ref): 
                    break
                funds.source = (li[i].ref if isinstance(li[i].ref, OrganizationReferent) else None)
                res.end_token = li[i].end_token
            elif (li[i].typ == FundsItemTyp.PERCENT): 
                if (funds.percent > 0 or li[i].float_val == 0): 
                    break
                funds.percent = li[i].float_val
                res.end_token = li[i].end_token
            elif (li[i].typ == FundsItemTyp.SUM): 
                if (funds.sum0 is not None): 
                    break
                funds.sum0 = (li[i].ref if isinstance(li[i].ref, MoneyReferent) else None)
                res.end_token = li[i].end_token
            elif (li[i].typ == FundsItemTyp.PRICE): 
                if (funds.price is not None): 
                    break
                funds.price = (li[i].ref if isinstance(li[i].ref, MoneyReferent) else None)
                res.end_token = li[i].end_token
            else: 
                break
        if (funds.percent > 0 and funds.source is not None and funds.kind == FundsKind.UNDEFINED): 
            funds.kind = FundsKind.STOCK
        if (not funds._check_correct()): 
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
                fr = (tt.get_referent() if isinstance(tt.get_referent(), FundsReferent) else None)
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
                refs = tt.get_referents()
                if (refs is not None): 
                    for r in refs: 
                        if (isinstance(r, OrganizationReferent)): 
                            ki = (r if isinstance(r, OrganizationReferent) else None).kind
                            if (ki == OrganizationKind.JUSTICE or ki == OrganizationKind.GOVENMENT): 
                                continue
                            funds.source = (r if isinstance(r, OrganizationReferent) else None)
                            cou = 10000
                            break
                tt = tt.previous
        return res

    
    @staticmethod
    def _new428(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FundsItemTyp', _arg4 : 'Referent') -> 'FundsItemToken':
        res = FundsItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        return res
    
    @staticmethod
    def _new430(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FundsItemTyp', _arg4 : 'FundsKind') -> 'FundsItemToken':
        res = FundsItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.kind = _arg4
        return res
    
    @staticmethod
    def _new431(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FundsItemTyp', _arg4 : 'FundsKind', _arg5 : str) -> 'FundsItemToken':
        res = FundsItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.kind = _arg4
        res.string_val = _arg5
        return res
    
    @staticmethod
    def _new433(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FundsKind', _arg4 : 'FundsItemTyp') -> 'FundsItemToken':
        res = FundsItemToken(_arg1, _arg2)
        res.kind = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new434(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FundsItemTyp', _arg4 : float) -> 'FundsItemToken':
        res = FundsItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.float_val = _arg4
        return res
    
    @staticmethod
    def _new435(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'FundsItemTyp', _arg4 : int) -> 'FundsItemToken':
        res = FundsItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.long_val = _arg4
        return res
    
    # static constructor for class FundsItemToken
    @staticmethod
    def _static_ctor():
        FundsItemToken.__m_act_types = list(["ОБЫКНОВЕННЫЙ", "ПРИВИЛЕГИРОВАННЫЙ", "ГОЛОСУЮЩИЙ", "ЗВИЧАЙНИЙ", "ПРИВІЛЕЙОВАНОГО", "ГОЛОСУЄ"])

FundsItemToken._static_ctor()