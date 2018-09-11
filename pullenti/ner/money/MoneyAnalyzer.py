# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
import math
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.bank.internal.ResourceHelper import ResourceHelper
from pullenti.ner.core.NumberExType import NumberExType


class MoneyAnalyzer(Analyzer):
    """ Анализатор для денежных сумм """
    
    ANALYZER_NAME = "MONEY"
    
    @property
    def name(self) -> str:
        return MoneyAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Деньги"
    
    @property
    def description(self) -> str:
        return "Деньги..."
    
    def clone(self) -> 'Analyzer':
        return MoneyAnalyzer()
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        from pullenti.ner.money.internal.MoneyMeta import MoneyMeta
        return [MoneyMeta.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        from pullenti.ner.money.internal.MoneyMeta import MoneyMeta
        res = dict()
        res[MoneyMeta.IMAGE_ID] = ResourceHelper.get_bytes("money2.png")
        res[MoneyMeta.IMAGE2ID] = ResourceHelper.get_bytes("moneyerr.png")
        return res
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["GEO"]
    
    def create_referent(self, type0_ : str) -> 'Referent':
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        if (type0_ == MoneyReferent.OBJ_TYPENAME): 
            return MoneyReferent()
        return None
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.get_analyzer_data(self)
        t = kit.first_token
        first_pass3940 = True
        while True:
            if first_pass3940: first_pass3940 = False
            else: t = t.next0_
            if (not (t is not None)): break
            mon = MoneyAnalyzer.try_parse(t)
            if (mon is not None): 
                mon.referent = ad.register_referent(mon.referent)
                kit.embed_token(mon)
                t = (mon)
                continue
    
    @staticmethod
    def try_parse(t : 'Token') -> 'ReferentToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.NumberExToken import NumberExToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.Referent import Referent
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (t is None): 
            return None
        if (not ((isinstance(t, NumberToken))) and t.length_char != 1): 
            return None
        nex = NumberExToken.try_parse_number_with_postfix(t)
        if (nex is None or nex.ex_typ != NumberExType.MONEY): 
            if ((isinstance(t, NumberToken)) and (isinstance(t.next0_, TextToken)) and (isinstance(t.next0_.next0_, NumberToken))): 
                if (t.next0_.is_hiphen or t.next0_.morph.class0_.is_preposition): 
                    res1 = NumberExToken.try_parse_number_with_postfix(t.next0_.next0_)
                    if (res1 is not None and res1.ex_typ == NumberExType.MONEY): 
                        res0 = MoneyReferent()
                        if ((t.next0_.is_hiphen and res1.value == (0) and res1.end_token.next0_ is not None) and res1.end_token.next0_.is_char('(')): 
                            nex2 = NumberExToken.try_parse_number_with_postfix(res1.end_token.next0_.next0_)
                            if ((nex2 is not None and nex2.ex_typ_param == res1.ex_typ_param and nex2.end_token.next0_ is not None) and nex2.end_token.next0_.is_char(')')): 
                                if (nex2.value == (t if isinstance(t, NumberToken) else None).value): 
                                    res0.currency = nex2.ex_typ_param
                                    res0.value = nex2.value
                                    return ReferentToken(res0, t, nex2.end_token.next0_)
                                if (isinstance(t.previous, NumberToken)): 
                                    if (nex2.value == ((((t.previous if isinstance(t.previous, NumberToken) else None).value * (1000)) + (t if isinstance(t, NumberToken) else None).value))): 
                                        res0.currency = nex2.ex_typ_param
                                        res0.value = nex2.value
                                        return ReferentToken(res0, t.previous, nex2.end_token.next0_)
                                    elif (isinstance(t.previous.previous, NumberToken)): 
                                        if (nex2.value == ((((t.previous.previous if isinstance(t.previous.previous, NumberToken) else None).value * (1000000)) + ((t.previous if isinstance(t.previous, NumberToken) else None).value * (1000)) + (t if isinstance(t, NumberToken) else None).value))): 
                                            res0.currency = nex2.ex_typ_param
                                            res0.value = nex2.value
                                            return ReferentToken(res0, t.previous.previous, nex2.end_token.next0_)
                        res0.currency = res1.ex_typ_param
                        res0.value = (t if isinstance(t, NumberToken) else None).value
                        return ReferentToken(res0, t, t)
            return None
        res = MoneyReferent()
        res.currency = nex.ex_typ_param
        res.value = (math.floor(nex.real_value))
        re = round(((nex.real_value - (res.value))) * (100), 6)
        res.rest = (math.floor(re))
        if (nex.real_value != nex.alt_real_value): 
            if (res.value != (math.floor(nex.alt_real_value))): 
                res.alt_value = (math.floor(nex.alt_real_value))
            re = (round(((nex.alt_real_value - (math.floor(nex.alt_real_value)))) * (100), 6))
            if ((math.floor(re)) != res.rest): 
                res.alt_rest = (math.floor(re))
        if (nex.alt_rest_money > 0): 
            res.alt_rest = nex.alt_rest_money
        t1 = nex.end_token
        if (t1.next0_ is not None and t1.next0_.is_char('(')): 
            rt = MoneyAnalyzer.try_parse(t1.next0_.next0_)
            if ((rt is not None and rt.referent.can_be_equals(res, Referent.EqualType.WITHINONETEXT) and rt.end_token.next0_ is not None) and rt.end_token.next0_.is_char(')')): 
                t1 = rt.end_token.next0_
            else: 
                rt = MoneyAnalyzer.try_parse(t1.next0_)
                if (rt is not None and rt.referent.can_be_equals(res, Referent.EqualType.WITHINONETEXT)): 
                    t1 = rt.end_token
        if (res.alt_value is not None and res.alt_value > res.value): 
            if (t.whitespaces_before_count == 1 and (isinstance(t.previous, NumberToken))): 
                delt = res.alt_value - res.value
                val = (t.previous if isinstance(t.previous, NumberToken) else None).value
                if ((((res.value < (1000)) and ((delt % (1000))) == (0))) or (((res.value < (1000000)) and ((delt % (1000000))) == (0)))): 
                    t = t.previous
                    res.value = res.alt_value
                    res.alt_value = None
        return ReferentToken(res, t, t1)
    
    def _process_referent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        return MoneyAnalyzer.try_parse(begin)
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.ProcessorService import ProcessorService
        ProcessorService.register_analyzer(MoneyAnalyzer())