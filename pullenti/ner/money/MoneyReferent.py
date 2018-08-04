# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import math
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.Referent import Referent



class MoneyReferent(Referent):
    """ Представление денежных сумм """
    
    def __init__(self) -> None:
        from pullenti.ner.money.internal.MoneyMeta import MoneyMeta
        super().__init__(MoneyReferent.OBJ_TYPENAME)
        self.instance_of = MoneyMeta.GLOBAL_META
    
    OBJ_TYPENAME = "MONEY"
    
    ATTR_CURRENCY = "CURRENCY"
    
    ATTR_VALUE = "VALUE"
    
    ATTR_ALTVALUE = "ALTVALUE"
    
    ATTR_REST = "REST"
    
    ATTR_ALTREST = "ALTREST"
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = Utils.newStringIO(None)
        v = self.value
        r = self.rest
        if (v > 0 or r > 0): 
            print(v, end="", file=res)
            cou = 0
            for i in range(res.tell() - 1, 0, -1):
                cou += 1
                if ((cou) == 3): 
                    Utils.insertStringIO(res, i, '.')
                    cou = 0
        else: 
            print("?", end="", file=res)
        if (r > 0): 
            print(",{0}".format("{:02d}".format(r)), end="", file=res, flush=True)
        print(" {0}".format(self.currency), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def currency(self) -> str:
        """ Тип валюты (3-х значный код ISO 4217) """
        return self.get_string_value(MoneyReferent.ATTR_CURRENCY)
    
    @currency.setter
    def currency(self, value_) -> str:
        self.add_slot(MoneyReferent.ATTR_CURRENCY, value_, True, 0)
        return value_
    
    @property
    def value(self) -> int:
        """ Значение """
        val = self.get_string_value(MoneyReferent.ATTR_VALUE)
        if (val is None): 
            return 0
        inoutarg1602 = RefOutArgWrapper(0)
        inoutres1603 = Utils.tryParseInt(val, inoutarg1602)
        v = inoutarg1602.value
        if (not inoutres1603): 
            return 0
        return v
    
    @value.setter
    def value(self, value_) -> int:
        self.add_slot(MoneyReferent.ATTR_VALUE, str(value_), True, 0)
        return value_
    
    @property
    def alt_value(self) -> int:
        """ Альтернативное значение (если есть, то значит неправильно написали сумму
         числом и далее прописью в скобках) """
        val = self.get_string_value(MoneyReferent.ATTR_ALTVALUE)
        if (val is None): 
            return None
        inoutarg1604 = RefOutArgWrapper(0)
        inoutres1605 = Utils.tryParseInt(val, inoutarg1604)
        v = inoutarg1604.value
        if (not inoutres1605): 
            return None
        return v
    
    @alt_value.setter
    def alt_value(self, value_) -> int:
        self.add_slot(MoneyReferent.ATTR_ALTVALUE, (None if value_ is None else str(value_)), True, 0)
        return value_
    
    @property
    def rest(self) -> int:
        """ Остаток (от 0 до 99) - копеек, центов и т.п. """
        val = self.get_string_value(MoneyReferent.ATTR_REST)
        if (val is None): 
            return 0
        inoutarg1606 = RefOutArgWrapper(0)
        inoutres1607 = Utils.tryParseInt(val, inoutarg1606)
        v = inoutarg1606.value
        if (not inoutres1607): 
            return 0
        return v
    
    @rest.setter
    def rest(self, value_) -> int:
        if (value_ > 0): 
            self.add_slot(MoneyReferent.ATTR_REST, str(value_), True, 0)
        else: 
            self.add_slot(MoneyReferent.ATTR_REST, None, True, 0)
        return value_
    
    @property
    def alt_rest(self) -> int:
        """ Остаток (от 0 до 99) - копеек, центов и т.п. """
        val = self.get_string_value(MoneyReferent.ATTR_ALTREST)
        if (val is None): 
            return None
        inoutarg1608 = RefOutArgWrapper(0)
        inoutres1609 = Utils.tryParseInt(val, inoutarg1608)
        v = inoutarg1608.value
        if (not inoutres1609): 
            return None
        return v
    
    @alt_rest.setter
    def alt_rest(self, value_) -> int:
        if (value_ is not None and value_ > 0): 
            self.add_slot(MoneyReferent.ATTR_ALTREST, str(value_), True, 0)
        else: 
            self.add_slot(MoneyReferent.ATTR_ALTREST, None, True, 0)
        return value_
    
    @property
    def real_value(self) -> float:
        """ Действительное значение """
        return self.value + ((self.rest / 100))
    
    @real_value.setter
    def real_value(self, value_) -> float:
        self.value = math.floor(value_)
        re = ((value_ - self.value)) * 100
        self.rest = math.floor((re + 0.0001))
        return value_
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        s = (obj if isinstance(obj, MoneyReferent) else None)
        if (s is None): 
            return False
        if (s.currency != self.currency): 
            return False
        if (s.value != self.value): 
            return False
        if (s.rest != self.rest): 
            return False
        if (s.alt_value != self.alt_value): 
            return False
        if (s.alt_rest != self.alt_rest): 
            return False
        return True

    
    @staticmethod
    def _new827(_arg1 : str, _arg2 : float) -> 'MoneyReferent':
        res = MoneyReferent()
        res.currency = _arg1
        res.real_value = _arg2
        return res