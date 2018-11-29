# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.Referent import Referent
from pullenti.ner.business.FundsKind import FundsKind


class FundsReferent(Referent):
    """ Ценные бумаги (акции, доли в уставном капитале и пр.) """
    
    def __init__(self) -> None:
        from pullenti.ner.business.internal.FundsMeta import FundsMeta
        super().__init__(FundsReferent.OBJ_TYPENAME)
        self.instance_of = FundsMeta.GLOBAL_META
    
    OBJ_TYPENAME = "FUNDS"
    
    ATTR_KIND = "KIND"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_SOURCE = "SOURCE"
    
    ATTR_PERCENT = "PERCENT"
    
    ATTR_COUNT = "COUNT"
    
    ATTR_SUM = "SUM"
    
    ATTR_PRICE = "PRICE"
    
    def toString(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.business.internal.FundsMeta import FundsMeta
        from pullenti.morph.MorphLang import MorphLang
        res = io.StringIO()
        if (self.typ is not None): 
            print(MiscHelper.convertFirstCharUpperAndOtherLower(self.typ), end="", file=res)
        else: 
            kind_ = self.getStringValue(FundsReferent.ATTR_KIND)
            if (kind_ is not None): 
                kind_ = (Utils.asObjectOrNull(FundsMeta.GLOBAL_META.kind_feature.convertInnerValueToOuterValue(kind_, MorphLang()), str))
            if (kind_ is not None): 
                print(MiscHelper.convertFirstCharUpperAndOtherLower(kind_), end="", file=res)
            else: 
                print("?", end="", file=res)
        if (self.source is not None): 
            print("; {0}".format(self.source.toString(short_variant, lang, 0)), end="", file=res, flush=True)
        if (self.count > (0)): 
            print("; кол-во {0}".format(self.count), end="", file=res, flush=True)
        if (self.percent > 0): 
            print("; {0}%".format(self.percent), end="", file=res, flush=True)
        if (not short_variant): 
            if (self.sum0_ is not None): 
                print("; {0}".format(self.sum0_.toString(False, lang, 0)), end="", file=res, flush=True)
            if (self.price is not None): 
                print("; номинал {0}".format(self.price.toString(False, lang, 0)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def parent_referent(self) -> 'Referent':
        return self.source
    
    @property
    def kind(self) -> 'FundsKind':
        """ Классификатор ценной бумаги """
        s = self.getStringValue(FundsReferent.ATTR_KIND)
        if (s is None): 
            return FundsKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, FundsKind)
            if (isinstance(res, FundsKind)): 
                return Utils.valToEnum(res, FundsKind)
        except Exception as ex450: 
            pass
        return FundsKind.UNDEFINED
    @kind.setter
    def kind(self, value) -> 'FundsKind':
        if (value != FundsKind.UNDEFINED): 
            self.addSlot(FundsReferent.ATTR_KIND, Utils.enumToString(value), True, 0)
        else: 
            self.addSlot(FundsReferent.ATTR_KIND, None, True, 0)
        return value
    
    @property
    def source(self) -> 'OrganizationReferent':
        """ Эмитент """
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        return Utils.asObjectOrNull(self.getSlotValue(FundsReferent.ATTR_SOURCE), OrganizationReferent)
    @source.setter
    def source(self, value) -> 'OrganizationReferent':
        self.addSlot(FundsReferent.ATTR_SOURCE, value, True, 0)
        return value
    
    @property
    def typ(self) -> str:
        """ Тип (например, привелигированная акция) """
        return self.getStringValue(FundsReferent.ATTR_TYPE)
    @typ.setter
    def typ(self, value) -> str:
        self.addSlot(FundsReferent.ATTR_TYPE, value, True, 0)
        return value
    
    @property
    def percent(self) -> float:
        """ Процент от общего количества """
        val = self.getStringValue(FundsReferent.ATTR_PERCENT)
        if (val is None): 
            return 0
        wrapf453 = RefOutArgWrapper(0)
        inoutres454 = Utils.tryParseFloat(val, wrapf453)
        f = wrapf453.value
        if (not inoutres454): 
            wrapf451 = RefOutArgWrapper(0)
            inoutres452 = Utils.tryParseFloat(val.replace('.', ','), wrapf451)
            f = wrapf451.value
            if (not inoutres452): 
                return 0
        return f
    @percent.setter
    def percent(self, value) -> float:
        if (value > 0): 
            self.addSlot(FundsReferent.ATTR_PERCENT, str(value).replace(',', '.'), True, 0)
        else: 
            self.addSlot(FundsReferent.ATTR_PERCENT, None, True, 0)
        return value
    
    @property
    def count(self) -> int:
        """ Количество """
        val = self.getStringValue(FundsReferent.ATTR_COUNT)
        if (val is None): 
            return 0
        wrapv455 = RefOutArgWrapper(0)
        inoutres456 = Utils.tryParseInt(val, wrapv455)
        v = wrapv455.value
        if (not inoutres456): 
            return 0
        return v
    @count.setter
    def count(self, value) -> int:
        self.addSlot(FundsReferent.ATTR_COUNT, str(value), True, 0)
        return value
    
    @property
    def sum0_(self) -> 'MoneyReferent':
        """ Сумма за все акции """
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        return Utils.asObjectOrNull(self.getSlotValue(FundsReferent.ATTR_SUM), MoneyReferent)
    @sum0_.setter
    def sum0_(self, value) -> 'MoneyReferent':
        self.addSlot(FundsReferent.ATTR_SUM, value, True, 0)
        return value
    
    @property
    def price(self) -> 'MoneyReferent':
        """ Сумма за одну акцию """
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        return Utils.asObjectOrNull(self.getSlotValue(FundsReferent.ATTR_PRICE), MoneyReferent)
    @price.setter
    def price(self, value) -> 'MoneyReferent':
        self.addSlot(FundsReferent.ATTR_PRICE, value, True, 0)
        return value
    
    def canBeEquals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        f = Utils.asObjectOrNull(obj, FundsReferent)
        if (f is None): 
            return False
        if (self.kind != f.kind): 
            return False
        if (self.typ is not None and f.typ is not None): 
            if (self.typ != f.typ): 
                return False
        if (self.source != f.source): 
            return False
        if (self.count != f.count): 
            return False
        if (self.percent != f.percent): 
            return False
        if (self.sum0_ != f.sum0_): 
            return False
        return True
    
    def _checkCorrect(self) -> bool:
        if (self.kind == FundsKind.UNDEFINED): 
            return False
        for s in self.slots: 
            if (s.type_name != FundsReferent.ATTR_TYPE and s.type_name != FundsReferent.ATTR_KIND): 
                return True
        return False