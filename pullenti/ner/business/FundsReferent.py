# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.Referent import Referent
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.business.FundsKind import FundsKind
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.money.MoneyReferent import MoneyReferent
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.business.internal.FundsMeta import FundsMeta
from pullenti.ner.core.MiscHelper import MiscHelper

class FundsReferent(Referent):
    """ Ценные бумаги (акции, доли в уставном капитале и пр.) """
    
    def __init__(self) -> None:
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
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        if (self.typ is not None): 
            print(MiscHelper.convert_first_char_upper_and_other_lower(self.typ), end="", file=res)
        else: 
            kind_ = self.get_string_value(FundsReferent.ATTR_KIND)
            if (kind_ is not None): 
                kind_ = (Utils.asObjectOrNull(FundsMeta.GLOBAL_META.kind_feature.convert_inner_value_to_outer_value(kind_, None), str))
            if (kind_ is not None): 
                print(MiscHelper.convert_first_char_upper_and_other_lower(kind_), end="", file=res)
            else: 
                print("?", end="", file=res)
        if (self.source is not None): 
            print("; {0}".format(self.source.to_string(short_variant, lang, 0)), end="", file=res, flush=True)
        if (self.count > 0): 
            print("; кол-во {0}".format(self.count), end="", file=res, flush=True)
        if (self.percent > 0): 
            print("; {0}%".format(self.percent), end="", file=res, flush=True)
        if (not short_variant): 
            if (self.sum0_ is not None): 
                print("; {0}".format(self.sum0_.to_string(False, lang, 0)), end="", file=res, flush=True)
            if (self.price is not None): 
                print("; номинал {0}".format(self.price.to_string(False, lang, 0)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def parent_referent(self) -> 'Referent':
        return self.source
    
    @property
    def kind(self) -> 'FundsKind':
        """ Классификатор ценной бумаги """
        s = self.get_string_value(FundsReferent.ATTR_KIND)
        if (s is None): 
            return FundsKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, FundsKind)
            if (isinstance(res, FundsKind)): 
                return Utils.valToEnum(res, FundsKind)
        except Exception as ex466: 
            pass
        return FundsKind.UNDEFINED
    @kind.setter
    def kind(self, value) -> 'FundsKind':
        if (value != FundsKind.UNDEFINED): 
            self.add_slot(FundsReferent.ATTR_KIND, Utils.enumToString(value), True, 0)
        else: 
            self.add_slot(FundsReferent.ATTR_KIND, None, True, 0)
        return value
    
    @property
    def source(self) -> 'OrganizationReferent':
        """ Эмитент """
        return Utils.asObjectOrNull(self.get_slot_value(FundsReferent.ATTR_SOURCE), OrganizationReferent)
    @source.setter
    def source(self, value) -> 'OrganizationReferent':
        self.add_slot(FundsReferent.ATTR_SOURCE, value, True, 0)
        return value
    
    @property
    def typ(self) -> str:
        """ Тип (например, привелигированная акция) """
        return self.get_string_value(FundsReferent.ATTR_TYPE)
    @typ.setter
    def typ(self, value) -> str:
        self.add_slot(FundsReferent.ATTR_TYPE, value, True, 0)
        return value
    
    @property
    def percent(self) -> float:
        """ Процент от общего количества """
        val = self.get_string_value(FundsReferent.ATTR_PERCENT)
        if (val is None): 
            return 0
        res = NumberHelper.string_to_double(val)
        if (res is None): 
            return 0
        return res
    @percent.setter
    def percent(self, value) -> float:
        if (value > 0): 
            self.add_slot(FundsReferent.ATTR_PERCENT, NumberHelper.double_to_string(value), True, 0)
        else: 
            self.add_slot(FundsReferent.ATTR_PERCENT, None, True, 0)
        return value
    
    @property
    def count(self) -> int:
        """ Количество """
        val = self.get_string_value(FundsReferent.ATTR_COUNT)
        if (val is None): 
            return 0
        wrapv467 = RefOutArgWrapper(0)
        inoutres468 = Utils.tryParseInt(val, wrapv467)
        v = wrapv467.value
        if (not inoutres468): 
            return 0
        return v
    @count.setter
    def count(self, value) -> int:
        self.add_slot(FundsReferent.ATTR_COUNT, str(value), True, 0)
        return value
    
    @property
    def sum0_(self) -> 'MoneyReferent':
        """ Сумма за все акции """
        return Utils.asObjectOrNull(self.get_slot_value(FundsReferent.ATTR_SUM), MoneyReferent)
    @sum0_.setter
    def sum0_(self, value) -> 'MoneyReferent':
        self.add_slot(FundsReferent.ATTR_SUM, value, True, 0)
        return value
    
    @property
    def price(self) -> 'MoneyReferent':
        """ Сумма за одну акцию """
        return Utils.asObjectOrNull(self.get_slot_value(FundsReferent.ATTR_PRICE), MoneyReferent)
    @price.setter
    def price(self, value) -> 'MoneyReferent':
        self.add_slot(FundsReferent.ATTR_PRICE, value, True, 0)
        return value
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
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
    
    def _check_correct(self) -> bool:
        if (self.kind == FundsKind.UNDEFINED): 
            return False
        for s in self.slots: 
            if (s.type_name != FundsReferent.ATTR_TYPE and s.type_name != FundsReferent.ATTR_KIND): 
                return True
        return False