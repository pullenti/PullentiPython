# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.ner.business.internal.BusinessFactItemTyp import BusinessFactItemTyp
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.business.BusinessFactKind import BusinessFactKind
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class BusinessFactItem(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.typ = BusinessFactItemTyp.BASE
        self.base_kind = BusinessFactKind.UNDEFINED
        self.is_base_passive = False
    
    @staticmethod
    def try_parse(t : 'Token') -> 'BusinessFactItem':
        if (t is None): 
            return None
        res = BusinessFactItem.__try_parse(t)
        if (res is None): 
            return None
        tt = res.end_token.next0_
        first_pass2909 = True
        while True:
            if first_pass2909: first_pass2909 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.morph.class0_.is_preposition): 
                continue
            if (not ((isinstance(tt, TextToken)))): 
                break
            npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0)
            if (npt is None): 
                break
            rr = BusinessFactItem.__try_parse(tt)
            if (rr is not None): 
                if (rr.base_kind == res.base_kind): 
                    pass
                elif (rr.base_kind == BusinessFactKind.GET and res.base_kind == BusinessFactKind.FINANCE): 
                    res.base_kind = rr.base_kind
                else: 
                    break
                res.end_token = rr.end_token
                tt = res.end_token
                continue
            if ((res.base_kind == BusinessFactKind.FINANCE or npt.noun.is_value("РЫНОК", None) or npt.noun.is_value("СДЕЛКА", None)) or npt.noun.is_value("РИНОК", None) or npt.noun.is_value("УГОДА", None)): 
                res.end_token = tt
                continue
            break
        return res
    
    @staticmethod
    def __try_parse(t : 'Token') -> 'BusinessFactItem':
        tok = BusinessFactItem.__m_base_onto.try_parse(t, TerminParseAttr.NO)
        if (tok is None and t.morph.class0_.is_verb and t.next0_ is not None): 
            tok = BusinessFactItem.__m_base_onto.try_parse(t.next0_, TerminParseAttr.NO)
        if (tok is not None): 
            ki = Utils.valToEnum(tok.termin.tag, BusinessFactKind)
            if (ki != BusinessFactKind.UNDEFINED): 
                return BusinessFactItem._new404(t, tok.end_token, BusinessFactItemTyp.BASE, ki, tok.morph, tok.termin.tag2 is not None)
            tt = tok.end_token.next0_
            first_pass2910 = True
            while True:
                if first_pass2910: first_pass2910 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.morph.class0_.is_preposition): 
                    continue
                tok = BusinessFactItem.__m_base_onto.try_parse(tt, TerminParseAttr.NO)
                if (tok is None): 
                    continue
                ki = (Utils.valToEnum(tok.termin.tag, BusinessFactKind))
                if (ki != BusinessFactKind.UNDEFINED): 
                    return BusinessFactItem._new405(t, tok.end_token, BusinessFactItemTyp.BASE, ki, tok.morph)
                tt = tok.end_token
        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
        if (npt is not None): 
            if (((((npt.noun.is_value("АКЦИОНЕР", None) or npt.noun.is_value("ВЛАДЕЛЕЦ", None) or npt.noun.is_value("ВЛАДЕЛИЦА", None)) or npt.noun.is_value("СОВЛАДЕЛЕЦ", None) or npt.noun.is_value("СОВЛАДЕЛИЦА", None)) or npt.noun.is_value("АКЦІОНЕР", None) or npt.noun.is_value("ВЛАСНИК", None)) or npt.noun.is_value("ВЛАСНИЦЯ", None) or npt.noun.is_value("СПІВВЛАСНИК", None)) or npt.noun.is_value("СПІВВЛАСНИЦЯ", None)): 
                return BusinessFactItem._new405(t, npt.end_token, BusinessFactItemTyp.BASE, BusinessFactKind.HAVE, npt.morph)
        if (npt is not None): 
            if ((npt.noun.is_value("ОСНОВАТЕЛЬ", None) or npt.noun.is_value("ОСНОВАТЕЛЬНИЦА", None) or npt.noun.is_value("ЗАСНОВНИК", None)) or npt.noun.is_value("ЗАСНОВНИЦЯ", None)): 
                return BusinessFactItem._new405(t, npt.end_token, BusinessFactItemTyp.BASE, BusinessFactKind.CREATE, npt.morph)
        return None
    
    @staticmethod
    def initialize() -> None:
        if (BusinessFactItem.__m_base_onto is not None): 
            return
        BusinessFactItem.__m_base_onto = TerminCollection()
        for s in ["КУПИТЬ", "ПОКУПАТЬ", "ПРИОБРЕТАТЬ", "ПРИОБРЕСТИ", "ПОКУПКА", "ПРИОБРЕТЕНИЕ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new119(s, BusinessFactKind.GET))
        for s in ["КУПИТИ", "КУПУВАТИ", "КУПУВАТИ", "ПРИДБАТИ", "ПОКУПКА", "ПРИДБАННЯ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new120(s, BusinessFactKind.GET, MorphLang.UA))
        for s in ["ПРОДАТЬ", "ПРОДАВАТЬ", "ПРОДАЖА"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new119(s, BusinessFactKind.SELL))
        for s in ["ПРОДАТИ", "ПРОДАВАТИ", "ПРОДАЖ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new120(s, BusinessFactKind.SELL, MorphLang.UA))
        for s in ["ФИНАНСИРОВАТЬ", "СПОНСИРОВАТЬ", "ПРОФИНАНСИРОВАТЬ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new119(s, BusinessFactKind.FINANCE))
        for s in ["ФІНАНСУВАТИ", "СПОНСОРУВАТИ", "ПРОФІНАНСУВАТИ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new120(s, BusinessFactKind.FINANCE, MorphLang.UA))
        for s in ["ВЛАДЕТЬ", "РАСПОРЯЖАТЬСЯ", "КОНТРОЛИРОВАТЬ", "ПРИНАДЛЕЖАТЬ", "СТАТЬ ВЛАДЕЛЬЦЕМ", "КОНСОЛИДИРОВАТЬ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new119(s, BusinessFactKind.HAVE))
        for s in ["ВОЛОДІТИ", "РОЗПОРЯДЖАТИСЯ", "КОНТРОЛЮВАТИ", "НАЛЕЖАТИ", "СТАТИ ВЛАСНИКОМ", "КОНСОЛІДУВАТИ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new120(s, BusinessFactKind.HAVE, MorphLang.UA))
        for s in ["ПРИНАДЛЕЖАЩИЙ", "КОНТРОЛИРУЕМЫЙ", "ВЛАДЕЕМЫЙ", "ПЕРЕЙТИ ПОД КОНТРОЛЬ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new121(s, BusinessFactKind.HAVE, s))
        for s in ["НАЛЕЖНИЙ", "КОНТРОЛЬОВАНИЙ", "ВЛАДЕЕМЫЙ", "ПЕРЕЙТИ ПІД КОНТРОЛЬ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new417(s, BusinessFactKind.HAVE, s, MorphLang.UA))
        for s in ["ЗАКРЫТЬ СДЕЛКУ", "СОВЕРШИТЬ СДЕЛКУ", "ЗАВЕРШИТЬ СДЕЛКУ", "ЗАКЛЮЧИТЬ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new119(s, BusinessFactKind.UNDEFINED))
        for s in ["ЗАКРИТИ ОПЕРАЦІЮ", "ЗДІЙСНИТИ ОПЕРАЦІЮ", "ЗАВЕРШИТИ ОПЕРАЦІЮ", "УКЛАСТИ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new120(s, BusinessFactKind.UNDEFINED, MorphLang.UA))
        for s in ["ДОХОД", "ПРИБЫЛЬ", "ВЫРУЧКА"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new119(s, BusinessFactKind.PROFIT))
        for s in ["ДОХІД", "ПРИБУТОК", "ВИРУЧКА"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new120(s, BusinessFactKind.PROFIT, MorphLang.UA))
        for s in ["УБЫТОК"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new119(s, BusinessFactKind.DAMAGES))
        for s in ["ЗБИТОК"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new120(s, BusinessFactKind.DAMAGES, MorphLang.UA))
        for s in ["СОГЛАШЕНИЕ", "ДОГОВОР"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new119(s, BusinessFactKind.AGREEMENT))
        for s in ["УГОДА", "ДОГОВІР"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new120(s, BusinessFactKind.AGREEMENT, MorphLang.UA))
        for s in ["ИСК", "СУДЕБНЫЙ ИСК"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new119(s, BusinessFactKind.LAWSUIT))
        for s in ["ПОЗОВ", "СУДОВИЙ ПОЗОВ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new120(s, BusinessFactKind.LAWSUIT, MorphLang.UA))
        for s in ["ДОЧЕРНЕЕ ПРЕДПРИЯТИЕ", "ДОЧЕРНЕЕ ПОДРАЗДЕЛЕНИЕ", "ДОЧЕРНЯЯ КОМПАНИЯ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new119(s, BusinessFactKind.SUBSIDIARY))
        for s in ["ДОЧІРНЄ ПІДПРИЄМСТВО", "ДОЧІРНІЙ ПІДРОЗДІЛ", "ДОЧІРНЯ КОМПАНІЯ"]: 
            BusinessFactItem.__m_base_onto.add(Termin._new120(s, BusinessFactKind.SUBSIDIARY, MorphLang.UA))
    
    __m_base_onto = None
    
    @staticmethod
    def _new404(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'BusinessFactItemTyp', _arg4 : 'BusinessFactKind', _arg5 : 'MorphCollection', _arg6 : bool) -> 'BusinessFactItem':
        res = BusinessFactItem(_arg1, _arg2)
        res.typ = _arg3
        res.base_kind = _arg4
        res.morph = _arg5
        res.is_base_passive = _arg6
        return res
    
    @staticmethod
    def _new405(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'BusinessFactItemTyp', _arg4 : 'BusinessFactKind', _arg5 : 'MorphCollection') -> 'BusinessFactItem':
        res = BusinessFactItem(_arg1, _arg2)
        res.typ = _arg3
        res.base_kind = _arg4
        res.morph = _arg5
        return res